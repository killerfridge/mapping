import geopandas as gpd
import os


ROOT_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(ROOT_DIR, 'data')


def df_from_folder(folder):

    path = os.path.join(DATA_DIR, folder)
    path = os.path.join(path, f'{folder}.shp')
    tmp = gpd.read_file(path)
    return tmp.to_crs({'init': 'epsg:4326'})


df = df_from_folder('Sustainability_and_Transformation_Partnerships_April_2019_EN_BFC')

print(df.head())

df.to_file('stp.geojson', driver='GeoJSON')
