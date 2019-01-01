from matplotlib import pyplot as plt
import numpy as N
from mpl_toolkits.basemap import Basemap
from read_data import Dataset

def plot_raster(myData,darray):

    #rank=['1','2','3','4','5','6','7','8','9','10']

    #Map Setup -------------------------------------------------------------------------
    plotfile='testplot.png'
    dotsperinch=150
    #m = Basemap(llcrnrlon=-180.,llcrnrlat=7.,urcrnrlon=-11.,urcrnrlat=85.,projection='merc',lat_ts=30)
    m = Basemap(width=6000000,height=4500000,rsphere=(6378137.00,6356752.3142),resolution='l',area_thresh=1000.,projection='lcc',lat_1=30.,lat_2=40.,lat_0=35.,lon_0=-90)
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
    m.pcolormesh(myData.longrid,myData.latgrid,darray,latlon=True,cmap=plt.get_cmap('YlGnBu'))
    plt.colorbar()
    #plt.clim((0,4))

    #Plotting Point Data -------------------------------------------------------------
    #x,y=m(lonlist,latlist)
    #m.plot(lonlist,latlist,'bo',latlon=True)

    #Plotting Text -------------------------------------------------------------------
    #for rank, xc, yc in zip(rank, x, y):
    #    plt.text(xc+100000,yc+1000,rank,color='k')

    #Ancillary Plot Details ----------------------------------------------------------
    plt.title("Ten Densest Places in North America")

    #Save and Show the Plot -----------------------------------------------------------
    plt.savefig(plotfile,dpi=dotsperinch)
    plt.show()
    f.clear()

    return