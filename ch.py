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
import requests
from lxml import html
import os

PAGE_ERROR = -1
PAGE_NOT_SUPPORTED = 0
PAGE_ARCHIVE = 1
PAGE_SINGLE = 2

def download_single(url):
    logging.debug(f"Downloading single comic at {url}")
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
        }
    page = requests.get(url, headers=headers)
    if (page.status_code == 200):
        tree = html.fromstring(page.text)
        comic_title = tree.xpath('//div[@data-shareable-model="FeatureItem"]/@data-feature-name')
        comic_date = tree.xpath('//div[@data-shareable-model="FeatureItem"]/@data-date')
        img_url = tree.xpath('//picture[@class="item-comic-image"]/img/@src')
        logging.debug(f"Downloading image {img_url[0]}")
        r = requests.get(img_url[0])
        path = './'
        filename = f"{comic_title[0]} - {comic_date[0]}.gif"
        with open(os.path.join(path, filename), 'wb') as fd:
            logging.debug(f"Writing file {filename} in folder {path}")
            fd.write(r.content)
    else:
        logging.error(f"Error downloading {url}. Status code: {page.status_code}")

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
    args = parser.parse_args()

    # Set up logging
    if (args.debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug('Booting up')

    # Identify the kind of URL we're working on and act accordingly
    url = args.url
    kind_of_page = identify_url(url)
    if (kind_of_page == PAGE_SINGLE):
        download_single(url)

if __name__ == "__main__":
    main()