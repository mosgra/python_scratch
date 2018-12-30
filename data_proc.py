import numpy as N
from read_data import Dataset
from sklearn.cluster import KMeans
from scipy.signal import medfilt2d
import time

def rank_top10_kmeans(myData):
    print(N.shape(myData.darray), myData.nrows, myData.ncols)
    myData.darray=N.reshape(myData.darray,(myData.nrows,myData.ncols))
    print("Done reshaping array.")
    sortedarray=N.sort(myData.darray, axis=None)
    print("Done sorting array.")
    sa2=sortedarray[::-1]
    print("Done reversing sorted array.")
    print("Maximum value: "+str(sa2[0]))
    print("Mean value: "+str(N.mean(myData.darray)))
    print("Standard Deviation: "+str(N.std(myData.darray)))

    #Example of applying a median filter to a 2-D grid using SciPy
    stime = time.time()
    filtered_data = medfilt2d(myData.darray,10)
    print("Total time for med filter: "+str(time.time()-stime))


    #Find the local maxes in the filtered grid
    stime = time.time()
    sortedarray=N.sort(filtered_data, axis=None)
    sa2=sortedarray[::-1] #Reverse an array order
    print("Total time for sorting: "+str(time.time()-stime))

    #The highest values after the median filter are the densest areas

    #Example of masking a 2-D array using masked_where
    stime = time.time()
    maskeddata = N.ma.masked_where(myData.darray<(N.mean(myData.darray)+3.0*(N.std(myData.darray))),myData.darray)
    print("Total time for masking: "+str(time.time()-stime))

    #Example of a k-means clustering in Scikit-Learn
    kmeans = KMeans(n_clusters=100)
    kmeans.fit(maskeddata)
    print(kmeans.cluster_centers_)
    print(kmeans.labels_)

    return kmeans,maskeddata

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