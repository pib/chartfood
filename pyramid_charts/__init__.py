from pyramid.renderers import render


def includeme(config):
    config.add_renderer(name='chart',
                        factory='pyramid_charts.InlineChartRenderer')
    config.add_renderer(name='chart_response',
                        factory='pyramid_charts.ChartResponseRenderer')


class InlineChartRenderer(object):
    def __init__(self, info):
        self._info = info

    def __call__(self, args, system):
        if isinstance(args, dict):
            tpl_vars = args.copy()
        else:
            tpl_vars = {'data_table': args}

        tpl_vars.setdefault('container_id', 'chart')

        if 'data_table' in tpl_vars:
            tpl_vars['data_line'] = "dataTable: {}".format(
                tpl_vars['data_table'].ToJSon().decode('utf-8'))
        elif 'datasource_url' in tpl_vars:
            tpl_vars['data_line'] = "dataSourceUrl: '{}'".format(
                tpl_vars['datasource_url'])

        return render('pyramid_charts:templates/inline_chart.pt', tpl_vars)


class ChartResponseRenderer(object):
    def __init__(self, info):
        self._info = info

    def __call__(self, value, system):
        tqx = system['request'].GET.get('tqx')
        return value.ToResponse(tqx=tqx)
