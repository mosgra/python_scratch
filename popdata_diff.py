#!/usr/bin/env python

import os, sys, re, stat, struct
import numpy as N
import array
from read_data import *
from data_proc import *
from plotting import plot_raster
from mpl_toolkits.basemap import maskoceans

inputformat='ascii' #My full code can open binary files, too
indata10='C:\\Users\\Heather\\Documents\\Python Scripts\\data\\nap10ag.asc'
indata90='C:\\Users\\Heather\\Documents\\Python Scripts\\data\\nap90ag.asc'

stime = time.time()
myData10 = Dataset(indata10)
myData90 = Dataset(indata90)
print("Total time for reading data: "+str(time.time()-stime))

trim_ascii(myData10,700,200,1300,1300)
#trim_ascii(myData90,500,500,1000,1000)

#native data resolution
lats = N.linspace(myData10.ullat,myData10.lllat,myData10.nrows)
lons = N.linspace(myData10.lllon,myData10.lllon+(myData10.dx*myData10.ncols),myData10.ncols)
myData10.longrid,myData10.latgrid = N.meshgrid(lons,lats)

#The log of the population data looks much nicer when plotted
logdarray10=N.log10(myData10.darray,where=(myData10.darray>0))
darray10_thresh=N.where(logdarray10>=0.0,logdarray10,0.0)
logdarray90=N.log10(myData90.darray,where=(myData90.darray>0))
darray90_thresh=N.where(logdarray90>=0.0,logdarray90,0.0)

land_only = maskoceans(myData10.longrid,myData10.latgrid,darray10_thresh)

#I removed the RBF code for now but it can still be found at:
#E:\python_scripts\aasg\exam\exam.py

plot_raster(myData10,land_only)

