# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:27:12 2020

Geofencing offset

@author: Guilherme De Moura Araujo (gdemoura@ucdavis.edu)

SUMMARY:
polygon_offset takes a set of 2D coordinates that make a polygon, an offseting
distance, and a desired direction to calculate new coordinates that make an
offset polygon.

INPUTS:
polygon: 2D array containing the coordinates of all vertices of a polygon
offset: desired offset distance
direction: direction at which the offset is desired 'i' for inward or 'o' for
outward
zone and letter: UTM zone at which the lat/long coordinates were collected

OUTPUT: 2D array containing the coordinates of all vertices
of the offset polygon (lat/long and UTM)
"""

def polygon_offset(geofence, offset, direction,zone,letter):
    import utm
    import numpy as np
    #Part 1: Define directional vectors for each side of the polygon and find
    #normal(perpendicular) vectors for each of directional vectors
    
    lat = geofence[0]
    long = geofence[1]
    UTM = utm.from_latlon(lat, long,zone,letter)
    x = list(UTM[0])
    y = list(UTM[1])
    x.append(x[0])
    y.append(y[0])
    
    dx = []
    dy = []
    n = []
    for i in range(0,len(x)-1):
        dx.append(x[i+1]-x[i])
        dy.append(y[i+1]-y[i])
        if dy[i] == 0:
            dy[i] = 1e-16 # Forces algorithm to converge if there's a horizontal line
        norm = np.sqrt(1 + (-dx[i]/dy[i])**2) # Normalizes perpendicular vector (||vector|| = 1)
        n.append([1/norm,(-dx[i]/dy[i])/norm]) # Create a normal vector to the current side of the polygon
        
    for i in range(0,len(n)): # Checks if normal vectors all point outwards and corrects them if not
        if dy[i] < 0:
            n[i][0] = n[i][0]*-1
            n[i][1] = n[i][1]*-1
            
  # Part 2: Define bisectors for each pair of normal vectors
  # Source: https://stackoverflow.com/questions/54033808/how-to-offset-polygon-edges  
        
    bis = []
    bis.append([(n[len(n)-1][0] + n[0][0])/np.sqrt(2),(n[len(n)-1][1] + n[0][1])/np.sqrt(2)])
    
    for i in range(1,len(n)):
        bis.append([(n[i-1][0] + n[i][0])/np.sqrt(2),(n[i-1][1] + n[i][1])/np.sqrt(2)])
        
    l = []
    l.append(offset/np.sqrt(1+np.dot(n[len(n)-1],n[0])))
    
    for i in range(1,len(n)):
        l.append(offset/np.sqrt(1+np.dot(n[i-1],n[i])))
    
    x_n = []
    y_n = []
    for i in range(0,len(x)-1):
        x_n.append(x[i]+l[i]*bis[i][0])
        y_n.append(y[i]+l[i]*bis[i][1])

    # Part 3: Checks orientation of dataset (clockwise vs. counter clockwise)
    # Calculate ratio of areas for original and new polygons.
    # If original area > new area --> Polygon was offset inwards
    # If original area < new area --> Polygon was offset outwards
    # Polygon offseting direction is checked against desired offsetting
    # direction and corrected accordingly.

    area_o = 0.0
    area_n = 0.0
    size = len(x_n)
    # Calculate value of shoelace formula 
    j = size - 1
    for i in range(0,size): 
        area_o += (x[j] + x[i]) * (y[j] - y[i])
        area_n += (x_n[j] + x_n[i]) * (y_n[j] - y_n[i]) 
        j = i   # j is previous vertex to i 
      
  
    # Return absolute value 
    area_o =  abs(area_o / 2.0)
    area_n =  abs(area_n / 2.0) 
    
    if area_o > area_n and direction == 'o' or area_o < area_n and direction == 'i':
        for i in range(0,len(n)):
            n[i][0] = n[i][0]*-1
            n[i][1] = n[i][1]*-1
        bis = []
        bis.append([(n[len(n)-1][0] + n[0][0])/np.sqrt(2),(n[len(n)-1][1] + n[0][1])/np.sqrt(2)])
    
        for i in range(1,len(n)):
            bis.append([(n[i-1][0] + n[i][0])/np.sqrt(2),(n[i-1][1] + n[i][1])/np.sqrt(2)])
        
        l = []
        l.append(offset/np.sqrt(1+np.dot(n[len(n)-1],n[0])))
    
        for i in range(1,len(n)):
            l.append(offset/np.sqrt(1+np.dot(n[i-1],n[i])))
    
        x_n = []
        y_n = []
        for i in range(0,len(x)-1):
            x_n.append(x[i]+l[i]*bis[i][0])
            y_n.append(y[i]+l[i]*bis[i][1])
            
    newpolygon_UTM = [x_n,y_n]
    newpolygon_latlong = utm.to_latlon(pd.Series(x_n), pd.Series(y_n), zone,letter)
    return newpolygon_latlong, newpolygon_UTM

#---------------------------------------------------------------------
# EXAMPLE CODE

import matplotlib.pyplot as plt
import pandas as pd
import utm
offset = 10 # 10 meters (about 30 ft)
direction = 'o' # --> Outward offset
zone = 10
letter = 's' # South

locations = ['Kemper+Bainer','MLS HQ','Mrak Hall roundabout','Kemper Hall']
loc = 0
# Load the coordinates of the locations for which data was collected
f1 = r'https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/example/irregular.csv'
f2 = r'https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/example/bainer.csv'
f3 = r'https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/example/mrak.csv'
f4 = r'https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/example/kemper.csv'
path = [f1,f2,f3,f4]
# Loop through the coordinates of all locations to create offset polygons
for i in path:
    fence = pd.read_csv(i)
    lat = fence.iloc[:,0]
    long = fence.iloc[:,1]
    # Array with [lat,long] coordinates
    geofence = [lat,long]
    [pol_latlong, pol_UTM] = polygon_offset(geofence, offset, direction,zone,letter)
    xn = pol_UTM[0]
    yn = pol_UTM[1]
    xn.append(xn[0])
    yn.append(yn[0])

    fence_UTM = utm.from_latlon(lat, long,10,'s')
    x = list(fence_UTM[0])
    y = list(fence_UTM[1])
    x.append(x[0])
    y.append(y[0])

    fig = plt.figure(i)
    ax = fig.add_subplot()
    plt.plot(x,y,'r-',label = 'Original')
    plt.plot(xn,yn,'b-',label='Offset')
    ax.set_aspect('equal',adjustable='box')
    plt.legend(loc = 'upper left',fontsize = 8)
    plt.title(locations[loc])
    loc = loc+1
