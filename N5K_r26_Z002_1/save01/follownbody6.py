import sys
import subprocess
import fileinput
import os
import time
import re
import numpy

#if the code is compiled for GPU, then set usegpu = True
#usegpu = False
#now set as an input 

#seconds, check the fort.2 output file at intervals of savetimes (and save new fort.2 files as checkpoints)
savetimes = 600 

#from params.h (double check this if reconfiguring the nbody code)
LMAX = 600 

#minimum time step allows
eta_min = 1e-4

#taken from http://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

#alist=[
#    "something1",
#    "something12",
#    "something17",
#    "something2",
#    "something25",
#    "something29"]
#
#alist.sort(key=natural_keys)
#print(alist)

def getinitdtadj():
  nl=0
  dtadj = 10.0
  for line in fileinput.input("input"):
      if (nl == 2) : dtadj=line.split()[3]
      nl+=1

  return float(dtadj)

def getinitvals():
  nl=0
  dtadj = 10.0
  etai = 0.02
  etar = 0.02
  nnbopt = 100
  for line in fileinput.input("input"):
      if (nl == 1) : nnbopt = int(line.split()[4])
      if (nl == 2) : 
          xx = line.split()
          etai = float(xx[0])
          etar = float(xx[0])
          dtadj = float(xx[3])
      nl+=1

  return dtadj, etai, etar, nnbopt

def makers_old(restart=False):
   nl=0
   rst=10.0
   rstimes=['10.0','5.0','2.0','1.0','0.5','0.0625','0.03125','0.001']
   toolow=False

   for line in fileinput.input("rs"):
      if (nl == 1) : rst=line.split()[0]  
      nl+=1

   pos=rstimes.index(rst)+1

   if (restart == True): pos=0

   if (pos >= len(rstimes)): 
      raise Exception('rstimes too low!')
   else:
      f = open('rs', 'w')
      f.write('3 1000000.0 0\n')
      f.write(rstimes[pos])
      f.write(' 0.0 0.0 0.0 0.0 0.0 0 0\n')
#      f.write(rst[1::])
      f.close()

   print '\n   Restarting with dt = ',rstimes[pos],'\n'

#I tried always forcing a manual stop and restarting at dt=10.0
#but this led to too many restarts and many cases without T6 in the logfiles
   if (pos >= 6) :
      subprocess.call('touch STOP',shell=True)
      print '\n   Forcing manual termination...\n'

def makers_old2(restart=False, dtadj = 10.0):
   nl=0
   rst=dtadj
   toolow=False

   Nmax = 2.**10. 
   line0 = '3 1000000.0 1.E6 40 40 640\n'

   for line in fileinput.input("rs"):
      if (nl == 0) : line0 = line
      if (nl == 1) : rst=float(line.split()[0])
      nl+=1

   if (restart == True): 
      rst = dtadj
   else:
      rst = rst/2.

   if (rst/dtadj < 1./Nmax): 
      raise Exception('rstimes too low!', rst, dtadj, rst/dtadj, Nmax)
   else:
      f = open('rs', 'w')
#      f.write('3 1000000.0 13000 40 40 640\n')
      f.write(line0)
      f.write(str(rst))
      f.write(' 0.0 0.0 0.0 0.0 0.0 0 0\n')
      f.close()

   print '\n   Restarting with dt = ',rst,'\n'

#I tried always forcing a manual stop and restarting at dt=10.0
#but this led to too many restarts and many cases without T6 in the logfiles
   if (rst/dtadj < 2./Nmax):
      subprocess.call('touch STOP',shell=True)
#      print '\n   Forcing manual termination...\n'
      raise Exception('Forcing manual termination.')

def getrsvals():
    eta1 = 0.02
    eta2 = 0.02
    nnbo = 100

    nl = 0
    for line in fileinput.input("rs"):
        if (nl == 0) : line0 = line
        if (nl == 1) : 
            xx = line.split()
            eta1 = float(xx[0])
            eta2 = float(xx[1])
            nnbo = int(xx[6])
        nl+=1
        
    return eta1, eta2, nnbo

def makers(restart = False, dtadj = 10.,  etai = 0.02, etar = 0.02, nnbopt = 100):
   global Nfort
   nl=0
   eta1 = etai
   eta2 = etar
   nnbo = nnbopt

   Nmax = 2.**10. 
   line0 = '4 1000000.0 1.E6 40 40 640\n'

   if (os.path.isfile('rs')):
       eta1, eta2, nnbo = getrsvals()

   if (restart == True): 
       eta1 = etai
       eta2 = etar
       nnbo = nnbopt
       print '\n   Starting with ETAI, ETAR, NNBOPT = ',eta1, eta2, nnbo,'\n'

   else:
      eta1 = eta1/2.
      eta2 = eta2/2.
      nnbo = int(round(nnbo + 20))
      print '\n   Restarting with ETAI, ETAR, NNBOPT = ',eta1, eta2, nnbo,'\n'


   if (nnbo > LMAX - 5):
