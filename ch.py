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

if __name__ == "__main__":
    main()