#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Asset Copying
########
##  Copyright 2017–2021 garrick. Some rights reserved.
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

import shutil, os, logging, glob
from distutils import dir_util
import springheel.socialbuttons
import springheel.acopy
from typing import List
from springheel.tl import gettext as _

copyfile = springheel.acopy.wrap(shutil.copyfile)
copy_tree = springheel.acopy.wrap(dir_util.copy_tree)


async def copyTheme(site_theme_path: str, new_site_theme_path: str, print_ipath: str):
    """
    Copy theme assets to the output folder.

    Parameters
    ----------
    site_theme_path : str
        The source directory for theme assets.
    new_site_theme_path : str
        The location in output/ whither the theme will be copied.
    print_ipath : str
        Path to the print.css stylesheet.
    """
    logging.debug(_("Copying theme..."))
    files = os.listdir(site_theme_path)
    files.append(print_ipath)
    logging.debug(", ".join([os.path.relpath(file) for file in files]))

    for i in files:
        source_path = os.path.join(site_theme_path, i)
        new_path = os.path.join(new_site_theme_path, os.path.basename(i))
        if not os.path.exists(new_path):
            await copyfile(source_path, new_path)
            logmesg = _("Copied theme to {new_path}").format(new_path=new_path)
            logging.debug(logmesg)
        else:
            logmesg = _(
                "{i} already exists in the output. To overwrite, remove the existing file from output."
            ).format(i=i)
            logging.debug(logmesg)


async def copyButtons(
    site: springheel.classes.Site,
    old_buttons_path: str,
    socialbuttons_path: str,
    translated_strings: dict,
):
    """
    Copy buttons to the output folder.

    Parameters
    ----------
    site : springheel.classes.Site
        The comic :class:`Site`. Buttons from this site will be copied.
    old_buttons_path : str
        The source directory for social buttons.
    socialbuttons_path : str
        The location in output/ whither the buttons will be copied.
    translated_strings : dict
        The translation file contents for this site.
    """
    try:
        files = os.listdir(old_buttons_path)
    except FileNotFoundError:
        logmesg = _("socialbuttons directory not found!")
        logging.error(logmesg)
        return False

    logmesg = _("Social icons: {icons}").format(icons=site.config.social_icons)
    logging.debug(logmesg)
    social_links = springheel.socialbuttons.getButtons(site, translated_strings)[0]
    images_to_copy = [item["image"] for item in social_links]

    for item in images_to_copy:
        source_path = os.path.join(old_buttons_path, item)
        out_path = os.path.join(socialbuttons_path, item)
        try:
            await copyfile(source_path, out_path)
        except FileNotFoundError:
            logmesg = _("Unable to copy {item} from socialbuttons to output.").format(
                item=item
            )
            logging.error(logmesg)
            return False

    logmesg = _("Copied feed/social buttons to {socialbuttons_path}").format(
        socialbuttons_path=socialbuttons_path
    )
    logging.debug(logmesg)


async def copyArrows(theme: str, old_arrows_path: str, new_arrows_path: str):
    """
    Copy navigation arrows to the output folder.

    Parameters
    ----------
    theme : str
        The name of a site theme. Arrows with this prefix will be
        copied.
    old_arrows_path : str
        The source directory for arrows.
    new_arrows_path : str
        The location in output/ whither the arrows will be copied.
    """
    arrtemplate = "{theme}_{dir}.png"
    needed_dirs = {"first", "prev", "next", "last"}
    needed_arrows = {arrtemplate.format(theme=theme, dir=item) for item in needed_dirs}

    logging.debug(_("Copying {theme} arrows...").format(theme=theme))
    for arrow in needed_arrows:
        old_arrow_path = os.path.join(old_arrows_path, arrow)
        new_arrow_path = os.path.join(new_arrows_path, arrow)
        try:
            if not os.path.exists(new_arrow_path):
                await copyfile(old_arrow_path, new_arrow_path)
            else:
                logmesg = _("Not overwriting {theme} arrows in output.").format(
                    theme=theme
                )
                logging.debug(logmesg)
        except FileNotFoundError:
            logmesg = _(
                "{old_arrow_path} not found in the currently-set style {theme}."
            ).format(old_arrow_path=old_arrow_path, theme=theme)
            logging.error(logmesg)
            return False
    logging.debug(_("{theme} arrows complete.").format(theme=theme))


async def copyHeader(old_header_path: str, new_header_path: str):
    """
    Copy a header/banner image to the output folder.

    Parameters
    ----------
    old_header_path : str
        The source directory for the image.
    new_header_path : str
        The location in output/ whither the header will be copied.
    """
    await copyfile(old_header_path, new_header_path)
    logmesg = _("Header copied to {path}.").format(path=new_header_path)
    logging.debug(logmesg)


async def copyMultiThemes(
    themes: List[str], c_path: str, o_path: str, assets_path: str
):
    """
    Concatenate themes into one stylesheet in the output folder.

    Parameters
    ----------
    themes : list of str
        The names of themes to use.
    c_path : str
        The current directory.
    o_path : str
        The path to the output directory (i.e. output/).
    assets_path : str
        The path to the assets directory in output. Usually "assets".
    """
    theme_path = os.path.join(c_path, "themes")
    new_theme_path = os.path.join(o_path, assets_path)
    theme_ds = []

    for theme in themes:
        t_path = os.path.join(theme_path, theme)
        files = os.listdir(t_path)
        sheet = os.path.join(t_path, "style.css")
        with open(sheet, "r", encoding="utf-8") as f:
            sheet_contents = f.read()

        theme_ds.append(
            {
                "theme": theme,
                "o_path": t_path,
                "files": files,
                "sheet": sheet,
                "sheet_contents": sheet_contents,
            }
        )

    style = ['@charset "utf-8";'] + [
        item["sheet_contents"]
        .replace('@charset "UTF-8";', "")
        .replace('@charset "utf-8";', "")
        for item in theme_ds
    ]
    knownfiles = set()

    for d in theme_ds:
        for i in d["files"]:
            source_dir = d["o_path"]
            source_path = os.path.join(source_dir, i)
            new_path = os.path.join(new_theme_path, i)
            if not os.path.exists(new_path) and i not in knownfiles:
                await copyfile(source_path, new_path)
                knownfiles.add(i)
                logmesg = _("{source_path} copied to {new_path}").format(
                    source_path=source_path, new_path=new_path
                )
                logging.debug(logmesg)
            else:
                if i not in knownfiles:
                    logmesg = _(
                        "{i} already exists in the output. To overwrite, remove the existing file from output."
                    ).format(i=i)
                    logging.debug(logmesg)
                    knownfiles.add(i)

    cstyle = "".join(style)
    new_style_path = os.path.join(new_theme_path, "style.css")
    with open(new_style_path, "w+") as fout:
        fout.write(cstyle)
    logmesg = _("Concatenated stylesheet written.")
    logging.debug(logmesg)
