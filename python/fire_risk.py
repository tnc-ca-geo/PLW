"""
Proof of concept of S3 access to GDAL
"""
# standard library
from functools import partial
import json
# third party
import fiona
import numpy as np
import pyproj
import rasterio
import rasterio.mask
from rasterio.windows import Window, get_data_window
from shapely.geometry import shape, mapping
from shapely.ops import transform


TEST_FEATURE = {
    "type": "Polygon",
    "coordinates": [
        [[-122.09, 37.56], [-122.04, 37.34], [-121.74, 37.28],
         [-121.64, 37.34], [-121.55, 37.40], [-121.51, 37.48],
         [-121.55, 37.60], [-121.76, 37.70], [-121.98, 37.74],
         [-122.09, 37.56]]]
    }
# https://gis.stackexchange.com/questions/127427/
# transforming-shapely-polygon-and-multipolygon-objects
PROJECT = partial(
    pyproj.transform, pyproj.Proj(init='epsg:4326'),
    pyproj.Proj(init='epsg:3310'))
TEST_GEOMETRY = shape(TEST_FEATURE)


def transform_geometry(geometry, in_crs, out_crs):
    reproject = partial(
        pyproj.transform, pyproj.Proj(init=in_crs), pyproj.Proj(init=out_crs))
    return transform(reproject, geometry)


def write_shape(filepath, geometry, crs=None):
    """
    Write shape for evaluation in GIS.
    """
    schema = {'geometry': 'Polygon', 'properties': {}}
    meta = {
        'schema': schema, 'crs': crs or 'EPSG:4326', 'mode': 'w',
        'driver': 'ESRI Shapefile'}
    with fiona.open('test.shp', **meta) as shp:
        shp.write({
            'geometry': mapping(geometry),
            'properties': {}})


def write_raster(filepath, data, meta_template, transform):
    """
    Write raster for evaluation in GIS.
    """
    meta = meta_template.copy()
    meta.update({
        'count': data.shape[0], 'width': data.shape[2],
        'height': data.shape[1], 'transform': transform})
    with rasterio.open(filepath, 'w', **meta) as dst:
        dst.write(data)


def parse_event(event):
    data = {}
    if event.get('httpMethod') == 'POST':
        if 'application/json' in event['headers'].get('Content-Type'):
            data = json.loads(event.get('body', {}))
    return data


def get_geometry(data):
    """
    Extract and validate a polygon from the data.
    """
    raw_geometry = data['geometry']


def get_fire_risk(geom, geom_crs='epsg:4326'):
    """
    Return the fire risk for an area
    """
    with rasterio.open('s3://plwassets/firerisk.tif') as src:
        geometry = transform_geometry(geom, geom_crs, 'epsg:3310')
        out_data, out_transform = rasterio.mask.mask(
            src, [geometry], crop=True, nodata=9, filled=True)
    # Leave that here for evaluation purposes
    # write_raster('raster.tif', out_data, src.meta, out_transform)
    flat = out_data.flatten()
    bins = np.bincount(flat)
    count = np.count_nonzero(flat)
    count = np.sum(bins[0:4])
    return {
        'fire risk': {
            'high': bins[1]/count * 100, 'very high': bins[2]/count * 100},
        'unit': 'percent of area'}


def lambda_handler(event, context):
    fire_risk = get_fire_risk(TEST_GEOMETRY)
    fire_risk.update({'event': event})
    data = parse_event(event)
    fire_risk.update({'data': data})
    return {
        'statusCode': 200,
        'body': json.dumps(fire_risk)}


def main():
    """
    The main function.
    """
    fake_event = {
        'httpMethod': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'body': '{\"drink\": \"beer\"}'
    }
    res = lambda_handler(fake_event, None)
    print(res)


if __name__ == '__main__':
    main()
