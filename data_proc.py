import numpy as N
from read_data import Dataset
from sklearn.feature_extraction import image
from scipy.signal import medfilt2d
import time
import matplotlib.pyplot as plt

def trim_ascii(myData,top,bot,left,right):
    if N.max([top,bot])>myData.nrows or N.max([left,right])>myData.ncols:
        print("ERROR: Attempting to trim more than the dimension of the array!")
        raise ValueError

    myData.darray = myData.darray[top:(myData.nrows-bot),left:(myData.ncols-right)] 
    #myData.darray = myData.darray[500:1500,1000:3000] 

    #now reset the metadata
    myData.lllon = myData.lllon+(myData.dx*left)
    myData.lllat = myData.lllat+(myData.dx*bot)
    myData.ullat = myData.ullat-(myData.dx*top)
    myData.ullon = myData.lllon
    myData.ncols = myData.ncols - (left+right)
    myData.nrows = myData.nrows - (top+bot)

    return

#sorting a numpy array example
def rank_top10(myData):
    cluster=1

    print(N.shape(myData.darray), myData.nrows, myData.ncols)
    myData.darray=N.reshape(myData.darray,(myData.nrows,myData.ncols))
    print("Done reshaping array.")
    #sortedarray=N.sort(myData.darray, axis=None)
    #print("Done sorting array.")
    #sa2=sortedarray[::-1]
    #print("Done reversing sorted array.")
    #print("Maximum value: "+str(sa2[0]))
    #print("Mean value: "+str(N.mean(myData.darray)))
    #print("Standard Deviation: "+str(N.std(myData.darray)))


    #Example of applying a median filter to a 2-D grid using SciPy
    stime = time.time()
    filtered_data = medfilt2d(myData.darray,3)
    print("Total time for med filter: "+str(time.time()-stime))

    #Find the local maxes in the filtered grid
    stime = time.time()
    sortedarray=N.sort(filtered_data, axis=None)
    sa2=sortedarray[::-1] #Reverse an array order
    print("Total time for sorting: "+str(time.time()-stime))

    #The highest values after the median filter are the densest areas

    n=0
    x=0
    mapx=[]
    mapy=[]
    latlist=[]
    lonlist=[]

    #Find the 10 highest areas
    #X=found areas, N=length of sorted list, Z=number of bins matching the data value
    while x<10:
        location=N.where(myData.darray==sa2[n])
        #print location

        #Z checks if there are multiple pixels with the same value
        z=0
        while z<len(location[0]):
            #print z
            latitude=myData.ullat-(float(location[0][z])*myData.dx)
            longitude=float(location[1][z])*myData.dx+myData.lllon
            #print "X: "+str(x)+" Latitude: "+str(latitude)+" Longitude: "+str(longitude)+" Population: "+str(sa2[n])
            if latitude<=15.0 or longitude>=-60.0: #Ignore Africa and Central/South America
                z+=1
                n+=1
                continue
            elif latitude<=24.5 and longitude>=-85.0: #Caribbean domain
                z+=1
                n+=1
                continue

            if n==0:
                latlist.append(latitude)
                lonlist.append(longitude)
                mapx.append(int(location[1][z]))
                mapy.append(int(location[0][z]))
                #print "X: "+str(x)+" Latitude: "+str(round(latitude,2))+" Longitude: "+str(round(longitude,2))+" Population: "+str(sa2[n])
                x+=1
            else:
                i=0
                proximity=0

                while i<len(latlist):
                    latdiff=abs(latitude-latlist[i])
                    londiff=abs(longitude-lonlist[i])
                    if cluster==1:
                        if latdiff<1.0 and londiff<1.0:
                            proximity=1
                            i=len(latlist)
                        else:
                            i+=1
                    else:
                        i+=1
                if proximity==1:
                    n+=1
                    z+=1
                    continue
                else:
                    latlist.append(latitude)
                    lonlist.append(longitude)
                    mapx.append(int(location[1][z]))
                    mapy.append(int(location[0][z]))
                    #print "X: "+str(x)+" Latitude: "+str(round(latitude,2))+" Longitude: "+str(round(longitude,2))+" Population: "+str(sa2[n])
                    if x==9: z=len(location[0])
                    x+=1
            n+=1
            z+=1

    return N.array(latlist),N.array(lonlist),filtered_data