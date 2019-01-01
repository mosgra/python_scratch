import os, sys, re, stat, struct
import numpy as N
import array
from read_data import *
from data_proc import *
from plotting import plot_raster
import time
#from mpl_toolkits.basemap import maskoceans, interp

indata='C:\\Users\\Heather\\Documents\\Python Scripts\\data\\nap10ag.asc'
#fname='nads10ag.asc'
#indata=path+fname

print(indata)

stime = time.time()
myData = Dataset(indata)
print("Total time for reading data: "+str(time.time()-stime))

latlist,lonlist,filtered_data = rank_top10(myData)

#kmeans,darray = rank_top10_kmeans(myData)

#native data resolution
lats = N.linspace(myData.ullat,myData.lllat,myData.nrows)
lons = N.linspace(myData.lllon,myData.lllon+(myData.dx*myData.ncols),myData.ncols)
myData.longrid,myData.latgrid = N.meshgrid(lons,lats)
#land_only = maskoceans(longrid,latgrid,myData.darray)

#interpolate input data to higher-res grid to avoid blockiness along coastlines
#NOTE: This can cause memory errors with large grids!
#lats_hi = N.linspace(myData.ullat,myData.lllat,myData.nrows*2)
#lons_hi = N.linspace(myData.lllon,myData.lllon+(myData.dx*myData.ncols),myData.ncols*2)
#longrid_hi,latgrid_hi = N.meshgrid(lons_hi,lats_hi)
#darray_hires = interp(myData.darray,lons,lats[::-1],longrid_hi,latgrid_hi,checkbounds=True,order=1)

#longrid,latgrid = N.meshgrid(lons_hi,lats_hi)
#land_only = maskoceans(longrid,latgrid,myData.darray)

plot_raster(myData)