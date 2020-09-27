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
