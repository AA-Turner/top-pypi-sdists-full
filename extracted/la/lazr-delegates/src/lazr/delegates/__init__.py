# Copyright 2008-2015 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.delegates.
#
# lazr.delegates is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.delegates is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.delegates.  If not, see <http://www.gnu.org/licenses/>.

"""Decorator helpers that simplify class composition."""

__all__ = [
    'Passthrough',
    'delegate_to',
    ]

try:
    import importlib.metadata as importlib_metadata
except ImportError:  # pragma: no cover
    import importlib_metadata

from lazr.delegates._delegates import (
    Passthrough,
    delegate_to,
    )

__version__ = importlib_metadata.version("lazr.delegates")
