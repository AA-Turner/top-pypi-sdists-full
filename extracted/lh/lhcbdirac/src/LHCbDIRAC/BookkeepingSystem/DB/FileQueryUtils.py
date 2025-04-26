###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import annotations

import sys
from enum import StrEnum

from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise


class TableJoins(StrEnum):
    """Enum class to store the table joins for the query.

    This class is used to store the table joins for when using the files table.
    The order of the values in the enum is important as it is used to order
    the joins in the query to ensure dependent tables are joined first.
    """

    JOBS = "JOIN jobs j ON f.jobid = j.jobid AND f.production = j.production"
    PRODUCTIONSCONTAINER = "JOIN productionscontainer cont ON f.production = cont.production"
    CONFIGURATIONS = "JOIN configurations c ON cont.configurationid = c.configurationid"
    FILETYPES = "JOIN filetypes ft ON f.filetypeid = ft.filetypeid"
    DATAQUALITY = "JOIN dataquality d ON f.qualityid = d.qualityid"
    CONDESC = "JOIN condesc cd ON (cont.simid = cd.simid OR cont.daqperiodid = cd.daqid)"
    PROCPATHS = "JOIN procpaths pp ON pp.id = cont.processingid"
    RUNS = "JOIN runs ON runs.runnumber = j.runnumber"
    SMOG2STATE = "JOIN smog2 s2s ON runs.smog2_id = s2s.id"

    TMP_PRODUCTION = "JOIN LHCB_DIRACBOOKKEEPING.temp_query_production tmp_p ON f.production = tmp_p.production"
    TMP_FILETYPES = "JOIN LHCB_DIRACBOOKKEEPING.temp_query_filetype tmp_ft ON ft.name = tmp_ft.name"

    @staticmethod
    def sort_key(value: str) -> int:
        try:
            return list(TableJoins).index(value)
        except ValueError:
            return sys.maxsize


TABLE_JOIN_TO_NAME = {
    None: "f",
    TableJoins.JOBS: "j",
    TableJoins.CONFIGURATIONS: "c",
    TableJoins.PRODUCTIONSCONTAINER: "cont",
    TableJoins.FILETYPES: "ft",
    TableJoins.DATAQUALITY: "d",
    TableJoins.CONDESC: "cd",
    TableJoins.PROCPATHS: "pp",
    TableJoins.RUNS: "runs",
    TableJoins.SMOG2STATE: "s2s",
}
JOIN_TO_TEMP_TABLE = {
    TableJoins.TMP_PRODUCTION: "temp_query_production",
    TableJoins.TMP_FILETYPES: "temp_query_filetype",
}

CTE_PROCPATHS_FULL = (
    "procpaths (procpath, id) as (\n"
    "    SELECT distinct SUBSTR(SYS_CONNECT_BY_PATH(name, '/'), 2), id\n"
    "    FROM processing\n"
    "    START WITH id in (select distinct id from processing where parentid is NULL)\n"
    "    CONNECT BY NOCYCLE PRIOR id=parentid\n"
    ")"
)
# If we're filtering on :procpath split it by / and only keep potentially
# relavant rows from the processing table to reduce the query's cost
CTE_PROCPATHS_FILTERED = (
    "procpaths (procpath, id) AS (\n"
    "    SELECT SUBSTR(SYS_CONNECT_BY_PATH(name, '/'), 2) as procpath, id\n"
    "    FROM (\n"
    "        select * from processing where name in (\n"
    "            SELECT REGEXP_SUBSTR(:procPass, '[^/]+', 1, LEVEL)\n"
    "            FROM dual\n"
    "            CONNECT BY REGEXP_SUBSTR(:procPass, '[^/]+', 1, LEVEL) IS NOT NULL\n"
    "        )\n"
    "    )\n"
    "    START WITH id IN (SELECT DISTINCT id FROM processing WHERE name = REGEXP_SUBSTR(:procPass, '[^/]+', 1, 1))\n"
    "    CONNECT BY NOCYCLE PRIOR id = parentid\n"
    ")"
)
CTE_CONDESC = (
    "condesc (daqid, simid, description) as (\n"
    "    SELECT distinct DAQPERIODID, NULL, DESCRIPTION FROM data_taking_conditions\n"
    "    UNION\n"
    "    SELECT distinct NULL, simid, simdescription FROM simulationConditions\n"
    ")"
)


def field_condition_builder_via_temp_table(
    join: TableJoins,
    values: str | int | list[str | int],
    pre_inserts: list[tuple[str, list[tuple[str]]]],
    joins: set[TableJoins],
) -> None:
    """Helper function to build a condition for a column with a single value or a list of values.

    This function adds an entry to the pre_inserts list to insert the values into a temporary table.
    The function also adds the corresponding join to the set of joins.
    """
    insert_stmt = f"INSERT INTO LHCB_DIRACBOOKKEEPING.{JOIN_TO_TEMP_TABLE[join]} VALUES (:1)"
    if isinstance(values, (str, int)):
        values = [values]
    pre_inserts.append((insert_stmt, [(value,) for value in values]))
    joins.add(join)


