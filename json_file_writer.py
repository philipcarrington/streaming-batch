import json


def create_event(dicts):
    # construct event by joining meta and data
    json = {}
    for d in dicts:
        json.update(d)
    return json


def write_event_to_file(
        output_filename,
        event
):
    with open(output_filename, "a+") as output_data:
        output_data.write('%s\n' % json.dumps(event))


def combine_and_write_meta_and_data(
        meta,
        data_output,
        output_filename,
        dict_name='file_columns'
):
    file_columns_data = {}
    if isinstance(data_output, list):
        for items in data_output:
            file_columns_data[dict_name] = items

            file_data = ({**meta, **file_columns_data})

            write_event_to_file(
                output_filename,
                file_data
            )
    elif isinstance(data_output, dict):
        file_columns_data[dict_name] = data_output
        file_data = ({**meta, **file_columns_data})

        write_event_to_file(
            output_filename,
            file_data
        )

def write_bad_rows_file(
        data_file_name,
        bad_payload_meta,
        bad_rows_dict,
        input_filepath,
        bad_output_filename
):
    # Make a var of the file:
    input_data = open(input_filepath, 'r')
    input_data_lines = input_data.readlines()

    # Dict for json'ing:
    bad_data_dict = {}
    bad_data_file_dict = {}

    # output_data = open(bad_output_filename, 'w')

    for file_line_no, std_out_reason in bad_rows_dict.items():
        bad_data_dict['file_name'] = data_file_name
        bad_data_dict['file_line_no'] = file_line_no
        bad_data_dict['reason'] = std_out_reason
        bad_data_dict['data'] = input_data_lines[file_line_no - 1]

        print(bad_data_dict)
        combine_and_write_meta_and_data(
            bad_payload_meta,
            bad_data_dict,
            bad_output_filename,
            'bad_file_data'
        )

        # output_data.write('%s\n' % json.dumps(bad_data_out_dict))