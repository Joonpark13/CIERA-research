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
__version__ = 1.0
__email__ = "JoonPark@u.northwestern.edu"

# Set data source directory relative to this file.
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "N5K_r26_Z002_1", "save01")
# Star type
NEUTRON_STAR = 13

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
            # Physical time is the second item in the first line
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
                # second item in row is star type
                if int(data_line[1]) == NEUTRON_STAR:
                    counter += 1
            starcounts.insert(position, counter)
                    
    return (timesteps, starcounts)

def get_binary_data():
    """Returns the number of neutron stars with physical times.

    For binary stars only, not single stars!

    return format:
        (
            [physical_time_1, physical_time_2, ...],
            [#_of_neutron_stars_1, #_of_neutron_stars_2, ...]
        )

        Ordered according to physical time.
    """
    # Grab all the binary star data files
    binary_stars = os.path.join(DATA_DIR, "bev.82_*")

    timesteps = [] # Will hold the physical times from each file
    starcounts = [] # Will hold numbers of neutron stars at each timestep.
    for filename in glob.glob(binary_stars):
        with open(filename, 'r') as f:
            # Physical time is the second item in the first line
            physical_time = float(f.readline().split()[1])
            # Save position so the starcount can be inserted at the same position
            position = bisect.bisect(timesteps, physical_time)
            # Insert so that timesteps is always ordered
            bisect.insort(timesteps, physical_time)

            # Count the number of neutron stars in this file (timestep)
            counter = 0
            for line in f:
                data_line = line.split()
                # third item in row is first star type
                if int(data_line[2]) == NEUTRON_STAR:
                    counter += 1
                # fourth item in row is second star type
                if int(data_line[3]) == NEUTRON_STAR:
                    counter += 1
            starcounts.insert(position, counter)

    return (timesteps, starcounts)

def main():
    single_data = get_single_data()
    plt.plot(single_data[0], single_data[1])
    plt.title("Evolution of Single Neutron Star Counts")
    plt.xlabel("Physical Time (Myr)")
    plt.ylabel("Neutron Star Count")
    plt.savefig("single_counts.png")
    plt.clf()

    binary_data = get_binary_data()
    plt.plot(binary_data[0], binary_data[1])
    plt.title("Evolution of Binary Neutron Star Counts")
    plt.xlabel("Physical Time (Myr)")
    plt.ylabel("Neutron Star Count")
    plt.savefig("binary_counts.png")

if __name__ == "__main__":
    main()
