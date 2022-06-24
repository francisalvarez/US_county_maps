import pandas as pd
import geopandas as gpd
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import os

def load_county_gdf():
    fp = 'data/raw/tl_2021_us_county/tl_2021_us_county.shp'
    gdf = gpd.read_file(fp)
    gdf['numbers'] = gdf['STATEFP'].astype(int)
    cols = ['STATEFP', 'COUNTYFP', 'COUNTYNS', 'GEOID', 'NAME', 'NAMELSAD', 'LSAD',
     'CLASSFP', 'MTFCC', 'CSAFP', 'CBSAFP', 'METDIVFP', 'FUNCSTAT', 'ALAND',
     'AWATER', 'INTPTLAT', 'INTPTLON', 'geometry']
    return gdf

def plot_county_heat():
    pass

def sample_chloropleth():
    df = px.data.election()
    geo_df = gpd.GeoDataFrame.from_features(
        px.data.election_geojson()["features"]
    ).merge(df, on="district").set_index("district")

    fig = px.choropleth(geo_df,
                        geojson=geo_df.geometry,
                        locations=geo_df.index,
                        color="Joly",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.show()

if __name__ == "__main__":

    gdf_county = load_county_gdf()
    CA = gdf_county.loc[gdf_county['STATEFP']=='06']
    CA["name"] = CA['NAME']
    CA = CA.set_index("NAME")

    fig = px.choropleth(CA,
                        geojson=CA.geometry,
                        locations=CA.index,
                        color="numbers",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)

    fig.add_scattergeo(lat=CA.INTPTLAT,
                       lon=CA.INTPTLON,
                       text=CA.name,
                       mode='text',
                       showlegend=False
                       )

    fig.show()
    # https: // community.plotly.com / t / annotations - on - plotly - choropleth / 36219 / 4