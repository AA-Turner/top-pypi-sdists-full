#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Transcript Parsing
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

"""Parse transcript files."""

import os, html, json
from springheel.splitseps import splitAtSeparators
from typing import List


def readTranscript(file_name: str) -> List[str]:
    """
    Retrieve the contents of the transcript file.

    Parameters
    ----------
    file_name : str
        The path to the transcript file.

    Returns
    -------
    list of str
        Lines from the transcript file.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            text_to_read = f.read()
        if text_to_read:
            return text_to_read
        else:
            return False
    except IOError:
        return False


def jsonTranscript(file_name: str) -> str:
    """
    Parse a JSON transcript file.

    Parameters
    ----------
    file_name : str
        Path to the JSON file to load.

    Returns
    -------
    str
        The converted transcript, in HTML format.

    """
    try:
        with open(file_name, "r", encoding="utf-8") as json_in:
            try:
                j = json.load(json_in)
            ## Maybe it's a non-JSON transcript even if json_mode is true?
            except json.decoder.JSONDecodeError:
                return False
    except FileNotFoundError:
        return False
    first_pass = []
    for line in j["transcript"]:
        dialogue = html.escape(line["line"])
        if "speaker" in line.keys():
            speaker = html.escape(line["speaker"])
            line_string = """<p class="line"><span class="charname">{speaker}</span>: <span class="linedia">{dialogue}</span></p>""".format(
                speaker=speaker, dialogue=dialogue
            )
            first_pass.append(line_string)
        else:
            # Otherwise it is an action.
            action_string = """<p class="action">({dialogue})</p>""".format(
                dialogue=dialogue
            )
            first_pass.append(action_string)
    second_pass = os.linesep.join(first_pass)
    return second_pass


def makeTranscript(file_name: str, json_mode: bool) -> str:
    """
    Create a format transcript from a transcript file.

    Parameters
    ----------
    file_name : str
        The path to the transcript file.
    json_mode : bool
        If True, parse the transcript as a JSON file. Otherwise, expect
        the normal syntax.

    Returns
    -------
    str
        The converted transcript, in HTML format.
    """
    if json_mode:
        second_pass = jsonTranscript(file_name)
        if second_pass:
            return second_pass
        else:
            return False
    raw_transcript = readTranscript(file_name)

    if not raw_transcript:
        return False

    separators = [
        "\r\n",
        "\r",
        "\n",
        "\v",
        "\f",
        "\x1c",
        "\x1d",
        "\x1e",
        "\x85",
        "\u2028",
        "\u2029",
    ]
    doubled_separators = [item * 2 for item in separators]

    ## separate the individual lines
    # sep_transcript = raw_transcript.splitlines()

    if any(sep in raw_transcript for sep in doubled_separators):
        sep_transcript = splitAtSeparators(raw_transcript, doubled_separators)
    else:
        sep_transcript = [raw_transcript]

    sep = "\n"

    ## Initializing a variable to hold the HTML transcript.
    first_pass = []

    for line in sep_transcript:
        # Blank lines are just there for ease of formatting and can be
        # ignored for the final product.
        if not line:
            pass
        elif len(line.splitlines()) > 1:
            # It's a line of dialogue if it has a newline in it.
            split_line = line.splitlines()
            speaker = html.escape(split_line[0])
            dialogue = html.escape(split_line[1].strip())
            line_list = [
                """<p class="line"><span class="charname">""",
                speaker,
                "</span>:",
                "\n",
                """<span class="linedia">""",
                dialogue,
                "</span></p>",
            ]
            line_string = "".join(line_list)
            first_pass.append(line_string)
        else:
            # Otherwise it is an action.
            escaped = html.escape(line)
            action_list = ["""<p class="action">""", escaped, "</p>"]
            action_string = "".join(action_list)
            first_pass.append(action_string)

    sep = "\n"
    second_pass = sep.join(first_pass)
    return second_pass
