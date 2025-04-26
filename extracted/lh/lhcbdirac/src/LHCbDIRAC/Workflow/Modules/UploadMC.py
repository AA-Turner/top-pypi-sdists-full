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
"""UploadMC module is used to upload to ES the json files for MC statistics."""
import os
import json
from datetime import datetime, timezone

from DIRAC import S_OK, S_ERROR, gLogger

from LHCbDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from LHCbDIRAC.ProductionManagementSystem.Client.MCStatsClient import MCStatsClient
from LHCbDIRAC.Core.Utilities.XMLSummaries import XMLSummary
from LHCbDIRAC.Core.Utilities.GeneratorLog import GeneratorLog


class UploadMC(ModuleBase):
    """Upload to LogSE."""

    def __init__(self):
        """Module initialization."""

        self.log = gLogger.getSubLogger("UploadMC")
        super().__init__(self.log)

    def _resolveInputVariables(self):
        """standard method for resolving the input variables."""

        super()._resolveInputVariables()

    def execute(
        self,
        production_id=None,
        prod_job_id=None,
        wms_job_id=None,
        workflowStatus=None,
        stepStatus=None,
        wf_commons=None,
        step_commons=None,
        step_number=None,
        step_id=None,
    ):
        """Main executon method.

        Takes care of indexing JSON files on ElasticSearch databases
        All these uploads are controlled by flags that can be found in
        'Operations/<setup>/Productions/'

        1) errors => /Operations/<setup>/Productions/UploadES_errors (default: True)
        2) Summary.xml -> JSON => /Operations/<setup>/Productions/UploadES_XMLSummary (default: False)
        3) GeneratorLog.xml -> JSON => /Operations/<setup>/Productions/UploadES_GeneratorLog (default: False)
        4) PRMon => /Operations/<setup>/Productions/UploadES_PrMon (default: False)

        """
        try:
            super().execute(
                production_id,
                prod_job_id,
                wms_job_id,
                workflowStatus,
                stepStatus,
                wf_commons,
                step_commons,
                step_number,
                step_id,
            )

            self._resolveInputVariables()

            mcStatsClient = MCStatsClient()

            # DBs list
            # db = {
            #     'XMLSummary': elasticApplicationSummaryDB,
            #     'errors': ElasticLogErrorsDB,
            #     'generatorLog': elasticMCGeneratorLogDB,
            #     'prMon': elasticMCGeneratorLogDB,
            # }

            # 1) MC errors
            # looking for json files that are 'self.jobID_Errors_Gauss.json'
            # TODO: it could be extended to at least Boole
            fn = f"{self.jobID}_Errors_Gauss.json"
            if os.path.exists(fn):
                with open(fn) as fd:
                    try:
                        jsonData = json.load(fd)
                        self.log.verbose("Content of JSON file", f"{fn}: {jsonData}")
                        errorList = []  # Fill this list to send the data in a bulk
                        for i, error in jsonData.items():
                            errorList.append(error)
                        if self._enableModule() and self.opsH.getValue("Productions/UploadES_errors", True):
                            res = mcStatsClient.set("errors", errorList)
                            if not res["OK"]:
                                self.log.error(
                                    "MC Error data not set, exiting without affecting workflow status",
                                    f"{str(errorList)}: {res['Message']}",
                                )
                        else:
                            # At this point we can see exactly what the module would have uploaded
                            self.log.info("Module disabled", f"would have attempted to upload the following file {fn}")
                    except Exception as ve:
                        self.log.error(repr(ve))
                        self.log.verbose(f"Exception loading the JSON file: content of {fn} follows")
                        self.log.verbose(fd.read)
                        # do not fail the job for this
                        # raise
            else:
                self.log.info("Gauss errors JSON file not found", fn)

            # 2) summary JSON files
            # looking for xml files that are 'summaryGauss_self.production_id_self.prod_job_id_1.xml'
            xmlfl = f"summaryGauss_{self.production_id}_{self.prod_job_id}_1.xml"
            if os.path.exists(xmlfl):
                try:
                    xmlData = XMLSummary(xmlfl)
                    xmlData.xmltojson()
                    # At this point 'summaryGauss_self.production_id_self.prod_job_id_1.json' should have been created
                    jsonfl = f"summaryGauss_{self.production_id}_{self.prod_job_id}_1.json"
                    with open(jsonfl) as JS:
                        jsonData = json.load(JS)
                        ids = dict()
                        ids["JobID"] = self.jobID
                        ids["ProductionID"] = self.production_id
                        ids["prod_job_id"] = self.prod_job_id
                        jsonData["Counters"]["ID"] = ids
                        with open(jsonfl, "w", encoding="utf-8") as output:
                            output.write(str(json.dumps(jsonData, indent=2)))

                        self.log.verbose("Content of JSON file", f"{jsonfl}: {jsonData}")
                        if self._enableModule() and self.opsH.getValue("Productions/UploadES_XMLSummary", False):
                            res = mcStatsClient.set("XMLSummary", jsonData)
                            if not res["OK"]:
                                self.log.error(
                                    "Gauss Summaries data not set, exiting without affecting workflow status",
                                    f"{str(jsonData)}: {res['Message']}",
                                )
                        else:
                            # At this point we can see exactly what the module would have uploaded
                            self.log.info(
                                "Module disabled", f"would have attempted to upload the following file {jsonfl}"
                            )

                except Exception:
                    self.log.exception("Exception creating/loading the XMLSummary JSON file")
                    # do not fail the job for this

            else:
                self.log.info("XML Gauss summary file not found", xmlfl)

            # 3) Generator logs
            # looking for xml files that are 'GeneratorLog.xml'
            xmlfile = "GeneratorLog.xml"
            if os.path.exists(xmlfile):
                try:
                    jsonfile = f"GeneratorLog_{self.production_id}_{self.prod_job_id}.json"
                    xmlData = GeneratorLog()
                    xmlData.generatorLogJson(jsonfile)
                    # At this point 'GeneratorLog_self.production_id_self.prod_job_id.json' should have been created
                    with open(jsonfile) as JS:
                        jsonData = json.load(JS)
                        ids = dict()
                        ids["JobID"] = self.jobID
                        ids["ProductionID"] = self.production_id
                        ids["prod_job_id"] = self.prod_job_id
                        jsonData["generatorCounters"]["ID"] = ids
                        jsonData["generatorCounters"]["timestamp"] = str(datetime.now(tz=timezone.utc))
                        with open(jsonfile, "w", encoding="utf-8") as output:
                            output.write(str(json.dumps(jsonData)))

                        self.log.verbose("Content of JSON file", f"{jsonfile}: {jsonData}")
                        if self._enableModule() and self.opsH.getValue("Productions/UploadES_GeneratorLog", False):
                            res = mcStatsClient.set("generatorLog", jsonData)
                            if not res["OK"]:
                                self.log.error(
                                    "Generator Log data not set, exiting without affecting workflow status",
                                    f"{str(jsonData)}: {res['Message']}",
                                )
                        else:
                            # At this point we can see exactly what the module would have uploaded
                            self.log.info(
                                "Module disabled", f"would have attempted to upload the following file {jsonfile}"
                            )

                except Exception:
                    self.log.exception("Exception creating/loading the GeneratorLog JSON file")
                    # do not fail the job for this

            else:
                self.log.info("XML GeneratorLog file not found", xmlfile)

            # 4) PRmon JSON files (only for Gauss)
            # looking for prmon files that are 'prmon_Gauss.json'
            prmonFile = "prmon_Gauss.json"
            if os.path.exists(prmonFile):
                with open(prmonFile) as JS:
                    try:
                        jsonData = json.load(JS)
                        jsonData["JobID"] = self.jobID
                        jsonData["ProductionID"] = self.production_id
                        jsonData["prod_job_id"] = self.prod_job_id
                        self.log.verbose("Content of JSON file", f"{prmonFile}: {jsonData}")
                        if self._enableModule() and self.opsH.getValue("Productions/UploadES_PrMon", False):
                            res = mcStatsClient.set("prMon", jsonData)
                            if not res["OK"]:
                                self.log.error(
                                    "prmon Metrics data not set, exiting without affecting workflow status",
                                    f"{str(jsonData)}: {res['Message']}",
                                )
                        else:
                            # At this point we can see exactly what the module would have uploaded
                            self.log.info(
                                "Module disabled", f"would have attempted to upload the following file {prmonFile}"
                            )
                    except Exception as ve:
                        self.log.error(repr(ve))
                        self.log.verbose(f"Exception loading the JSON file: content of {prmonFile} follows")
                        self.log.verbose(JS.read())
                        # do not fail the job for this
                        # raise
            else:
                self.log.info("prmon JSON file not found", prmonFile)

            return S_OK()

        except Exception as e:
            self.log.exception("Failure in UploadMC execute module", lException=e)
            return S_ERROR(repr(e))

        finally:
            super().finalize()
