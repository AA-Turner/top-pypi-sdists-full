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
"""Run the StdHepCutJava utility.

Apply a set of cuts on input stdhep files

:since: Apr 10, 2013

:author: Stephane Poss
"""

from __future__ import absolute_import
import os

from DIRAC import gLogger
from ILCDIRAC.Workflow.Modules.StdHepCut import StdHepCut

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class StdHepCutJava(StdHepCut):
  """Apply cuts on stdhep files, based on L.

  Weuste utility, rewritten in java by C. Grefe.
  """

  def __init__(self):
    super(StdHepCutJava, self).__init__()
    self.applicationName = 'stdhepcutjava'

  def prepareScript(self, mySoftDir):
    """Overloaded from stdhepcuts."""
    self.scriptName = '%s_%s_Run_%s.sh' % (self.applicationName, self.applicationVersion, self.STEP_NUMBER)
    if os.path.exists(self.scriptName):
      os.remove(self.scriptName)
    script = open(self.scriptName, 'w')
    script.write('#!/bin/sh \n')
    script.write('#####################################################################\n')
    script.write('# Dynamically generated script to run a production or analysis job. #\n')
    script.write('#####################################################################\n')
    if os.path.exists("lib"):
      script.write("declare -x CLASSPATH=./lib:$CLASSPATH\n")
    script.write('echo =========\n')
    script.write('echo java version :\n')
    script.write('java -version\n')
    script.write('env | sort >> localEnv.log\n')
    script.write('echo =============================\n')
    extraopts = ""
    if self.MaxNbEvts:
      extraopts = '-m %s' % self.MaxNbEvts
    comm = 'java -Xmx1536m -Xms256m -jar %s %s -o %s -c %s  %s\n' % (mySoftDir, extraopts,
                                                                     self.OutputFile, self.SteeringFile,
                                                                     self.fileMask)
    LOG.info("Running %s" % comm)
    script.write(comm)
    script.write('declare -x appstatus=$?\n')
    script.write('exit $appstatus\n')
    script.close()
