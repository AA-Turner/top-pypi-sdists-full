""" CTA specific RegisterReplica class to handle lfns starting with both the old and new VO name """

from DIRAC import S_ERROR, S_OK
from DIRAC.DataManagementSystem.Agent.RequestOperations.RegisterReplica import (
    RegisterReplica,
)
from DIRAC.DataManagementSystem.Client.DataManager import DataManager

from CTADIRAC.DataManagementSystem.Agent.RequestOperations.CTADMSRequestOperationsBase import (
    CTADMSRequestOperationsBase,
)

########################################################################


class CTARegisterReplica(RegisterReplica, CTADMSRequestOperationsBase):
    def __call__(self):
        """call me maybe"""

        self._initMonitoring()
        # # counter for failed replicas

        failedReplicas = 0
        # # catalog to use
        catalogs = self._prepareCatalogs()
        # # get waiting files
        waitingFiles = self.getWaitingFilesList()

        self._recordMonitoring("Attempted", len(waitingFiles))

        # # loop over files
        registerOperations = {}
        successReplicas = 0

        targetSE = self.operation.targetSEList[0]
        replicaTuples = [(opFile.LFN, opFile.PFN, targetSE) for opFile in waitingFiles]

        ## LA: Added for CTA-DIRAC Legacy
        first_lfn = replicaTuples[0][0]
        voName = first_lfn.split("/")[1]
        self.dm = DataManager(vo=voName)

        registerReplica = self.dm.registerReplica(replicaTuples, catalogs)

        for opFile in waitingFiles:
            lfn = opFile.LFN
            # # check results
            if not registerReplica["OK"] or lfn in registerReplica["Value"]["Failed"]:
                # There have been some errors
                self._recordMonitoring("Failed", 1)
                #        self.dataLoggingClient().addFileRecord( lfn, "RegisterReplicaFail", ','.join( catalogs )
                # if catalogs else "all catalogs", "", "RegisterReplica" )

                self._handleOpsFailure(
                    registerReplica,
                    registerOperations,
                    lfn,
                    targetSE,
                    opFile,
                    catalogs,
                    failedReplicas,
                )
            else:
                # All is OK
                if self.rmsMonitoring:
                    self._recordMonitoring("Successful", 1)
                else:
                    successReplicas += 1
                    self.log.verbose(
                        "Replica %s has been registered at %s"
                        % (lfn, ",".join(catalogs) if catalogs else "all catalogs")
                    )

                opFile.Status = "Done"

        # # if we have new replications to take place, put them at the end
        if registerOperations:
            self.log.info(f"adding {len(registerOperations)} operations to the request")
        for operation in registerOperations.values():
            self.operation._parent.addOperation(operation)

        self._commitMonitoring()

        return self._finalStatus(successReplicas, failedReplicas)

    def _prepareCatalogs(self):
        catalogs = self.operation.Catalog
        if catalogs:
            return [cat.strip() for cat in catalogs.split(",")]
        return []

    def _handleOpsFailure(
        self,
        registerReplica,
        registerOperations,
        lfn,
        targetSE,
        opFile,
        catalogs,
        failedReplicas,
    ):
        #        self.dataLoggingClient().addFileRecord( lfn, "RegisterReplicaFail", ','.join( catalogs )
        # if catalogs else "all catalogs", "", "RegisterReplica" )
        reason = registerReplica.get(
            "Message",
            registerReplica.get("Value", {}).get("Failed", {}).get(lfn, "Unknown"),
        )
        errorStr = f"failed to register LFN {lfn}: {str(reason)}"
        # FIXME: this is incompatible with the change made in the DM that we
        # ignore failures if successful in at least one catalog
        if lfn in registerReplica.get("Value", {}).get("Successful", {}) and isinstance(
            reason, dict
        ):
            # As we managed, let's create a new operation for just the remaining registration
            errorStr += " - adding registerReplica operations to request"
            self._handleFailedCatlogs(registerOperations, reason, targetSE, opFile)
            opFile.Status = "Done"
        else:
            opFile.Error = errorStr
            self._fileNotExistsInFC(reason, opFile, lfn, targetSE, catalogs)

            if opFile.Status != "Done":
                failedReplicas += 1

        self.log.warn(errorStr)

    def _fileNotExistsInFC(self, reason, opFile, lfn, targetSE, catalogs):
        catMaster = True
        if isinstance(reason, dict):
            from DIRAC.Resources.Catalog.FileCatalog import FileCatalog

            for failedCatalog in reason:
                catMaster = catMaster and FileCatalog()._getCatalogConfigDetails(
                    failedCatalog
                ).get("Value", {}).get("Master", False)
        # If one targets explicitly a catalog and it fails or if it fails on the master catalog
        if (catalogs or catMaster) and (
            "file does not exist" in opFile.Error.lower()
            or "no such file" in opFile.Error.lower()
        ):
            # Check if the file really exists in SE, if not, consider this file registration as Done
            res = self.dm.getReplicaMetadata(lfn, targetSE)
            notExist = bool(
                "No such file" in res.get("Value", {}).get("Failed", {}).get(lfn, "")
            )
            if not notExist:
                opFile.Status = "Failed"
            else:
                opFile.Status = "Done"

    def _handleFailedCatlogs(self, registerOperations, reason, targetSE, opFile):
        for failedCatalog in reason:
            key = f"{targetSE}/{failedCatalog}"
            newOperation = self.getRegisterOperation(
                opFile,
                targetSE,
                type="RegisterReplica",
                catalog=failedCatalog,
            )
            if key not in registerOperations:
                registerOperations[key] = newOperation
            else:
                registerOperations[key].addFile(newOperation[0])

    def _finalStatus(self, successReplicas, failedReplicas):
        infoStr = ""
        if successReplicas:
            infoStr = "%d replicas successfully registered" % successReplicas
        if failedReplicas:
            infoStr += ", %d replicas failed to register" % failedReplicas
        self.log.info(f"All replicas processed {infoStr}")
        if failedReplicas:
            self.operation.Error = "some replicas failed to register"
            return S_ERROR(self.operation.Error)

        return S_OK()
