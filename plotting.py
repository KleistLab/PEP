#!/usr/bin/env python3
# Lanxin Zhang

import os
import sys
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import argparse

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=11)

def plot_fig1():
    # read the efficacy data
    fig1c_truvada = np.load('./data/Fig1/fig1c_TDF_FTC.npy')
    fig1c_truvdtg = np.load('./data/Fig1/fig1c_TDF_FTC_DTG.npy')
    fig1c_truvefv = np.load('./data/Fig1/fig1c_TDF_FTC_EFV.npy')

    fig1d_truvada = np.load('./data/Fig1/fig1d_TDF_FTC.npy')
    fig1d_truvdtg = np.load('./data/Fig1/fig1d_TDF_FTC_DTG.npy')
    fig1d_truvefv = np.load('./data/Fig1/fig1d_TDF_FTC_EFV.npy')

    cm = 1/2.54
    fig, axes = plt.subplots(1, 2, figsize=[18*cm, 8*cm])
    plt.subplots_adjust(top=0.95, bottom=0.3, wspace=0.4, hspace=0.5)
    for i in range(2):
        right_side = axes[i].spines["right"]
        right_side.set_visible(False)
        right_side = axes[i].spines["top"]
        right_side.set_visible(False)


    # define a function to plot the efficacy trajectory for 
    # 1000 virtual individuals
    def plot_1000(t, phi, color, label, ax, axis=1):
        q = [0.025, 0.25, 0.5, 0.75, 0.975]
        quan = np.quantile(phi, q, axis=axis)
        p_50 = quan[2,:]
        p_2_5 = quan[0,:]
        p_25 = quan[1,:]
        p_75 = quan[3,:]
        p_97 = quan[4,:]
        ax.plot(np.array(t), p_50, lw=1, c=color, label=label)
        ax.fill_between(np.array(t), p_2_5, p_97, color='lightgray')
        ax.fill_between(np.array(t), p_25, p_75, color='gray')

    # Fig1C
    t = [i for i in range(97)][::-1]
    axes[0].set_xlabel('Delay of PEP initiation after exposure [hr]')
    axes[0].set_ylabel('PEP efficacy [$\%$]')
    plot_1000(t, fig1c_truvada * 100, 'orangered', 'TDF/FTC', axes[0])
    plot_1000(t, fig1c_truvdtg * 100, 'limegreen', 'TDF/FTC+DTG', axes[0])
    plot_1000(t, fig1c_truvefv* 100, 'dodgerblue', 'TDF/FTC+EFV', axes[0])
    axes[0].set_xlim([0, 90])
    axes[0].set_ylim([0, 105])
    # mark 90% efficacy
    axes[0].set_xticks([i*20 for i in range(5)])
    axes[0].plot(t, [90]*97, '--', color='black')

    # Fig1D
    duration = [i/7 for i in range(7, 50, 2)]
    plot_1000(duration, fig1d_truvada * 100, 'orangered', 
              'TDF/FTC', axes[1], axis=0)
    plot_1000(duration, fig1d_truvdtg * 100, 'limegreen', 
              'TDF/FTC+DTG', axes[1], axis=0)
    plot_1000(duration, fig1d_truvefv * 100, 'dodgerblue', 
              'TDF/FTC+EFV', axes[1], axis=0)
    axes[1].set_xticks([i for i in range(1, 8)])
    axes[1].set_xlim([1, 7])
    axes[1].set_ylim([0, 105])
    axes[1].set_xlabel('Duration of PEP [wk]')
    axes[1].set_ylabel('PEP efficacy [$\%$]')
    # mark 90% efficacy
    axes[1].plot(duration, [90]*22, '--', color='black')
    # plot legend for both subplots
    axes[1].legend(loc='upper center', bbox_to_anchor=(-0.3, -0.3),
            fancybox=True, shadow=True, ncol=5)
    plt.savefig('fig1.svg', format='svg')


