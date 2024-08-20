#!/usr/bin/env python3
# Lanxin Zhang

from PEP_Vectorized.PEPV import *
from utils import compute_efficacy
import sys
import numpy as np
import pandas as pd
import argparse

def run_prep_pep_decaying_adherence(adhs = [1/7, 2/7, 3/7, 4/7, 5/7, 6/7, 7/7], drug3=None):
    """
    compute the extinction probability of PEP with declining adherence,  
    following 30-days PrEP with different adherence level. The time between 
    last PrEP dose and viral exposure is 48 hr, and the time between exposure 
    and PEP initiation is 2days, 3days and 7 days, respectively.  
    Return:
    Dictionary that contains the extinction probability profiles of 1000 virtual
    individuals for 7 different PrEP adherence levels, for PEP initialized 2days,
    3days and 7days post exposure.
    """
    res = dict()
    t0 = 0

    def generate_pep_dosing_pattern(dose):
        # generate a decaying dosing pattern for PEP
        dosing_pattern = np.array([])
        f = lambda x, a, b: 0.5 * (1 + np.tanh(a*(b-x)))  # adherence function of PEP
        a = np.random.uniform(0.5, 1.5, 1)
        b = np.random.uniform(5, 10, 1)
        for i in range(dose):
            adh = f(i, a, b)
            dosing_pattern = np.append(dosing_pattern, np.random.binomial(1, adh, 1))
        return dosing_pattern
    
    # define a function to compute the extinction probability for one PrEP 
    # adherence, one PEP dosing regimen and one gap between exposure and 
    # PEP initiation.
    def compute_pe_for_one(texp, adh):
        t1 = (20 + texp + 30 + 15) * 24
        pep_pattern = generate_pep_dosing_pattern(28)
        # 48 hrs between PrEP and exposure
        gap = [0] + [0] * texp
        pattern = np.concatenate((np.where(adh > np.random.rand(30), 1, 0), gap, pep_pattern))
        adh_pattern = pattern[np.newaxis, :]
        # dosing pattern of 3rd drug
        pattern1 = np.concatenate((np.zeros((30,)), gap, pep_pattern))[np.newaxis, :]
        e = EfficacyPredictor()
        r = Regimen('FTC', 24, (t0, t1), 200, 1, 1, adh_pattern=adh_pattern)
        r1 = Regimen('TDF', 24, (t0, t1), 300, 1, 1, adh_pattern=adh_pattern)
        r2 = Regimen('DTG', 24, (t0,  t1), 50, 1, 1, adh_pattern=pattern1)
        r3 = Regimen('EFV', 24, (t0,  t1), 400, 1, 1, adh_pattern=pattern1)

        e.add_regimen(r)
        e.add_regimen(r1)
        e.add_sample_files('./PEP_Vectorized/Data/ftc_pk.csv')
        e.add_sample_files('./PEP_Vectorized/Data/tdf_pk.csv')
        e.set_pk_ode_solver('TDF', rk4)
        e.set_pk_time_step('TDF', 0.002)

        if drug3 == 'DTG':
            e.add_regimen(r2)
            e.add_sample_files('./PEP_Vectorized/Data/dtg_pk.xlsx')
        elif drug3 == 'EFV':
            e.add_regimen(r3)
            e.add_sample_files('./PEP_Vectorized/Data/efv_pk.csv')

        e.compute_extinction_probability_fullmodel()
        pe = e.get_extinction_probability()
        return pe[31*24*50,:, 0,0,0].numpy().copy()

    
    for texp in [2,3, 7]:
        res[texp] = dict()
        for idx, adh in enumerate(adhs):
            tmp = compute_pe_for_one(texp, adh)
            res[texp][idx+1] = tmp
    return res
    


def main(itr_index):
    parser = argparse.ArgumentParser()
    parser.add_argument('--repeat', type=int, default=1, help='Iteration number\
                         to repeat the computation')
    parser.add_argument('--drug3', type=str.upper, default='', 
                        help='Third drug except for TDF and FTC, options are \
                        DTG and EFV')
    args = parser.parse_args()
    if args.drug3:
        if args.drug3 not in ['DTG', 'EFV']:
            sys.stderr.write('Drug not available. Valid option: DTG and EFV')
            sys.exit
    for i in range(args.repeat):
        pe = run_prep_pep_decaying_adherence(drug3=args.drug3)
        for texp in [2,3,7]:
            phi = compute_efficacy(pd.DataFrame(pe[texp]))
            phi.to_csv('fig5_TDF_FTC_{}_gap{}_{}.csv'
                                          .format(args.drug3, texp, i))

