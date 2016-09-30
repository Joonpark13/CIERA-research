import os
import init_parse as ip
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from cycler import cycler
import math

def blackHoleOverTime(saveLocation='', inf='', to_return=False):
    """
    Plots the various counts of black holes over time for a given simulation
    'saveLocation' is the folder in which to save the plots
    'inf' is the the suffix for the relevant shortfiles (usually the simulation name, e.g. 'N10K_r10_Z01_1')
    'to_return' set to true if instead of ploting the data, return it instead
    """
    if not saveLocation == '':
        if not os.path.exists(saveLocation):
            os.makedirs(saveLocation)
    sevData, meta = ip.bh_data('sev.83', [0, 2], meta_data={}, info=inf)
    bevData, meta = ip.bh_data('bev.82', [0, 3, 4], meta_data=meta, info=inf)
    hiData, meta = ip.bh_data('hidat.87', [0, 4, 5, 6], meta_data=meta, info=inf)
    escData, meta = ip.bh_data('esc.11', [0, 4], meta_data=meta, info=inf)
    count = {}
    for val in sevData:
        if not val[0] in count:
            count[val[0]] = {'sBH' : 0 , 'bBH' : 0 , 'tBH' : 0 , 'eBH' : 0}
        if val[1] == 14:
            count[val[0]]['sBH'] += 1
    for val in bevData:
        if not val[0] in count:
            count[val[0]] = {'sBH' : 0 , 'bBH' : 0 , 'tBH' : 0 , 'eBH' : 0}
        if val[1] == 14:
            count[val[0]]['bBH'] += 1
        if val[2] == 14:
            count[val[0]]['bBH'] += 1
    for val in hiData:
        if not val[0] in count:
            count[val[0]] = {'sBH' : 0 , 'bBH' : 0 , 'tBH' : 0 , 'eBH' : 0}
        if val[1] == 14:
            count[val[0]]['tBH'] += 1
        if val[2] == 14:
            count[val[0]]['tBH'] += 1
        if val[3] == 14:
            count[val[0]]['tBH'] += 1
    for val in escData:
        if not val[0] in count:
            count[val[0]] = {'sBH' : 0 , 'bBH' : 0 , 'tBH' : 0 , 'eBH' : 0}
        if val[1] == 14:
            count[val[0]]['eBH'] += 1
    time = []
    sBH = []
    bBH = []
    tBH = []
    eBH = []
    totBH = []
    key_list = count.keys()
    key_list.sort()
    for key in key_list:
        time.append(key)
        sBH.append(count[key]['sBH'])
        bBH.append(count[key]['bBH'])
        tBH.append(count[key]['tBH'])
        eBH.append(count[key]['eBH'])
        totBH.append(count[key]['sBH'] + count[key]['bBH'] + count[key]['tBH'] + count[key]['eBH'])
    if to_return:
        return(time, sBH, bBH, tBH, eBH, totBH)
    plt.figure()
    plt.hold(True)
    plt.plot(time, sBH, '-')
    plt.plot(time, bBH, '-')
    plt.plot(time, tBH, '-')
    plt.plot(time, eBH, '-')
    plt.plot(time, totBH, '-')
    plt.title('Black Hole Count Over Time')
    plt.xlabel('Physical Time (MY)')
    plt.ylabel('N')
    plt.legend(['Single BH', 'Binary BH', 'Triple BH', 'Escape BH', 'Total BH'], loc='best')
    plt.savefig((saveLocation + 'blackHoleCount.png'))
    plt.close('all')

