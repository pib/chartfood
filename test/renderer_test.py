from datetime import date
from nose.tools import assert_equals
from pyramid_charts.gviz_api import DataTable
from pyramid.renderers import render

import pyramid.testing
import unittest


class GoogleInlineChartTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.config = pyramid.testing.setUp()

    def tearDown(self):
        pyramid.testing.tearDown()

    def testRenderInlineGoogleChart(self):
        self.config.add_renderer(name='chart', factory='pyramid_charts.InlineChartRenderer')

        table = DataTable([('day', 'date'), ('score', 'number')],
                          [[date(2013, 12, 11), 42],
                           [date(2013, 12, 12), 45],
                           [date(2013, 12, 13), 32],
                           [date(2013, 12, 14), 15]])

        rendered = render('chart', table)
        expected = """\
<div id="chart"></div>
<script>
  google.load('visualization', '1');
  google.setOnLoadCallback(function() {
    var data = {"cols":[{"id":"day","label":"day","type":"date"},{"id":"score","label":"score","type":"number"}],"rows":[{"c":[{"v":"Date(2013,11,11)"},{"v":42}]},{"c":[{"v":"Date(2013,11,12)"},{"v":45}]},{"c":[{"v":"Date(2013,11,13)"},{"v":32}]},{"c":[{"v":"Date(2013,11,14)"},{"v":15}]}]};
    google.visualization.drawChart({
      containerId: 'chart',
      chartType: 'LineChart',
      dataTable: data
    });
  });
</script>"""
        self.assertEqual(rendered, expected)
