from chartfood.ga import GaDataTable

import json
import unittest


class GaTest(unittest.TestCase):
    maxDiff = None

    def testGaToDataTable(self):
        ga = {
            "columnHeaders": [
                {
                    "name": "ga:date",
                    "columnType": "DIMENSION",
                    "dataType": "STRING"
                },
                {
                    "name": "ga:visitors",
                    "columnType": "METRIC",
                    "dataType": "INTEGER"
                }
            ],
            "rows": [
                ["20130704", "48"],
                ["20130705", "47"],
                ["20130706", "40"]
            ]
        }
        dt_expected = {
            'cols': [
                {'id': 'ga:date', 'label': 'Date', 'type': 'date'},
                {'id': 'ga:visitors', 'label': 'Visitors', 'type': 'number'}
            ],
            'rows': [
                {'c': [{'v': 'Date(2013,6,4)'}, {'v': 48}]},
                {'c': [{'v': 'Date(2013,6,5)'}, {'v': 47}]},
                {'c': [{'v': 'Date(2013,6,6)'}, {'v': 40}]}
            ]
        }

        dt = json.loads(GaDataTable(ga).ToJSon().decode('utf-8'))
        self.assertEqual(dt, dt_expected)
