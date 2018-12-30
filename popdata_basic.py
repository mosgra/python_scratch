import os, sys, re, stat, struct
from matplotlib import pyplot as plt
import numpy as N
import array
from read_data import *
from data_proc import *
import time
from mpl_toolkits.basemap import Basemap
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
longrid,latgrid = N.meshgrid(lons,lats)
#land_only = maskoceans(longrid,latgrid,myData.darray)

#interpolate input data to higher-res grid to avoid blockiness along coastlines
#NOTE: This can cause memory errors with large grids!
#lats_hi = N.linspace(myData.ullat,myData.lllat,myData.nrows*2)
#lons_hi = N.linspace(myData.lllon,myData.lllon+(myData.dx*myData.ncols),myData.ncols*2)
#longrid_hi,latgrid_hi = N.meshgrid(lons_hi,lats_hi)
#darray_hires = interp(myData.darray,lons,lats[::-1],longrid_hi,latgrid_hi,checkbounds=True,order=1)

#longrid,latgrid = N.meshgrid(lons_hi,lats_hi)
#land_only = maskoceans(longrid,latgrid,myData.darray)

rank=['1','2','3','4','5','6','7','8','9','10']

#Map Setup -------------------------------------------------------------------------
plotfile='testplot.png'
dotsperinch=150
#m = Basemap(llcrnrlon=-180.,llcrnrlat=7.,urcrnrlon=-11.,urcrnrlat=85.,projection='merc',lat_ts=30)
m = Basemap(width=7000000,height=5000000,rsphere=(6378137.00,6356752.3142),resolution='l',area_thresh=1000.,projection='lcc',lat_1=30.,lat_2=40.,lat_0=35.,lon_0=-100)
f=plt.figure(figsize=(8,6))
ax = plt.gca()
#ax.set_facecolor('#3333CC')
m.drawcoastlines(color='#999999') # draw coastlines
m.drawmapboundary() # draw a line around the map region
m.drawparallels(N.arange(-90.,120.,10.),labels=[1,0,0,0]) # draw parallels
m.drawmeridians(N.arange(0.,420.,10.),labels=[0,0,0,1]) # draw meridians
m.drawstates(linewidth=0.5, color='#999999', antialiased=1, ax=None, zorder=None)
m.drawcountries(linewidth=0.5, color='#999999', antialiased=1, ax=None, zorder=None)

#Plotting Gridded Data -----------------------------------------------------------
#xgrid,ygrid = m(longrid,latgrid)
#m.pcolormesh(longrid_hi,latgrid_hi,land_only,latlon=True,cmap=plt.get_cmap('YlGnBu'))
#plt.colorbar()
#plt.clim((0,20000))

#Plotting Point Data -------------------------------------------------------------
x,y=m(lonlist,latlist)
#m.plot(lonlist,latlist,'bo',latlon=True)

#Plotting Text -------------------------------------------------------------------
for rank, xc, yc in zip(rank, x, y):
    plt.text(xc+100000,yc+1000,rank,color='k')

#Ancillary Plot Details ----------------------------------------------------------
plt.title("Ten Densest Places in North America")

#Save and Show the Plot -----------------------------------------------------------
#plt.savefig(plotfile,dpi=dotsperinch)
plt.show()
f.clear()