#!/usr/bin/env python3
# Lanxin Zhang

from PEP_Vectorized.PEPV import *
from utils import compute_efficacy
import numpy as np



def compute_pe_for_pep_initiation(drug3, dose3, drug3file, t0=-96, ndose=28):
    """
    compute the extinction probability for different start time of PEP. 
    Parameters: 
        drug3: name of the third drug
        dose3: dosage of 3rd drug
        drug3file: file containing the PK parameters for the third drug
        t0: time point at which the computation begins (time before first dose)
        ndose: total doses of 
    return:
    numpy array that contains the extinction probability of single initial virus
    for delay of PEP initiation of 96 - 0 hrs post exposure (1000 virtual 
    inidividuals)
    """
    e = EfficacyPredictor()
    t1 = (ndose + 20) * 24
    r_ftc = Regimen('FTC', 24, (t0, t1), 200, ndose, 1)
    r_tdf = Regimen('TDF', 24, (t0, t1), 300, ndose, 1)
    e.add_regimen(r_ftc)
    e.add_regimen(r_tdf)
    e.add_sample_files('./PEP_Vectorized/Data/ftc_pk.csv')
    e.add_sample_files('./PEP_Vectorized/Data/tdf_pk.csv')
    e.set_pk_ode_solver('TDF', rk4)
    e.set_pk_time_step('TDF', 0.002)
    if drug3: 
        r3 = Regimen(drug3, 24, (t0, t1), dose3, ndose, 1)
        e.add_regimen(r3)
        e.add_sample_files(drug3file)
    e.compute_extinction_probability_fullmodel()
    pe = e.get_extinction_probability()
    return pe[:97*50:50, :, 0, 0, 0].numpy()

def compute_pe_for_pep_duration(drug3, dose3, drug3file, t0=-72):
    """
    compute the extinction probability for different duration of PEP.
    Parameters: 
        drug3: name of the third drug
        dose3: dosage of 3rd drug
        drug3file: file containing the PK parameters for the third drug
        t0: time point at which the computation begins (time before first dose)
    return:
    numpy array that contains the extinction probability of single initial virus 
    for duration 1 - 7 weeks (1000 virtual individuals), PEP initiation of 
    72 - 0 hrs post exposure
    """
    res = None
    for ndose in range(7, 50,2):
        t1 = (ndose + 15) * 24
        e = EfficacyPredictor()
        r = Regimen('FTC', 24, (t0, t1), 200, ndose, 1)
        r1 = Regimen('TDF', 24, (t0,  t1), 300, ndose, 1)
        e.add_regimen(r)
        e.add_regimen(r1)
        e.add_sample_files('./PEP_Vectorized/Data/ftc_pk.csv')
        e.add_sample_files('./PEP_Vectorized/Data/tdf_pk.csv')
        e.set_pk_ode_solver('TDF', rk4)
        e.set_pk_time_step('TDF', 0.002)
        if drug3: 
            r2 = Regimen(drug3, 24, (t0, t1), dose3, ndose, 1)
            e.add_regimen(r2)
            e.add_sample_files(drug3file)
        e.compute_extinction_probability_fullmodel()
        pe = e.get_extinction_probability()
        if res is None:
            res = pe[:72*50:50, :, 0, [0], 0].numpy()
        else:
            res = np.concatenate((res, pe[:72*50:50, :, 0, [0], 0].numpy()), 
                                 axis=2)
    return res


if __name__ == '__main__':
    # compute and save the data of Fig1C TDF/FTC
    pep_initiation_tdf_fct = compute_pe_for_pep_initiation(None, 0, None)
    phi_initiation_tdf_ftc = compute_efficacy(pep_initiation_tdf_fct)
    np.save('fig1c_TDF_FTC', phi_initiation_tdf_ftc)
    
    # compute and save the data of Fig1C TDF/FTC + DTG
    pep_initiation_tdf_fct_dtg = compute_pe_for_pep_initiation('DTG', 50, 
                                                               './PEP_Vectorized/Data/dtg_pk.xlsx')
    phi_initiation_tdf_ftc_dtg = compute_efficacy(pep_initiation_tdf_fct_dtg)
    np.save('fig1c_TDF_FTC_DTG', phi_initiation_tdf_ftc_dtg)
    
    # compute the data of Fig1C TDF/FTC + EFV
    pep_initiation_tdf_fct_efv = compute_pe_for_pep_initiation('EFV', 400, 
                                                               './PEP_Vectorized/Data/efv_pk.csv')
    phi_initiation_tdf_ftc_efv = compute_efficacy(pep_initiation_tdf_fct_efv)
    np.save('fig1c_TDF_FTC_EFV', phi_initiation_tdf_ftc_efv)

    # compute and save the data of Fig1D TDF/FTC
    pep_duration_tdf_ftc = compute_pe_for_pep_duration(None, 0, None)
    phi_duration_tdf_ftc = compute_efficacy(pep_duration_tdf_ftc[24, :, :])
    np.save('fig1d_TDF_FTC', phi_duration_tdf_ftc)

    # compute and save the data of Fig1D TDF/FTC + DTG
    pep_duration_tdf_ftc_dtg = compute_pe_for_pep_duration('DTG', 50, 
                                                       './PEP_Vectorized/Data/dtg_pk.xlsx')
    phi_duration_tdf_ftc_dtg = compute_efficacy(pep_duration_tdf_ftc_dtg[24, :, :])
    np.save('fig1d_TDF_FTC_DTG', phi_duration_tdf_ftc_dtg)

    # compute and save the data of Fig1D TDF/FTC
    pep_duration_tdf_ftc_efv = compute_pe_for_pep_duration('EFV', 400, 
                                                       './PEP_Vectorized/Data/efv_pk.csv')
    phi_duration_tdf_ftc_efv = compute_efficacy(pep_duration_tdf_ftc_efv[24, :, :])
    np.save('fig1d_TDF_FTC', phi_duration_tdf_ftc_efv)

    print('Done')


    
