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
""" Gaudi Application module - main module: creates the environment,
    executes gaudirun with the right options

    This is the module used for each and every job of productions. It can also be used by users.
"""
import json
import os

from DIRAC import S_OK, S_ERROR, gLogger, gConfig
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations

from LHCbDIRAC.Core.Utilities.ProductionOptions import getDataOptions, getModuleOptions
from LHCbDIRAC.Workflow.Modules.ModuleBase import ModuleBase
from LHCbDIRAC.Core.Utilities.RunApplication import RunApplication, LHCbApplicationError, LHCbDIRACError


class GaudiApplication(ModuleBase):
    """GaudiApplication class."""

    def __init__(self, bkClient=None, dm=None):
        """Usual init for LHCb workflow modules."""

        self.log = gLogger.getSubLogger("GaudiApplication")
        super().__init__(self.log, bkClientIn=bkClient, dm=dm)

        self.systemConfig = ""
        self.stdError = ""
        self.inputDataType = "MDF"
        self.stepInputData = []  # to be resolved
        self.poolXMLCatName = "pool_xml_catalog.xml"
        self.optionsFile = ""
        self.optionsLine = ""
        self.extraOptionsLine = ""
        self.eventTimeout = None
        self.extraPackages = ""
        self.jobType = ""

    def _resolveInputVariables(self):
        """Resolve all input variables for the module here."""

        super()._resolveInputVariables()
        super()._resolveInputStep()

    def execute(
        self,
        production_id=None,
        prod_job_id=None,
        wms_job_id=None,
        workflowStatus=None,
        stepStatus=None,
        wf_commons=None,
        step_commons=None,
        step_id=None,
        step_number=None,
    ):
        """The main execution method of GaudiApplication.

        It runs a gaudirun app using RunApplication module. This is the
        module used for each and every job of productions. It can also be
        used by users.
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

            if not self._checkWFAndStepStatus():
                return S_OK()

            self._resolveInputVariables()

            self.log.info(
                "Executing application %s %s for binary tag %s"
                % (self.applicationName, self.applicationVersion, self.systemConfig)
            )

            if self.jobType in Operations().getValue("Productions/DisableWatchdog", ["Merge"]) and self._WMSJob():
                self._disableWatchdogCPUCheck()

            # Resolve options files
            if self.optionsFile.startswith("{"):
                commandOptions = json.loads(self.optionsFile)
                self.log.info("Found lbexec style configuration:", commandOptions)
            else:
                commandOptions = []
                if self.optionsFile and self.optionsFile != "None":
                    commandOptions += self.optionsFile.split(";")
                self.log.info("Final options files:", ", ".join(commandOptions))

            runNumberGauss = 0
            firstEventNumberGauss = 0
            if self.applicationName.lower() == "gauss" and self.production_id and self.prod_job_id:
                if self.jobType.lower() == "user":
                    eventsMax = self.numberOfEvents
                else:
                    # maintaining backward compatibility
                    eventsMax = self.maxNumberOfEvents if self.maxNumberOfEvents else self.numberOfEvents
                runNumberGauss = int(self.production_id) * 100 + int(self.prod_job_id)
                firstEventNumberGauss = eventsMax * (int(self.prod_job_id) - 1) + 1

            if self.optionsLine or self.jobType.lower() == "user":
                self.log.debug("Won't get any step outputs (USER job)")
                stepOutputs = []
                stepOutputTypes = []
                histogram = False
            else:
                self.log.debug("Getting the step outputs")
                stepOutputs, stepOutputTypes, histogram = self._determineOutputs()
                self.log.debug(
                    "stepOutputs, stepOutputTypes, histogram  ==>  %s, %s, %s"
                    % (stepOutputs, stepOutputTypes, histogram)
                )

            # Simple check for slow processors: auto increase of Event Timeout
            eventTimeout = self.eventTimeout
            cpuNormalization = int(gConfig.getValue("/LocalSite/CPUNormalizationFactor", 10))
            if cpuNormalization < 10:
                if not eventTimeout:
                    eventTimeout = 3600
                eventTimeout = int(eventTimeout * 10 / cpuNormalization)

            if self.optionsLine or self.jobType.lower() == "user":
                # Prepare standard project run time options
                generatedOpts = "gaudi_extra_options.py"
                if os.path.exists(generatedOpts):
                    os.remove(generatedOpts)
                inputDataOpts = getDataOptions(
                    self.applicationName, self.stepInputData, self.inputDataType, self.poolXMLCatName
                )[
                    "Value"
                ]  # always OK
                projectOpts = getModuleOptions(
                    self.applicationName,
                    self.numberOfEvents,
                    inputDataOpts,
                    self.optionsLine,
                    runNumberGauss,
                    firstEventNumberGauss,
                    self.jobType,
                )[
                    "Value"
                ]  # always OK
                self.log.info(f"Extra options generated for {self.applicationName} {self.applicationVersion} step:")
                print(
                    projectOpts
                )  # Always useful to see in the logs (don't use gLogger as we often want to cut n' paste)
                with open(generatedOpts, "w") as options:
                    options.write(projectOpts)
                # TODO Don't do this with lbexec
                commandOptions.append(generatedOpts)

            # How to run the application
            ra = RunApplication(
                self,
                commandOptions,
                stepOutputTypes,
                histogram,
                runNumberGauss,
                firstEventNumberGauss,
                eventTimeout,
            )

            # Now really running
            self.setApplicationStatus(f"{self.applicationName} step {self.step_number}")
            ra.run()  # This would trigger an exception in case of failure, or application status != 0

            self.log.info(f"Going to manage {self.applicationName} output")
            self._manageAppOutput(stepOutputs)

            # Still have to set the application status e.g. user job case.
            self.setApplicationStatus(f"{self.applicationName} {self.applicationVersion} Successful")

            return S_OK(f"{self.applicationName} {self.applicationVersion} Successful")
        except LHCbApplicationError as lbae:  # This is the case for real application errors
            self.setApplicationStatus(repr(lbae))
            return S_ERROR(str(lbae))
        except LHCbDIRACError as lbde:  # This is the case for LHCbDIRAC errors (e.g. subProcess call failed)
            self.setApplicationStatus(repr(lbde))
            return S_ERROR(str(lbde))
        except Exception as exc:  # pylint:disable=broad-except
            self.log.exception("Failure in GaudiApplication execute module", lException=exc, lExcInfo=True)
            self.setApplicationStatus("Error in GaudiApplication module")
            return S_ERROR(str(exc))
        finally:
            super().finalize()
