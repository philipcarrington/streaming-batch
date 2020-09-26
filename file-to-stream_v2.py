# Load various libs:
import pandas as pd
import csv
import sys
from io import StringIO
from datetime import date
import json

# Get the local libs:
from pandas_schema_from_file import get_schema_json, get_file_columns_from_dict, \
    get_schema_columns, get_schema_columns_datatypes
from pandas_bad_rows_dealer import parse_bad_rows_string, write_bad_rows_file
from generate_payload_meta import get_meta_data


@staticmethod
def create_event(dicts):
    # construct event by joining meta and data
    json = {}
    for d in dicts:
        json.update(d)
    return json


def write_event_to_file(
        good_output_filename,
        event
):
    with open(good_output_filename, "a+") as fp:
        json.dump(event, fp)
        fp.write("\n")


def combine_and_write_meta_and_data(
        meta,
        data_output,
        output_filename
):
    file_columns_data = {}
    for items in data_output:
        file_columns_data['file_columns'] = items

        file_data = json.dumps({**meta, **file_columns_data})

        write_event_to_file(
            output_filename,
            file_data
        )


def delimited_file_to_json(
        # File data:
        data_file_dir,
        data_file_name,
        output_file_dir,
        schema_file_name,
        file_delimiter=',',
        skip_rows=0,
        footer_rows=0,
        # Meta data:
        is_client=False,
        service='airflow-data-products',
        environment='production',
        schema_version='1.0.0',
        published=date.today().strftime("%Y-%m-%d %H:%m:%s"),
        organisation='Holiday Extras Limited',
        data_context='batch__streaming'
):
    # Create the file names to be used:
    input_filepath = '{}/{}'.format(data_file_dir, data_file_name)
    good_output_filename = '{}{}.json'.format(output_file_dir, data_file_name)
    bad_output_filename = '{}{}_BAD.json'.format(output_file_dir, data_file_name)
    bad_report_output_filename = '{}{}_BAD_REPORT.txt'.format(output_file_dir, data_file_name)

    # Get the column names:
    schema_dict = get_schema_json(schema_file_name=schema_file_name)
    schema_file_columns = get_file_columns_from_dict(schema=schema_dict)
    schema_columns = get_schema_columns(file_columns_schema=schema_file_columns)
    schema_columns_datatypes = get_schema_columns_datatypes(file_columns_schema=schema_file_columns)

    # To reporting on the errors:
    cur_stderr = sys.stderr
    bad_report = StringIO()
    sys.stderr = bad_report

    # Process the data:
    data = pd.read_csv(
        # The file name to load;
        input_filepath,
        # Set the file delimiter:
        sep=file_delimiter,
        # The number of header rows:
        skiprows=skip_rows,
        # Replace the column names
        header=0,
        names=schema_columns,
        # The column types:
        dtype=schema_columns_datatypes,
        # The number of rows at the bottom of the file:
        skipfooter=footer_rows,
        # Does the file have quoted chars:
        quoting=csv.QUOTE_ALL,
        # Chauntry files ar rubbish:
        encoding='latin-1',
        # Remove the padding from start of fields:
        skipinitialspace=True,
        # So it does not put NAN in:
        keep_default_na=False,
        # Makes the bad line disappear!:
        error_bad_lines=False,
        warn_bad_lines=True
    )

    # Capture the bad lines:
    sys.stderr = cur_stderr
    result_string = bad_report.getvalue()

    # Get the bad rows and the reason
    bad_rows_dict = parse_bad_rows_string(result_string)
    write_bad_rows_file(
        data_file_name,
        bad_rows_dict,
        input_filepath,
        bad_output_filename
    )

    # Generate the meta data:
    payload_meta = get_meta_data(
        event_type=data_file_name,
        is_client=is_client,
        service=service,
        environment=environment,
        schema_version=schema_version,
        published=published,
        organisation=organisation,
        data_context=data_context
    )

    # Turn the dataframe into data for the file:
    data_output = data.to_dict(orient='records')

    # Combine the dicts and write to file:
    combine_and_write_meta_and_data(
        payload_meta,
        data_output,
        good_output_filename
    )

if __name__ == '__main__':
    delimited_file_to_json(
        data_file_dir='data/working/',
        data_file_name='HXUK_ARRIVAL_DAILY_EXPORT',
        output_file_dir='data/output/',
        schema_file_name='hxuk_arrivals_v3.json',
        file_delimiter='\t',
        skip_rows=0, # 0 based therefore 0 is line 1 (the headers)
        is_client=False,
        service='airflow-data-products',
        environment='production',
        schema_version='1.0.0',
        published=date.today().strftime("%Y-%m-%d %H:%m:%s"),
        organisation='Holiday Extras Limited',
        data_context='batch__streaming'
    )
