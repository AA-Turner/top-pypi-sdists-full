#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: EPL-1.0
##############################################################################
# Copyright (c) 2017-2018 The Linux Foundation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
##############################################################################
"""Configuration for Sphinx."""

import os
import sys

# Sys.path for RTD to resolve docs_conf package
sys.path.insert(0, os.path.abspath(".."))

from pbr.version import VersionInfo  # noqa

from docs_conf.conf import *  # noqa

version = str(VersionInfo("lfdocs-conf"))
release = str(VersionInfo("lfdocs-conf"))

linkcheck_ignore = [
    # The '#' in the path makes sphinx think it's an anchor
    "https://gerrit.linuxfoundation.org/infra/#/admin/projects/releng/docs-conf"
]
