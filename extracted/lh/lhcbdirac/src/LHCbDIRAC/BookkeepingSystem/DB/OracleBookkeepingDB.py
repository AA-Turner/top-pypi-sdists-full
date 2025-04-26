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
from __future__ import annotations

import os
import time
from typing import Any
from collections.abc import Callable

from DIRAC import gLogger, gConfig
from DIRAC.ConfigurationSystem.Client.PathFinder import getDatabaseSection
from DIRAC.Core.Utilities.ReturnValues import DReturnType
from DIRAC.FrameworkSystem.private.standardLogging.LoggingRoot import LoggingRoot

from .OracleDB import OracleDB
from .LegacyOracleBookkeepingDB import LegacyOracleBookkeepingDB
from .NewOracleBookkeepingDB import NewOracleBookkeepingDB


DCallable = Callable[..., DReturnType[Any]]


class OracleBookkeepingDB:
    """Proxy class which routes calls to the legacy or new OracleBookkeepingDB implementation.

    This class has three modes of operation:

    * By default it call methods in ``LegacyOracleBookkeepingDB`` by default and only use ``NewOracleBookkeepingDB``
        if the requested method is not implemented in ``LegacyOracleBookkeepingDB``.
    * If ``LHCBDIRAC_BOOKKEEPING_DO_COMPARE`` is set, it will call both implementations and compare the results for
        methods which are implemented in both and deemed safe to compare. If the results differ, it will log a warning.
        The safety of calling a method is determined by the ``DUPLICATION_SAFE_METHODS`` variable.
    * The ``LHCBDIRAC_BOOKKEEPING_METHODS_PREFER_NEW`` environment variable is a comma separated list that can be used
        to force the proxy to prefer the new implementation for specific methods.
    """

    def __init__(self, *, host: str = None, username: str = None, password: str = None, **kwargs):
        self.log = gLogger.getSubLogger("ProxyOracleBookkeepingDB")
        self._legacydb = LegacyOracleBookkeepingDB(
            dbR=OracleDB(**kwargs, **_init_kwargs(with_write=False, username=username, password=password, host=host)),
            dbW=OracleDB(**kwargs, **_init_kwargs(with_write=True, username=username, password=password, host=host)),
        )
        self._newdb = NewOracleBookkeepingDB(
            dbR=OracleDB(**kwargs, **_init_kwargs(with_write=False, username=username, password=password, host=host)),
            dbW=OracleDB(**kwargs, **_init_kwargs(with_write=True, username=username, password=password, host=host)),
        )

    def __dir__(self) -> list[str]:
        return list(set(dir(self._legacydb)) | set(dir(self._newdb)))

    def __getattr__(self, name: str) -> DCallable:
        legacy_impl = getattr(self._legacydb, name, None)
        new_impl = getattr(self._newdb, name, None)
        if legacy_impl is None and new_impl is None:
            raise AttributeError(f"{self.__name!r} object has no attribute {name!r}")

        # If we only find it on one of the implementations, just return that callable
        if legacy_impl is None:
            return new_impl
        if new_impl is None:
            return legacy_impl

        # Check which implementation we prefer according to the environment variable
        if name in METHODS_PREFER_NEW:
            self.log.debug("Preferring new implementation", f"for {name}")
            preferred_impl = new_impl
            reference_impl = legacy_impl
        else:
            self.log.debug("Preferring old implementation", f"for {name}")
            preferred_impl = legacy_impl
            reference_impl = new_impl

        if not DO_COMPARE:
            return preferred_impl

        # Check if the method is safe for duplication (i.e. read-only)
        if name not in DUPLICATION_SAFE_METHODS:
            self.log.debug("Method is not safe for duplication", f"for {name}")
            return preferred_impl

        return ProxyMethod(self.log, preferred_impl, reference_impl)


def _init_kwargs(*, with_write: bool, username: str = None, password: str = None, host: str = None) -> dict[str, str]:
    """Get the connection keyword arguments for the OracleDB constructor.

    For any parameters which are not specified, the values are read from
    ``gConfig``. If ``username`` is not given, the ``with_write`` parameter
    determines whether the ``LHCbDIRACBookkeepingUser`` (read-only) or
    ``LHCbDIRACBookkeepingServer`` (read-write) configuration option is used.
    """
    cs_path = getDatabaseSection("Bookkeeping", "BookkeepingDB")

    if host is None:
        result = gConfig.getOption(cs_path + "/LHCbDIRACBookkeepingTNS")
        if not result["OK"]:
            raise ValueError("Failed to get the configuration parameters: LHCbDIRACBookkeepingTNS")
        host = result["Value"]

    if username is None:
        if with_write:
            result = gConfig.getOption(cs_path + "/LHCbDIRACBookkeepingServer")
        else:
            result = gConfig.getOption(cs_path + "/LHCbDIRACBookkeepingUser")
        if not result["OK"]:
            raise ValueError("Failed to get the configuration parameter for username", f"for {with_write=}")
        username = result["Value"]

    if password is None:
        result = gConfig.getOption(cs_path + "/LHCbDIRACBookkeepingPassword")
        if not result["OK"]:
            raise ValueError("Failed to get the configuration parameters: LHCbDIRACBookkeepingPassword")
        password = result["Value"]

    return dict(
        userName=username,
        password=password,
        tnsEntry=host,
        confDir=gConfig.getValue(cs_path + "/LHCbDIRACBookkeepingConfDir", ""),
        mode=gConfig.getValue(cs_path + "/LHCbDIRACBookkeepingMode", ""),
    )


