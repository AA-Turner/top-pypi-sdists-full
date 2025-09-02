#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import Annotated

from typer import Option

JsonOption = Annotated[bool, Option("--json", help="Render output as JSON.")]
LimitOption = Annotated[
    int, Option("--limit", "-l", help="Limit the number of results.", min=1)
]
