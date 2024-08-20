#!/usr/bin/env python3
# Lanxin Zhang

from scipy import special
from PEP_Vectorized.PEPV import *
import warnings

def compute_inoculum_distribution(mode='rvi'):
    """
    compute the probability distribution of inoculum size according to 
    exposure route. Available exposure routes are 
    receptive anal intercourse (RAI) and receptive vaginal intercourse (RVI).
    By default the inoculum for RVI will be computed.
    The virus exposure model is adopted form doi:10.1002/psp4.12095.
    Return:
    am array containing the probability of inoculum size in range(0, 100)
    """
    # parameters in virus exposure model 
    mu = 4.51
    sigma = 0.98
    m = 0.3892

    # cumulative density function of log-normal distribution, x = VL^m
    def cdf(x):
        return (1 + special.erf((np.log10(x ** (1/m)) - mu)/
                                (2 ** 0.5 * sigma))) / 2

    # VL: define an upper bound for VL^m
    # v0: upper bound for v0
    # compute distribution in vectorized way
    def p_v0(r, vl=20000, v0=100):
        # an array containing every possible entry of VL^m
        vl_array = np.arange(1, vl)    
        # # an array containing every possible entry of v0
        v0_array = np.arange(0, v0)    
        g_array = cdf(vl_array) - cdf(vl_array-1)    
        # row_mat: each row is v0_array, col_mat: each column is vl_array
        row_mat, col_mat = np.meshgrid(v0_array, vl_array) 
        # probability of binomial distribution
        binomial_matrix = special.comb(col_mat, row_mat) * (r ** row_mat) * \
                          ((1 - r) ** (col_mat - row_mat))
        # matrix multiplication
        return np.matmul(g_array, binomial_matrix)

    # success rate for different exposure
    r = 9.1e-5 if mode == 'rai' else 3.7136e-3 
    warnings.filterwarnings('ignore')
    return p_v0(r)


def compute_efficacy(pe, mode='rvi'):
    """
    Compute the prophylactic efficacy for a given extinction probability array, 
    for the given exposure route.
    Return:
    array of prophylactic efficacy
    """
    # compute the extinction probability (PE0) without any ART
    t0 = -24 * 2
    t1 = 24 * 20
    ndose = 28
    r0 = Regimen('EFV', 24, (t0, t1), 0, ndose, 1) 
    e_0 = EfficacyPredictor()
    e_0.add_regimen(r0)
    e_0.compute_extinction_probability_fullmodel()
    res_0 = e_0.get_extinction_probability()
    pe_0 = float(res_0[0,0,0,0,0])
    # probability distribution of inoculum
    p_virus = compute_inoculum_distribution(mode)
    # calculte the averge extinction probability based on inoculum size
    def calculate_average_extinction_probability(pe):
        res = 0
        for v, p in enumerate(p_virus):
            res += p * pe ** v 
        return res
    pe0_average = calculate_average_extinction_probability(pe_0)
    pe_average = calculate_average_extinction_probability(pe)
    phi = 1 - (1 - pe_average) / (1 - pe0_average)
    return phi