#      print 'NNBOPT too high. Forcing manual termination', nnbo, eta1, eta2
#      subprocess.call('touch STOP',shell=True)
#      raise Exception('NNBOPT too high. Forcing manual termination', nnbo, eta1, eta2)
#      print '\n   Forcing manual termination...\n'
#      raise Exception('Forcing manual termination.')
#try to restart from the most recent savepoint before the one we're stuck at
      print 'NNBOPT too high. Trying subsequent savepoint', nnbo
      Nfort += 1
      return False

   elif (eta1 < eta_min or eta2 < eta_min):
      print 'etai and etar too low. Trying subsequent savepoint', eta1, eta2, eta_min
      Nfort += 1
      return False

   else:
      f = open('rs', 'w')
      f.write(line0)
      f.write(str(eta1) + ' ' + str(eta2) + ' 0 0 0 0 ' + str(nnbo) + ' 0\n')
      f.close()
      if (os.path.isfile('STOP')): 
          subprocess.call('rm -f STOP',shell=True)
      return True

def findprevfort2(dtadj = 10.,  etai = 0.02, etar = 0.02, nnbopt = 100, fatalnnb = False):
    global N, Nfort, restarted

#check for other fort.2 files
    dir='save'+str(N).zfill(2)
    print "trying to restart from a previous save point in "+dir, Nfort

    foundf2 = False
    mrs = False

    while (N > 0 and not foundf2):

#fort.2 file (always the most recent savepoint in a given directory)
        if (Nfort == -1):
            x = 1
            while (x == 1 and N > 0): 
                if (os.path.isfile('fort.1')):
                    print "WARNING: fort.1 file already exists in this directory -- removing..."
                    y = subprocess.call('rm -f fort.1',shell=True)
                x = subprocess.call('cp '+dir+'/fort.2 fort.1',shell=True)
                print x, 'cp '+dir+'/fort.2 fort.1'
                if (x == 1):
#if there is no fort.2 file in the directory, then there won't be any other savepoints there
# in that case, go up one level and start again at the fort.2 file (most recent savepoint)
                    print "No fort.2 file in "+dir
                    N -= 1
                    dir='save'+str(N).zfill(2)

            print "using fort.2 : ",dir+'/fort.2'
            test = numpy.where(numpy.logical_and(numpy.array(restarted["N"]) == N, numpy.array(restarted["Nfort"]) == Nfort))[0]
            print "test", test            
            if (len(test) > 0):
                print "already used this savepoint : ",restarted, test
                subprocess.call('cp '+dir+'/rs .',shell=True)
                subprocess.call('chmod +w rs',shell=True)
                eta1, eta2, nnbo = getrsvals()
                if (fatalnnb):
                    usennb = nnbopt
                else:
                    usennb = int(round(restarted["nnbopt"][test[-1]] + 20))
                mrs = makers(restart = True, etai = restarted["etai"][test[-1]]/2. , etar = restarted["etar"][test[-1]]/2. , nnbopt = usennb )
                eta1, eta2, nnbo = getrsvals()
            else:
                mrs = makers(restart = True, etai = etai, etar = etar, nnbopt = nnbopt)
                eta1, eta2, nnbo = getrsvals()
            
            if (mrs):
                restarted["N"].append(N)
                restarted["Nfort"].append(Nfort)
                restarted["etai"].append(eta1) #Note: These are going to contain the values before makers (e.g., twice eta1, eta2)
                restarted["etar"].append(eta2)
                restarted["nnbopt"].append(nnbo)
                foundf2 = True
                break
            else:
                if (os.path.isfile('fort.1')):
                    y = subprocess.call('rm -f fort.1',shell=True)

