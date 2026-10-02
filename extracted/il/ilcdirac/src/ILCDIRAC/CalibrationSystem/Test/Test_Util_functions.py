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
"""Unit tests for the CalibrationSystem/Utilities/functions.py."""

from __future__ import print_function
from __future__ import absolute_import
import pytest
import os
import string
import random
import tempfile
import shutil

from ILCDIRAC.CalibrationSystem.Utilities.functions import readParameterDict
from ILCDIRAC.CalibrationSystem.Utilities.functions import readParametersFromSteeringFile
from ILCDIRAC.CalibrationSystem.Utilities.functions import updateSteeringFile
from ILCDIRAC.CalibrationSystem.Utilities.functions import addParameterToProcessor
from six.moves import range

__RCSID__ = "$Id$"
MODULE_NAME = 'ILCDIRAC.CalibrationSystem.Utilities.functions'


def copySteeringFile(tag, calibID):
  """Copy steering files to local test directory."""
  workdirName = 'calib%s' % calibID
  if not os.path.exists(workdirName):
    os.makedirs(workdirName)

  if tag == 'CLIC':
    src = os.path.join(os.environ['ILCDIRAC_BASE_FOLDER'], 'Tests', 'Files', 'clicReconstruction.xml')
    shutil.copyfile(src, '%s/clicReconstruction.xml' % workdirName)
    return '%s/clicReconstruction.xml' % workdirName
  elif tag == 'FCCee':
    src = os.path.join(os.environ['ILCDIRAC_BASE_FOLDER'], 'Tests', 'Files', 'fccReconstruction.xml')
    shutil.copyfile(src, '%s/fccReconstruction.xml' % workdirName)
    return '%s/fccReconstruction.xml' % workdirName
  else:
    return None


def cleanDir(calibID):
  """Remove test directory."""
  workdirName = 'calib%s' % calibID
  if os.path.exists(workdirName):
    try:
      shutil.rmtree(workdirName)
    except EnvironmentError as e:
      print("Failed to delete directory: %s; ErrMsg: %s" % (workdirName, str(e)))
      assert False


@pytest.fixture
def copyFccSteeringFile():
  """Copy FCC steering file."""
  calibID = 1
  yield copySteeringFile('FCCee', calibID)
  #  cleanDir(calibID)


@pytest.fixture
def copyClicSteeringFile():
  """Copy CLIC steering file."""
  calibID = 1
  yield copySteeringFile('CLIC', calibID)
  cleanDir(calibID)


@pytest.fixture
def produceRandomTextFile():
  """Produce random text."""
  f = tempfile.NamedTemporaryFile(delete=False)
  nLines = random.randint(2, 20)
  for _ in range(0, nLines):
    nSymbolsInLine = random.randint(0, 120)
    line = ''
    for _ in range(0, nSymbolsInLine):
      line += random.choice(string.ascii_letters + '       ')
    f.write(line.encode())
  f.close()
  yield f.name
  os.unlink(f.name)


@pytest.fixture
def readEmptyParameterDict():
  """Read parameters from the file."""
  import ILCDIRAC.CalibrationSystem.Utilities as utilities
  fileDir = os.path.join(utilities.__path__[0], 'auxiliaryFiles')

  inFileName = os.path.join(fileDir, 'parameterListMarlinSteeringFile.txt')
  parDict = readParameterDict(inFileName)
  for iKey in list(parDict.keys()):
    if 'RootFile' in iKey:
      parDict.pop(iKey, None)
  return parDict


def test_addParameterToProcessor(produceRandomTextFile, copyFccSteeringFile, mocker):
  """Test adding of parameter to processor in Marlin steering file."""
  # non-existing input file
  res = addParameterToProcessor('dummy.xml', 'dummyProc', {'name': 'dummyValue'})
  assert not res['OK']
  assert "cannot find input" in res['Message']
  # non-xml input file
  randomFile = produceRandomTextFile
  res = addParameterToProcessor(randomFile, 'dummyProc', {'name': 'dummyValue'})
  assert not res['OK']
  assert "cannot parse input" in res['Message']
  # good input file, non-existing processor
  steeringFile = copyFccSteeringFile
  res = addParameterToProcessor(steeringFile, 'dummyProc', {'name': 'dummyValue'})
  assert not res['OK']
  assert "Can't find processor" in res['Message']
  # good input file, good processor name, no 'name' key in the parameter dict
  steeringFile = copyFccSteeringFile
  res = addParameterToProcessor(steeringFile, 'dummyProc', {'dummy': 'dummyValue'})
  assert not res['OK']
  assert "parameter dict should have key 'name'" in res['Message']
  # good input file, good processor name
  res = addParameterToProcessor(steeringFile, 'MyAIDAProcessor', {'name': 'dummyValue'})
  assert res['OK']
  # good input file, good processor name, second append of the parameter with the same name
  res = addParameterToProcessor(steeringFile, 'MyAIDAProcessor', {'name': 'dummyValue'})
  assert not res['OK']
  assert ("parameter with name %s already exists" % 'dummyValue') in res['Message']
  # good input file, good processor name
  res = addParameterToProcessor(steeringFile, 'MyDDCaloDigi_10ns', {'name': 'ECALLayers', 'type': 'IntVec',
                                                                    'value': '10 31'})
  assert res['OK']


