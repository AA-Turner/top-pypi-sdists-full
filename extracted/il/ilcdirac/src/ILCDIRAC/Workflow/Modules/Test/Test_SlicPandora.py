#!/usr/bin/env python
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
"""Test user jobfinalization."""
from __future__ import print_function
from __future__ import absolute_import
__RCSID__ = "$Id$"

import unittest
import os
import shutil
import six.moves.urllib.request
import six.moves.urllib.error
import six.moves.urllib.parse
import tempfile
import ssl

from DIRAC import gLogger
#from ILCDIRAC.Workflow.Modules.SLICPandoraAnalysis import SLICPandoraAnalysis

gLogger.setLevel("ERROR")
gLogger.showHeaders(True)


def cleanup(tempdir):
  """Remove files after run."""
  try:
    shutil.rmtree(tempdir)
  except OSError:
    pass


class TestSlicPandoraAnalysis(unittest.TestCase):
  """test SlicPandoraAnalysis."""

  def setUp(self):
    self.curdir = os.getcwd()
    self.tempdir = tempfile.mkdtemp("", dir="./")
    os.chdir(self.tempdir)

    super(TestSlicPandoraAnalysis, self).setUp()
    #self.spa = SLICPandoraAnalysis()
    self.mydir = "temp_dir"
    #detURL = "http://www.lcsim.org/detectors/clic_sid_cdr.zip"
    detURL = "https://lcd-data.web.cern.ch/lcd-data/ILCDIRACTars/testfiles/clic_sid_cdr.zip"
    self.zipfile = "clic_sid_cdr.zip"

    attempts = 0

    # create a fake ssl context to avoid checking certificate
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    while attempts < 3:
      try:
        response = six.moves.urllib.request.urlopen(detURL, timeout=5, context=ctx)
        content = response.read()
        with open(self.zipfile, 'wb') as zipF:
          zipF.write(content)
        break
      except six.moves.urllib.error.URLError as e:
        attempts += 1
        print(type(e), str(e))

  def tearDown(self):
    os.chdir(self.curdir)
    cleanup(self.tempdir)

  def test_Unzip_file_into_dir(self):
    """test unzip_file_into_dir....................................................................."""

    from ILCDIRAC.Core.Utilities.CombinedSoftwareInstallation import unzip_file_into_dir
    if not os.path.exists(self.mydir):
      os.mkdir(self.mydir)
    unzip_file_into_dir(self.zipfile, self.mydir)
    unzip_file_into_dir(self.zipfile, self.mydir)
    self.assertTrue(os.path.exists(os.path.join(self.mydir, "compact.xml")))


def runTests():
  """Runs our tests."""
  suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSlicPandoraAnalysis)
  testResult = unittest.TextTestRunner(verbosity=2).run(suite)
  print(testResult)


if __name__ == '__main__':
  runTests()
