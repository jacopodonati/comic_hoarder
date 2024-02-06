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

class GoComics(BasicPlatform):
    name = 'GoComics'

    @staticmethod
    def identify_url(url):
        logging.debug(f"Checking what kind of URL is {url}")
        o = urlparse(url)
        re_archive = re.compile('/[a-zA-Z0-9-]+')
        re_single = re.compile('/[a-zA-Z0-9-]+/[0-9]+/[0-9]+/[0-9]+')
        if re_archive.fullmatch(o.path):
            logging.debug('URL is an archive')
            return PAGE_ARCHIVE
        elif re_single.fullmatch(o.path):
            logging.debug('URL is a single page')
            return PAGE_SINGLE
        else:
            logging.debug('URL error')
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
            latest_path = tree.xpath('//span[text()="Read Now"]/ancestor::div/ancestor::div/ancestor::a/@href')
            latest_url = urlunparse(o._replace(path=latest_path[0]))
            for i in range(quantity):
                logging.debug(f"Latest URL is {latest_url}.")
                GoComics.download_single(latest_url, dry)
                if i < quantity:
                    page = requests.get(latest_url, headers=headers)
                    tree = html.fromstring(page.text)
                    latest_path = tree.xpath('//a[contains(@class, "js-previous-comic")]/@href')
                    latest_url = urlunparse(o._replace(path=latest_path[0]))

    @staticmethod
    def download_single(url, dry):
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
            if not dry:
                logging.debug(f"Downloading image {img_url[0]}")
                r = requests.get(img_url[0])
                path = './'
                filename = f"{comic_title[0]} - {comic_date[0]}.gif"
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