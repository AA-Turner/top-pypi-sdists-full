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
"""Get the overlay files.

:since: Jan 27, 2011

:author: sposs
"""

from __future__ import print_function
from __future__ import absolute_import
import glob
import os
import random
import subprocess
import time
from math import ceil, pi, sin, cos

import DIRAC
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.DataManagementSystem.Utilities.DMSHelpers import DMSHelpers
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.Resources.Storage.StorageElement import StorageElement
from DIRAC.Core.Utilities.ReturnValues import returnSingleResult
from DIRAC.Core.Utilities.Subprocess import shellCall
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.ConfigurationSystem.Client.Helpers.Resources import getSites, getSitePath
from DIRAC import S_OK, S_ERROR, gLogger, gConfig

from ILCDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from ILCDIRAC.Core.Utilities.WasteCPU import wasteCPUCycles
from ILCDIRAC.Core.Utilities.OverlayFiles import energyWithLowerCaseUnit
from ILCDIRAC.Core.Utilities.Configuration import getOptionValue
from ILCDIRAC.Core.Utilities.InputFilesUtilities import getNumberOfEvents
from ILCDIRAC.OverlaySystem.Client.OverlaySystemClient import OverlaySystemClient
from six.moves import zip

__RCSID__ = '$Id$'
LOG = gLogger.getSubLogger(__name__)


def allowedBkg(bkg, energy=None, detector=None, detectormodel=None, machine='clic_cdr'):
  """Check is supplied bkg is allowed."""
  #gLogger.info("Those are the arguments: %s, %s, %s, %s, %s" % (bkg, energy, detector, detectormodel, machine) )
  ops = Operations()
  #bkg_allowed = [ 'gghad', 'pairs' ]
  # if not bkg in bkg_allowed:
  #  return S_ERROR( "Bkg not allowed" )
  res = -1
  if energy:
    if detectormodel:
      res = ops.getValue("/Overlay/%s/%s/%s/%s/ProdID" % (machine, energy, detectormodel, bkg), -1)
      if res < 0:
        return S_ERROR("No background to overlay")
    if detector:  # needed for backward compatibility
      res = ops.getValue("/Overlay/%s/%s/%s/%s/ProdID" % (machine, detector, energy, bkg), -1)
      if res < 0:
        return S_ERROR("No background to overlay")
  return S_OK(res)


