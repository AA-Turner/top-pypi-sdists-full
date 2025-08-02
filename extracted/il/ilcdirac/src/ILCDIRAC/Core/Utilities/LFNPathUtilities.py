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
"""Utilities to deal with the normalisation of LFNs for various occasions.

:author: sailer
"""

from __future__ import absolute_import
__RCSID__ = "$Id$"

# use posixpath because it always uses "/"
import posixpath
from DIRAC import gLogger

LOG = gLogger.getSubLogger(__name__)


def joinPathForMetaData(*args):
  """Returns path expected by MetaDataDictionaries, always ends with a slash When paths are used for metadata, the ending "/" will be rstripped."""
  # if there is a lone slash in this list then the end result is only "/" so we remove them
  cleanedEntries = tuple(ent for ent in args if ent != "/")
  LOG.debug("After cleaning", cleanedEntries)
  finalPath = ""
  for entry in cleanedEntries:
    LOG.debug("This entry", entry)
    finalPath = posixpath.join(finalPath, entry)
  LOG.debug("After Joining", finalPath)
  finalPath = posixpath.normpath(finalPath)
  LOG.debug("After norming", finalPath)
  finalPath = finalPath + "/"
  LOG.verbose("Final Path ", finalPath)
  return finalPath


def cleanUpLFNPath(lfn):
  """Normalise LFNs and remove 'LFN:' prefix."""
  LOG.debug("LFN before Cleanup", lfn)
  lfn = posixpath.normpath(lfn)
  if lfn.lower().startswith('lfn'):
    LOG.debug("LFN starts with lfn:'")
    lfn = lfn[4:]
  LOG.verbose("LFN after Cleanup", lfn)
  return lfn
