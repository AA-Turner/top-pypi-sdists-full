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
"""module for splitting utilities and everything related to it."""


def addJobIndexToFilename(filename, jobIndex):
  """add the jobIndex number to the filename before the extension or replace %n with jobIndex.

  For example::

    'myOutputFile.root' --> 'myOutputFile_123.root'
    'myOutput_%n_File.root' --> 'myOutput_123_File.root'

  :param str filename: the original name of the file
  :param int jobIndex: the jobIndex number
  :returns: new filename with jobIndex
  """
  if '%n' in filename:
    filename = filename.replace('%n', str(jobIndex))
    return filename

  fileParts = filename.rsplit('.', 1)
  if len(fileParts) == 2:
    filename = "%s_%d.%s" % (fileParts[0], jobIndex, fileParts[1])
    return filename

  filename = "%s_%d" % (filename, jobIndex)
  return filename
