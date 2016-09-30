#!/usr/bin/env python
"""Grabs the number of neutron stars from single and binary systems.

For preliminary task as assigned by Aaron Geller to Joon Park on 9/30/16.
Grabs data from sev.83_# and bev.82_# files from the
N5K_r26_Z002_1/save01 directory, where # is the nbody time.
"""

import os
import glob
import matplotlib.pyplot as plt
import bisect

__author__ = "Joon Park"
__version__ = 0.1
__email__ = "JoonPark@u.northwestern.edu"

# Set data source directory relative to this file.
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "N5K_r26_Z002_1", "save01")
# The first 3 lines of each file are header information.

def get_single_data():
    """Returns the number of neutron stars with physical times.
    
    For single stars only, not binary stars!

    return format:
        (
            [physical_time_1, physical_time_2, ...],
            [#_of_neutron_stars_1, #_of_neutron_stars_2, ...]
        )

        Ordered according to physical time.
    """
    # Grab all the single star data files
    single_stars = os.path.join(DATA_DIR, "sev.83_*")

    timesteps = [] # Will hold the physical times from each file
    starcounts = [] # Will hold numbers of neutron stars at each timestep.
    for filename in glob.glob(single_stars):
        with open(filename, 'r') as f:
            physical_time = float(f.readline().split()[1])
            # Save position so the starcount can be inserted at the same position
            position = bisect.bisect(timesteps, physical_time)
            # Insert so that timesteps is always ordered
            bisect.insort(timesteps, physical_time)

            # Skip the header
            for _ in range(2):
                next(f)

            # Count the number of neutron stars in this file (timestep)
            counter = 0
            for line in f:
                data_line = line.split()
                if int(data_line[1]) == 13:
                    counter += 1
            starcounts.insert(position, counter)
                    
    return (timesteps, starcounts)

def main():
    data = get_single_data()
    plt.plot(data[0], data[1])
    plt.title("Evolution of Single Neutron Star Counts")
    plt.xlabel("Physical Time (Myr)")
    plt.ylabel("Neutron Star Count")
    plt.savefig("single_counts.png")

if __name__ == "__main__":
    main()
