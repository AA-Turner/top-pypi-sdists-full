###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import annotations

from DIRAC import gLogger
from DIRAC.Core.Utilities.ReturnValues import DReturnType, returnValueOrRaise, convertToReturnValue
from .FileQueryUtils import TableJoins, buildQuery, combineDescription, TABLE_JOIN_TO_NAME


GETFILESWITHMETADATA_AVAILABLE_COLUMNS = {
    "filename": None,
    "eventstat": None,
    "filesize": None,
    "creationdate": None,
    "jobstart": TableJoins.JOBS,
    "jobend": TableJoins.JOBS,
    "workernode": TableJoins.JOBS,
    "name": TableJoins.FILETYPES,
    "runnumber": TableJoins.JOBS,
    "fillnumber": TableJoins.JOBS,
    "fullstat": None,
    "dataqualityflag": TableJoins.DATAQUALITY,
    "eventinputstat": TableJoins.JOBS,
    "totalluminosity": TableJoins.JOBS,
    "luminosity": None,
    "instluminosity": None,
    "tck": TableJoins.JOBS,
    "guid": None,
    "adler32": None,
    "eventtypeid": None,
    "md5sum": None,
    "visibilityflag": None,
    "jobid": TableJoins.JOBS,
    "gotreplica": None,
    "inserttimestamp": None,
}

GETFILESWITHMETADATA_NAME_TO_COL = {
    "FileName": "filename",
    "EventStat": "eventstat",
    "FileSize": "filesize",
    "CreationDate": "creationdate",
    "JobStart": "jobstart",
    "JobEnd": "jobend",
    "WorkerNode": "workernode",
    "FileType": "name",
    "RunNumber": "runnumber",
    "FillNumber": "fillnumber",
    "FullStat": "fullstat",
    "DataqualityFlag": "dataqualityflag",
    "EventInputStat": "eventinputstat",
    "TotalLuminosity": "totalluminosity",
    "Luminosity": "luminosity",
    "InstLuminosity": "instluminosity",
    "TCK": "tck",
    "GUID": "guid",
    "ADLER32": "adler32",
    "EventType": "eventtypeid",
    "MD5SUM": "md5sum",
    "VisibilityFlag": "visibilityflag",
    "JobId": "jobid",
    "GotReplica": "gotreplica",
    "InsertTimeStamp": "inserttimestamp",
}


