#!/usr/bin/env python

from log import *

"""
 Common functionality that can be used in many parsers ..
"""

def column_cleanup(headers, ditch_map, table_contents):

    # note the columns ids we want to ditch ..
    ditch_idx = 0
    ditch_ids = []
    for header in headers:
        for ditch_col in ditch_map:
            if header == ditch_col:
                ditch_ids.append(ditch_idx)
                break

        ditch_idx = ditch_idx + 1

    # confirm we have some columns to ditch, otherwise we're done
    if len(ditch_ids) == 0:
        return table_contents

    # add all the ones we want to a temp list
    cleaned_headers = []
    idx = 0
    for header in headers:
        if idx not in ditch_ids:
            cleaned_headers.append(header)
        idx = idx + 1

    cleaned_contents = []

    # then iterate through the records and actually delete the cell content
    for record in table_contents:
        tmp_record = []
        i = 0
        for cell in record:
            if i not in ditch_ids:
                tmp_record.append(cell)
            i = i + 1

        cleaned_contents.append(tmp_record)

    cleaned_contents = {
        'headers': cleaned_headers,
        'content': cleaned_contents
    }

    return cleaned_contents