def massDist(saveLocation='', inf='', to_return=False):
    """
    Plots the the mass distribution of black holes from the various simulation snapshots as color-coded CDFs
    'saveLocation' is the folder in which to save the plots
    'inf' is the the suffix for the relevant shortfiles (usually the simulation name, e.g. 'N10K_r10_Z01_1')
    'to_return' set to true if instead of ploting the data, return it instead
    """
    if not saveLocation == '':
        if not os.path.exists(saveLocation):
            os.makedirs(saveLocation)
    sevData, meta = ip.bh_data('sev.83', [0, 3], meta_data={}, info=inf)
    bevData, meta = ip.bh_data('bev.82', [0, 3, 4, 9, 10], meta_data=meta, info=inf)
    hiData, meta = ip.bh_data('hidat.87', [0, 4, 5, 6, 7, 8, 9], meta_data=meta, info=inf)
    mass = {}
    for val in sevData:
        if not val[0] in mass:
            mass[val[0]] = {'sBH' : [] , 'bBH' : [] , 'tBH' : []}
        mass[val[0]]['sBH'].append(val[1])
    for val in bevData:
        if not val[0] in mass:
            mass[val[0]] = {'sBH' : [] , 'bBH' : [] , 'tBH' : []}
        if val[1] == 14:
            mass[val[0]]['bBH'].append(val[3])
        if val[2] == 14:
            mass[val[0]]['bBH'].append(val[4])
    for val in hiData:
        if not val[0] in mass:
            mass[val[0]] = {'sBH' : [] , 'bBH' : [] , 'tBH' : []}
        if val[1] == 14:
            mass[val[0]]['tBH'].append(val[4])
        if val[2] == 14:
            mass[val[0]]['tBH'].append(val[5])
        if val[3] == 14:
            mass[val[0]]['tBH'].append(val[6])
    if to_return:
        return(mass)
    all_keys = list(mass.keys())
    all_keys.sort()
    mass_keys = []
    for key in all_keys:
        non_zero = False
        for sub_key in mass[key]:
            if mass[key][sub_key] != []:
                non_zero = True
        if non_zero:
            mass_keys.append(key)
    plt.figure(1)
    colormap = plt.cm.coolwarm
    plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 0.9, len(mass_keys))]))
    plt.figure(2)
    plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 0.9, len(mass_keys))]))
    plt.figure(3)
    plt.hold(True)
    plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 0.9, len(mass_keys))]))
    b_max_key = 0
    b_min_key = -1
    s_max_key = 0
    s_min_key = -1
    started = False
    for i, key in enumerate(mass_keys):
        tBH = mass[key]['sBH'] + mass[key]['bBH'] + mass[key]['tBH']
        tBH.sort()
        mass[key]['sBH'].sort()
        mass[key]['bBH'].sort()
        sBH_tot = _buildFraction(mass[key]['sBH'])
        bBH_tot = _buildFraction(mass[key]['bBH'])
        tBH_tot = _buildFraction(tBH)
        plt.figure(1)
        sBH_plot, = plt.step(([0] +mass[key]['sBH']),([0] + sBH_tot), where='post')
        plt.figure(2)
        bBH_plot, = plt.step(([0] + mass[key]['bBH']),([0] + bBH_tot), where='post')
        plt.figure(3)
        tBH_plot, = plt.step(([0] + tBH),([0] + tBH_tot), where='post')
        if not started:
            tBH_pi = tBH_plot
        if (b_min_key == -1) and (mass[key]['bBH'] != []):
            b_min_key = key
            started = True
            bBH_pi = bBH_plot
        if (s_min_key == -1) and (mass[key]['sBH'] != []):
            s_min_key = key
            started = True
            sBH_pi = sBH_plot
        if started:
            if (b_min_key != -1) and (mass[key]['bBH'] != []):
                b_max_key = key
                bBH_pf = bBH_plot
                tBH_pf = tBH_plot
            if (s_min_key != -1) and (mass[key]['sBH'] != []):
                s_max_key = key
                sBH_pf = sBH_plot
                tBH_pf = tBH_plot
    plt.figure(4)
    Z = [[0,0],[0,0]]
    levels = range(int(s_min_key), int(s_max_key) + 6, 5)#the +6 is so the countour will have at least 2 items, in case there is less than 5 difference between the min and max
    print('levels range: ', int(s_min_key), int(s_max_key))
    if not int(s_min_key) == -1:
        print('plotting')
        CS3 = plt.contourf(Z, levels, cmap=colormap)
        plt.clf()
        plt.figure(1)
        x1, x2, y1, y2 = plt.axis()
        plt.axis([x1, x2, 0, 1.1])
        plt.colorbar(CS3) 
        plt.title('Single Black Hole Mass CDF')
        plt.xlabel('Black Hole Mass (M*)')
        plt.ylabel('Mass Fraction')
        plt.savefig((saveLocation + 'sBH_massFraction.png'))
        plt.figure(4)
    levels = range(int(b_min_key), int(b_max_key) + 6, 5)
    print('levels range: ', int(b_min_key), int(b_max_key))
    if not int(b_min_key) == -1:
        print('plotting')
        CS3 = plt.contourf(Z, levels, cmap=colormap)
        plt.clf()
        plt.figure(2)
        x1, x2, y1, y2 = plt.axis()
        plt.axis([x1, x2, 0, 1.1])
        plt.colorbar(CS3) 
        plt.title('Binary Black Hole Mass CDF')
        plt.xlabel('Black Hole Mass (M*)')
        plt.ylabel('Mass Fraction')
        plt.savefig((saveLocation + 'bBH_massFraction.png'))
        plt.figure(4)
    levels = range(int(min(s_min_key, b_min_key)), int(max(s_max_key, b_max_key)) + 6, 5)#Include special case for in only one of the files doesn't have any BHs
    print('levels range: ', int(min(s_min_key, b_min_key)), int(max(s_max_key, b_max_key)))
    if not int(min(s_min_key, b_min_key)) == -1:
        print('plotting')
        CS3 = plt.contourf(Z, levels, cmap=colormap)
        plt.clf()
        plt.figure(3)
        x1, x2, y1, y2 = plt.axis()
        plt.axis([x1, x2, 0, 1.1])
        plt.colorbar(CS3) 
        plt.title('Total Black Hole Mass CDF')
        plt.xlabel('Black Hole Mass (M*)')
        plt.ylabel('Mass Fraction')
        plt.savefig((saveLocation + 'tBH_massFraction.png'))
    plt.close('all')

