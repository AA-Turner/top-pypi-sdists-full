#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

import trafaret as t

from datarobot.models.api_object import APIObject

notebook_settings_trafaret = t.Dict(
    {
        t.Key("show_line_numbers"): t.Bool,
        t.Key("hide_cell_titles"): t.Bool,
        t.Key("hide_cell_outputs"): t.Bool,
        t.Key("show_scrollers"): t.Bool,
        t.Key("hide_cell_footers"): t.Bool,
        t.Key("highlight_whitespace"): t.Bool,
    }
).ignore_extra("*")


class NotebookSettings(APIObject):
    """
    Settings for a DataRobot Notebook.

    Attributes
    ----------

    show_line_numbers : bool
        Whether line numbers in cells should be displayed.
    hide_cell_titles : bool
        Whether cell titles should be displayed.
    hide_cell_outputs : bool
        Whether the cell outputs should be displayed.
    show_scrollers : bool
        Whether scroll bars should be shown on cells.
    hide_cell_footers : bool
        Whether footers should be shown on cells.
    highlight_whitespace : bool
        Whether whitespace should be highlighted or not.
    """

    _converter = notebook_settings_trafaret

    def __init__(
        self,
        show_line_numbers: bool,
        hide_cell_titles: bool,
        hide_cell_outputs: bool,
        show_scrollers: bool,
        hide_cell_footers: bool,
        highlight_whitespace: bool,
    ):
        self.show_line_numbers = show_line_numbers
        self.hide_cell_titles = hide_cell_titles
        self.hide_cell_outputs = hide_cell_outputs
        self.show_scrollers = show_scrollers
        self.hide_cell_footers = hide_cell_footers
        self.highlight_whitespace = highlight_whitespace
