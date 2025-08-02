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
"""Mixin for userjob splitting options."""

from __future__ import absolute_import

from DIRAC import S_OK, gLogger
from DIRAC.Core.Utilities.List import breakListIntoChunks

from ILCDIRAC.Core.Utilities.Utilities import toInt
from six.moves import range

LOG = gLogger.getSubLogger(__name__)


class SplitMixin(object):
  """Mixin class for user job splitting functions."""

  def _initialize(self):
    """Initialize splitting members."""
    self._data = []
    self._splittingOption = None
    self._switch = {'byEvents': self._splitByEvents,
                    'byData': self._splitByData,
                    'bySkip': self._splitBySkip,
                    }

    self._numberOfJobs = None
    self._totalNumberOfEvents = None
    self._eventsPerJob = None
    self._eventsPerFile = None
    self._numberOfFilesPerJob = 1
    self._startJobIndex = 0
    self._jobIndexList = None

  def _checkSplitConsistency(self):
    """Check if splitting options are consistent.

    :return: The success or the failure of the consistency checking
    :rtype: bool
    """
    LOG.notice("Checking job consistency")

    if self._splittingOption and self._splittingOption not in self._switch:
      splitOptions = ",".join(list(self._switch.keys()))
      return self._reportError("Consistency check failed: Bad split value: possible values are %s" % splitOptions)

    # All applications should have the same number of events
    # We can get this number from the first application for example
    sameNumberOfEvents = next(iter(self.applicationlist)).numberOfEvents

    if not all(app.numberOfEvents == sameNumberOfEvents for app in self.applicationlist):
      return self._reportError("Job: Applications should all have the same number of events")

    if sameNumberOfEvents == -1 and not self._data:
      return self._reportError("Job: Number of events is -1 without input data. Was that intentional?")

    LOG.notice("Consistency check successful")
    return S_OK()

  def setSplitEvents(self, eventsPerJob=None, numberOfJobs=None, totalNumberOfEvents=None):
    """Set up to run a given number of jobs producing a certain number of events.

    Example usage:

    >>> job = UserJob()
    >>> job.setSplitEvents(numberOfJobs=42, totalNumberOfEvents=126)

    Exactly two of the parmeters should be set

    :param int eventsPerJob: The events processed by a single job
    :param int numberOfJobs: The number of jobs
    :param int totalNumberOfEvents: The total number of events processed by all jobs

    .. note::

       This functionality is meant to simulate particle guns or for running MC
       generators, where the only parameter that change are the random seed and
       the output filename.
    """
    self._totalNumberOfEvents = totalNumberOfEvents
    self._eventsPerJob = eventsPerJob
    self._numberOfJobs = numberOfJobs

    self._addParameter(self.workflow, 'NbOfEvts', 'JDL', -1, 'Number of Events')

    self._splittingOption = "byEvents"

  def setSplitInputData(self, lfns, numberOfFilesPerJob=1):
    """Set up to run over a list of input files.

    Example usage:

    >>> job = UserJob()
    >>> job.setSplitInputData(listOfLFNs, numberOfFilesPerJob=10)

    :param lfns: Logical File Names
    :type lfns: list(str)
    :param int numberOfFilesPerJob: The number of input data processed by a single job
    """
    self._data = lfns if isinstance(lfns, list) else [lfns]
    self._numberOfFilesPerJob = numberOfFilesPerJob

    self._splittingOption = 'byData'

  def setSplitFilesAcrossJobs(self, lfns, eventsPerFile, eventsPerJob):
    """Split a list of input files into many jobs per file.

    :param lfns: Logical File Names
    :type lfns: list(str)
    :param int eventsPerFile: number of evenst in each file
    :param int eventsPerJob: number of events in each job. There will be eventsPerFile/eventsPerJob jobs for each file
    """
    self._data = lfns if isinstance(lfns, list) else [lfns]
    self._eventsPerFile = eventsPerFile
    self._eventsPerJob = eventsPerJob
    self._splittingOption = 'bySkip'
    self._addParameter(self.workflow, 'NbOfEvts', 'JDL', -1, 'Number of Events')

  def setSplitDoNotAlterOutputFilename(self, value=True):
    """Disable the changing the output filename for jobs with splitting.

    If this option is set the output data lfns will _not_ include the JobIndex

    :param bool value: if *True* disable the changing of the output data
        filenames. If *False* the JobIndex will be added at the end of
        OutputData LFNs before the extension. Or replace '%n' with the jobIndex
        in the fileName. See :func:`~ILCDIRAC.Core.Utilities.Splitting.addJobIndexToFilename`
    """
    self._addParameter(self.workflow, 'DoNotAlterOutputData', 'JDL', value, 'Do Not Change Output Data')

  def _split(self):
    """Check the consistency of the job and call the right split method.

    :return: The success or the failure of the consistency checking, :func`~DIRAC.Core.Utilities.ReturnValues.S_OK`, :func:`~DIRAC.Core.Utilities.ReturnValues.S_ERROR`
    """
    LOG.notice("Job splitting...")

    self._eventsPerJob = toInt(self._eventsPerJob, cond=lambda x: x >= 0)
    self._numberOfJobs = toInt(self._numberOfJobs, cond=lambda x: x >= 0)

    if self._numberOfJobs is False or self._eventsPerJob is False:
      return self._reportError("Splitting: Invalid values for splitting: %s, %s" %
                               (self._eventsPerJob, self._numberOfJobs))

    resCheck = self._checkSplitConsistency()
    if not resCheck['OK']:
      return resCheck

    sequences = self._switch.get(self._splittingOption, lambda: [])()
    sequenceLength = 0
    for sequenceType, sequenceList, addToWorkflow in sequences:
      LOG.debug("Adding sequence %s %s" % (sequenceType, addToWorkflow))
      self.setParameterSequence(sequenceType, sequenceList, addToWorkflow)
      sequenceLength = len(sequenceList)

    if sequences:
      LOG.debug("Adding jobIndexList")
      if not self._jobIndexList:
        self._jobIndexList = list(range(self._startJobIndex, sequenceLength + self._startJobIndex))
      if sequenceLength != len(self._jobIndexList):
        return self._reportError("JobIndexList (length=%s) does not have the correct length of %s" %
                                 (len(self._jobIndexList), sequenceLength))
      self.setParameterSequence('JobIndexList', self._jobIndexList, addToWorkflow='JobIndex')
      self._addParameter(self.workflow, 'JobIndex', 'int', self._startJobIndex, 'JobIndex')

    LOG.notice("Job splitting successful")

    return S_OK()

  def _splitByData(self):
    """Split into one job per input file.

    :return: parameter name and parameter values for setParameterSequence()
    :rtype: list(tuple(str, list, bool/str))
    """
    # reset split attribute to avoid infinite loop
    self._splittingOption = None

    LOG.notice("Job splitting: Splitting 'byData' method...")

    # Ensure that data have been specified by setInputData() method
    if not self._data:
      self._reportError("Job splitting: missing input data")
      return []

    if self._numberOfFilesPerJob > len(self._data):
      self._reportError("'numberOfFilesPerJob' must be less/equal than the number of input data")
      return []

    data = breakListIntoChunks(self._data, self._numberOfFilesPerJob)

    LOG.notice('Job splitting: submission consists of %d job(s)' % len(data))

    return [('InputData', data, 'ParametricInputData')]

  def _splitByEvents(self):
    """Split into job per subset of events.

    :return: parameter name and parameter values for setParameterSequence()
    :rtype: list(tuple(str, list, bool/str))
    """
    # reset split attribute to avoid infinite loop
    self._splittingOption = None

    LOG.notice("Job splitting: splitting 'byEvents' method...")

    if self._eventsPerJob and self._numberOfJobs:
      # 1st case: (numberOfJobs=3, eventsPerJob=10)
      # trivial case => each job (total of 3) run applications of 10 events each
      LOG.debug("Job splitting: events per job and number of jobs")

      mapEventJob = [self._eventsPerJob] * self._numberOfJobs

    elif self._eventsPerJob and self._totalNumberOfEvents:
      # 2nd case: (split="byEvents", eventsPerJob=10, totalNumberOfEvents=10)
      # Given the number of events per job and total of number of event we want,
      # we can compute the unknown which is the number of jobs.

      LOG.debug("Job splitting: Events per job and total number of events")

      if self._eventsPerJob > self._totalNumberOfEvents:
        self._reportError("Job splitting: The number of events per job has to be lower than or equal"
                          "to the total number of events")
        return []

      numberOfJobsIntDiv = self._totalNumberOfEvents // self._eventsPerJob
      numberOfJobsRest = self._totalNumberOfEvents % self._eventsPerJob

      mapEventJob = [self._eventsPerJob] * numberOfJobsIntDiv

      mapEventJob += [numberOfJobsRest] if numberOfJobsRest != 0 else []

    else:

      # 3rd case: (split='byEvents', njobs=10, totalNumberOfEvents=10)
      # Then compute the right number of events per job
      LOG.debug("Job splitting: The number of jobs and the total number of events")

      if (not self._totalNumberOfEvents) or (self._totalNumberOfEvents < self._numberOfJobs):
        self._reportError("Job splitting: The number of events has to be greater than or equal to the number of jobs")
        return []

      eventPerJobIntDiv = self._totalNumberOfEvents // self._numberOfJobs
      eventPerJobRest = self._totalNumberOfEvents % self._numberOfJobs

      mapEventJob = [eventPerJobIntDiv] * self._numberOfJobs

      if eventPerJobRest != 0:
        for suplement in range(eventPerJobRest):
          mapEventJob[suplement] += 1

    LOG.debug("Job splitting: events over the jobs: %s" % mapEventJob)
    LOG.notice("Job splitting: submission consists of %d job(s)" % len(mapEventJob))

    return [('NumberOfEvents', mapEventJob, 'NbOfEvts')]

  def _splitBySkip(self):
    """Split the input data over many jobs per file."""
    lfns = self._data
    eventsPerFile = self._eventsPerFile
    eventsPerJob = self._eventsPerJob
    jobsPerFile = eventsPerFile // eventsPerJob
    remainder = eventsPerFile % eventsPerJob
    if remainder > 0:
      jobsPerFile += 1
    # we only need to split for the first application, the rest picks it up from there...
    # we have to set the inputData, startFrom and numberOfEvents parameter for each input data
    inputDataList = []
    startFromList = []
    nEventsList = []
    for lfn in lfns:
      inputDataList.extend([lfn] * jobsPerFile)
      startFromList.extend(list(range(0, eventsPerFile, eventsPerJob)))
      nEventsList.extend([eventsPerJob] * jobsPerFile)
      if remainder > 0:
        nEventsList[-1] = remainder

    self._numberOfJobs = len(inputDataList)

    LOG.notice("Job splitting: submission consists of %d job(s)" % self._numberOfJobs)

    return [('InputData', inputDataList, 'InputData'),
            ('startFrom', startFromList, 'startFrom'),
            ('NumberOfEvents', nEventsList, 'NbOfEvts'),
            ]

  def setSplittingStartIndex(self, start):
    """Set the initial job index for the JobIndex parameter used to define the output file name index.

    :param int start: value where to start from, must be positive integer
    :returns: S_OK, S_ERROR
    """
    start = toInt(start, cond=lambda x: x > 0)
    if not start:
      return self._reportError("Start Index must be positive integer")
    self._startJobIndex = start
    return S_OK()

  def setSplitJobIndexList(self, jobIndexList):
    """Set the list of job indices to use.

    Define the list of indices to use to name output files. By default numbers from *0* to *n* are used.
    This function should be used when rerunning a select sample of input files for example.

    The length of the list must be as long as the number of jobs.

    See also :func:`setSplittingStartIndex`

    :param list jobIndexList: list of job indices
    """
    self._checkArgs({'jobIndexList': list})
    self._jobIndexList = list(jobIndexList)
    return S_OK()

  def setSplitOutputData(self, listOfOutputFiles, OutputPath='', OutputSE=''):
    """Set the list of output file names.

    :param list listOfOutputFiles: list of strings or list of list to set the output files for each split job.
    :param str OutputPath: Optional parameter to specify the Path in the Storage, postpended to /ilc/user/u/username/
    :param OutputSE: Optional parameter to specify the Storage Element to store data or files, e.g. CERN-SRM
    :type OutputSE: `python:list` or `str`
    """
    self._checkArgs({'listOfOutputFiles': list})
    self.setOutputData('PARAMETRIC_OUTPUT', OutputPath, OutputSE)
    self.setParameterSequence('OutputDataSplit', listOfOutputFiles, addToWorkflow='UserOutputData')

  def setSplitParameter(self, parameterName, listOfValues):
    """Set a list of parameter values that can be used to replace a named placeholder in application parameters.

    This only works for application parameters, not for job parameters, and at the moment only for string types.

    For example::

      outputFiles = ['electron.slcio', 'muon.slcio', 'pion.slcio']
      particles = ['e-', 'mu-', 'pi-']
      job = UserJob()
      job.setSplitDoNotAlterOutputFilename()
      job.setName('DDSimTest_%n')
      job.setSplitParameter('particle', particles)
      job.setSplitParameter('outputFile', outputFiles)
      job.setSplitOutputData(outputFiles, 'test/ddsim', 'CERN-DST-EOS')
      job.setOutputSandbox('*.log')
      ddsim = DDSim()
      ddsim.setVersion('ILCSoft-2018-08-10_gcc62')
      ddsim.setDetectorModel('CLIC_o3_v14')

      # the named placeholder '%(particle)s' has the same name as the first argument of setSplitParameter
      ddsim.setExtraCLIArguments('--gun.particle=%(particle)s')
      ddsim.setOutputFile('%(outputFile)s.slcio')

    :param str parameterName: name of the parameter and the placeholder
    :param list listOfValues: the list of values to be used, one per job
    """
    self.setParameterSequence(parameterName + 's', listOfValues, addToWorkflow=parameterName)
    self._addParameter(self.workflow, parameterName, 'string', '', parameterName)
