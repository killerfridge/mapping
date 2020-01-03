import dash_core_components as dcc
import dash_html_components as html
import dash
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import json
import geopandas as gpd
import os

MAPBOX_TOKEN = 'pk.eyJ1Ijoia2lsbGVyZnJpZGdlIiwiYSI6ImNrNGUzNnBjdTA4c2czZWxoNjJ3MjY4ajYifQ.Nf_B_iK2zst6vGvgYT6YRQ'
app = dash.Dash(__name__)

ROOT_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(ROOT_DIR, 'data')


def df_from_folder(folder):

    path = os.path.join(DATA_DIR, folder)
    path = os.path.join(path, f'{folder}.shp')
    tmp = gpd.read_file(path)
    return tmp.to_crs({'init': 'epsg:4326'})


df = df_from_folder('Sustainability_and_Transformation_Partnerships_April_2019_EN_BFC')

# print(df.columns)
# df.to_file('ccg.geojson', driver='GeoJSON')

with open('stp.json', 'r') as f:
    cancer_json = json.load(f)


app.layout = html.Div([
        html.H1('This is where the header is'),
        dcc.Graph(
            id='country-choropleth',
            figure=dict(
                data=[dict(
                    lat=df['lat'],
                    lon=df['long'],
                    text=df['stp19nm'],
                    type='scattermapbox',
                    marker=dict(
                        size=5,
                        opacity=0,
                        color='white',
                    ),
                    hoverinfo='text',
                )],
                layout=dict(
                    mapbox=dict(
                        layers=[
                            dict(
                                sourcetype='geojson',
                                source=cancer_json['features'][i],
                                type='fill',
                                color='red',
                                opacity=.6
                            ) for i in range(len(cancer_json['features']))
                        ],
                        accesstoken=MAPBOX_TOKEN,
                        center=dict(
                            lon=-1.5,
                            lat=52,
                        ),
                        zoom=5,
                    ),
                    hovermode='closest',
                )
            )
        )
    ])

if __name__ == "__main__":
    app.run_server(debug=True)