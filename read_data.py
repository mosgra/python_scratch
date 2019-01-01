import os, sys, stat, struct
import numpy as N

class Dataset:
    dx=0
    dy=0
    ncols=0
    nrows=0
    dtype='int'
    dformat = 'asc'
    ullon=0
    ullat=0
    lllon=0
    lllat=0
    missing=-1
    darray=0
    latgrid=0
    longrid=0

    def __init__(self,infile):
        fname=infile

        self.datafromfile(fname)

    def datafromfile(self,fname):
        #first verify the file exists
        if not os.path.isfile(fname):
            raise IOError
    
        #try to guess file type from name
        items = fname.split('.')
        if 'bil' in items:
            self.dformat='bil'
            self.readbil(fname)
        elif 'asc' in items:
            self.dformat='asc'
            self.readascii(fname)
        else:
            print("READ ERROR: Unknown format. Exiting...")
            sys.exit()

    # Reading ASCII Grid file
    def readascii(self,fname):
        data=open(fname,'r')
        content=data.readlines()
        data.close()

        nline=0
        for line in content:
            line=line.strip()
            items=line.split()
            if nline==0:
                self.ncols=int(items[1])
                nline+=1
                continue
            elif nline==1:
                self.nrows=int(items[1])
                nline+=1
                continue
            elif nline==2:
                self.lllon=float(items[1])
                nline+=1
                continue
            elif nline==3:
                self.lllat=float(items[1])
                nline+=1
                continue
            elif nline==4:
                self.dx=float(items[1])
                nline+=1
                continue
            elif nline==5:
                self.missing=items[1]
                nline+=1
                continue
            elif nline==6:
                self.darray=N.zeros((self.nrows,self.ncols))
                nline+=1
                self.darray[0,:]=N.array(items[:], dtype='f')
                continue
            else:
                i=nline-6
                self.darray[i,:]=N.array(items[:], dtype='f')
                nline+=1

        self.ullon=self.lllon
        self.ullat=self.lllat+(float(self.nrows)*self.dx)

        print("Columns: "+str(self.ncols))
        print("Rows: "+str(self.nrows))
        print("LL Corner: "+str(self.lllon)+" "+str(self.lllat))
        print("UL Corner: "+str(self.ullon)+" "+str(self.ullat))
        print("Cellsize: "+str(self.dx))
        print("Missing Values: "+str(self.missing))
        #print "Shape of Array: ",N.shape(self.darray)
        print("Reading of ascii file complete.")
        #sys.exit()
        return


    #Code for reading .bil files adapted from:
    #http://arsf-dan.nerc.ac.uk/trac/attachment/wiki/Processing/SyntheticDataset/data_handler.py
    def readbil(self,fname):
        #Some variables we need to understand and read the binary data
        fileinfo=os.stat(fname)
        filesize=fileinfo[stat.ST_SIZE]

        #Read header information   
        header=open(fname,'r')
        content=header.readlines()
        header.close()
        for line in content:
            line=line.strip()
            items=line.split()
            if items[0]=='NROWS':
                self.nrows=int(items[1])
            elif items[0]=='NCOLS':
                self.ncols=int(items[1])
            elif items[0]=='NBANDS':
                nbands=int(items[1])
            elif items[0]=='NBITS':
                nbits=int(items[1])
                if nbits==16:
                    datatype='>h2'
                elif nbits==32:
                    datatype='>i4'
                bytesperpix=struct.calcsize(datatype)
                #print bytesperpix
            elif items[0]=='BANDROWBYTES':
                bandbytes=int(items[1])

        #Read lat/lon and resolution information
        geo=open(fname,'r')
        geodata=geo.readlines()
        self.dx=float(geodata[0].strip())
        self.ullon=float(geodata[4].strip())
        self.ullat=float(geodata[5].strip())

        #print ncols, nrows, ncols*nrows
        numlines=1
        pixperline=(float(filesize)/float(nbands))/float(numlines)/float(bytesperpix)
        print("Pixperline: "+str(pixperline))


        #Read data from binary .bil file
        data=open(fname,'rb')

        dlist=[]

        y=0
        while y<nbands:
            p=0
            while p<pixperline:
                databit=data.read(bytesperpix)
                #print databit

                datavalue=struct.unpack(datatype, databit)[0]
                dlist.append(datavalue)
                p+=1
            y+=1
        data.close()

        self.darray=N.array(dlist,(self.nrows,self.ncols))

        print("Reading of .bil file complete.")
        return

