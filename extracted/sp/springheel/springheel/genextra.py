#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Extra Page Generation
########
##  Copyright 2019 garrick. Some rights reserved.
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

"""Generate extras pages."""

import json, os, shutil
from springheel.classes import EXpage
import springheel.acopy
from typing import Tuple
import logging

copyfile = springheel.acopy.wrap(shutil.copyfile)


def duH(size_in_b: int, decimal_separator: str) -> str:
    """
    Convert a filesize from bytes to kibibytes or mebibytes.

    Used for indicating the filesize of downloads on extra pages in a
    more human-comprehensible manner.

    Parameters
    ----------
    size_in_b : int
        The filesize in bytes.
    decimal_separator : str
        The decimal separator used by the current site locale.

    Returns
    -------
    str
        The filesize and unit used.

    Examples
    --------
    >>> springheel.genextra.duH(2357621, ".")
    '2.2 MiB'
    """
    kib = 1024
    mib = 1048576
    if size_in_b >= 1024:
        if size_in_b // kib >= 1024:
            h_size = size_in_b / mib
            formatted = "{0:.1f}".format(h_size)
            scale = "MiB"
        else:
            h_size = size_in_b / kib
            formatted = "{0:.1f}".format(h_size)
            scale = "KiB"
    else:
        h_size = size_in_b
        formatted = "{0:.1f}".format(h_size)
        scale = "B"
    if formatted[-2:] == ".0":
        formatted = formatted[:-2]
    if decimal_separator != ".":
        formatted = formatted.replace(".", decimal_separator)
    formatted_w_ext = "{num} {scale}".format(num=formatted, scale=scale)
    return formatted_w_ext


def gen_extra(
    i_path: str, o_path: str, extras_j: str, translated_strings: dict, all_images: dict
) -> Tuple[EXpage, dict]:
    """
    Generate an extras page.

    Parameters
    ----------
    i_path : str
        Path to the input folder.
    o_path : str
        Path to the output folder.
    extras_j : str
        Path to the Extra.json file.
    translated_strings : dict
        The translation file contents for this site.
    all_images : dict
        A dictionary mapping image filenames to (width, height) in
        pixels.

    Returns
    -------
    EXpage
        The completed extras page. A :class:`springheel.classes.EXpage`
        object.
    j : dict
        Raw JSON of the extras page.
    """
    with open(extras_j, "r", encoding="utf-8") as json_in:
        try:
            j = json.load(json_in)
        except json.decoder.JSONDecodeError:
            return False, False
    extras = EXpage()
    extra_elements = []
    sorted_j = sorted(j.items())
    copy_queue = []
    for cat, elements in sorted_j:
        extras.headings.append(cat)
        subhead = "<h2>{cat}</h2>".format(cat=cat)
        extra_elements.append(subhead)
        for el in elements:
            title = "<h3>{title}</h3>".format(title=el["title"])
            if el["type"] == "image":
                images = []
                for image in el["files"]:
                    width, height = all_images[image]
                    images.append(
                        """<img src="{image}" alt="" width="{width}" height="{height}">""".format(
                            title=el["title"], image=image, width=width, height=height
                        )
                    )
                    copy_queue.append(
                        {
                            "source": os.path.join(i_path, image),
                            "output": os.path.join(o_path, image),
                        }
                    )
                images = "".join(images)
                el_template = """<figure>{images}<figcaption>{image_s}{desc}</figcaption></figure>""".format(
                    images=images,
                    image_s=translated_strings["image_s"],
                    desc=el["desc"],
                )
            else:
                fils = []
                for fil in el["files"]:
                    inp_file = os.path.join(i_path, fil["path"])
                    bytes_size = os.path.getsize(inp_file)
                    fsize = duH(bytes_size, translated_strings["decimal_separator"])
                    if not os.path.exists(inp_file):
                        logmesg = _(
                            "Error: file {inp} described in Extras.json does not exist."
                        ).format(inp=inp)
                        logging.error(logmesg)
                        return False
                    fbytes = os.path.getsize(inp_file)
                    fils.append(
                        """<li><a href="{path}">{link} [{size}]</a></li>""".format(
                            path=fil["path"], link=fil["link"], size=fsize
                        )
                    )
                    copy_queue.append(
                        {
                            "source": inp_file,
                            "output": os.path.join(o_path, fil["path"]),
                        }
                    )
                fils = "".join(fils)
                el_template = "<p>{desc}</p><ul>{fils}</ul>".format(
                    desc=el["desc"], fils=fils
                )
            elem = "\n".join([title, el_template])
            extra_elements.append(elem)
    extra_combined = "\n".join(extra_elements)
    extras.content = extra_combined
    return extras, j, copy_queue


async def copyExtras(copy_queue: list) -> None:
    """
    Asynchronously copy items for the extras page.

    Parameters
    ----------
    copy_queue : list of dict
        A dictionary indicating the original paths and output paths of
        files to be copied.
    """
    for queued_file in copy_queue:
        await copyfile(queued_file["source"], queued_file["output"])
