import numpy as np
from datetime import datetime, timedelta

ais_sample = ais_filter_ori[ais_filter_ori['mmsi'] == 533130901]
ais_sample = ais_sample[['time','longitude','latitude','sog','cog','heading']]

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