class ProxyMethod:
    """Callable class which calls the two bookkeeping database implementations and logs the results."""

    def __init__(self, log: LoggingRoot, preferred_impl: DCallable | None, reference_impl: DCallable | None):
        self.log = log
        self.preferred_impl = preferred_impl
        self.reference_impl = reference_impl

    def __call__(self, *args, **kwargs):
        start = time.perf_counter()
        result = self.preferred_impl(*args, **kwargs)
        preferred_duration = time.perf_counter() - start

        start = time.perf_counter()
        reference = self.reference_impl(*args, **kwargs)
        reference_duration = time.perf_counter() - start

        error_message = None
        if {result["OK"], reference["OK"]} == {True, False}:
            error_message = "One implementation errored while the other did not"
        elif result["OK"]:
            if self.name in USE_SET_COMPARISON:
                try:
                    result_set = set(result["Value"])
                    reference_set = set(reference["Value"])
                except Exception as e:
                    error_message = f"Error while comparing sets: {e}"
                else:
                    if result_set != reference_set:
                        error_message = "Legacy and new methods returned different results"
                    if len(result_set) != len(result["Value"]):
                        error_message = "Legacy method returned duplicate results"
                    if len(reference_set) != len(reference["Value"]):
                        error_message = "New method returned duplicate results"
            elif result != reference:
                error_message = "Legacy and new methods returned different results"

        if error_message is None:
            diff_duration = preferred_duration - reference_duration
            diff_desc = "faster" if diff_duration > 0 else "slower"
            diff_rel = abs(diff_duration) / preferred_duration
            varmsg = (
                f"for {self.name}, reference was {abs(diff_duration):.4f} seconds {diff_desc} ({diff_rel:.1%}) "
                f"with {args=} {kwargs=}"
            )
            if diff_rel > 0.5 and diff_duration < -1:
                self.log.warn("Legacy and new methods matched but reference is notably slower", varmsg)
            else:
                self.log.info("Legacy and new methods matched", varmsg)
        else:
            msgresult = str(result)[:1000] if result["OK"] else result
            msgreference = str(reference)[:1000] if reference["OK"] else reference
            varmsg = (
                f"for {self.name} with {args=} {kwargs=}:\n"
                f"{self.preferred_name} gave {msgresult!r} in {preferred_duration:.4f} seconds\n"
                f"{self.reference_name} gave {msgreference!r} in {reference_duration:.4f} seconds"
            )
            self.log.warn(error_message, varmsg)
            if FAIL_ON_DIFFERENCE:
                raise BookkeepingResultMismatch(f"{error_message} {varmsg}")

        return result

    @property
    def name(self) -> str:
        return self.preferred_impl.__name__

    @property
    def preferred_name(self) -> str:
        return self.preferred_impl.__self__.__class__.__name__

    @property
    def reference_name(self) -> str:
        return self.reference_impl.__self__.__class__.__name__


class BookkeepingResultMismatch(Exception):
    pass