#go through the other savepoints
        else:
            p1 = subprocess.Popen(['ls', dir], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(['grep','fort.2.'], stdin=p1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            p1.stdout.close()
            out, err = p2.communicate()
            fort2s = out.splitlines()
            if (len(fort2s) > 0 and Nfort < len(fort2s)):
                fort2s.sort(key=natural_keys)
                fort2s.reverse()
                print fort2s
                cmd = 'cp '+dir+'/'+fort2s[Nfort] + ' fort.1'
                print cmd
                if (os.path.isfile('fort.1')):
                    print "WARNING: fort.1 file already exists in this directory -- removing..."
                    y = subprocess.call('rm -f fort.1',shell=True)
                subprocess.call(cmd,shell=True)
                print "found savepoint : ",dir+'/'+fort2s[Nfort]
                test = numpy.where(numpy.logical_and(numpy.array(restarted["N"]) == N, numpy.array(restarted["Nfort"]) == Nfort))[0]
                if (len(test) > 0):
                    subprocess.call('cp '+dir+'/rs .',shell=True)
                    subprocess.call('chmod +w rs',shell=True)
                    eta1, eta2, nnbo = getrsvals()
                    print "already used this savepoint : ",restarted, test
                    if (fatalnnb):
                        usennb = nnbopt
                    else:
                        usennb = int(round(restarted["nnbopt"][test[-1]] + 20))
                    mrs = makers(restart = True, etai = restarted["etai"][test[-1]]/2. , etar = restarted["etar"][test[-1]]/2. , nnbopt = usennb )
                    eta1, eta2, nnbo = getrsvals()
                else:
                    mrs = makers(restart = True, etai = etai, etar = etar, nnbopt = nnbopt)
                    eta1, eta2, nnbo = getrsvals()

                if (mrs):
                    restarted["N"].append(N)
                    restarted["Nfort"].append(Nfort)
                    restarted["etai"].append(eta1) #Note: These are going to contain the values before makers (e.g., twice eta1, eta2)
                    restarted["etar"].append(eta2)
                    restarted["nnbopt"].append(nnbo)
                    foundf2 = True
                    break
                else:
                    if (os.path.isfile('fort.1')):
                        y = subprocess.call('rm -f fort.1',shell=True)

            else:
                N -= 1
                Nfort = -1
#check for other fort.2 files
                dir='save'+str(N).zfill(2)
                print "trying to restart from a previous save point in "+dir, Nfort


    if (not foundf2):
        raise Exception("Cannot restart from previous fort.2 file.")


def waitnb(nb, constantcheck = False):


#wait until the nb process is completed
#but copy the fort.2 output file occasionally to new file so that we can have multiple restart points!
   fnum = 0
   while nb.poll() is None:
#     print "running",nb.poll()
#     sys.stdout.flush()

     tfort2_1 = 0.0
     if (os.path.isfile('fort.2')):

       if (os.stat('fort.2').st_mtime != tfort2_1):
         ADJUST = subprocess.Popen(['grep', 'ADJUST','logfile'], stdout=subprocess.PIPE).communicate()[0].splitlines()
         if (len(ADJUST) > 0):
           print ADJUST[-1]
         else:
           print 'WARNING: no adjust line in the logfile...'

         print 'saving fort.2 to fort.2.' + str(fnum)
         sys.stdout.flush()
         subprocess.call('cp fort.2 fort.2.' + str(fnum),shell=True)
         fnum += 1

       tfort2_1 = os.stat('fort.2').st_mtime
#       print tfort2_1, nb.poll()
       time1 = time.time()
       time2 = time1
       done = False
       while ( (os.stat('fort.2').st_mtime == tfort2_1) and (not done) ): 
#this is better than sleep because it should break out immediately when the code dies (though maybe this will slow things down with the constant time checks? -- yes, I think it slows down the code substantially for some reason)
         if (constantcheck):
             while ((time2 - time1) < savetimes):
                 time2 = time.time()
                 if nb.poll() is not None:
                     done = True
                     break
         else:
             if nb.poll() is not None:
                 done = True
                 break
             time.sleep(savetimes) #check this every 10 minutes
#         print "checking fort.2...",nb.poll()
#         sys.stdout.flush()

#  nb.wait()

def savework():
    global N, Nfort

    N += 1
    Nfort = -1
    dir='save'+str(N).zfill(2)
    while (os.path.exists(dir)):
        N += 1
        dir='save'+str(N).zfill(2)

    if (N > 99):
        raise Exception('TOO MANY SAVE POINTS! N = ',N)

    if not os.path.exists(dir):
        print '\n   Copying files to directory : ',dir,'\n'
        os.makedirs(dir)
        subprocess.call('cp * '+dir,shell=True)
        subprocess.call('./cleanup',shell=True)
        subprocess.call('chmod -w -R '+dir,shell=True)
    else:
        raise Exception('Directory exists',dir)


def follownbody6(dtadj = 10.,  etai = 0.02, etar = 0.02, nnbopt = 100, usegpu = False):
   global N, Nfort
    
   nnbopt0 = nnbopt

   done=False

#this starts the code from t=0
   if (N == 0) : 
      mrs = makers(restart=True, dtadj = dtadj, etai = etai, etar = etar, nnbopt = nnbopt)
      if (usegpu):
        nb=subprocess.Popen('./nbody6++.avx.gpu.mpi < input > logfile', shell=True)  
      else:
        nb=subprocess.Popen('./nbody6++.avx.mpi < input > logfile', shell=True)  
      print '\n pID = ',nb.pid,'\n'
      sys.stdout.flush()

#this restarts it from the current time
   if (N > 0) :
      subprocess.call('chmod +w fort.1',shell=True)
      if (usegpu):
        nb=subprocess.Popen('./nbody6++.avx.gpu.mpi < rs > logfile', shell=True)
      else:
        nb=subprocess.Popen('./nbody6++.avx.mpi < rs > logfile', shell=True)
      print '\n pID = ',nb.pid,'\n'
      sys.stdout.flush()

   
   waitnb(nb)

   print "nb process finished..."
   sys.stdout.flush()

#when the code comes back, check why it stopped and potentially restart it
   while (not done) :

      T6 = subprocess.Popen(['grep', 'T6','logfile'], stdout=subprocess.PIPE).communicate()[0]
      MAN = subprocess.Popen(['grep', 'MANUAL','logfile'], stdout=subprocess.PIPE).communicate()[0]
      ENDRUN = subprocess.Popen(['grep', 'END RUN','logfile'], stdout=subprocess.PIPE).communicate()[0]
      FATAL = subprocess.Popen(['grep', 'FATAL ERROR!   BAD INPUT   N =','logfile'], stdout=subprocess.PIPE).communicate()[0]
      found=False
      restart=False
      fatalnnb = False

#if there were no savepoints, try a smaller time step
      output = subprocess.Popen(['tail', 'logfile'], stdout=subprocess.PIPE).communicate()[0]

#in case for some reason there isn't a fort.2 now, but there was previously and we saved it -- doubtful that this would ever happen
      if (not os.path.isfile('fort.2') and not os.path.isfile('fort.2.0')):
#      if (len(T6) == 0 and len(MAN) == 0 and len(ENDRUN) == 0):
         print 'tail logfile : '
         print output
         dir='save'+str(N).zfill(2)
         print '\n   No save points detected.  Restarting from previous directory : ',dir,'\n'
         subprocess.call('./cleanup',shell=True)
 
#if there are savepoints, or a manual termination, or the end of the run, save the output, then restart
      else:

#determine what to do based on the logfile
         for line in output.split('\n'):
            if (('Stepsize' in line) or ('CALCULATIONS' in line) or ('./lib/cnbint.cpp' in line)):
               found=True
               print '\n',line,'\n'

            elif ('MANUAL' in line or len(MAN) != 0):
               found=True
               print '\n',line,'\n'
               restart=True

            elif ((('END' in line) and ('RUN' in line)) or len(ENDRUN) != 0):
               found=True
               print '\n',line,'\n'
               print 'DONE!'
               done=True
               break

#save this step
         savework()             

      if (done == False): 
         if (len(FATAL) != 0):
             nnbmax = FATAL.split()[9]
             print 'NNBMAX = ',nnbmax
             nnbopt = int(nnbmax) - 1 
             fatalnnb = True
         else:
#need to reset this each time
             nnbopt = nnbopt0
         findprevfort2(dtadj = dtadj, etai = etai, etar = etar, nnbopt = nnbopt, fatalnnb = fatalnnb)
         subprocess.call('chmod +w fort.1',shell=True)
         if (not fatalnnb):
             mrs = makers(restart=restart, dtadj = dtadj, etai = etai, etar = etar, nnbopt = nnbopt)
#I think that I have to run this even if mrs is False, or else we'll never get out of this loop
         if (usegpu):
           nb=subprocess.Popen('./nbody6++.avx.gpu.mpi < rs > logfile', shell=True)
         else:
           nb=subprocess.Popen('./nbody6++.avx.mpi < rs > logfile', shell=True)
         print '\n pID = ',nb.pid,'\n'
         sys.stdout.flush()
         waitnb(nb)

if __name__ == '__main__':

    global N, Nfort, restarted

#do not modify these
    N = 0
    Nfort = -1
    restarted =  {"N":[],  "Nfort":[], "etai":[], "etar":[], "nnbopt":[]}

#find the original DTADJ from the input file
    dtadj0, etai0, etar0, nnbopt0 = getinitvals()

    print '\n DTADJ, ETAI, ETAR, NNBOPT = ',dtadj0, etai0, etar0, nnbopt0, '\n'
    sys.stdout.flush()

#this is kind of a silly way to do this, but it should be fine for only two inputs
# the gpu flag must always come last
    usegpu = False
    if (len(sys.argv) > 1):
        if (sys.argv[1] == 'gpu'):
            usegpu = True
        else:
            N = int(sys.argv[1])
 
    if (len(sys.argv) > 2):
        if (sys.argv[1] == 'gpu' or sys.argv[2] == 'gpu'):
            usegpu = True


    follownbody6(dtadj = dtadj0, etai = etai0, etar = etar0, nnbopt = nnbopt0, usegpu = usegpu)