class OverlayInput (ModuleBase):
  """Download the files for overlay."""

  def __init__(self):
    super(OverlayInput, self).__init__()
    self.enable = True
    self.STEP_NUMBER = ''
    self.applicationName = 'OverlayInput'
    self.curdir = os.getcwd()
    self.applicationLog = ''
    self.printoutflag = ''
    self.prodid = 0
    self.detector = ''  # needed for backward compatibility
    self.detectormodel = ""
    self.energytouse = ''
    self.energy = 0
    self.nbofeventsperfile = 100
    self.lfns = []
    self.nbfilestoget = 0
    self.BkgEvtType = 'gghad'
    self.metaEventType = self.BkgEvtType
    self.BXOverlay = 0
    self.ggtohadint = 3.2
    self.nbsigeventsperfile = 0
    self.nbinputsigfile = 1
    self.NbSigEvtsPerJob = 0
    self.datMan = DataManager()
    self.fcc = FileCatalogClient()
    self.site = DIRAC.siteName()
    self.useEnergyForFileLookup = True
    self.machine = 'clic_cdr'
    self.pathToOverlayFiles = ''
    self.processorName = ''

    self._dmshelpers = DMSHelpers()

  def applicationSpecificInputs(self):

    self.pathToOverlayFiles = self.step_commons.get("pathToOverlayFiles", self.pathToOverlayFiles)

    if 'Detector' in self.step_commons:
      self.detectormodel = self.step_commons['Detector']
    if not self.detectormodel and not self.detector and not self.pathToOverlayFiles:
      return S_ERROR('Detector model not defined')

    if 'Energy' in self.step_commons:
      self.energytouse = self.step_commons['Energy']

    if self.energy:
      self.energytouse = energyWithLowerCaseUnit(self.energy)

    if not self.energytouse and not self.pathToOverlayFiles:
      return S_ERROR("Energy not set anywhere!")

    if 'BXOverlay' in self.step_commons:
      self.BXOverlay = self.step_commons['BXOverlay']
    if not self.BXOverlay:
      return S_ERROR("BXOverlay parameter not defined")

    if 'ggtohadint' in self.step_commons:
      self.ggtohadint = self.step_commons['ggtohadint']

    if 'ProdID' in self.step_commons:
      self.prodid = self.step_commons['ProdID']

    if 'NbSigEvtsPerJob' in self.step_commons:
      self.NbSigEvtsPerJob = self.step_commons['NbSigEvtsPerJob']

    if 'BkgEvtType' in self.step_commons:
      self.BkgEvtType = self.step_commons['BkgEvtType']
    self.metaEventType = self.BkgEvtType

    res = allowedBkg(self.BkgEvtType, self.energytouse, detector=self.detector,
                      detectormodel=self.detectormodel, machine=self.machine)
    if not res['OK']:
      return res
    if res['Value'] < 0 and not self.pathToOverlayFiles:
      return S_ERROR("No suitable ProdID")
    # if 'Site' in self.workflow_commons:
    #  self.site = self.workflow_commons['Site']

    self.useEnergyForFileLookup = self.step_commons.get("useEnergyForFileLookup", self.useEnergyForFileLookup)

    if self.InputData:
      if self.NumberOfEvents:
        self.nbsigeventsperfile = self.NumberOfEvents
      else:
        return S_ERROR("Number of events in the signal file is missing")
      self.nbinputsigfile = len(self.InputData)

    LOG.info("Signal Events Per Job: %d " % self.NbSigEvtsPerJob)
    LOG.info("Background Event Type: %s " % self.BkgEvtType)
    LOG.info("Meta Event Type: %s " % self.metaEventType)
    LOG.info("Background Events per bunch crossing: %3.2f" % self.ggtohadint)
    LOG.info("SignalEventsPerFile: %d " % self.nbsigeventsperfile)

    if not self.NbSigEvtsPerJob and not self.nbsigeventsperfile:
      return S_ERROR("Could not determine the number of signal events per input file")
    return S_OK("Input variables resolved")

  def __getFilesFromFC(self):
    """Get the list of files from the FileCatalog."""
    meta = {}
    if self.energy and self.useEnergyForFileLookup:
      meta['Energy'] = str(int(self.energy))
    meta['EvtType'] = self.BkgEvtType
    meta['Datatype'] = 'SIM'
    if self.detectormodel:
      meta['DetectorModel'] = self.detectormodel
    if self.machine == 'ilc_dbd':
      meta['Machine'] = 'ilc'
    if self.machine == 'clic_cdr':
      meta['Machine'] = 'clic'
    res = None
    if self.detector:
      res = self.ops.getValue("/Overlay/%s/%s/%s/%s/ProdID" % (self.machine, self.detector,
                                                               self.energytouse, self.BkgEvtType), 0)
      self.nbofeventsperfile = self.ops.getValue("/Overlay/%s/%s/%s/%s/NbEvts" % (self.machine,
                                                                                  self.energytouse,
                                                                                  self.detector,
                                                                                  self.BkgEvtType),
                                                 100)

      self.metaEventType = self.ops.getValue("/Overlay/%s/%s/%s/%s/EvtType" % (self.machine,
                                                                                 self.energytouse,
                                                                                 self.detector,
                                                                                 self.BkgEvtType),
                                              self.BkgEvtType)

    else:
      res = self.ops.getValue("/Overlay/%s/%s/%s/%s/ProdID" % (self.machine,
                                                               self.energytouse,
                                                               self.detectormodel,
                                                               self.BkgEvtType),
                              0)
      self.nbofeventsperfile = self.ops.getValue("/Overlay/%s/%s/%s/%s/NbEvts" % (self.machine,
                                                                                  self.energytouse,
                                                                                  self.detectormodel,
                                                                                  self.BkgEvtType),
                                                 100)
      self.metaEventType = self.ops.getValue("/Overlay/%s/%s/%s/%s/EvtType" % (self.machine,
                                                                                 self.energytouse,
                                                                                 self.detectormodel,
                                                                                 self.BkgEvtType),
                                              self.BkgEvtType)

    LOG.info("Number of Events Per BackgroundFile: %d " % self.nbofeventsperfile)

    meta['EvtType'] = self.metaEventType
    meta['ProdID'] = res
    if self.prodid:
      meta['ProdID'] = self.prodid
    LOG.info("Using %s as metadata" % (meta))

    return self.fcc.findFilesByMetadata(meta)

  def __getFilesFromPath(self):
    """Get the list of files from the FileCatalog via the user specified path."""
    meta = {}
    listOfFiles = self.fcc.findFilesByMetadata(meta, self.pathToOverlayFiles)
    if not listOfFiles['OK']:
      return listOfFiles

    # find the number of events from the metadata
    resNE = getNumberOfEvents(listOfFiles['Value'][:1])
    if resNE['OK']:
      self.nbofeventsperfile = int(resNE.get('Value', {}).get('nbevts', self.nbofeventsperfile))
      LOG.info("Number of Events Per BackgroundFile: %d " % self.nbofeventsperfile)
    else:
      LOG.warn('Failed to find the number of events:', resNE['Message'])
      LOG.warn("Using Default number of Events Per BackgroundFile: %d " % self.nbofeventsperfile)

    return listOfFiles

  def __getFilesFromLyon(self, meta):
    """List the files present at Lyon, not used."""
    prodID = meta['ProdID']
    prod = str(prodID).zfill(8)
    energy = meta['Energy']
    bkg = meta["EvtType"]
    detector = meta["DetectorType"]
    path = "/ilc/prod/clic/%s/%s/%s/SIM/%s/" % (energy, bkg, detector, prod)
    comm = ["nsls", "%s" % path]
    res = subprocess.Popen(comm, stdout=subprocess.PIPE).communicate()
    dirlist = res[0].rstrip().split("\n")
    mylist = []
    for mydir in dirlist:
      if mydir.count("dirac_directory"):
        continue
      curdir = path + mydir
      comm2 = ["nsls", curdir]
      res = subprocess.Popen(comm2, stdout=subprocess.PIPE).communicate()
      for oFile in res[0].rstrip().split("\n"):
        if oFile.count("dirac_directory"):
          continue
        mylist.append(path + mydir + "/" + oFile)
    if not mylist:
      return S_ERROR("File list is empty")
    return S_OK(mylist)

  def __getFilesFromCastor(self, meta):
    """Get the available files (list) from the CERN castor storage."""
    prodID = meta['ProdID']
    prod = str(prodID).zfill(8)
    energy = meta['Energy']
    bkg = meta["EvtType"]
    detector = meta["DetectorType"]
    path = "/castor/cern.ch/grid/ilc/prod/%s/%s/%s/%s/SIM/%s/" % (self.machine, energy, bkg, detector, prod)
    comm = ["nsls", "%s" % path]
    res = subprocess.Popen(comm, stdout=subprocess.PIPE).communicate()
    dirlist = res[0].rstrip().split("\n")
    mylist = []
    for mydir in dirlist:
      if mydir.count("dirac_directory"):
        continue
      curdir = path + mydir
      comm2 = ["nsls", curdir]
      res = subprocess.Popen(comm2, stdout=subprocess.PIPE).communicate()
      for oFile in res[0].rstrip().split("\n"):
        if oFile.count("dirac_directory"):
          continue
        mylist.append(path + mydir + "/" + oFile)
    if not mylist:
      return S_ERROR("File list is empty")
    return S_OK(mylist)

  def __getFilesLocaly(self):
    """Download the files."""
    numberofeventstoget = ceil(self.BXOverlay * self.ggtohadint)
    nbfiles = len(self.lfns)
    availableevents = nbfiles * self.nbofeventsperfile
    if availableevents < numberofeventstoget:
      return S_ERROR("Number of %s events available is less than requested" % (self.BkgEvtType))

    if not self.NbSigEvtsPerJob:
      # Compute Nsignal events
      self.NbSigEvtsPerJob = self.nbinputsigfile * self.nbsigeventsperfile
    if not self.NbSigEvtsPerJob:
      return S_ERROR('Could not determine the number of signal events per job')
    LOG.verbose("There are %s signal event" % self.NbSigEvtsPerJob)
    # Now determine how many files are needed to cover all signal events
    totnboffilestoget = int(ceil(self.NbSigEvtsPerJob * numberofeventstoget / self.nbofeventsperfile))

    # Limit ourself to some configuration maximum
    levels = [self.machine, self.energytouse, self.detectormodel, self.BkgEvtType]
    maxNbFilesToGet = getOptionValue(ops=self.ops, basePath="/Overlay", optionName="MaxNbFilesToGet", defaultValue=20,
                                     levels=levels)

    if totnboffilestoget > maxNbFilesToGet:
      totnboffilestoget = maxNbFilesToGet

    self.__disableWatchDog()
    overlaymon = OverlaySystemClient()
    # Now need to check that there are not that many concurrent jobs getting the overlay at the same time
    error_count = 0
    count = 0
    while True:
      if error_count > 10:
        LOG.error('OverlayDB returned too many errors')
        return S_ERROR('Failed to get number of concurrent overlay jobs')

      res = overlaymon.canRun(self.site)
      if not res['OK']:
        error_count += 1
        time.sleep(60)
        continue
      error_count = 0
      # if running < max_concurrent_running:
      if res['Value']:
        break
      else:
        count += 1
        if count > 300:
          return S_ERROR("Waited too long: 5h, so marking job as failed")
        if count % 10 == 0:
          self.setApplicationStatus("Overlay standby number %s" % count)
        time.sleep(60)

    self.__enableWatchDog()

    self.setApplicationStatus('Getting overlay files')

    LOG.info('Will obtain %s files for overlay' % totnboffilestoget)

    os.mkdir("./overlayinput_" + self.metaEventType)
    os.chdir("./overlayinput_" + self.metaEventType)
    filesobtained = []
    usednumbers = []
    fail = False
    fail_count = 0

    max_fail_allowed = self.ops.getValue("/Overlay/MaxFailedAllowed", 20)
    while not len(filesobtained) == totnboffilestoget:
      if fail_count > max_fail_allowed:
        LOG.error('Reached the max fail count')
        fail = True
        break

      fileindex = random.randrange(nbfiles)
      if fileindex in usednumbers:
        LOG.info('File index is already used, re-try')
        continue

      usednumbers.append(fileindex)

      res = S_ERROR('Have not tried anything yet')
      if self.site == 'LCG.CERN.ch':
        res = self.getEOSFile(self.lfns[fileindex])
      elif self.site == 'LCG.IN2P3-CC.fr':
        res = self.getLyonFile(self.lfns[fileindex])
      elif self.site == 'LCG.UKI-LT2-IC-HEP.uk':
        res = self.getImperialFile(self.lfns[fileindex])
      elif self.site == 'LCG.RAL-LCG2.uk':
        res = self.getRALFile(self.lfns[fileindex])
      elif self.site == 'LCG.KEK.jp':
        res = self.getKEKFile(self.lfns[fileindex])

      # In case the specific copying did not work (mostly because the files do
      # not exist locally) try again to get the file via the DataManager
      if not res['OK']:
        res = self.getDataManagerFile(self.lfns[fileindex])

      if not res['OK']:
        LOG.warn('Could not obtain %s' % self.lfns[fileindex])
        fail_count += 1
        # Wait for a random time around 3 minutes
        LOG.verbose("Waste happily some CPU time (on average 3 minutes)")
        resWaste = wasteCPUCycles(60 * random.gauss(3, 0.1))
        if not resWaste['OK']:
          LOG.error("Could not waste as much CPU time as wanted, but whatever!")
        continue

      filesobtained.append(self.lfns[fileindex])

    # If no file could be obtained, need to make sure the job fails
    if len(usednumbers) == nbfiles and not filesobtained:
      LOG.error('Could not get all the files needed')
      fail = True

    # Remove all scripts remaining
    scripts = glob.glob("*.sh")
    for script in scripts:
      os.remove(script)

    # Print the file list
    mylist = os.listdir(os.getcwd())
    LOG.info("List of Overlay files:")
    LOG.info("\n".join(mylist))
    os.chdir(self.curdir)
    res = overlaymon.jobDone(self.site)
    if not res['OK']:
      LOG.error("Could not declare the job as finished getting the files")
    if fail:
      LOG.error("Did not manage to get all files needed, too many errors")
      return S_ERROR("Failed to get files")
    LOG.info('Got all files needed.')
    return S_OK()

  def getCASTORFile(self, lfn):
    """Use xrdcp or rfcp to get the files from castor."""
    prependpath = "/castor/cern.ch/grid"
    if not lfn.count("castor/cern.ch"):
      lfile = prependpath + lfn
    else:
      lfile = lfn
    LOG.info("Getting %s" % lfile)
    #command = "rfcp %s ./"%file

    basename = os.path.basename(lfile)

    if os.path.exists("overlayinput.sh"):
      os.unlink("overlayinput.sh")
    with open("overlayinput.sh", "w") as script:
      script.write('#!/bin/sh \n')
      script.write('###############################\n')
      script.write('# Dynamically generated scrip #\n')
      script.write('###############################\n')
      if 'X509_USER_PROXY' in os.environ:
        script.write("cp %s /tmp/x509up_u%s \n" % (os.environ['X509_USER_PROXY'], os.getuid()))
      script.write('declare -x STAGE_SVCCLASS=ilcdata\n')
      script.write('declare -x STAGE_HOST=castorpublic\n')
      script.write(
          r"xrdcp -s root://castorpublic.cern.ch/%s ./ -OSstagerHost=castorpublic\&svcClass=ilcdata\n" %
          lfile.rstrip())
      #script.write("/usr/bin/rfcp 'rfio://cgenstager.ads.rl.ac.uk:9002?svcClass=ilcTape&path=%s' %s\n"%(lfile,basename))
      script.write("""
if [ ! -s %s ]; then
  echo "Using rfcp instead"
  rfcp %s ./
fi\n""" % (basename, lfile))
      script.write('declare -x appstatus=$?\n')
      script.write('exit $appstatus\n')
    os.chmod("overlayinput.sh", 0o755)
    comm = 'sh -c "./overlayinput.sh"'
    self.result = shellCall(600, comm, callbackFunction=self.redirectLogOutput, bufferLimit=20971520)

    localfile = os.path.basename(lfile)
    if os.path.exists(localfile):
      return S_OK(localfile)

    return S_ERROR("Failed")

  def getEOSFile(self, lfn):
    """Use xrdcp to get the files from EOS."""
    prependpath = "/eos/experiment/clicdp/grid"
    if not lfn.startswith(prependpath):
      lfile = prependpath + lfn
    else:
      lfile = lfn
    LOG.info('Getting File from CERN-EOS', lfile)

    if os.path.exists("overlayinput.sh"):
      os.unlink("overlayinput.sh")
    with open("overlayinput.sh", "w") as script:
      script.write('#!/bin/sh \n')
      script.write('################################\n')
      script.write('# Dynamically generated script #\n')
      script.write('################################\n')
      if 'X509_USER_PROXY' in os.environ:
        script.write("cp %s /tmp/x509up_u%s \n" % (os.environ['X509_USER_PROXY'], os.getuid()))
      script.write("xrdcp -s root://eospublic.cern.ch/%s ./ \n" % lfile.rstrip())
      script.write('declare -x appstatus=$?\n')
      script.write('exit $appstatus\n')
    os.chmod("overlayinput.sh", 0o755)
    comm = 'sh -c "./overlayinput.sh"'
    self.result = shellCall(600, comm, callbackFunction=self.redirectLogOutput, bufferLimit=20971520)

    localfile = os.path.basename(lfile)
    if os.path.exists(localfile):
      LOG.info('Successfully got file from CERN-EOS')
      return S_OK(localfile)

    return S_ERROR("Failed")

  def getLyonFile(self, lfn):
    """Use xrdcp to get the files from Lyon."""
    prependpath = '/pnfs/in2p3.fr/data'
    if not lfn.count('in2p3.fr/data'):
      lfile = prependpath + lfn
    else:
      lfile = lfn
    LOG.info('Getting file from LYON', lfile)
    #command = "rfcp %s ./"%file
    #comm = []
    #comm.append("cp $X509_USER_PROXY /tmp/x509up_u%s"%os.getuid())

    if os.path.exists("overlayinput.sh"):
      os.unlink("overlayinput.sh")
    with open("overlayinput.sh", "w") as script:
      script.write('#!/bin/sh \n')
      script.write('###############################\n')
      script.write('# Dynamically generated scrip #\n')
      script.write('###############################\n')
      script.write("cp %s /tmp/x509up_u%s \n" % (os.environ['X509_USER_PROXY'], os.getuid()))
      script.write(". /afs/in2p3.fr/grid/profiles/lcg_env.sh\n")
      script.write("xrdcp root://ccdcacsn179.in2p3.fr:1094%s ./ -s\n" % lfile.rstrip())
      #script.write("/usr/bin/rfcp 'rfio://cgenstager.ads.rl.ac.uk:9002?svcClass=ilcTape&path=%s' %s\n"%(lfile,basename))
      # script.write("""
