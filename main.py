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
    gdf['numbers_2'] = range(len(gdf['STATEFP']))
    gdf['text_numbers_2'] = "<br><br>" + gdf['numbers_2'].astype(str)
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

def running_example(gdf_county):
    CA = gdf_county.loc[gdf_county['STATEFP'] == '06']
    CA["name"] = CA['NAME']
    CA = CA.set_index("NAME")

    fig = px.choropleth(CA,
                        geojson=CA.geometry,
                        locations=CA.index,
                        color="numbers_2",
                        color_continuous_scale="Greens",
                        width=1800,
                        height=1200,
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)

    # https: // community.plotly.com / t / annotations - on - plotly - choropleth / 36219 / 4
    fig.add_scattergeo(lat=CA.INTPTLAT,
                       lon=CA.INTPTLON,
                       text=CA.name,
                       mode='text',
                       showlegend=False,
                       textfont=dict(
                           family="sans serif",
                           size=14,
                           color="Black")
                       )

    fig.add_scattergeo(lat=CA.INTPTLAT,
                       lon=CA.INTPTLON,
                       text=CA.text_numbers_2,
                       mode='text',
                       showlegend=False,
                       textfont=dict(
                           family="arial",
                           size=14,
                           color="Red")
                       )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Number of <> per County",
            # tickvalues=[0, 1, 2, 3],
            # ticklabels=[
            #     "No measures",
            #     "Recommend closing",
            #     "Require closing (only some levels)",
            #     "Require closing all levels",
            # ],
        )
    )
    # Updated Layout for 'Title with Font Size 8' and 'Narrower Legend'


    return fig


if __name__ == "__main__":

    DIRS = {'imgs': 'images'}
    if not os.path.exists(DIRS['imgs']):
        os.mkdir(DIRS['imgs'])

    gdf_county = load_county_gdf()

    fig = running_example(gdf_county)
    # fig.write_image(os.path.join(DIRS['imgs'], "fig1.png"), scale=20)
    fig.write_image(os.path.join(DIRS['imgs'], "fig1.png"))
    # fig.show()