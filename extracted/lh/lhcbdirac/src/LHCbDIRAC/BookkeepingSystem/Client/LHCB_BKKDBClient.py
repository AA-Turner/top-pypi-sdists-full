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
"""LHCb Bookkeeping database client."""
import os
from LHCbDIRAC.BookkeepingSystem.Client.LHCbBookkeepingManager import LHCbBookkeepingManager


class LHCB_BKKDBClient:
    """Client used to browse the Entities."""

    def __init__(self):
        """Initialize the basic class."""

        self.__ESManager = LHCbBookkeepingManager()
        result = self.__ESManager.getAbsolutePath("/")
        if result["OK"]:
            self.__currentDirectory = result["Value"]

    def help(self):
        """help function."""
        return self.__ESManager.help()  # pylint: disable=no-member

    def list(self, path="", selectionDict=None, sortDict=None, startItem=0, maxitems=0):
        """It lists the database content as a Linux File System."""
        selectionDict = selectionDict if selectionDict is not None else {}
        sortDict = sortDict if sortDict is not None else {}
        res = self.__ESManager.getAbsolutePath(os.path.join(self.__currentDirectory, path))
        if not res["OK"]:
            return res
        return self.__ESManager.list(res["Value"], selectionDict, sortDict, startItem, maxitems)

    def get(self, path=""):
        """get path."""
        return self.__ESManager.get(path)

    def getPossibleParameters(self):
        """available trees."""
        return self.__ESManager.getPossibleParameters()  # pylint: disable=no-member

    def setParameter(self, name):
        """tree used."""
        return self.__ESManager.setParameter(name)  # pylint: disable=no-member

    def getLogicalFiles(self):
        """lfns."""
        return self.__ESManager.files_  # pylint: disable=no-member

    def getFilesPFN(self):
        """PFNS."""
        return self.__ESManager.getFilesPFN()  # pylint: disable=no-member

    def getNumberOfEvents(self, files):
        """number of events."""
        return self.__ESManager.getNumberOfEvents(files)  # pylint: disable=no-member

    def writeJobOptions(
        self, files, optionsFile="jobOptions.opts", savedType=None, catalog=None, savePfn=None, dataset=None
    ):
        """Gaudi card."""
        return self.__ESManager.writeJobOptions(  # pylint: disable=no-member
            files, optionsFile, savedType, catalog, savePfn, dataset
        )

    def getJobInfo(self, lfn):
        """how a file is created."""
        return self.__ESManager.getJobInfo(lfn)  # pylint: disable=no-member

    def setAdvancedQueries(self, value):
        """Advanced queries."""
        return self.__ESManager.setAdvancedQueries(value)  # pylint: disable=no-member

    def getLimitedFiles(self, selectionDict, sortDict, startItem, maxitems):
        """get files used by Web portal."""
        return self.__ESManager.getLimitedFiles(  # pylint: disable=no-member
            selectionDict, sortDict, startItem, maxitems
        )

    def getAncestors(self, files, depth):
        """ancestor of files."""
        return self.__ESManager.getAncestors(files, depth)  # pylint: disable=no-member

    def getFileCreationLog(self, filename):
        """log file of a given file."""
        return self.__ESManager.getFileCreationLog(filename)  # pylint: disable=no-member

    def writePythonOrJobOptions(self, startItem, maxitems, path, optstype):
        """python job option."""
        return self.__ESManager.writePythonOrJobOptions(  # pylint: disable=no-member
            startItem, maxitems, path, optstype
        )

    def getLimitedInformations(self, startItem, maxitems, path):
        """statistics."""
        return self.__ESManager.getLimitedInformations(startItem, maxitems, path)  # pylint: disable=no-member

    def getProcessingPassSteps(self, in_dict):
        """step."""
        return self.__ESManager.getProcessingPassSteps(in_dict)  # pylint: disable=no-member

    def getMoreProductionInformations(self, prodid):
        """production details."""
        return self.__ESManager.getMoreProductionInformations(prodid)  # pylint: disable=no-member

    def getAvailableProductions(self):
        """available productions."""
        return self.__ESManager.getAvailableProductions()  # pylint: disable=no-member

    def getFileHistory(self, lfn):
        """ "file history."""
        return self.__ESManager.getFileHistory(lfn)  # pylint: disable=no-member

    def getCurrentParameter(self):
        """curent bookkeeping path."""
        return self.__ESManager.getCurrentParameter()  # pylint: disable=no-member

    def getQueriesTypes(self):
        """type of the current query."""
        return self.__ESManager.getQueriesTypes()  # pylint: disable=no-member

    def getProductionProcessingPassSteps(self, in_dict):
        """the steps which produced a given production."""
        return self.__ESManager.getProductionProcessingPassSteps(in_dict)  # pylint: disable=no-member

    def getAvailableDataQuality(self):
        """available data quality."""
        return self.__ESManager.getAvailableDataQuality()  # pylint: disable=no-member

    def getAvailableExtendedDQOK(self):
        """available extended DQOK systems."""
        return self.__ESManager.getAvailableExtendedDQOK()  # pylint: disable=no-member

    def getAvailableSMOG2States(self):
        """available SMOG2 states."""
        return self.__ESManager.getAvailableSMOG2States()  # pylint: disable=no-member

    def setDataQualities(self, values):
        """set data qualities."""
        self.__ESManager.setDataQualities(values)  # pylint: disable=no-member

    def getStepsMetadata(self, bkDict):
        """returns detailed step metadata."""
        return self.__ESManager.getStepsMetadata(bkDict)  # pylint: disable=no-member

    def setFileTypes(self, fileTypeList):
        """it sets the file types."""
        return self.__ESManager.setFileTypes(fileTypeList)  # pylint: disable=no-member

    def getFilesWithMetadata(self, dataset):
        """it sets the file types.

        :param dict dataset: it is a bookkeeping dictionary, which contains the conditions used to retreive the lfns
        :return: S_OK lfns with metadata
        """
        return self.__ESManager.getFilesWithMetadata(dataset)  # pylint: disable=no-member
