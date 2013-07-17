def includeme(config):
    config.add_renderer(name='chart', factory='pyramid_charts.InlineChartRenderer')


class InlineChartRenderer(object):
    def __init__(self, info):
        self._info = info

    def __call__(self, value, system):
        tpl = """\
<div id="chart"></div>
<script>
  google.load('visualization', '1');
  google.setOnLoadCallback(function() {{
    var data = {};
    google.visualization.drawChart({{
      containerId: 'chart',
      chartType: 'LineChart',
      dataTable: data
    }});
  }});
</script>"""
        return tpl.format(value.ToJSon().decode('utf-8'))
