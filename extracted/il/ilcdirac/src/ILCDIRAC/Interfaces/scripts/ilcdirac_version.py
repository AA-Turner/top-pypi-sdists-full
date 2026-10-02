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
"""Print version of current iLCDirac installation.

Mandatory when submitting support requests

.. seealso::

  :ref:`dirac-version`, :ref:`dirac-info` and how
  to submit a :ref:`support-request`.

.. versionadded:: 23.0

:author: A. Sailer
"""

from __future__ import print_function
from __future__ import absolute_import
import pprint
import os

import DIRAC
from DIRAC import gConfig
from DIRAC.Core.Base.Script import Script
from DIRAC.Core.Security.ProxyInfo import getProxyInfo
from DIRAC.ConfigurationSystem.Client.Helpers.Registry import getVOForGroup
from DIRAC.Core.Utilities.PrettyPrint import printTable

import ILCDIRAC

__RCSID__ = "$Id$"


@Script()
def main():
  """Print the ILCDIRAC and DIRAC versions and other information."""
  fields, records = getInfo()
  records.insert(0, ("ILCDirac Version:", ILCDIRAC.version))
  records.insert(1, ("DIRAC version:", DIRAC.version))

  printTable(fields, records, numbering=False)


def getInfo():
  """Retrieve information about setup, etc."""
  records = []

  records.append(('Setup', gConfig.getValue('/DIRAC/Setup', 'Unknown')))
  records.append(('ConfigurationServer', gConfig.getValue('/DIRAC/Configuration/Servers', [])))
  records.append(('Installation path', DIRAC.rootPath))

  if os.path.exists(os.path.join(DIRAC.rootPath, DIRAC.getPlatform(), 'bin', 'mysql')):
    records.append(('Installation type', 'server'))
  else:
    records.append(('Installation type', 'client'))

  records.append(('Platform', DIRAC.getPlatform()))

  ret = getProxyInfo(disableVOMS=False)
  if ret['OK']:
    print(pprint.pformat(ret))
    if 'group' in ret['Value']:
      vo = getVOForGroup(ret['Value']['group'])
    else:
      vo = getVOForGroup('')
    if not vo:
      vo = "None"
    records.append(('VirtualOrganization', vo))
    if 'identity' in ret['Value']:
      records.append(('User DN', ret['Value']['identity']))
    if 'secondsLeft' in ret['Value']:
      records.append(('Proxy validity, secs', {'Value': str(ret['Value']['secondsLeft']), 'Just': 'L'}))

  if gConfig.getValue('/DIRAC/Security/UseServerCertificate', True):
    records.append(('Use Server Certificate', 'Yes'))
  else:
    records.append(('Use Server Certificate', 'No'))
  if gConfig.getValue('/DIRAC/Security/SkipCAChecks', False):
    records.append(('Skip CA Checks', 'Yes'))
  else:
    records.append(('Skip CA Checks', 'No'))

  try:
    import gfalthr  # pylint: disable=import-error
    records.append(('gfal version', gfalthr.gfal_version()))
  except BaseException:
    pass

  fields = ['Option', 'Value']

  return fields, records


if __name__ == "__main__":
  main()
