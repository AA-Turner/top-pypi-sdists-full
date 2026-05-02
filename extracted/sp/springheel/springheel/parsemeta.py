#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Metadata Parsing
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

"""Parse metadata files."""

import springheel.parseconf
from slugify import slugify
import html, json
import logging
from typing import Tuple, List
from springheel.tl import gettext as _


def readMeta(file_name: str) -> List[str]:
    """
    Retrieve a metadata file.

    Parameters
    ----------
    file_name : str
        The path to the metadata file.

    Returns
    -------
    list of str
        Lines from the metadata file.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            text_to_read = f.read().splitlines()
    except FileNotFoundError:
        logging.error(_("File {file_name} not found.").format(file_name=file_name))
    except IOError:
        logging.error(
            _(
                "An I/O error has occurred. {file_name} seems to exist but I'm unable to open it. It may be corrupt."
            ).format(file_name=file_name)
        )
        return False
    except UnboundLocalError:
        logging.error(
            _(
                "An Unbound Local Error has occurred on file {file_name}. I'm probably looking for a page that doesn't exist."
            ).format(file_name=file_name)
        )
        return False
    return text_to_read


def getMetaCom(meta_raw: list, translated_strings: dict) -> Tuple[list, list]:
    """
    Separate the metadata from formatting info and commentary.

    Parameters
    ----------
    meta_raw : list
        Lines from the metadata file.
    translated_strings : dict
        The translation file contents for this site.

    Returns
    -------
    meta_nl : list
        Metadata lines with key: value pairs.
    comments : list
        HTML-escaped creator commentary lines.
    """
    meta_nl = []
    comments = []
    for i in [item for item in meta_raw if item]:
        if set(i.strip()) == {"-"}:
            continue
        else:
            if i[0:2] == "  ":
                meta_nl.append(i.strip())
            else:
                comments.append(html.escape(i))
    if not comments:
        comments = [translated_strings["no_comment"]]
    return (meta_nl, comments)


def dictizeMeta(m: list, file_name: str) -> dict:
    """
    Convert the plain metadata into a dictionary.

    Parameters
    ----------
    m : list
        A list of lines with colon-separated metadata.
    file_name : str
        The path to the metadata file.

    Returns
    -------
    dict
        The dictionary-fied metadata.
    """
    meta = []
    for i in m:
        s = i.split(": ", 1)
        try:
            d = {s[0]: s[1]}
        except IndexError:
            logging.warning(
                _(
                    "Error: No value set for {s} in {file_name}. Remaining generation may fail."
                ).format(s=s[0], file_name=file_name)
            )
        meta.append(d)
    result = {}
    for d in meta:
        result.update(d)
    meta = result
    return meta


def readJsonMeta(file_name: str, translated_strings: dict) -> dict:
    """
    Retrieve a metadata file in JSON format.

    Parameters
    ----------
    file_name : str
        The path to the metadata file.
    translated_strings : dict
        The translation file contents for this site.

    Returns
    -------
    dict
        A dictionary of strip metadata.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as json_in:
            j = json.load(json_in)
    except IOError:
        logging.error(_("An I/O error has occurred."))
        return False
    except UnboundLocalError:
        logging.error(
            _(
                "An Unbound Local Error has occurred. I'm probably looking for a page that doesn't exist."
            )
        )
        return False
    # Maybe it's a non-JSON transcript even if json_mode is true?
    except json.decoder.JSONDecodeError:
        return False, False
    meta = j["metadata"]
    c = meta["commentary"]
    if not c:
        c = [translated_strings["no_comment"]]
    escaped_c = [html.escape(item) for item in c if item]
    return meta, escaped_c


def parseMetadata(
    file_name: str, translated_strings: dict, json_mode: bool
) -> Tuple[dict, str, list]:
    """
    Read a comic strip metadata file.

    Parameters
    ----------
    file_name : str
        The path to the metadata file.
    translated_strings : dict
        The translation file contents for this site.
    json_mode : bool
        Whether to load the metadata file as JSON (True) or plain text
        (False).

    Returns
    -------
    meta : dict
        A dictionary of strip metadata.
    commentary : str
        Creator commentary formatted as HTML paragraphs.
    c : list
        Raw commentary block.
    """

    if json_mode:
        meta, c = readJsonMeta(file_name, translated_strings)
        if not meta:
            # Read the metadata from the file.
            meta_raw = readMeta(file_name)
            # Get the metadata proper and the commentary.
            m, c = getMetaCom(meta_raw, translated_strings)
            # Convert the metadata list to a dictionary.
            meta = dictizeMeta(m, file_name)
    else:
        # Read the metadata from the file.
        meta_raw = readMeta(file_name)
        # Get the metadata proper and the commentary.
        m, c = getMetaCom(meta_raw, translated_strings)
        # Convert the metadata list to a dictionary.
        meta = dictizeMeta(m, file_name)

    # Create slug if unspecified.
    meta.setdefault(
        "title_slug", slugify(meta["title"], lowercase=True, max_length=200)
    )

    # Format commentary lines.
    commentary = []
    for line in c:
        comm = ["<p>", line, "</p>"]
        comm = "".join(comm)
        commentary.append(comm)
    commentary = "".join(commentary)
    return meta, commentary, c
