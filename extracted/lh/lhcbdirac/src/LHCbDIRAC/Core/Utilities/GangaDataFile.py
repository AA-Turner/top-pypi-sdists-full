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
"""GangaDataFile is a utility to create a Data file, to be used by ganga.

Givn input files, it will create something like::

  from Gaudi.Configuration import *
  from GaudiConf import IOHelper
  IOHelper("ROOT").inputFiles([
      "LFN:foo",
      "LFN:bar"
  ], clear=True)

  FileCatalog().Catalogs = ["xmlcatalog_file:pool_xml_catalog.xml"]
"""
import os

from DIRAC import gLogger

from LHCbDIRAC.BookkeepingSystem.Client.LHCB_BKKDBClient import LHCB_BKKDBClient


class GangaDataFile:
    """Creates ganga data file."""

    def __init__(self, fileName="data.py", xmlcatalog_file="pool_xml_catalog.xml", log=None):
        """initialize."""
        if not log:
            self.log = gLogger.getSubLogger("GangaDataFile")
        else:
            self.log = log

        self.fileName = fileName
        self.xmlcatalog_file = xmlcatalog_file

        try:
            os.remove(self.fileName)
        except OSError:
            pass

        self.log.info(f"Creating Ganga data file {self.fileName} from scratch")

    ################################################################################

    def generateDataFile(self, lfns, persistency=None):
        """generate the data file."""
        if isinstance(lfns, str) and lfns:
            lfns = [lfns]
        elif not isinstance(lfns, list):
            self.log.error("Was expecting a list")
            raise TypeError("Expected List")
        if not len(lfns):
            self.log.warn("No file generated: was expecting a non-empty list")
            raise ValueError("list empty")

        try:
            persistency = persistency.upper()
            # Create a fake LFN->PFN dictionary to give the persistency
            fakePfns = dict.fromkeys(lfns, {"pfntype": persistency})
        except AttributeError:
            fakePfns = None

        script = LHCB_BKKDBClient().writeJobOptions(
            lfns, optionsFile=self.fileName, catalog=self.xmlcatalog_file, savePfn=fakePfns
        )
        self.log.info(f"Created Ganga data file {self.fileName}")

        return script