def _buildFraction(massList):
    """
    Used to turn a list of data into a CDF for plotting
    """
    mass_tot = []
    if massList == []:
        return mass_tot
    for i, M in enumerate(massList):
        if i == 0:
            mass_tot.append(massList[0])
        else:
            mass_tot.append(mass_tot[i-1] + massList[i])
    mass_sum = mass_tot[-1]
    for i in range(len(mass_tot)):
        mass_tot[i] = float(mass_tot[i]) / (mass_sum + 0.001)
    return mass_tot

def binaryStats(saveLocation='', ECC=True, PB=True, SEMI=True, hist=False, numBins=100, inf='', to_return=False):
    """
    Plots statistics of binary black hoels orbits from the various snapshots as color coded CDFs
    'saveLocation' is the folder in which to save the plots
    'ECC' True to plot eccentricity
    'PB' True to plot orbital period
    'SEMI' True to plot orbital semi-major axis
    'hist' True to plot an idividual histogram for each snapshot (WARNING: very slow)
    'numBins' to set the number of bins if 'hist' is True
    'inf' is the the suffix for the relevant shortfiles (usually the simulation name, e.g. 'N10K_r10_Z01_1')
    'to_return' set to true if instead of ploting the data, return it instead
    """
    if not saveLocation == '':
        if not os.path.exists(saveLocation):
            os.makedirs(saveLocation)
    columns = [0]
    indicies = [1, 1, 1]
    if ECC:
        columns = columns + [6]
        indicies[1] += 1
        indicies[2] += 1
    if PB:
        columns = columns + [7]
        indicies[2] += 1
    if SEMI:
        columns = columns + [8]
    bevData, meta = ip.bh_data('bev.82', columns, meta_data={}, info=inf)
    stats = {}
    for val in bevData:
        if not val[0] in stats:
            stats[val[0]] = {'ECC' : [] , 'PB' : [] , 'SEMI' : []}
        if ECC:
            stats[val[0]]['ECC'].append(val[indicies[0]])
        if PB:
            stats[val[0]]['PB'].append(val[indicies[1]])
        if SEMI:
            stats[val[0]]['SEMI'].append(val[indicies[2]])
    if to_return:
        return(stats)
    all_keys = list(stats.keys())
    all_keys.sort()
    stats_keys = []
    for key in all_keys:
        non_zero = False
        for sub_key in stats[key]:
            if stats[key][sub_key] != []:
                non_zero = True
        if non_zero:
            stats_keys.append(key)
    plt.figure(1)
    colormap = plt.cm.coolwarm
    plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 0.9, len(stats))]))
    plt.figure(2)
    plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 0.9, len(stats))]))
    plt.figure(3)
    plt.hold(True)
    plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 0.9, len(stats))]))
    for i, key in enumerate(stats_keys):
        temp_AU_list = []
        for item in stats[key]['SEMI']:
            AU = (10.0 ** item) * 0.00465047
            temp_AU_list.append(math.log10(AU))
        stats[key]['SEMI'] = temp_AU_list
        stats[key]['ECC'].sort()
        stats[key]['PB'].sort()
        stats[key]['SEMI'].sort()
        ECC_tot = _buildFraction(stats[key]['ECC'])
        PB_tot = _buildFraction(stats[key]['PB'])
        SEMI_tot = _buildFraction(stats[key]['SEMI'])
        if ECC:
            plt.figure(1)
            ECC_plot, = plt.step(([0] +stats[key]['ECC']),([0] + ECC_tot), where='post')
        if PB:
            plt.figure(2)
            PB_plot, = plt.step(([0] + stats[key]['PB']),([0] + PB_tot), where='post')
        if SEMI:
            plt.figure(3)
            SEMI_plot, = plt.step(([0] + stats[key]['SEMI']),([0] + SEMI_tot), where='post')
        if i==0:
            if ECC:
                ECC_pi = ECC_plot
            if PB:
                PB_pi = PB_plot
            if SEMI:
                SEMI_pi = SEMI_plot
        if i == (len(stats_keys) - 1):
            if ECC:
                ECC_pf = ECC_plot
            if PB:
                PB_pf = PB_plot
            if SEMI:
                SEMI_pf = SEMI_plot
    empty = True
    if stats_keys != []:
        min_key = stats_keys[0]
        max_key = stats_keys[-1]
        empty = False
    if ECC and not empty:
        plt.figure(5)
        Z = [[0,0],[0,0]]
        levels = range(int(min_key), int(max_key) + 6, 5)#the +6 is so the countour will have at least 2 items, in case there is less than 5 difference between the min and max
        CS3 = plt.contourf(Z, levels, cmap=colormap)
        plt.clf()
        plt.figure(1)
        x1, x2, y1, y2 = plt.axis()
        plt.axis([x1, x2, 0, 1.1])
        plt.colorbar(CS3) 
        plt.title('Binary Black Hole Eccentricity CDF')
        plt.xlabel('Eccentricity')
        plt.ylabel('Eccentricity Fraction')
        plt.savefig((saveLocation + 'ECC.png'))
    if PB and not empty:
        plt.figure(5)
        Z = [[0,0],[0,0]]
        levels = range(int(min_key), int(max_key) + 6, 5)
        CS3 = plt.contourf(Z, levels, cmap=colormap)
        plt.clf()
        plt.figure(2)
        x1, x2, y1, y2 = plt.axis()
        plt.axis([x1, x2, 0, 1.1])
        plt.colorbar(CS3) 
        plt.title('Binary Black Hole Period CDF')
        plt.xlabel('Log_10( Period (days))')
        plt.ylabel('Period Fraction')
        plt.savefig((saveLocation + 'PB.png'))

        time = []
        max = []
        mean = []
        median = []
        mode = []
        min = []
        key_list = stats.keys()
        key_list.sort()
        for key in key_list:
            npList = np.asarray(stats[key]['PB'])
            modeList = scipy.stats.mode(npList).mode
            for i in range(len(modeList)):
                time.append(key)
                max.append(np.amax(npList))
                mean.append(np.mean(npList))
                median.append(np.median(npList))
                mode.append(modeList[i])
                min.append(np.amin(npList))
        plt.figure(4)
        plt.plot(time, max, '-')
        plt.plot(time, mean, '-')
        plt.plot(time, median, '-')
        plt.plot(time, mode, '-')
        plt.plot(time, min, '-')
        plt.legend(['Max', 'Mean', 'Median', 'Mode', 'Min'])
        plt.title('Black Hole Binary Statistics Over Time')
        plt.xlabel('Physical Time (MY)')
        plt.ylabel('Log_10( Period (days))')
        plt.savefig((saveLocation + 'bBH_PBStats.png'))
    if SEMI and not empty:
        plt.figure(5)
        Z = [[0,0],[0,0]]
        levels = range(int(min_key), int(max_key) + 6, 5)
        CS3 = plt.contourf(Z, levels, cmap=colormap)
        plt.clf()
        plt.figure(3)
        x1, x2, y1, y2 = plt.axis()
        plt.axis([x1, x2, 0, 1.1])
        plt.colorbar(CS3) 
        plt.title('Binary Black Hole Semi-major Axis CDF')
        plt.xlabel('Log_10( Semi-major Axis (Au))')
        plt.ylabel('Semi-major Axis Fraction')
        plt.savefig((saveLocation + 'SEMI.png'))
    plt.close('all')
    if hist and not empty:
        if ECC:
            for time in stats:
                plt.figure()
                n, bins, patches = plt.hist(stats[time]['ECC'], numBins, normed=False, histtype='bar', rwidth=1)
                plt.title('Eccentricity Distribution of Black Hole Binaries: {0} MY'.format(time))
                plt.xlabel('Eccentricity')
                plt.ylabel('N')
                plt.savefig((saveLocation + 'ECC.{0}MY.png'.format(time)))
                plt.close('all')
        if PB:
            for time in stats:
                plt.figure()
                n, bins, patches = plt.hist(stats[time]['PB'], numBins, normed=False, histtype='bar', rwidth=1)
                plt.title('Period Distribution of Black Hole Binaries: {0} MY'.format(time))
                plt.xlabel('Log_10( Period (days))')
                plt.ylabel('N')
                plt.savefig((saveLocation + 'PB.{0}MY.png'.format(time)))
                plt.close('all')
        if SEMI:
            for time in stats:
                plt.figure()
                n, bins, patches = plt.hist(stats[time]['SEMI'], numBins, normed=False, histtype='bar', rwidth=1)
                plt.title('Semi-major Axis Distribution of Black Hole Binaries: {0} MY'.format(time))
                plt.xlabel('Log_10( Semi-major Axis (Au))')
                plt.ylabel('N')
                plt.savefig((saveLocation + 'SEMI.{0}MY.png'.format(time)))
                plt.close('all')
    plt.close('all')

