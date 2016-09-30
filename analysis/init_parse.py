from glob import glob
import os
from parseExceptions import *
import subprocess

# esc.11 file header
# Time[MYr]     M[M*]     EESC    VI[km/s]     K*    Name

def find_bh(read_file, write_file, Tstar):
    """
    Used by the bh_short() function to search a given file for black hole output, and write the information to a short file
    behavior changes based on the type of file to read:
         bev.82 for binary objects
         sev.83 for single objects
         hidat.87 for triple objects
         esc.11 for escaped objects
    refer to the NBody6++ manual for the output structure of these files
    """
    with open(read_file, 'r') as r, open(write_file, 'a') as w:
        if 'bev.82' in read_file:
            header = r.readline().split()
            w.write('time: ' + header[1] + '\n')
            w.write('binaries: ' + header[0] + '\n')
        elif 'sev.83' in read_file:
            header = r.readline().split()
            w.write('time: ' + header[1] + '\n')
            w.write('singles: ' + header[0] + '\n')
            header = r.readline().split()
            w.write('NC: ' + header[0] + '\n')
            w.write('RC: ' + header[1] + '\n')
            header = r.readline().split()
            w.write('RSCALE: ' + header[-1] + '\n')
        elif 'esc.11' in read_file:
            header = r.readline().split()
            if header != []:
                if header[4] == 14:
                    w.write(header)
        elif 'hidat.87' in read_file:
            while True:
                header = r.readline().split()
                if header != []:
                    if header[0] != 'NAME(I1)':
                        break
                    w.write('time: ' + str(float(header[-1]) * Tstar) + '\n')
                    #w.write('triples: ' + lineSplit[
        for line in r:
            lineSplit = line.split()
            if lineSplit != []:
                if 'sev.83' in read_file:
                    if lineSplit[1] == '14':
                        w.write(line)
                elif 'bev.82' in read_file:
                    if len(lineSplit) > 2:
                        if lineSplit[2] == '14' or lineSplit[3] == '14':
                            w.write(line)
                elif 'esc.11' in read_file:
                    if lineSplit[4] == '14':
                        w.write(line)
                elif 'hidat.87' in read_file:
                    if lineSplit[3] == '14' or lineSplit[4] == '14' or lineSplit[5] == '14':
                        w.write(line)

def bh_short(type, info=''):
    """
    Creates a short file by reading a set of NBody6++ output files
    Each short file is specific to a simulation (e.g. N10K_r10_Z01_1)
        and to a output file type (e.g. sev.83, bev.82, etc)
    The short file contains relevant metadata and any output relevant to a black hole (k=14)
    Calls find_bh()
    """
    write_file = type + '.short' + info
    grabFiles = subprocess.Popen('ls -1 {0}* | sed s/"_"/" "/ | sort -n -k 2 | sed s/" "/"_"/'.format(type), shell=True, stdout=subprocess.PIPE)
    stdout, stderr = grabFiles.communicate()
    inFileList = stdout.split()
    savePaths = subprocess.Popen('ls -d */', shell=True, stdout=subprocess.PIPE)
    stdout, stderr = savePaths.communicate()
    dirList = stdout.split()
    for dir in dirList:
        if 'save' in dir:
            os.chdir(dir)
            grabFiles = subprocess.Popen('ls -1 {0}* | sed s/"_"/" "/ | sort -n -k 2 | sed s/" "/"_"/'.format(type), shell=True, stdout=subprocess.PIPE)
            stdout, stderr = grabFiles.communicate()
            filesInDir = stdout.split()
            for dataFile in filesInDir:
                inFileList.append((dir + dataFile))
            os.chdir('../')
    if os.path.isfile(write_file):
        raise shortAlreadyExists('Short file already exists for this set')
    Tstar = 0
    if type == 'hidat.87':
        if os.path.isdir('save01/'):
            os.chdir('save01/')
            with open('logfile', 'r') as log:
                for line in log:
                    lineSplit = line.split()
                    if 'PHYSICAL' in lineSplit and 'SCALING:' in lineSplit:
                        Tstar = float(lineSplit[(lineSplit.index('T*') + 2)])
                        break
            os.chdir('../')
        elif os.path.isfile('logfile'):
            with open('logfile', 'r') as log:
                for line in log:
                    lineSplit = line.split()
                    if 'PHYSICAL' in lineSplit and 'SCALING:' in lineSplit:
                        print(lineSplit)
                        Tstar = float(lineSplit[(lineSplit.index('T*') + 2)])
                        break
        """
        with open(write_file, 'a+') as w:
            for read_file in inFileList:
                if read_file[:4] == 'save':
                    os.chdir(read_file[:6])
                    if os.path.isfile('logfile'):
                        with open('logfile', 'r') as log:
                            for line in log:
                                lineSplit = line.split()
                                if 'PHYSICAL' in lineSplit and 'SCALING' in lineSplit:
                                    Tstar = lineSplit[(lineSplit.index('T*') + 1)]
                                    break
                    os.chdir('../')
                else:
                    if os.path.isfile('logfile'):
                        with open('logfile', 'r') as log:
                            for line in log:
                                lineSplit = line.split()
                                if 'PHYSICAL' in lineSplit and 'SCALING' in lineSplit:
                                    Tstar = lineSplit[(lineSplit.index('T*') + 1)]
                                    break
                find_bh(read_file, write_file, Tstar)
    else:
        with open(write_file, 'a+') as w:
            for read_file in inFileList:
                find_bh(read_file, write_file, Tstar)
        """
    with open(write_file, 'a+') as w:
        for read_file in inFileList:
            find_bh(read_file, write_file, Tstar)

