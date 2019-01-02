from matplotlib import pyplot as plt
import numpy as N
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from read_data import Dataset

def two_horiz_subplots(myData,darray1,darray2):
    f,(ax1,ax2) = plt.subplots(1, 2, sharey=True)
    f.set_figheight(4)
    f.set_figwidth(10)
    f.subplots_adjust(left=0.05, right=0.95, wspace=0.2)

    #Set up Map -------------------------------------------------------------------------
    plotfile='testplot_subplots.png'
    dotsperinch=150

    grids = [darray1,darray2]
    axes = [ax1,ax2]
    year = ["2010","1990"]

    #Subplot details ------------------------------------------------------------------
    for i in range(2):
        #plt.subplot(1, 2, i+1)
        axis = axes[i]
        axis.set_title("Population of North America - "+year[i])
        axis.set_xlabel("Latitude (deg)",labelpad=15)
        axis.set_ylabel("Longitude (deg)",labelpad=30)

        m = get_bmap(axis,myData,proj='merc')

        mesh = m.pcolormesh(myData.longrid,myData.latgrid,grids[i],latlon=True,cmap=plt.get_cmap('YlGnBu'),ax=axis)

        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        divider = make_axes_locatable(axis)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(mesh,cax=cax,label="log(population)")

    #Figure details to go outside the subplots 
    #plt.tight_layout()  


    #Save and Show the Plot -----------------------------------------------------------
    plt.savefig(plotfile,dpi=dotsperinch)
    plt.show()
    f.clear()

    return


def plot_raster(myData,darray,ptlats,ptlons):

    #rank=['1','2','3','4','5','6','7','8','9','10']
    plotfile = 'testplot_diff.png'
    dotsperinch = 150

    f = plt.figure()
    ax = plt.gca()

    #Ancillary Plot Details ----------------------------------------------------------
    plt.title("Population Change in North America: 1990-2010")
    ax.set_xlabel("Latitude (deg)",labelpad=15)
    ax.set_ylabel("Longitude (deg)",labelpad=30)

    #Get Basemap
    m = get_bmap(ax,myData,proj='merc')

    #Plotting Gridded Data -----------------------------------------------------------
    #xgrid,ygrid = m(longrid,latgrid)
    mesh = m.pcolormesh(myData.longrid,myData.latgrid,darray,latlon=True,cmap=plt.get_cmap('RdBu_r'),ax=ax)
    #mesh = m.pcolormesh(myData.longrid,myData.latgrid,darray,latlon=True,cmap=plt.get_cmap('YlGnBu'),ax=ax)

    

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(mesh,cax=cax,label="log(difference)")
    #plt.clim((0,4))

    #Plotting Point Data -------------------------------------------------------------
    #x,y=m(lonlist,latlist)
    m.plot(ptlons,ptlats,'bo',latlon=True)

    #Plotting Text -------------------------------------------------------------------
    #for rank, xc, yc in zip(rank, x, y):
    #    plt.text(xc+100000,yc+1000,rank,color='k')

    #Save and Show the Plot -----------------------------------------------------------
    plt.savefig(plotfile,dpi=dotsperinch)
    plt.show()
    f.clear()

    return

def get_bmap(self,myData,proj='lcc'):
    if proj=='merc':
        m = Basemap(ax=self,llcrnrlon=myData.lllon,llcrnrlat=myData.lllat,urcrnrlon=(myData.lllon+(myData.dx*myData.ncols)),urcrnrlat=myData.ullat,projection='merc',lat_ts=30)
    elif proj=='cyl':
        m = Basemap(ax=self,llcrnrlon=myData.lllon,llcrnrlat=myData.lllat,urcrnrlon=(myData.lllon+(myData.dx*myData.ncols)),urcrnrlat=myData.ullat,projection='cyl')
    elif proj=='lcc':
        m = Basemap(ax=self,width=6000000,height=4500000,rsphere=(6378137.00,6356752.3142),resolution='l',area_thresh=1000.,projection='lcc',lat_1=30.,lat_2=40.,lat_0=35.,lon_0=-90)

    #ax.set_facecolor('#3333CC')
    m.drawcoastlines(color='#999999') # draw coastlines
    m.drawmapboundary() # draw a line around the map region
    m.drawparallels(N.arange(-90.,120.,10.),labels=[1,0,0,0]) # draw parallels
    m.drawmeridians(N.arange(0.,420.,10.),labels=[0,0,0,1]) # draw meridians
    m.drawstates(linewidth=0.5, color='#999999', antialiased=1, ax=None, zorder=None)
    m.drawcountries(linewidth=0.5, color='#999999', antialiased=1, ax=None, zorder=None)

    return m