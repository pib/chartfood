from pyramid.renderers import render


def includeme(config):
    config.add_renderer(name='chart',
                        factory='chartfood.InlineChartRenderer')
    config.add_renderer(name='chart_response',
                        factory='chartfood.ChartResponseRenderer')


class ChartRenderer(object):

    def cache_get(self, args):
        try:
            return args['cache'].get(args['datasource_url'])
        except KeyError:
            return None

    def cache_set(self, args, data):
        try:
            args['cache'].put(args['datasource_url'], data)
        except KeyError:
            return


class InlineChartRenderer(ChartRenderer):
    def __init__(self, info):
        self._info = info

    def __call__(self, args, system):
        if isinstance(args, dict):
            tpl_vars = args.copy()
            cached_data = self.cache_get(tpl_vars)
            if cached_data:
                tpl_vars['data_table'] = cached_data
        else:
            tpl_vars = {'data_table': args}
            cached_data = None

        tpl_vars.setdefault('container_id', 'chart')

        if 'data_table' in tpl_vars:
            data = tpl_vars['data_table'].ToJSon().decode('utf-8')
            if not cached_data:
                self.cache_set(tpl_vars, tpl_vars['data_table'])
            tpl_vars['data_line'] = "dataTable: {}".format(data)
        elif 'datasource_url' in tpl_vars:
            tpl_vars['data_line'] = "dataSourceUrl: '{}'".format(
                tpl_vars['datasource_url'])

        return render('chartfood:templates/inline_chart.pt', tpl_vars)


class ChartResponseRenderer(ChartRenderer):
    def __init__(self, info):
        self._info = info

    def __call__(self, args, system):
        if not isinstance(args, dict):
            args = {'data_table': args}

        args.setdefault('datasource_url', system['request'].path_url)
        self.cache_set(args, args['data_table'])

        tqx = system['request'].GET.get('tqx')
        return args['data_table'].ToResponse(tqx=tqx)