def field_condition_builder_via_params(
    column: str,
    value: str | int | list[str | int],
    param_prefix: str,
    kwparams: dict[str, str | int],
    conditions: set[str],
) -> None:
    """Helper function to build a condition for a column with a single value or a list of values.

    The function adds the condition to the set of conditions and updates the kwparams dictionary with the
    appropriate parameters. Parameters are named with the prefix followed by a number, starting from 0 for
    the first value in the list.

    The prefix must be unique for each column, as the function will overwrite the parameters in the kwparams.
    """
    if isinstance(value, (str, int)):
        conditions.add(f"{column} = :{param_prefix}")
        kwparams[param_prefix] = value
    elif isinstance(value, (list, tuple)):
        if len(set(value)) > 100:
            raise NotImplementedError(f"Too many values for IN clause on {column}, should use temp table")
        parameters = {f"{param_prefix}{j}": prod for j, prod in enumerate(value)}
        kwparams.update(parameters)
        conditions.add(f"{column} IN ({', '.join(f':{x}' for x in parameters)})")
    else:
        raise TypeError(f"Invalid type for {column}: {type(value)}")


def combineDescription(simdesc, datataking):
    """Combine the simulation description and data taking description.

    TODO: The calling code should be refactored to remove the separate handling of simdesc and datataking.
    """
    if simdesc is None or simdesc == "ALL":
        return datataking
    if datataking is None or datataking == "ALL":
        return None
    if simdesc != datataking:
        raise ValueError(f"Conditions inconsistency: {simdesc=} {datataking=}")
    return datataking


