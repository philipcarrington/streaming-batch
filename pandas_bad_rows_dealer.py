import json


def parse_bad_rows_string(bad_result_string):
    # Split the output string by sep into "lines":
    split_bad_result_string = bad_result_string.split('\\n')

    # For all the "lines" get the line number and the reason:
    bad_line_dict = {}
    for bad_lines in split_bad_result_string:
        bad_line_split_space = bad_lines.split(' ')
        bad_line_split_colon = bad_lines.split(':')

        if len(bad_line_split_space) > 2:
            bad_line_number = int(bad_line_split_space[2].replace(':', ''))
        if len(bad_line_split_colon) > 1:
            bad_line_reason = bad_line_split_colon[1]

        bad_line_dict[bad_line_number] = bad_line_reason

    return bad_line_dict


def write_bad_rows_file(
        data_file_name,
        bad_rows_dict,
        input_filepath,
        bad_output_filename
):
    # Make a var of the file:
    input_data = open(input_filepath, 'r')
    input_data_lines = input_data.readlines()

    # Dict for json'ing:
    bad_data_out_dict = {}

    output_data = open(bad_output_filename, 'w')

    for file_line_no, std_out_reason in bad_rows_dict.items():
        bad_data_out_dict['file_name'] = data_file_name
        bad_data_out_dict['file_line_no'] = file_line_no
        bad_data_out_dict['reason'] = std_out_reason
        bad_data_out_dict['data'] = input_data_lines[file_line_no - 1]

        output_data.write('%s\n' % json.dumps(bad_data_out_dict))