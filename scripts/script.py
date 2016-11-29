#!/usr/bin/env python

import os
import glob
# For running on quest
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import parse

params = {
    'star_num': [10, 20, 40, 80, 160],
    'rad': [26],
    'metallicity': ['02', '002']
}

data_dir = os.path.join(
    "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run/RgSun_NZgrid_BHFLAG2",
    "N{0}K_r{1}_Z{2}_*".format(
        params['star_num'][0],
        params['rad'][0],
        params['metallicity'][0]
    )
)

for dir in glob.glob(data_dir):
    # Neutron star counts
    single_data = parse.parse_run(dir, "single")
    single_timesteps = [x['time'] for x in single_data]
    single_counts = [x['stars'] for x in single_data]

    single_hist = parse.hist_data(single_timesteps, single_counts)
    plt.plot(single_hist[0], single_hist[1], label="Single Counts")

    # Single neutron star escape counts
    single_escapes = parse.parse_single_run_esc(dir)
    plt.hist(single_escapes, bins=single_timesteps, histtype="stepfilled", label="Escapes", fill=False)

    # Binary neutron star counts
    binary_data = parse.parse_run(dir, "binary")
    binary_timesteps = [x['time'] for x in binary_data]
    binary_counts = [x['stars'] for x in binary_data]

    binary_hist = parse.hist_data(binary_timesteps, binary_counts)
    plt.plot(binary_hist[0], binary_hist[1], label="Binary Counts")

    plt.title("Evolution of Single Neutron Star Counts")
    plt.xlabel("Physical Time (Myr)")
    plt.ylabel("Neutron Star Count")
    plt.legend()
    plt.savefig("output/single_counts_{0}.png".format(dir.split('_')[-1]))

    plt.clf()
