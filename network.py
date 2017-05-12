#!/usr/bin/env python

from log import *
from urllib2 import urlopen
import hashlib
import os.path
import time

"""
Given the url, check if it's been cached already..  

If it has, fetch the cached version.

If it hasn't, fetch it over the web, and cache it for next time.

TODO :: implement a time-till-stale so that pages can be partially
         static .. i.e. when fetching the player list, these pages
         are likely to change drastically every season

"""
def fetch_static_page(url, clean=False, sleep=5):

    hash_obj = hashlib.sha1(url)
    hex_dig = hash_obj.hexdigest()
    cached_file = "static_cache/" + hex_dig + ".cache"

    # if the file is cached, and we don't want clean copy
    if clean == False and os.path.isfile(cached_file):
        with open(cached_file, 'r') as content_file:
            return content_file.read()

    time.sleep(sleep)

    # if not, download the contents and cache it
    content_file = urlopen(url)
    test = content_file.read()

    file = open(cached_file, "w")
    file.write(test)
    file.close()

    return test


