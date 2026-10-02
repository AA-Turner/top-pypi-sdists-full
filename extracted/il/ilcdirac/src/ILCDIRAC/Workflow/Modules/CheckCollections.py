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
"""Module to check the file contents.

:author: Ching Bon Lam
"""

from __future__ import absolute_import
import os

from string import Template

from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities.Subprocess import shellCall
from ILCDIRAC.Core.Utilities.PrepareLibs import removeLibc
from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


class CheckCollections(ModuleBase):
  """Check the collections in a given slcio file."""

  def __init__(self):

    super(CheckCollections, self).__init__()

    self.STEP_NUMBER = ''
    self.args = ''
    #self.result      = S_ERROR()
    self.jobID = None
    self.applicationName = 'CheckCollections'
    # Step parameters

    self.InputFile = []
    self.collections = None

  def execute(self):
    """Run the thing."""
    # Get input variables

    result = self.resolveInputVariables()

    # Checks

    if not self.platform:
      result = S_ERROR('No ILC platform selected')

    if 'LCIO' not in os.environ:
      LOG.error("Environment variable LCIO was not defined, cannot do anything")
      result = S_ERROR("Environment variable LCIO was not defined, cannot do anything")

    if not result['OK']:
      LOG.error("Failed to resolve the input parameters:", self.result["Message"])
      return result

    removeLibc(os.path.join(os.environ["LCIO"], "lib"))

    # Setting up script

    LD_LIBRARY_PATH = os.path.join("$LCIO", "lib")
    if 'LD_LIBRARY_PATH' in os.environ:
      LD_LIBRARY_PATH += ":" + os.environ['LD_LIBRARY_PATH']

    PATH = "$LCIO/bin"
    if 'PATH' in os.environ:
      PATH += ":" + os.environ['PATH']

    scriptContent = Template('''
#!/bin/sh

#------------------------------------------------------------------------------#
# Dynamically generated script by CheckCollections module                      #
#------------------------------------------------------------------------------#

declare -x LD_LIBRARY_PATH=$LD_LIBRARY_PATH_
declare -x PATH=$PATH_

python <<PYTHONSCRIPT

import sys, subprocess

exitStatus = 0

for file in $files:

    cmdResult      = subprocess.Popen( ["lcio", "count", file], stdout=subprocess.PIPE ).communicate()[ 0 ]
    numberOfEvents = int( cmdResult.strip().split()[1] )

    cmdAnajobResult = subprocess.Popen( ["anajob", file], stdout=subprocess.PIPE ).communicate()[ 0 ]

    for collection in $collections:

        cmdResult           = subprocess.Popen( ["grep", "-c", collection], stdin=subprocess.PIPE, stdout=subprocess.PIPE ).communicate( cmdAnajobResult )[ 0 ]
        numberOfCollections = int( cmdResult.strip() )

        if numberOfEvents != numberOfCollections:

            print 'Inconsistency in %s: %i events vs %i collections (%s)' % ( file, numberOfEvents, numberOfCollections, collection )

            exitStatus = 1
            #sys.exit( exitStatus )

sys.exit( exitStatus )

PYTHONSCRIPT

declare -x appstatus=$$?
exit $$appstatus

''')

    scriptContent = scriptContent.substitute(LD_LIBRARY_PATH_=LD_LIBRARY_PATH,
                                              PATH_=PATH,
                                              files=self.InputFile,
                                              collections=self.collections
                                            )

    # Write script to file

    scriptPath = 'CheckCollections_%s_Run_%s' % (self.applicationVersion, self.STEP_NUMBER)

    if os.path.exists(scriptPath):
      os.remove(scriptPath)

    script = open(scriptPath, 'w')
    script.write(scriptContent)
    script.close()

    # Setup log file for application stdout

    if os.path.exists(self.applicationLog):
      os.remove(self.applicationLog)

    # Run code

    os.chmod(scriptPath, 0o755)

    command = '"./%s"' % (scriptPath)

    self.setApplicationStatus('CheckCollections %s step %s' % (self.applicationVersion, self.STEP_NUMBER))
    self.stdError = ''

    self.result = shellCall(0,
                             command,
                             callbackFunction=self.redirectLogOutput,
                             bufferLimit=20971520
                           )

    # Check results

    resultTuple = self.result['Value']
    status = resultTuple[0]

    LOG.info("Status after the application execution is %s" % str(status))

    return self.finalStatusReport(status)

  def applicationSpecificInputs(self):

    # Logfile

    if not self.applicationLog:
      self.applicationLog = 'CheckCollections_%s_Run_%s.log' % (self.applicationVersion, self.STEP_NUMBER)

    #
    self.InputFile = [os.path.basename(myfile) for myfile in self.InputFile]
    #

    if len(self.collections) == 0:
      return S_ERROR('No list of collections defined to check for.')

    #

    return S_OK('Parameters resolved')
