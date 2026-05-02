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

"""Process comics in webtoon mode."""

import typing
from springheel.classes import Strip
import springheel.renameimgs


def webtoon(
    strip: Strip, pieces: typing.List[dict], images: dict, translated_strings: dict
) -> typing.List[str]:
    """
    Create a webtoon-style image block.

    Parameters
    ----------
    strip : Strip
        The "individual strip" from a metadata perspective.
    pieces : list of dict
        The images to use and various data about them.
    images : dict
        A dictionary mapping image filenames to (width, height) in
        pixels.
    translated_strings : dict
        The translation file contents for this site.

    Returns
    -------
    list of str
        A list of HTML image elements.
    """
    imgpatt = (
        """<img src="{img_path}" alt="{page_alt}" width="{width}" height="{height}">"""
    )
    w, h = images[strip.imagef]
    first_img = imgpatt.format(
        img_path="".join(["pages/", strip.img]),
        page_alt=translated_strings["page_alt_s"],
        width=w,
        height=h,
    )
    imgs = [first_img]
    mode = strip.mode
    for piece in pieces:
        piece_img = piece["img"]
        w, h = images[piece_img]
        imgs.append(
            imgpatt.format(img_path=piece["prn_path"], page_alt="", width=w, height=h)
        )
    return imgs