# if [ ! -s %s ]; then
#  rfcp %s ./
# fi\n"""%(basename,lfile))
      script.write('declare -x appstatus=$?\n')
      script.write('exit $appstatus\n')
    os.chmod("overlayinput.sh", 0o755)
    comm = 'sh -c "./overlayinput.sh"'
    self.result = shellCall(600, comm, callbackFunction=self.redirectLogOutput, bufferLimit=20971520)

    localfile = os.path.basename(lfile)
    if os.path.exists(localfile):
      LOG.info('Successfully got file from LYON-SE')
      return S_OK(localfile)

    return S_ERROR("Failed")

  def getImperialFile(self, lfn):
    """Use dccp to get the files from the Imperial SE."""
    prependpath = '/pnfs/hep.ph.ic.ac.uk/data'
    if not lfn.count('hep.ph.ic.ac.uk/data'):
      lfile = prependpath + lfn
    else:
      lfile = lfn
    LOG.info('Getting file from IMPERIAL', lfile)
    # Don't check for CPU time as other wise, job can get killed
    self.__disableWatchDog()

    if os.path.exists("overlayinput.sh"):
      os.unlink("overlayinput.sh")
    with open("overlayinput.sh", "w") as script:
      script.write('#!/bin/sh \n')
      script.write('###############################\n')
      script.write('# Dynamically generated scrip #\n')
      script.write('###############################\n')
      script.write("dccp dcap://%s%s ./\n" % (os.environ['VO_ILC_DEFAULT_SE'], lfile.rstrip()))
      #script.write("/usr/bin/rfcp 'rfio://cgenstager.ads.rl.ac.uk:9002?svcClass=ilcTape&path=%s' %s\n"%(lfile,basename))
      # script.write("""
