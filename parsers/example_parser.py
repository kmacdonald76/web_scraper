#!/usr/bin/env python

import calendar
import datetime
import time
import re

from log import *
from database import table_insert
from database import db_delete

from random import randint
from bs4 import BeautifulSoup as bs
from parsers.html import parse_tables_generic
from parsers.team import fetch_teams
from network import fetch_static_page
from parsers.common import column_cleanup

db_name = 'dbname'
db_user = 'user'
MAX_COLS = 32
some_dank_url = 'https://dank.com'

def parse_example():

    contents = fetch_static_page(some_dank_url, False, randint(3,5))

    # retry if fetch failed ..
    if contents == None or len(contents) == 0:

        for retry in range(1,3):
            info("Retrying (" + some_dank_url + ")")
            contents = fetch_static_page(some_dank_url, True, randint(5,7))
            if contents != None and len(contents) > 0:
                break

        # give up.. reset the retry counter and continue to the next page ..
        if contents == None:
            warn("Giving up (" + some_dank_url + ")")
            return False


    # sometimes headers are defined in a <th>, but this example, it's the first row in the table
    # and content should start from the second row
    header_depth = 1
    table_contents = parse_tables_generic(contents, MAX_COLS, [], header_depth, header_depth+1)

    # if we don't have any data to work with, we're done here
    if table_contents == None or len(table_contents) == 0:
        info("No data found ..")
        return False

    table_contents = post_massage(table_contents, [], {'year': year})
    table_insert('table_name', table_contents)

    return False


"""
 do some custom massaging of the data ..
"""
def post_massage(content, table_type, add_columns=[], meta_data={}):

    # columns to drop ..
    remove_columns = [ 'bad_col1', 'bad_col2', 'string_time' ]

    modified_contents = []

    for table_content in table_contents:

        headers = table_content['headers']
        for new_col in add_columns:
            headers.append(new_col)

        # identify which column you want to modify
        modify_idx_example = 2
        modify_idx_time = 4

        # be prepared to ignore certain rows of our choosing..
        ignored_rows = []

        # ready to iterate through each row ..
        iter_idx = -1
        for record in table_content['content']:
            iter_idx = iter_idx + 1

            # Example 1: ignore empty rows
            if len(record) <= 0 :
                delete_rows.append(iter_idx)
                continue

            # Example 2: if our column contains a link tag, and we want  
            # the inner text and URL split into two columns i.e. 
            #
            #  <a href="http://some_interesting_link/>Cool name</a>
            #
            #     ------------------------------- -----------
            #    |       Interesting Url         |    Name   |
            #     ------------------------------- -----------
            #    | http://some_interesting_link/ | Cool name |
            #     ------------------------------- -----------
            #
            example_col = record[modify_idx_example]
            soup = bs(example_col, 'html.parser')
            link_tags = soup.find_all('a')
            if len(link_tags) != 2:
                warn("failed to find url in row!")
                return

            interesting_url = link_tags[0].get('href')
            name = link_tags[0].contents[0]
            record.append(interesting_url)
            record.append(name)

            # Example 3: converting a string 'timestamp' value to an epoch
            date_col = record[modify_idx_time] + " " + str(meta_data['year'])
            date = datetime.datetime.strptime(date_col, "%b %d %Y")
            timestamp = calendar.timegm(date.utctimetuple())
            record.append(timestamp)

        # delete any rows marked as such
        if len(delete_rows) > 0:
            idx = 0
            for d_idx in delete_rows:
                del table_content['content'][d_idx - idx]
                idx = idx + 1

        # note the columns ids we want to ditch ..
        table_content = column_cleanup(headers, remove_columns, table_content['content'])
        modified_contents.append(table_content)

    return modified_contents

