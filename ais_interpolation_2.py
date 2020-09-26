import math
import pandas as pd
import geopandas as gpd
from datetime import datetime
import matplotlib.pyplot as plt
from shapely.geometry import Point
from pyproj import Proj, transform

def calculate_coordinates(departure_point, bearing, distance):
    R = 63781000
    d = distance

    lat1 = math.radians(departure_point[1]) #Current lat point converted to math.radians
    lon1 = math.radians(departure_point[0]) #Current long point converted to math.radians

    bearing = math.radians(bearing)

    lat2 = math.asin(math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(bearing))

    lon2 = lon1 + math.atan2(math.sin(bearing)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return (round(lon2, 4), round(lat2, 4))

def total_seconds(td):
    return td.total_seconds()

def total_minutes(td):
    return td.total_seconds()/60

def total_hours(td):
    return td.total_seconds()/3600

def total_days(td):
    return td.total_seconds()/(3600*24)

def curve_interp(ais_df, ti):
    ais1 = ais_df[ais_df['time'] <= ti].iloc[-1]
    ais2 = ais_df[ais_df['time'] > ti].iloc[0]

    x1 = ais1['geometry'].x
    y1 = ais1['geometry'].y
    v1 = ais1['sog']*0.514444
    h1 = math.radians(ais1['cog'])
    t1 = ais1['time']

    x2 = ais2['geometry'].x
    y2 = ais2['geometry'].y
    v2 = ais2['sog']*0.514444
    h2 = math.radians(ais2['cog'])
    t2 = ais2['time']

#    d1 = v1*((ti-t1).seconds)
#    d2 = v2*((t2-ti).seconds)
#    xi1, yi1 = calculate_coordinates((x1,y1), h1, d1)
#    xi2, yi2 = calculate_coordinates((x2,y2), h2, d2)

    xi1 = x1 + (v1*math.sin(h1)*total_seconds(ti-t1))
    yi1 = y1 + (v1*math.cos(h1)*total_seconds(ti-t1))

    xi2 = x2 + (v2*math.sin(h2)*total_seconds(ti-t2))
    yi2 = y2 + (v2*math.cos(h2)*total_seconds(ti-t2))

    W1 = 1-(total_seconds(ti-t1)/total_seconds(t2-t1))
    W2 = 1-(total_seconds(t2-ti)/total_seconds(t2-t1))

    xi = W1*xi1 + W2*xi2
    yi = W1*yi1 + W2*yi2

    return xi, yi

def interpolate_ais(ais_df, mmsi):
    ais_df = ais_df.loc[ais_df['mmsi'] == mmsi]
    if len(ais_df) > 1:
        ais_df['time'] = ais_df['time'].astype('datetime64')

        lon_list = []
        lat_list = []
        time_list = []

        time1 = ais_df['time'].iloc[0]
        time2 = ais_df['time'].iloc[-1]

        date_list = pd.date_range(start=time1, end=time2, freq='30min').to_pydatetime().tolist()

        basemap_gdf = gpd.read_file(basemap_path)
        inProj = Proj(init=proj_crs)
        outProj = Proj(init=geo_crs)
        for ti in date_list:
            xi_proj, yi_proj = curve_interp(ais_df, ti)
            xi_geo,yi_geo = transform(inProj,outProj,xi_proj,yi_proj)
            ais_land = basemap_gdf[basemap_gdf.intersects(Point(xi_geo, yi_geo))]
            if len(ais_land) == 0:
                lon_list.append(xi_geo)
                lat_list.append(yi_geo)
                time_list.append(str(ti))

        ais_interp = gpd.GeoDataFrame({'time':time_list, 'mmsi':mmsi}, geometry=gpd.points_from_xy(lon_list, lat_list), crs=geo_crs)
    else:
        ais_interp = ais_df.loc[:,['time','mmsi']]
    
    return ais_interp

#ais_path = r"D:\Suhendra\Riset BARATA\oils_ais_analysis\kepri_20181220_102057_ais_sample.csv"
#ais_df = pd.read_csv(ais_path)
ais_df = ais_filter_ori.copy()

geo_crs = 'epsg:4326'
proj_crs = 'epsg:32648'
ais_df.crs = {'init':geo_crs}
ais_df.to_crs(proj_crs, inplace=True)

interp_df_list = []
mmsi_list = [525114003]
#mmsi_list = list(set(ais_df['mmsi']))
for mmsi in mmsi_list:
    interp_df = interpolate_ais(ais_df, mmsi)
    interp_df_list.append(interp_df)

ais_interp = gpd.GeoDataFrame(pd.concat(interp_df_list, ignore_index=True))
ais2_layer = QgsVectorLayer(ais_interp.to_json(), f'interpolation_2', 'ogr')
QgsProject.instance().addMapLayer(ais2_layer)
