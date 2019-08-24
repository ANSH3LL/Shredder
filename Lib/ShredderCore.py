import os
import shutil
from APILib import PowerPlant

class FileShredder(object):
    def __init__(self, counter):
        self.nom = ''
        self.ext = ''
        self.shrd = 0 #Shred counter for whoever might need to use it
        self.counter = counter #Shred counter label
        self.ngen = PowerPlant()

    def __generate_rand_name(self):
        #Random Name generator
        self.ngen.select('alphanum')
        self.ngen.load_entropy(10)
        self.nom = self.ngen.generate()
        self.ngen.load_entropy(4)
        self.ext = self.ngen.generate()

    def __walker(self, a, b, c):
        #Recurse shredding files and skipping directories
        for x in c:
            if os.path.isdir('%s/%s' %(b, x)):
                pass
            else:
                self.shred_single('%s/%s' %(b, x))

    def rst_cntr(self): #Reset shred counter to zero when starting a new shred job
        self.shrd = 0

    def shred_single(self, fname):
        fsize = os.stat(fname)[6]
        #Rename file with random name
        self.__generate_rand_name()
        rname = '%s/%s.%s' %(os.path.dirname(fname), self.nom, self.ext)
        os.rename(fname, rname)
        #To support most RAM allowances
        if fsize <= 350000000:#<=350 MB
            #1st pass
            owdata = os.urandom(fsize)
            with open(rname, 'wb') as fobj:
                fobj.write(owdata)
            #2nd pass
            owdata = os.urandom(fsize)
            with open(rname, 'wb') as fobj:
                fobj.write(owdata)
            #3rd pass
            owdata = os.urandom(fsize)
            with open(rname, 'wb') as fobj:
                fobj.write(owdata)
            #Overwrite with 100MB of zeroes
            with open(rname, 'w') as fobj:
                fobj.write('0'*100000000)
            #Clean up...
            fobj = open(rname, 'w')
            fobj.close()
        #Huge files >350MB
        else:
            owchunks = fsize/1000
            #1st pass
            with open(rname, 'wb') as fobj:
                for x in range(1000):
                    fobj.write(os.urandom(owchunks))
            #Overwrite with 100MB of zeroes
            with open(rname, 'w') as fobj:
                fobj.write('0'*100000000)
            #Clean up...
            fobj = open(rname, 'w')
            fobj.close()
        #Delete file
        os.remove(rname)
        #Increment shred counter
        self.shrd += 1
        self.counter.config(text = self.shrd)

    def shred_multiple(self, folder, pfolder = True): #Preserves folders by default
        files_present = os.listdir(folder)
        files_present = ['%s/%s' %(folder, x) for x in files_present]
        for files in files_present:
            #Check for subdirectories and walk
            if os.path.isdir(files):
                os.path.walk(files, self.__walker, None)
            else:
                self.shred_single(files)
        #Finally, remove entire directory tree if not preserve flag
        if not pfolder:
            shutil.rmtree(folder)
        else:
            pass
