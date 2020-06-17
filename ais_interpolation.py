import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.interpolate import interp1d, PchipInterpolator

def curvature(x, y):
    dx_dt = np.gradient(x)
    dy_dt = np.gradient(y)

    d2x_dt2 = np.gradient(dx_dt)
    d2y_dt2 = np.gradient(dy_dt)

    k = np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt * dx_dt + dy_dt * dy_dt)**1.5
    
    return k

ais_sample = ais_filter_ori[ais_filter_ori['mmsi'] == 431220000]
ais_sample = ais_sample[['time','longitude','latitude','sog','cog','heading']]

t = (pd.to_datetime(ais_sample['time']) - pd.to_datetime('1970-01-01')).dt.total_seconds()
t_intp = np.arange(t.iloc[0], t.iloc[len(t)-1], 10*60)

lon_intp = []
lat_intp = []
sog_intp = []
cog_intp = []
hdg_intp = []
course_type = []
k_mean = []
k_std = []

ais_test = ais_sample.copy()
ais_test['time'] = t

for ti in t_intp:
    ais1 = ais_test[ais_test['time'] <= ti].iloc[-2:]
    ais2 = ais_test[ais_test['time'] > ti].iloc[:2]
    
    ais_ti = pd.concat([ais1, ais2], ignore_index=True)
    
    x = ais_ti['longitude']
    y = ais_ti['latitude']
    k = curvature(x, y)
    k_mean.append(k.mean())
    std = k.std()
    k_std.append(std)
    
    if k.mean() < 0.5 and k.mean() > -0.5:
        print('Course is linear')
        L_lon = interp1d(ais_ti['time'], ais_ti['longitude'])
        L_lat = interp1d(ais_ti['time'], ais_ti['latitude'])
        lon_intp.append(L_lon(ti))
        lat_intp.append(L_lat(ti))
        course_type.append('linear')
    else:
        print('Course is curve')
        L_lon = PchipInterpolator(ais_ti['time'], ais_ti['longitude'])
        L_lat = PchipInterpolator(ais_ti['time'], ais_ti['latitude'])
        lon_intp.append(P_lon(ti))
        lat_intp.append(P_lat(ti))
        course_type.append('curve')
"""
for ti in t_intp:
    ais1 = ais_test[ais_test['time'] < ti]
    ais2 = ais_test[ais_test['time'] > ti]
    
    if len(ais1) >= 2:
        x1 = ais1.iloc[:2]['longitude']
        y1 = ais1.iloc[:2]['latitude']
        k1 = curvature(x1, y1)
    else:
        k1 = np.array(0)
    std1 = k1.std()
    
    if len(ais2) >= 2:
        x2 = ais2.iloc[:2]['longitude']
        y2 = ais2.iloc[:2]['latitude']
        k2 = curvature(x2, y2)
    else:
        k2 = np.array(0)
    std2 = k2.std()
    
    if (k1.mean()-2*std1) <= k2.mean() <= (k1.mean()+2*std1):
        print('Course is linear')
        lon_intp.append(L_lon(ti))
        lat_intp.append(L_lat(ti))
    else:
        print('Course is curve')
        lon_intp.append(P_lon(ti))
        lat_intp.append(P_lat(ti))
"""
t_df = pd.to_datetime(t_intp, unit='s').astype(str)
intp_gdf = gpd.GeoDataFrame({'time':t_df, 'course_type':course_type, 'k_mean':k_mean, 'k_std':k_std}, geometry=gpd.points_from_xy(lon_intp, lat_intp))
intp_layer = QgsVectorLayer(intp_gdf.to_json(), 'interpolasi', 'ogr')
QgsProject.instance().addMapLayer(intp_layer)

#intp_time = str(datetime.strptime(ais_sample['time'].iloc[1], '%Y-%m-%d %H:%M:%S') + timedelta(hours=1))