def bh_data(type, request='all', info='', meta_data={}):
    """
    Reads from a shortfile to creat a dictionary of the requested data, and a set of metadata
    'type' is a string of the requested short file type (e.g. 'sev.83')
    'request' is either the string 'all' or a list of numbers
        if 'all', the output dictionary will contain all data from the shortfile
        else the output dictionary will contain only the requested column numbers, with 'time' always being column 0
            refer to the NBody6++ manual for the the output of the various file types
    Calls bh_short(), _runoverLines()
    
    EDIT: No longer calles runoverLines, as the bug this function was meant to address has been fixed
    """
    read_file = type + '.short' + info
    if not os.path.isfile(read_file):
        bh_short(type, info)
    with open(read_file, 'r') as r:
        validTime = False
        timeStamp = 0
        bh_Data = []
        for line in r:
            tempLine = []
            finalLine = []
            line = line.split()
            if line[0] == 'time:':
                checkTime = str(line[1]).split('.')
                timeStamp = int(float(checkTime[0] + '.' + checkTime[1][0:5]))#added int to try and fix BHcount error
                validTime = True
                indexOffset = 0
            elif line[0] == 'singles:':
                if not timeStamp in meta_data:
                    meta_data[timeStamp] = {'singles' : int(line[1])}
                else:
                    meta_data[timeStamp]['singles'] = int(line[1])
            elif line[0] == 'binaries:':
                if not timeStamp in meta_data:
                    meta_data[timeStamp] = {'binaries' : int(line[1])}
                else:
                    meta_data[timeStamp]['binaries'] = int(line[1])
            elif line[0] == 'RC:':
                meta_data[timeStamp]['RC'] = line[1]
            elif line[0] == 'NC:':
                meta_data[timeStamp]['NC'] = line[1]
            elif line[0] == 'RSCALE:':
                meta_data[timeStamp]['RSCALE'] = line[1]
            elif validTime:
                line = [timeStamp] + line
                for index, item in enumerate(line):
                    """
                    if len(str(item)) > 10:
                        pass #for fixed runover line problem
                        #sepItems, n = _runoverLines(item, index, indexOffset, request)
                        #indexOffset = indexOffset + n
                        #for i in sepItems:
                        #    tempLine.append(float(i))
                    else:
                        tempLine.append(float(item))
                    """
                    tempLine.append(float(item))
            elif type == 'esc.11':
                line = [timeStamp] + line
                for item in line:
                    tempLine.append(float(item))
            elif type == 'hidat.87':
                line = [timeStamp] + line
                for item in line:
                    tempLine.append(float(item))
            """
            for j, k in enumerate(tempLine):
                if request == 'all':
                    finalLine.append(k)
                else:
                    if j in request:
                        finalLine.append(k)
            """
            if tempLine != []:# This for loop only for sims with missing KSTAR(ICM) column
                if "bev.82" in type:
                    tempLine = tempLine[:5] + ["XXX"] + tempLine[5:]
                if request == 'all':
                    finalLine = tempLine
                else:
                    for index in request:
                        finalLine.append(tempLine[index])
                bh_Data.append(finalLine)
    return bh_Data, meta_data


def _runoverLines(item, index, indexOffset, request):
    """
    Handles an error where there was no white space between data in the NBody6++ output
    
    EDIT: No longer used because the error has been fixed
    """
    n = len(item)/10
    it0 = float(item[0:(len(item)-n*10)])
    itList = [it0]
    for i in range(n):
        start = len(item) -n*10 + 10*i
        end = start + 10
        itList.append(float(item[start:end]))
    final = []
    for j, k in enumerate(itList):
        if request == 'all':
            final.append(itList[j])
        elif (index + j + indexOffset) in request:
            final.append(itList[j])
    return final, n