def metaGen(saveLocation='', RC=True, RSCALE=True, TotalN=True, NC=True, inf='', to_return=False):
    """
    Plots general cluster information over time
    'saveLocation' is the folder in which to save the plots
    'RC' True to plot core radius over time
    'RSCALE' True to plot half-mass radius over time
    'TotalN' True to plot total objects in the cluster over time
    'NC' True to plot objects in cluster core over time
    'inf' is the the suffix for the relevant shortfiles (usually the simulation name, e.g. 'N10K_r10_Z01_1')
    'to_return' set to true if instead of ploting the data, return it instead
    """
    if not saveLocation == '':
        if not os.path.exists(saveLocation):
            os.makedirs(saveLocation)
    sevData, meta = ip.bh_data('sev.83', [], meta_data={}, info=inf)
    bevData, meta = ip.bh_data('bev.82', [], meta_data=meta, info=inf)
    timeList = []
    RCList = []
    RSCALEList = []
    singleList = []
    binaryList = []
    TotalNList = []
    NCList = []
    time_key_list = meta.keys()
    time_key_list.sort()
    for time in time_key_list:
        if ('singles' in meta[time]) and ('binaries' in meta[time]):
            timeList.append(time)
            if RC:
                RCList.append(meta[time]['RC'])
            if RSCALE:
                RSCALEList.append(meta[time]['RSCALE'])
            if TotalN:
                singleList.append(meta[time]['singles'])
                binaryList.append(meta[time]['binaries'])
                TotalNList.append((meta[time]['singles'] + meta[time]['binaries']))
            if NC:
                NCList.append((meta[time]['NC']))
    if to_return:
        return(timeList, RCList, RSCALEList, singleList, binaryList, TotalNList)
    if RC:
        plt.figure()
        plt.plot(timeList, RCList, '-')
        plt.title('Core Radius Over Time')
        plt.xlabel('Physical Time (MY)')
        plt.ylabel('Core Radius (N-body Units)')
        plt.xscale('log')
        RCnumpy = np.array(map(float, RCList))
        RCavg = np.mean(RCnumpy)
        RCstd = np.std(RCnumpy)
        plt.ylim(0, min((RCavg + 3*RCstd), plt.ylim()[1]))
        plt.savefig((saveLocation + 'RCTime.png'))
        plt.close('all')
    if RSCALE:
        plt.figure()
        plt.plot(timeList, RSCALEList, '-')
        plt.title('Half-mass Radius Over Time')
        plt.xlabel('Physical Time (MY)')
        plt.ylabel('Half-mass Radius (N-body Units)')
        plt.xscale('log')
        RSCALEnumpy = np.array(map(float, RSCALEList))
        RSavg = np.mean(RSCALEnumpy)
        RSstd = np.std(RSCALEnumpy)
        plt.ylim(0, min((RSavg + 3*RSavg), plt.ylim()[1]))
        plt.savefig((saveLocation + 'RSCALETime.png'))
        plt.close('all')
    if TotalN:
        plt.figure()
        plt.plot(timeList, singleList, '-')
        plt.plot(timeList, binaryList, '-')
        plt.plot(timeList, TotalNList, '-')
        plt.title('Number of Stars in System Over Time')
        plt.xlabel('Physical Time (MY)')
        plt.ylabel('Star Count')
        plt.xscale('log')
        plt.legend(['Singles', 'Binaries', 'Total'], loc='best')
        plt.savefig((saveLocation + 'TotalNTime.png'))
        plt.close('all')
    if NC:
        plt.figure()
        plt.plot(timeList, NCList, '-')
        plt.title('Number of Stars in Core Over Time')
        plt.xlabel('Physical Time (MY)')
        plt.ylabel('Star Count in Core')
        plt.xscale('log')
        plt.savefig((saveLocation + 'CoreNTime.png'))
        plt.close('all')
    plt.close('all')

