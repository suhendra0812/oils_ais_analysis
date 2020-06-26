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

mmsi = 477858800
ais_sample = ais_filter_ori[ais_filter_ori['mmsi'] == mmsi]
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
        L_lon = interp1d(ais_ti['time'], ais_ti['longitude'])
        L_lat = interp1d(ais_ti['time'], ais_ti['latitude'])
        L_sog = interp1d(ais_ti['time'], ais_ti['sog'])
        L_cog = interp1d(ais_ti['time'], ais_ti['cog'])
        L_hdg = interp1d(ais_ti['time'], ais_ti['heading'])
        lon_intp.append(float(L_lon(ti)))
        lat_intp.append(float(L_lat(ti)))
        sog_intp.append(float(L_sog(ti)))
        cog_intp.append(float(L_cog(ti)))
        hdg_intp.append(float(L_hdg(ti)))
        course_type.append('linear')
    else:
        P_lon = PchipInterpolator(ais_ti['time'], ais_ti['longitude'])
        P_lat = PchipInterpolator(ais_ti['time'], ais_ti['latitude'])
        P_sog = PchipInterpolator(ais_ti['time'], ais_ti['sog'])
        P_cog = PchipInterpolator(ais_ti['time'], ais_ti['cog'])
        P_hdg = PchipInterpolator(ais_ti['time'], ais_ti['heading'])
        lon_intp.append(float(P_lon(ti)))
        lat_intp.append(float(P_lat(ti)))
        sog_intp.append(float(P_sog(ti)))
        cog_intp.append(float(P_cog(ti)))
        hdg_intp.append(float(P_hdg(ti)))
        course_type.append('curve')

t_df = pd.to_datetime(t_intp, unit='s').astype(str)
intp_gdf = gpd.GeoDataFrame({'time':t_df, 'longitude':lon_intp, 'latitude':lat_intp, 'sog':sog_intp, 'cog':cog_intp, 'heading':hdg_intp, 'course_type':course_type, 'k_mean':k_mean, 'k_std':k_std}, geometry=gpd.points_from_xy(lon_intp, lat_intp))
intp_layer = QgsVectorLayer(intp_gdf.to_json(), f'{mmsi}_interpolation_1', 'ogr')
QgsProject.instance().addMapLayer(intp_layer)

