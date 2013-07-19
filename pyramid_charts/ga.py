from .gviz_api import DataTable
from datetime import datetime


_name_to_type = {
    'ga:date': 'date'
}
_type_to_type = {
    'INTEGER': 'number',
    'STRING': 'string'
}


class GaDataTable(DataTable):
    def __init__(self, ga_data):
        """ A DataTable which takes a Google Analytics response dict
        """

        columns = [self.convert_ga_column(c) for c in ga_data['columnHeaders']]
        column_types = [c[1] for c in columns]
        data = self.convert_ga_rows(ga_data['rows'], column_types)

        super(GaDataTable, self).__init__(columns, data)

    def convert_ga_column(self, column):
        name = column['name']
        dtype = column['dataType']
        return (
            name,
            _name_to_type.get(name, _type_to_type.get(dtype, 'string')),
            name.split(':')[1].capitalize()
        )

    def convert_ga_rows(self, rows, column_types):
        convert_fns = [getattr(self, '_convert_ga_' + ctype)
                       for ctype in column_types]
        return [[fn(data) for data, fn in zip(row, convert_fns)]
                for row in rows]

    def _convert_ga_date(self, date_str):
        return datetime.strptime(date_str, '%Y%m%d')

    def _convert_ga_number(self, num_str):
        try:
            return int(num_str)
        except ValueError:
            return float(num_str)

    def _convert_ga_string(self, s):
        return s
