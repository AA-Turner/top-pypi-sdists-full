###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
:mod: SEUsageAgent

.. module: SEUsageAgent

:synopsis: SEUsageAgent browses the SEs to determine their content and store it into a DB.
"""
# # imports
import os
import time
import tarfile
import signal
from datetime import datetime
from urllib.request import urlopen
from urllib.error import HTTPError

# # from DIRAC
from DIRAC import S_OK, S_ERROR, rootPath, gConfig
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Core.Utilities.File import mkDir
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.Utilities.SiteSEMapping import getSEsForSite
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.Resources.Storage.StorageElement import StorageElement
from DIRAC.Interfaces.API.Dirac import Dirac

# # from LHCbDIRAC
from LHCbDIRAC.DataManagementSystem.Client.StorageUsageClient import StorageUsageClient
from LHCbDIRAC.DataManagementSystem.DB.StorageUsageDB import StorageUsageDB

AGENT_NAME = "DataManagement/SEUsageAgent"


def alarmTimeoutHandler(*args):
    """handler for signal.SIGALRM."""
    raise Exception("Timeout")


class SEUsageAgent(AgentModule):
    """..class:: SEUsageAgent

    :param mixed storageUsage: StorageUsageDB or StorageUsage client
    :param DataManager dataManager: DataManager instance
    :param Operations opHelper: operations helper
    :param int maximumDelaySinceSD: max delay after SE dump creation
    :param list activeSites: active sites
    """

    def __init__(self, *args, **kwargs):
        """c'tor."""
        AgentModule.__init__(self, *args, **kwargs)

        self.storageUsage = None
        self.dataManager = None
        self.opHelper = None
        self.diracApi = None

        self.activeSites = None

        self.specialReplicas = []
        self.workDirectory = ""
        # maximum delay after storage dump creation
        self.maximumDelaySinceSD = 43200
        self.spaceTokToIgnore = None  # STs to skip during checks
        self.pathToUploadResults = "/lhcb/test/dataNotRegistered"
        self.inputFilesLocation = ""
        self.spaceTokens = {}
        self.siteConfig = {}

    def initialize(self):
        """agent initialisation."""
        # This sets the Default Proxy to used as that defined under
        # /Operations/Shifter/DataManager
        # the shifterProxy option in the Configsorteduration can be used to change this default.
        self.am_setOption("shifterProxy", "DataManager")
        self.am_setModuleParam("shifterProxyLocation", f"{rootPath}/runit/{AGENT_NAME}/proxy")

        if self.am_getOption("DirectDB", False):
            self.storageUsage = StorageUsageDB()
        else:
            self.storageUsage = StorageUsageClient()
        # # replica mgr
        self.dataManager = DataManager()
        # # operations helper
        self.opHelper = Operations()
        # # Dirac API
        self.diracApi = Dirac()
        self.activeSites = self.am_getOption("ActiveSites", None)

        self.specialReplicas = self.am_getOption("SpecialReplicas", [])
        self.workDirectory = self.am_getOption("WorkDirectory", None)
        # maximum delay after storage dump creation
        self.maximumDelaySinceSD = self.am_getOption("MaximumDelaySinceStorageDump", 43200)
        self.spaceTokToIgnore = self.am_getOption("SpaceTokenToIgnore", None)  # STs to skip during checks
        self.pathToUploadResults = self.am_getOption("PathToUploadResults", "/lhcb/test/dataNotRegistered")

        mkDir(self.workDirectory)
        self.log.info(f"Working directory is {self.workDirectory}")
        self.inputFilesLocation = self.am_getOption("InputFilesLocation", "")
        mkDir(self.inputFilesLocation)
        self.log.info(f"Input files will be downloaded to: {self.inputFilesLocation}")
        # FIXME: totally useless
        if self.specialReplicas:
            self.log.info(f"Special replica types: {self.specialReplicas}")
        else:
            self.log.info("No special replica configured.")
        self.log.info(f"Path to upload results: {self.pathToUploadResults} ")
        return S_OK()

    def execute(self):
        """execution in one cycle.

        Loops on the input files to read the content of Storage Elements,
        process them, and store the result into the DB. It reads directory
        by directory (every row of the input file being a directory). If the
        directory exists in the StorageUsage su_Directory table, and if a
        replica also exists for the given SE in the su_SEUsage table, then
        the directory and its usage are stored in the replica table (the
        se_Usage table) together with the insertion time, otherwise it is
        added to the problematic data table (problematicDirs)
        """

        self.log.info("Starting the execute method")
        self.log.info(f"Sites active for checks: {self.activeSites} ")
        siteList = self.activeSites.split(",")
        timingPerSite = {}
        self.spaceTokens = {}
        self.siteConfig = {}
        siteList.sort()
        for lcgSite in siteList:
            site = lcgSite.split(".")[1]
            timingPerSite[site] = {}
            start = time.time()
            res = self.setupSiteConfig(lcgSite)
            if not res["OK"]:
                self.log.warn(f"Error during site configuration {res['Message']} ")
                continue

            self.log.info(f"Parse and read input files for site: {site}")
            res = self.readInputFile(site)
            if not res["OK"]:
                self.log.error(f"Failed to read input files for site {site} ")
                continue
            if res["Value"] < 0:
                self.log.warn(f"Input files read successfully, but not valid for checks (too old?). Skip site {site} ")
                continue

            # ONLY FOR DEBUGGING
            debug = False
            if debug:  # get the problematic summary at the beginning (to debug this part without waiting until the end)
                res = self.getProblematicDirsSummary(site)
                if not res["OK"]:
                    return S_ERROR(res["Message"])
            else:  # follow the usual work flow
                # Flush the problematicDirs table
                self.log.info(f"Flushing the problematic directories table for site {site}...")
                res = self.storageUsage.removeAllFromProblematicDirs(site)
                if not res["OK"]:
                    self.log.error(
                        "Error for site %s: Could not remove old entries from the problematicDirs table! %s:"
                        % (site, res["Message"])
                    )
                    continue
                self.log.info(
                    "Removed %d entries from the problematic directories table for site %s" % (res["Value"], site)
                )
            # END OF DEBUGGING MODIFICATION ###########

            # Start the main loop:
            # read all file of type directory summary for the given site:
            pathToSummary = self.siteConfig[site]["pathToInputFiles"]
            for fileP3 in os.listdir(pathToSummary):
                fullPathFileP3 = os.path.join(pathToSummary, fileP3)
                if "dirSummary" not in fileP3:
                    continue
                self.log.info(f"Start to scan file {fullPathFileP3}")
                for line in open(fullPathFileP3).readlines():
                    splitLine = line.split()
                    try:
                        spaceToken = splitLine[0]
                        storageDirPath = splitLine[1]
                        files = splitLine[2]
                        size = splitLine[3]
                    except IndexError:
                        self.log.error(f"ERROR in input data format. Line is: {line}")
                        continue
                    oneDirDict = {}
                    dirPath = storageDirPath
                    # specialRep = False
                    replicaType = "normal"
                    for sr in self.specialReplicas:
                        prefix = "/lhcb/" + sr
                        self.log.verbose(f"Trying to match prefix {prefix} ")
                        if prefix in dirPath:
                            # strip the initial prefix, to get the LFN as registered in the FC
                            dirPath = storageDirPath.split(prefix)[1]
                            replicaType = sr
                            self.log.info(f"prefix: {prefix} \n storageDirPath: {storageDirPath}\n dirPath: {dirPath}")
                            break
                    oneDirDict[dirPath] = {
                        "SpaceToken": spaceToken,
                        "Files": files,
                        "Size": size,
                        "Updated": "na",
                        "Site": site,
                        "ReplicaType": replicaType,
                    }
                    # the format of the entry to be processed must be a dictionary with LFN path as key
                    # use this format for consistency with already existing methods of StorageUsageDB
                    # which take in input a dictionary like this
                    self.log.info(f"Processing directory: {oneDirDict}")
                    # initialize the isRegistered flag. Change it according to the checks SE vs FC
                    # possible values of isRegistered flag are:
                    # NotRegisteredInFC: data not registered in FC
                    # RegisteredInFC: data correctly registered in FC
                    # MissingDataFromSE: the directory exists in the FC for that SE, but there is
                    # less data on the SE than what reported in the FC
                    isRegistered = False
                    lfcFiles = -1
                    lfcSize = -1
                    self.log.verbose(f"check if dirName exists in su_Directory: {dirPath}")
                    # select entries with that LFN path (no reference to a particular site in this query)
                    res = self.storageUsage.getIDs(oneDirDict)
                    if not res["OK"]:
                        self.log.warn(f"failed to get DID from StorageUsageDB.su_Directory table for dir: {dirPath} ")
                        continue
                    elif not res["Value"]:
                        self.log.info(
                            "NO LFN registered in the FC for the given path %s => insert the entry in the "
                            "problematicDirs table and delete this entry from the replicas table" % dirPath
                        )
                        isRegistered = "NotRegisteredInFC"
                    else:
                        value = res["Value"]
                        self.log.info(f"directory LFN is registered in the FC, output of getIDs is {value}")
                        for directory in value:
                            self.log.verbose("Path: %s su_Directory.DID %d" % (directory, value[directory]))
                        self.log.verbose("check if this particular replica is registered in the FC.")
                        res = self.storageUsage.getAllReplicasInFC(dirPath)
                        if not res["OK"]:
                            self.log.error(f"failed to get replicas for {dirPath} directory ")
                            continue
                        elif not res["Value"]:
                            self.log.warn(
                                "NO replica found for %s on any SE! Anomalous case: the LFN is registered in the FC"
                                "but with NO replica! For the time being, insert it into "
                                "problematicDirs table " % dirPath
                            )
                            # TODO: we should decide what to do in this case.
                            # This might happen, but it is a problem at FC level...
                            isRegistered = "NotRegisteredInFC"
                        else:  # got some replicas! let's see if there is one for this SE
                            associatedDiracSEs = self.spaceTokens[site][spaceToken]["DiracSEs"]
                            self.log.verbose(f"SpaceToken: {spaceToken} list of its DiracSEs: {associatedDiracSEs}")
                            lfcFiles = 0
                            lfcSize = 0
                            for lfn in res["Value"]:
                                matchedSE = ""
                                for se in res["Value"][lfn]:
                                    self.log.verbose(f"SpaceToken: {spaceToken} -- se: {se}")
                                    if se in associatedDiracSEs:
                                        # consider only the FC replicas of the corresponding Dirac SE
                                        if oneDirDict[dirPath]["ReplicaType"] in self.specialReplicas:
                                            self.log.info(f"SpecialReplica: {oneDirDict[dirPath]['ReplicaType']}")
                                            seSuffix = oneDirDict[dirPath]["ReplicaType"].upper()
                                            if seSuffix not in se:
                                                self.log.verbose(f"SE does not contain the suffix: {seSuffix}. Skip it")
                                                continue
                                        lfcFiles += int(res["Value"][lfn][se]["Files"])
                                        lfcSize += int(res["Value"][lfn][se]["Size"])
                                        self.log.info(f"==> the replica is registered in the FC with DiracSE= {se}")
                                        # this is because there can be DST and M-DST files in the same directory
                                        if not matchedSE:
                                            matchedSE = se
                                        else:
                                            matchedSE = matchedSE + ".and." + se
                            # check also whether the number of files and total directory size match:
                            seSize = int(oneDirDict[dirPath]["Size"])
                            seFiles = int(oneDirDict[dirPath]["Files"])
                            self.log.info(f"Matched SE: {matchedSE}")
                            oneDirDict[dirPath]["SEName"] = matchedSE
                            self.log.info(
                                "lfcFiles = %d lfcSize = %d seFiles = %d seSize = %d"
                                % (lfcFiles, lfcSize, seFiles, seSize)
                            )
                            if seSize > lfcSize:
                                self.log.info("Data on SE exceeds what reported in FC! some data not registered in FC")
                                isRegistered = "NotRegisteredInFC"
                            elif seSize < lfcSize:
                                self.log.info("Data on FC exceeds what reported by SE dump! missing data from storage")
                                isRegistered = "MissingDataFromSE"
                            elif lfcFiles == seFiles and lfcSize == seSize:
                                self.log.info("Number of files and total size matches with what reported by FC")
                                isRegistered = "RegisteredInFC"
                            else:
                                self.log.info("Unexpected case: seSize = lfcSize but seFiles != lfcFiles")
                                isRegistered = "InconsistentFilesSize"

                    self.log.info(f"isRegistered flag is {isRegistered}")
                    # now insert the entry into the problematicDirs table,
                    # or the replicas table according the isRegistered flag.
                    if not isRegistered:
                        self.log.error(f"the isRegistered flag could not be updated for this directory: {oneDirDict} ")
                        continue
                    if isRegistered in ("NotRegisteredInFC", "MissingDataFromSE", "InconsistentFilesSize"):
                        self.log.info(
                            "problematic directory! Add the entry %s to problematicDirs table. "
                            "Before (if necessary) remove it from se_Usage table" % (dirPath)
                        )
                        res = self.storageUsage.removeDirFromSe_Usage(oneDirDict)
                        if not res["OK"]:
                            self.log.error(f"failed to remove from se_Usage table: {res['Message']}")
                            continue
                        else:
                            removedDirs = res["Value"]
                            if removedDirs:
                                self.log.verbose(f"entry {oneDirDict} correctly removed from se_Usage table")
                            else:
                                self.log.verbose(f"entry {oneDirDict} was NOT in se_Usage table")
                            # update the oneDirDict and insert into problematicDirs
                            oneDirDict[dirPath]["Problem"] = isRegistered
                            oneDirDict[dirPath]["LFCFiles"] = lfcFiles
                            oneDirDict[dirPath]["LFCSize"] = lfcSize
                            res = self.storageUsage.publishToProblematicDirs(oneDirDict)
                            if not res["OK"]:
                                self.log.error(f"failed to publish entry {dirPath} to problematicDirs table")
                            else:
                                self.log.info(f"entry {oneDirDict} correctly published to problematicDirs table")
                    elif isRegistered == "RegisteredInFC":  # publish to se_Usage table!
                        self.log.verbose(
                            "replica %s is registered! remove from problematicDirs (if necessary) and "
                            " publish to se_Usage table" % dirPath
                        )
                        res = self.storageUsage.removeDirFromProblematicDirs(oneDirDict)
                        if not res["OK"]:
                            self.log.error(f"failed to remove from problematicDirs: {oneDirDict}")
                            continue
                        else:
                            removedDirs = res["Value"]
                            if removedDirs:
                                self.log.verbose(f"entry {oneDirDict} correctly removed from problematicDirs")
                            else:
                                self.log.verbose(f"entry {oneDirDict} was NOT in problematicDirs")
                            res = self.storageUsage.publishToSEReplicas(oneDirDict)
                            if not res["OK"]:
                                self.log.warn(f"failed to publish {oneDirDict} entry to se_Usage table")
                            else:
                                self.log.info(f"entry {oneDirDict} correctly published to se_Usage")
                    else:
                        self.log.error(f"Unknown value of isRegistered flag: {isRegistered} ")

                self.log.info(f"Finished loop on file: {fileP3} ")

            self.log.info(f"Finished loop for site: {site} ")
            # query problematicDirs table to get a summary of directories with the flag: NotRegisteredInFC
            self.log.info("Get the summary of problematic directories..")
            res = self.getProblematicDirsSummary(site)
            if not res["OK"]:
                return res
            end = time.time()
            timingPerSite[site]["timePerCycle"] = end - start

        self.log.info("--------- End of cycle ------------------")
        self.log.info("checked sites:")
        for site, siteTiming in timingPerSite.items():
            self.log.info(f"Site: {site} -  total time {siteTiming}")
        return S_OK()

    def setupSiteConfig(self, lcgSite):
        """Setup the configuration for the site."""
        site = lcgSite.split(".")[1]
        self.spaceTokens[site] = {
            "LHCb-Tape": {"year": "2011", "DiracSEs": [site + "-RAW", site + "-RDST", site + "-ARCHIVE"]},
            "LHCb-Disk": {
                "year": "2011",
                "DiracSEs": [site + "-DST", site + "_MC-DST", site + "-FAILOVER", site + "-BUFFER"],
            },
            "LHCb_USER": {"year": "2011", "DiracSEs": [site + "-USER"]},
            "LHCb_RAW": {"year": "2010", "DiracSEs": [site + "-RAW"]},
            "LHCb_RDST": {"year": "2010", "DiracSEs": [site + "-RDST"]},
            "LHCb_DST": {"year": "2010", "DiracSEs": [site + "-DST"]},
            "LHCb_MC_DST": {"year": "2010", "DiracSEs": [site + "_MC-DST"]},
            "LHCb_FAILOVER": {"year": "2010", "DiracSEs": [site + "-FAILOVER"]},
        }
        # for CERN: two more SEs: FREEZER AND HISTO

        for st in self.spaceTokens[site]:
            if st in self.spaceTokToIgnore:
                self.spaceTokens[site][st]["Check"] = False
            else:
                self.spaceTokens[site][st]["Check"] = True

        rootConfigPath = "DataConsistency"
        res = self.opHelper.getOptionsDict(f"{rootConfigPath}/{site}")
        # res = gConfig.getOptionsDict( "%s/%s" % ( rootConfigPath, site ) )
        if not res["OK"]:
            self.log.error(f"could not get configuration for site {site} : {res['Message']} ")
            return S_ERROR(res["Message"])
        storageDumpFileName = res["Value"]["StorageDumpFileName"]
        storageDumpURL = res["Value"]["StorageDumpURL"]
        fileType = res["Value"]["FileType"]
        pathInsideTar = res["Value"]["PathInsideTar"]
        # res = getSEsForSite( site )
        res = getSEsForSite(lcgSite)
        if not res["OK"]:
            self.log.error(f"could not get SEs for site {site} ")
            return S_ERROR(res["Message"])
        ses = res["Value"]
        self.log.info(f"SEs: {ses}")
        seName = site + "-RAW"
        res = gConfig.getOption(f"/Resources/StorageElements/{seName}/AccessProtocol.1/Path")
        if not res["OK"]:
            self.log.error(f"could not get configuration for SE {res['Message']} ")
            return S_ERROR(res["Message"])
        saPath = res["Value"]

        self.siteConfig[site] = {
            "originFileName": storageDumpFileName,
            "pathInsideTar": pathInsideTar,
            "originURL": storageDumpURL,
            "targetPath": os.path.join(self.inputFilesLocation, "downloadedFiles", site),
            "pathToInputFiles": os.path.join(self.inputFilesLocation, "goodFormat", site),
            "DiracName": lcgSite,
            "FileNameType": fileType,
            "SEs": ses,
            "SAPath": saPath,
        }
        self.log.info(f"Configuration for site {site} : {self.siteConfig[site]} ")
        return S_OK()

    def readInputFile(self, site):
        """Download, read and parse input files with SEs content.

        Write down the results to the ASCII files.
        There are 3 phases in the manipulation of input files:
        1. it is directly the format of the DB query output, right after uncompressing the
        tar file provided by the site:
        PFN | size | update (ms)
        2. one row per file, with format:  LFN size update
        3. directory summary files: one row per directory, with format:
        SE DirectoryLFN NumOfFiles TotalSize Update(actually, not used)
        """

        retCode = 0
        originFileName = self.siteConfig[site]["originFileName"]
        originURL = self.siteConfig[site]["originURL"]
        targetPath = self.siteConfig[site]["targetPath"]
        mkDir(targetPath)
        pathToInputFiles = self.siteConfig[site]["pathToInputFiles"]
        mkDir(pathToInputFiles)
        if pathToInputFiles[-1] != "/":
            pathToInputFiles = f"{pathToInputFiles}/"
        self.log.info(f"Reading input files for site {site} ")
        self.log.info(
            "originFileName: %s, originURL: %s, targetPath: %s, pathToInputFiles: %s "
            % (originFileName, originURL, targetPath, pathToInputFiles)
        )

        if targetPath[-1] != "/":
            targetPath = f"{targetPath}/"
        targetPathForDownload = targetPath + self.siteConfig[site]["pathInsideTar"]
        self.log.info(f"Target path to download input files: {targetPathForDownload}")
        # delete all existing files in the target directory if necessary:
        previousFiles = []
        try:
            previousFiles = os.listdir(targetPathForDownload)
            self.log.info(f"In {targetPathForDownload} found these files: {previousFiles}")
        except TypeError:
            pass
        except OSError:
            self.log.info(f"no leftover to remove from {targetPathForDownload}. Proceed downloading input files...")
        if previousFiles:
            self.log.info(f"delete these files: {previousFiles} ")
            for fileName in previousFiles:
                fullPath = os.path.join(targetPathForDownload, fileName)
                self.log.info(f"removing {fullPath}")
                os.remove(fullPath)

        # Download input data made available by the sites. Reuse the code of dirac-install:
        # urlretrieveTimeout, downloadAndExtractTarball
        res = self.downloadAndExtractTarball(originFileName, originURL, targetPath)
        if not res["OK"]:
            return S_ERROR(res["Message"])

        defaultDate = "na"
        # defaultSize = 0

        self.log.info("Check storage dump creation time..")
        self.StorageDumpCreationTime = None
        res = self.checkCreationDate(targetPathForDownload)
        if not res["OK"]:
            self.log.error(f"Failed to check storage dump date for site {site} ")
            return S_ERROR(res)
        if res["Value"] != 0:
            self.log.warn(f"Stale storage dump for site {site} ")
            retCode = -1
            return S_OK(retCode)
        self.log.info("Creation date check is fine!")

        inputFilesListP1 = os.listdir(targetPathForDownload)
        self.log.info(f"List of raw input files in {targetPathForDownload}: {inputFilesListP1} ")

        # delete all leftovers of previous runs from the pathToInputFiles
        try:
            previousParsedFiles = os.listdir(pathToInputFiles)
            self.log.info(f"In {pathToInputFiles} found these files: {previousParsedFiles}")
        except TypeError:
            pass
        except OSError:
            self.log.info(f"no leftover to remove from {pathToInputFiles} . Proceed to parse the input files...")
        if previousParsedFiles:
            self.log.info(f"delete these files: {previousParsedFiles} ")
            for fileName in previousParsedFiles:
                fullPath = os.path.join(pathToInputFiles, fileName)
                self.log.info(f"removing {fullPath}")
                os.remove(fullPath)

        # If necessary, call the special Castor pre-parser which analyse the name server dump and creates
        # one file per space token. The space token attribution is totally fake! it's based on the namespace.
        # For Castor, no other way to do it.
        if site in ["RAL"]:
            self.log.info("Calling special parser for Castor")
            res = self.castorPreParser(site, targetPathForDownload)
            if not res["OK"]:
                self.log.error("Error parsing storage dump")
            else:
                # recompute the list of input files
                inputFilesListP1 = os.listdir(targetPathForDownload)
                self.log.info(f"List of raw input files in {targetPathForDownload}: {inputFilesListP1} ")

        # if necessary, merge the files in order to have one file per space token: LHCb-Tape, LHCb-Disk, LHCb_USER
        # this is necessary in the transition phase while there are still some data on the old space tokens of 2010
        self.log.info("Merge the input files to have one file per space token")
        # Loop on N files relative to the site (one file for each space token)
        # previously open files for writing
        # every input file corresponds to one space token
        # whereas for the output, there is one file per NEW space token, so a merging is done

        outputFileMerged = {}
        for st in self.spaceTokens[site]:
            outputFileMerged[st] = {}
            if self.spaceTokens[site][st]["year"] == "2011":
                self.log.info(f"Preparing output files for space tokens: {st}")
                # merged file:
                fileP2Merged = pathToInputFiles + st + ".Merged.txt"
                outputFileMerged[st]["MergedFileName"] = fileP2Merged
                self.log.info(f"Opening file {fileP2Merged} in w mode")
                fP2Merged = open(fileP2Merged, "w")
                outputFileMerged[st]["pointerToMergedFile"] = fP2Merged
                # directory summary file:
                fileP3DirSummary = pathToInputFiles + st + ".dirSummary.txt"
                outputFileMerged[st]["DirSummaryFileName"] = fileP3DirSummary
                self.log.info(f"Opening file {fileP3DirSummary} in w mode")
                fP3DirSummary = open(fileP3DirSummary, "w")
                outputFileMerged[st]["pointerToDirSummaryFile"] = fP3DirSummary
        if st in ["LHCb-Disk", "LHCb-EOS", "LHCb_USER"]:
            try:
                outputFileMerged[st] = outputFileMerged["LHCb-Disk"]
            except KeyError:
                self.log.error(f"no pointer to file for st={st} ")
        if st == "LHCb-Tape":
            try:
                outputFileMerged[st] = outputFileMerged["LHCb-Tape"]
            except KeyError:
                self.log.error(f"no pointer to file for st={st} ")
        self.log.info("Parsed output files : ")
        for st in outputFileMerged:
            self.log.info(
                "space token: %s -> \n  %s\n %s  "
                % (st, outputFileMerged[st]["MergedFileName"], outputFileMerged[st]["DirSummaryFileName"])
            )

        for inputFileP1 in inputFilesListP1:
            self.log.info(f"+++++ input file: {inputFileP1} ++++++")
            # the expected input file line is: pfn | size | date
            # manipulate the input file to create a directory summary file (one row per directory)
            # Check the validity of the input file name:
            splitFile = inputFileP1.split(".")
            st = splitFile[0]
            if st not in self.spaceTokens[site]:
                self.log.warn(f"Not a  valid space token in the file name: {inputFileP1} ")
                continue

            completeSTId = st
            if len(splitFile) > 3:
                # file with format provided by SARA e.g. LHCb_RAW.31455.INACTIVE.txt
                completeSTId = splitFile[0] + "." + splitFile[1] + "." + splitFile[2]
            fullPathFileP1 = os.path.join(targetPathForDownload, inputFileP1)
            if not os.path.getsize(fullPathFileP1):
                self.log.info(f"{inputFileP1} file has zero size, will be skipped ")
                continue
            if "INACTIVE" in inputFileP1:
                self.log.info(f"WARNING: File {inputFileP1} will be analysed, even if space token is inactive")
            self.log.info(f"processing input file for space token: {st} ")
            fP2 = outputFileMerged[st]["pointerToMergedFile"]
            fileP2 = outputFileMerged[st]["MergedFileName"]
            self.log.info(f"Reading from file {fullPathFileP1}\n and writing to: {fileP2}")
            totalLines = 0  # counts all lines in input
            processedLines = 0  # counts all processed lines
            dirac_dir_lines = 0
            totalSize = 0
            totalFiles = 0
            for line in open(fullPathFileP1).readlines():
                totalLines += 1
                try:
                    splitLine = line.split("|")
                except BaseException:
                    self.log.error(f"Error: impossible to split line : {line}")
                    continue

                providedFilePath = splitLine[0].rstrip()
                if "dirac_directory" in providedFilePath:
                    dirac_dir_lines += 1
                    continue
                # get LFN from PFN if necessary:
                filePath = ""
                if self.siteConfig[site]["FileNameType"] == "LFN":
                    filePath = providedFilePath
                elif self.siteConfig[site]["FileNameType"] == "PFN":
                    res = self.getLFNPath(site, providedFilePath)
                    if not res["OK"]:
                        self.log.error(f"ERROR getLFNPath returned: {res} ")
                        continue
                    filePath = res["Value"]
                self.log.debug(f"filePath: {filePath}")
                if not filePath:
                    self.log.info(f"it was not possible to get the LFN for PFN={filePath}, skip this line")
                    continue

                self.log.debug(f"splitLine: {splitLine} ")
                size = splitLine[1].lstrip()
                totalSize += int(size)
                totalFiles += 1
                updated = splitLine[2].lstrip()
                newLine = filePath + " " + size + " " + updated
                if newLine[-1] != "\n":
                    newLine = f"{newLine}\n"
                fP2.write(f"{newLine}")
                processedLines += 1
            #        except:
            #          # the last line of these files is empty, so it will give this exception
            #          self.log.error( "Error in input line format! Line is: %s" % line )
            #          continue
            fP2.flush()

            self.log.info(f"Cleaning the STSummary table entries for site {site} and space token {completeSTId} ...")
            res = self.storageUsage.removeSTSummary(site, completeSTId)
            if not res["OK"]:
                self.log.error(
                    f"Unable to remove old entries from the STSummary table for site {site}: {res['Message']} "
                )
                continue
            self.log.info("Removed %d entries from the STSummary table for site %s" % (res["Value"], site))

            self.log.info(
                "%s - %s Total size: %d , total files: %d : publish to STSummary"
                % (site, completeSTId, totalSize, totalFiles)
            )
            res = self.storageUsage.publishTose_STSummary(
                site, completeSTId, totalSize, totalFiles, self.StorageDumpCreationTime
            )
            if not res["OK"]:
                self.log.error(f"failed to publish {site} - {st} summary ")
                return S_ERROR(res)
            self.log.info(
                "Total lines: %d , correctly processed: %d, dirac_directory found %d "
                % (totalLines, processedLines, dirac_dir_lines)
            )
        # close output files:
        for st in outputFileMerged:
            p2 = outputFileMerged[st]["pointerToMergedFile"]
            p2.close()

        # produce directory summaries:
        mergedFilesList = os.listdir(pathToInputFiles)
        for fileName in mergedFilesList:
            if "Merged" not in fileName:
                continue
            fileP2 = os.path.join(pathToInputFiles, fileName)
            self.log.info(f"Reading from Merged file fileP2 {fileP2} ")
            for spaceTok in self.spaceTokens[site]:
                self.log.debug(f"..check for space token: {spaceTok}")
                if spaceTok in fileP2:
                    st = spaceTok
                    break

            if not self.spaceTokens[site][st]["Check"]:
                self.log.info(f"Skip this space token: {st}")
                continue
            self.log.info(f"Space token: {st}")
            totalLines = 0  # counts all lines in input
            processedLines = 0  # counts all processed lines
            self.dirDict = {}
            for line in open(fileP2).readlines():
                self.log.debug(f"..processing line: {line}")
                totalLines += 1
                splitLine = line.split()
                filePath = splitLine[0]
                updated = defaultDate
                size = int(splitLine[1])
                # # currently the creation data is NOT stored in the DB.
                # # The time stamp stored for every entry is the insertion time
                # updatedMS = int( splitLine[3] )*1./1000
                # # convert to tuple format in UTC. Still to be checked which format the DB requires
                # updatedTuple = time.gmtime( updatedMS )
                # updated = time.asctime( updatedTuple )
                directories = filePath.split("/")
                fileName = directories[len(directories) - 1]
                basePath = ""
                for segment in directories[0:-1]:
                    basePath = basePath + segment + "/"
                if basePath not in self.dirDict:
                    self.dirDict[basePath] = {}
                    self.dirDict[basePath]["Files"] = 0
                    self.dirDict[basePath]["Size"] = 0
                    self.dirDict[basePath]["Updated"] = updated
                self.dirDict[basePath]["Files"] += 1
                self.dirDict[basePath]["Size"] += size
                processedLines += 1

            self.log.info("total lines: %d,  correctly processed: %d " % (totalLines, processedLines))
            # write to directory summary file
            fileP3 = outputFileMerged[st]["DirSummaryFileName"]
            fP3 = outputFileMerged[st]["pointerToDirSummaryFile"]
            self.log.info(f"Writing to file {fileP3}")
            for basePath in self.dirDict:
                summaryLine = " ".join(
                    [st, basePath, str(self.dirDict[basePath]["Files"]), str(self.dirDict[basePath]["Size"])]
                )
                self.log.debug(f"Writing summaryLine {summaryLine}")
                fP3.write(f"{summaryLine}\n")
            fP3.flush()
            fP3.close()

            self.log.debug("-------------------------summary of ReadInputFile-------------------------")
            for k in self.dirDict:
                self.log.debug(
                    "(lfn,st): %s-%s files=%d size=%d updated=%s"
                    % (k, st, self.dirDict[k]["Files"], self.dirDict[k]["Size"], self.dirDict[k]["Updated"])
                )

        return S_OK(retCode)

    def getLFNPath(self, site, pfnFilePath):
        """Given a PFN returns the LFN, stripping the suffix relative to the
        particular site.

        Important: usually the transformation is done simply removing the SApath of the site.
        So for ARCHIVE and FREEZER and FAILOVER data:
        the LFN will be: /lhcb/archive/<LFN> etc...
        even if LHCb register those replicas in the FC with the LFN: <LFN>, stripping the
        initial '/lhcb/archive'
        this is taken into account by the main method of the agent when it queries for replicas in the FC
        """

        outputFile = os.path.join(self.workDirectory, site + ".UnresolvedPFNs.txt")
        # this should be done with the replicaManager, but it does not work for archive files . tbu why
        # seName = site + '-RAW'
        sePath = self.siteConfig[site]["SAPath"]
        lfn = "None"
        try:
            lfn = pfnFilePath.split(sePath)[1]
        except BaseException:
            self.log.error(f"ERROR retrieving LFN from PFN = {pfnFilePath}, sePath = {sePath} ")
            if not os.path.exists(outputFile):
                of = open(outputFile, "w")
            else:
                of = open(outputFile, "a")
            of.write(f"{pfnFilePath}\n")
            of.close()
            return S_ERROR("Could not retrieve LFN")
        # additional check on the LFN format:
        if not lfn.startswith("/lhcb"):
            self.log.error(f"LFN should start with /lhcb: PFN={pfnFilePath} LFN={lfn}. Skip this file.")
            if not os.listdir(outputFile):
                of = open(outputFile, "w")
            else:
                of = open(outputFile, "a")
            os.write(f"{pfnFilePath}\n")
            os.close()
            return S_ERROR("Anomalous LFN does not start with '/lhcb' string")

        return S_OK(lfn)

    def urlretrieveTimeout(self, url, fileName, timeout=0):
        """Borrowed from dirac-install (and slightly modified to fit in this
        agent).

        Retrieve remote url to local file (fileName), with timeout wrapper
        """
        # NOTE: Not thread-safe, since all threads will catch same alarm.
        #       This is OK for dirac-install, since there are no threads.
        self.log.info(f'Retrieving remote file "{url}"')

        if timeout:
            signal.signal(signal.SIGALRM, alarmTimeoutHandler)
            # set timeout alarm
            signal.alarm(timeout)
        try:
            remoteFD = urlopen(url)
            expectedBytes = int(remoteFD.info()["Content-Length"])
            localFD = open(fileName, "wb")
            receivedBytes = 0
            data = remoteFD.read(16384)
            while data:
                receivedBytes += len(data)
                localFD.write(data)
                data = remoteFD.read(16384)
            localFD.close()
            remoteFD.close()
            if receivedBytes != expectedBytes:
                self.log.info(f"File should be {expectedBytes} bytes but received {receivedBytes}")
                return False
        except HTTPError as x:
            if x.code == 404:
                self.log.info(f"{url} does not exist")
                return False
        except Exception as x:
            if x == "TimeOut":
                self.log.info(f'Timeout after {str(timeout)} seconds on transfer request for "{url}"')
            if timeout:
                signal.alarm(0)
            raise x

        if timeout:
            signal.alarm(0)
        return True

    def downloadAndExtractTarball(self, originFileName, originURL, targetPath):
        """Borrowed from dirac-install ( slightly modified to fit in this agent).

        It download a tar archive and extract the content, using the method
        urlretrieveTimeout
        """
        tarName = f"{originFileName}"
        # destination file:
        tarPath = os.path.join(targetPath, tarName)
        try:
            if not self.urlretrieveTimeout(f"{originURL}/{tarName}", tarPath, 300):
                self.log.error(f"Cannot download {tarName}")
                return S_ERROR("Cannot download file")
        except Exception as e:
            self.log.error(f"Cannot download {tarName}: {str(e)}")
            return S_ERROR("Cannot download file")
        # check if the file has to be uncompressed
        self.log.info(f"The downloaded file is: {tarPath} ")
        if tarPath[-3:] not in ["bz2", "tgz", "tar"]:
            self.log.info("File ready to be read (no need to uncompress) ")
            return S_OK()
        # Extract
        cwd = os.getcwd()
        os.chdir(targetPath)
        try:
            tf = tarfile.open(tarPath, "r")
        except Exception as e:
            self.log.error(f"Cannot open file {tarPath}: {str(e)}")
            return S_ERROR("Cannot open file")
        for member in tf.getmembers():
            tf.extract(member)
        os.chdir(cwd)
        # Delete tar
        os.unlink(tarPath)
        return S_OK()

    def downloadFiles(self, originFileNames, originURL, targetPath):
        """Downloads a list of files from originURL locally to targetPath."""
        if not isinstance(originFileNames, list):
            self.log.error("first argument for downloadFiles method should be a list! ")
            return False
        for fileName in originFileNames:
            destinationPath = os.path.join(targetPath, fileName)
            try:
                if not self.urlretrieveTimeout(f"{originURL}/{fileName}", destinationPath, 300):
                    self.log.error(f"Cannot download {fileName}")
                    return False
            except Exception as e:
                self.log.error(f"Cannot download {fileName}: {str(e)}")
                return False
        return True

    def pathInLFC(self, dirName):
        """Get the path as registered in the FC.

        Different from the path that is used to build the pfn only for the
        special replicas (failover, archive, freezer)
        """
        lfcDirName = dirName
        for specialReplica in self.specialReplicas:
            prefix = "/lhcb/" + specialReplica
            if prefix in dirName:
                lfcDirName = dirName.split(prefix)[1]
                self.log.verbose(f"special replica! dirname = {dirName} -- lfcDirName = {lfcDirName}")
                return lfcDirName
        return lfcDirName

    def pathWithSuffix(self, dirName, replicaType):
        """Takes in input the path as registered in FC and returns the path with
        the initial suffix for the special replicas."""
        pathWithSuffix = dirName
        if replicaType in self.specialReplicas:
            pathWithSuffix = "/lhcb/" + replicaType + dirName
        return pathWithSuffix

    def getProblematicDirsSummary(self, site):
        """Produce a list of files that are not registered in the File Catalog and
        writes it down to a text file:

        1. queries the problematicDirs table to get all directories for a given site that have
           more data on SE than in LFCfor each replica type: (normal, archive, failover, freezer )
        2. scan the input files (from the sites storage dumps) to get all the files belonging
           to the problematic directories
        3. lookup in in FC file by file to check if they have a replica registered at the site
        4. the files that are found not to have a replica registered for the site, are written down to a file
        """
        self.log.info(f"*** Execute getProblematicDirsSummary method for site: {site} ")
        fileNameMissingReplicas = os.path.join(self.workDirectory, site + ".replicasMissingFromSite.txt")
        self.log.info(f"Opening file for replicas not registered: {fileNameMissingReplicas} ")
        fpMissingReplicas = open(fileNameMissingReplicas, "w")
        fileNameMissingFiles = os.path.join(self.workDirectory, site + ".filesMissingFromFC.txt")
        self.log.info(f"Opening file for files not registered: {fileNameMissingFiles} ")
        fpMissingFiles = open(fileNameMissingFiles, "w")
        problem = "NotRegisteredInFC"
        res = self.storageUsage.getProblematicDirsSummary(site, problem)
        if not res["OK"]:
            self.log.error(f"ERROR! {res}")
            return S_ERROR(res)
        val = res["Value"]
        problematicDirectories = {}  # store a list of directories for each replica type
        self.log.verbose("List of problematic directories: ")
        for row in val:
            # ('SARA', 'LHCb-Disk', 0L, 43L, '/lhcb/MC/2010/DST/00007332/0000/', 'NotRegisteredInFC','failover')
            site = row[0]
            lfcPath = row[4]
            problem = row[5]
            replicaType = row[6]
            pathWithSuffix = self.pathWithSuffix(lfcPath, replicaType)
            self.log.verbose(f"{lfcPath} {replicaType} - {pathWithSuffix}")
            if replicaType not in problematicDirectories:
                problematicDirectories[replicaType] = []
            if pathWithSuffix not in problematicDirectories[replicaType]:
                problematicDirectories[replicaType].append(pathWithSuffix)  # fix 13.03.2012
            else:
                self.log.error(
                    "the directory should be listed only once for a given site and type of replica! "
                    " site=%s, path= %s, type of replica =%s  " % (site, lfcPath, replicaType)
                )
                continue
        self.log.info("Found the following problematic directories:")
        for replicaType, problematicDir in problematicDirectories.items():
            self.log.info(f"replica type: {replicaType} , directories: {problematicDir} ")
        # retrieve the list of files belonging to problematic directories from the merged files:
        filesInProblematicDirs = {}
        # read the files from the Merged files
        pathToMergedFiles = self.siteConfig[site]["pathToInputFiles"]
        if pathToMergedFiles[:-1] != "/":
            pathToMergedFiles = pathToMergedFiles + "/"
        for mergedFile in os.listdir(pathToMergedFiles):
            if "Merge" not in mergedFile:
                continue
            fullFilePath = os.path.join(pathToMergedFiles, mergedFile)
            self.log.info(f"Scanning file: {fullFilePath} ... ")
            for line in open(fullFilePath).readlines():
                lfn = line.split()[0]  # this LFN includes the initial suffix (e.g./lhcb/archive/)
                directories = lfn.split("/")
                basePath = ""
                for segment in directories[0:-1]:
                    basePath = basePath + segment + "/"  # basepath is the directory including the initial suffix
                for replicaType in problematicDirectories:
                    if basePath in problematicDirectories[replicaType]:  # these paths do include initial suffix
                        if replicaType not in filesInProblematicDirs:
                            filesInProblematicDirs[replicaType] = []
                        if lfn not in filesInProblematicDirs[replicaType]:  # lfn including suffix
                            filesInProblematicDirs[replicaType].append(lfn)

        self.log.info("Files in problematic directories:")
        for replicaType in filesInProblematicDirs:
            self.log.info(f"replica type: {replicaType} files: {len(filesInProblematicDirs[replicaType])} ")
            for fil in filesInProblematicDirs[replicaType]:
                self.log.verbose(f"file in probl Dir {fil} {replicaType}")

        for replicaType in filesInProblematicDirs:
            res = self.checkReplicasInFC(
                replicaType, filesInProblematicDirs[replicaType], site, fileNameMissingReplicas, fileNameMissingFiles
            )
        fpMissingReplicas.close()
        fpMissingFiles.close()
        if self.pathToUploadResults[-1] != "/":
            self.pathToUploadResults = self.pathToUploadResults + "/"
        lfnToUploadResults = self.pathToUploadResults + fileNameMissingReplicas.split("/")[-1]
        self.log.info(f"Upload the file {fileNameMissingReplicas} to the grid with LFN: {lfnToUploadResults} ")
        guid = None
        res = self.diracApi.removeFile(lfnToUploadResults)
        if not res["OK"]:
            self.log.error(f"Failed to remove the file already existing {res['Message']} ")
        else:
            res = self.diracApi.addFile(
                lfnToUploadResults, fileNameMissingReplicas, "CERN-DEBUG", guid, printOutput=True
            )
            if not res["OK"]:
                self.log.error(f"Failed to upload to the grid the file {fileNameMissingReplicas} : {res['Message']} ")
        lfnToUploadResults = self.pathToUploadResults + fileNameMissingFiles.split("/")[-1]
        self.log.info(f"Upload the file {fileNameMissingFiles} to the grid with LFN: {lfnToUploadResults} ")
        res = self.diracApi.removeFile(lfnToUploadResults)
        if not res["OK"]:
            self.log.error(f"Failed to remove the file already existing {res['Message']} ")
        else:
            res = self.diracApi.addFile(lfnToUploadResults, fileNameMissingFiles, "CERN-DEBUG", guid, printOutput=True)
            if not res["OK"]:
                self.log.error(f"Failed to upload to the grid the file {fileNameMissingFiles} : {res['Message']} ")
        return S_OK()

    # ...............................................................................................................
    def checkReplicasInFC(self, replicaType, filesToBeChecked, site, fileNameMissingReplicas, fileNameMissingFiles):
        """Check the existance of the replicas for the given site and replica type
        in the FC."""
        self.log.info(f"*** Execute checkReplicasInFC for replicaType={replicaType}, site={site} ")
        filesMissingFromFC = []
        replicasMissingFromSite = []
        # totalSizeMissingFromFC = 0
        # totalSizeReplicasMissingFromSite = 0
        # for files in problematic directories look up in the FC:
        specialReplicasSEs = []
        for sr in self.specialReplicas:
            se = site + "-" + sr.upper()
            specialReplicasSEs.append(se)
        self.log.verbose(f"SEs for special replicas: {specialReplicasSEs} ")

        filesInProblematicDirs = []
        if replicaType in self.specialReplicas:
            for lfn in filesToBeChecked:
                filesInProblematicDirs.append(self.pathInLFC(lfn))
        else:
            filesInProblematicDirs = filesToBeChecked

        active = False  # then this should be moved to a config parameter
        start = time.time()
        if not filesInProblematicDirs:
            self.log.info(f"No file to be checked in the FC for site {site} ")
            return S_OK()
        if active:
            repsResult = self.dataManager.getActiveReplicas(filesInProblematicDirs)
        else:
            repsResult = self.dataManager.getReplicas(filesInProblematicDirs)
        timing = time.time() - start
        self.log.info(
            "%d replicas Lookup Time: %.2f s -> %.2f s/replica"
            % (len(filesInProblematicDirs), timing, float(timing) / len(filesInProblematicDirs))
        )
        if not repsResult["OK"]:
            return S_ERROR(repsResult["Message"])
        goodFiles = repsResult["Value"]["Successful"]
        badFiles = repsResult["Value"]["Failed"]
        for lfn in badFiles:
            if "No such file or directory" in badFiles[lfn]:
                self.log.info(f"missing from FC {lfn} {replicaType}")
                # check if the storage files have been removed in the meanwhile after the storage dump creation and the check
                # to be done
                storageFileStatus = self.storageFileExists(lfn, replicaType, site)
                if storageFileStatus == 1:
                    self.log.info(f"Storage file exists: Inconsistent file! {lfn} ")
                    filesMissingFromFC.append(lfn)
                elif storageFileStatus == 0:
                    self.log.info(f"Storage file does not exist (temporary file) {lfn} ")
                else:
                    self.log.warn(f"Failed request for storage file {lfn} ")
            else:
                self.log.info(f"Unknown message from Fc: {lfn} - {badFiles[lfn]} ")
        for lfn in goodFiles:
            # check if the replica exists at the given site:
            replicaAtSite = False
            if replicaType in self.specialReplicas:
                specialReplicaSE = site + "-" + replicaType.upper()
                for se in goodFiles[lfn]:
                    if se == specialReplicaSE:
                        self.log.verbose(f"matching se: {se} ")
                        replicaAtSite = True
                        break
            else:
                for se in goodFiles[lfn]:
                    if se in specialReplicasSEs:
                        self.log.verbose(f"Replica type is {replicaType}, skip this SE: {se} ")
                        continue
                    if site in se:
                        self.log.verbose(f"matching se: {se} ")
                        replicaAtSite = True
                        break
            if not replicaAtSite:
                # check if storage file currently exists or if it was a temporary file
                storageFileStatus = self.storageFileExists(lfn, replicaType, site)
                if storageFileStatus == 1:
                    self.log.info(f"Storage file exists: Inconsistent file! {lfn} ")
                    replicasMissingFromSite.append(lfn)
                elif storageFileStatus == 0:
                    self.log.info(f"Storage file does not exist (temporary file) {lfn} ")
                else:
                    self.log.warn(f"Failed request for storage file {lfn} ")

        assignedSE = "Unknown"
        if replicaType in self.specialReplicas:
            assignedSE = site + "-" + replicaType.upper()

        fpMissingReplicas = open(fileNameMissingReplicas, "a")
        self.log.info(f"Writing list of replicas missing from site to file {fileNameMissingReplicas} ")
        for lfn in replicasMissingFromSite:
            fpMissingReplicas.write(f"{lfn} {assignedSE}\n")
            self.log.info(f"{lfn} {assignedSE}\n")
        fpMissingReplicas.flush()

        self.log.info(f"Writing list of files missing from FC to file {fileNameMissingFiles} ")
        fpMissingFiles = open(fileNameMissingFiles, "a")
        for lfn in filesMissingFromFC:
            fpMissingFiles.write(f"{lfn} {assignedSE}\n")
            self.log.info(f"{lfn} {assignedSE}\n")
        fpMissingFiles.flush()

        fileName = os.path.join(self.workDirectory, site + "." + replicaType + ".consistencyChecksSummary.txt")
        self.log.info(f"Writing consistency check summary to file {fileName} ")
        date = time.asctime()
        line = "Site: " + site + "  Date: " + date
        fp = open(fileName, "w")
        fp.write(f"{line}\n")
        totSizeMissingFromFC = 0  # to be implemented!!!
        totSizeReplicasMissingFromSite = 0  # to be implemented!!!
        fp.write(
            "Total number of LFN at site not registered in the FC: %d , "
            "total size: %.2f GB \n" % (len(filesMissingFromFC), totSizeMissingFromFC / 1.0e9)
        )
        fp.write(
            "Total number of replicas  at site not registered in the FC: %d , "
            "total size: %.2f GB \n" % (len(replicasMissingFromSite), totSizeReplicasMissingFromSite / 1.0e9)
        )
        fp.close()

        return S_OK()

    def storageFileExists(self, lfn, replicaType, site):
        """Check if the replica exists on storage. This is to filter many temporary
        files (e.g. un-merged..) that are removed in the while between storage dump
        and consistency check. Return values:

        -1 : request failed
         0 : storage file does not exist
         1 : storage file exists
        """
        storageFileExist = -1
        # get the PFN
        seList = []
        if replicaType in self.specialReplicas:
            seName = site + "-" + replicaType.upper()
            seList.append(seName)
        else:
            specialReplicasSEs = []
            for sr in self.specialReplicas:
                se = site + "-" + sr.upper()
                specialReplicasSEs.append(se)
            # seName is not known
            # try with all the SEs available for the site, except the ones for special replicas
            allSEs = self.siteConfig[site]["SEs"]
            for se in allSEs:
                if se not in specialReplicasSEs:
                    seList.append(se)
        self.log.verbose(f"list of SEs : {seList}")

        for seName in seList:
            storageElement = StorageElement(seName)
            res = storageElement.getURL(lfn)
            self.log.verbose(f"checking existance for {lfn} - {seName}")
            res = storageElement.exists(lfn)
            self.log.verbose(f"result of getStorageFileExists: {res} ")
            if not res["OK"]:
                self.log.error(f"error executing StorageElement.exists {res['Message']} ")
                storageFileExist = -1
                continue
            if res["Value"]["Failed"]:
                self.log.error(f"error executing StorageElement.exists {res} ")
                storageFileExist = -1
                continue
            elif res["Value"]["Successful"]:
                if res["Value"]["Successful"][lfn]:
                    self.log.info(f"storage file exists: {res['Value']} ")
                    storageFileExist = 1
                    return storageFileExist
                else:
                    self.log.verbose(f"storage file NOT found: {res['Value']} ")
                    storageFileExist = 0

        return storageFileExist

    def castorPreParser(self, site, inputFilesDir):
        """Preliminary parsing for Castor nameserver dump Separates the files in 3
        space tokens relying on the namespace."""

        if inputFilesDir[-1:] != "/":
            inputFilesDir = inputFilesDir + "/"
        inputFile = os.listdir(inputFilesDir)
        if len(inputFile) != 1:
            self.log.error(f"For this parser, there should be one and only one file. Found these files: {inputFile} ")
            return S_ERROR()

        p1FilesDict = {
            "LHCb_USER": {"fileName": inputFilesDir + "LHCb_USER.txt"},
            "LHCb-Disk": {"fileName": inputFilesDir + "LHCb-Disk.txt"},
            "LHCb-Tape": {"fileName": inputFilesDir + "LHCb-Tape.txt"},
        }
        for st in p1FilesDict:
            fp = open(p1FilesDict[st]["fileName"], "w")
            p1FilesDict[st]["filePointer"] = fp

        fullPath = os.path.join(inputFilesDir, inputFile[0])
        for line in open(fullPath).readlines():
            splitLine = line.split()
            if len(splitLine) < 2:
                self.log.debug(f"Empty directory. Skip line! {line} ")
                continue
            size = splitLine[4]
            pfn = splitLine[10]
            # updated = should be reconstructed on the basis of the ascii date
            update = "na"
            res = self.getLFNPath(site, pfn)
            if not res["OK"]:
                return S_ERROR()
            lfn = res["Value"]
            probableSpaceToken = ""
            if lfn[:11] == "/lhcb/user/":
                probableSpaceToken = "LHCb_USER"
            elif (lfn[-3:] == "raw" or lfn[-4:] == "sdst" or lfn[:19] == "/lhcb/archive/lhcb/") and (
                lfn[:20] != "/lhcb/failover/lhcb/"
            ):
                probableSpaceToken = "LHCb-Tape"
            else:
                probableSpaceToken = "LHCb-Disk"
            newLine = pfn + " |  " + size + " |  " + update
            fp = p1FilesDict[probableSpaceToken]["filePointer"]
            fp.write(f"{newLine}\n")

        for st in p1FilesDict:
            fp = p1FilesDict[st]["filePointer"]
            fp.close()
        return S_OK()

    def checkCreationDate(self, directory):
        """Check the storage dump creation date.

        Returns 0 if the creation date is more recent than a given time
        interval (set as configuration parameter), otherwise returns -1
        """
        retCode = 0

        for fileName in os.listdir(directory):
            fullPath = os.path.join(directory, fileName)
            # # ( mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime ) = os.stat( fullPath )
            mtime = os.path.getmtime(fullPath)
            self.StorageDumpCreationTime = datetime.utcfromtimestamp(mtime)
            self.log.info(f"in checkCreationDate StorageDumpCreationTime {self.StorageDumpCreationTime} ")
            now = time.time()
            elapsedTime = now - mtime
            self.log.info(
                "creation time: %s, elapsed time: %d h "
                "(max delay allowed : %d h ) "
                % (time.ctime(mtime), elapsedTime / 3600, self.maximumDelaySinceSD / 3600)
            )

            if elapsedTime > self.maximumDelaySinceSD:
                self.log.warn(
                    "storage dump creation date is older "
                    "than maximum limit! %s s ( %d h ) - %s "
                    % (self.maximumDelaySinceSD, self.maximumDelaySinceSD / 3600, fullPath)
                )
                retCode = -1
                return S_OK(retCode)
        return S_OK(retCode)