# if [ ! -s %s ]; then
#  rfcp %s ./
# fi\n"""%(basename,lfile))
      script.write('declare -x appstatus=$?\n')
      script.write('exit $appstatus\n')
    os.chmod("overlayinput.sh", 0o755)
    comm = 'sh -c "./overlayinput.sh"'
    self.result = shellCall(600, comm, callbackFunction=self.redirectLogOutput, bufferLimit=20971520)

    localfile = os.path.basename(lfile)
    if os.path.exists(localfile):
      LOG.info('Successfully got file from IMPERIAL')
      return S_OK(localfile)

    return S_ERROR("Failed")

  def getRALFile(self, lfn):
    """Use rfcp to get the files from RAL castor."""
    prependpath = '/castor/ads.rl.ac.uk/prod'
    if not lfn.count('ads.rl.ac.uk/prod'):
      lfile = prependpath + lfn
    else:
      lfile = lfn
    LOG.info('Getting file from RAL', lfile)
    # Don't check for CPU time as other wise, job can get killed
    self.__disableWatchDog()

    #command = "rfcp %s ./"%file
    #comm = []
    #comm.append("cp $X509_USER_PROXY /tmp/x509up_u%s"%os.getuid())
    if 'X509_USER_PROXY' in os.environ:
      comm2 = ["cp", os.environ['X509_USER_PROXY'], "/tmp/x509up_u%s" % os.getuid()]
      res = subprocess.Popen(comm2, stdout=subprocess.PIPE).communicate()
      print(res)
    #comm.append("xrdcp root://ccdcacsn179.in2p3.fr:1094%s ./ -s"%file)
    #command = string.join(comm,";")
    #logfile = file(self.applicationLog,"w")
    os.environ['CNS_HOST'] = 'castorns.ads.rl.ac.uk'
    #comm4= ['declare','-x','CNS_HOST=castorns.ads.rl.ac.uk']
    #res = subprocess.Popen(comm4,stdout=logfile,stderr=subprocess.STDOUT)
    #print res
    os.environ['STAGE_SVCCLASS'] = 'ilcTape'
