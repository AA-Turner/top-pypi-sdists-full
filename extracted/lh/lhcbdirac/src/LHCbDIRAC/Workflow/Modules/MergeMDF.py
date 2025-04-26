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
"""Simple merging module for MDF files."""
import shlex

from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities.Subprocess import systemCall
from DIRAC.Resources.Catalog.PoolXMLCatalog import PoolXMLCatalog

import LHCbDIRAC
from LHCbDIRAC.Workflow.Modules.ModuleBase import ModuleBase


class MergeMDF(ModuleBase):
    """To be used in normal workflows."""

    #############################################################################
    def __init__(self, bkClient=None, dm=None):
        """Module initialization."""
        self.log = gLogger.getSubLogger("MergeMDF")
        super().__init__(self.log, bkClientIn=bkClient, dm=dm)

        self.outputLFN = ""
        # List all input parameters here
        self.stepInputData = []
        self.poolXMLCatName = "pool_xml_catalog.xml"
        self.applicationName = "cat"

    #############################################################################
    def _resolveInputVariables(self):
        """By convention the module parameters are resolved here."""

        super()._resolveInputVariables()
        super()._resolveInputStep()

    #############################################################################

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
        """Main execution function."""

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

            poolCat = PoolXMLCatalog(self.poolXMLCatName)

            self._resolveInputVariables()

            stepOutputs, stepOutputTypes, _histogram = self._determineOutputs()

            logLines = ["#" * len(LHCbDIRAC.version), LHCbDIRAC.version, "#" * len(LHCbDIRAC.version)]

            localInputs = [str(list(poolCat.getPfnsByLfn(x)["Replicas"].values())[0]) for x in self.stepInputData]
            inputs = " ".join(localInputs)
            cmd = f"cat {inputs} > {self.outputFilePrefix + '.' + stepOutputTypes[0]}"
            logLines.append("\nExecuting merge operation...")
            self.log.info(f'Executing "{cmd}"')
            result = systemCall(timeout=600, cmdSeq=shlex.split(cmd))
            if not result["OK"]:
                self.log.error(result)
                logLines.append(f"Merge operation failed with result:\n{result}")
                return S_ERROR("Problem Executing Application")

            status = result["Value"][0]
            stdout = result["Value"][1]
            stderr = result["Value"][2]
            self.log.info(stdout)
            if stderr:
                self.log.error(stderr)

            if status:
                msg = f'Non-zero status {status} while executing "{cmd}"'
                self.log.info(msg)
                logLines.append(msg)
                return S_ERROR("Problem Executing Application")

            self.log.info(f"Going to manage {self.applicationName} output")
            self._manageAppOutput(stepOutputs)

            # Still have to set the application status e.g. user job case.
            self.setApplicationStatus(f"{self.applicationName} {self.applicationVersion} Successful")

            # Write to log file
            msg = "Produced merged MDF file"
            self.log.info(msg)
            logLines.append(msg)
            logLines = [str(i) for i in logLines]
            logLines.append("#EOF")
            with open(self.applicationLog, "w") as fopen:
                fopen.write("\n".join(logLines) + "\n")

            return S_OK(f"{self.applicationName} {self.applicationVersion} Successful")

        except Exception as e:  # pylint:disable=broad-except
            self.log.exception("Failure in MergeMDF execute module", lException=e)
            return S_ERROR(str(e))

        finally:
            super().finalize()


# EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#
