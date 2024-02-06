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

__all__ = [
    'BasicPlatform',
    'GoComics',
    'xkcd'
]

from platforms.BasicPlatform import BasicPlatform
from platforms.GoComics import GoComics
from platforms.xkcd import xkcd