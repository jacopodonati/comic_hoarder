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

from platforms import *

PAGE_NOT_SUPPORTED = 0
PAGE_ERROR = -1
PAGE_ARCHIVE = 1
PAGE_SINGLE = 2

def get_platform(url):
    logging.debug(f"Checking which platform hosts the comic")
    platforms = {
        'www.gocomics.com': GoComics}
    o = urlparse(url)
    if o.hostname in platforms:
        p = platforms[o.hostname]
        logging.debug(f"URL is hosted on {p.name}")
        return p
    else:
        logging.debug('URL not supported')
        return PAGE_NOT_SUPPORTED


def main():
    # Define the args you can pass
    parser = argparse.ArgumentParser(
                    prog='Comic Hoarder',
                    description='Downloads comics for later enjoyment',
                    )
    parser.add_argument('url',
                        help='URL of the single comic'
                        )
    parser.add_argument('--debug',
                        action='store_true'
                        )
    parser.add_argument('--dry',
                        default=False,
                        action='store_true',
                        help='Simulate the download without downloading any file'
                        )
    parser.add_argument('--quantity',
                        nargs=1,
                        default=1,
                        type=int,
                        help='How many comics to download from an archive. Default is 1 (i.e. the latest).'
                        )
    args = parser.parse_args()

    # Set up logging
    if (args.debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug('Booting up')

    # Identify the kind of URL we're working on and act accordingly
    settings = {}
    settings['url'] = args.url
    settings['dry'] = args.dry
    settings['quantity'] = args.quantity[0]
    logging.debug(f"Downloading {settings['quantity']} comics from {settings['url']}.")
    platform = get_platform(settings['url'])
    if platform != PAGE_NOT_SUPPORTED:
        settings['kind_of_page'] = platform.identify_url(url=settings['url'])
        if (settings['kind_of_page'] == PAGE_SINGLE):
            platform.download_single(url=settings['url'], dry=settings['dry'])
        elif (settings['kind_of_page'] == PAGE_ARCHIVE):
            platform.download_archive(url=settings['url'], quantity=settings['quantity'], dry=settings['dry'])

if __name__ == "__main__":
    main()