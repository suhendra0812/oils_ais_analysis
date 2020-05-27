import geopandas as gpd
import pandas as pd
from datetime import datetime, timedelta
import os
from shapely.geometry import LineString

oil_path = r"E:\Development\BARATA\Riset\02-oil-spill\kepri_201812_oils\kepri_20181212_oils.shp"
ais_path = r"E:\Development\BARATA\Riset\09-data-ais\2018\indo_20181212_ais.csv"

oil_gdf = gpd.read_file(oil_path)
ais_df = pd.read_csv(ais_path)
ais_gdf = gpd.GeoDataFrame(ais_df, geometry=gpd.points_from_xy(ais_df['longitude'], ais_df['latitude']))

oil_gdf['DATETIME-UNIFORM'] = [datetime.strptime(i[:-11], '%Y-%m-%dT%H').strftime('%Y-%m-%dT%H:%M:%S') for i in oil_gdf['DATE-TIME']]
oil_dissolve = oil_gdf.dissolve(by='DATETIME-UNIFORM')

oil_buffer = oil_dissolve.copy()
oil_buffer.geometry = oil_buffer.geometry.centroid.buffer(0.5)

ais_name = os.path.basename(os.path.splitext(ais_path)[0])
ais_clip = gpd.clip(ais_gdf, oil_buffer)

ais_filter_list = []
ais_filter_ori_list = []
ais_line_gdf_list = []

for oil_dtime in oil_dissolve['DATE-TIME'].values:
    oildate = datetime.strptime(oil_dtime, '%Y-%m-%dT%H:%M:%S.%fZ')
    startdate = (oildate - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
    stopdate = (oildate + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')

    ais_filter = ais_clip.loc[(ais_clip['time'] >= startdate) & (ais_clip['time'] <= stopdate)]
    ais_filter_ori = ais_gdf.loc[ais_gdf['mmsi'].isin(ais_filter['mmsi'])]

    ais_line = ais_filter_ori.groupby('mmsi')['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else None)
    ais_min_time = ais_filter_ori.groupby('mmsi')['time'].agg('min')
    ais_max_time = ais_filter_ori.groupby('mmsi')['time'].agg('max')

    ais_line_gdf = gpd.GeoDataFrame(ais_line, geometry=ais_line[ais_line != None])
    ais_line_gdf = ais_line_gdf.merge(ais_min_time, on='mmsi')
    ais_line_gdf = ais_line_gdf.merge(ais_max_time, on='mmsi', suffixes=('_start', '_end'))
    
    ais_filter_list.append(ais_filter)
    ais_filter_ori_list.append(ais_filter_ori)
    ais_line_gdf_list.append(ais_line_gdf)
    
ais_filter = gpd.GeoDataFrame(pd.concat(ais_filter_list, ignore_index=True))
ais_filter_ori = gpd.GeoDataFrame(pd.concat(ais_filter_ori_list, ignore_index=True))
ais_line_gdf = gpd.GeoDataFrame(pd.concat(ais_line_gdf_list, ignore_index=True))

ais_filter_layer = QgsVectorLayer(ais_filter.to_json(), ais_name+"_clip", "ogr")
ais_filter_ori_layer = QgsVectorLayer(ais_filter_ori.to_json(), ais_name, "ogr")
ais_line_layer = QgsVectorLayer(ais_line_gdf.to_json(), ais_name+'_line','ogr')

oil_name = os.path.basename(os.path.splitext(oil_path)[0])

oil_layer = QgsVectorLayer(oil_gdf.to_json(), oil_name, "ogr")
oil_buffer_layer = QgsVectorLayer(oil_buffer.to_json(), oil_name+"_buffer", "ogr")
QgsProject.instance().addMapLayer(oil_buffer_layer)
QgsProject.instance().addMapLayer(oil_layer)
QgsProject.instance().addMapLayer(ais_line_layer)
QgsProject.instance().addMapLayer(ais_filter_ori_layer)
QgsProject.instance().addMapLayer(ais_filter_layer)