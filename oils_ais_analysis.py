import geopandas as gpd
import pandas as pd
from datetime import datetime, timedelta
import os
from shapely.geometry import LineString

oil_path = r"E:\Development\BARATA\Riset\02-oil-spill\kepri_201812_oils\kepri_20181220_oils.shp"
ais_path = r"E:\Development\BARATA\Riset\09-data-ais\2018\indo_20181220_ais.csv"

oil_gdf = gpd.read_file(oil_path).sort_values(by='DATE-TIME')
ais_df = pd.read_csv(ais_path)
ais_gdf = gpd.GeoDataFrame(ais_df, geometry=gpd.points_from_xy(ais_df['longitude'], ais_df['latitude']))

#oil_gdf['DATETIME-UNIFORM'] = [datetime.strptime(i[:-11], '%Y-%m-%dT%H').strftime('%Y-%m-%dT%H:%M:%S') for i in oil_gdf['DATE-TIME']]
#oil_dissolve = oil_gdf.dissolve(by='DATETIME-UNIFORM')

# membuat buffer dari centroid oil
oil_buffer = oil_gdf.copy()
oil_buffer.geometry = oil_buffer.geometry.centroid.buffer(0.5)

oil_buffer['DATE-TIME'] = [datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%fZ') for i in oil_buffer['DATE-TIME']]

# menghomogenkan waktu untuk nilai waktu yang masih dalam rentang 1 jam
for i in range(len(oil_buffer['DATE-TIME']) - 1):
    if oil_buffer['DATE-TIME'][i] is None:
        continue
    for j in range(i+1, len(oil_buffer['DATE-TIME'])):
        if oil_buffer['DATE-TIME'][j] is None:
            continue
        if oil_buffer['DATE-TIME'][j] - oil_buffer['DATE-TIME'][i] <= timedelta(hours=1):
            oil_buffer['DATE-TIME'][j] = oil_buffer['DATE-TIME'][i]

oil_buffer['DATE-TIME'] = oil_buffer['DATE-TIME'].astype(str)
oil_buffer = oil_buffer.dissolve(by='DATE-TIME', aggfunc='mean').reset_index()

ais_name = os.path.basename(os.path.splitext(ais_path)[0])

ais_filter_a_list = []
ais_filter_b_list = []
ais_filter_ori_list = []
ais_line_gdf_list = []

# looping setiap buffer oil
for i, row in oil_buffer.iterrows():
    oilstrptime = datetime.strptime(row['DATE-TIME'], '%Y-%m-%d %H:%M:%S')
    oildate = oilstrptime.strftime('%Y-%m-%dT%H:%M:%S')
    startdate = (oilstrptime - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
    stopdate = (oilstrptime + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # clip ais pada setiap buffer oil
    ais_clip = gpd.clip(ais_gdf, row.geometry)
    
    # filter ais pada rentang waktu 1 jam sebelum dan sesudah waktu oil
    ais_filter = ais_clip.loc[(ais_clip['time'] >= startdate) & (ais_clip['time'] <= stopdate)]
    ais_filter_a = ais_clip.loc[(ais_clip['time'] >= oildate) & (ais_clip['time'] <= stopdate)]
    ais_filter_b = ais_clip.loc[(ais_clip['time'] >= startdate) & (ais_clip['time'] <= oildate)]
    ais_filter_ori = ais_gdf.loc[ais_gdf['mmsi'].isin(ais_filter['mmsi'])]
    
    # membuat data ais dalam bentuk line dengan sortir waktu
    ais_filter_ori = ais_filter_ori.sort_values(by='time')
    ais_line = ais_filter_ori.groupby('mmsi')['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else None)
    ais_min_time = ais_filter_ori.groupby('mmsi')['time'].agg('min')
    ais_max_time = ais_filter_ori.groupby('mmsi')['time'].agg('max')

    ais_line_gdf = gpd.GeoDataFrame(ais_line, geometry=ais_line[ais_line != None])
    ais_line_gdf = ais_line_gdf.merge(ais_min_time, on='mmsi')
    ais_line_gdf = ais_line_gdf.merge(ais_max_time, on='mmsi', suffixes=('_start', '_end')).reset_index()
    
    # menggabungkan data yang telah diperoleh dari setiap baris
    ais_filter_a_list.append(ais_filter_a)
    ais_filter_b_list.append(ais_filter_b)
    ais_filter_ori_list.append(ais_filter_ori)
    ais_line_gdf_list.append(ais_line_gdf)
    
ais_filter_a = gpd.GeoDataFrame(pd.concat(ais_filter_a_list, ignore_index=True))
ais_filter_b = gpd.GeoDataFrame(pd.concat(ais_filter_b_list, ignore_index=True))
ais_filter_ori = gpd.GeoDataFrame(pd.concat(ais_filter_ori_list, ignore_index=True))
ais_line_gdf = gpd.GeoDataFrame(pd.concat(ais_line_gdf_list, ignore_index=True))

# memuat data agar dapat ditampilkan di canvas QGIS
ais_filter_a_layer = QgsVectorLayer(ais_filter_a.to_json(), ais_name+"_clip_a", "ogr")
ais_filter_b_layer = QgsVectorLayer(ais_filter_b.to_json(), ais_name+"_clip_b", "ogr")
ais_filter_ori_layer = QgsVectorLayer(ais_filter_ori.to_json(), ais_name, "ogr")
ais_line_layer = QgsVectorLayer(ais_line_gdf.to_json(), ais_name+'_line','ogr')

oil_name = os.path.basename(os.path.splitext(oil_path)[0])

oil_layer = QgsVectorLayer(oil_gdf.to_json(), oil_name, "ogr")
oil_buffer_layer = QgsVectorLayer(oil_buffer.to_json(), oil_name+"_buffer", "ogr")

oil_buffer_layer.loadNamedStyle(r"E:\Development\BARATA\Riset\02-oil-spill\oils_ais_analysis\templates\oils_buffer.qml")
oil_layer.loadNamedStyle(r"E:\Development\BARATA\Riset\02-oil-spill\oils_ais_analysis\templates\oils_fill.qml")
ais_line_layer.loadNamedStyle(r"E:\Development\BARATA\Riset\02-oil-spill\oils_ais_analysis\templates\ais_line_trajectory.qml")
ais_filter_ori_layer.loadNamedStyle(r"E:\Development\BARATA\Riset\02-oil-spill\oils_ais_analysis\templates\ais_all.qml")
ais_filter_a_layer.loadNamedStyle(r"E:\Development\BARATA\Riset\02-oil-spill\oils_ais_analysis\templates\ais_clip_a.qml")
ais_filter_b_layer.loadNamedStyle(r"E:\Development\BARATA\Riset\02-oil-spill\oils_ais_analysis\templates\ais_clip_b.qml")

QgsProject.instance().addMapLayer(oil_buffer_layer)
QgsProject.instance().addMapLayer(oil_layer)
QgsProject.instance().addMapLayer(ais_line_layer)
QgsProject.instance().addMapLayer(ais_filter_ori_layer)
QgsProject.instance().addMapLayer(ais_filter_b_layer)
QgsProject.instance().addMapLayer(ais_filter_a_layer)