def plot_fig2():
    fig2b = pd.read_csv('./data/Fig2/fig2b.csv', index_col=0)
    fig2c = pd.read_csv('./data/Fig2/fig2c.csv', index_col=0)
    fig2d = pd.read_csv('./data/Fig2/fig2d.csv', index_col=0)
    fig2e = pd.read_csv('./data/Fig2/fig2e.csv', index_col=0)
    # change the index of rows
    fig2b.index = [0, 1,2,3,4,5,6,7, 'no 3rd\n drug']
    fig2c.index = [0, 1,2,3,4,5,6,7, 'no 3rd\n drug']
    fig2d.index = [0, 1,2,3,4,5,6,7, 'no 3rd\n drug']
    fig2e.index = [0, 1,2,3,4,5,6,7, 'no 3rd\n drug']

    cm = 1/2.54
    fig, axes = plt.subplots(2,2,figsize=[16*cm, 16*cm])
    plt.subplots_adjust(top=0.95, bottom=0.2, wspace=0.5, hspace=0.5)
    # add an axis for legend
    cbar_ax = fig.add_axes([.2, 0.08, .6, .03])
    # Fig2B
    g1 = sns.heatmap(fig2b*100,cmap='BuPu_r', ax=axes[0,0], 
                     vmin=20, vmax=100, cbar=True, cbar_ax=cbar_ax, 
                     linewidths=0.5, linecolor='whitesmoke', clip_on=False, 
                     cbar_kws={'ticks':[i*10 for i in range(11)], 
                               'label':'PEP efficacy [$\%$]', 
                               'orientation': 'horizontal'})
    g1.set_xlabel('Delayed initiation of Truvada [hr]')
    g1.set_ylabel('Delay of third drug [day]')
    g1.set_title('TDF/FTC+DTG')

    # Fig2C
    g2 = sns.heatmap(fig2c*100,cmap='BuPu_r', cbar=False,ax=axes[0,1],
                     vmin=20, vmax=100, cbar_ax=None, linewidths=0.5, 
                     linecolor='whitesmoke', clip_on=False)
    g2.set_title('TDF/FTC+EFV')
    g2.set_ylabel('Delay of third drug [day]')
    g2.set_xlabel('Delayed initiation of Truvada [hr]')
    
    # Fig2D
    g3 = sns.heatmap(fig2d*100,cmap='BuPu_r', cbar=False,ax=axes[1,0], 
                     vmin=20, vmax=100, cbar_ax=None, linewidths=0.5, 
                     linecolor='whitesmoke', clip_on=False)
    g3.set_ylabel('Delay of third drug [day]')
    g3.set_xlabel('Delayed initiation of Truvada [hr]')

    # Fig2E
    g4 = sns.heatmap(fig2e*100,cmap='BuPu_r', cbar=False, ax=axes[1,1], 
                     vmin=20, vmax=100,cbar_ax=None, linewidths=0.5, 
                     linecolor='whitesmoke', clip_on=False)
    g4.set_xlabel('Delayed initiation of Truvada [hr]')
    g4.set_ylabel('Delay of third drug [day]')
    fig.savefig('fig2.svg', format='svg')


