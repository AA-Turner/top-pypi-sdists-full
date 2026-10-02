#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import (
    absolute_import,
    division,
    generators,
    nested_scopes,
    print_function,
    unicode_literals,
    with_statement,
)

from .middleware import get_request
from .middleware import GlobalRequest
from .middleware import GlobalRequestStorage

app_middleware_requires = [
    "django_middleware_global_request.middleware.GlobalRequestMiddleware",
]