def genEscape(type):
    """
    Builds a function to parse the 'logfile' output for system escapes.
    For example:
        findBinaryEscape = genEscape('BINARY')
        list_of_binary_escapes = findBinaryEscape()
    """
    def specEscape():
        savePaths = subprocess.Popen('ls -d */', shell=True, stdout=subprocess.PIPE)
        stdout, stderr = savePaths.communicate()
        dirList = stdout.split()
        bEscData_temp = []
        for i, dir in enumerate(dirList):
            if 'save' in dir:
                awk_cmd = ('cat {0}'.format(dir) + 'logfile | awk \'{if ($1 ~ "ADJUST") TIME= $3 ; if ($1 ~ "' + type + '") print TIME, $0}\' | grep "' + type + ' ESCAPE" | sed s/"="/"= "/g'.format(type))
                stdout = subprocess.Popen(awk_cmd, shell=True, stdout=subprocess.PIPE)
                stdout = stdout.communicate()
                bEscData_temp = bEscData_temp + (stdout[0].split('\n'))
        bEscData = []
        for line in bEscData_temp:
            if line != '':
                line_split = line.split()
                if (line_split[12] == '14') and (line_split[13] == '14'):
                    bEscData.append(line)
        return bEscData
    return specEscape

def getHist(objNum, simDir='', saveLocation='', to_return=False):
    objNum = str(objNum)
    write_file = saveLocation + '/' + objNum + '.hist'
    print(write_file)
    curDir = os.getcwd()
    if simDir != '':
        os.chdir(simDir)
    fullFileList = []
    for type in ['sev.83', 'bev.82', 'hidat.87', 'esc.11']:
        grabFiles = subprocess.Popen('ls -1 {0}* | sed s/"_"/" "/ | sort -n -k 2 | sed s/" "/"_"/'.format(type), shell=True, stdout=subprocess.PIPE)
        stdout, stderr = grabFiles.communicate()
        inFileList = stdout.split()
        savePaths = subprocess.Popen('ls -d */', shell=True, stdout=subprocess.PIPE)
        stdout, stderr = savePaths.communicate()
        dirList = stdout.split()
        for dir in dirList:
            if 'save' in dir:
                os.chdir(dir)
                grabFiles = subprocess.Popen('ls -1 {0}* | sed s/"_"/" "/ | sort -n -k 2 | sed s/" "/"_"/'.format(type), shell=True, stdout=subprocess.PIPE)
                stdout, stderr = grabFiles.communicate()
                filesInDir = stdout.split()
                for dataFile in filesInDir:
                    inFileList.append((dir + dataFile))
                os.chdir('../')
        fullFileList = fullFileList + inFileList
    if os.path.isfile((saveLocation + write_file)):
        raise shortAlreadyExists('Hist file already exists for this set')
    Tstar = 0
    if os.path.isdir('save01/'):
        os.chdir('save01/')
        with open('logfile', 'r') as log:
            for line in log:
                lineSplit = line.split()
                if 'PHYSICAL' in lineSplit and 'SCALING:' in lineSplit:
                    Tstar = float(lineSplit[(lineSplit.index('T*') + 2)])
                    break
        os.chdir('../')
    elif os.path.isfile('logfile'):
        with open('logfile', 'r') as log:
            for line in log:
                lineSplit = line.split()
                if 'PHYSICAL' in lineSplit and 'SCALING:' in lineSplit:
                    print(lineSplit)
                    Tstar = float(lineSplit[(lineSplit.index('T*') + 2)])
                    break
    temp = curDir + '/temp'
    with open(temp, 'a') as w:
        for read_file in fullFileList:
            with open(read_file, 'r') as r:
                if 'bev.82' in read_file:
                    header = r.readline().split()
                    time = int(float(header[1]))
                    for line in r:
                        lineSplit = line.split()
                        if lineSplit[0] == objNum or lineSplit[1] == objNum:
                            w.write(('binary\t' + str(time) + '\t' + line))
                            #break
                if 'sev.83' in read_file:
                    header = r.readline().split()
                    time = int(float(header[1]))
                    for line in r:
                        lineSplit = line.split()
                        if lineSplit[0] == objNum:
                            w.write(('single\t' + str(time) + '\t' + line))
                            #break
                if 'hidat.87' in read_file:
                    while True:
                        header = r.readline().split()
                        if header != []:
                            if header[0] == 'NAME(I1)':
                                break
                            else:
                                time = int(float(header[-1]) * Tstar)
                    for line in r:
                        lineSplit = line.split()
                        if lineSplit[0] == objNum or lineSplit[1] == objNum or lineSplit[2] == objNum:
                            w.write(('triple\t' + str(time) + '\t' + line))
                            #break
                if 'esc.11' in read_file:
                    for line in r:
                        lineSplit = line.split()
                        if lineSplit != []:
                            if lineSplit[-1] == objNum:
                                w.write(('escape\t' + line))
                                #break
    lines = []
    with open(temp, 'r') as r:
        for line in r:
            print(line)
            lineSplit = line.split()
            lines.append(lineSplit)
    lines = sorted(lines, key = lambda row: int(float(row[1])))
    if os.path.exists(temp):
        os.remove(temp)
    if to_return:
        return lines
    with open(write_file, 'w') as w:
        for line_list in lines:
            line = ''
            for item in line_list:
                line = line + (str(item) + '\t')
            line = line + '\n'
            w.write(line)


