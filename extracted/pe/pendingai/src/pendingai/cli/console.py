#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import Any

from rich.console import Console as BaseConsole
from rich.theme import Theme


class Console(BaseConsole):
    """
    `rich` console singleton with shared config options.
    """

    _styles: dict = {
        "warn": "yellow not bold",
        "success": "green not bold",
        "fail": "red bold",
        "link": "blue bold underline",
    }

    def __init__(self, *args: Any, **kwargs: Any):
        kwargs["theme"] = Theme(styles=self._styles, inherit=True)
        # kwargs["width"] = 88
        super().__init__(*args, **kwargs)
