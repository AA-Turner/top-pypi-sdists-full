#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Add Image
########
##  Copyright 2017-2021 garrick. Some rights reserved.
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

"""Add a new strip to Springheel's input."""

import os, sys, re, datetime, configparser, glob, json, argparse, typing
import springheel.parseconf
from PIL import Image


def getInfo() -> typing.Tuple[str, dict, bool]:
    """
    Retrieve info from a .conf file and command line input.

    Notes
    -----
    Fields that are not provided by the command-line invocation of
    ``springheel-addimg`` will be requested with ``input()``. If non-
    optional fields are still left empty, they default to
    "<Missing Field>" to call attention to this fact.

    Returns
    -------
    meta_path : str
        Output path for the metadata file.
    meta_dict : str
        A dictionary with image metadata.
    json_mode : bool
        Whether the output should be in JSON format or not.
    """
    falses = {False, "False", None, "None", ""}
    input_dir = os.path.abspath(os.path.join(os.getcwd(), "input"))
    commands = parseCommandInput()
    filename = (
        input(_("Comic's filename? > ")) if not commands.input else commands.input
    )
    file_path = os.path.abspath(commands.input)
    fn_noext = os.path.splitext(file_path)[0]
    if commands.json:
        json_mode = True
        meta_ext = ".meta.json"
    else:
        json_mode = input("JSON mode? y/N > ").lower() == "y"
        if json_mode:
            meta_ext = ".meta.json"
        else:
            meta_ext = ".meta"
    meta_name = "".join([fn_noext, meta_ext])
    meta_path = os.path.join(input_dir, meta_name)
    if not commands.conf:
        confs = checkConfs(input_dir)
        conf_fn = input(_(".conf file? > "))
        conf_path = os.path.join(input_dir, conf_fn)
    else:
        conf_fn = os.path.basename(commands.conf)
        conf_path = commands.conf
    conf = springheel.parseconf.comicCParse(conf_path)
    date = False
    alt = False
    title = input(_("Title? > ")) if not commands.title else commands.title
    page = input(_("Page number? > ")) if not commands.num else commands.num
    if conf["chapters"] not in falses:
        chapter = input("Chapter? > ") if not commands.chapter else commands.chapter
    else:
        chapter = ""
    alt = (
        input(_("Alt text? (Press Enter to skip) > "))
        if not commands.alt
        else commands.alt
    )
    source = (
        input(_("Source URL? (Press Enter to skip) > "))
        if not commands.source
        else commands.source
    )
    commentary = (
        input(_("Commentary? > ")) if not commands.commentary else commands.commentary
    )
    try:
        with Image.open(file_path) as im:
            width, height = im.size
    except NameError:
        width, height = ("", "")
    category = conf["category"]
    author = conf["author"]
    email = conf["email"]
    if not date:
        mtime_raw = os.path.getmtime(file_path)
        mtime_dt = datetime.datetime.fromtimestamp(mtime_raw)
        try:
            date = re.search("(\d{4}-\d+-\d+)", filename).group(0)
        except AttributeError:
            date = datetime.datetime.strftime(mtime_dt, "%Y-%m-%d")
    lang = conf["language"]
    meta_dict = {
        "title": title,
        "author": author,
        "email": email,
        "date": date,
        "conf": conf_fn,
        "category": category,
        "page": page,
        "height": height,
        "width": width,
        "language": lang,
        "mode": conf["mode"],
        "commentary": commentary,
    }
    for key, value in meta_dict.items():
        if not value:
            meta_dict.update({key: "<Missing Field>"})
    # don't add empty fields
    for key, value in {"chapter": chapter, "alt": alt, "source": source}.items():
        if value not in falses:
            meta_dict[key] = value
    return meta_path, meta_dict, json_mode


def checkConfs(input_dir: str) -> typing.List[str]:
    """
    Check which .conf files exist in input.

    Parameters
    ----------
    input_dir : str
        Absolute path of the input/ directory.

    Returns
    -------
    list of str
        A list of config files.
    """
    globpatt = os.path.join(input_dir, "*.conf")
    confs = glob.glob(globpatt)
    print(
        _("Comic config files in input: {confs}").format(
            confs=",".join([os.path.basename(item) for item in confs])
        )
    )
    return confs


def parseCommandInput() -> argparse.Namespace:
    """
    Read info on the strip from the command line.

    Returns
    -------
    argparse.Namespace
        Arguments provided by the user, if any. Should contain values
        (including None) for input, conf, title, num, chapter, alt,
        source, json, and commentary.
    """
    parser = argparse.ArgumentParser(prog="springheel-addimg")
    parser.add_argument(
        "-i",
        "--input",
        help=_("The strip's image filename"),
    )
    parser.add_argument(
        "-c",
        "--conf",
        help=_("The category .conf file to use"),
    )
    parser.add_argument(
        "-t",
        "--title",
        help=_("The strip's title"),
    )
    parser.add_argument(
        "-n",
        "--num",
        help=_("The strip's page number"),
    )
    parser.add_argument(
        "-k",
        "--chapter",
        help=_("The strip's chapter number"),
    )
    parser.add_argument(
        "-a",
        "--alt",
        help=_("The strip's extra text"),
    )
    parser.add_argument(
        "-s",
        "--source",
        help=_("The strip's source URL"),
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help=_("Enable JSON output mode"),
    )
    parser.add_argument(
        "--commentary",
        help=_("Commentary on the strip"),
    )
    choice = parser.parse_args()
    return choice


def formatOutput(meta_dict, json_mode, output_file):
    """
    Save metadata to a file.

    Parameters
    ----------
    meta_dict : dict
        Dictionary of all needed metadata for the strip.
    json_mode : bool
        Whether to save the metadata as JSON or not.
    output_file : str
        The output filename to use.
    """
    if json_mode:
        j = {"metadata": meta_dict}
        j["metadata"]["commentary"] = meta_dict["commentary"].splitlines()
        with open(output_file, "w", encoding="utf-8") as fout:
            json.dump(j, fout)
    else:
        lines = ["---"]
        for key, value in meta_dict.items():
            if key == "commentary":
                break
            lines.append(f"  {str(key)}: {value}")
        lines.append("---")
        lines.extend(meta_dict["commentary"].splitlines())
        lines.append("---")
        meta_template = "\n".join(lines)
        with open(output_file, "w", encoding="utf-8") as fout:
            fout.write(meta_template)


def addImg():
    """Add an image as a Springheel comic with metadata."""
    meta_path, meta_dict, json_mode = getInfo()
    formatOutput(meta_dict, json_mode, meta_path)
    print(_(f"Wrote {os.path.relpath(meta_path)}. Please create a transcript file."))
