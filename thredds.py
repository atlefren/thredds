from owslib.wcs import WebCoverageService
from scipy.io import netcdf
import io
import datetime


def to_celsius(kelvin):
    return kelvin - 273.15


wcs = WebCoverageService('http://thredds.met.no/thredds/wcs/arome25/arome_metcoop_test2_5km_latest.nc?service=WCS&version=1.0.0&request=GetCapabilities')


def get_coverage(identifier, bbox):
    cvg = wcs.getCoverage(
        identifier=identifier,
        bbox=bbox,
        format='NetCDF3'
    )
    d = io.BytesIO(cvg.read())
    return netcdf.netcdf_file(d)


def print_stuff(f, identifier):
    print f.dimensions
    print f.variables
    times = f.variables['time'].data
    #print f.variables['time'].units
    #print f.variables['time'].shape
    #print f.variables['lon'].data
    #print f.variables['lat'].data
    data = f.variables[identifier].data
    #print "?"
    #print f.variables['hybrid0'].shape
    #print f.variables['hybrid0'].units
    #print f.variables['hybrid0'].data
    #print f.variables[identifier].shape
    #print data[0][0][0]
    
    for (time, ident) in zip(times, data):
        date = datetime.datetime.fromtimestamp(time)
        print date
        for d in ident:
            print to_celsius(d[0][0])
        print "---"
    

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

items = wcs.items()
for item in items:
    print item[0], item[1].title
   # print item[1].boundingBoxWGS84
   # print item[1].timelimits
   # print item[1].grid


item_id = 'x_wind_10m'

item = [item[1] for item in items if item[0] == item_id][0]

#print item.boundingBoxWGS84

x_wind = get_coverage('x_wind_10m', bbox)

#print x_wind.variables

y_wind = get_coverage('y_wind_10m', bbox)

x_data = x_wind.variables['x_wind_10m'].data
y_data = y_wind.variables['y_wind_10m'].data

print x_wind.variables
print x_wind.variables['x_wind_10m'].shape
print x_wind.variables['height2'].data

#for wx, wy in zip(x_data, y_data):
    #print wx[0][0][0], wx[0][1][0]
    #print wy


#print_stuff(f, item_id)