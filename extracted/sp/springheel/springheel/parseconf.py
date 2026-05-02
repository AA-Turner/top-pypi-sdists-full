#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Configuration Parser
########
##  Copyright 2017 garrick. Some rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU Lesser General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Parse configuration files."""

import configparser, os


def comicCParse(conf: str) -> dict:
    """
    Parse a configuration file.

    Parameters
    ----------
    conf : str
        The path to the configuration file.

    Returns
    -------
    dict
        The comic's configuration file formatted as a dictionary.
    """

    parser = configparser.ConfigParser()
    cc = parser.read(conf, encoding="utf-8")
    if not cc:
        raise ValueError("No config file for this comic")
    comic_config = dict(parser.items("ComicConfig"))
    for k, v in comic_config.items():
        try:
            v = parser.getboolean("ComicConfig", k)
            comic_config.update({k: v})
        except ValueError:
            pass

    # Line breaks
    try:
        about = comic_config["about"].replace("\\r", "\r").replace("\\n", "\n")
        comic_config.update({"about": about})
    except KeyError:
        pass
    return comic_config
