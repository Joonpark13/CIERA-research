#!/usr/bin/env python
"""Grabs the number of neutron stars from single and binary systems.

For preliminary task as assigned by Aaron Geller to Joon Park on 9/30/16.
Grabs data from sev.83_# and bev.82_# files from the
N5K_r26_Z002_1/save01 directory, where # is the nbody time.
"""

import os
import glob

__author__ = "Joon Park"
__version__ = 0.1
__email__ = "JoonPark@u.northwestern.edu"

# Set data source directory relative to this file.
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "N5K_r26_Z002_1", "save01")

def get_single_neutron_stars():
    """Returns the number of neutron stars per nbody timestep.
    
    For single stars only, not binary stars!

    return format:
        (
            [nbody_time_1, nbody_time_2, ...],
            [#_of_neutron_stars_1, #_of_neutron_stars_2, ...]
        )
    """
    # Grab all the single 
    single_stars = os.path.join(DATA_DIR, "sev.83_*")
    for filename in glob.glob(single_stars):
        f = open(filename, 'r')
        print f.read()
        print " "

def main():
    get_single_neutron_stars()

if __name__ == "__main__":
    main()
