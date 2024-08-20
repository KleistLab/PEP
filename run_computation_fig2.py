#!/usr/bin/env python3
# Lanxin Zhang

from PEP_Vectorized.PEPV import *
from utils import compute_efficacy
import pandas as pd


def compute_pe_delayed_3rd_drug(dose=14, drug3='DTG', dosage3=50):
    """
    Compute the extinction probability: TDF/FTC as basic PEP, third drug 
    (DTG or EFV) will be initiated later after the initiation of TDF/FTC. 
    Parameters: 
        dose: doses of TDF/FTC; 
        drug3: name of the third drug; 
        dosage3: dosage of 3rd drug
    Return:
        dictionary of extinction probability for the initiation of TDF/FTC in 
        1 - 48 hr post exposure, then the third drug initiated 1 - 7 days after 
        initiation of TDF/FTC.
    """
    t0_list = [-1, -3, -6, -12, -24, -36, -48]
    res_dict = dict()
    for t0 in t0_list:
        t1 = (dose + 25) * 24
        r_tdf = Regimen('TDF', 24, (t0, t1), 300, dose, 1)
        r_ftc = Regimen('FTC', 24, (t0, t1), 200, dose, 1)
        res_dict[t0] = dict()
        for t in range(0, 8):
            t0_delayed = t0 - t * 24
            r_drug3 = Regimen(drug3, 24, (t0_delayed, t1-t*24), dosage3, dose-t, 1)
            e = EfficacyPredictor()
            e.add_regimen(r_tdf)
            e.add_regimen(r_ftc)
            e.add_regimen(r_drug3)
            e.compute_extinction_probability_fullmodel()
            pe = e.get_extinction_probability()
            res_dict[t0][t] = pe[0,0,0,0,0]
    return res_dict


if __name__ == '__main__':
    # compute the data for Fig2
    df_dtg_14 = pd.DataFrame(compute_pe_delayed_3rd_drug(), dtype=float)
    df_dtg_28 = pd.DataFrame(compute_pe_delayed_3rd_drug(dose=28), dtype=float)
    df_efv_14 = pd.DataFrame(compute_pe_delayed_3rd_drug(drug3='EFV', 
                                                         dosage3=400), dtype=float)
    df_efv_28 = pd.DataFrame(compute_pe_delayed_3rd_drug(dose=28, drug3='EFV', 
                                                         dosage3=400), dtype=float)
    df_efv_14.to_csv('test.csv')
    # compute efficacy
    phi_dtg_14 = compute_efficacy(df_dtg_14)
    phi_dtg_28 = compute_efficacy(df_dtg_28)
    phi_efv_14 = compute_efficacy(df_efv_14)
    phi_efv_28 = compute_efficacy(df_efv_28)
    # save the data 
    phi_dtg_14.to_csv('fig2b.csv')
    phi_efv_14.to_csv('fig2c.csv')
    phi_dtg_28.to_csv('fig2d.csv')
    phi_efv_28.to_csv('fig2e.csv')

    print('Done')





