from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
import numpy as N
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.axes_grid1 import make_axes_locatable
from read_data import Dataset
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

#PROJ = ccrs.LambertConformal(central_longitude=-95.0,central_latitude=35.0,standard_parallels=[30,40])

#Assume this for now until we use data that is otherwise:
DATA_PROJ = ccrs.PlateCarree()

def plot_raster_c2py(myData,darray,ptlats,ptlons):

    #rank=['1','2','3','4','5','6','7','8','9','10']
    plotfile = 'testplot_c2py.png'
    dotsperinch = 150

    f = plt.figure()

    ax = get_c2py(myData,proj='cyl')

    #Ancillary Plot Details ----------------------------------------------------------
    plt.title("Population of North America: 2010")
    ax.set_xlabel("Latitude (deg)",labelpad=15)
    ax.set_ylabel("Longitude (deg)",labelpad=30)

    #Plotting Gridded Data -----------------------------------------------------------
    mesh = ax.pcolormesh(myData.longrid,myData.latgrid,darray,cmap=plt.get_cmap('YlGnBu'),transform=DATA_PROJ,zorder=1)

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="5%", pad=0.05, axes_class=plt.Axes)
    f.add_axes(ax_cb)
    plt.colorbar(mesh, cax=ax_cb,label="log(difference)")
    #plt.clim((0,4))

    #Plotting Point Data -------------------------------------------------------------
    ax.plot(ptlons,ptlats,'bo',transform=DATA_PROJ,zorder=3)

    #Plotting Text -------------------------------------------------------------------
    #for rank, xc, yc in zip(rank, x, y):
    #    plt.text(xc+100000,yc+1000,rank,color='k')

    #Save and Show the Plot -----------------------------------------------------------
    plt.savefig(plotfile,dpi=dotsperinch)
    plt.show()
    f.clear()

    return

def get_c2py(myData,proj='lcc'):
    if proj=='lcc':
        PROJ = ccrs.LambertConformal(central_longitude=-95.0,central_latitude=35.0,standard_parallels=[30,40])
    elif proj=='merc':
        PROJ = ccrs.Mercator(central_longitude=-95.0,min_latitude=myData.lllat,max_latitude=myData.ullat)
    elif proj=='cyl':
        PROJ = ccrs.PlateCarree(central_longitude=-95.0)

    ax = plt.axes(projection=PROJ)

    #Trim the extent a bit so we don't see edges of the data..set_extent doesn't work with Mercator
    ax.set_extent([myData.ullon+10.0, myData.ullon+(myData.dx*myData.ncols)-10.0, myData.lllat+10.0, myData.ullat-20.0])

    # Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

    #Add Map features
    ax.add_feature(cfeature.COASTLINE,zorder=3)
    ax.add_feature(cfeature.BORDERS,zorder=2)
    #ax.add_feature(cfeature.OCEAN,zorder=1)
    ax.add_feature(cfeature.LAKES,zorder=2)
    ax.add_feature(states_provinces,edgecolor='k',zorder=2) #linestyle=":",edgecolor='gray',zorder=1)
    ax.stock_img()

    if proj in ['merc','cyl']:
        #Add Latitude/Longitude Gridlines
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                    linewidth=2, color='gray', alpha=0.5, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_left = True
        gl.ylabels_right = False
        gl.xlines = True
        gl.xlocator = mticker.FixedLocator([-130, -120, -110, -100, -90, -80, -70, -60])
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 15, 'color': 'gray'}
        gl.xlabel_style = {'color': 'k'}

    return ax