def metaBinary(saveLocation='', All=True, BH=True, inf='', to_return=False):
    """
    Plots binary frequency over time
    'saveLocation' is the folder in which to save the plots
    'All' True to plot binary fraction for all objects
    'BH' True to plot binary fraction for black holes only
    'inf' is the the suffix for the relevant shortfiles (usually the simulation name, e.g. 'N10K_r10_Z01_1')
    'to_return' set to true if instead of ploting the data, return it instead
    """
    if not saveLocation == '':
        if not os.path.exists(saveLocation):
            os.makedirs(saveLocation)
    sevData, meta = ip.bh_data('sev.83', [0], meta_data={}, info=inf)
    bevData, meta = ip.bh_data('bev.82', [0, 3, 4], meta_data=meta, info=inf)
    if to_return:
        return(meta, sevData, bevData)
    if All:
        timeList = []
        AllRatio = []
        time_key_list = meta.keys()
        time_key_list.sort()
        for time in time_key_list:
            if ('singles' in meta[time]) and ('binaries' in meta[time]):
                timeList.append(time)
                ratio = float(meta[time]['binaries']) / (meta[time]['binaries'] + meta[time]['singles'] + 0.001)
                AllRatio.append(ratio)
        plt.figure()
        plt.plot(timeList, AllRatio, '-')
        plt.title('Binary Frequency Over Time')
        plt.xlabel('Physical Time (MY)')
        plt.ylabel('Binary Frequency')
        plt.savefig((saveLocation + 'AllBinary.png'))
    if BH:
        count = {}
        for val in sevData:
            if not val[0] in count:
                count[val[0]] = {'singles' : 0 , 'binaries' : 0}
            count[val[0]]['singles'] += 1
        for val in bevData:
            if not val[0] in count:
                count[val[0]] = {'singles' : 0 , 'binaries' : 0}
            if val[1] == 14:
                count[val[0]]['binaries'] += 1
            if val[2] == 14:
                count[val[0]]['binaries'] += 1
        timeList = []
        BHRatio = []
        key_list = count.keys()
        key_list.sort()
        for time in key_list:
            timeList.append(time)
            ratio = float(count[time]['binaries']) / (count[time]['binaries'] + count[time]['singles'] + 0.001)
            BHRatio.append(ratio)
        plt.figure()
        plt.plot(timeList, BHRatio, '-')
        plt.title('Black Hole Binary Frequency Over Time')
        plt.xlabel('Physical Time (MY)')
        plt.ylabel('Black Hole Binary Frequency')
        plt.xscale('log')
        plt.savefig((saveLocation + 'BHBinary.png'))
    plt.close('all')

