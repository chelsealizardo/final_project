#!/usr/bin/env python
# coding: utf-8

# In[1]:


#For my final project, I decided to use some of what we have learned in class to create high quality maps that can be used to analyze datasets


# In[2]:


#The first thing we always have to do is import libraries. For this module I will be using pandas, numpy, matplotlib, scipy, and netCDF4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap  
from scipy import signal
import matplotlib.dates as dates


# In[3]:


#We start by opening the file that contains the variables we want to eventually plot. fh becomes the file handle of the open netCDF file, and the ‘r’ denotes that we want to open the file in read only mode.
my_example_nc_file = '../data/bay_of_fundy.grd' #use https://www.gmrt.org/GMRTMapTool/ Map tool to to create a NetCDF4 hi-resolution grid that identifies spatial resolution
fh = Dataset(my_example_nc_file, mode='r')


# In[4]:


#Then use the fh.variables operation to see what different variables you are able to access within this dataset. For this case, we want to use Latitude and Longitude 
fh.variables 


# In[4]:


#Assign a variable to the dataset that is being analyzed. In this case, we will be using data collected from the Bay of fundy which lies between Canada’s Nova Scotia and New Brunswick provinces, and Maine to analyze tide frequency throughout the day  
data_df = pd.read_csv('../data/tides.csv')

#We want to make sure that our data is correct and working, so we can use the data_df function to check that everyting looks the way it should.
data_df


# In[5]:


#We want to assign names to the variables that we want to use, which in this case are longitude, latitude, and altitude
longitude = fh.variables['lon'] [:]
latitude = fh.variables['lat'] [:]
altitude = fh.variables['altitude'] [:]


# In[6]:


#We also need to create a basemap to display the data on. Do this using the Basemap operation from the mpl_toolkits.basemap library
m = Basemap(projection='merc', llcrnrlat= 41.85646965, urcrnrlat=46.21937207, 
            llcrnrlon=-71.70996094, urcrnrlon=-62.49902344 , lat_ts=20, resolution='i') #llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlo are the lat/lon values of the lower left and upper right corners of the map.
#We want to use a mercator projection since its a cylindrical and conformal projection whic is ideal for this map. Keep in mind that this may not be the best projection for other maps 

#We can then check the number of variables in our list using the len() function.
print(len(altitude[0]))
print(len(altitude))


# In[8]:


#Now we can start to put our map together. We can use the matplotlib libraries to help us do this 
import matplotlib.colors #allows use to use color within matplotlib
from matplotlib.colors import LightSource #LightSource allows us to Create a light source coming from the specified azimuth and elevation. Angles are in degrees, with the azimuth measured clockwise from north and elevation up from the zero plane of the surface
from matplotlib import cm #cm lets us build color maps, allowing us to see changes is data more clearly

 
dlat = data_df['latitude'] #Assign variables to the dataframes that will be used 
dlon = data_df['longitude']
name = data_df['place']
high_time = data_df['185']
high_amount = data_df['186']

lonnew = [] #make a new numpy array for longitudes
latnew = [] #make a new numpy array for latitudes


# In[9]:


# We want to set up a for loop to keep the list index in range 
for i in range(0, len(dlon)):
    lonnew.append(dlon[i])
    latnew.append(dlat[i])
#print high_time 
print(high_time)


# In[10]:


##convert high tide start times to minutes (i.e 18:53 -> 53 )
high_time[0] = 53
high_time[1] = 55
high_time[2] = 24
high_time[3] = 26
high_time[4] = 31
high_time[5] = 49
high_time[6] = 51
high_time[7] = 56
high_time[8] = 55
high_time[9] = 26
high_time[10] = 68
high_time[11] = 55
high_time[12] = 35
high_time[13] = 105
high_time[14] = 99
high_time[15] = 7
high_time[16] = 122
high_time[17] = 56
high_time[18] = 14
high_time[19] = 9
high_time[20] = 0
high_time[21] = 20
high_time[22] = 93


# In[11]:


# Get image pixel locations from map longitude and latitude
x, y = m(lonnew, latnew)

#ls = and ve = help us set up false illuminations
ls = LightSource(azdeg=135, altdeg=30)
ve = 0.1 #This describes the intensity of the illumation

my_cmap =cm.terrain; #assign variable 

plt.figure(figsize=(30,16))
m.imshow(altitude, cmap=my_cmap, vmin=-257, vmax=257) #this allows you Display an image, i.e. data on a 2D regular raster.

#modifications that help us plot the color bar 
norm = matplotlib.colors.Normalize(vmin=-257 , vmax=257) #this instance is used to scale scalar data to the [0, 1] range before mapping to colors using cmap.
r = cm.ScalarMappable(cmap=my_cmap,norm=norm) #This is a mixin class to support scalar data to RGBA mapping. The ScalarMappable makes use of data normalization before returning RGBA colors from the given colormap.
r.set_array([]) #You need to use the function set_array([]) to get values used to generate the colors.
plt.colorbar(r, label='Elevation (m)') #This function allows us to add a colorbar to the map, which will show us the elevation of the terrain shown in the map 

#Add the relevant Basemap methods that allow us to draw in coastlines 

m.drawcoastlines()

# draw parallels and meridians. label parallels on right and top meridians on bottom and left
m.drawparallels(np.arange(40.,47.,.5),labels=[True,False,True,True]) #np.arange() just defines the coordinates you are working with, in this case these are the coordinates for the bay of fundy 
m.drawmeridians(np.arange(-71.,-63.,.5),labels=[False,True,True,False])

#Define some parameters for your scatterplot. Including x & y (The data positions), c (color), s (scalar shape), alpha (The alpha blending value)
plt.scatter(x, y, c='r', s=80, alpha=0.75) 


#Add another for loop to iterate over a sequence of text and layout properties
for i in range(0, len(name)):
    plt.text(x[i], y[i], " " + name[i], color='black', size=15, horizontalalignment='left', verticalalignment='center') #Properties for text in map (i.e locations and data points)
    plt.text(x[i], (y[i]), "\n\n" + str(high_time[i]), color='white', size=15, horizontalalignment='left', verticalalignment='center')
    plt.text(x[i], (y[i]), "\n\n\n\n" + str(high_amount[i]), color='r', size=15, horizontalalignment='left', verticalalignment='center')

#display the title
plt.title("Bay of Fundy", pad=40, fontsize=50)
plt.suptitle("By Chelsea Lizardo", x=.43, y=.05, fontsize=18)

plt.show()


# In[ ]:


#References I used to help me put together this notebook
#https://joehamman.com/2013/10/12/plotting-netCDF-data-with-Python/
#https://matplotlib.org/basemap/users/merc.html
#https://matplotlib.org/basemap/users/geography.html
#https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.LightSource.html
#https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.imshow.html
#https://www.gmrt.org/GMRTMapTool/
#http://bayoffundytourism.com/worlds-highest-tides/times/

