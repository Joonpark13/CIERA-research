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
import numpy as np

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

def get_single_escape_data():
    """Returns the number of escaped neutron stars with physical times.

    For single stars only, not binary stars!

    return format:
        (
            [physical_time_1, physical_time_2, ...],
            [#_of_escaped_neutron_stars_1, #_of_escaped_neutron_stars_2, ...]
        )

        Ordered according to physical time.
    """
    filename = os.path.join(DATA_DIR, "esc.11")

    timesteps = [] # Will hold the physical times from each file
    starcounts = [] # Will hold numbers of escaped neutron stars at each timestep.
    with open(filename, 'r') as f:
        # Skip the header
        next(f)

        for line in f:
            data_line = line.split()
            # 5th item in row is star type
            type = data_line[4]

            if int(type) == NEUTRON_STAR:
                # Physical time is the first item in each line
                time = data_line[0]
                # If timestep is same as previous line, update instead of add data.
                last_ind = len(timesteps) - 1
                if last_ind >= 0 and timesteps[last_ind] == time:
                    starcounts[last_ind] += 1
                else:
                    timesteps.append(time)
                    starcounts.append(1)

    return (timesteps, starcounts)

def hist_data(timesteps, counts):
    """Converts timesteps and counts to a histogrammable format.

    timesteps and counts must have the same length.
    """
    converted = ([], [])
    for i in range(len(timesteps)):
        converted[0].append(timesteps[i])
        converted[0].append(timesteps[i])
        converted[1].append(counts[i])
        converted[1].append(counts[i])
    # remove the first extra 0
    converted[0].pop(0)
    # remove the last extra height
    converted[1].pop()

    return converted


def main():
    single = get_single_data()
    single_escape = get_single_escape_data()

    single_hist = hist_data(single[0], single[1])

    plt.plot(single_hist[0], single_hist[1], label="Counts")
    # plt.plot(single_escape[0], single_escape[1], 'o', label="Escapes")
    plt.title("Evolution of Single Neutron Star Counts")
    plt.xlabel("Physical Time (Myr)")
    plt.ylabel("Neutron Star Count")
    plt.legend()
    plt.savefig("output/single_counts.png")

    # plt.clf()
    #
    # binary_data = get_binary_data()
    # plt.plot(binary_data[0], binary_data[1])
    # plt.title("Evolution of Binary Neutron Star Counts")
    # plt.xlabel("Physical Time (Myr)")
    # plt.ylabel("Neutron Star Count")
    # plt.savefig("output/binary_counts.png")

if __name__ == "__main__":
    main()
