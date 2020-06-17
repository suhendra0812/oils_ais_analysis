import geopandas as gpd
import pandas as pd
from datetime import datetime, timedelta
import os, sys
from shapely.geometry import LineString

basemap_path = r"D:\BARATA\1.basemaps\base_p_ina_geo_fix.shp"
wpp_path = r"D:\BARATA\1.basemaps\WPP_NEW.shp"

# SUHENDRA-PC
#os.chdir(r"E:\Development\BARATA\Riset\02-oil-spill\oils_ais_analysis")
#oil_path = r"E:\Development\BARATA\Riset\02-oil-spill\kepri_201812_oils\kepri_20181212_oils.shp"
#ais_path = r"E:\Development\BARATA\Riset\09-data-ais\2018\indo_20181212_ais.csv"

# WSBARATA01
os.chdir(r"D:\Suhendra\Riset BARATA\oils_ais_analysis")
oil_path = r"D:\Suhendra\Riset BARATA\data oil\kepri_201812_oils\kepri_20181213_oils.shp"
ais_path = r"D:\BARATA\10.ais\2018\indo_20181213_ais.csv"

oil_gdf = gpd.read_file(oil_path).sort_values(by='DATE-TIME')
ais_df = pd.read_csv(ais_path)
ais_gdf = gpd.GeoDataFrame(ais_df, geometry=gpd.points_from_xy(ais_df['longitude'], ais_df['latitude']))

#oil_gdf['DATETIME-UNIFORM'] = [datetime.strptime(i[:-11], '%Y-%m-%dT%H').strftime('%Y-%m-%dT%H:%M:%S') for i in oil_gdf['DATE-TIME']]
#oil_dissolve = oil_gdf.dissolve(by='DATETIME-UNIFORM')

# membuat buffer dari centroid oil
oil_buffer = oil_gdf.copy()
oil_buffer.geometry = oil_buffer.geometry.centroid.buffer(1)

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

def timedelta_max(dt_list):
    td_list = [dt_list.iloc[i]-dt_list.iloc[i-1] for i in range(1, len(dt_list))]
    if not len(td_list) == 0:
        td_max = max(td_list)
    else:
        td_max = timedelta(0)

    return td_max

def rule_based_style(layer, symbol, renderer, label, color, expression=None):
    root_rule = renderer.rootRule()
    rule = root_rule.children()[0].clone()
    rule.setLabel(label)
    if expression != None:
        rule.setFilterExpression(expression)
    else:
        rule.setIsElse(True)
    rule.symbol().setColor(QColor(color))
    root_rule.appendChild(rule)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())

root = QgsProject.instance().layerTreeRoot()

