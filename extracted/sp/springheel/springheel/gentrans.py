#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Translation generator
########
##  Copyright 2017-2020 garrick. Some rights reserved.
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

"""Get translation strings."""

import json, logging
from springheel.tl import gettext as _


def generateTranslations(lang: str, strings_path: str) -> dict:
    """
    Get language strings from the translation file.

    You may ask why I don't use the existing i18n methods, like gettext.
    Putting strings in a user-editable JSON file makes it far easier for fluent
    speakers to correct mistakes or oddities in my translations. Based on
    experience with other static site generators, I resolved that it should be
    possible to fix the TL of a Springheel site with a simple text editor and
    little or no technical knowledge. No re-installing Springheel, editing
    system settings, entering your root password, figuring out how to build pot
    files, or joining mailing lists. Just change one file and you're done.
    This method also allows one to build a site in a different language than
    the "system" language, which is more valuable than it sounds.

    Parameters
    ----------
    lang : str
        The site language.
    strings_path : str
        The path to the strings.json translation file.

    Returns
    -------
    dict
        All sorts of UI strings in the site language. Sub-dict
        "language_names" has language code-name mappings.
    """
    with open(strings_path, "r", encoding="utf-8") as f:
        try:
            json_data = json.load(f)
        except json.decoder.JSONDecodeError:
            logging.error(
                _(
                    "Unable to load translation strings. The string file {strings_path} may be invalid or missing."
                ).format(strings_path=strings_path)
            )
            return False
    strings = {}
    for stringname, langvals in json_data.items():
        # Try for the expected language and default to English if it doesn't
        # have that string
        try:
            strings[stringname] = langvals[lang]
        except KeyError:
            strings[stringname] = langvals["en"]
    # Language names should stay as a dictionary
    strings["language_names"] = json_data["language_names"]
    return strings
