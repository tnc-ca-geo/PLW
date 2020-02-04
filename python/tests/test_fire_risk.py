from unittest import TestCase
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
        print(res)