class NewOracleBookkeepingDB:
    def __init__(self, *, dbW, dbR):
        self.log = gLogger.getSubLogger("LegacyOracleBookkeepingDB")
        self.dbW_ = dbW
        self.dbR_ = dbR

    def getAvailableFileTypes(self) -> DReturnType[list[str]]:
        """Retrieve all available file types from the database."""
        return self.dbR_.executeStoredProcedure("BOOKKEEPINGORACLEDB.getAvailableFileTypes", [])

    @convertToReturnValue
    def getFileTypesForProdID(self, prodID: int) -> list[str]:
        query_parts = [
            "SELECT DISTINCT filetypes.name",
            "FROM files, jobs, filetypes",
            "WHERE files.jobid = jobs.jobid AND jobs.production = :prodid AND filetypes.filetypeid = files.filetypeid",
        ]
        result = returnValueOrRaise(self.dbR_.query(" ".join(query_parts), kwparams={"prodid": prodID}))
        return [ft for ft, in result]

    @convertToReturnValue
    def getAvailableSMOG2States(self) -> list[str]:
        """Retrieve all available SMOG2 states."""
        result = returnValueOrRaise(self.dbR_.query("SELECT state FROM smog2"))
        return [state for state, in result]

    @convertToReturnValue
    def getRunsForSMOG2(self, state: str) -> list[int]:
        """Retrieve all runs with specified SMOG2 state

        :param str state: required state
        """
        query = "SELECT runs.runnumber FROM smog2 LEFT JOIN runs ON runs.smog2_id = smog2.id WHERE smog2.state = :state"
        result = returnValueOrRaise(self.dbR_.query(query, kwparams={"state": state}))
        return [run for run, in result]

    def setSMOG2State(self, state: str, update: bool, runs: list[int]) -> DReturnType[None]:
        """Set SMOG2 state for runs.

        :param str state: state for given runs
        :param bool update: when True, updates existing state, when False throw an error in such case
        :param list[int] runs: runs list
        """
        return self.dbW_.executeStoredProcedure(
            "BOOKKEEPINGORACLEDB.setSMOG2", parameters=[state, update], output=False, array=runs
        )

    def setExtendedDQOK(self, run: int, update: bool, dqok: list[str]) -> DReturnType[None]:
        """Set ExtendedDQOK for specified run and systems. In case update is allowed,
        not specified systems are unset for the run.

        :param int run: run number for which systems are specified
        :param bool update: when True, updates existing set, when False throw an error in such case
        :param list[str] dqok: list of system names
        """
        return self.dbW_.executeStoredProcedure(
            "BOOKKEEPINGORACLEDB.setExtendedDQOK", parameters=[run, update, dqok], output=False
        )

    @convertToReturnValue
    def getRunsWithExtendedDQOK(self, dqok: list[str]) -> list[int]:
        """Retrieve all runs with specified systems in ExtendedDQOK
        NOTE: it is NOT checking quality is set to OK, so it should NOT be used
        for end user operations.

        :param list[str] dqok: systems
        """
        if not dqok:
            return []
        sql = ["SELECT ok.runnumber FROM extendeddqok ok"]
        params = {"sysname0": dqok[0]}
        for i, system in enumerate(dqok[1::]):
            sql.append(
                f"INNER JOIN extendeddqok ok{i} ON ok{i}.runnumber = ok.runnumber AND ok{i}.systemname = :sysname{i}"
            )
            params[f"sysname{i}"] = system
        sql.append("WHERE ok.systemname = :sysname0")
        result = returnValueOrRaise(self.dbR_.query(" ".join(sql), kwparams=params))
        return [run for run, in result]

    @convertToReturnValue
    def getRunExtendedDQOK(self, runnb: int) -> list[str]:
        """Return the list of systems in ExtendedDQOK for given run

        :param int runnb: run number
        """
        query = "SELECT systemname FROM extendeddqok WHERE runnumber = :run"
        result = returnValueOrRaise(self.dbR_.query(query, kwparams={"run": runnb}))
        return [sysname for sysname, in result]

    @convertToReturnValue
    def getAvailableExtendedDQOK(self) -> list[str]:
        """Retrieve all available Extended DQOK systems."""
        result = returnValueOrRaise(self.dbR_.query("select distinct systemname from extendeddqok"))
        return [systemname for systemname, in result]

    @convertToReturnValue
    def getListOfRunsInProd(self, prod_id) -> list[int]:
        query = "SELECT DISTINCT j.runnumber FROM jobs j WHERE j.production = :prod_id"
        result = returnValueOrRaise(self.dbR_.query(query, kwparams={"prod_id": prod_id}))
        return [run for run, in result]

    @convertToReturnValue
    def getInputOutputFilesForProd(self, prod_id, run_number):
        query_parts = [
            "SELECT f2.filename aname, f.filename dname, f.gotreplica, dt.name dtype",
            "FROM jobs j",
            "LEFT JOIN files f ON j.jobid = f.jobid AND j.production = f.production",
            "LEFT JOIN filetypes dt ON dt.filetypeid = f.filetypeid",
            "LEFT JOIN inputfiles i ON i.jobid = j.jobid",
            "LEFT JOIN files f2 ON i.fileid = f2.fileid",
            "where j.production = :prod_id",
        ]
        kwparams = {"prod_id": prod_id}
        if run_number is not None:
            query_parts.append("AND j.runnumber = :run_number")
            kwparams["run_number"] = run_number
        result = returnValueOrRaise(self.dbR_.query("\n".join(query_parts), kwparams=kwparams))
        return {
            "Records": result,
            "ParameterNames": ["AncestorLFN", "DescendantLFN", "GotReplica", "FileType"],
            "TotalRecords": len(result),
        }

    @convertToReturnValue
    def getOutputDescendantsForProd(self, prod_id, run_number):
        query_parts = [
            "SELECT f.filename AS aname,",
            "    f2.filename AS dname,",
            "    f2.gotreplica,",
            "    ft2.name",
            "FROM jobs j",
            "LEFT JOIN files f ON j.jobid = f.jobid AND j.production = f.production",
            "INNER JOIN inputfiles i ON i.fileid = f.fileid",
            "LEFT JOIN jobs j2 ON j2.jobid = i.jobid",
            "LEFT JOIN files f2 ON j2.jobid = f2.jobid AND j2.production = f2.production",
            "LEFT JOIN filetypes ft2 ON ft2.filetypeid = f2.filetypeid",
            "WHERE j.production = :prod_id",
        ]
        kwparams = {"prod_id": prod_id}
        if run_number is not None:
            query_parts.append("AND j.runnumber = :run_number")
            kwparams["run_number"] = run_number
        result = returnValueOrRaise(self.dbR_.query("\n".join(query_parts), kwparams=kwparams))
        return {
            "Records": result,
            "ParameterNames": ["AncestorLFN", "DescendantLFN", "GotReplica", "FileType"],
            "TotalRecords": len(result),
        }

    def _collectFileDescendents(
        self, lfns: list[str], depth: int, production: int, checkreplica: bool, tree: bool
    ) -> dict:
        """collects descendents for specified ancestors

        :param list lfns: a list of LFNs (ancestors)
        :param int depth: the depth of the processing pass chain(how far to go)
        :param productin: production number, when not zero, search descendats in that production only
        :param bool checkreplica: when set, returned descendents should have a replica
        :param bool tree: return direct ancestors relations when true
        :returns: descendent relations and metadata
        """
        # max number of lfns to process in one query, should be less then 1000 (with current implementation)
        block_size = 100
        # allowed depth range as in original version
        depth = min(10, max(1, depth))

        processed = dict.fromkeys(lfns, False)  # to detect "NotProcessed"
        dfiles = {lfn: {} for lfn in lfns}  # requested ancestors are always included
        metadata = {}

        sql_fields = [
            f"{'PRIOR' if tree else 'CONNECT_BY_ROOT'} f.filename aname",
            "f.filename dname",
            "f.gotreplica",
            "f.eventstat",
            "f.eventtypeid",
            "f.luminosity",
            "f.instluminosity",
            "dt.name dtype",
            "j.production" if production != 0 else "0",
        ]
        sql_fields = ", ".join(sql_fields)

        sql_joins = [
            "LEFT JOIN inputfiles i ON i.fileid = f.fileid",
            "LEFT JOIN filetypes dt ON dt.filetypeid = f.filetypeid",
        ]
        if production != 0:
            sql_joins.append("LEFT JOIN jobs j ON j.jobid = f.jobid")
        sql_joins = " ".join(sql_joins)

        sql_where = f"LEVEL > 1 AND LEVEL < {depth+2}"  # LEVEL 1 is ancestor, depth is inclusive
        sql_connect = "PRIOR i.jobid = f.jobid"

        block_idx = 0
        while True:
            block_lfns = lfns[block_idx : block_idx + block_size :]
            if not block_lfns:
                break
            block_idx += block_size  # for the next block
            # bind as proposed in https://python-oracledb.readthedocs.io/en/latest/user_guide/bind.html , 7.13
            sql_start = "f.filename IN (" + ",".join([f":{i}" for i in range(1, len(block_lfns) + 1)]) + ")"

            sql = (
                f"SELECT {sql_fields} FROM files f {sql_joins} WHERE {sql_where}"
                f" START WITH {sql_start} CONNECT BY {sql_connect}"
            )
            result = returnValueOrRaise(self.dbR_.query(sql, params=[block_lfns]))
            for aname, dname, gotreplica, eventstat, eventtype, lumi, instlumi, dtype, prod in result:
                if aname in processed:  # for tree == true case
                    processed[aname] = True  # mimic previous behaviour ("processed" if there is any descendant)
                if (not checkreplica or (gotreplica != "No")) and (
                    prod == production
                ):  # should work correctly for production == 0
                    if aname not in dfiles:  # can happened when tree == true
                        dfiles[aname] = {}
                    dfiles[aname][dname] = {}
                    metadata[dname] = {
                        "GotReplica": gotreplica,
                        "EventStat": eventstat,
                        "EventType": eventtype,
                        "Luminosity": lumi,
                        "InstLuminosity": instlumi,
                        "FileType": dtype,
                    }
                elif tree:  # in case of tree, we need all relations to build it
                    if aname not in dfiles:
                        dfiles[aname] = {}
                    dfiles[aname][dname] = {}

        return processed, dfiles, metadata

    @convertToReturnValue
    def getFileDescendents(
        self, lfns: list[str], depth: int = 0, production: int = 0, checkreplica: bool = True
    ) -> dict:
        """collects descendents for specified ancestors

        :param list lfns: a list of LFNs (ancestors)
        :param int depth: the depth of the processing pass chain(how far to go)
        :param productin: production number, when not zero, search descendats in that production only
        :param bool checkreplica: when set, returned descendents should have a replica
        :returns: descendents and suplementary information
        """
        # AZ: original code never fail, it returns "Failed" list in case of problems with Oracle.
        #     So the behaviour is NOT identical when there are problems with Oracle
        # AZ: the order of files in lists of "Successful" is different from original (dictionary "WithMetadata" should match)
        if not lfns:
            return {"Failed": [], "NotProcessed": [], "Successful": {}, "WithMetadata": {}}
        processed, dfiles, metadata = self._collectFileDescendents(lfns, depth, production, checkreplica, False)
        return {
            "Failed": [],  # always emtpy (or error) in this implementation
            "NotProcessed": [lfn for lfn in lfns if not processed[lfn]],  # preserve original order
            "Successful": {lfn: list(dfiles[lfn]) for lfn in dfiles if processed[lfn]},
            "WithMetadata": {lfn: {dlfn: metadata[dlfn] for dlfn in dfiles[lfn]} for lfn in dfiles if processed[lfn]},
        }

    @convertToReturnValue
    def getFileDescendentsTree(
        self, lfns: list[str], depth: int = 0, production: int = 0, checkreplica: bool = True
    ) -> dict:
        """collects descendents for specified ancestors

        :param list lfns: a list of LFNs (ancestors)
        :param int depth: the depth of the processing pass chain(how far to go)
        :param productin: production number, when not zero, search descendats in that production only
        :param bool checkreplica: when set, returned descendents should have a replica
        :returns: the tree of descendents and metadata (metadata are filteres)
        """
        if not lfns:
            return {"descendents": {}, "metadata": {}}
        _, dfiles, metadata = self._collectFileDescendents(lfns, depth, production, checkreplica, True)
        if checkreplica or production != 0:
            # cleanup by removing branches to not interesting files
            # not interesting (not in metadata) leafs (not in dfiles)
            for lfn in dfiles:
                to_clean = [dlfn for dlfn in dfiles[lfn] if dlfn not in metadata and dlfn not in dfiles]
                for dlfn in to_clean:
                    del dfiles[lfn][dlfn]
            # iteratively remove not interesting branches
            while True:
                to_clean = [lfn for lfn in dfiles if lfn not in metadata and lfn not in lfns and not dfiles[lfn]]
                if not to_clean:
                    break
                for lfn in to_clean:
                    for dlfn in dfiles:
                        if lfn in dfiles[dlfn]:
                            del dfiles[dlfn][lfn]
                    del dfiles[lfn]
        for lfn in dfiles:  # make the tree from direct descendents
            dfiles[lfn].update({dlfn: dfiles[dlfn] if dlfn in dfiles else {} for dlfn in dfiles[lfn]})
        return {"descendents": {lfn: dfiles[lfn] for lfn in lfns}, "metadata": metadata}

    @convertToReturnValue
    def getFiles(
        self,
        simdesc,
        datataking,
        procPass,
        ftype,
        evt,
        configName="ALL",
        configVersion="ALL",
        production="ALL",
        flag="ALL",
        startDate=None,
        endDate=None,
        nbofEvents=False,
        startRunID=None,
        endRunID=None,
        runnumbers=None,
        replicaFlag="ALL",
        visible="ALL",
        filesize=False,
        tcks=None,
        jobStart=None,
        jobEnd=None,
        smog2States=None,
        dqok=None,
        seed_md5=None,
        sample_max=None,
    ):
        if nbofEvents:
            selection = "SUM(f.eventstat)"
        elif filesize:
            selection = "SUM(f.filesize)"
        else:
            # TODO: Ideally DISTINCT shouldn't be needed here but we should
            # probably add a unique constraint to the DB before removing it.
            # Actually, the previous two queries don't consider the DISTINCT
            # so if it's needed here those queries are incorrect.
            selection = "DISTINCT f.filename"

        return buildQuery(
            self.dbR_,
            selection,
            combineDescription(simdesc, datataking),
            procPass,
            ftype,
            evt,
            configName,
            configVersion,
            production,
            flag,
            startDate,
            endDate,
            startRunID,
            endRunID,
            runnumbers,
            replicaFlag,
            visible,
            tcks,
            jobStart,
            jobEnd,
            smog2States,
            dqok,
            seed_md5,
            sample_max,
        )

    @convertToReturnValue
    def getFilesWithMetadata(
        self,
        configName,
        configVersion,
        conddescription="ALL",
        processing="ALL",
        evt="ALL",
        production="ALL",
        filetype="ALL",
        quality="ALL",
        visible="ALL",
        replicaflag="ALL",
        startDate=None,
        endDate=None,
        runnumbers=None,
        startRunID=None,
        endRunID=None,
        tcks="ALL",
        jobStart=None,
        jobEnd=None,
        selection=None,
        smog2States=None,
        dqok=None,
        seed_md5=None,
        sample_max=None,
        *,
        parameters=None,
    ):
        if selection is not None:
            raise NotImplementedError("Selection is not implemented")

        forceJoins = []
        if parameters is None:
            parameters = list(GETFILESWITHMETADATA_NAME_TO_COL)
        selection = []
        for parameter in parameters:
            col = GETFILESWITHMETADATA_NAME_TO_COL[parameter]
            join = GETFILESWITHMETADATA_AVAILABLE_COLUMNS[col]
            selection.append(f"{TABLE_JOIN_TO_NAME[join]}.{col}")
            if join is not None:
                forceJoins.append(join)

        return buildQuery(
            self.dbR_,
            ", ".join(selection),
            conddescription,
            processing,
            filetype,
            evt,
            configName,
            configVersion,
            production,
            quality,
            startDate,
            endDate,
            startRunID,
            endRunID,
            runnumbers,
            replicaflag,
            visible,
            tcks,
            jobStart,
            jobEnd,
            smog2States,
            dqok,
            seed_md5,
            sample_max,
            forceJoins=forceJoins,
            # FIXME: Arguably this is a bug but it's needed to reproduce the behaviour of the original code
            # After we've migrated to the new method we should probably remove this?
            extraConditions={"f.eventtypeid IS NOT NULL"},
        )

    @convertToReturnValue
    def getVisibleFilesWithMetadata(
        self,
        simdesc,
        datataking,
        procPass,
        ftype,
        evt,
        configName="ALL",
        configVersion="ALL",
        production="ALL",
        flag="ALL",
        startDate=None,
        endDate=None,
        nbofEvents=None,
        startRunID=None,
        endRunID=None,
        runnumbers=None,
        replicaFlag="Yes",
        tcks=None,
        jobStart=None,
        jobEnd=None,
        smog2States=None,
        dqok=None,
        seed_md5=None,
        sample_max=None,
    ):
        # These options are broken the in the original code
        if nbofEvents is not None:
            raise NotImplementedError("nbofEvents is not implemented for visible files")
        if replicaFlag != "Yes":
            raise NotImplementedError("This option is broken in the original code")

        selection = (
            "DISTINCT f.filename, f.eventstat, j.eventinputstat, j.runnumber, j.fillnumber, f.filesize, "
            "j.totalluminosity, f.luminosity, f.instLuminosity, j.tck"
        )
        return buildQuery(
            self.dbR_,
            selection,
            combineDescription(simdesc, datataking),
            procPass,
            ftype,
            evt,
            configName,
            configVersion,
            production,
            flag,
            startDate,
            endDate,
            startRunID,
            endRunID,
            runnumbers,
            replicaFlag,
            "Y",
            tcks,
            jobStart,
            jobEnd,
            smog2States,
            dqok,
            seed_md5,
            sample_max,
            forceJoins={TableJoins.JOBS},
        )

    @convertToReturnValue
    def getFilesSummary(
        self,
        configName,
        configVersion,
        conditionDescription="ALL",
        processingPass="ALL",
        eventType="ALL",
        production="ALL",
        fileType="ALL",
        dataQuality="ALL",
        startRun="ALL",
        endRun="ALL",
        visible="ALL",
        startDate=None,
        endDate=None,
        runNumbers=None,
        replicaFlag="ALL",
        tcks="ALL",
        jobStart=None,
        jobEnd=None,
        smog2States=None,
        dqok=None,
        seed_md5=None,
        sample_max=None,
    ):
        selection = "COUNT(fileid), SUM(f.EventStat), SUM(f.FILESIZE), SUM(f.luminosity), SUM(f.instLuminosity)"
        return buildQuery(
            self.dbR_,
            selection,
            conditionDescription,
            processingPass,
            fileType,
            eventType,
            configName,
            configVersion,
            production,
            dataQuality,
            startDate,
            endDate,
            startRun,
            endRun,
            runNumbers,
            replicaFlag,
            visible,
            tcks,
            jobStart,
            jobEnd,
            smog2States,
            dqok,
            seed_md5,
            sample_max,
        )
