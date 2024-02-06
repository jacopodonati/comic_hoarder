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

from platforms.BasicPlatform import BasicPlatform
from urllib.parse import urlparse, urlunparse
import logging
import requests
from lxml import html
import os
import re

PAGE_ERROR = -1
PAGE_ARCHIVE = 1
PAGE_SINGLE = 2

class xkcd(BasicPlatform):
    name = 'xkcd'

    @staticmethod
    def get_comic_number(path):
        comic_number = re.sub('[^0-9]+', '', path)
        return int(comic_number)

    @staticmethod
    def identify_url(url):
        logging.debug(f"Checking what kind of URL is {url}")
        o = urlparse(url)
        re_archive = re.compile('/')
        re_single = re.compile('/[0-9-]+[/]?')
        if re_archive.fullmatch(o.path):
            logging.debug('URL is an archive')
            return PAGE_ARCHIVE
        elif re_single.fullmatch(o.path):
            logging.debug('URL is a single page')
            return PAGE_SINGLE
        else:
            logging.debug('URL error')
            logging.debug(o)
            return PAGE_ERROR
    
    @staticmethod
    def download_archive(url, quantity=1, dry=False):
        logging.debug(f"Downloading {quantity} comic from archive at {url}")
        headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
            }
        page = requests.get(url, headers=headers)
        if (page.status_code == 200):
            tree = html.fromstring(page.text)
            o = urlparse(url)
            latest_path = xkcd.get_comic_number(tree.xpath('//a[@rel="prev"]/@href')[0]) + 1
            latest_url = urlunparse(o._replace(path=str(latest_path)))
            for i in range(quantity):
                logging.debug(f"Latest URL is {latest_url}.")
                xkcd.download_single(latest_url, dry)
                if i < quantity:
                    page = requests.get(latest_url, headers=headers)
                    tree = html.fromstring(page.text)
                    latest_path = xkcd.get_comic_number(tree.xpath('//a[@rel="prev"]/@href')[0])
                    latest_url = urlunparse(o._replace(path=str(latest_path)))

    @staticmethod
    def download_single(url, dry):
        logging.debug(f"Downloading single comic at {url}")
        headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
            }
        page = requests.get(url, headers=headers)
        if (page.status_code == 200):
            tree = html.fromstring(page.text)
            o = urlparse(url)
            comic_title = 'xkcd'
            comic_number = xkcd.get_comic_number(o.path)
            img_url = tree.xpath('//div[@id="comic"]/img/@src')
            if not dry:
                logging.debug(f"Downloading image {img_url[0]}")
                r = requests.get(f"https:{img_url[0]}")
                path = './'
                filename = f"{comic_title} - {comic_number}.png"
                file = os.path.join(path, filename)
                if os.path.exists(file):
                    logging.debug(f"File {file} already exists. Skipping.")
                else:
                    with open(file, 'wb') as fd:
                        logging.debug(f"Writing file {filename} in folder {path}")
                        fd.write(r.content)
            else:
                logging.debug(f"Simulating the download of image {img_url[0]}")
        else:
            logging.error(f"Error downloading {url}. Status code: {page.status_code}")