def test_updateSteeringFile(copyClicSteeringFile, readEmptyParameterDict):
  """Test updateSteeringFile."""
  initialParDict = readEmptyParameterDict

  parDict1 = dict(initialParDict)
  #  inFileName = os.path.join(self.fileDir, 'clicReconstruction_2019-04-17.xml')
  inFileName = copyClicSteeringFile
  res = readParametersFromSteeringFile(inFileName, parDict1)
  #  key1 = "processor[@name='MyPfoAnalysis']/parameter[@name='RootFile']"
  #  parDict1[key1] = "dummyDummyRootFile.root"
  #  key2 = "global/parameter[@name='LCIOInputFiles']"
  #  parDict1[key2] = "in1.slcio, in2.slcio"
  #  self.assertTrue(len(parDict1) == len(initialParDict),
  #                  "two dictionaries have to be the same size. len1: %s; len2: %s"
  #                  % (len(parDict1), len(initialParDict)))

  outFileName = os.path.join(os.path.dirname(inFileName), 'out1.xml')
  res = updateSteeringFile(inFileName, outFileName, parDict1)
  assert res['OK']

  parDict2 = dict(initialParDict)
  res = readParametersFromSteeringFile(outFileName, parDict2)
  assert len(parDict1) == len(parDict2)

  notEqualValues = False
  for iKey in initialParDict:
    if parDict1[iKey] != parDict2[iKey]:
      notEqualValues = True
  assert not notEqualValues


def test_readParameterDict(readEmptyParameterDict):
  """Test readParameterDict."""
  parDict = readEmptyParameterDict
  assert '' not in parDict

  allValuesAreNone = True
  for _, iVal in parDict.items():
    if iVal is not None:
      allValuesAreNone = False
  assert allValuesAreNone


def test_readParametersFromSteeringFile(copyClicSteeringFile, readEmptyParameterDict):
  """Test readParametersFromSteeringFile."""
  parDict = readEmptyParameterDict
  inFileName = copyClicSteeringFile
  res = readParametersFromSteeringFile(inFileName, parDict)
  print(res)
  assert res['OK']

  someValuesAreNone = False
  for _, iVal in parDict.items():
    if iVal is None:
      someValuesAreNone = True
  assert not someValuesAreNone


def test_splitFilesAcrossJobs(mocker):
  """Test splitting of file across jobs."""
  from ILCDIRAC.CalibrationSystem.Utilities.functions import splitFilesAcrossJobs
  inputFiles = {'muon': ['muon1', 'muon2', 'muon3', 'muon4', 'muon5'],
                'kaon': ['kaon1', 'kaon2', 'kaon3', 'kaon4', 'kaon5'],
                'gamma': ['gamma1', 'gamma2', 'gamma3', 'gamma4', 'gamma5'],
                'zuds': ['zuds1', 'zuds2', 'zuds3', 'zuds4', 'zuds5']}
  nEventsPerFile = {'muon': 20, 'kaon': 24, 'gamma': 25, 'zuds': 30}

  def printOut(nJobs):
    print("\nnEventsPerFile: %s" % nEventsPerFile)
    print("nTotalEvents:")
    for iKey, iFiles in inputFiles.items():
      print("%s: %s" % (iKey, len(iFiles) * nEventsPerFile[iKey]))
    print("")

    outDict = splitFilesAcrossJobs(inputFiles, nEventsPerFile, nJobs)
    for i in range(0, nJobs):
      print("Job #%s:" % i)
      for iKey, iVal in outDict[i].items():
        print("%s\t --> %s" % (iKey, iVal))

  nJobs = 5
  printOut(nJobs)
  outDict = splitFilesAcrossJobs(inputFiles, nEventsPerFile, nJobs)
  for i in range(0, nJobs):
    for iKey, iVal in outDict[i].items():
      assert len(iVal[0]) == 1
      assert iVal[1] == 0
      assert iVal[2] == nEventsPerFile[iKey]

  nJobs = 2
  printOut(nJobs)
  outDict = splitFilesAcrossJobs(inputFiles, nEventsPerFile, nJobs)
  for i in range(0, nJobs):
    for iKey, iVal in outDict[i].items():
      assert len(iVal[0]) == 3
      assert iVal[1] == 0 or iVal[1] == nEventsPerFile[iKey] // 2
      assert iVal[2] == len(inputFiles[iKey]) * nEventsPerFile[iKey] // 2

  #  assert False
