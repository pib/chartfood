from datetime import date
from .dummy_cache import DummyCache
from pyramid_charts.gviz_api import DataTable
from pyramid.renderers import render

import json
import pyramid.testing
import unittest


class GoogleChartTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.config = pyramid.testing.setUp()
        self.day_score = DataTable([('day', 'date'), ('score', 'number')],
                                   [[date(2013, 12, 11), 42],
                                    [date(2013, 12, 12), 45],
                                    [date(2013, 12, 13), 32],
                                    [date(2013, 12, 14), 15]])
        day_score_dict = {
            "cols": [
                {"id": "day", "label": "day", "type": "date"},
                {"id": "score", "label": "score", "type": "number"}
            ],
            "rows": [
                {"c": [{"v": "Date(2013,11,11)"}, {"v": 42}]},
                {"c": [{"v": "Date(2013,11,12)"}, {"v": 45}]},
                {"c": [{"v": "Date(2013,11,13)"}, {"v": 32}]},
                {"c": [{"v": "Date(2013,11,14)"}, {"v": 15}]}
            ]
        }
        self.day_score_json = json.dumps(day_score_dict, separators=(',', ':'),
                                         sort_keys=True)

        self.inline_prefix = '\n'.join((
            '<script>',
            "  google.load('visualization', '1');",
            '  google.setOnLoadCallback(function() {',
            '    google.visualization.drawChart({'))
        self.inline_postfix = '\n'.join((
            '    });',
            '  });',
            '</script>',
            ''))

    def tearDown(self):
        pyramid.testing.tearDown()

    def testRenderInlineGoogleChart(self):
        self.config.add_renderer(name='chart',
                                 factory='pyramid_charts.InlineChartRenderer')

        rendered = render('chart', self.day_score)
        expected = '\n'.join((
            self.inline_prefix,
            "      containerId: 'chart',",
            "      chartType: 'LineChart',",
            '      dataTable: {}'.format(self.day_score_json),
            self.inline_postfix))
        self.assertEqual(rendered, expected)

    def testRenderDefaultChartResponse(self):
        req = pyramid.testing.DummyRequest({'tqx': 'reqId:42'})
        self.config.add_renderer(
            name='chart_response',
            factory='pyramid_charts.ChartResponseRenderer')

        rendered = render('chart_response', self.day_score, request=req)
        expected = ('google.visualization.Query.setResponse({{"reqId":"42",'
                    '"status":"ok","table":{},"version":"0.6"}});'
                    ).format(self.day_score_json)
        self.assertEqual(rendered, expected)

    def testRenderJsonChartResponse(self):
        req = pyramid.testing.DummyRequest({
            'tqx': 'reqId:42;version:0.6;out:json'
        })
        self.config.add_renderer(
            name='chart_response',
            factory='pyramid_charts.ChartResponseRenderer')

        rendered = render('chart_response', self.day_score, request=req)
        expected = ('google.visualization.Query.setResponse({{"reqId":"42",'
                    '"status":"ok","table":{},"version":"0.6"}});'
                    ).format(self.day_score_json)
        self.assertEqual(rendered, expected)

    def testRenderCsvChartResponse(self):
        req = pyramid.testing.DummyRequest({
            'tqx': 'reqId:42;version:0.6;out:csv'
        })
        self.config.add_renderer(
            name='chart_response',
            factory='pyramid_charts.ChartResponseRenderer')

        rendered = render('chart_response', self.day_score, request=req)
        expected = '\r\n'.join(('day,score',
                                '2013-12-11,42',
                                '2013-12-12,45',
                                '2013-12-13,32',
                                '2013-12-14,15',
                                ''))
        self.assertEqual(rendered, expected)

    def testRenderInlineDatasourceResponse(self):
        self.config.add_renderer(
            name='chart',
            factory='pyramid_charts.InlineChartRenderer')

        rendered = render('chart', {'datasource_url': 'http://test.com/data'})
        expected = '\n'.join((
            self.inline_prefix,
            "      containerId: 'chart',",
            "      chartType: 'LineChart',",
            "      dataSourceUrl: 'http://test.com/data'",
            self.inline_postfix))
        self.assertEqual(rendered, expected)

    def testRenderInlineNonDefault(self):
        self.config.add_renderer(name='chart',
                                 factory='pyramid_charts.InlineChartRenderer')

        rendered = render('chart', {'data_table': self.day_score,
                                    'container_id': 'foo'})
        expected = '\n'.join((
            self.inline_prefix,
            "      containerId: 'foo',",
            "      chartType: 'LineChart',",
            '      dataTable: {}'.format(self.day_score_json),
            self.inline_postfix))
        self.assertEqual(rendered, expected)

    def testRenderInlineCached(self):
        self.config.add_renderer(name='chart',
                                 factory='pyramid_charts.InlineChartRenderer')

        cache = DummyCache()

        rendered = render('chart', {'datasource_url': 'http://test.com/data',
                                    'cache': cache,
                                    'container_id': 'foo'})
        expected = '\n'.join((
            self.inline_prefix,
            "      containerId: 'foo',",
            "      chartType: 'LineChart',",
            "      dataSourceUrl: 'http://test.com/data'",
            self.inline_postfix))
        self.assertEqual(rendered, expected)

        cache['http://test.com/data'] = self.day_score

        rendered = render('chart', {'datasource_url': 'http://test.com/data',
                                    'cache': cache,
                                    'container_id': 'foo'})
        expected = '\n'.join((
            self.inline_prefix,
            "      containerId: 'foo',",
            "      chartType: 'LineChart',",
            "      dataTable: {}".format(self.day_score_json),
            self.inline_postfix))
        self.assertEqual(rendered, expected)

    def testRenderChartResponseCache(self):
        cache = DummyCache()
        req = pyramid.testing.DummyRequest({'tqx': 'reqId:42'})
        req.path_url = 'http://test.com/data'
        self.config.add_renderer(
            name='chart_response',
            factory='pyramid_charts.ChartResponseRenderer')

        expected = ('google.visualization.Query.setResponse({{"reqId":"42",'
                    '"status":"ok","table":{},"version":"0.6"}});'
                    ).format(self.day_score_json)

        args = {
            'data_table': self.day_score,
            'cache': cache
        }
        rendered = render('chart_response', args, request=req)
        self.assertEqual(rendered, expected)

        self.assertEqual(cache.get('http://test.com/data'), self.day_score)
