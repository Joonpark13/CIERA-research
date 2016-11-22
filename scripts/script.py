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
    data = parse.parse_run(dir)
    timesteps = [x['time'] for x in data]
    counts = [x['stars'] for x in data]

    single_hist = parse.hist_data(timesteps, counts)

    plt.plot(single_hist[0], single_hist[1], label="Counts")

    plt.title("Evolution of Single Neutron Star Counts")
    plt.xlabel("Physical Time (Myr)")
    plt.ylabel("Neutron Star Count")
    plt.legend()
    plt.savefig("output/single_counts_{0}.png".format(dir.split('_')[-1]))

    plt.clf()
