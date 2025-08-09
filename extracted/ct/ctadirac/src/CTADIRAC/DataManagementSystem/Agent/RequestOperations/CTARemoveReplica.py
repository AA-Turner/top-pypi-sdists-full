from DIRAC import S_OK
from DIRAC.DataManagementSystem.Agent.RequestOperations.RemoveReplica import (
    RemoveReplica,
)
from DIRAC.DataManagementSystem.Client.DataManager import DataManager

from CTADIRAC.DataManagementSystem.Agent.RequestOperations.CTADMSRequestOperationsBase import (
    CTADMSRequestOperationsBase,
)


class CTARemoveReplica(RemoveReplica, CTADMSRequestOperationsBase):
    """CTA specific RemoveReplica class to handle lfns starting with both the old and new VO name."""

    def __call__(self):
        """Remove replicas."""

        self._initMonitoring()
        # # prepare list of targetSEs
        targetSEs = self.operation.targetSEList
        # # check targetSEs for removal
        bannedTargets = self.checkSEsRSS(targetSEs, access="RemoveAccess")
        if not bannedTargets["OK"]:
            self._recordMonitoring(["Attempted", "Failed"], len(self.operation))
            self._commitMonitoring()
            return bannedTargets

        if bannedTargets["Value"]:
            return S_OK(
                f"{','.join(bannedTargets['Value'])} targets are banned for removal"
            )

        # # get waiting files
        waitingFiles = self.getWaitingFilesList()
        # # and prepare dict
        toRemoveDict = {opFile.LFN: opFile for opFile in waitingFiles}
        ## LA: Added for CTA-DIRAC Legacy
        first_lfn = next(iter(toRemoveDict))
        voName = first_lfn.split("/")[1]
        self.dm = DataManager(vo=voName)

        self.log.info(
            f"Todo: {len(toRemoveDict)} replicas to delete from {len(targetSEs)} SEs"
        )

        self._recordMonitoring("Attempted", len(toRemoveDict))

        # # keep status for each targetSE
        removalStatus = {lfn: dict.fromkeys(targetSEs, None) for lfn in toRemoveDict}

        # # loop over targetSEs
        for targetSE in targetSEs:
            self._processTargetSE(targetSE, toRemoveDict, removalStatus)

        # # update file status for waiting files
        failed = self._updateOpFileStatus(removalStatus)

        if failed:
            self.operation.Error = f"failed to remove {failed} replicas"

        self._commitMonitoring()

        return S_OK()

    def _processTargetSE(self, targetSE, toRemoveDict, removalStatus):
        self.log.info(f"Removing replicas at {targetSE}")
        # # 1st step - bulk removal
        bulkRemoval = self._bulkRemoval(toRemoveDict, targetSE)
        if not bulkRemoval["OK"]:
            self.log.error(f"Bulk replica removal failed {bulkRemoval['Message']}")

            self._commitMonitoring()

            return bulkRemoval

        # # report removal status for successful files
        opFiles = [opFile for opFile in toRemoveDict.values() if not opFile.Error]
        self._recordMonitoring("Successful", len(opFiles))

        # # 2nd step - process the rest again
        toRetry = {lfn: opFile for lfn, opFile in toRemoveDict.items() if opFile.Error}
        for lfn, opFile in toRetry.items():
            self._removeWithOwnerProxy(opFile, targetSE)
            if opFile.Error:
                self._recordMonitoring("Failed", 1)
                removalStatus[lfn][targetSE] = opFile.Error
            else:
                self._recordMonitoring("Successful", 1)

    def _updateOpFileStatus(self, removalStatus):
        failed = 0
        for opFile in self.operation:
            if opFile.Status == "Waiting":
                errors = list(
                    {err for err in removalStatus[opFile.LFN].values() if err}
                )
                if errors:
                    opFile.Error = "\n".join(errors)
                    # This seems to be the only unrecoverable error
                    if "Write access not permitted for this credential" in opFile.Error:
                        failed += 1
                        opFile.Status = "Failed"
                else:
                    opFile.Status = "Done"

        return failed
