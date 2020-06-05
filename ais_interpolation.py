import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.interpolate import interp1d, PchipInterpolator

ais_sample = ais_filter_ori[ais_filter_ori['mmsi'] == 533130901]
ais_sample = ais_sample[['time','longitude','latitude','sog','cog','heading']]

t = (pd.to_datetime(ais_sample['time']) - pd.to_datetime('1970-01-01')).dt.total_seconds()
lon = ais_sample['longitude']
lat = ais_sample['latitude']

t_intp = np.arange(t.iloc[0], t.iloc[len(t)-1], 10*60)

L_lon = interp1d(t, lon)
L_lat = interp1d(t, lat)

P_lon = PchipInterpolator(t, lon)
P_lat = PchipInterpolator(t, lat)

lon_intp = []
lat_intp = []
for ti in t_intp:
    lon_intp.append(P_lon(ti))
    lat_intp.append(P_lat(ti))

intp_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(lon_intp, lat_intp))
intp_layer = QgsVectorLayer(intp_gdf.to_json(), 'interpolasi', 'ogr')
QgsProject.instance().addMapLayer(intp_layer)

x1 = ais_sample.iloc[:3]['longitude']
y1 = ais_sample.iloc[:3]['latitude']

x2 = ais_sample.iloc[3:]['longitude']
y2 = ais_sample.iloc[3:]['latitude']

def curvature(x, y):
    dx_dt = np.gradient(x)
    dy_dt = np.gradient(y)

    d2x_dt2 = np.gradient(dx_dt)
    d2y_dt2 = np.gradient(dy_dt)

    k = np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt * dx_dt + dy_dt * dy_dt)**1.5
    
    return k

k1 = curvature(x1, y1)
k2 = curvature(x2, y2)

std1 = k1.std()
std2 = k2.std()
    
if (k1.mean()-std1) <= k2.mean() <= (k1.mean()+std1):
    print('Course is linear')
else:
    print('Course is curve')

#intp_time = str(datetime.strptime(ais_sample['time'].iloc[1], '%Y-%m-%d %H:%M:%S') + timedelta(hours=1))

