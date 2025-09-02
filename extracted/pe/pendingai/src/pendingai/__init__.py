#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import enum


@enum.unique
class Environment(str, enum.Enum):
    """
    Deployment environment used for building client connection strings,
    authentication flows for the device or refresh tokens, and controls
    cached state data between different environments
    """

    DEV = "dev"
    STAGING = "stage"
    DEFAULT = "default"
