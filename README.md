# This repository is now OUTDATED. Find the newer version here: https://github.com/Joonpark13/neutron-stars

## From Aaron:

this directory contains 1 N-body simulation from our current grid.  This was copied from Quest:

 /projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run/RgSun_NZgrid_BHFLAG2_smallN_retry/N5K_r26_Z002_1

The directory naming convention has the following information :
N + number of initial stars
r + initial virial radius*10 (i.e., r_virial = 2.6) in parsecs
Z + metallicity*1000 (i.e., Z = 0.002)
the last number indicates which number this is in the series that all have the same N,r,Z values

--------------------------
within the N5K_r26_Z002_1 directory you will fine the following:
cleanup : a shell script that simply removes the files created by the N-body simulation (and used by follownbody6.py)

follownbody6.py : a python wrapper that I wrote to run the nbody code, catch it anytime it dies and restart it.  the hope is that this will enable us to start runs going and not have to monitor them by hand.  (the nbody code requires a LOT of hand holding).  This doesn't work perfectly, but it's a huge step forward. 

input : the input file required by nbody6

joberr : stderr output from nbody6, follownbody6 and Quest

jobout : stdout output from follownbody6 and Quest

mrunnb6.sh : the submission script for Quest

nbody6++.avx.mpi : the nbody6 executable

rs : a restart input file for nbody6

save01 : this directory contains all of the output from the nbody code.  In general, there may be many save# directories.  Each is created when the nbody code either dies or finishes.  In this directory the code ran to completion without dying (so there's only a save01 directory)


------------------
There are a few important files in save01 that I will describe here.  Others we can go through togehter at a later date:

logfile : where I dump all of the stdout from nbody6.  Lots of useful bits of information in here, and we can discuss what you might want to pull out later.  For instance, there are conversions in the logfile that you can use to go from N-body units to physical units.  Search for "PHYSICAL SCALING".  There are also indications when an ECS or AIC neutron star forms.

sev.83_# : these contain information for all of the single stars at each time step, where # is the nbody time.  Inside this file you will find the following format:

a header:
         WRITE(83,101)NS,TPHYS,TCR,TSCALE
         WRITE(83,102)NC,RC,RBAR,RTIDE,(RDENS(K),K=1,3)
         WRITE(83,103)ZMBAR,TURN,RSCALE

(not 100% sure about the units)
NS = number singles
TPHYS = the physical time in the simulation [Myr]
TCR = crossing time in N-body units
TSCALE = scaling for time [Myr]
NC = number of stars in core
RC = core radius in N-body units
RBAR = scaling for position [pc]
RTIDE = tidal radius in N-body units
RDENS = density center position in N-body units
ZMBAR = scaling for mass [Msun]
TURN = turnoff mass [Msun]
RSCALE = half-mass radius in N-body units

then one line per single star of the format:
    WRITE(83,121)NAME(IX),KW,M1,ZL1,R1,(XS(K),K=1,3),(VS(K),K=1,3),EP1,OSPIN

NAME = the ID number
KW = star type (see below)
M1 = star mass [MSun]
ZL1 = log10(luminosity [LSun])
R1 = log10(radius [RSun])
XS = x,y,z in N-body units
VS = vx, vy, vz in N-body units
EP1 = ?
OSPIN = spin [1/day ?]

bev.82_# : these contain information for all of the single stars at each time step, where # is the nbody time.  Inside this file you will find the following format:

a header:
    WRITE(82,100)NPAIRS,TPHYS

NPAIRS = number of binaries
TPHYS = simulation time (Myr)
NPAIRS = number of binaries


    WRITE(82,123)NAME(J1),NAME(J2),KW,KW2,
     &            KSTAR(ICM),ECC,PB,SEMI,M1,M2,ZL1,ZL2,R1,R2,
     &            (XS(K),K=1,3),(VS(K),K=1,3),
     &            EP1,EP2,OSPIN,OSPIN2
 
NAME = the ID numbers of each star
KW, KW2 = star types (see below)
KSTAR = a type indicator for the binary (let's ignore this for now)
ECC = eccentricity
PB = log10(orbital period [days])
SEMI = log10(semi-major axis [RSun])
M1, M2 = star masses [MSun]
ZL1, ZL2 = log10(luminosity [LSun]) for each star
R1, R2 = log10(radius [RSun]) for each star
XS = x,y,z for center of mass in N-body units
VS = vx, vy, vz for center of mass in N-body units
EP1,EP2 = ?
OSPIN1,OSPIN2 = spin for each star [1/day ?]

hidat.87_# : these contain informaion on the triples at each time step.  Each file has a line that explans what each column is, and I've copied that here for reference:

NAME(I1)    NAME(I2)    NAME(I3)    K*(I1)      K*(I2)      K*(INCM)    M(I1)[M*]                 M(I2)[M*]                 M(I3)[M*]                 RI[NB]                    ECCMAX                    ECC0                      ECC1                      P0[days]                  P1[days]

Above that is a header with the following format:

     WRITE (87,3)  NPAIRS, NRUN, N, NC, NMERGE, MULT, NEWHI,
     &              TTOT,TPHYS

I'd have to look back through the code to remind myself what every one of these entries means, but the most relevant one for us is TPHYS (the physical time in Myr) 

There are plenty more files in there of eventual interest.  But for now, this should be plenty to start with.

*       ---------------------------------------------------------------------
*
*
*       Stellar evolution types (i.e., KW)
*       ***********************
*
*       ---------------------------------------------------------------------
*       0       Low main sequence (M < 0.7).
*       1       Main sequence.
*       2       Hertzsprung gap (HG).
*       3       Red giant.
*       4       Core Helium burning.
*       5       First AGB.
*       6       Second AGB.
*       7       Helium main sequence.
*       8       Helium HG.
*       9       Helium GB.
*      10       Helium white dwarf.
*      11       Carbon-Oxygen white dwarf.
*      12       Oxygen-Neon white dwarf.
*      13       Neutron star.
*      14       Black hole.
*      15       Massless supernova remnant.
*      19       Circularizing binary (c.m. value).
*      20       Circularized binary.
*      21       First Roche stage (inactive).
*      22       Second Roche stage.
*       ---------------------------------------------------------------------



------------------
Also, there is an analysis directory that contains Josh Fuhrman's files that he used to analyse the entire grid (where this N5K_r26_Z002_1) directory was one simulation.  There's a short README file in there that I created.  I think Josh also made some README somewhere, but I couldn't find it today.

------------------

## `/scripts` directory

The `/scripts` directory contains the python analysis scripts and their output files.
