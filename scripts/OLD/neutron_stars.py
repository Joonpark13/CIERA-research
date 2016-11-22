#!/usr/bin/env python
"""Grabs the number of neutron stars from single and binary systems.

For preliminary task as assigned by Aaron Geller to Joon Park on 9/30/16.
Grabs data from sev.83_# and bev.82_# files from the
N5K_r26_Z002_1/save01 directory, where # is the nbody time.
"""

import os
import glob
# For running on quest
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import bisect

__author__ = "Joon Park"
__email__ = "JoonPark@u.northwestern.edu"

# Star type
NEUTRON_STAR = 13

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

def get_single_data(data_dir):
    """Returns the number of neutron stars with physical times.
    
    For single stars only, not binary stars!

    return format:
        (
            [physical_time_1, physical_time_2, ...],
            [#_of_neutron_stars_1, #_of_neutron_stars_2, ...]
        )

        Ordered according to physical time.
    """
    data_dir = os.path.join(data_dir, "save*")

    total_timesteps = []
    total_counts = []

    # Go through all the save01, save02, etc folders
    for dirname in glob.glob(data_dir):
        print dirname # DEBUG
        # Grab all the single star data files
        single_stars = os.path.join(dirname, "sev.83_*")
        sev_list = glob.glob(single_stars)

        timesteps = [] # Will hold the physical times from each file
        starcounts = [] # Will hold numbers of neutron stars at each timestep.
        for filename in sev_list:
            with open(filename, 'r') as f:
                row = f.readline().split()
                # Physical time is the second item in the first line
                physical_time = float(row[1])
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

        if len(total_timesteps) == 0: # If save01
            total_timesteps = timesteps
            total_counts = starcounts
        else:
            for ind, timestep in enumerate(timesteps):
                if timestep > total_timesteps[-1]: # Only append those that are not duplicates
                    total_timesteps.append(timestep)
                    total_counts.append(starcounts[ind])

    return (total_timesteps, total_counts)

def get_binary_data(data_dir):
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
    binary_stars = os.path.join(data_dir, "bev.82_*")

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

def get_single_escapes(data_dir):
    """Returns a list of physics times at which a neutron star escaped.

    For single stars only, not binary stars!
    """
    save_dirs = os.path.join(data_dir, "save*")

    escape_times = []
    for dirname in glob.glob(save_dirs):
        # Neutron star escape counts
        filename = os.path.join(dirname, "esc.11")

        with open(filename, 'r') as f:
            # Skip the header
            next(f)

            cut = False
            for line in f:
                data_line = line.split()
                # 5th item in row is star type
                type = data_line[4]

                if int(type) == NEUTRON_STAR:
                    if len(escape_times) == 0: # For save01
                        escape_times.append(float(data_line[0])) # Physical time is the first item in each row
                    else:
                        time = float(data_line[0])
                        # Throw away duplicate data from previous save
                        if not cut:
                            cut_ind = 0
                            for ind, val in enumerate(escape_times):
                                if time < val:
                                    cut_ind = ind
                            escape_times = escape_times[:cut_ind + 1]
                            cut = True
                        escape_times.append(time)

    return escape_times


def main():
    params = {
        'star_num': [10, 20, 40, 80, 160],
        'rad': [26],
        'metallicity': ['02', '002']
    }
    # data_dir = os.path.join("/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
                            # "RgSun_NZgrid_BHFLAG2",
                            # "N{0}K_r{1}_Z{2}_*".format(params['star_num'][0],
                                                       # params['rad'][0],
                                                       # params['metallicity'][0]
                                                      # )
                           # )
    # DEBUG
    data_dir = os.path.join(
        "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
        "RgSun_NZgrid_BHFLAG2",
        "N10K_r26_Z02_11"
    )
    for dir in glob.glob(data_dir):
        timesteps, counts = get_single_data(dir)
        single_hist = hist_data(timesteps, counts)
        plt.plot(single_hist[0], single_hist[1], label="Counts")

        single_escapes = get_single_escapes(dir)
        plt.hist(single_escapes, bins=timesteps, histtype="stepfilled", label="Escapes", fill=False)

        plt.title("Evolution of Single Neutron Star Counts")
        plt.xlabel("Physical Time (Myr)")
        plt.ylabel("Neutron Star Count")
        plt.legend()
        plt.savefig("output/single_counts_{0}.png".format(dir.split('_')[-1]))

        plt.clf()

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
