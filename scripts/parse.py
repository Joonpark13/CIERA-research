#!/user/bin/env python
"""Helper modules for neutron star data parsing."""

import os
import glob

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

def parse_sev(sev_name):
    counter = 0
    with open(sev_name, 'r') as f:
        row = f.readline().split()

        # Physical time is the second item in the first line
        physical_time = float(row[1])

        # Skip the header
        for _ in range(2):
            next(f)

        # Count the number of neutron stars in this file (timestep)
        for line in f:
            data_line = line.split()
            if int(data_line[0]) == -1000: # -1000 is sentinel value indicating EOF
                return { "time": physical_time, "stars": counter }
            try:
                if int(data_line[1]) == NEUTRON_STAR: # second item in row is star type
                    counter += 1
            # In case the sev file is incorrectly formatted
            except ValueError:
                print "Incorrectly formatted sev file detected. Ignoring incorrecty formatted data from:"
                print sev_name

    # This should only be required in case there is no -1000 EOF value
    return { "time": physical_time, "stars": counter }

def parse_bev(bev_name):
    count = 0
    with open(bev_name, 'r') as f:
        row = f.readline().split()

        # Physical time is the second item in the first line
        physical_time = float(row[1])

        for line in f:
            data_line = line.split()
            # third item in row is first star type
            if int(data_line[2]) == NEUTRON_STAR:
                count += 1
            # fourth item in row is second star type
            if int(data_line[3]) == NEUTRON_STAR:
                count += 1

    return { "time": physical_time, "stars": count }

def parse_save(save_dir):
    sev_files = os.path.join(save_dir, "sev.83_*")

    data = []
    for filename in glob.glob(sev_files):
        data.append(parse_sev(filename))

    # Sort by physical time
    # http://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
    return sorted(data, key=lambda k: k['time'])

def parse_run(run_dir):
    save_dirs = os.path.join(run_dir, "save*")

    data = []
    for dirname in glob.glob(save_dirs):
        save_data = parse_save(dirname)
        if len(save_data) is 0:
            continue

        if len(data)is 0:
            data = save_data
        # Make sure there is no overlap
        elif len(save_data) > 0 and data[-1]['time'] < save_data[0]['time']:
            data += save_data
        else:
            index = 0
            for i in range(len(data)):
                # In case of overlapping data between save files
                if len(save_data) > 0 and data[i]['time'] >= save_data[0]['time']:
                    index = i
                    break
            # Throw out all elements of data from that element onward
            data = data[:index] # If no overlap detected, this line will do nothing.
            # Add save_data to the end of data
            data += save_data

    return data

def parse_single_esc(save_dir):
    escape_times = []
    with open(os.path.join(save_dir, "esc.11"), 'r') as f:
        try:
            # Skip the header
            next(f)
        except StopIteration: # Empty file
            return []

        for line in f:
            data_line = line.split()
            # 5th item in row is star type
            type = data_line[4]

            if int(type) == NEUTRON_STAR:
                escape_times.append(float(data_line[0])) # Physical time is the first item in each row

    return escape_times

def parse_single_run_esc(run_dir):
    save_dirs = os.path.join(run_dir, "save*")

    escapes = []
    for dirname in glob.glob(save_dirs):
        save_escapes = parse_single_esc(dirname)

        # Check for overlap
        index = len(escapes)
        for i in range(len(escapes)):
            if len(save_escapes) > 0 and escapes[i] >= save_escapes[0]:
                index = i
                break
        # Throw out all overlapping elements from earlier save files
        escapes = escapes[:index] # If no overlap detected, this line will do nothing.
        # Append new data from savefile.
        escapes += save_escapes

    return escapes


def test_parse_sev():
    data_dir = os.path.join(
        "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
        "RgSun_NZgrid_BHFLAG2",
        "N10K_r26_Z02_11",
        "save02",
        "sev.83_105"
    )
    print parse_sev(data_dir) # Should be around 69.43697 and 16 respectively

def test_parse_save():
    data_dir = os.path.join(
        "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
        "RgSun_NZgrid_BHFLAG2",
        "N10K_r26_Z02_11",
        "save02"
    )
    print parse_save(data_dir)

def test_parse_run():
    data_dir = os.path.join(
        "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
        "RgSun_NZgrid_BHFLAG2",
        "N10K_r26_Z02_11"
    )
    print parse_run(data_dir)

def test_parse_single_esc():
    data_dir = os.path.join(
        "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
        "RgSun_NZgrid_BHFLAG2",
        "N10K_r26_Z02_11",
        "save02"
    )
    print parse_single_esc(data_dir)

def test_parse_single_run_esc():
    data_dir = os.path.join(
        "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
        "RgSun_NZgrid_BHFLAG2",
        "N10K_r26_Z02_11"
    )
    print parse_single_run_esc(data_dir)

def test_parse_bev():
    data_dir = os.path.join(
        "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
        "RgSun_NZgrid_BHFLAG2",
        "N10K_r26_Z02_11",
        "save02",
        "bev.82_805"
    )
    print parse_bev(data_dir)

def main():
    # test_parse_sev()
    # test_parse_save()
    # test_parse_run()
    # test_parse_single_esc()
    # test_parse_single_run_esc()
    test_parse_bev()

if __name__ == "__main__":
    main()
