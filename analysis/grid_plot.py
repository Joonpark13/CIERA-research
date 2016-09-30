import os
import subprocess
import init_parse as ip
import plot_script as ps
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from operator import add
from operator import sub
import math
import inspiral

def _get_grid():
    """
    Gathers all of the short files in the current directory and returns a list of the unique suffixes (generally the reference to each simulation)
    """
    data_files = subprocess.Popen('ls *.short*', shell=True, stdout=subprocess.PIPE)
    stdout, stderr = data_files.communicate()
    stdout = stdout.split()
    sim_list = []
    for file in stdout:
        split_file = file.split('short')
        sim_list.append(split_file[1])
    sim_list = list(set(sim_list))
    sim_set = set()
    for sim in sim_list:
        sim_type = sim.split('_')[:-1]
        sim_name = ''
        for item in sim_type:
            sim_name = sim_name + item + '_'
        sim_set.add((sim_name[:-1]))
    sim_set = list(sim_set)
    return sim_set

def grid_bh_count(saveLocation='', grid=[], num_bins=0):
    """
    Gathers and plots a count of black holes over time for an entire grid.
    Bins the data for groups of simulations with the same initial conditions (e.g. 'N10K_r10_Z01_1' and 'N10K_r10_Z01_2', etc)
    saveLocation designates where to save the plots
    Grid allows the user to pass a list of simulations to include. Will run _get_grid() otherwise.
    num_bins specifies the number of bins to use for each set of initial conditions. Will place approx. 5 data points per bin otherwise
    Calls _get_grid(), ps.blackHoleOverTime()
    """
    plt.close('all')
    if grid == []:
        grid = _get_grid()
    plt.figure(1)
    plt.figure(2)
    plt.figure(3)
    legend = []
    for sim_type in grid:
        legend.append(sim_type)
        sim_type_list = subprocess.Popen('ls *short{0}*'.format(sim_type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_type_list.communicate()
        stdout = stdout.split()
        times = []
        sBH = []
        bBH = []
        totBH = []
        for sim in stdout:
            data = ps.blackHoleOverTime(saveLocation=saveLocation, inf=sim.split('short')[-1], to_return=True)
            times = times + data[0]
            sBH = sBH + data[1]
            bBH = bBH + data[2]
            totBH = totBH + data[5]
        if num_bins == 0:
            avg_sim_len = float(len(times)) / len(stdout)
            num_bins = int(avg_sim_len / 5)
        time_bins = []
        sBH_bins = []
        bBH_bins = []
        totBH_bins = []
        for i in range(num_bins):
            time_bins.append([])
            sBH_bins.append([])
            bBH_bins.append([])
            totBH_bins.append([])
        bin_min = min(times)
        bin_cutoffs = [0] * num_bins
        dtime = float((max(times)) - min(times)) / num_bins
        for i in range(len(bin_cutoffs)):
            bin_cutoffs[i] = bin_min + ((i+1) * dtime)
        for i, time in enumerate(times):
            for j, cutoff in enumerate(bin_cutoffs):
                if time < cutoff:
                    time_bins[j].append(times[i])
                    sBH_bins[j].append(sBH[i])
                    bBH_bins[j].append(bBH[i])
                    totBH_bins[j].append(totBH[i])
                    break
        for i in range(len(time_bins)):
             time_bins[i] = bin_cutoffs[i] - (float(dtime) / 2)
             sBH_bins[i] = float(sum(sBH_bins[i])) / (len(sBH_bins[i]) + 0.001)
             bBH_bins[i] = float(sum(bBH_bins[i])) / (len(bBH_bins[i]) + 0.001)
             totBH_bins[i] = float(sum(totBH_bins[i])) / (len(totBH_bins[i]) + 0.001)
        plt.figure(1)
        plt.plot(time_bins, sBH_bins)
        plt.xscale('log')
        plt.figure(2)
        plt.plot(time_bins, bBH_bins)
        plt.xscale('log')
        plt.figure(3)
        plt.plot(time_bins, totBH_bins)
        plt.xscale('log')
    plt.figure(1)
    plt.legend(legend, loc=0)
    plt.title('Grid Single Black Hole Count')
    plt.ylabel('N')
    plt.xlabel('Physical Time (Myr)')
    plt.savefig((saveLocation + 'gridSingleBH.png'))
    plt.figure(2)
    plt.legend(legend, loc=0)
    plt.title('Grid Binary Black Hole Count')
    plt.ylabel('N')
    plt.xlabel('Physical Time (Myr)')
    plt.savefig((saveLocation + 'gridBinaryBH.png'))
    plt.figure(3)
    plt.legend(legend, loc=0)
    plt.title('Grid Total Black Hole Count')
    plt.ylabel('N')
    plt.xlabel('Physical Time (Myr)')
    plt.savefig((saveLocation + 'gridTotalBH.png'))
    plt.close('all')

def grid_metaGen(saveLocation='', grid=[], num_bins=0):
    """
    Gathers and plots cluster statistics over time for an entire grid.
    Bins the data for groups of simulations with the same initial conditions (e.g. 'N10K_r10_Z01_1' and 'N10K_r10_Z01_2', etc)
    saveLocation designates where to save the plots
    Grid allows the user to pass a list of simulations to include. Will run _get_grid() otherwise.
    num_bins specifies the number of bins to use for each set of initial conditions. Will place approx. 5 data points per bin otherwise
    Calls _get_grid(), ps.metaGen()
    """
    plt.close('all')
    if grid == []:
        grid = _get_grid()
    plt.figure(1)
    plt.figure(2)
    plt.figure(3)
    plt.figure(4)
    plt.figure(5)
    legend = []
    for sim_type in grid:
        legend.append(sim_type)
        sim_type_list = subprocess.Popen('ls *short{0}*'.format(sim_type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_type_list.communicate()
        stdout = stdout.split()
        times = []
        sBH = []
        bBH = []
        tBH = []
        for sim in stdout:
            data = ps.metaGen(saveLocation=saveLocation, inf=sim.split('short')[-1], to_return=True)
            times = list(map(float, data[0]))
            RC = list(map(float, data[1]))
            RSCALE = list(map(float, data[2]))
            singleN = list(map(float, data[3]))
            binaryN = list(map(float, data[4]))
            totalN = list(map(float, data[5]))
        if num_bins == 0:
            avg_sim_len = float(len(times)) / len(stdout)
            num_bins = int(avg_sim_len / 5)
        time_bins = []
        RC_bins = []
        RSCALE_bins = []
        singleN_bins = []
        binaryN_bins = []
        totalN_bins = []
        for i in range(num_bins):
            time_bins.append([])
            RC_bins.append([])
            RSCALE_bins.append([])
            singleN_bins.append([])
            binaryN_bins.append([])
            totalN_bins.append([])
        bin_min = min(times)
        bin_cutoffs = [0] * num_bins
        dtime = float((max(times)) - min(times)) / num_bins
        for i in range(len(bin_cutoffs)):
            bin_cutoffs[i] = bin_min + ((i+1) * dtime)
        for i, time in enumerate(times):
            for j, cutoff in enumerate(bin_cutoffs):
                if time < cutoff:
                    time_bins[j].append(times[i])
                    RC_bins[j].append(RC[i])
                    RSCALE_bins[j].append(RSCALE[i])
                    singleN_bins[j].append(singleN[i])
                    binaryN_bins[j].append(binaryN[i])
                    totalN_bins[j].append(totalN[i])
                    break
        for i in range(len(time_bins)):
             time_bins[i] = bin_cutoffs[i] - (float(dtime) / 2)
             RC_bins[i] = float(sum(RC_bins[i])) / (len(RC_bins[i]) + 0.001)
             RSCALE_bins[i] = float(sum(RSCALE_bins[i])) / (len(RSCALE_bins[i]) + 0.001)
             singleN_bins[i] = float(sum(singleN_bins[i])) / (len(singleN_bins[i]) + 0.001)
             binaryN_bins[i] = float(sum(binaryN_bins[i])) / (len(binaryN_bins[i]) + 0.001)
             totalN_bins[i] = float(sum(totalN_bins[i])) / (len(totalN_bins[i]) + 0.001)
        plt.figure(1)
        plt.plot(time_bins, RC_bins)
        plt.xscale('log')
        plt.figure(2)
        plt.plot(time_bins, RSCALE_bins)
        plt.xscale('log')
        plt.figure(3)
        plt.plot(time_bins, singleN_bins)
        plt.xscale('log')
        plt.figure(4)
        plt.plot(time_bins, binaryN_bins)
        plt.xscale('log')
        plt.figure(5)
        plt.plot(time_bins, totalN_bins)
        plt.xscale('log')
    plt.figure(1)
    plt.legend(legend, loc=0)
    plt.title('Grid Core Radius Over Time')
    plt.ylabel('Core Radius (N-body Units)')
    plt.xlabel('Physical Time (Myr)')
    plt.savefig((saveLocation + 'gridRC.png'))
    plt.figure(2)
    plt.legend(legend, loc=0)
    plt.title('Grid Half-mass Radius Over Time')
    plt.ylabel('Half-mass Radius (N-body Units)')
    plt.xlabel('Physical Time (Myr)')
    plt.savefig((saveLocation + 'gridRSCALE.png'))
    plt.figure(3)
    plt.legend(legend, loc=0)
    plt.title('Grid Single Objects Over Time')
    plt.ylabel('N')
    plt.xlabel('Physical Time (Myr)')
    plt.savefig((saveLocation + 'gridSingleN.png'))
    plt.figure(4)
    plt.legend(legend, loc=0)
    plt.title('Grid Binary Objects Over Time')
    plt.ylabel('N')
    plt.xlabel('Physical Time (Myr)')
    plt.savefig((saveLocation + 'gridBinaryN.png'))
    plt.figure(5)
    plt.legend(legend, loc=0)
    plt.title('Grid Total Objects Over Time')
    plt.ylabel('N')
    plt.xlabel('Physical Time (Myr)')
    plt.savefig((saveLocation + 'gridTotalN.png'))
    plt.close('all')

def grid_metaBinary(saveLocation='', grid=[], num_bins=0):
    """
    Gathers and plots binary frequencies over time for an entire grid.
    Bins the data for groups of simulations with the same initial conditions (e.g. 'N10K_r10_Z01_1' and 'N10K_r10_Z01_2', etc)
    saveLocation designates where to save the plots
    Grid allows the user to pass a list of simulations to include. Will run _get_grid() otherwise.
    num_bins specifies the number of bins to use for each set of initial conditions. Will place approx. 5 data points per bin otherwise
    Calls _get_grid(), ps.metaBinary()
    """
    plt.close('all')
    if grid == []:
        grid = _get_grid()
    plt.figure(1)
    plt.figure(2)
    plt.figure(3)
    plt.figure(4)
    plt.figure(5)
    legend = []
    for sim_type in grid:
        legend.append(sim_type)
        sim_type_list = subprocess.Popen('ls *short{0}*'.format(sim_type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_type_list.communicate()
        stdout = stdout.split()
        time_all = []
        all_ratio = []
        time_BH = []
        BH_ratio = []
        for sim in stdout:
            meta, sevData, bevData = ps.metaBinary(saveLocation=saveLocation, inf=sim.split('short')[-1], to_return=True)
            times = meta.keys()
            times.sort()
            for time in times:
                if ('singles' in meta[time]) and ('binaries' in meta[time]):
                    ratio = float(meta[time]['binaries']) / (meta[time]['binaries'] + meta[time]['singles'] + 0.001)
                    time_all.append(time)
                    all_ratio.append(ratio)
            count = {}
            for val in sevData:
                if not val[0] in count:
                    count[val[0]] = {'singles' : 0, 'binaries' : 0}
                count[val[0]]['singles'] += 1
            for val in bevData:
                if not val[0] in count:
                    count[val[0]] = {'singles' : 0, 'binaries' : 0}
                if val[1] == 14:
                    count[val[0]]['binaries'] += 1
                if val[2] == 14:
                    count[val[0]]['binaries'] += 1
            times = count.keys()
            times.sort()
            for time in times:
                ratio = float(count[time]['binaries']) / (count[time]['binaries'] + count[time]['singles'])
                time_BH.append(time)
                BH_ratio.append(ratio)
        # all
        if num_bins == 0:
            avg_sim_len = float(len(time_all)) / len(stdout)
            num_bins = int(avg_sim_len / 5)
        time_bins = []
        ratio_bins = []
        for i in range(num_bins):
            time_bins.append([])
            ratio_bins.append([])
        bin_min = min(time_all)
        bin_cutoffs = [0] * num_bins
        dtime = float((max(time_all)) - min(time_all)) / num_bins
        for i in range(len(bin_cutoffs)):
            bin_cutoffs[i] = bin_min + ((i+1) * dtime)
        for i, time in enumerate(time_all):
            for j, cutoff in enumerate(bin_cutoffs):
                if time < cutoff:
                    time_bins[j].append(time_all[i])
                    ratio_bins[j].append(all_ratio[i])
                    break
        for i in range(len(time_bins)):
             time_bins[i] = bin_cutoffs[i] - (float(dtime) / 2)
             ratio_bins[i] = float(sum(ratio_bins[i])) / (len(ratio_bins[i]) + 0.001)
        plt.figure(1)
        plt.plot(time_bins, ratio_bins)
        # BH
        if num_bins == 0:
            avg_sim_len = float(len(time_BH)) / len(stdout)
            num_bins = int(avg_sim_len / 5)
        time_bins = []
        ratio_bins = []
        for i in range(num_bins):
            time_bins.append([])
            ratio_bins.append([])
        bin_min = min(time_BH)
        bin_cutoffs = [0] * num_bins
        dtime = float((max(time_BH)) - min(time_BH)) / num_bins
        for i in range(len(bin_cutoffs)):
            bin_cutoffs[i] = bin_min + ((i+1) * dtime)
        for i, time in enumerate(time_BH):
            for j, cutoff in enumerate(bin_cutoffs):
                if time < cutoff:
                    time_bins[j].append(time_BH[i])
                    ratio_bins[j].append(BH_ratio[i])
                    break
        for i in range(len(time_bins)):
             time_bins[i] = bin_cutoffs[i] - (float(dtime) / 2)
             ratio_bins[i] = float(sum(ratio_bins[i])) / (len(ratio_bins[i]) + 0.001)
        plt.figure(2)
        plt.plot(time_bins, ratio_bins)
    plt.figure(1)
    plt.legend(legend, loc=0)
    plt.title('Grid Binary Frequency Over Time')
    plt.ylabel('Binary Frequency')
    plt.xlabel('Physical Time (Myr)')
    plt.xscale('log')
    plt.savefig((saveLocation + 'gridAllBinary.png'))
    plt.figure(2)
    plt.legend(legend, loc=0)
    plt.title('Grid Black Hole Binary Frequency Over Time')
    plt.ylabel('Black Hole Binary Frequency')
    plt.xlabel('Physical Time (Myr)')
    plt.xscale('log')
    plt.savefig((saveLocation + 'gridBHBinary.png'))
    plt.close('all')

def grid_massDist(saveLocation='', num_bins=0, grid=[]):
    """
    Gathers and plots black hole mass distribution over time for an entire grid.
    Bins the data for groups of simulations with the same initial conditions (e.g. 'N10K_r10_Z01_1' and 'N10K_r10_Z01_2', etc)
    saveLocation designates where to save the plots
    Grid allows the user to pass a list of simulations to include. Will run _get_grid() otherwise.
    num_bins specifies the number of bins to use for each set of initial conditions. Will place approx. 5 data points per bin otherwise
    Calls _get_grid(), ps.massDist()
    """
    plt.close('all')
    if grid == []:
        grid = _get_grid()
    grid_len = len(grid)
    subplotStr = str(grid_len) + '11'
    subplotInt = int(subplotStr)
    plt.figure(1)
    plt.subplot(subplotInt)
    plt.figure(2)
    plt.subplot(subplotInt)
    plt.figure(3)
    plt.subplot(subplotInt)
    legend = []
    t_times = []
    t_sBH = []
    t_bBH = []
    t_tBH = []
    x_max = 0
    y_max = 0
    for sim_index, sim_type in enumerate(grid):
        legend.append(sim_type)
        sim_type_list = subprocess.Popen('ls *short{0}*'.format(sim_type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_type_list.communicate()
        stdout = stdout.split()
        time_list = []
        sBH = []
        bBH = []
        tBH = []
        for sim in stdout:
            mass = ps.massDist(saveLocation=saveLocation, inf=sim.split('short')[-1], to_return=True)
            times = mass.keys()
            times.sort()
            for time in times:
                time_list.append(time)
                sBH.append(mass[time]['sBH'])
                bBH.append(mass[time]['bBH'])
                tBH.append(sBH[-1] + bBH[-1])
        if num_bins == 0:
            avg_sim_len = float(len(time_list)) / len(stdout)
            num_bins = int(avg_sim_len / 30)
        time_bins = []
        sBH_bins = []
        bBH_bins = []
        tBH_bins = []
        for i in range(num_bins):
            time_bins.append([])
            sBH_bins.append([])
            bBH_bins.append([])
            tBH_bins.append([])
        bin_min = min(time_list)
        bin_cutoffs = [0] * num_bins
        dtime = float((max(time_list)) - min(time_list)) / num_bins
        for i in range(len(bin_cutoffs)):
            bin_cutoffs[i] = bin_min + ((i+1) * dtime)
        for i, time in enumerate(time_list):
            for j, cutoff in enumerate(bin_cutoffs):
                if time < cutoff:
                    time_bins[j].append(time_list[i])
                    sBH_bins[j].append(sBH[i])
                    bBH_bins[j].append(bBH[i])
                    tBH_bins[j].append(tBH[i])
                    break
        for i in range(len(time_bins)):
             time_bins[i] = bin_cutoffs[i] - (float(dtime) / 2)
             sBH_bins[i] = [item for sublist in sBH_bins[i] for item in sublist]
             bBH_bins[i] = [item for sublist in bBH_bins[i] for item in sublist]
             tBH_bins[i] = [item for sublist in tBH_bins[i] for item in sublist]
        time_bins = list(map(int, time_bins))
        t_times.append(time_bins)
        t_sBH.append(sBH_bins)
        t_bBH.append(bBH_bins)
        t_tBH.append(tBH_bins)
        plt.figure(1)
        sub_str = subplotStr[0:2] + str(sim_index + 1)
        sub_int = int(sub_str)
        plt.subplot(sub_int)
        plt.boxplot(sBH_bins, positions=time_bins, widths=35)
        ax = plt.gca()
        if ax.get_xlim()[1] > x_max:
            x_max = ax.get_xlim()[1]
        if ax.get_ylim()[1] > y_max:
            y_max = ax.get_ylim()[1]
        plt.figure(2)
        sub_str = subplotStr[0:2] + str(sim_index + 1)
        sub_int = int(sub_str)
        plt.subplot(sub_int)
        plt.boxplot(bBH_bins, positions=time_bins, widths=35)
        ax = plt.gca()
        if ax.get_xlim()[1] > x_max:
            x_max = ax.get_xlim()[1]
        if ax.get_ylim()[1] > y_max:
            y_max = ax.get_ylim()[1]
        plt.figure(3)
        sub_str = subplotStr[0:2] + str(sim_index + 1)
        sub_int = int(sub_str)
        plt.subplot(sub_int)
        plt.boxplot(tBH_bins, positions=time_bins, widths=35) 
        ax = plt.gca()
        if ax.get_xlim()[1] > x_max:
            x_max = ax.get_xlim()[1]
        if ax.get_ylim()[1] > y_max:
            y_max = ax.get_ylim()[1]
    for i in range(len(grid)):
        plt.figure(1)
        sub_str = subplotStr[0:2] + str(i + 1)
        sub_int = int(sub_str)
        plt.subplot(sub_int)
        plt.xlim(0, x_max)
        plt.ylim(0, y_max)
        ax = plt.gca()
        ax.yaxis.set_ticks(np.arange(0, y_max, (y_max / 5)))
        if i != (len(grid) - 1):
            ax.get_xaxis().set_visible(False)
            ax.text(0.77, 0.95, grid[i], transform=ax.transAxes, fontsize=14, verticalalignment='top')
        else:
            ax.xaxis.set_ticks(np.arange(0, x_max, (x_max / 10)))
            ax.text(0.77, 0.95, grid[i], transform=ax.transAxes, fontsize=14, verticalalignment='top')
        plt.figure(2)
        sub_str = subplotStr[0:2] + str(i + 1)
        sub_int = int(sub_str)
        plt.subplot(sub_int)
        plt.xlim(0, x_max)
        plt.ylim(0, y_max)
        ax = plt.gca()
        ax.yaxis.set_ticks(np.arange(0, y_max, (y_max / 5)))
        if i != (len(grid) - 1):
            ax.get_xaxis().set_visible(False)
            ax.text(0.77, 0.95, grid[i], transform=ax.transAxes, fontsize=14, verticalalignment='top')
        else:
            ax.xaxis.set_ticks(np.arange(0, x_max, (x_max / 10)))
            ax.text(0.77, 0.95, grid[i], transform=ax.transAxes, fontsize=14, verticalalignment='top')
        plt.figure(3)
        sub_str = subplotStr[0:2] + str(i + 1)
        sub_int = int(sub_str)
        plt.subplot(sub_int)
        plt.xlim(0, x_max)
        plt.ylim(0, y_max)
        ax = plt.gca()
        ax.yaxis.set_ticks(np.arange(0, y_max, (y_max / 5)))
        if i != (len(grid) - 1):
            ax.get_xaxis().set_visible(False)
            ax.text(0.77, 0.95, grid[i], transform=ax.transAxes, fontsize=14, verticalalignment='top')
        else:
            ax.xaxis.set_ticks(np.arange(0, x_max, (x_max / 10)))
            ax.text(0.77, 0.95, grid[i], transform=ax.transAxes, fontsize=14, verticalalignment='top')
    plt.figure(1)
    plt.subplot(subplotInt)
    plt.title('Single Black Hole Mass Statistics')
    plt.subplot(sub_int)
    plt.xlabel('Physical Time (Myr)')
    plt.ylabel('Mass (M*)')
    plt.subplots_adjust(hspace=0)
    plt.savefig((saveLocation + 'grid_sBH_massFraction.png'))
    plt.figure(2)
    plt.subplot(subplotInt)
    plt.title('Binary Black Hole Mass Statistics')
    plt.subplot(sub_int)
    plt.xlabel('Physical Time (Myr)')
    plt.ylabel('Mass (M*)')
    plt.subplots_adjust(hspace=0)
    plt.savefig((saveLocation + 'grid_bBH_massFraction.png'))
    plt.figure(3)
    plt.subplot(subplotInt)
    plt.title('Total Black Hole Mass Statistics')
    plt.subplot(sub_int)
    plt.xlabel('Physical Time (Myr)')
    plt.ylabel('Mass (M*)')
    plt.subplots_adjust(hspace=0)
    plt.savefig((saveLocation + 'grid_tBH_massFraction.png'))
    plt.close('all')

def grid_massDist2(saveLocation='', num_bins=0, grid=[]):
    """
    A modified version of grid_massDist()
    Gathers and plots the mass distribution of black holes over time for an entire grid.
    Bins the data for groups of simulations with the same initial conditions (e.g. 'N10K_r10_Z01_1' and 'N10K_r10_Z01_2', etc)
    saveLocation designates where to save the plots
    Grid allows the user to pass a list of simulations to include. Will run _get_grid() otherwise.
    num_bins specifies the number of bins to use for each set of initial conditions. Will place approx. 5 data points per bin otherwise
    Calls _get_grid(), ps.massDist()
    """
    plt.close('all')
    if grid == []:
        grid = _get_grid()
    legend = []
    plt.figure(1)
    plt.figure(2)
    plt.figure(3)
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for sim_index, sim_type in enumerate(grid):
        legend.append(sim_type)
        sim_type_list = subprocess.Popen('ls *short{0}*'.format(sim_type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_type_list.communicate()
        stdout = stdout.split()
        time_list = []
        sBH = []
        bBH = []
        tBH = []
        for sim in stdout:
            mass = ps.massDist(saveLocation=saveLocation, inf=sim.split('short')[-1], to_return=True)
            times = mass.keys()
            times.sort()
            for time in times:
                time_list.append(time)
                sBH.append(mass[time]['sBH'])
                bBH.append(mass[time]['bBH'])
                tBH.append(sBH[-1] + bBH[-1])
        if num_bins == 0:
            avg_sim_len = float(len(time_list)) / len(stdout)
            num_bins = int(avg_sim_len / 30)
        time_bins = []
        sBH_bins = []
        bBH_bins = []
        tBH_bins = []
        for i in range(num_bins):
            time_bins.append([])
            sBH_bins.append([])
            bBH_bins.append([])
            tBH_bins.append([])
        bin_min = min(time_list)
        bin_cutoffs = [0] * num_bins
        dtime = float((max(time_list)) - min(time_list)) / num_bins
        for i in range(len(bin_cutoffs)):
            bin_cutoffs[i] = bin_min + ((i+1) * dtime)
        for i, time in enumerate(time_list):
            for j, cutoff in enumerate(bin_cutoffs):
                if time < cutoff:
                    time_bins[j].append(time_list[i])
                    sBH_bins[j].append(sBH[i])
                    bBH_bins[j].append(bBH[i])
                    tBH_bins[j].append(tBH[i])
                    break
        for i in range(len(time_bins)):
             time_bins[i] = bin_cutoffs[i] - (float(dtime) / 2)
             sBH_bins[i] = [item for sublist in sBH_bins[i] for item in sublist]
             bBH_bins[i] = [item for sublist in bBH_bins[i] for item in sublist]
             tBH_bins[i] = [item for sublist in tBH_bins[i] for item in sublist]
        time_bins = list(map(int, time_bins))
        sBH_std = []
        bBH_std = []
        tBH_std = []
        sBH_avg = []
        bBH_avg = []
        tBH_avg = []
        for i in range(len(time_bins)):
            if sBH_bins[i] == []:
                sBH_avg.append(0)
                sBH_std.append(0)
            else:
                sBH_avg.append(float(sum(sBH_bins[i])) / (len(sBH_bins[i]) + 0.001))
                sBH_std.append(np.std(sBH_bins[i]))
            if bBH_bins[i] == []:
                bBH_avg.append(0)
                bBH_std.append(0)
            else:
                bBH_avg.append(float(sum(bBH_bins[i])) / (len(bBH_bins[i]) + 0.001))
                bBH_std.append(np.std(bBH_bins[i]))
            if tBH_bins[i] == []:
                tBH_avg.append(0)
                tBH_std.append(0)
            else:
                tBH_avg.append(float(sum(tBH_bins[i])) / (len(tBH_bins[i]) + 0.001))
                tBH_std.append(np.std(tBH_bins[i]))
        plt.figure(1)
        plt.plot(time_bins, sBH_avg, '-',  color=color_list[sim_index])
        plt.fill_between(time_bins, map(add, sBH_avg, sBH_std), map(sub, sBH_avg, sBH_std), color=color_list[sim_index], alpha=0.3)
        plt.figure(2)
        plt.plot(time_bins, bBH_avg, '-',  color=color_list[sim_index])
        plt.fill_between(time_bins, map(add, bBH_avg, bBH_std), map(sub, bBH_avg, bBH_std), color=color_list[sim_index], alpha=0.3)
        plt.figure(3)
        plt.plot(time_bins, tBH_avg, '-',  color=color_list[sim_index])
        plt.fill_between(time_bins, map(add, tBH_avg, tBH_std), map(sub, tBH_avg, tBH_std), color=color_list[sim_index], alpha=0.3)
    plt.figure(1)
    plt.title('Single Black Hole Mass Statistics')
    plt.ylabel('Mass (M*)')
    plt.xlabel('Physical Time (Myr)')
    #plt.xscale('log')
    plt.legend(legend, loc=0)
    plt.savefig((saveLocation + 'grid22_sBH_massFraction.png'))
    plt.figure(2)
    plt.title('Binary Black Hole Mass Statistics')
    plt.ylabel('Mass (M*)')
    plt.xlabel('Physical Time (Myr)')
    #plt.xscale('log')
    plt.legend(legend, loc=0)
    plt.savefig((saveLocation + 'grid22_bBH_massFraction.png'))
    plt.figure(3)
    plt.title('Total Black Hole Mass Statistics')
    plt.ylabel('Mass (M*)')
    plt.xlabel('Physical Time (Myr)')
    #plt.xscale('log')
    plt.legend(legend, loc=0)
    plt.savefig((saveLocation + 'grid22_tBH_massFraction.png'))
    plt.close('all')

def grid_minSEMI(saveLocation='', num_bins=0, grid=[], return_min_inspiral=False, inspiral_cutoff=0.001):
    """
    Gathers and plots the minimum semi-major axis of a binary system with at least one black hole over time for an entire grid.
    Caclulates the corresponding inspiral time using Peter's equation. Code found in inspiral.py
    Bins the data for groups of simulations with the same initial conditions (e.g. 'N10K_r10_Z01_1' and 'N10K_r10_Z01_2', etc)
    saveLocation designates where to save the plots
    Grid allows the user to pass a list of simulations to include. Will run _get_grid() otherwise.
    num_bins specifies the number of bins to use for each set of initial conditions. Will place approx. 5 data points per bin otherwise
    Calls _get_grid(), ip.bh_data(), inspiral.inspiral_time_peters()
    """
    plt.close('all')
    if grid == []:
        grid = _get_grid()
    legend = []
    semis = []
    eccens = []
    m1s = []
    m2s = []
    times = []
    plt.figure(1)
    plt.figure(2)
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    BHBH_names = {}
    for sim_index, sim_type in enumerate(grid):
        legend.append(sim_type)
        sim_type_list = subprocess.Popen('ls bev.82.short{0}*'.format(sim_type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_type_list.communicate()
        stdout = stdout.split()
        stdout = list(set(stdout))
        data = {}
        for sim in stdout:
            BHBH_names[sim.split('short')[-1]] = []
            bevData, meta  = ip.bh_data('bev.82', [0, 3, 4, 6, 8, 9, 10, 1, 2], meta_data={}, info=sim.split('short')[-1])
            for val in bevData:
                if (val[1] == 14) and (val[2] == 14):
                    if not val[0] in data:
                        data[val[0]] = []
                    data[val[0]].append((val[4], val[3], val[5], val[6], val[7], val[8], sim.split('short')[-1]))
        inspiral_time_list = []
        inspiral_list = []
        for key in data:
            inspirals = []
            for binary in data[key]:
                if binary[1] < 1.0:
                    print(binary)
                    it = inspiral.inspiral_time_peters(binary[0], binary[1], binary[2], binary[3])
                    inspirals.append(it)
                    if it < inspiral_cutoff:
                        BHBH_names[binary[6]].append(int(binary[4]))
                        BHBH_names[binary[6]].append(int(binary[5]))
            if inspirals != []:
                print('inspiral found')
                inspiral_time_list.append(key)
                inspiral_list.append(min(inspirals))
        for sim in BHBH_names:
            BHBH_names[sim] = list(set(BHBH_names[sim]))
        plt.figure(1)
        plt.plot(inspiral_time_list, inspiral_list)
        plt.figure(2)
        for key in data:
            data[key] = min(data[key])
        if num_bins == 0:
            avg_sim_len = float(len(time_list)) / len(stdout)
            num_bins = int(avg_sim_len / 30)
        time_bins = []
        semi_bins = []
        ecc_bins = []
        m1_bins = []
        m2_bins = []
        keys = data.keys()
        keys.sort()
        for i in range(num_bins):
            time_bins.append([])
            semi_bins.append([])
            ecc_bins.append([])
            m1_bins.append([])
            m2_bins.append([])
        bin_min = min(keys)
        bin_cutoffs = [0] * num_bins
        dtime = float((max(keys)) - min(keys)) / num_bins
        for i in range(len(bin_cutoffs)):
            bin_cutoffs[i] = bin_min + ((i+1) * dtime)
        for time in keys:
            for j, cutoff in enumerate(bin_cutoffs):
                if time < cutoff:
                    time_bins[j].append(time)
                    semi_bins[j].append(data[time][0])
                    ecc_bins[j].append(data[time][1])
                    m1_bins[j].append(data[time][2])
                    m2_bins[j].append(data[time][3])
                    break
        for i in range(len(time_bins)):
             time_bins[i] = bin_cutoffs[i] - (float(dtime) / 2)
             if semi_bins[i] == []:
                 semi_bins[i] = semi_bins[i-1]
                 ecc_bins[i] = ecc_bins[i-1]
                 m1_bins[i] = m1_bins[i-1]
                 m2_bins[i] = m2_bins[i-1]
             else:
                 Rstar = min(semi_bins[i])
                 min_index = semi_bins[i].index(Rstar)
                 ecc_bins[i] = ecc_bins[i][min_index]
                 m1_bins[i] = m1_bins[i][min_index]
                 m2_bins[i] = m2_bins[i][min_index]
                 AU = (10 ** Rstar) * 0.00465047
                 semi_bins[i] = math.log10(AU)
        plt.plot(time_bins, semi_bins, color=color_list[sim_index])
        semis.append(semi_bins)
        eccens.append(ecc_bins)
        m1s.append(m1_bins)
        m2s.append(m2_bins)
        times.append(time_bins)
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax2.set_yscale('log')
    inspiral_list = []
    for i in range(len(eccens)):
        inspiral_list.append([])
        for j in range(len(eccens[i])):
            inspiral_list[i].append(inspiral.inspiral_time_peters(semis[i][j], eccens[i][j], m1s[i][j], m2s[i][j])) 
            if inspiral_list[i][j] < 1:
                print(i, j, semis[i][j], eccens[i][j], m1s[i][j], m2s[i][j], inspiral_list[i][j])
        ax2.plot(times[i], inspiral_list[i], ':', color=color_list[i])
    plt.title('Min BHBH Binary Semi-major Axis')
    ax1.set_ylabel('Semi-major Axis (log_10( Semi (AU)))')
    ax2.set_ylabel('Corresponding Inspiral Time (Gyr)')
    plt.xlabel('Physical Time')
    plt.legend(legend, loc=0)
    plt.savefig((saveLocation + 'gridMinBHBHSemi.png'))
    plt.figure(1)
    plt.title('Min Inspiral Time')
    plt.ylabel('Inpiral Time (Gyr)')
    plt.xlabel('Physical Time (Myr)')
    plt.yscale('log')
    plt.legend(legend, loc=0)
    plt.savefig((saveLocation + 'gridInspiralTime.png'))
    plt.close('all')
    if return_min_inspiral:
        return(BHBH_names)

def grid_BHpartner(saveLocation='', grid=[], num_bins=0):
    """
    Gathers and plots a ratio of BHBH binaries to BH-other binaries over time for an entire grid.
    Bins the data for groups of simulations with the same initial conditions (e.g. 'N10K_r10_Z01_1' and 'N10K_r10_Z01_2', etc)
    saveLocation designates where to save the plots
    Grid allows the user to pass a list of simulations to include. Will run _get_grid() otherwise.
    num_bins specifies the number of bins to use for each set of initial conditions. Will place approx. 5 data points per bin otherwise
    Calls _get_grid(), ip.bh_data()
    """
    if grid == []:
        grid = _get_grid()
    legend = []
    for sim_index, sim_type in enumerate(grid):
        legend.append(sim_type)
        sim_type_list = subprocess.Popen('ls bev.82.short{0}*'.format(sim_type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_type_list.communicate()
        stdout = stdout.split()
        stdout = list(set(stdout))
        data = {}
        for sim in stdout:
            bevData, meta  = ip.bh_data('bev.82', [0, 3, 4], meta_data={}, info=sim.split('short')[-1])
            for val in bevData:
                if not val[0] in data:
                    data[val[0]] = [0, 0]
                if (val[1] == 14) and (val[2] == 14):
                    data[val[0]][0] = data[val[0]][0] + 1
                else:
                    data[val[0]][1] = data[val[0]][1] + 1
        if num_bins == 0:
            avg_sim_len = float(len(time_list)) / len(stdout)
            num_bins = int(avg_sim_len / 30)
        time_bins = []
        BHBH_bins = []
        BHO_bins = []
        keys = data.keys()
        keys.sort()
        for i in range(num_bins):
            time_bins.append([])
            BHBH_bins.append([])
            BHO_bins.append([])
        bin_min = min(keys)
        bin_cutoffs = [0] * num_bins
        dtime = float((max(keys)) - min(keys)) / num_bins
        for i in range(len(bin_cutoffs)):
            bin_cutoffs[i] = bin_min + ((i+1) * dtime)
        for time in keys:
            for j, cutoff in enumerate(bin_cutoffs):
                if time < cutoff:
                    time_bins[j].append(time)
                    BHBH_bins[j].append(data[time][0])
                    BHO_bins[j].append(data[time][1])
                    break
        ratio_bins = []
        for i in range(len(time_bins)):
             time_bins[i] = bin_cutoffs[i] - (float(dtime) / 2)
             ratio_bins.append(float(sum(BHBH_bins[i])) / (sum(BHBH_bins[i]) + sum(BHO_bins[i]) + 0.000001))
        plt.plot(time_bins, ratio_bins)
    plt.title('BH Binary Partner Ratio')
    plt.ylabel('BHBH Binary Ratio')
    plt.xlabel('Physical Time (Myr)')
    plt.legend(legend, loc=0)
    plt.savefig((saveLocation + 'gridBHBHpartner.png'))
    plt.close('all')
    

def _primordial(grid=[]):
    """
    Builds a list of all BHs in bianry systems, in order to search for BHs in primordial binary systems
    """
    if grid == []:
        grid = _get_grid()
    IC = {}
    for sim_index, sim_type in enumerate(grid):
        sim_type_list = subprocess.Popen('ls bev.82.short{0}*'.format(sim_type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_type_list.communicate()
        stdout = stdout.split()
        stdout = list(set(stdout))
        data = {}
        IC[sim_type] = {}
        for sim in stdout:
            BHBH_set = set()
            bevData, meta  = ip.bh_data('bev.82', [0, 1, 2, 3, 4], meta_data={}, info=sim.split('short')[-1])
            for val in bevData:
                if (val[3] == 14):
                    BHBH_set.add(val[1])
                if (val[4] == 14): 
                    BHBH_set.add(val[2])
            IC[sim_type][sim] = BHBH_set
    return IC


def _fromIC(objNum1, objNum2, ecc, scale=0.1):
    with open('bev.82_0.000', 'r') as r:
        header = r.readline()
        for line in r:
            lineSplit = line.split()
            if lineSplit[0] == objNum1 or lineSplit[1] == objNum1:
                if lineSplit[0] == objNum2 or lineSplit[1] == objNum2:
                    if lineSplit[5] > (ecc * (1 - scale)) and lineSplit[5] < (ecc * (1 + scale)):
                        return True
                    else:
                        return False
                else:
                    return False
        return False

def grid_BHBHhist(saveLocation='', grid=[]):
    if grid == []:
        sim_list = subprocess.Popen('ls -d N*/', shell=True, stdout=subprocess.PIPE)
        stdout, stderr = sim_list.communicate()
        stdout = stdout.split()
        grid = list(set(stdout))
    plt.figure(1)
    plt.figure(2)
    plt.figure(3)
    legend = []
    leg_ind = []
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    grid2 = []
    for sim in grid:
        if 'Z02' in sim:
            grid2.append(sim)
    for sim in grid2:
        leg_ent = sim.split('_')[:2]
        leg_ent = leg_ent[0] + '_' + leg_ent[1]
        if not leg_ent in legend:
            legend.append(leg_ent)
            leg_ind.append(legend.index(leg_ent))
        index = legend.index(leg_ent)
        os.chdir(sim)
        hist_list = subprocess.Popen('ls *.hist', shell=True, stdout=subprocess.PIPE)
        stdout, stderr = hist_list.communicate()
        stdout = stdout.split()
        hist_grid = list(set(stdout))
        for hist in hist_grid:
            time = [[]]
            ecc = [[]]
            PB = [[]]
            M1 = [[]]
            M2 = [[]]
            Semi = [[]]
            Inspiral = [[]]
            started = True
            with open(hist, 'r') as r:
                for line in r:
                    line = line.split()
                    if line[0] == 'single':
                        started = False
                        if time[-1] != []:
                            time.append([])
                            ecc.append([])
                            PB.append([])
                            M1.append([])
                            M2.append([])
                            Semi.append([])
                            Inspiral.append([])
                    else:
                        started = True
                    if started:
                        if line[0] == 'binary':
                            time[-1].append(float(line[1]))
                            ecc[-1].append(1.0 - float(line[6]))
                            PB[-1].append(10 ** float(line[7]))
                            M1[-1].append(float(line[9]))
                            M2[-1].append(float(line[10]))
                            Semi[-1].append(float(line[8]) * 0.00465047)
                            Inspiral[-1].append(inspiral.inspiral_time_peters(float(line[8]), float(line[6]), float(line[9]), float(line[10])))
                        if line[0] == 'triple':
                            pass
                            """
                            time[-1].append(float(line[1]))
                            ecc[-1].append(1.0 - float(line[13]))
                            PB[-1].append(float(line[15]))
                            M1[-1].append(float(line[8]))
                            M2[-1].append(float(line[9]))
                            Semi[-1].append((float(line[15]) ** 2) ** (1.0/3))
                            Inspiral[-1].append(inspiral.inspiral_time_peters(Semi[-1][-1], float(line[13]), float(line[8]), float(line[9])))
                            """
            print(time)
            for i in range(len(time)):
                if time[i] != []:
                    plt.figure(1)
                    plt.plot(time[i], ecc[i], color=color_list[index], alpha=0.7, label=leg_ent)
                    plt.plot([time[i][0]], [ecc[i][0]], 'o', color=color_list[index])
                    plt.plot([time[i][-1]], [ecc[i][-1]], 'x', color=color_list[index])
                    plt.figure(2)
                    plt.plot(time[i], Semi[i], color=color_list[index], alpha=0.7, label=leg_ent)
                    plt.plot([time[i][0]], [Semi[i][0]], 'o', color=color_list[index])
                    plt.plot([time[i][-1]], [Semi[i][-1]], 'x', color=color_list[index])
                    plt.figure(3)
                    plt.plot(time[i], Inspiral[i], color=color_list[index], alpha=0.7, label=leg_ent)
                    plt.plot(time[i][0], Inspiral[i][0], 'o', color=color_list[index])
                    plt.plot(time[i][-1], Inspiral[i][-1], 'x', color=color_list[index])
        os.chdir('..')
    handles, labels = plt.gca().get_legend_handles_labels()
    new_handles, new_labels = [], []
    for handle, label in zip(handles, labels):
        if label not in new_labels:
            new_handles.append(handle)
            new_labels.append(label)
    new_handles, new_labels = _sortLegend(new_handles, new_labels)
    for i, label in enumerate(new_labels):
        new_labels[i] = label.split('_')[0]
    plt.figure(1)
    plt.title('Ecc Over Time')
    plt.xlabel('Time')
    plt.ylabel('Ecc')
    plt.yscale('log')
    plt.xscale('log')
    plt.legend(new_handles, new_labels)
    plt.savefig((saveLocation + 'EccObjectsOverTime.png'))
    plt.figure(2)
    plt.title('Semi-major Axis Over Time')
    plt.xlabel('Time')
    plt.ylabel('Semi-Major Axis (Au)')
    plt.xscale('log')
    plt.legend(new_handles, new_labels)
    plt.yscale('log')
    plt.savefig((saveLocation + 'PBObjectsOverTime.png'))
    plt.figure(3)
    plt.title('Inspiral Time Over Time')
    plt.xlabel('Time')
    plt.ylabel('Inspiral Time (Gyr)')
    plt.legend(new_handles, new_labels)
    plt.yscale('log')
    plt.xscale('log')
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2, y1, 13.6))
    plt.savefig((saveLocation + 'InspiralObjectsOverTime.png'))
    plt.close('all')
                            
def _sortLegend(handles=[], labels=[]):
    if labels == []:
        handles, labels = plt.gca().get_legend_handles_labels()
    label_int = []
    for label in labels:
        split = label.split('_')
        for item in split:
            if 'r' in item:
                label_int.append(int(item[1:]))
    label_int, labels, handles = zip(*sorted(zip(label_int, labels, handles)))
    handles, labels = list(handles), list(labels)
    return handles, labels
        





"""
grid_bh_count(saveLocation='test/', num_bins=40)
grid_metaGen(saveLocation='test/', num_bins=40)
grid_metaBinary(saveLocation='test/', num_bins=40)
grid_massDist(saveLocation='test/', num_bins=15)
grid_massDist2(saveLocation='test/', num_bins=30)
grid_minSEMI(saveLocation='test/', num_bins=40)
grid_BHpartner(saveLocation='test/', num_bins=40)
#print(_primordial())
"""

