#!/usr/bin/env python

from log import *

from bs4 import BeautifulSoup as bs

MAX_COLS = 32

"""
Collect all relevant tables that contain data of interest, and ignore all tables that
 may not have anything important for data collection.

Optionally, allow to specify the extact table by an index value that may be on a page

"""
def parse_tables_generic(contents, max_columns=32, exclude_tables=[], header_row_depth=0, start_row_depth=0):
    column_names = []
    column_idx = 0
    table_body = 0;
    table_idx = 1;

    # sanity checks ..
    if contents == None or len(contents) == 0:
        warn("Empty contents passed to generic parser")
        return None

    soup = bs(contents, 'html.parser')

    relevant_tables = []
    i = 0

    # grab list of columns from table header
    for table_main in soup.find_all('table'):

        # if we agreed to exclude this table, skip it
        if (table_idx in exclude_tables):
            table_idx=table_idx+1
            continue

        column_names = grab_headers(table_main, MAX_COLS, 
            header_row_depth)

        # if there are no table headers within this table, skip it
        if column_names == None or len(column_names) == 0:
            table_idx=table_idx+1
            continue

        # I think we're good, grab the cell content
        cell_content = grab_cell_content(table_main, column_names, start_row_depth)

        clean_column_names = []
        for idx, column in column_names.iteritems():
            clean_column_names.append(column)

        relevant_tables.append( {
            'headers': clean_column_names,
            'content': cell_content
        } )

        i=i+1
        table_idx=table_idx+1

    return relevant_tables

"""
Grab all the table headers <th> tags found within the table, these are
 going to be our column names. 

Hopefully these can be taken as raw for the most part, but some trimming 
 might be necessary in order to be flexibil across sites

@row_depth introduced in order to parse the column headers from 
            a specified row.

"""
def grab_headers(table_content, max_columns=32, row_depth=0):

    column_names = {}
    i = 0
    column_idx = -1

    for header_tag in table_content.find_all('th'):

        column_idx = column_idx+1;

        # make sure there's content ..
        if len(header_tag.contents) == 0:
            continue

        # grab the contents of the header
        header_content_raw = header_tag.contents[0]

        # if we have enough columns, skip it
        if column_idx > max_columns:
            break

        # if it's an empty column name, skip it
        if header_content_raw == None or header_content_raw == "":
            continue

        # clean up the formatting of the raw content to code style
        header_clean = header_content_raw.lower()
        header_clean = header_clean.replace(' ', '_')

        column_names[column_idx] = header_clean

    # we found column headers, we're done here ..
    if len(column_names) > 0:
        return column_names

    # either this table doesn't have any actual data or column headers 
    #  in it, or the headers are styled differently..

    # another common format instead of <th> is going to be the first
    #  <tr> is going to display the column names, but we can't assume
    #  that.. if the class of the first row contains a 'th', we'll take
    #  that as assurance that it is indeed used for headers  

    rows_tag = table_content.find_all('tr')

    # if there aren't enough rows to fetch from, it ain't the right place
    #  to grab our headers
    if len(rows_tag) <= row_depth: 
        return

    row_tag = rows_tag[row_depth]
    row_class = row_tag.get('class')
    if len(row_class) > 0:
        row_class = row_class[0]

    if "th" not in row_class:
        return None

    column_idx = -1
    for header_tag in row_tag.find_all('td'):

        column_idx = column_idx+1;

        if len(header_tag.contents) == 0:
            continue

        header_content_raw = header_tag.contents[0]

        if column_idx > max_columns:
            break

        if header_content_raw == None or header_content_raw == "":
            continue

        header_clean = header_content_raw.lower()
        header_clean = header_clean.replace(' ', '_')

        column_names[column_idx] = header_clean

    return column_names

"""
Iterate through each row of data in the table.  Iterate through each
 relevant cell (according to the column name indexes) that we have
 an associated column name mapped to.

The return value should be the cell contents, with the same order of 
 values that correspond to the column names.  
Assuming 3 columns, "name", "weight", "height", the return value might
 look like:

[
 [
    "tom",
    123,
    47
 ], [
    "bob",
    321,
    52
 ]

]

"""
def grab_cell_content(table_main, column_names, start_row_depth=0):

    combined_cell_data = []

    start_idx = 0

    for table_row in table_main.find_all('tr'):

        if start_idx < start_row_depth:
            start_idx = start_idx + 1
            continue

        row_content = []

        ## collect all the cells
        cells = table_row.find_all('td')

        cell_idx = -1
        active_column = ""
        active_column_idx = -1

        ## iterate through each cell ..
        for cell in cells:

            cell_idx = cell_idx + 1

            # if there's a new active column, increment our index ..
            if cell_idx in column_names and len(column_names[cell_idx]) > 0:
                active_column = column_names[cell_idx]
                active_column_idx = active_column_idx + 1

            # sanity check we have an active column selected
            if active_column == None or len(active_column) <= 0:
                continue

            cell_content = ""

            if cell.contents != None and len(cell.contents) > 0:

                # clean up the cell data, if there is anything..
                for field in cell.contents:
                    encoded_str = field.encode('utf-8')
                    encoded_str = encoded_str.strip()
                    cell_content = cell_content + encoded_str

            # append it to our existing row 
            if len(row_content) > active_column_idx:
                row_content[active_column_idx] = row_content[active_column_idx] + cell_content
            else:
                row_content.append(cell_content)

        if len(row_content) > 0:
            combined_cell_data.append(row_content)

    return combined_cell_data
