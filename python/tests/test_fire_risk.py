# standard library
import json
from unittest import TestCase
# third party
import shapely.geometry
# module to test
import fire_risk


class TestHelpers(TestCase):

    def test_parse_event(self):
        fake_event = {
            'httpMethod': 'POST',
            'headers': {'Content-Type': 'application/json'},
            'body': '{\"drink\": \"beer\"}'}
        res = fire_risk.parse_event(fake_event)
        self.assertEqual(res, {'drink': 'beer'})

    def test_get_geometry(self):
        fake_data = {
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}}
        res = fire_risk.get_geometry(fake_data)
        self.assertTrue(isinstance(res, shapely.geometry.Polygon))


class TestRequestParsing(TestCase):

    def test_parse_post(self):
        geometry = {
            'type': 'Polygon',
            'coordinates': [[
                [-121.8, 37.5], [-121.8, 37.51], [-121.81, 37.51],
                [-121.81, 37.5], [-121.8, 37.5]]]}
        fake_event = {
            'httpMethod': 'POST',
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'geometry': geometry})}
        res = fire_risk.parse_event(fake_event)
        self.assertIn('geometry', res)
        self.assertEqual(res['geometry'], geometry)

    def test_parse_get(self):
        geometry = {
            'type': 'Polygon',
            'coordinates': [[
                [-121.8, 37.5], [-121.8, 37.51], [-121.81, 37.51],
                [-121.81, 37.5], [-121.8, 37.5]]]}
        fake_event = {
            'httpMethod': 'GET',
            'queryStringParameters': {
                'geometry': json.dumps(geometry)
            }
        }
        res = fire_risk.parse_event(fake_event)
        print(res)
