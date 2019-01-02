from matplotlib import pyplot as plt
import numpy as N
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.axes_grid1 import make_axes_locatable
from read_data import Dataset

PROJ = ccrs.LambertConformal(central_longitude=-95.0,central_latitude=35.0,standard_parallels=[30,40])
DATA_PROJ = ccrs.PlateCarree()

def plot_raster_c2py(myData,darray,ptlats,ptlons):

    #rank=['1','2','3','4','5','6','7','8','9','10']
    plotfile = 'testplot_diff.png'
    dotsperinch = 150

    # Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')


    f = plt.figure()
    ax = plt.axes(projection=PROJ)
    ax.set_extent([myData.ullon+10.0, myData.ullon+(myData.dx*myData.ncols)-10.0, myData.lllat+10.0, myData.ullat-20.0])
    ax.add_feature(cfeature.COASTLINE,zorder=3)
    ax.add_feature(cfeature.BORDERS,zorder=2)
    #ax.add_feature(cfeature.OCEAN,zorder=1)
    ax.add_feature(cfeature.LAKES,zorder=2)
    ax.add_feature(states_provinces,edgecolor='k',zorder=2) #linestyle=":",edgecolor='gray',zorder=1)
    #ax = plt.gca()

    #Ancillary Plot Details ----------------------------------------------------------
    plt.title("Population of North America: 2010")
    ax.set_xlabel("Latitude (deg)",labelpad=15)
    ax.set_ylabel("Longitude (deg)",labelpad=30)

    #Plotting Gridded Data -----------------------------------------------------------
    #xgrid,ygrid = m(myData.longrid,myData.latgrid)
    mesh = ax.pcolormesh(myData.longrid,myData.latgrid,darray,cmap=plt.get_cmap('YlGnBu'),transform=DATA_PROJ,zorder=1)
    #mesh = m.pcolormesh(myData.longrid,myData.latgrid,darray,latlon=True,cmap=plt.get_cmap('YlGnBu'),ax=ax)

    ax.stock_img()

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    #divider = make_axes_locatable(ax)
    #cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(mesh,label="log(difference)")
    #plt.clim((0,4))

    #Plotting Point Data -------------------------------------------------------------
    #x,y=m(lonlist,latlist)
    ax.plot(ptlons,ptlats,'bo',transform=DATA_PROJ,zorder=3)

    #Plotting Text -------------------------------------------------------------------
    #for rank, xc, yc in zip(rank, x, y):
    #    plt.text(xc+100000,yc+1000,rank,color='k')

    #Save and Show the Plot -----------------------------------------------------------
    plt.savefig(plotfile,dpi=dotsperinch)
    plt.show()
    f.clear()

    return