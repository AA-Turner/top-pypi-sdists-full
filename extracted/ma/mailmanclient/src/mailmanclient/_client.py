# Copyright (C) 2017-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailmanclient.
#
# mailman.client is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailman.client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.

"""Old module for backwards compatibility"""

from __future__ import absolute_import, print_function, unicode_literals

from mailmanclient import *                                      # noqa

__metaclass__ = type

# XXX: This module exists for backwards compatibility with older versions of
# MailmanClient which had all the API under this module. It will be removed in
# future after few cycles of deprecation.
