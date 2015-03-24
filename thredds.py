from owslib.wcs import WebCoverageService
from scipy.io import netcdf
from pyproj import Proj
import io
import datetime


def to_celsius(kelvin):
    return kelvin - 273.15


wcs = WebCoverageService('http://thredds.met.no/thredds/wcs/arome25/arome_metcoop_test2_5km_latest.nc?service=WCS&version=1.0.0&request=GetCapabilities')


def lambert_to_latlon(x, y):
    p1 = Proj('+proj=lcc +lat_0=63 +lon_0=15 +lat_1=63 +lat_2=63 +no_defs +R=6.371e+06')
    lon, lat = p1(x, y, inverse=True)
    return lat, lon


def get_coverage(identifier, bbox):
    cvg = wcs.getCoverage(
        identifier=identifier,
        bbox=bbox,
        format='NetCDF3'
    )
    d = io.BytesIO(cvg.read())
    return netcdf.netcdf_file(d)


def parse_netcdf(coverage, identifier):
    times = coverage.variables['time'].data
    data = coverage.variables[identifier].data
    units = coverage.variables[identifier].units
    z = 0
    for time, time_value in enumerate(times):
        time_data = datetime.datetime.fromtimestamp(time_value)
        print 'time: %s' % time_data
        for x, x_value in enumerate(coverage.variables['x'].data):
            for y, y_value in enumerate(coverage.variables['y'].data):
                lat, lon = lambert_to_latlon(x_value, y_value)
                data = coverage.variables[identifier].data[time][z][y][x]
                print '\tpos: %s, %s' % (lat, lon)
                print '\t\t%s: %s %s' % (identifier, data, units)

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

print "data for bbox [%s, %s, %s, %s]:\n" % bbox
for identifier in layers:
    print identifier
    coverage = get_coverage(identifier, bbox)
    parse_netcdf(coverage, identifier)
