#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re

SMILES_PATTERN: re.Pattern[str] = re.compile(
    r"^[A-Za-z0-9\(\)+-=#%+@\/\\\[\]\*]{1,10000}$", re.ASCII
)


BATCH_ID_PATTERN: re.Pattern[str] = re.compile(r"^bat_[a-zA-Z0-9]+$")

JWT_PATTERN: re.Pattern[str] = re.compile(r"^[\w-]+\.[\w-]+\.[\w-]+$", re.ASCII)
JOB_ID_PATTERN: re.Pattern[str] = re.compile(r"[a-f\d]{24}")
