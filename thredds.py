from owslib.wcs import WebCoverageService
from scipy.io import netcdf
from pyproj import Proj, transform
import io
import datetime


def to_celsius(kelvin):
    return kelvin - 273.15


wcs = WebCoverageService('http://thredds.met.no/thredds/wcs/arome25/arome_metcoop_test2_5km_latest.nc?service=WCS&version=1.0.0&request=GetCapabilities')


def lambert_to_latlon(x, y):
    p1 = Proj('')  # ?????
    p2 = Proj(init='EPSG:4326')
    x1, y1 = p1(x, y)
    x2, y2 = transform(p1, p2, x1, y1)
    print x2, y2


def get_coverage(identifier, bbox):
    cvg = wcs.getCoverage(
        identifier=identifier,
        bbox=bbox,
        format='NetCDF3'
    )
    d = io.BytesIO(cvg.read())
    return netcdf.netcdf_file(d)

layers = [
    'air_temperature_ml',
    'wind_speed_of_gust',
    'turbulent_kinetic_energy_pl',
    'x_wind_10m',
    'y_wind_10m'
]

x = 10.46303
y = 59.93956

offset = 0.01

bbox = (x - offset, y - offset, x + offset, y + offset)

print bbox

items = wcs.items()
# for item in items:
#    print item[0], item[1].title
#    print item[1].boundingBoxWGS84
#    print item[1].timelimits
#    print item[1].grid


item_id = 'x_wind_10m'

# item = [item[1] for item in items if item[0] == item_id][0]


x_wind = get_coverage('x_wind_10m', bbox)


y_wind = get_coverage('y_wind_10m', bbox)

x_data = x_wind.variables['x_wind_10m'].data
y_data = y_wind.variables['y_wind_10m'].data

print x_wind.variables['projection_lambert'].data

# print x_wind.variables['x'].data
# print x_wind.variables['y'].data
# print x_wind.variables['x_wind_10m'].shape


times = x_wind.variables['time'].data

data = x_wind.variables['x_wind_10m'].data

# response crs:
# [EPSG:9802 [Lambert_Conformal_Conic_2SP]]

z = 0
for time, time_value in enumerate(times):
    print 'time=%s' % time_value
    for x, x_value in enumerate(x_wind.variables['x'].data):
        print '\tx = %s' % x_value
        for y, y_value in enumerate(x_wind.variables['y'].data):
            # lambert_to_latlon(x_value, y_value)
            print '\t\ty=%s' % y_value
            # t, z, y, x
            x_wind_10m = x_wind.variables['x_wind_10m'].data[time][z][y][x]
            print '\t\t\tx_wind_10m=%s' % x_wind_10m
