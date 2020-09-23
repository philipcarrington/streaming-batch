import json


# read the json schema file:
def get_schema_json(schema_file_name):
    with open('schemas/{}'.format(schema_file_name)) as json_file:
        # Turn the read lint into a dict:
        return json.load(json_file)


def get_file_columns_from_dict(schema):
    return schema['properties']['file_columns']['properties']


def get_schema_columns(file_columns_schema):
    columns = []
    for field_name in file_columns_schema:
        columns.append(field_name)

    return columns


def get_schema_columns_datatypes(file_columns_schema):
    column_dtype = {}
    for column_name, column_attributes in file_columns_schema.items():
        column_data_types = column_attributes['type']
        if isinstance(column_data_types, list):
            column_data_type = column_data_types[0]
        else:
            column_data_type = column_data_types

        if column_data_type == 'string':
            pandas_data_type = 'str'
        elif column_data_type == 'number':
            pandas_data_type = 'float64'
        elif column_data_type == 'integer':
            pandas_data_type = 'int64'

        column_dtype[column_name] = pandas_data_type

    return column_dtype


if __name__ == '__main__':
    schema_dict = get_schema_json(schema_file_name='hxuk_arrivals_v3.json')
    schema_file_columns = get_file_columns_from_dict(schema=schema_dict)
    schema_columns = get_schema_columns(file_columns_schema=schema_file_columns)
    schema_columns_datatypes = get_schema_columns_datatypes(file_columns_schema=schema_file_columns)