# looping setiap buffer oil
for i, oil in oil_buffer.iterrows():
    oilstrptime = datetime.strptime(oil['DATE-TIME'], '%Y-%m-%d %H:%M:%S')
    oildate = oilstrptime.strftime('%Y-%m-%dT%H:%M:%S')
    startdate = (oilstrptime - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
    stopdate = (oilstrptime + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # clip ais pada setiap buffer oil
    ais_clip = gpd.clip(ais_gdf, oil.geometry)
    
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
    
    ais_filter_ori['time'] = ais_filter_ori['time'].astype('datetime64')
    ais_max_td = ais_filter_ori.groupby('mmsi')['time'].apply(timedelta_max)
    ais_filter_ori['time'] = ais_filter_ori['time'].astype(str)
    
    ais_line_gdf = gpd.GeoDataFrame(ais_line[~ais_line.isna()])
    ais_line_gdf = ais_line_gdf.merge(ais_min_time, on='mmsi')
    ais_line_gdf = ais_line_gdf.merge(ais_max_time, on='mmsi', suffixes=('_start', '_end')).reset_index()
    
    oil_row = oil_gdf[oil_gdf['DATE-TIME'].str.contains(oildate[:-6])]
    oil_buffer_row = gpd.GeoDataFrame([oil])
    
    # memuat data agar dapat ditampilkan di canvas QGIS
    ais_filter_ori_layer = QgsVectorLayer(ais_filter_ori.to_json(), oildate+"_ais", "ogr")
    ais_line_layer = QgsVectorLayer(ais_line_gdf.to_json(), oildate+'_line','ogr')
    
    oil_layer = QgsVectorLayer(oil_row.to_json(), oildate+"_oil", "ogr")
    oil_buffer_layer = QgsVectorLayer(oil_buffer_row.to_json(), oildate+"_buffer", "ogr")
    
    QgsProject.instance().addMapLayer(oil_buffer_layer, False)
    QgsProject.instance().addMapLayer(oil_layer, False)
    QgsProject.instance().addMapLayer(ais_line_layer, False)
    QgsProject.instance().addMapLayer(ais_filter_ori_layer, False)
    
    oil_date = oilstrptime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

    symbol = QgsSymbol.defaultSymbol(ais_filter_ori_layer.geometryType())
    renderer = QgsRuleBasedRenderer(symbol)
        
    #rule_based_style(ais_filter_ori_layer, symbol, renderer,  'before', f"\"time\" < '{oil_date}'", 'cyan')
    #rule_based_style(ais_filter_ori_layer, symbol, renderer, 'after', f"\"time\" > '{oil_date}'", 'yellow')
    
    style_exp1 = f"minute(to_datetime(\"time\") - to_datetime('{oil_date}')) < -60"
    style_exp2 = f"minute(to_datetime(\"time\") - to_datetime('{oil_date}')) < -30 AND minute(to_datetime(\"time\") - to_datetime('{oil_date}')) >= -60"
    style_exp3 = f"minute(to_datetime(\"time\") - to_datetime('{oil_date}')) < 0 AND minute(to_datetime(\"time\") - to_datetime('{oil_date}')) >= -30"
    style_exp4 = f"minute(to_datetime(\"time\") - to_datetime('{oil_date}')) > 0 AND minute(to_datetime(\"time\") - to_datetime('{oil_date}')) <= 30"
    style_exp5 = f"minute(to_datetime(\"time\") - to_datetime('{oil_date}')) > 30 AND minute(to_datetime(\"time\") - to_datetime('{oil_date}')) <= 60"
    style_exp6 = f"minute(to_datetime(\"time\") - to_datetime('{oil_date}')) > 60"
    
    rule_based_style(ais_filter_ori_layer, symbol, renderer,  '> 60 minutes before', 'cyan', style_exp1)
    rule_based_style(ais_filter_ori_layer, symbol, renderer, '30 - 60 minutes before', 'yellow', style_exp2)
    rule_based_style(ais_filter_ori_layer, symbol, renderer,  '0 - 30 minutes before', 'orange', style_exp3)
    rule_based_style(ais_filter_ori_layer, symbol, renderer, '0 - 30 minutes after', 'red', style_exp4)
    rule_based_style(ais_filter_ori_layer, symbol, renderer, '30 - 60 minutes after', 'green', style_exp5)
    rule_based_style(ais_filter_ori_layer, symbol, renderer, '> 60 minutes after', 'blue', style_exp6)
    
    oil_buffer_layer.loadNamedStyle(r"templates\oils_buffer.qml")
    oil_layer.loadNamedStyle(r"templates\oils_fill.qml")
    ais_line_layer.loadNamedStyle(r"templates\ais_line_trajectory.qml")
    
    data_group = root.addGroup(oildate)
    data_group.addLayer(ais_filter_ori_layer)
    data_group.addLayer(ais_line_layer)
    data_group.addLayer(oil_layer)
    data_group.addLayer(oil_buffer_layer)

basemap_layer = QgsVectorLayer(basemap_path, 'Peta Indonesia', 'ogr')
wpp_layer = QgsVectorLayer(wpp_path, 'WPP RI', 'ogr')

basemap_group = root.addGroup('Basemap')
    
QgsProject.instance().addMapLayer(basemap_layer, False)
QgsProject.instance().addMapLayer(wpp_layer, False)

basemap_layer.loadNamedStyle(r"templates\basemap.qml")
wpp_layer.loadNamedStyle(r"templates\wpp.qml")

basemap_group.addLayer(wpp_layer)
basemap_group.addLayer(basemap_layer)
