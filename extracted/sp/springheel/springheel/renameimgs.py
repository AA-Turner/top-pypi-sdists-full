#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Webtoon Mode
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

"""Get renamed images."""

import os, typing
from springheel.classes import *


def renameImages(
    site: Site,
    strip: Strip,
    pages_path: str,
    m_ext: str,
    t_ext: str,
    image_rename_pattern: str,
) -> typing.Tuple[str, str, str, str]:
    """
    Rename images and related data files as necessary.

    Parameters
    ----------
    site : Site
        The Site this strip belongs to. Needed for config values.
    strip : Strip
        The Strip to process.
    pages_path : str
        Path to the pages/ directory in output/.
    m_ext : str
        The file extension for metadata files.
    t_ext : str
        The file extension for transcript files.
    image_rename_pattern : str
        The pattern to use for image renaming.

    Returns
    -------
    renamed_fn : str
        The new image filename.
    renamed_path : str
        The path to the renamed image in output.
    new_meta : str
        The new metadata filename.
    new_transcr : str
        The new transcript filename.
    """
    if site.config.rename_images:
        renamed_fn = image_rename_pattern.format(
            comic=strip.series_slug,
            page=strip.page_padded,
            chapter=strip.chapter,
            height=strip.height,
            width=strip.width,
            titleslug=strip.title_slug,
            date=strip.date_s,
            ext=os.path.splitext(strip.imagef)[1][1:],
        )
        new_meta = image_rename_pattern.format(
            comic=strip.series_slug,
            page=strip.page_padded,
            chapter=strip.chapter,
            height=strip.height,
            width=strip.width,
            titleslug=strip.title_slug,
            date=strip.date_s,
            ext=m_ext,
        )
        new_transcr = image_rename_pattern.format(
            comic=strip.series_slug,
            page=strip.page_padded,
            chapter=strip.chapter,
            height=strip.height,
            width=strip.width,
            titleslug=strip.title_slug,
            date=strip.date_s,
            ext=t_ext,
        )
    else:
        renamed_fn = strip.imagef
        new_meta = strip.metaf
        new_transcr = strip.transf
    renamed_path = os.path.join(pages_path, renamed_fn)
    return renamed_fn, renamed_path, new_meta, new_transcr


def renamePieces(
    site: Site,
    strip: Strip,
    pid: int,
    piece: str,
    pages_path: str,
    image_rename_pattern: str,
    images: dict,
) -> typing.Tuple[str, str]:
    """
    File renaming for pieces of webtoon-style comics.

    Parameters
    ----------
    site : Site
        The Site this strip belongs to. Needed for config values.
    strip : Strip
        The "individual strip" from a metadata perspective.
    pid : int
        The current piece's position within the total strip.
    piece : str
        The filename of the piece to process.
    pages_path : str
        Path to the pages/ directory in output/.
    image_rename_pattern : str
        The pattern to use for image renaming.
    images : dict
        A dictionary mapping image filenames to (width, height) in
        pixels.

    Returns
    -------
    renamed_fn : str
        The new image filename.
    renamed_path : str
        The path to the renamed image in output.
    """
    if site.config.rename_images:
        width, height = images[piece]
        renamed_fn = image_rename_pattern.format(
            comic=strip.series_slug,
            page="_".join([strip.page_padded, str(pid + 1)]),
            chapter=strip.chapter,
            height=strip.height,
            width=strip.width,
            titleslug=strip.title_slug,
            date=strip.date_s,
            ext=os.path.splitext(piece)[1][1:],
        )
        renamed_path = os.path.join(pages_path, renamed_fn)
    else:
        renamed_fn = piece
    renamed_path = os.path.join(pages_path, renamed_fn)
    return renamed_fn, renamed_path
