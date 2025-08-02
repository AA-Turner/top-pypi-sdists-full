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
"""Create productions for the generation/simulation/reconstruction software chain.

First create a config file template::

  dirac-fcc-make-productions -p

Then modify the template to describe the productions::

  [whizard2]
  Version = 2.8.3
  EvtType = ZHH

  [delphesapp]
  ExecutableName = DelphesSTDHEP_EDM4HEP
  DetectorCard = card_IDEA.tcl
  OutputCard = edm4hep_IDEA.tcl
  Version = key4hep_230408

  [Production Parameters]
  machine = ee
  prodGroup = several

  softwareVersion = key4hep_230408
  generatorApplication = whizard2
  simulationApplication = ddsim
  reconstructionApplication = gaudiapp
  generatorSteeringFile = ee_ZHH_1500gev_polp80.sin
  secondaryGeneratorSteeringFile = Bd2PhiKs.dec
  processingAfterGen = delphesapp

  configVersion = key4hep-devel-2
  configPackage = fccConfig
  eventsPerJobs = 1000

  numberOfTasks = 1

  campaign = winter2023
  energies = 1500
  processes = ZHH
  detectorModel = idea

  productionLogLevel = VERBOSE
  outputSE = CERN-DST-EOS

  finalOutputSE = CERN-SRM
  MoveStatus = Stopped
  MoveGroupSize = 10

  ProdTypes = Gen

Further options can be found in the created template file. Many options can contain comma separated values to submit
multiple chains of productions in one command. The example above will create a chain of Generation with pythia and processing
with delphes, everything using a delphes standalone executable.

Then test if everything works::

  dirac-fcc-make-productions -f myProd

And finally submit to the system::

  dirac-fcc-make-productions -f myProd -x

Options:

   -p, --printConfigFile      Create the template to create productions
   -f, --configFile <file>    Defines the file with the parameters to create a production
   -x, --enable               Disable dry-run mode and actually create the production
   --additionalName       Define a string to add to the production name if the original name already exists


Parameters in the steering file

  :configPackage: Steering file package to use for simulation and reconstruction
  :configVersion: Steering file version to use for simulation and reconstruction
  :outputSE: output SE for transformation jobs
  :finalOutputSE: final destination for files when moving transformations are enabled
  :machine: the name of the machine: ee
  :campaign: season and year of the simulations
  :energies: energies of the processes
  :processes: name informative of process and final state
  :detectorModel: Detector Model appearing in the filepath
  :prodGroup: basename of the production group the productions are part of
  :productionLogLevel: log level to use in production jobs
  :softwareVersion: softwareVersion to use for generation/simulation/reconstruction
  :additionalName: additionalName to add to the transformation name in case a transformation
     with that name already exists

  :ProdTypes: Which transformations to create: Gen, Split, Sim, Rec, RecOver
  :MoveTypes: Which output file types to move: Gen, Sim, Rec, Dst
  :MoveGroupSize: The number of files to put in one replicationRequest
  :MoveStatus: The status of the Replication transformations: Active or Stopped
  :move: Whether or not to create the transformations to the output files to the finalOutputSE

  :energies: energy to use for generation or meta data search for each transformation chain
  :eventsPerJobs: number of events per job
  :processes: name of the processes to generate or use in meta data search
  :prodids: transformation IDs to use in meta data search for the first transformation of each chain

  :generatorSteeringFile: path to steering file for the generator
  :secondarygeneratorSteeringFile: optional path to a second steering file for the generator (for example when a pythia card AND a EvtGen user decay file are both required)
  :generatorApplication: specify which application to use for event generation
  :simulationApplication: specify which application to use for event simulation
  :reconstructionApplication: specify which application to use for event reconstruction
  :numberOfTasks: number of production jobs/task to create for Gen transformations (default is 1)

  :eventsInSplitFiles: For split transformations, number of events in the input files

  :cliReco: additional CLI options for reconstruction

  :overlayEvents: For ``RecOver`` transformations use these events for Overlay. By default the gghad
     events with the process energy are used for overlay. E.g.: ``380GeV``


The individual applications can be further modified in their respective section::

  [KKMC]
  #ApplicationAttributeName=Value

  [gaudiapp]
  #ApplicationAttributeName=Value

  [delphesapp]
  #ApplicationAttributeName=Value

All attributes with a ``set`` method can be changed. See
:mod:`~ILCDIRAC.Interfaces.API.NewInterface.Applications.KKMC`,
:mod:`~ILCDIRAC.Interfaces.API.NewInterface.Applications.GaudiApp`,
:mod:`~ILCDIRAC.Interfaces.API.NewInterface.Applications.DelphesApp`,



:since: July 14, 2017
:author: A Sailer
"""

# pylint disable=wrong-import-position

from __future__ import print_function
from __future__ import absolute_import
from pprint import pformat
from collections import defaultdict
from copy import deepcopy
from six.moves import range

import six.moves.configparser
import os

from DIRAC.Core.Base.Script import Script
from DIRAC import S_OK, S_ERROR, gLogger

from ILCDIRAC.Core.Utilities.PrepareOptionFiles import metaEnergy
from ILCDIRAC.Core.Utilities.Utilities import listify, lowerFirst
from ILCDIRAC.ILCTransformationSystem.Utilities.Utilities import Task
import six
from six.moves import zip_longest

PRODUCTION_PARAMETERS = 'Production Parameters'
PP = PRODUCTION_PARAMETERS
APPLICATION_LIST = ['KKMC', 'delphesapp', 'gaudiapp', 'babayaga', 'bhlumi', 'whizard2', 'ddsim']
LIST_ATTRIBUTES = ['ignoreMetadata',
                   'generatorSteeringFile',
                   'secondaryGeneratorSteeringFile',
                   'energies',
                   'eventsPerJobs',
                   'numberOfTasks',
                   'processes',
                   'prodIDs',
                   'eventsInSplitFiles',
                   'taskNames',
                   ]

