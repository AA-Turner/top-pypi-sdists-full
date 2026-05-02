#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
author: inklov3
date: 2025-07-16
description: 导出工具类
"""

from dataclasses import dataclass, field


@dataclass
class LabelMeLabel:
    """
    LabelMe标签
    """

    name: str
    shape: str
    group_id: int


@dataclass
class LabelMeFrame:
    """
    LabelMe帧
    """

    imagePath: str
    imageData: str | None = field(default=None)