def buildQuery(
    dbR,
    selection,
    conddescription,
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
    *,
    forceJoins=None,
    extraConditions=None,
):
    joins = set()
    ctes = set()
    pre_inserts = []
    if forceJoins:
        joins.update(forceJoins)
    conditions = set()
    if extraConditions:
        conditions.update(extraConditions)
    kwparams = {}

    # TODO: When checking for all we should apply str.upper() if it's a string
    if configName is not None and configName != "ALL":
        joins.add(TableJoins.PRODUCTIONSCONTAINER)
        joins.add(TableJoins.CONFIGURATIONS)
        conditions.add("c.configname = :configName")
        kwparams["configName"] = configName

    if configVersion is not None and configVersion != "ALL":
        joins.add(TableJoins.PRODUCTIONSCONTAINER)
        joins.add(TableJoins.CONFIGURATIONS)
        conditions.add("c.configversion = :configVersion")
        kwparams["configVersion"] = configVersion

    if production is not None and production != "ALL":
        joins.add(TableJoins.PRODUCTIONSCONTAINER)
        field_condition_builder_via_temp_table(TableJoins.TMP_PRODUCTION, production, pre_inserts, joins)

    if tcks is not None and tcks != "ALL" and tcks:
        joins.add(TableJoins.JOBS)
        field_condition_builder_via_params("j.tck", tcks, "tck", kwparams, conditions)

    if procPass is not None and procPass != "ALL":
        procPass = procPass.lstrip("/")
        joins.add(TableJoins.PRODUCTIONSCONTAINER)
        joins.add(TableJoins.PROCPATHS)
        ctes.add(CTE_PROCPATHS_FILTERED)
        # TODO: We probably need to support like here for some other methods
        conditions.add("pp.procpath = :procPass")
        kwparams["procPass"] = procPass

    if ftype is not None and ftype != "ALL" and ftype:
        joins.add(TableJoins.FILETYPES)
        field_condition_builder_via_temp_table(TableJoins.TMP_FILETYPES, ftype, pre_inserts, joins)

    if runnumbers is not None and runnumbers != "ALL" and runnumbers:
        # As far as I can tell LegacyOracleBookkeepingDB has bizarre behavior
        # if both runnumbers and startRunID/endRunID are specified so let's
        # see if we can get away with not supporting both.
        if startRunID is not None and startRunID != "ALL":
            raise NotImplementedError("Both runnumbers and startRunID are specified")
        if endRunID is not None and endRunID != "ALL":
            raise NotImplementedError("Both runnumbers and endRunID are specified")
        joins.add(TableJoins.JOBS)
        field_condition_builder_via_params("j.runnumber", runnumbers, "run", kwparams, conditions)

    if startRunID is not None and startRunID != "ALL":
        joins.add(TableJoins.JOBS)
        conditions.add("j.runnumber >= :startRunID")
        kwparams["startRunID"] = startRunID

    if endRunID is not None and endRunID != "ALL":
        joins.add(TableJoins.JOBS)
        conditions.add("j.runnumber <= :endRunID")
        kwparams["endRunID"] = endRunID

    if evt != 0 and evt is not None and evt != "ALL" and evt:
        field_condition_builder_via_params("f.eventtypeid", evt, "evt", kwparams, conditions)

    if startDate is not None and startDate != "ALL":
        conditions.add("f.inserttimestamp >= TO_TIMESTAMP (:startDate,'YYYY-MM-DD HH24:MI:SS')")
        kwparams["startDate"] = startDate

    # TODO __buildStartenddate uses utcnow for some reason, seems useless but someone else should check
    if endDate is not None and endDate != "ALL":
        conditions.add("f.inserttimestamp <= TO_TIMESTAMP (:endDate,'YYYY-MM-DD HH24:MI:SS')")
        kwparams["endDate"] = endDate

    if jobStart is not None and jobStart != "ALL":
        joins.add(TableJoins.JOBS)
        conditions.add("j.jobstart >= TO_TIMESTAMP (:jobStart,'YYYY-MM-DD HH24:MI:SS')")
        kwparams["jobStart"] = jobStart

    if jobEnd is not None and jobEnd != "ALL":
        joins.add(TableJoins.JOBS)
        conditions.add("j.jobend <= TO_TIMESTAMP (:jobEnd,'YYYY-MM-DD HH24:MI:SS')")
        kwparams["jobEnd"] = jobEnd

    if flag is not None and flag != "ALL" and flag:
        joins.add(TableJoins.DATAQUALITY)
        field_condition_builder_via_params("d.dataqualityflag", flag, "dq", kwparams, conditions)

    if dqok:
        joins.add(TableJoins.JOBS)
        if flag is None or flag == "ALL":
            raise ValueError("DataQuality OK must be explicitly specified to use ExtendedDQOK")
        if isinstance(flag, str):
            flag = [flag]
        if flag != ["OK"]:
            raise ValueError("ExtendedDQOK can be specified with DataQuality=OK only")
        if isinstance(dqok, str):
            dqok = [dqok]
        for i, system in enumerate(set(dqok)):
            joins.add(f"JOIN extendeddqok dqok{i} ON dqok{i}.runnumber = j.runnumber")
            conditions.add(f"dqok{i}.systemname = :dqok{i}")
            kwparams[f"dqok{i}"] = system

    if replicaFlag is not None and replicaFlag != "ALL":
        conditions.add("f.gotreplica = :replicaFlag")
        kwparams["replicaFlag"] = replicaFlag

    if visible is not None and visible != "ALL":
        conditions.add("f.visibilityflag = :visibilityflag")
        kwparams["visibilityflag"] = visible[0].upper()

    if conddescription is not None and conddescription != "ALL":
        joins.add(TableJoins.PRODUCTIONSCONTAINER)
        joins.add(TableJoins.CONDESC)
        ctes.add(CTE_CONDESC)
        conditions.add("cd.description = :conddescription")
        kwparams["conddescription"] = conddescription

    if smog2States is not None and smog2States != "ALL":
        joins.add(TableJoins.RUNS)
        joins.add(TableJoins.SMOG2STATE)
        if isinstance(smog2States, str):
            smog2States = [smog2States]
        smog2States = set(smog2States)
        smog2Conditions = []
        if "Undefined" in smog2States:
            smog2States.remove("Undefined")
            smog2Conditions.append("s2s.id IS NULL")
        if smog2States:
            stateVars = []
            for i, state in enumerate(smog2States):
                kwparams[f"smog2State{i}"] = state
                stateVars.append(f":smog2State{i}")
            smog2Conditions.append(f"s2s.state IN ({', '.join(stateVars)})")
        if len(smog2Conditions) < 2:
            conditions.add(smog2Conditions[0])
        else:
            conditions.add("(" + " OR ".join(smog2Conditions) + ")")

    if seed_md5 or sample_max:
        if not (seed_md5 and sample_max):
            raise ValueError("Both seed_md5 and sample_max MUST be specified.")

        if not (len(seed_md5) == len(sample_max) == 32 and seed_md5.isupper() and sample_max.isupper()):
            raise ValueError("seed_md5 and sample_max must each be 32-character upper-case MD5 hashes.")

        md5_hash_stmt = "STANDARD_HASH(CONCAT(f.filename, :seed_md5), 'MD5')"
        conditions.add(f"({md5_hash_stmt} <= :sample_max)")

        kwparams["seed_md5"] = seed_md5
        kwparams["sample_max"] = sample_max

    query = []
    if ctes:
        query.append("WITH " + ", ".join(ctes))
    query += [
        f"SELECT {selection}",
        "FROM files f",
    ]
    query += sorted(joins, key=TableJoins.sort_key)
    if conditions:
        query.append(f"WHERE {' AND '.join(sorted(conditions))}")
    return returnValueOrRaise(dbR.query("\n".join(query), kwparams=kwparams, pre_inserts=pre_inserts))
