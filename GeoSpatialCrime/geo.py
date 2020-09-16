import pandas as pd
import folium
import math
from folium.plugins import MarkerCluster,HeatMap
import plotly.graph_objects as go
import plotly.express as px
import datetime 
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv("boston-crime 2.csv")
print(df.head(3))

####    generate base map    ####
boston=(42.358443,-71.05977)
m=folium.Map(location=boston,tiles='Stamen terrain',zoom_start=12)

""""    This part is used to display the map outside of any jupyter or colab notebook
        folium by default doesn't have a function to display the maps"""
import os
import webbrowser
filepath='C:/GeoSpatialCrime/map1.html'
m.save(filepath)
webbrowser.open('file://'+filepath)

        ####    Mark Crime Scenes    ####
mc=MarkerCluster()
for idx,row in df.iterrows():
  if not math.isnan(row['Long']) and not math.isnan(row['Lat']):
    mc.add_child(folium.Marker([row['Lat'],row['Long']]))
m.add_child(mc)

        ####  map the district with the highest crime  ####
crime=df.groupby(['DISTRICT','STREET','REPORTING_AREA','Lat','Long']).sum().reset_index()

crime.update(crime['DISTRICT'].map('districts:{}'.format))
crime.update(crime['REPORTING_AREA'].map('reports:{}'.format))

                #generate the map
m2=folium.Map(location=boston,tiles='Stamen Toner',zoom_start=12)
HeatMap(data=crime[['Lat','Long']],radius=15).add_to(m2)

        ####    markers   #####
def plotDot(point):
  folium.CircleMarker(location=[point.Lat,point.Long],
                      radius=5,
                      weight=2,
                      popup=[point.DISTRICT,point.REPORTING_AREA],
                      fill_color='#000000').add_to(m2)

crime.apply(plotDot,axis=1)
m2.fit_bounds(m2.get_bounds())

filepath='C:/GeoSpatialCrime/map2.html'
m2.save(filepath)
webbrowser.open("file://"+filepath)

        ####    medical assistance analysis  ######
med=df.loc[df.OFFENSE_CODE_GROUP=='Medical Assistance'][['Lat','Long']]
med.Lat.fillna(0,inplace=True)
med.Long.fillna(0,inplace=True)
m3=folium.Map(location=boston,tiles='openstreetmap',zoom_start=11)

                #generate heat map
HeatMap(data=med,radius=16).add_to(m3)
filepath='C:/GeoSpatialCrime/map3.html'
m3.save(filepath)
webbrowser.open("file://"+filepath)

        ####    crimes committed    ####
sns.catplot(y='OFFENSE_CODE_GROUP',
            kind='count',
            height=8,
            aspect=1.5,
            order=df.OFFENSE_CODE_GROUP.value_counts().index,
            data=df)

plt.show()

        ####  motor vehicle accident response ####
mv=df.loc[df.OFFENSE_CODE_GROUP=='Motor Vehicle Accident Response'][['Lat','Long']]
mv.fillna(0,inplace=True)
mv.Lat.fillna(0,inplace=True)
mv.Long.fillna(0,inplace=True)
m4=folium.Map(location=boston,tiles='openstreetmap',zoom_start=11)
HeatMap(data=mv,radius=16).add_to(m4)
filepath='C:/GeoSpatialCrime/map4.html'
m4.save(filepath)
webbrowser.open("file://"+filepath)

        ####   larceny   ####
lar=df.loc[df.OFFENSE_CODE_GROUP=='Larceny'][['Lat','Long']]
lar.fillna(0,inplace=True)
lar.Lat.fillna(0,inplace=True)
lar.Long.fillna(0,inplace=True)
m5=folium.Map(location=boston,tiles='openstreetmap',zoom_start=11)
HeatMap(data=lar,radius=16).add_to(m5)
filepath='C:/GeoSpatialCrime/map5.html'
m5.save(filepath)
webbrowser.open("file://"+filepath)



