#
# Copyright (c) 2009-2022 CERN. All rights nots expressly granted are
# reserved.
#
# This file is part of iLCDirac
# (see ilcdirac.cern.ch, contact: ilcdirac-support@cern.ch).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# In applying this licence, CERN does not waive the privileges and
# immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""ILCDIRAC package, implements ILC/CLIC production and application specific stuff."""
from __future__ import absolute_import
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import six

__RCSID__ = "$Id$"

# pylint: disable=invalid-name

# Define Version
if six.PY3:
  from pkg_resources import get_distribution, DistributionNotFound

  try:
    __version__ = get_distribution(__name__).version
    version = __version__
  except DistributionNotFound:
    # package is not installed
    version = "Unknown"
else:
  majorVersion = 32
  minorVersion = 0
  patchLevel = 0
  preVersion = 0

  version = "v%sr%s" % (majorVersion, minorVersion)
  buildVersion = "v%dr%d" % (majorVersion, minorVersion)
  if patchLevel:
    version = "%sp%s" % (version, patchLevel)
    buildVersion = "%s build %s" % (buildVersion, patchLevel)
  if preVersion:
    version = "%s-pre%s" % (version, preVersion)
    buildVersion = "%s pre %s" % (buildVersion, preVersion)


def extension_metadata():
  """Extension metadata for ILCDIRAC bootstrap."""
  return {
      "primary_extension": True,
      "priority": 100,
      "setups": {
          "ILC-Production": "dips://voilcdiracconfig.cern.ch:9135/Configuration/Server",
          "ILC-Certification": "dips://voilcdiracconfig.cern.ch:9135/Configuration/Server",
          },
      "default_setup": "ILC-Production",
      }
