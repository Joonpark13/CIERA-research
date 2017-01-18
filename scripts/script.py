#!/usr/bin/env python

import os
import glob
# For running on quest
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import parse

def plot_individual(data_dir, output):
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

        # TODO: Binary esc counts

        plt.title("Evolution of Single Neutron Star Counts")
        plt.xlabel("Physical Time (Myr)")
        plt.ylabel("Neutron Star Count")
        plt.legend()
        plt.savefig("{0}/ns_counts_{1}.png".format(output, dir.split('_')[-1]))

        plt.clf()

def plot_cumulative(data_dir, output, option='single'):
    accumulated = []

    for dir in glob.glob(data_dir):
        # Neutron star counts
        parsed_data = parse.parse_run(dir, option)
        for item in parsed_data:
            accumulated += ([item['time']] * item['stars'])

    plt.hist(accumulated, bins=100, histtype="stepfilled", fill=False)
    plt.title("Evolution of " + option + "  Neutron Star Counts, Cumulative")
    plt.xlabel("Physical Time (Myr)")
    plt.ylabel("Neutron Star Count")
    plt.savefig("{0}/{1}_counts_cumulative.png".format(output, option))

    plt.clf()

def plot_avg(data_dir, output, option):
    # TODO: Update var names to reflect that it may be single or binary
    single_accumulated = []
    max_time = 0

    for dir in glob.glob(data_dir):
        # Neutron star counts
        single_data = parse.parse_run(dir, option)
        single_accumulated.append(single_data)
        if (single_data[-1]['time'] > max_time):
            max_time = single_data[-1]['time']


    # single_accumulated is now a list of lists
    # Each internal list contains data fron a run
        
    split_delims = np.linspace(0, max_time, num=100)

    calculated = []
    prev_delim = 0
    for delim in split_delims:
        if delim == 0:
            continue
        # Go through each run_data_list and take the objects with time values < delim and values > prev_delim
        # Store those objects in a temporary list (store)
        store = []
        for run_data_list in single_accumulated:
            store += [x['stars'] for x in run_data_list if x['time'] > prev_delim and x['time'] <= delim]
        # calculate avg and std_dev of counts
        calculated.append({
            "avg": np.mean(store),
            "std_dev": np.std(store)
        })

        prev_delim = delim

    plt.errorbar(split_delims[1:], [x['avg'] for x in calculated], yerr=[x['std_dev'] for x in calculated], fmt='o')
    plt.title("Evolution of " + option + " Neutron Star Counts, Avg")
    plt.xlabel("Physical Time (Myr)")
    plt.ylabel("Neutron Star Count")
    plt.savefig("{0}/{1}_counts_avg.png".format(output, option))

    plt.clf()