STRING_ATTRIBUTES = ['configPackage',
                     'configVersion',
                     'additionalName',
                     'productionloglevel',
                     'outputSE',
                     'finalOutputSE',
                     'generatorApplication',
                     'simulationApplication',
                     'reconstructionApplication',
                     'MoveStatus',
                     'MoveGroupSize',
                     'prodGroup',
                     'machine',
                     'detectorModel',
                     'softwareVersion',
                     'overlayEvents',
                     'overlayEventType',
                     'campaign',
                     'processingAfterGen',
                     ]

class _Params(object):
  """Parameter Object."""

  def __init__(self):
    self.prodConfigFilename = None
    self.dumpConfigFile = False
    self.dryRun = True
    self.additionalName = ''

  def setProdConf(self, fileName):
    if not os.path.exists(fileName):
      return S_ERROR("ERROR: File %r not found" % fileName)
    self.prodConfigFilename = fileName
    return S_OK()

  def setDumpConf(self, _):
    self.dumpConfigFile = True
    return S_OK()

  def setEnable(self, _):
    self.dryRun = False
    return S_OK()

  def setAddName(self, addName):
    self.additionalName = addName
    return S_OK()

  def registerSwitches(self):
    Script.registerSwitch("f:", "configFile=", "Set config file for production", self.setProdConf)
    Script.registerSwitch("x", "enable", "create productions, if off dry-run", self.setEnable)
    Script.registerSwitch("p", "printConfigFile", "Print a config file to stdout", self.setDumpConf)
    Script.registerSwitch("", "additionalName=", "Name to add to the production", self.setAddName)
    Script.setUsageMessage("""%s --configFile=myProduction""" % ("dirac-fcc-make-productions", ))


