#Import Python Libraries
import pandas as pd
import folium 
import geopandas as gpd
from folium.features import GeoJsonPopup, GeoJsonTooltip
import streamlit as st
from streamlit_folium import folium_static



#Add sidebar to the app
st.sidebar.markdown("# Visualização com Streamlit")
st.sidebar.markdown("Este é um simples exemplo de como criar Dashboards interativos utilizando a biblioteca Streamlit")
st.sidebar.markdown("É possível realizar muitas customizações de interfaces e construir Dashboards sofisticados porém, o intuito deste exemplo é apresentar como podemos construir interfaces abstraindo bastante conceitos de Desenvolvimento WEB.")

#Add title and subtitle to the main interface of the app
st.title("Cidades Brasileiras")
st.markdown("Uma breve apresentação das cidades brasileiras")


@st.cache_data
def read_file(path):
    return gpd.read_file(path)

#Read the geojson file
gdf = read_file('./geonames-postal-code.geojson')
gdf = gdf.astype({'admin_code1':'int'})

new = gdf.filter(['country_code','postal_code','place_name','admin_name1'], axis=1)
new.rename(columns = {'place_name':'city'}, inplace = True)
new.rename(columns = {'admin_name1':'state'}, inplace = True)


#Create two columns/filters
col1, col2 = st.columns(2)

with col1:
     state_list=new["state"].unique().tolist()
     state_list.sort(reverse=False)
     state = st.selectbox("Estados", state_list, index=0)

with col2:
     city_list=new["city"].unique().tolist()
     city_list.sort(reverse=False)
     state = st.selectbox("Cidades", city_list, index=0)


#Initiate a folium map
m = folium.Map(location=[-12, -52], 
               tiles="cartodbpositron",
               zoom_start=4)

#Plot Choropleth map using folium
choropleth1 = folium.Choropleth(
    geo_data='./geonames-postal-code.geojson',     #This is the geojson file for the Unite States
    name='Estados brasileiros',
    data=gdf,                                  #This is the dataframe we created in the data preparation step
    columns=['admin_name1', 'admin_code1'],                #'state code' and 'metrics' are the two columns in the dataframe that we use to grab the median sales price for each state and plot it in the choropleth map
    key_on='feature.properties.admin_code1',             #This is the key in the geojson file that we use to grab the geometries for each state in order to add the geographical boundary layers to the map
    fill_color='YlGn',
    nan_fill_color="White",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Cidades Brasileiras',
    highlight=True,
    line_color='black').geojson.add_to(m)

folium_static(m)
st.write(new)