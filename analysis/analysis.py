import init_parse as ip
import plot_script as ps
import grid_plot as gp
import os
import subprocess
import re

"""
Required Files in Analysis:
    analysis.py
    init_parse.py
    plot_script.py
    grid_plot.py
    inspiral.py
    parseExceptions.py
"""

aDir = os.getcwd()
os.chdir('../')
pathList = subprocess.Popen('ls -d */', shell=True, stdout=subprocess.PIPE)
stdout, stderr = pathList.communicate()
simList = stdout.split()
compDir = re.compile('^N\d{1,3}K_r\d{1,2}_Z\d\d.*')#change if the directory naming structure changes

"""
#findBBHEsc = ip.genEscape('BINARY')
#BBHEsc = {}
for sim in simList:
    if re.match(compDir, sim):
        os.chdir(sim)
        failed = os.path.isfile('logfile')
        started = os.path.exists('save01')
        os.chdir((aDir))
        if started and not failed:
            print(sim)
            if not os.path.exists(sim):
                os.makedirs(sim)
                os.chdir(sim)
                os.makedirs((sim[:-1] + '_plots'))
                os.chdir('../')
            os.chdir(('../' + sim))
            #BBHEsc[sim] = len(findBBHEsc())
            ip.bh_short('sev.83', info=sim[:-1])
            ip.bh_short('bev.82', info=sim[:-1])
            ip.bh_short('hidat.87', info=sim[:-1])
            ip.bh_short('esc.11', info=sim[:-1])
            subprocess.Popen('mv *short* {0}'.format(aDir), shell=True)
            if os.path.exists('save01'):
                subprocess.Popen('cp save01/bev.82_0.000 {0}/{1}'.format(aDir, sim), shell=True)
        os.chdir('../')
"""
os.chdir(aDir)
if not os.path.exists('grid_plots'):
    os.makedirs('grid_plots')
"""
fileList = subprocess.Popen('ls *.short*', shell=True, stdout=subprocess.PIPE)
stdout, stderr = fileList.communicate()
fileList = stdout.split()
simList = []
for file in fileList:
    if 'short' in file:
        splitFile = file.split('short')
        x = splitFile[1]
        simList.append(x)
simList = list(set(simList))
print(simList)

BHcount = {}
for sim in simList:
    print(sim)
    ps.blackHoleOverTime(saveLocation=(sim + '/plots/'), inf=sim)
    #os.makedirs((sim + '/plots/'))
    ps.blackHoleOverTime(saveLocation=(sim + '/plots/'), inf=sim)
    ps.massDist(saveLocation=(sim + '/plots/'), inf=sim)
    ps.binaryStats(saveLocation=(sim + '/plots/'), ECC=True, PB=True, SEMI=True, hist=False, numBins=100, inf=sim)
    ps.metaGen(saveLocation=(sim + '/plots/'), RC=True, RSCALE=True, TotalN=True, NC=True, inf=sim)
    ps.metaBinary(saveLocation=(sim + '/plots/'), All=True, BH=True, inf=sim)

gp.grid_bh_count(saveLocation='grid_plots/', num_bins=40)
gp.grid_metaGen(saveLocation='grid_plots/', num_bins=40)
gp.grid_metaBinary(saveLocation='grid_plots/', num_bins=40)
gp.grid_massDist(saveLocation='grid_plots/', num_bins=40)
gp.grid_massDist2(saveLocation='grid_plots/', num_bins=40)

min_inspirals = gp.grid_minSEMI(saveLocation='grid_plots/', num_bins=40, return_min_inspiral=True, inspiral_cutoff=0.1)
gp.grid_BHpartner(saveLocation='grid_plots/', num_bins=40)

print(min_inspirals)


os.chdir('..')
for sim in min_inspirals:
    print(sim)
    os.chdir(sim)
    saveLoc = aDir + '/' + sim
    for objNum in min_inspirals[sim]:
        ip.getHist(objNum, saveLocation=saveLoc)
    os.chdir('..')
os.chdir(aDir)
"""


gp.grid_BHBHhist(saveLocation='grid_plots/')


subprocess.Popen('tar -czf plots.tar.gz grid_plots N*/', shell=True)


