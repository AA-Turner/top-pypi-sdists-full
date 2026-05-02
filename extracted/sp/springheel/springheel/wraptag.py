#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017–2021 garrick. Some rights reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


def wrapWithTag(s: str, tag: str) -> str:
    """
    Wrap a string in an HTML tag.

    Parameters
    ----------
    s : str
        The string to wrap.
    tag : str
        The HTML tag to wrap the string in.

    Returns
    -------
    str
        The string wrapped in the tag.
    """
    wrapped = "<{tag}>{s}</{tag}>".format(tag=tag, s=s)
    return wrapped


def wrapWithComment(s: str, comment: str) -> str:
    """
    Wrap a string in an HTML comment.

    Notes
    -----
    Mostly just makes it easier to debug problems in templates. It
    marks up the various sections of the output.

    Parameters
    ----------
    s : str
        The string to wrap.
    comment : str
        The HTML comment to use.

    Returns
    -------
    str
        The string wrapped in the comment.
    """
    wrapped = "<!--{comment}-->{s}<!--END {comment}-->".format(comment=comment, s=s)
    return wrapped
