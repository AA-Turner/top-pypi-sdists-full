#
# This software is part of the DenodoConnect component collection.
#
# Copyright (c) 2025 Denodo Technologies (https://www.denodo.com)
#
# This module is based on SQLAlchemy's dialect for PostgreSQL:
#
# Copyright (C) 2005-2025 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from sqlalchemy.sql import operators


_eq_precedence = operators._PRECEDENCE[operators.eq]

HAS_ALL = operators.custom_op(
    "?&",
    precedence=_eq_precedence,
    natural_self_precedent=True,
    eager_grouping=True,
    is_comparison=True,
)

HAS_ANY = operators.custom_op(
    "?|",
    precedence=_eq_precedence,
    natural_self_precedent=True,
    eager_grouping=True,
    is_comparison=True,
)

PATH_EXISTS = operators.custom_op(
    "@?",
    precedence=_eq_precedence,
    natural_self_precedent=True,
    eager_grouping=True,
    is_comparison=True,
)

PATH_MATCH = operators.custom_op(
    "@@",
    precedence=_eq_precedence,
    natural_self_precedent=True,
    eager_grouping=True,
    is_comparison=True,
)

# ARRAY
CONTAINS = operators.custom_op(
    "@>",
    precedence=_eq_precedence,
    natural_self_precedent=True,
    eager_grouping=True,
    is_comparison=True,
)

CONTAINED_BY = operators.custom_op(
    "<@",
    precedence=_eq_precedence,
    natural_self_precedent=True,
    eager_grouping=True,
    is_comparison=True,
)

# ARRAY
OVERLAP = operators.custom_op(
    "&&",
    precedence=_eq_precedence,
    is_comparison=True,
)
