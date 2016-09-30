#!/bin/bash
#MOAB -N N5K_r26_Z002_1
#MOAB -o jobout
#MOAB -e joberr
#MOAB -l nodes=1:ppn=6
#MOAB -l walltime=168:00:00

#MOAB -A p20633

echo Deploying job ...
cat $PBS_NODEFILE
echo $PBS_O_WORKDIR
cd $PBS_O_WORKDIR

export OMP_NUM_THREADS=6
ulimit -s unlimited
#this will start a simulation with an input file named "input" and try to restart with decreasing dt if it crashes
python follownbody6.py
#for a restart from some savepoint, use this line and change the number to that of the last save directory
#python follownbody6.py 1

echo done
