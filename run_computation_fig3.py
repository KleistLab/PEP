#!/usr/bin/env python3
# Lanxin Zhang

from PEP_Vectorized.PEPV import *
from utils import compute_efficacy
import numpy as np
import os
import argparse
import sys

# to avoid the printed messages when running repetitive computation 
class HiddenPrints:
    def __enter__(self):
        self._jupyter_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._jupyter_stdout


def compute_pep_initiation_ondemand_PrEP(gap, drug3, exposure=48, duration=7):
    """
    compute the extinction probability for PEP following on-demand PrEP
    Parameters: 
        gap: time between viral exposure and initiation of PEP (multiples of 4, 
        e.g. gap=1 is equal to 4hrs between exposure and PEP)
        drug3: name of the third drug
        exposure: time between last dose of PrEP and viral exposure (hr)
        duration: duration of PEP
    """
    t0 = 0
    t1 = (duration + 20) * 24
    p = [[2]+[0] * 5 + [1]+[0]*5 + [1]+[0]*5 + [0]*(exposure//4) + [0]*gap + 
         ([1]+[0]*5) * duration]
    p1 = [[0]*18 + [0]*(exposure//4) + [0]*gap + ([1]+[0]*5) * duration]
    r_ftc = Regimen('FTC', 4, (t0, t1), 200, 1, 1, adh_pattern=p)
    r_tdf = Regimen('TDF', 4, (t0, t1), 300, 1, 1, adh_pattern=p)
    r_efv = Regimen('EFV', 4, (t0,  t1), 400, 1, 1, adh_pattern=p1)
    r_dtg = Regimen('DTG', 4, (t0,  t1), 50, 1, 1, adh_pattern=p1)
    e = EfficacyPredictor()
    e.add_regimen(r_ftc)
    e.add_regimen(r_tdf)
    e.add_sample_files('./PEP_Vectorized/Data/ftc_pk.csv')
    e.add_sample_files('./PEP_Vectorized/Data/tdf_pk.csv')
    e.set_pk_ode_solver('TDF', rk4)
    e.set_pk_time_step('TDF', 0.002)
    if drug3 == 'DTG':
        e.add_regimen(r_dtg)
        e.add_sample_files('./PEP_Vectorized/Data/dtg_pk.xlsx')
    elif drug3 == 'EFV':
        e.add_regimen(r_efv)
        e.add_sample_files('./PEP_Vectorized/Data/efv_pk.csv')
    e.compute_extinction_probability_fullmodel()
    pe = e.get_extinction_probability()
    return pe[[24*(3+exposure//24)*50],:, 0,0,0].numpy()


def compute_pep_baseline_noprep(drug3=None, duration=7):
    """
    Compute the extinction probability for the baseline scenario without PrEP 

    """
    t0 = -72
    t1 = (duration+15) * 24
    r_ftc = Regimen('FTC', 24, (t0, t1), 200, duration, 1)
    r_tdf = Regimen('TDF', 24, (t0, t1), 300, duration, 1)
    r_efv = Regimen('EFV', 24, (t0,  t1), 400, duration, 1)
    r_dtg = Regimen('DTG', 24, (t0,  t1), 50, duration, 1)
    e = EfficacyPredictor()
    e.add_regimen(r_ftc)
    e.add_regimen(r_tdf)
    e.add_sample_files('./PEP_Vectorized/Data/ftc_pk.csv')
    e.add_sample_files('./PEP_Vectorized/Data/tdf_pk.csv')
    e.set_pk_ode_solver('TDF', rk4)
    e.set_pk_time_step('TDF', 0.002)
    if drug3 == 'DTG':
        e.add_regimen(r_dtg)
        e.add_sample_files('./PEP_Vectorized/Data/dtg_pk.xlsx')
    elif drug3 == 'EFV':
        e.add_regimen(r_efv)
        e.add_sample_files('./PEP_Vectorized/Data/efv_pk.csv')
    e.compute_extinction_probability_fullmodel()
    pe = e.get_extinction_probability()
    return pe


if __name__ == '__main__':
    def str2bool(v):
        # def a boolean type for argparse
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--exposure', type=int, default=48,
                        help='Time between last dose of PrEP and viral exposure\
                            (hr)')
    parser.add_argument('--drug3', type=str.upper, default='',
                        help='Third drug in addition to TDF and FTC, options are \
                            DTG and EFV')
    parser.add_argument('--duration', type=int, default=7,
                        help='Duration of PEP in days')
    parser.add_argument('--ifPrEP', type=str2bool, default=True,
                        help='Indicate if on-demand PrEP is used')
    arg = parser.parse_args()
    if arg.ifPrEP:
        if arg.drug3:
            if arg.drug3 not in ['DTG', 'EFV']:
                sys.stderr.write('Drug not available. Valid option: DTG and EFV')
                sys.exit
        res = None
        for gap in range(19):
            tmp = compute_pep_initiation_ondemand_PrEP(gap, drug3=arg.drug3, 
                                                       exposure=arg.exposure,
                                                       duration=arg.duration)
            if res is None:
                res = tmp
            else:
                res = np.concatenate((res, tmp), axis=0)

        phi = compute_efficacy(res)
        np.save('fig3_TDF_FTC_{}_{}_{}d'.format(arg.drug3, arg.exposure, 
                                                   arg.duration), phi)
    else:
        pe = compute_pep_baseline_noprep(arg.drug3, arg.duration)
        phi = compute_efficacy(pe)
        np.save('fig3_noPrEP_TDF_FTC_{}_{}d'.format(arg.drug3, arg.duration), phi)
        