class FCCDetProdChain(object):
  """Create applications and productions for FCC physics studies."""

  class Flags(object):
    """flags to enable or disable productions.

    :param bool dryRun: if False no productions are created
    :param bool gen: if True create generation production
    :param bool spl: if True create split production
    :param bool sim: if True create simulation production
    :param bool rec: if True create reconstruction production
    :param bool over: if True create reconstruction production with overlay, if `rec` is False this flag is also False
    :param bool move: if True create moving transformations, the other move flags only take effect if this one is True
    :param bool moveGen: if True move GEN files after they have been used in the production, also for split files
    :param bool moveSim: if True move SIM files after they have been used in the production
    :param bool moveRev: if True move REC files when they were created
    :param bool moveDst: if True move DST files when they were created
    """

    def __init__(self):
      # general flag to create anything at all
      self._dryRun = True

      # create transformations
      self._gen = False
      self._spl = False
      self._sim = False
      self._rec = False
      self._over = False

      # create moving transformations
      self._moves = False
      self._moveGen = False
      self._moveSim = False
      self._moveRec = False
      self._moveDst = False

      # list of tuple to preserve order
      self._prodTypes = [('gen', 'Gen'), ('spl', 'Split'), ('sim', 'Sim'), ('rec', 'Rec'), ('over', 'RecOver')]
      self._moveTypes = [('moveGen', 'Gen'), ('moveSim', 'Sim'), ('moveRec', 'Rec'), ('moveDst', 'Dst')]

    @property
    def dryRun(self):  # pylint: disable=missing-docstring
      return self._dryRun

    @property
    def gen(self):  # pylint: disable=missing-docstring
      return self._gen

    @property
    def spl(self):  # pylint: disable=missing-docstring
      return self._spl

    @property
    def sim(self):  # pylint: disable=missing-docstring
      return self._sim

    @property
    def rec(self):  # pylint: disable=missing-docstring
      return self._rec

    @property
    def over(self):  # pylint: disable=missing-docstring
      return self._over

    @property
    def move(self):  # pylint: disable=missing-docstring
      return self._moves

    @property
    def moveGen(self):  # pylint: disable=missing-docstring
      return (self._gen or self._spl) and self._moves and self._moveGen

    @property
    def moveSim(self):  # pylint: disable=missing-docstring
      return self._sim and self._moves and self._moveSim

    @property
    def moveRec(self):  # pylint: disable=missing-docstring
      return (self._rec or self._over) and self._moves and self._moveRec

    @property
    def moveDst(self):  # pylint: disable=missing-docstring
      return (self._rec or self._over) and self._moves and self._moveDst

    def __str__(self):
      pDict = vars(self)
      self.updateDictWithFlags(pDict)
      return """

#Productions to create: %(prodOpts)s
ProdTypes = %(prodTypes)s

move = %(_moves)s

#Datatypes to move: %(moveOpts)s
MoveTypes = %(moveTypes)s
""" % (vars(self))

    def updateDictWithFlags(self, pDict):
      """add flags and values to pDict."""
      for attr in dir(self):
        if isinstance(getattr(type(self), attr, None), property):
          pDict.update({attr: str(getattr(self, attr))})

      pDict.update(prodOpts=", ".join([pTuple[1]
                                           for pTuple in self._prodTypes]))
      pDict.update(prodTypes=", ".join([pTuple[1]
                                            for pTuple in self._prodTypes
                                            if getattr(self, pTuple[0])]))
      pDict.update(moveOpts=", ".join([pTuple[1]
                                            for pTuple in self._moveTypes]))
      pDict.update(moveTypes=", ".join([pTuple[1]
                                            for pTuple in self._moveTypes
                                            if getattr(self, '_' + pTuple[0])]))

    def __splitStringToOptions(self, config, tuples, optString, prefix='_'):
      """split the option string into separate values and set the corresponding flag."""
      prodsToCreate = config.get(PRODUCTION_PARAMETERS, optString)
      for prodType in listify(prodsToCreate):
        if not prodType:
          continue
        found = False
        for attribute, name in tuples:
          if name.capitalize() == prodType.strip().capitalize():
            setattr(self, prefix + attribute, True)
            found = True
            break
        if not found:
          raise AttributeError("Unknown parameter: %r " % prodType)

    def loadFlags(self, config):
      """load flags values from configfile."""
      self.__splitStringToOptions(config, self._prodTypes, 'ProdTypes', prefix='_')
      self.__splitStringToOptions(config, self._moveTypes, 'MoveTypes', prefix='_')
      self._moves = config.getboolean(PP, 'move')

  def __init__(self, params=None, group='fcc_prod'):

    from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
    self._ops = Operations(group=group)

    self.machine = {'ilc_prod': 'clic',
                    'fcc_prod': 'ee',
                    }[group]

    self.overlayEventType = {'ilc_prod': 'gghad',
                             'fcc_prod': 'pairs',
                             }[group]

    self.prodGroup = 'several'
    self._basepath = None  # resolved lazily via property
    prodPath = os.path.join('/Production', self.machine)
    self.detectorModel = self._ops.getValue(os.path.join(prodPath, 'DefaultDetectorModel'))
    self.softwareVersion = self._ops.getValue(os.path.join(prodPath, 'DefaultSoftwareVersion'))
    self.configVersion = self._ops.getValue(os.path.join(prodPath, 'DefaultConfigVersion'))
    self.configPackage = self._ops.getValue(os.path.join(prodPath, 'DefaultConfigPackage'))
    self.productionLogLevel = 'VERBOSE'
    self.outputSE = 'CERN-DST-EOS'
    self.moveStatus = 'Stopped'
    self.moveGroupSize = '10'

    self.eventsPerJobs = []
    self.numberOfTasks = []
    self.energies = []
    self.processes = []
    self.prodIDs = []
    self.eventsInSplitFiles = []
    self.taskNames = []

    # final destination for files once they have been used
    self.finalOutputSE = self._ops.getValue('Production/CLIC/FailOverSE')

    self.additionalName = params.additionalName

    self.overlayEvents = ''

    self.cliRecoOption = ''
    self.cliReco = ''

    self.generatorApplication = 'KKMC'
    self.generatorSteeringFile = []
    self.secondaryGeneratorSteeringFile = []
    self.processingAfterGen = ''

    self.campaign = ''

    self.simulationApplication = 'ddsim'

    self.reconstructionApplication = 'gaudiapp'

    self.ignoreMetadata = []

    self.applicationOptions = {appName: {} for appName in APPLICATION_LIST}

    self._flags = self.Flags()

    self.loadParameters(params)

    self._flags._dryRun = params.dryRun  # pylint: disable=protected-access

  @property
  def basepath(self):
    """Return the basepath"""
    if not self._basepath:
      prodPath = os.path.join('/Production', self.machine.upper())
      self._basepath = self._ops.getValue(os.path.join(prodPath, 'BasePath'))
    return os.path.join(self._basepath, self.campaign) + '/'
  
  def meta(self, prodID, process, energy):
    """return meta data dictionary, always new."""
    metaD = {'ProdID': str(prodID),
             'EvtType': process,
             'Energy': metaEnergy(energy),
             'Machine': self.machine,
             }
    for key in self.ignoreMetadata:
      metaD.pop(key)
    return metaD

  def loadParameters(self, parameter):
    """Load parameters from config file."""
    if parameter.prodConfigFilename is not None:
      defaultValueDict = vars(self)
      defaultValueDict = {key: str(value) for key, value in defaultValueDict.items()}
      self._flags.updateDictWithFlags(defaultValueDict)
      # we are passing all instance attributes as the default dict so generally we do not have to check
      # if an option exists, also options are case insensitive and stored in lowercase
      config = six.moves.configparser.SafeConfigParser(defaults=defaultValueDict, dict_type=dict)
      config.read(parameter.prodConfigFilename)
      self._flags.loadFlags(config)

      for attribute in LIST_ATTRIBUTES:
        setattr(self, attribute, listify(config.get(PP, attribute)))

      for attribute in STRING_ATTRIBUTES:
        setattr(self, lowerFirst(attribute), config.get(PP, attribute))

      # this parameter is deprecated and not part of the instance attributes so we need to check for existence
      if config.has_option(PP, 'clicConfig'):
        gLogger.warn('"clicConfig" parameter is deprected, please dump a new steering file!')
        self.configVersion = config.get(PP, 'clicConfig')

      # attribute and option names differ, special treatment
      self.cliRecoOption = config.get(PP, 'cliReco')

      if self.moveStatus not in ('Active', 'Stopped'):
        raise AttributeError("MoveStatus can only be 'Active' or 'Stopped' not %r" % self.moveStatus)

      # self.overlayEvents = self.checkOverlayParameter(self.overlayEvents)
      # self.overlayEventType = self.overlayEventType + self.overlayEvents.lower()

      self.processes = [process.strip() for process in self.processes if process.strip()]
      self.energies = [float(eng.strip()) for eng in self.energies if eng.strip()]
      self.eventsPerJobs = [int(epj.strip()) for epj in self.eventsPerJobs if epj.strip()]
      # these do not have to exist so we fill them to the same length if they are not set
      self.prodIDs = [int(pID.strip()) for pID in self.prodIDs if pID.strip()]
      self.prodIDs = self.prodIDs if self.prodIDs else [1 for _ in self.energies]

      # if one of the lists only has size 1 and there is a longer list we extend
      # the list to the maximum size assuming the values are re-used
      maxLength = 0
      parameterLists = [self.processes, self.energies, self.eventsPerJobs, self.generatorSteeringFile, self.secondaryGeneratorSteeringFile]
      
      for parList in parameterLists:
        maxLength = len(parList) if len(parList) > maxLength else maxLength
      for parList in parameterLists:
        if len(parList) == 1 and maxLength > 1:
          parList.extend([parList[0]] * (maxLength - 1))

      if not (self.processes and self.energies and self.eventsPerJobs) and self.prodIDs:
        eventsPerJobSave = list(self.eventsPerJobs) if self.eventsPerJobs else None
        self._getProdInfoFromIDs()
        self.eventsPerJobs = eventsPerJobSave if eventsPerJobSave else self.eventsPerJobs

      self.numberOfTasks = [int(nbtask.strip()) for nbtask in self.numberOfTasks if nbtask.strip()]
      self.numberOfTasks = self.numberOfTasks if self.numberOfTasks else [1] * len(self.energies)
      self.taskNames = self.taskNames if self.taskNames else [''] * len(self.energies)

      if len(self.processes) != len(self.energies) or \
         len(self.energies) != len(self.eventsPerJobs) or \
         len(self.prodIDs) != len(self.eventsPerJobs) or \
         len(self.eventsPerJobs) != len(self.taskNames) or \
         False:
        raise AttributeError('Lengths of Processes, Energies, EventsPerJobs, AdditionalNames do not match')

      if self._flags.gen:
        if len(self.numberOfTasks) != len(self.energies) or \
           (self.generatorSteeringFile and (len(self.generatorSteeringFile) != len(self.energies))) or \
           (self.secondaryGeneratorSteeringFile and (len(self.secondaryGeneratorSteeringFile) != len(self.generatorSteeringFile))):
          raise AttributeError("Lengths of numberOfTasks, generatorSteeringFile, secondaryGeneratorSteeringFile, and Energies do not match")

      self.eventsInSplitFiles = listify(self.eventsInSplitFiles, int)
      self.eventsInSplitFiles = self.eventsInSplitFiles if self.eventsInSplitFiles else [-1] * len(self.energies)

      if self._flags.spl and len(self.eventsInSplitFiles) != len(self.energies):
        raise AttributeError("Length of eventsInSplitFiles does not match: %d vs %d" % (
            len(self.eventsInSplitFiles),
            len(self.energies)))

      # read options from application sections
      config2 = six.moves.configparser.SafeConfigParser(dict_type=dict)
      config2.optionxform = str  # do not transform options to lowercase
      config2.read(parameter.prodConfigFilename)
      for appName in APPLICATION_LIST:
        try:
          self.applicationOptions[appName] = dict(config2.items(appName))
        except six.moves.configparser.NoSectionError:
          pass

    if parameter.dumpConfigFile:
      print(self)
      raise RuntimeError('')

  def _getProdInfoFromIDs(self):
    """get the processName, energy and eventsPerJob from the MetaData catalog.

    :raises: AttributeError if some of the information cannot be found
    :returns: None
    """
    if not self.prodIDs:
      raise AttributeError("No prodIDs defined")

    self.eventsPerJobs = []
    self.processes = []
    self.energies = []
    from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
    from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
    trc = TransformationClient()
    fc = FileCatalogClient()
    for prodID in self.prodIDs:
      gLogger.notice("Getting information for %s" % prodID)
      tRes = trc.getTransformation(str(prodID))
      if not tRes['OK']:
        raise AttributeError("No prodInfo found for %s" % prodID)
      self.eventsPerJobs.append(int(tRes['Value']['EventsPerTask']))
      lfnRes = fc.findFilesByMetadata({'ProdID': prodID})
      if not lfnRes['OK'] or not lfnRes['Value']:
        raise AttributeError("Could not find files for %s: %s " % (prodID, lfnRes.get('Message', lfnRes.get('Value'))))
      path = os.path.dirname(lfnRes['Value'][0])
      fileRes = fc.getDirectoryUserMetadata(path)
      self.processes.append(fileRes['Value']['EvtType'])
      self.energies.append(fileRes['Value']['Energy'])
      gLogger.notice("Found (Evts,Type,Energy): %s %s %s " %
                     (self.eventsPerJobs[-1], self.processes[-1], self.energies[-1]))

  def __str__(self):
    pDict = vars(self)
    appOptionString = ''
    for appName in APPLICATION_LIST:
      appOptionString += '[%s]\n#ApplicationAttributeName=Value\n\n' % appName

    pDict.update({'ProductionParameters': PRODUCTION_PARAMETERS})
    pDict.update({'ApplicationOptions': appOptionString})
    return """
%(ApplicationOptions)s
[%(ProductionParameters)s]
machine = %(machine)s
prodGroup = %(prodGroup)s
softwareVersion = %(softwareVersion)s

generatorApplication = %(generatorApplication)s
simulationApplication = %(simulationApplication)s
reconstructionApplication = %(reconstructionApplication)s
generatorSteeringFile = %(generatorSteeringFile)s
secondaryGeneratorSteeringFile = %(secondaryGeneratorSteeringFile)s
processingAfterGen = %(processingAfterGen)s

campaign = %(campaign)s
energies = %(energies)s
processes = %(processes)s
detectorModel = %(detectorModel)s

configVersion = %(configVersion)s
configPackage = %(configPackage)s
eventsPerJobs = %(eventsPerJobs)s
## Number of jobs/task to generate (default = 1)
# numberOfTasks =

## optional prodid to search for input files
# prodIDs =

## number of events for input files to split productions
eventsInSplitFiles = %(eventsInSplitFiles)s

productionLogLevel = %(productionLogLevel)s
outputSE = %(outputSE)s

finalOutputSE = %(finalOutputSE)s
MoveStatus = %(moveStatus)s
MoveGroupSize = %(moveGroupSize)s

## optional additional name
# additionalName = %(additionalName)s
## optional additional names, for for each process, prodID, etc.
# taskNames =

overlayEventType = %(overlayEventType)s
## optional energy to use for overlay: e.g. 3TeV
# overlayEvents = %(overlayEvents)s

%(_flags)s

""" % (pDict)

  def createGeneratorApplication(self, task):
    """Create the selected Generator application."""
    genApp = {'kkmc': self.createKKMCApplication,
              'whizard2': self.createWhizard2Application,
              'babayaga': self.createBabayagaApplication,
              'bhlumi': self.createBhlumiApplication,
              'delphesapp': self.createDelphesApplication,
              'gaudiapp': self.createGaudiApplication,
              }[self.generatorApplication.lower()](task)
    return genApp

  def createSimulationApplication(self, task):
    """Create the selected Simulation application."""
    simApp = {'ddsim': self.createDDSimApplication,
              'gaudiapp': self.createGaudiApplication,
              'delphesapp': self.createDelphesApplication,
              }[self.simulationApplication.lower()](task)
    return simApp

  def createReconstructionApplication(self, task, over):
    """Create the selected Reconstruction application."""
    recApp = {'gaudiapp': self.createGaudiApplication,
              }[self.reconstructionApplication.lower()](task)
    recApp.datatype = 'rec'
    return recApp

  def createKKMCApplication(self, task):
    """create KKMCee Application."""
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import KKMC
    kkmcee = KKMC()
    kkmcee.setVersion(self.softwareVersion)
    kkmcee.setNumberOfEvents(task.eventsPerJob)
    if task.genFile:
      kkmcee.setConfigFile(task.genFile)
    kkmcee.setEvtType(''.join(task.meta['EvtType'][:len(task.meta['EvtType']) // 2]).capitalize())
    kkmcee.setEnergy(task.meta['Energy'])
    kkmcee.datatype = 'hepmc'
    self._setApplicationOptions('KKMC', kkmcee, task.applicationOptions)
    return kkmcee

  def createWhizard2Application(self, task):
    """create Whizard2 Application."""
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import Whizard2
    whiz = Whizard2()
    whiz._decayProc = ['proc']
    whiz.setVersion(self.softwareVersion)
    whiz.setNumberOfEvents(task.eventsPerJob)
    whiz.setSinFile(task.genFile)
    whiz.setEvtType(task.meta['EvtType'])
    whiz.setEnergy(task.meta['Energy'])
    whiz.datatype = 'stdhep'
    self._setApplicationOptions('whizard2', whiz, task.applicationOptions)
    return whiz

  def createBabayagaApplication(self, task):
    """create Babayaga Application."""
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import Babayaga
    babayaga = Babayaga()
    babayaga.setVersion(self.softwareVersion)
    babayaga.setNumberOfEvents(task.eventsPerJob)
    if task.genFile:
      babayaga.setConfigFile(task.genFile)
    babayaga.setEnergy(task.meta['Energy'])
    babayaga.datatype = 'lhef'
    self._setApplicationOptions('Babayaga', babayaga, task.applicationOptions)
    return babayaga
  
  def createBhlumiApplication(self, task):
    """create Bhlumi Application."""
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import Bhlumi
    bhlumi = Bhlumi()
    bhlumi.setVersion(self.softwareVersion)
    bhlumi.setNumberOfEvents(task.eventsPerJob)
    if task.genFile:
      bhlumi.setConfigFile(task.genFile)
    bhlumi.setEnergy(task.meta['Energy'])
    bhlumi.datatype = 'lhef'
    self._setApplicationOptions('Bhlumi', bhlumi, task.applicationOptions)
    return bhlumi
  
  def createDelphesApplication(self, task):
    """create Delphes Application."""
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import DelphesApp
    delphes = DelphesApp()
    delphes.setVersion(self.softwareVersion)
    if task.genFile:
      delphes.setPythia8Card(task.genFile)
    if task.secondGenFile:
      delphes.setEvtGenDecCard(task.secondGenFile)
    delphes.setNumberOfEvents(task.eventsPerJob)
    delphes.setEnergy(task.meta['Energy'])
    delphes.detector = self.detectorModel
    delphes.datatype = 'delphes'
    self._setApplicationOptions('delphesapp', delphes, task.applicationOptions)
    return delphes

  def createGaudiApplication(self, task):
    """create Gaudi Application."""
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import GaudiApp
    gaudi = GaudiApp()
    gaudi.setVersion(self.softwareVersion)
    gaudi.setNumberOfEvents(task.eventsPerJob)
    gaudi.setEnergy(task.meta['Energy'])
    gaudi.detector = self.detectorModel
    self._setApplicationOptions('gaudiapp', gaudi, task.applicationOptions)
    if gaudi.gaudiWorkFlow == 'fastsim':
      gaudi.setPythia8Card(task.genFile)
      gaudi.datatype = 'delphes'
    elif gaudi.gaudiWorkFlow == 'fullsim':
      gaudi.setKeepRecFile(True)
    return gaudi

  def createDDSimApplication(self, task):
    """create DDSim Application."""
    from ILCDIRAC.Interfaces.API.NewInterface.Applications import DDSim
    ddsim = DDSim()
    ddsim.setVersion(self.softwareVersion)
    ddsim.setDetectorModel(self.detectorModel)
    ddsim.setNumberOfEvents(task.eventsPerJob)
    ddsim.setEnergy(task.meta['Energy'])
    self._setApplicationOptions('ddsim', ddsim, task.applicationOptions)
    ddsim.datatype = 'sim'
    return ddsim

  def createGenerationProduction(self, task):
    """Create generation production."""
    prodName = task.getProdName(self.machine, 'gen', self.additionalName)
    parameterDict = task.parameterDict
    nbTasks = task.nbTasks
    gLogger.notice("*" * 80 + "\nCreating generation production: %s " % prodName)
    genProd = self.getProductionJob()
    genProd.setConfigPackage(appName=self.configPackage, version=self.configVersion)
    genProd.evttype = parameterDict['process']
    genProd.setProdType('MCGeneration')
    genProd.setWorkflowName(prodName)
    # this might modify task
    genApp = self.createGeneratorApplication(task)
    if task.generator:
      genProd.generator = task.generator
    res = genProd.append(genApp)
    if not res['OK']:
      raise RuntimeError("Error creating generation production: %s" % res['Message'])
    if self.processingAfterGen:
      processingapp = {'delphesapp': self.createDelphesApplication,
                       'gaudiapp': self.createGaudiApplication,
                       }[self.processingAfterGen](task)
      processingapp.setInputFile('events.' + genApp._extension)
      res = genProd.append(processingapp)
      if not res['OK']:
        raise RuntimeError("Error creating generation production: %s" % res['Message'])
        
    genProd.addFinalization(True, True, True, True)
    if not prodName:
      raise RuntimeError("Error creating generation production: prodName empty")
    genProd.setDescription(prodName)
    res = genProd.createProduction()
    if not res['OK']:
      raise RuntimeError("Error creating generation production: %s" % res['Message'])

    for finalPath in genProd.finalpaths:
      if 'lhef' in finalPath:
        genProd.specialFinalMetaData.setdefault(finalPath, {})['SWPackages'] = \
          ';'.join(pkg for pkg in genProd.prodparameters["SWPackages"].split(';') if 'kkmc' in pkg.lower())

    # genProd.addMetadataToFinalFiles({'BeamParticle1': parameterDict['pname1'],
    #                                  'BeamParticle2': parameterDict['pname2'],
    #                                  'EPA_B1': parameterDict['epa_b1'],
    #                                  'EPA_B2': parameterDict['epa_b2'],
    #                                 }
    #                                )

    res = genProd.finalizeProd()
    if not res['OK']:
      raise RuntimeError("Error finalizing generation production: %s" % res['Message'])

    genProd.setNbOfTasks(nbTasks)
    generationMeta = genProd.getMetadata()
    return generationMeta

  def createSimulationProduction(self, task):
    """Create simulation production."""
    meta = task.meta
    prodName = task.getProdName('sim', self.detectorModel, self.additionalName)
    parameterDict = task.parameterDict
    gLogger.notice("*" * 80 + "\nCreating simulation production: %s " % prodName)
    simProd = self.getProductionJob()
    simProd.setProdType('MCSimulation')
    simProd.setConfigPackage(appName=self.configPackage, version=self.configVersion)
    res = simProd.setInputDataQuery(meta)
    if not res['OK']:
      raise RuntimeError("Error creating Simulation Production: %s" % res['Message'])
    simProd.setWorkflowName(prodName)
    # Add the application
    simApp = self.createSimulationApplication(task)
    res = simProd.append(simApp)
    if not res['OK']:
      raise RuntimeError("Error creating simulation Production: %s" % res['Message'])
    simProd.addFinalization(True, True, True, True)
    description = "Model: %s" % self.detectorModel
    if prodName:
      description += ", %s" % prodName
    simProd.setDescription(description)
    res = simProd.createProduction()
    if not res['OK']:
      raise RuntimeError("Error creating simulation production: %s" % res['Message'])

    # simProd.addMetadataToFinalFiles({'BeamParticle1': parameterDict['pname1'],
    #                                    'BeamParticle2': parameterDict['pname2'],
    #                                    'EPA_B1': parameterDict['epa_b1'],
    #                                    'EPA_B2': parameterDict['epa_b2'],
    #                                  }
    #                                )

    res = simProd.finalizeProd()
    if not res['OK']:
      raise RuntimeError("Error finalizing simulation production: %s" % res['Message'])

    simulationMeta = simProd.getMetadata()
    return simulationMeta

  def createReconstructionProduction(self, task, over):
    """Create reconstruction production."""
    gLogger.notice('Creating Reconstruction production', task)
    meta = task.meta
    recType = 'rec_overlay' if over else 'rec'
    prodName = task.getProdName(recType, self.detectorModel, self.additionalName)
    if over:
      prodName = prodName.replace('overlay', 'overlay%s' % self.overlayEvents if self.overlayEvents else meta['Energy'])
    parameterDict = task.parameterDict
    gLogger.notice("*" * 80 + "\nCreating %s reconstruction production: %s " % ('overlay' if over else '', prodName))
    recProd = self.getProductionJob()
    productionType = 'MCReconstruction_Overlay' if over else 'MCReconstruction'
    recProd.setProdType(productionType)
    recProd.setConfigPackage(appName=self.configPackage, version=self.configVersion)

    res = recProd.setInputDataQuery(meta)
    if not res['OK']:
      raise RuntimeError("Error setting inputDataQuery for Reconstruction production: %s " % res['Message'])

    recProd.setWorkflowName(prodName)

    # # Add overlay if needed
    # if over:
    #   res = recProd.append(self.createOverlayApplication(task))
    #   if not res['OK']:
    #     raise RuntimeError("Error appending overlay to reconstruction transformation: %s" % res['Message'])

    # add reconstruction
    res = recProd.append(self.createReconstructionApplication(task, over))
    if not res['OK']:
      raise RuntimeError("Error appending reconstruction application to reconstruction production: %s" % res['Message'])
    recProd.addFinalization(True, True, True, True)

    description = "CLICDet2017 %s" % meta['Energy']
    description += "Overlay" if over else "No Overlay"
    if prodName:
      description += ", %s" % prodName
    recProd.setDescription(description)

    res = recProd.createProduction()
    if not res['OK']:
      raise RuntimeError("Error creating reconstruction production: %s" % res['Message'])

    # recProd.addMetadataToFinalFiles({'BeamParticle1': parameterDict['pname1'],
    #                                    'BeamParticle2': parameterDict['pname2'],
    #                                    'EPA_B1': parameterDict['epa_b1'],
    #                                    'EPA_B2': parameterDict['epa_b2'],
    #                                  }
    #                                )

    res = recProd.finalizeProd()
    if not res['OK']:
      raise RuntimeError("Error finalising reconstruction production: %s " % res['Message'])

    reconstructionMeta = recProd.getMetadata()
    return reconstructionMeta

  def createSplitProduction(self, task, limited=False):
    """Create splitting transformation for splitting files."""
    meta = task.meta
    prodName = task.getProdName('split', task.meta['ProdID'], self.additionalName)
    parameterDict = task.parameterDict
    eventsPerJob = task.eventsPerJob
    eventsPerBaseFile = task.eventsPerBaseFile

    gLogger.notice("*" * 80 + "\nCreating split production: %s " % prodName)
    splitProd = self.getProductionJob()
    splitProd.setProdPlugin('Limited' if limited else 'Standard')
    splitProd.setProdType('Split')

    res = splitProd.setInputDataQuery(meta)
    if not res['OK']:
      raise RuntimeError('Split production: failed to set inputDataQuery: %s' % res['Message'])
    splitProd.setWorkflowName(prodName)

    # # Add the application
    # res = splitProd.append(self.createSplitApplication(eventsPerJob, eventsPerBaseFile, 'stdhep'))
    # if not res['OK']:
    #   raise RuntimeError('Split production: failed to append application: %s' % res['Message'])
    # splitProd.addFinalization(True, True, True, True)
    # description = 'Splitting stdhep files'
    # splitProd.setDescription(description)

    res = splitProd.createProduction()
    if not res['OK']:
      raise RuntimeError("Failed to create split production: %s " % res['Message'])

    splitProd.addMetadataToFinalFiles({"BeamParticle1": parameterDict['pname1'],
                                         "BeamParticle2": parameterDict['pname2'],
                                         "EPA_B1": parameterDict['epa_b1'],
                                         "EPA_B2": parameterDict['epa_b2'],
                                       }
                                     )

    res = splitProd.finalizeProd()
    if not res['OK']:
      raise RuntimeError('Split production: failed to finalize: %s' % res['Message'])

    return splitProd.getMetadata()

  def createMovingTransformation(self, meta, prodType):
    """create moving transformations for output files."""

    sourceSE = self.outputSE
    targetSE = self.finalOutputSE
    prodID = meta['ProdID']
    try:
      dataTypes = {'MCReconstruction': ('DST', 'REC'),
                    'MCReconstruction_Overlay': ('DST', 'REC'),
                    'MCSimulation': ('SIM',),
                    'MCGeneration': ('GEN',),
                  }[prodType]
    except KeyError:
      raise RuntimeError("ERROR creating MovingTransformation" + repr(prodType) + "unknown")

    if not any(getattr(self._flags, "move%s" % dataType.capitalize()) for dataType in dataTypes):
      gLogger.notice("*" * 80 + "\nNot creating moving transformation for prodID: %s, %s " % (meta['ProdID'], prodType))
      return

    from DIRAC.TransformationSystem.Utilities.ReplicationTransformation import createDataTransformation
    from DIRAC.TransformationSystem.Client.Transformation import Transformation
    for dataType in dataTypes:
      if getattr(self._flags, "move%s" % dataType.capitalize()):
        gLogger.notice("*" * 80 + "\nCreating moving transformation for prodID: %s, %s, %s " %
                       (meta['ProdID'], prodType, dataType))
        parDict = dict(flavour='Moving',
                       targetSE=targetSE,
                       sourceSE=sourceSE,
                       plugin='Broadcast%s' % ('' if dataType.lower() not in ('gen', 'sim') else 'Processed'),
                       metaKey='ProdID',
                       metaValue=prodID,
                       extraData={'Datatype': dataType},
                       tGroup=self.prodGroup,
                       groupSize=int(self.moveGroupSize),
                       enable=not self._flags.dryRun,
                      )
        message = "Moving transformation with parameters"
        gLogger.notice("%s:\n%s" % (message, pformat(parDict, indent=len(message) + 2, width=120)))
        res = createDataTransformation(**parDict)
        if not res['OK']:
          gLogger.error("Failed to create moving transformation:", res['Message'])

        elif isinstance(res['Value'], Transformation):
          newTrans = res['Value']
          newTrans.setStatus(self.moveStatus)

  def getProductionJob(self):
    """return production job instance with some parameters set."""
    from ILCDIRAC.Interfaces.API.NewInterface.ProductionJob import ProductionJob
    prodJob = ProductionJob()
    prodJob.setLogLevel(self.productionLogLevel)
    prodJob.setProdGroup(self.prodGroup)
    prodJob.setOutputSE(self.outputSE)
    prodJob.basepath = self.basepath
    prodJob.campaign = self.campaign
    prodJob.dryrun = self._flags.dryRun
    prodJob.maxFCFoldersToCheck = 1
    return prodJob

  def _setApplicationOptions(self, appName, app, optionsDict=None):
    """set options for given application.

    :param str appName: name of the application, for print out
    :param app: application instance
    """
    if optionsDict is None:
      optionsDict = {}
    allOptions = dict(self.applicationOptions.get(appName, {}))
    allOptions.update(optionsDict)
    for option, value in allOptions.items():
      if option.startswith(('FE.', 'C_', 'additionalName')):
        continue
      gLogger.notice("%s: setting option %s to %s" % (appName, option, value))
      setterFunc = 'set' + option
      if not hasattr(app, setterFunc):
        raise AttributeError("Cannot set %s for %s, check spelling!" % (option, appName))
      if value.lower() in ('false', 'true'):
        value = value.lower() == 'true'
      getattr(app, setterFunc)(value)

  def createTransformations(self, taskDict):
    """Create all the transformations we want to create."""
    for pType, createProduction in [('GEN', self.createGenerationProduction),
                                    ('SPLIT', self.createSplitProduction)]:
      for task in taskDict.get(pType, []):
        meta = createProduction(task)
        self.addSimTask(taskDict, meta, originalTask=task)
        taskDict['MOVE_' + pType].append(dict(meta))

    for task in taskDict.get('SIM', []):
      if not self._flags.sim:
        continue
      gLogger.notice("Creating task %s" % task)
      simMeta = self.createSimulationProduction(task)
      self.addRecTask(taskDict, simMeta, originalTask=task)
      taskDict['MOVE_SIM'].append(dict(simMeta))

    for task in taskDict.get('REC', []):
      for name, over, enabled in [('REC', False, self._flags.rec),
                                  ('OVER', True, self._flags.over)]:
        if enabled:
          recMeta = self.createReconstructionProduction(task, over=over)
          taskDict['MOVE_' + name].append(dict(recMeta))

    for name, pType in [('GEN', 'MCGeneration'),
                        ('SPLIT', 'MCGeneration'),
                        ('SIM', 'MCSimulation'),
                        ('REC', 'MCReconstruction'),
                        ('OVER', 'MCReconstruction_Overlay')]:
      for meta in taskDict.get('MOVE_' + name, []):
        self.createMovingTransformation(meta, pType)

  def createTaskDict(self, prodID, process, energy, eventsPerJob, sinFile, secondFile, nbTasks,
                     eventsPerBaseFile, taskName):
    """Create a dictionary of tasks for the first level of transformations."""
    taskDict = defaultdict(list)
    metaInput = self.meta(prodID, process, energy)
    prodName = metaInput['EvtType']
    parameterDict = {'process': metaInput['EvtType']}
    if self._flags.gen:
      self.addGenTask(taskDict, Task(metaInput, parameterDict, eventsPerJob, nbTasks=nbTasks,
                                     genFile=sinFile,
                                     secondGenFile=secondFile,
                                     taskName=taskName))

    elif self._flags.spl and eventsPerBaseFile == eventsPerJob:
      gLogger.notice("*" * 80 + "\nSkipping split transformation for %s\n" % prodName + "*" * 80)
      if self._flags.sim:
        self.addSimTask(taskDict, metaInput, Task({}, parameterDict, eventsPerJob,
                                                  taskName=taskName))
    elif self._flags.spl:
      taskDict['SPLIT'].append(Task(metaInput, parameterDict, eventsPerJob,
                                    eventsPerBaseFile=eventsPerBaseFile))
    elif self._flags.sim:
      self.addSimTask(taskDict, metaInput, Task({}, parameterDict, eventsPerJob, taskName=taskName))
    elif self._flags.rec or self._flags.over:
      self.addRecTask(taskDict, metaInput, Task({}, parameterDict, eventsPerJob, taskName=taskName))

    return taskDict

  def _addTask(self, taskDict, metaInput, originalTask, prodType, applicationName):
    """Add a task to the taskDict."""
    options = defaultdict(list)
    nTasks = 0
    for option, value in self.applicationOptions[applicationName].items():
      if option.startswith('FE.'):
        optionName = option.split('.', 1)[1]
        options[optionName] = listify(value)
        gLogger.notice("Found option %s with values %s" % (optionName, pformat(options[optionName])))
        nTasks = len(options[optionName])

    theTask = Task(metaInput,
                   parameterDict=originalTask.parameterDict,
                   eventsPerJob=originalTask.eventsPerJob,
                   metaPrev=originalTask.meta,
                   genFile=originalTask.genFile,
                   secondGenFile=originalTask.secondGenFile,
                   nbTasks=originalTask.nbTasks,
                   )
    theTask.sourceName = '_'.join([originalTask.sourceName, originalTask.taskName])
    if not nTasks:
      taskDict[prodType].append(theTask)
      return

    taskList = [deepcopy(theTask) for _ in range(nTasks)]
    taskDict[prodType].extend(taskList)
    self.addTaskOptions(options, taskList)
    return

  def addGenTask(self, taskDict, originalTask):
    """Add a generator task with required options."""
    return self._addTask(taskDict, metaInput=originalTask.meta,
                         originalTask=originalTask, prodType='GEN',
                         applicationName=self.generatorApplication,
                         )

  def addSimTask(self, taskDict, metaInput, originalTask):
    """Add a simulation task."""
    return self._addTask(taskDict, metaInput, originalTask, prodType='SIM',
                         applicationName=self.simulationApplication)

  def addRecTask(self, taskDict, metaInput, originalTask):
    """Add a reconstruction task."""
    return self._addTask(taskDict, metaInput, originalTask, prodType='REC',
                         applicationName=self.reconstructionApplication)

  @staticmethod
  def addTaskOptions(options, taskList):
    """Add the options to each task in the taskList."""
    for optionName, values in options.items():
      if optionName.startswith('Query'):
        queryParameter = optionName[len('Query'):]
        for index, value in enumerate(values):
          taskList[index].meta[queryParameter] = value
      elif optionName == 'additionalName':
        for index, value in enumerate(values):
          taskList[index].taskName = value
      # cliReco only makes sense for REC application, but it is otherwise ignored
      elif optionName == 'cliReco':
        for index, value in enumerate(values):
          taskList[index].cliReco = value
      else:
        for index, value in enumerate(values):
          taskList[index].applicationOptions[optionName] = value

  def createAllTransformations(self):
    """Loop over the list of processes, energies and possibly prodIDs to create all the productions."""
    for energy, process, prodID, eventsPerJob, eventsPerBaseFile, genFile, secondGenFile, nbTasks, taskName in \
        zip_longest(self.energies, self.processes, self.prodIDs, self.eventsPerJobs, self.eventsInSplitFiles,
                     self.generatorSteeringFile, self.secondaryGeneratorSteeringFile, self.numberOfTasks, self.taskNames, fillvalue=None):
      taskDict = self.createTaskDict(prodID, process, energy, eventsPerJob, genFile, secondGenFile,
                                     nbTasks, eventsPerBaseFile, taskName)
      self.createTransformations(taskDict)


@Script()
def main():
  CLIP = _Params()
  CLIP.registerSwitches()
  Script.parseCommandLine()
  from ILCDIRAC.Core.Utilities.CheckAndGetProdProxy import checkOrGetGroupProxy
  CHECKGROUP = checkOrGetGroupProxy(['ilc_prod', 'fcc_prod'])
  if CHECKGROUP['OK']:
    pass
  elif CLIP.dryRun:
    gLogger.notice('Did not find correct group, dryRun enabled, assuming "fcc_prod"')
    CHECKGROUP = S_OK('fcc_prod')
  else:
    exit(1)
  try:
    CHAIN = FCCDetProdChain(params=CLIP, group=CHECKGROUP['Value'])
    CHAIN.createAllTransformations()
  except (AttributeError, RuntimeError) as excp:
    if str(excp) != '':
      gLogger.exception('Failure to create transformations', lException=excp)
      exit(1)
  exit(0)

if __name__ == "__main__":
  main()
