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
"""Utility for invoking running LHCb applications."""
import asyncio
import json
import shlex
import subprocess

from DIRAC import gLogger, gConfig, S_OK
from DIRAC.WorkloadManagementSystem.Utilities.RemoteRunner import RemoteRunner
from LHCbDIRAC.Workflow.Modules.ModulesUtilities import getEventsToProduce


class LHCbApplicationError(RuntimeError):
    """Exception for application errors."""


class LHCbDIRACError(RuntimeError):
    """Exception for application errors."""


class RunApplication:
    """Encapsulate logic for running an LHCb application."""

    def __init__(
        self,
        gaudiAppModule,
        commandOptions,
        stepOutputTypes,
        histogram,
        runNumberGauss,
        firstEventNumberGauss,
        eventTimeout,
    ):
        self.log = gLogger.getSubLogger("RunApplication")

        self.applicationName = gaudiAppModule.applicationName
        self.cleanedApplicationName = gaudiAppModule.cleanedApplicationName
        self.applicationVersion = gaudiAppModule.applicationVersion
        self.prmonPath = "/cvmfs/lhcb.cern.ch/lib/experimental/prmon/bin/prmon"
        self.usePrmon = gaudiAppModule.usePrmon

        if gaudiAppModule.executable != "gaudirun.py":
            raise LHCbDIRACError(f"gaudiAppModule.executable={gaudiAppModule.executable!r} is not supported")

        self.prodConfFileName = "prodConf_{}_{}_{}_{}.json".format(
            self.cleanedApplicationName,
            gaudiAppModule.production_id,
            gaudiAppModule.prod_job_id,
            gaudiAppModule.step_number,
        )
        self.numberOfProcessors = gaudiAppModule.numberOfProcessors
        self.applicationLog = gaudiAppModule.applicationLog or "applicationLog.txt"
        self.stdError = gaudiAppModule.stdError or self.applicationLog

        # Sanity checks
        if not gaudiAppModule.stepInputData and self.applicationName.lower() != "gauss":
            raise RuntimeError("No MC, but no input data")
        if gaudiAppModule.TCK and gaudiAppModule.mcTCK:
            raise RuntimeError(f"{self.applicationName} step: TCK set in step, and should't be!")

        # Initialise the prodInfo object
        prodInfo = {
            "spec_version": 1,
            "application": {
                "data_pkgs": [".".join(p) for p in gaudiAppModule.extraPackages],
                "name": self.applicationName,
                "number_of_processors": self.numberOfProcessors,
                "version": gaudiAppModule.applicationVersion,
            },
            "options": {},
            "db_tags": {},
            "input": {
                "files": ["LFN:" + sid for sid in gaudiAppModule.stepInputData],
                "first_event_number": firstEventNumberGauss,
                "tck": gaudiAppModule.TCK if gaudiAppModule.TCK else gaudiAppModule.mcTCK,
                "xml_file_catalog": gaudiAppModule.poolXMLCatName,
                "xml_summary_file": gaudiAppModule.XMLSummary,
            },
            "output": {
                "prefix": gaudiAppModule.outputFilePrefix,
                "types": stepOutputTypes,
            },
        }
        if gaudiAppModule.applicationVersion.startswith("{"):
            appInfo = json.loads(gaudiAppModule.applicationVersion)
            if prodInfo["application"]["name"] != appInfo["name"]:
                raise RuntimeError(f"Application name mismatch: {prodInfo['application']['name']} != {appInfo['name']}")
            if appInfo.get("binary_tag") is not None:
                if gaudiAppModule.systemConfig != appInfo["binary_tag"]:
                    raise RuntimeError(
                        f"System config mismatch: {gaudiAppModule.systemConfig} != {appInfo['binary_tag']}"
                    )
            prodInfo["application"]["version"] = appInfo["version"]
            if appInfo.get("nightly"):
                prodInfo["application"]["nightly"] = appInfo["nightly"]

        # application
        if gaudiAppModule.systemConfig and gaudiAppModule.systemConfig.lower() != "any":
            prodInfo["application"]["binary_tag"] = gaudiAppModule.systemConfig
        prodInfo["application"]["event_timeout"] = eventTimeout

        # options
        if isinstance(commandOptions, dict):
            # This is an lbexec style application
            prodInfo["options"] = commandOptions
        else:
            prodInfo["options"]["files"] = commandOptions
            prodInfo["options"]["processing_pass"] = gaudiAppModule.processingPass
            if gaudiAppModule.optionsFormat:
                prodInfo["options"]["format"] = gaudiAppModule.optionsFormat
            if gaudiAppModule.extraOptionsLine:
                prodInfo["options"]["gaudi_extra_options"] = gaudiAppModule.extraOptionsLine

        # db_tags
        if gaudiAppModule.DDDBTag:
            if gaudiAppModule.DDDBTag.lower() == "online":
                try:
                    prodInfo["db_tags"]["dddb_tag"] = gaudiAppModule.onlineDDDBTag
                    self.log.debug("Set the online DDDB tag")
                except NameError:
                    self.log.exception("Could not find online DDDb Tag")
                    raise RuntimeError("Could not find online DDDb Tag")
            else:
                prodInfo["db_tags"]["dddb_tag"] = gaudiAppModule.DDDBTag

        if gaudiAppModule.condDBTag:
            prodInfo["db_tags"]["conddb_tag"] = (
                gaudiAppModule.onlineCondDBTag
                if gaudiAppModule.condDBTag.lower() == "online"
                else gaudiAppModule.condDBTag
            )

        if gaudiAppModule.dqTag:
            prodInfo["db_tags"]["dq_tag"] = gaudiAppModule.dqTag

        # input
        if (
            self.applicationName.lower() == "gauss"
            and gaudiAppModule.CPUe
            and gaudiAppModule.maxNumberOfEvents
            and gaudiAppModule.numberOfEvents <= 0
        ):
            # Here we set maxCPUTime to 24 hours, which seems reasonable
            prodInfo["input"]["n_of_events"] = getEventsToProduce(
                gaudiAppModule.CPUe, maxNumberOfEvents=gaudiAppModule.maxNumberOfEvents, jobMaxCPUTime=86400
            )
        else:
            prodInfo["input"]["n_of_events"] = gaudiAppModule.numberOfEvents

        if runNumberGauss:
            prodInfo["input"]["run_number"] = runNumberGauss
        if gaudiAppModule.runNumber and gaudiAppModule.runNumber not in ("Unknown", "Multiple"):
            prodInfo["input"]["run_number"] = gaudiAppModule.runNumber

        # output
        if histogram:
            prodInfo["output"]["histogram_file"] = gaudiAppModule.histoName

        with open(self.prodConfFileName, "w") as fp:
            json.dump(prodInfo, fp, indent=2)

    def run(self):
        """Invokes lb-prod-run (what you call after having setup the object)"""
        returncode, stdout, stderr = asyncio.get_event_loop().run_until_complete(self._runApp())
        if returncode != 0:
            self.log.error("lb-run or its application exited with status %d" % returncode)
            self.log.error(stderr)
            raise LHCbApplicationError(
                f"{self.applicationName} {self.applicationVersion} exited with status {returncode}"
            )

        return S_OK((returncode, stdout, stderr))

    async def _runApp(self):
        command = ["lb-prod-run", self.prodConfFileName, "--prmon", "--verbose"]
        if self.applicationName == "Gauss" and self.usePrmon:
            command = [self.prmonPath, "--json-summary", "./prmon_Gauss.json", "--"] + command
        self.log.notice("Running command", shlex.join(command))

        stdout = ""
        stderr = ""
        if gConfig.getValue("/LocalSite/RemoteExecution", False):
            remoteRunner = RemoteRunner(
                gConfig.getValue("/LocalSite/Site"),
                gConfig.getValue("/LocalSite/GridCE"),
                gConfig.getValue("/LocalSite/CEQueue"),
            )
            outputDict = remoteRunner.execute(shlex.join(command), numberOfProcessors=self.numberOfProcessors)
            if not outputDict["OK"]:
                returncode = outputDict["Errno"]
                stderr = outputDict["Message"]
            else:
                returncode, stdout, stderr = outputDict["Value"]

            self._handleRemoteOutput(stdout, self.applicationLog)
            self._handleRemoteOutput(stderr, self.stdError)
        else:
            proc = await asyncio.create_subprocess_exec(
                *command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout_fh = None
            if self.applicationLog:
                stdout_fh = open(self.applicationLog, "a")

            stderr_fh = None
            if self.stdError == self.applicationLog:
                stderr_fh = stdout_fh
            elif self.stdError:
                stderr_fh = open(self.applicationLog, "a")

            try:
                await asyncio.gather(
                    self._handleOutput(proc.stdout, stdout_fh),
                    self._handleOutput(proc.stderr, stderr_fh),
                    proc.wait(),
                )
            finally:
                if stdout_fh:
                    stdout_fh.close()
                if stderr_fh and stdout_fh != stderr_fh:
                    stderr_fh.close()
            returncode = proc.returncode
        return (returncode, stdout, stderr)

    async def _handleOutput(self, stream, fh):
        """Process the output of a current local execution"""
        while line := await stream.readline():
            line = line.decode(errors="backslashreplace")
            self._handleLine(line)
            if fh:
                fh.write(line)

    def _handleRemoteOutput(self, lines, filename):
        """Process the output of a remote execution"""
        if filename:
            with open(filename, "a") as log:
                log.write(lines)
        for line in lines.split("\n"):
            self._handleLine(line)

    def _handleLine(self, line):
        """Print a given line to the standard output if related to an event"""
        if "INFO Evt" in line or "Reading Event record" in line or "lb-run" in line:
            # These ones will appear in the std.out log too
            print(line.rstrip())