def plot_fig3():
    # read efficacy data 
    fig3b_truvada = np.load('./data/Fig3/fig3b_TDF_FTC.npy')
    fig3b_truvdtg = np.load('./data/Fig3/fig3b_TDF_FTC_DTG.npy')
    fig3b_truvefv = np.load('./data/Fig3/fig3b_TDF_FTC_EFV.npy')

    fig3c_truvada = np.load('./data/Fig3/fig3c_TDF_FTC.npy')
    fig3c_truvdtg = np.load('./data/Fig3/fig3c_TDF_FTC_DTG.npy')
    fig3c_truvefv = np.load('./data/Fig3/fig3c_TDF_FTC_EFV.npy')

    fig3d_truvada = np.load('./data/Fig3/fig3d_TDF_FTC.npy')
    fig3d_truvdtg = np.load('./data/Fig3/fig3d_TDF_FTC_DTG.npy')
    fig3d_truvefv = np.load('./data/Fig3/fig3d_TDF_FTC_EFV.npy')

    fig3e_truvada = np.load('./data/Fig3/fig3e_TDF_FTC.npy')
    fig3e_truvdtg = np.load('./data/Fig3/fig3e_TDF_FTC_DTG.npy')
    fig3e_truvefv = np.load('./data/Fig3/fig3e_TDF_FTC_EFV.npy')

    fig3f_truvada = np.load('./data/Fig3/fig3f_TDF_FTC.npy')
    fig3f_truvdtg = np.load('./data/Fig3/fig3f_TDF_FTC_DTG.npy')
    fig3f_truvefv = np.load('./data/Fig3/fig3f_TDF_FTC_EFV.npy')

    fig3g_truvada = np.load('./data/Fig3/fig3g_TDF_FTC.npy')
    fig3g_truvdtg = np.load('./data/Fig3/fig3g_TDF_FTC_DTG.npy')
    fig3g_truvefv = np.load('./data/Fig3/fig3g_TDF_FTC_EFV.npy')

    fig3h_truvada = np.load('./data/Fig3/fig3h_TDF_FTC.npy')
    fig3h_truvdtg = np.load('./data/Fig3/fig3h_TDF_FTC_DTG.npy')
    fig3h_truvefv = np.load('./data/Fig3/fig3h_TDF_FTC_EFV.npy')

    fig3i_truvada = np.load('./data/Fig3/fig3i_TDF_FTC.npy')
    fig3i_truvdtg = np.load('./data/Fig3/fig3i_TDF_FTC_DTG.npy')
    fig3i_truvefv = np.load('./data/Fig3/fig3i_TDF_FTC_EFV.npy')

    cm = 1/2.54
    fig, axes = plt.subplots(2, 4, figsize=[18*cm, 10*cm])
    plt.subplots_adjust(top=0.95, bottom=0.2, left=0.1, right=0.95, 
                        wspace=0.3, hspace=0.3)
    for i in range(2):
        for j in range(4):
            right_side = axes[i,j].spines["right"]
            right_side.set_visible(False)
            right_side = axes[i,j].spines["top"]
            right_side.set_visible(False)
        
    def plot_1000(ax, t, phi, color, label):
        q = [0.025, 0.25, 0.5, 0.75, 0.975]
        quan = np.quantile(phi, q, axis=1)
        p_50 = quan[2,:]
        p_25 = quan[1,:]
        p_75 = quan[3,:]
        ax.plot(np.array(t), p_50, lw=1.3, c=color, label=label)
        ax.fill_between(np.array(t), p_25, p_75, color=color+[0.2])

    plot_1000(axes[0,0], [i*4 for i in range(19)], fig3b_truvada*100, 
              [1, 69/255, 0], 'TDF/FTC')
    plot_1000(axes[0,0], [i*4 for i in range(19)], fig3b_truvdtg*100, 
              [0.2, 0.8, 0.4], 'TDF/FTC+DTG')
    plot_1000(axes[0,0], [i*4 for i in range(19)], fig3b_truvefv*100, 
              [30/255, 144/255, 1], 'TDF/FTC+EFV')
    axes[0,0].set_xticks([i*24 for i in range(4)])
    axes[0,0].set_xlim(0, 72)
    axes[0,0].set_ylim(0, 101)
    axes[0,0].set_ylabel('PEP efficacy ($\%$)')

    plot_1000(axes[0,1], [i*4 for i in range(19)], fig3c_truvada*100, 
              [1, 69/255, 0], 'TDF/FTC')
    plot_1000(axes[0,1], [i*4 for i in range(19)], fig3c_truvdtg*100, 
              [0.2, 0.8, 0.4], 'TDF/FTC+DTG')
    plot_1000(axes[0,1], [i*4 for i in range(19)], fig3c_truvefv*100, 
              [30/255, 144/255, 1], 'TDF/FTC+EFV')
    axes[0,1].set_xticks([i*24 for i in range(4)])
    axes[0,1].set_xlim(0, 72)
    axes[0,1].set_ylim(0, 101)

    plot_1000(axes[0,2], [i*4 for i in range(19)], fig3d_truvada*100, 
              [1, 69/255, 0], 'TDF/FTC')
    plot_1000(axes[0,2], [i*4 for i in range(19)], fig3d_truvdtg*100, 
              [0.2, 0.8, 0.4], 'TDF/FTC+DTG')
    plot_1000(axes[0,2], [i*4 for i in range(8)]+[i*4 for i in range(9, 19)], 
              fig3d_truvefv*100, [30/255, 144/255, 1], 'TDF/FTC+EFV')
    axes[0,2].set_xticks([i*24 for i in range(4)])
    axes[0,2].set_xlim(0, 72)
    axes[0,2].set_ylim(0, 101)

    plot_1000(axes[0,3], [i for i in range(72)], fig3e_truvada*100, 
              [1, 69/255, 0], 'TDF/FTC')
    plot_1000(axes[0,3], [i for i in range(72)], fig3e_truvdtg*100, 
              [0.2, 0.8, 0.4], 'TDF/FTC+DTG')
    plot_1000(axes[0,3], [i for i in range(72)], fig3e_truvefv*100, 
              [30/255, 144/255, 1], 'TDF/FTC+EFV')
    axes[0,3].set_xticks([i*24 for i in range(4)])
    axes[0,3].set_xlim(0, 72)
    axes[0,3].set_ylim(0, 101)

    plot_1000(axes[1,0], [i*4 for i in range(19)], fig3f_truvada*100, 
              [1, 69/255, 0], 'TDF/FTC')
    plot_1000(axes[1,0], [i*4 for i in range(19)], fig3f_truvdtg*100, 
              [0.2, 0.8, 0.4], 'TDF/FTC+DTG')
    plot_1000(axes[1,0], [i*4 for i in range(19)], fig3f_truvefv*100, 
              [30/255, 144/255, 1], 'TDF/FTC+EFV')
    axes[1,0].set_xticks([i*24 for i in range(4)])
    axes[1,0].set_xlim(0, 72)
    axes[1,0].set_ylim(0, 101)
    axes[1,0].set_ylabel('PEP efficacy ($\%$)')

    plot_1000(axes[1,1], [i*4 for i in range(19)], fig3g_truvada*100, 
              [1, 69/255, 0], 'TDF/FTC')
    plot_1000(axes[1,1], [i*4 for i in range(19)], fig3g_truvdtg*100, 
              [0.2, 0.8, 0.4], 'TDF/FTC+DTG')
    plot_1000(axes[1,1], [i*4 for i in range(19)], fig3g_truvefv*100, 
              [30/255, 144/255, 1], 'TDF/FTC+EFV')
    axes[1,1].set_xticks([i*24 for i in range(4)])
    axes[1,1].set_xlim(0, 72)
    axes[1,1].set_ylim(0, 101)
    axes[1,1].set_xlabel('Time of PEP initiation post exposure (hr)')

    plot_1000(axes[1,2], [i*4 for i in range(19)], fig3h_truvada*100, 
              [1, 69/255, 0], 'TDF/FTC')
    plot_1000(axes[1,2], [i*4 for i in range(19)], fig3h_truvdtg*100,
               [0.2, 0.8, 0.4], 'TDF/FTC+DTG')
    plot_1000(axes[1,2], [i*4 for i in range(8)]+[i*4 for i in range(9, 19)],
              fig3h_truvefv*100, [30/255, 144/255, 1], 'TDF/FTC+EFV')
    axes[1,2].set_xticks([i*24 for i in range(4)])
    axes[1,2].set_xlim(0, 72)
    axes[1,2].set_ylim(0, 101)

    plot_1000(axes[1,3], [i for i in range(72)], fig3i_truvada*100, 
              [1, 69/255, 0], 'TDF/FTC')
    plot_1000(axes[1,3], [i for i in range(72)], fig3i_truvdtg*100, 
              [0.2, 0.8, 0.4], 'TDF/FTC+DTG')
    plot_1000(axes[1,3], [i for i in range(72)], fig3i_truvefv*100, 
              [30/255, 144/255, 1], 'TDF/FTC+EFV')
    axes[1,3].set_xticks([i*24 for i in range(4)])
    axes[1,3].set_xlim(0, 72)
    axes[1,3].set_ylim(0, 101)

    axes[1, 1].legend(loc='upper center', bbox_to_anchor=(1, -0.3),
            fancybox=True, shadow=True, ncol=5)
    plt.savefig('fig3.svg', format='svg')


