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
            # In case the sev file is incorrectly formatted
            try:
                if int(data_line[1]) == NEUTRON_STAR: # second item in row is star type
                    counter += 1
            except ValueError:
                print "Incorrectly formatted sev file detected. Ignoring incorrecty formatted data from:"
                print sev_name

    return { "time": physical_time, "stars": counter }

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
        elif data[-1]['time'] < save_data[0]['time']:
            data += save_data
        else:
            # Iterate through data until an element with time >= than that of save_data[0]'s time is found
            index = 0
            for i in range(len(data)):
                if data[i]['time'] >= save_data[0]['time']:
                    index = i
                    break
            # Throw out all elements of data from that element onward
            data = data[:i]
            # Add save_data to the end of data
            data += save_data

    return data

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
        "save02",
    )
    print parse_save(data_dir)

def test_parse_run():
    data_dir = os.path.join(
        "/projects/b1011/ageller/NBODY6ppGPU/Nbody6ppGPU-newSE/run",
        "RgSun_NZgrid_BHFLAG2",
        "N10K_r26_Z02_11"
    )
    print parse_run(data_dir)

def main():
    test_parse_sev()
    test_parse_save()
    test_parse_run()

if __name__ == "__main__":
    main()