#     comm5= ['declare','-x','STAGE_SVCCLASS=ilcTape']
#      res = subprocess.call(comm5)
#      print res
    os.environ['STAGE_HOST'] = 'cgenstager.ads.rl.ac.uk'
#      comm6=['declare','-x','STAGE_HOST=cgenstager.ads.rl.ac.uk']
#      res = subprocess.call(comm6)
#      print res
    basename = os.path.basename(lfile)

    if os.path.exists("overlayinput.sh"):
      os.unlink("overlayinput.sh")
    with open("overlayinput.sh", "w") as script:
      script.write('#!/bin/sh \n')
      script.write('###############################\n')
      script.write('# Dynamically generated scrip #\n')
      script.write('###############################\n')
      script.write(
          "/usr/bin/rfcp 'rfio://cgenstager.ads.rl.ac.uk:9002?svcClass=ilcTape&path=%s' %s\n" %
          (lfile, basename))
      script.write('declare -x appstatus=$?\n')
      script.write('exit $appstatus\n')
    os.chmod("overlayinput.sh", 0o755)
    comm = 'sh -c "./overlayinput.sh"'
    self.result = shellCall(600, comm, callbackFunction=self.redirectLogOutput, bufferLimit=20971520)

    localfile = os.path.basename(lfile)
    if os.path.exists(localfile):
      LOG.info('Successfully got file from RAL')
      return S_OK(localfile)

    return S_ERROR("Failed")

  def getKEKFile(self, lfn):
    """Use cp to get the files from kek-se."""
    prependpath = '/grid'
    lfile = prependpath + lfn
    LOG.info('Getting file from KEK', lfile)
    self.__disableWatchDog()

    if os.path.exists("overlayinput.sh"):
      os.unlink("overlayinput.sh")
    with open("overlayinput.sh", "w") as script:
      script.write('#!/bin/sh \n')
      script.write('###############################\n')
      script.write('# Dynamically generated scrip #\n')
      script.write('###############################\n')
      script.write("cp %s ./ -s\n" % lfile.rstrip())
      script.write('declare -x appstatus=$?\n')
      script.write('exit $appstatus\n')

    os.chmod("overlayinput.sh", 0o755)
    comm = 'sh -c "./overlayinput.sh"'
    self.result = shellCall(600, comm, callbackFunction=self.redirectLogOutput, bufferLimit=20971520)

    localfile = os.path.basename(lfile)
    if os.path.exists(localfile):
      LOG.info('Successfully got file from KEK')
      return S_OK(localfile)

    return S_ERROR("Failed")

  def getDataManagerFile(self, lfn):
    """Try to download the file via the DataManager.

    First get the available SEs, then sort them by distance to the Site, then try each SE in turn.

    :param str lfn: the lfn to download
    :return: S_OK/S_ERROR
    """
    self.__disableWatchDog()
    resRepl = returnSingleResult(self.datMan.getActiveReplicas(lfn, getUrl=False))
    # value is a dictionary of {SE:true/false}
    if not resRepl['OK']:
      LOG.error('Failed to get active replicas', '%s: %s' % (lfn, resRepl['Message']))
      return resRepl
    availableAt = [se for se, active in resRepl['Value'].items() if active]
    LOG.info('The file is available at these SEs', '%s: %s' % (lfn, availableAt))
    LOG.info('Running at site', self.site)
    orderedSEs = sorted(availableAt, key=self.__distanceToSE)
    LOG.info('Ordered SEs', orderedSEs)
    for SE in orderedSEs:
      LOG.info('Trying to download from:', SE)
      res = returnSingleResult(self.datMan.getFile(lfn, sourceSE=SE))
      if res['OK']:
        LOG.info('Successfully downloaded')
        return res
      LOG.error('Failed to download from', '%s: %s' % (SE, res['Message']))
    return S_ERROR('Failed to get the file from any sourceSE')

  def execute(self):
    """Run the module, called rom Workflow."""
    self.result = self.resolveInputVariables()
    if not self.result['OK']:
      LOG.error("Failed to resolve input parameters:", self.result['Message'])
      return self.result

    LOG.info("Information after resolveInputVariables:")
    LOG.info("Signal Events Per Job: %d " % self.NbSigEvtsPerJob)
    LOG.info("Background Event Type: %s " % self.BkgEvtType)
    LOG.info("Meta Event Type: %s " % self.metaEventType)
    LOG.info("Background Events per bunch crossing: %3.2f" % self.ggtohadint)
    LOG.info("SignalEventsPerFile: %d " % self.nbsigeventsperfile)

    if not self.applicationLog:
      self.applicationLog = 'Overlay_input.log'
    self.applicationLog = os.path.join(os.getcwd(), self.applicationLog)

    if not self.workflowStatus['OK'] or not self.stepStatus['OK']:
      LOG.verbose('Workflow status = %s, step status = %s' % (self.workflowStatus['OK'], self.stepStatus['OK']))
      return S_OK('OverlayInput should not proceed as previous step did not end properly')
    self.setApplicationStatus('Starting up Overlay')

    if self.pathToOverlayFiles:
      res = self.__getFilesFromPath()
    else:
      res = self.__getFilesFromFC()

    if not res['OK']:
      LOG.error("Failed to get the file list from the catalog:", res["Message"])
      self.setApplicationStatus('OverlayProcessor failed to get file list')
      return res
    else:
      LOG.debug("Found these files: %s" % res)

    self.lfns = res['Value']
    if not self.lfns:
      LOG.error("No Overlay LFNs found")
      self.setApplicationStatus('OverlayProcessor got an empty list')
      return S_ERROR('OverlayProcessor got an empty list')

    res = self.__getFilesLocaly()
    # Now that module is finished,resume CPU time checks
    self.__enableWatchDog()

    if not res['OK']:
      LOG.error("Overlay failed with", res['Message'])
      self.setApplicationStatus('OverlayInput failed to get files locally with message %s' % res['Message'])
      return S_ERROR('OverlayInput failed to get files locally')
    self.setApplicationStatus('OverlayInput finished getting all files successfully')

    # add overlay background information to workflow_commons
    stepNumber = int(self.step_commons['STEP_NUMBER'])
    self.workflow_commons["OI_%i_eventType" % stepNumber] = self.metaEventType
    self.workflow_commons["OI_%i_eventsPerBackgroundFile" % stepNumber] = self.nbofeventsperfile
    self.workflow_commons["OI_%i_processorName" % stepNumber] = self.processorName

    # clear the StorageElementCache to clear sessions
    LOG.info('SEs cached now: %d' % len(StorageElement.seCache.getKeys()))
    StorageElement.seCache.purgeAll()
    LOG.info('SEs cached cleared: %d' % len(StorageElement.seCache.getKeys()))

    return S_OK('OverlayInput finished successfully')

  def __disableWatchDog(self):
    """create the watchdog disable if it does not exists."""
    watchDogFilename = 'DISABLE_WATCHDOG_CPU_WALLCLOCK_CHECK'
    fullPath = os.path.join(self.curdir, watchDogFilename)
    if not os.path.exists(fullPath):
      with open(fullPath, 'w') as checkFile:
        checkFile.write('Dont look at cpu')

  def __enableWatchDog(self):
    """remove the watchdog disable file if it exists."""
    watchDogFilename = 'DISABLE_WATCHDOG_CPU_WALLCLOCK_CHECK'
    fullPath = os.path.join(self.curdir, watchDogFilename)
    if os.path.exists(fullPath):
      os.remove(fullPath)

  def __getSELocation(self, SE):
    """Get the coordinates of the site.

    Using the country code we find all sites in the same country and from that obtain the
    coordinates in latitude and longitude.
    """
    try:
      countryCode = StorageElement(SE).storages[0].getParameters()['Host'].rsplit('.', 1)[-1]
    except Exception as e:
      LOG.error('Failed to instantiate SE', str(e))
      return [-180, -90.0]
    allSites = getSites()
    if not allSites['OK']:
      LOG.error('Could not get allSites', allSites['Message'])
      return [0.0, -90.0]
    allSites = [site for site in allSites['Value'] if site.rsplit('.', 1)[-1] == countryCode]
    LOG.debug('Found these sites in %s' % countryCode, allSites)
    coordinates = [self.__getSiteLocation(site) for site in allSites]
    LOG.debug('Coordinates found ', coordinates)
    averageCoordinates = [sum(y) / len(y) for y in zip(*coordinates)]
    LOG.debug('Avarage Location is', averageCoordinates)
    return averageCoordinates if averageCoordinates else [0.0, 0.0]

  def __getSiteLocation(self, site=None):
    """Return Coordinates of the site."""
    if site is None:
      site = self.site
    sitePath = getSitePath(site)
    if not sitePath['OK']:
      LOG.error('Could not get sitePath for', site + sitePath['Message'])
      return [0.0, 0.0]
    coordinates = gConfig.getValue(os.path.join(sitePath['Value'], 'Coordinates'), ('0.0:0.0')).split(':')
    return [float(coord) for coord in coordinates]

  def __distanceToSE(self, SE):
    """Calculate the distance from the current site to the given SE."""
    seLocation = self.__getSELocation(SE)
    t1 = pi / 2.0 + seLocation[1] * pi / 180.0
    p1 = seLocation[0] * pi / 180.0
    siteLocation = self.__getSiteLocation()
    t2 = pi / 2.0 + siteLocation[1] * pi / 180.0
    p2 = siteLocation[0] * pi / 180.0
    # we do not take the sqrt, because it does not matter for sorting
    distance = 2.0 - 2.0 * (sin(t1) * sin(t2) * cos(p1 - p2) + cos(t1) * cos(t2))
    LOG.debug('Distance found to %s: %s' % (SE, distance))
    return distance