def plot_fig4_5(data2='./data/Fig4/fig4b.pkl', data3='./data/Fig4/fig4c.pkl', 
                data7='./data/Fig4/fig4d.pkl', figname='fig4'):
    data2 = pd.read_pickle(data2, 
                           compression={'method': 'zip', 'compresslevel': 1})
    data3 = pd.read_pickle(data3, 
                           compression={'method': 'zip', 'compresslevel': 1})
    data7 = pd.read_pickle(data7, 
                           compression={'method': 'zip', 'compresslevel': 1})
    cm = 1/2.54
    fig, axes = plt.subplots(1, 3, figsize=[30*cm, 10*cm])
    plt.subplots_adjust(top=0.95, bottom=0.25, left=0.1, right=0.95, 
                        wspace=0.2, hspace=0.1)
    for i in range(3):
        right_side = axes[i].spines["right"]
        right_side.set_visible(False)
        right_side = axes[i].spines["top"]
        right_side.set_visible(False)
    my_pal = {"TDF/FTC": [230/255, 128/255, 128/255], 
              "TDF/FTC+DTG": [73/255, 210/255, 118/255], 
              "TDF/FTC+EFV":[76/255, 178/255, 230/255], 'no PEP':[1,1,1]}
    sns.boxplot(ax=axes[0], data=data2, x='Dose per week', 
                y='Prophylactic efficacy', hue='Drug',orient='v', 
                whis=[2.5, 97.5], showfliers=False, width=0.9, palette=my_pal)
    sns.boxplot(ax=axes[1], data=data3, x='Dose per week', 
                y='Prophylactic efficacy', hue='Drug',orient='v', 
                whis=[2.5, 97.5], showfliers=False, width=0.9, palette=my_pal)
    sns.boxplot(ax=axes[2], data=data7, x='Dose per week', 
                y='Prophylactic efficacy', hue='Drug',orient='v', 
                whis=[2.5, 97.5], showfliers=False, width=0.9, palette=my_pal)

    for ax in axes:
        ax.set_ylim(-1, 102)
        ax.plot([-0.5, 7.5], [50, 50], '--', c='maroon')
        ax.plot([-0.5, 7.5], [90, 90], '--', c='black')
        ax.set_xlabel('Adherence to PrEP (dose per week)')
        ax.set_ylabel('Prophylactic efficacy [$\%$]')


    axes[0].legend([],[], frameon=False)
    axes[2].legend([],[], frameon=False)
    axes[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
            fancybox=True, shadow=True, ncol=5)
    plt.savefig('{}.svg'.format(figname), format='svg')    

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--figure', type=int, default=1,
                        help='choose the figure you want to plot')
    arg = parser.parse_args()
    if arg.figure == 1:
        plot_fig1()
    elif arg.figure == 2:
        plot_fig2()
    elif arg.figure == 3:
        plot_fig3()
    elif arg.figure == 4:
        plot_fig4_5()
    elif arg.figure == 5: 
        plot_fig4_5(data2='./data/Fig5/fig5c.pkl', 
                    data3='./data/Fig5/fig5d.pkl', 
                    data7='./data/Fig5/fig5e.pkl', figname='fig5')
    else:
        print('No corresponding figure. Please give a number in range 1-5.')
    print('Done')
