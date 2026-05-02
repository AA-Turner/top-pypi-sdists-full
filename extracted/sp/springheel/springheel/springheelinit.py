#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Project Initialization
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

"""Initialize a Springheel site."""

import sys, os, shutil, asyncio, logging
import springheel.acopy
from distutils import dir_util
from typing import Tuple
from springheel.tl import gettext as _

copyfile = springheel.acopy.wrap(shutil.copyfile)
copy_tree = springheel.acopy.wrap(dir_util.copy_tree)


def initDir(output_path: str, dir_name: str) -> str:
    """
    Create a subdirectory in the output if it doesn't already exist.

    Parameters
    ----------
    output_path : str
        Path to the output folder.
    dir_name : str
        The name of the directory to create.

    Returns
    -------
    str
        Path to the (new) directory.
    """
    dir_path = os.path.join(output_path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path, mode=0o755)
        os.chmod(dir_path, mode=0o755)
    return dir_path


def makeOutput() -> Tuple[str, str, str, str, str, str]:
    """
    Create an output directory if it doesn't already exist.

    Returns
    -------
    c_path : str
        Current (root) path.
    output_path : str
        Path to the output directory.
    pages_path : str
        Path to the pages directory in output.
    assets_path : str
        Path to the assets directory in output.
    arrows_path : str
        Path to the navigation arrow directory in output.
    socialbuttons_path : str
        Path to the social media icon directory in output.
    """
    if not os.path.exists("output"):
        os.mkdir("output", mode=0o755)
        os.chmod("output", mode=0o755)
    c_path = os.path.abspath(".")
    output_path = os.path.abspath("output")

    pages_path = initDir(output_path, "pages")
    assets_path = initDir(output_path, "assets")
    arrows_path = initDir(output_path, "arrows")
    socialbuttons_path = initDir(output_path, "socialbuttons")
    templates_path = initDir(c_path, "templates")
    input_path = initDir(c_path, "input")

    return (
        c_path,
        output_path,
        pages_path,
        assets_path,
        arrows_path,
        socialbuttons_path,
    )


def getTemplatesPath() -> Tuple[str, str]:
    """
    Find the install directory of Springheel and its templates.

    Returns
    -------
    raw_springheel_path : str
        The directory in which Springheel is installed.
    templates_path : str
        The path to the Springheel installation's templates.
    """
    try:
        raw_springheel_path = sys.modules["springheel"].__path__[0]
        logging.info(
            _("Springheel directory found at {path}...").format(
                path=raw_springheel_path
            )
        )
    except KeyError:
        logging.error(
            _(
                "Could not initialize because the Springheel directory was not found, somehow. I have no idea how you are running this at all. File an issue with the full details, but I may take some time to get back to you."
            )
        )
        return False
    ## From there, find the path where templates are stored.
    templates_path = os.path.join(raw_springheel_path, "templates")
    return (raw_springheel_path, templates_path)


async def copyAssets() -> str:
    """
    Copy assets from Springheel's install directory to the current one.

    Returns
    -------
    str
        The path to templates in Springheel's install directory.
    """
    raw_springheel_path, templates_path = getTemplatesPath()
    strings_path = os.path.join(templates_path, "strings.json")
    logging.info(
        _("Getting templates from {templates_path}...").format(
            templates_path=templates_path
        )
    )
    if not os.path.exists(templates_path):
        logging.error(
            _(
                "The Springheel module was found, but template files do not exist. Please make sure {templates_path} exists and try again."
            ).format(templates_path=templates_path)
        )
        return False
    current_dir = os.getcwd()

    templates_o = os.path.join(current_dir, "templates")

    logging.info(
        _("Copying templates and translation strings to {templates_output}...").format(
            templates_output=templates_o
        )
    )
    await copy_tree(templates_path, templates_o)

    # input
    input_path = initDir(current_dir, "input")

    # conf.ini
    o_conf = os.path.join(raw_springheel_path, "conf.ini")
    n_conf = os.path.join(current_dir, "conf.ini")
    if not os.path.exists(n_conf):
        try:
            confpy_path = shutil.copy(o_conf, n_conf)
            logging.info(_("Created conf.ini."))
        except FileNotFoundError:
            logging.error(
                _(
                    "Couldn't find conf.ini in the Springheel install directory. Did you delete it somehow?"
                )
            )
    else:
        logging.info(_("conf.ini already exists in output directory; not overwriting."))

    # arrows
    base_arrows_path = os.path.join(raw_springheel_path, "arrows")
    arrows_path = initDir(current_dir, "arrows")

    # themes
    base_themes_path = os.path.join(raw_springheel_path, "themes")
    themes_path = initDir(current_dir, "themes")

    # social buttons
    base_socialbuttons_path = os.path.join(raw_springheel_path, "socialbuttons")
    socialbuttons_path = initDir(current_dir, "socialbuttons")

    await copy_tree(base_arrows_path, arrows_path)
    logging.info(_("Copied arrows..."))
    await copy_tree(base_themes_path, themes_path)
    logging.info(_("Copied themes..."))
    await copy_tree(base_socialbuttons_path, socialbuttons_path)
    logging.info(_("Copied social buttons..."))

    # I have reasons! Now we shall see!
    logging.info(_("Springheel initialized. Have fun! ^_^"))
    return templates_path
