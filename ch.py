# Copyright (C) 2024 Jacopo Donati
# 
# This file is part of comic_hoarder.
# 
# comic_hoarder is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# comic_hoarder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with comic_hoarder.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
from urllib.parse import urlparse
import re

PAGE_ERROR = -1
PAGE_NOT_SUPPORTED = 0
PAGE_ARCHIVE = 1
PAGE_SINGLE = 2

def identify_url(url):
    logging.debug(f"Checking what kind of URL is {url}")
    o = urlparse(url)
    re_archive = re.compile('\/[a-zA-Z0-9\-]+')
    re_single = re.compile('\/[a-zA-Z0-9\-]+\/[0-9]+\/[0-9]+\/[0-9]+')
    if o.hostname != 'www.gocomics.com':
        logging.debug('URL not supported')
        return PAGE_NOT_SUPPORTED
    elif re_archive.fullmatch(o.path):
        logging.debug('URL is an archive')
        return PAGE_ARCHIVE
    elif re_single.fullmatch(o.path):
        logging.debug('URL is a single page')
        return PAGE_SINGLE
    else:
        logging.debug('URL error')
        return PAGE_ERROR

def main():
    # Define the args you can pass
    parser = argparse.ArgumentParser(
                    prog = 'Comic Hoarder',
                    description = 'Downloads comics for later enjoyment',
                    )
    parser.add_argument('url',
                        help='URL of the single comic')
    parser.add_argument('--debug',
                        action='store_true')
    # parser.add_argument('--start-at',
    #                     type=int,
    #                     default=1)
    args = parser.parse_args()

    # Make progressbar play nicely with logging
    progressbar.streams.wrap_stderr()

    if (args.debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug('Booting up')

    # Identify the kind of URL we're working on and act accordingly
    url = args.url
    kind_of_page = identify_url(url)
if __name__ == "__main__":
    main()