METHODS_PREFER_NEW = os.environ.get("LHCBDIRAC_BOOKKEEPING_METHODS_PREFER_NEW", "").split(",")
FAIL_ON_DIFFERENCE = os.environ.get("LHCBDIRAC_BOOKKEEPING_FAIL_ON_DIFFERENCE", "") == "True"
DO_COMPARE = os.environ.get("LHCBDIRAC_BOOKKEEPING_DO_COMPARE") == "True"
# Some methods don't have a well defined order of results, so we need to compare them as sets
USE_SET_COMPARISON = {
    "getFiles",
    "getFilesWithMetadata",
    "getVisibleFilesWithMetadata",
}
DUPLICATION_SAFE_METHODS = [
    # "addProcessing",
    # "addProduction",
    # "addProductionSteps",
    # "addReplica",
    # "bulkgetIDsFromFilesTable",
    # "bulkinsertEventType",
    # "bulkJobInfo",
    # "bulkupdateEventType",
    # "bulkupdateFileMetaData",
    # "checkEventType",
    # "checkfile",
    # "checkFileTypeAndVersion",
    # "checkProcessingPassAndSimCond",
    # "deleteCertificationData",
    # "deleteDataTakingCondition",
    # "deleteFile",
    # "deleteFiles",
    # "deleteInputFiles",
    # "deleteJob",
    # "deleteProductionsContainer",
    # "deleteSimulationConditions",
    # "deleteStep",
    # "deleteStepContainer",
    # "exists",
    # "existsTag",
    # "fixRunLuminosity",
    # "getAvailableConfigNames",
    # "getAvailableConfigurations",
    # "getAvailableDataQuality",
    # "getAvailableEventTypes",
    "getAvailableFileTypes",
    # "getAvailableProductions",
    # "getAvailableRuns",
    # "getAvailableSteps",
    # "getAvailableTags",
    # "getAvailableTagsFromSteps",
    # "getConditions",
    # "getConfigsAndEvtType",
    # "getConfigVersions",
    # "getDataTakingCondDesc",
    # "getDataTakingCondId",
    # "getDirectoryMetadata",
    # "getEventTypes",
    # "getFileAncestorHelper",
    # "getFileAncestors",
    # "getFileCreationLog",
    "getFileDescendents",
    # "getFileHistory",
    # "getFileMetadata",
    "getFiles",
    # "getFilesForGUID",
    "getFilesSummary",
    "getFilesWithMetadata",
    # "getFileTypes",
    # "getFileTypeVersion",
    # "getInputFiles",
    # "getJobInfo",
    # "getJobInformation",
    # "getJobInputOutputFiles",
    # "getLimitedFiles",
    # "getListOfFills",
    # "getListOfRuns",
    # "getMoreProductionInformations",
    # "getNbOfJobsBySites",
    # "getNbOfRawFiles",
    # "getOutputFiles",
    # "getProcessingPass",
    # "getProcessingPassId",
    # "getProcessingPassSteps",
    # "getProductionFiles",
    # "getProductionFilesBulk",
    # "getProductionFilesForWeb",
    # "getProductionFilesStatus",
    # "getProductionInformation",
    # "getProductionNbOfEvents",
    # "getProductionNbOfFiles",
    # "getProductionNbOfJobs",
    # "getProductionOutputFileTypes",
    # "getProductionProcessedEvents",
    # "getProductionProcessingPass",
    # "getProductionProcessingPassID",
    # "getProductionProcessingPassSteps",
    # "getProductionProducedEvents",
    # "getProductions",
    # "getProductionsFromView",
    # "getProductionSimulationCond",
    # "getProductionSizeOfFiles",
    # "getProductionSummary",
    # "getProductionSummaryFromView",
    # "getRunAndProcessingPass",
    # "getRunAndProcessingPassDataQuality",
    # "getRunConfigurationsAndDataTakingCondition",
    # "getRunFiles",
    # "getRunFilesDataQuality",
    # "getRunInformation",
    # "getRunInformations",
    # "getRunNbAndTck",
    # "getRunNumber",
    # "getRunProcessingPass",
    # "getRuns",
    # "getRunsForAGivenPeriod",
    # "getRunsForFill",
    # "getRunsGroupedByDataTaking",
    # "getRunStatus",
    # "getRuntimeProjects",
    # "getRunWithProcessingPassAndDataQuality",
    # "getSimConditions",
    # "getSimulationConditions",
    # "getStepIdandNameForRUN",
    # "getStepInputFiles",
    # "getStepOutputFiles",
    # "getSteps",
    # "getStepsMetadata",
    # "getTCKs",
    "getVisibleFilesWithMetadata",
    # "insertDataTakingCond",
    # "insertDataTakingCondDesc",
    # "insertEventTypes",
    # "insertFileTypes",
    # "insertInputFile",
    # "insertJob",
    # "insertOutputFile",
    # "insertProductionOutputFiletypes",
    # "insertproductionscontainer",
    # "insertRunStatus",
    # "insertRuntimeProject",
    # "insertSimConditions",
    # "insertStep",
    # "insertTag",
    # "removeReplica",
    # "removeRuntimeProject",
    # "renameFile",
    # "setFileDataQuality",
    # "setFilesInvisible",
    # "setFilesVisible",
    # "setProductionDataQuality",
    # "setRunAndProcessingPassDataQuality",
    # "setRunDataQuality",
    # "setRunStatusFinished",
    # "setStepInputFiles",
    # "setStepOutputFiles",
    # "updateEventType",
    # "updateFileMetaData",
    # "updateProductionOutputfiles",
    # "updateReplicaRow",
    # "updateRuntimeProject",
    # "updateSimulationConditions",
    # "updateStep",
]
