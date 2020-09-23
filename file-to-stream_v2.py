# Load various libs:
import pandas as pd
import csv

# Get the local libs:
from pandas_schema_from_file import get_schema_json, get_file_columns_from_dict, \
    get_schema_columns, get_schema_columns_datatypes

def csv_file_to_json(
        data_file_name,
        schema_file_name,
        file_delimiter=',',
        header_rows=0,
        footer_rows=0
):
    # Get the column names:
    if header_rows == 0:
        schema_dict = get_schema_json(schema_file_name=schema_file_name)
        schema_file_columns = get_file_columns_from_dict(schema=schema_dict)
        schema_columns = get_schema_columns(file_columns_schema=schema_file_columns)
        schema_columns_datatypes = get_schema_columns_datatypes(file_columns_schema=schema_file_columns)

    # Process the data:
    data = pd.read_csv(
        # The file name to load;
        data_file_name,
        # Set the file delimeter:
        sep=file_delimiter,
        # The number of header rows:
        header=header_rows,
        # The column names
        names=schema_columns,
        # The column types:
        dtype=schema_columns_datatypes,
        # The number of rows at the bottom of the file:
        skipfooter=footer_rows,
        # Does the file have quoted chars:
        quoting=csv.QUOTE_ALL,
        # Chauntry files ar rubbish:
        encoding='latin-1'
    )

    out = data.to_dict(orient='records')

    with open('data/output/HXUK_ARRIVAL_DAILY_EXPORT.json', 'w') as output_file:
        for json_payloads in out:
            output_file.write('%s\n' % json_payloads)


if __name__ == '__main__':
    csv_file_to_json(
        data_file_name='data/working/HXUK_ARRIVAL_DAILY_EXPORT',
        schema_file_name='hxuk_arrivals_v3.json',
        file_delimiter='\t'
    )