def massDistBinary(saveLocation='', numBins=100, inf='', to_return=False):
    """
    Plots binary frequency over time
    'saveLocation' is the folder in which to save the plots
    'numBins' sets the number of bins for the histograms
    'inf' is the the suffix for the relevant shortfiles (usually the simulation name, e.g. 'N10K_r10_Z01_1')
    'to_return' set to true if instead of ploting the data, return it instead

    EDIT: Not currently set up to be used as part of the analysis.py package.
    WARNING: very slow
    """
    if not saveLocation == '':
        if not os.path.exists(saveLocation):
            os.makedirs(saveLocation)
    bevData, meta = ivp.bh_data('bev.82', [0, 3, 4, 9, 10], meta_data={}, info=inf)
    ratio = {}
    for val in bevData:
        if not val[0] in ratio:
            ratio[val[0]] = []
        if val[1] == 14:
            if val[2] == 14:
                ratio[val[0]].append(min(float(val[3]) / val[4] , float(val[4]) / val[3] ))
            else:
                ratio[val[0]].append(float(val[4]) / val[3])
        else:
            ratio[val[0]].append(float(val[3]) / val[4])
    for time in ratio:
        plt.figure()
        n, bins, patches = plt.hist(ratio[time], numBins, histtype='bar', normed=False, rwidth=1)
        plt.title('Black Hole Binary System Mass Ratio: {0} MY'.format(time))
        plt.xlabel('Mass Ratio [(M* star or M* smaller BH) / M* larger BH]')
        plt.ylabel('N')
        plt.savefig((saveLocation + 'bBHMassRatio.{0}MY.png'.format(time)))
        plt.close('all')
    plt.figure()
    plt.hold(True)
    colormap = plt.cm.coolwarm
    plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 0.9, len(ratio))]))
    for i, key in enumerate(ratio):
        ratio[key].sort()
        ratio_tot = _buildFraction(ratio[key])
        ratio_plot, = plt.step(([0] +ratio[key]),([0] + ratio_tot))
        if i==0:
            ratio_pi = ratio_plot
        if i==(len(ratio)-1):
            ratio_pf = ratio_plot
    x1, x2, y1, y2 = plt.axis()
    plt.axis([x1, x2, 0, 1.1])
    plt.legend([ratio_pi, ratio_pf], ['{0} MY'.format(list(ratio.keys())[0]), '{0} MY'.format(list(ratio.keys())[-1])], loc=2) 
    plt.title('Binary Black Hole Mass Ratio CDF')
    plt.xlabel('Binary Mass Ratio (M* Partner / M* Black Hole)')
    plt.ylabel('Mass Ratio Fraction')
    plt.savefig((saveLocation + 'bBHMassRatio.CDF.png'))
    plt.close('all')
