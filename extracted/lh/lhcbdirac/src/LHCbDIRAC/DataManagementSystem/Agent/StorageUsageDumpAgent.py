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
"""
.. versionadded:: v11.0.53

This agent consolidates data from the bookkeeping and the DFC, generates json out of it,
uploads them to a storage.
It also sends the accounting data to OpenSearch, and fill in 2 tables in the StorageUsageDB

.. literalinclude:: ../ConfigTemplate.cfg
  :start-after: ##BEGIN StorageUsageDumpAgent
  :end-before: ##END StorageUsageDumpAgent
  :dedent: 2
  :caption: StorageUsageDumpAgent options

"""
# # imports
import asyncio
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from functools import lru_cache, partial
from pathlib import Path
from textwrap import dedent

from opensearchpy import OpenSearch, helpers

from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Boolean, text, delete, Engine
from sqlalchemy.orm import declarative_base

import numpy as np
import pandas as pd
import zstandard
import time
import re
import boto3
from botocore.exceptions import ClientError

# # from DIRAC
from DIRAC import S_OK, S_ERROR, gLogger, gConfig
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise
from DIRAC.ConfigurationSystem.Client.Utilities import getDBParameters
from DIRAC.DataManagementSystem.DB.FileCatalogDB import FileCatalogDB


from LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB import OracleBookkeepingDB


def nested_defaultdict():
    return defaultdict(nested_defaultdict)


AGENT_NAME = "DataManagement/StorageUsageDumpAgent"

S3_BUCKET_NAME = "lhcbdirac"
S3_ENDPOINT_URL = "https://s3.cern.ch:443"
OS_ENDPOINT_URL = "os-lhcb-dirac.cern.ch:443/os"


# This are directory which should not be considered
BAD_PREFIXES = {
    "/lhcb/data/2008/",
    "/lhcb/testCfg/",
    "/lhcb/EXPFEB2022/",
    "/lhcb/calib/",
    "/lhcb/certification/",
    "/lhcb/swtest/",
    "/lhcb/grid/user/",
    "/lhcb/grid/wg/",
    "/lhcb/prdata/",
}

STREAM_TO_EVENTTYPE = {
    "ION": 90700000,
    "IONRAW": 90800000,
    "TURBORAW": 90400000,
    "BEAMGAS": 97000000,
    "FULL": 90000000,
    "TURBO": 94000000,
    "HLT2CALIB": 95200000,
    "TURCAL": 95100000,
    "NOBIAS": 96000000,
    "PASSTHROUGH": 98100000,
    "LUMI": 93000000,
    "SMOGPHY": 90300000,
    "LOWMULT": 90600000,
    "EXPRESS": 91000000,
    "CALIB": 95000000,
    "ERRORS": 92000000,
    "HLTONE": 98000000,
    "L0YES": 99000000,
}

TAPE_STORAGE_TYPES = ("ARCHIVE", "RAW", "RDST")

# Define the SQLAlchemy model
Base = declarative_base()


class StorageSummary(Base):
    __tablename__ = "dump_storage_summary"

    SEName = Column(String(255), primary_key=True)
    SESize = Column(BigInteger)
    SEFiles = Column(BigInteger)
    SESite = Column(String(255))
    SEType = Column(String(255))
    IsDisk = Column(Boolean)


# Some folders are "duplicated", with case sensitivity issue
# PHYSICS / physics
# ALICE / alice
# +----------------------------------------+---+
# | Name                                   | t |
# +----------------------------------------+---+
# | /lhcb/data/2008/RAW/LHCb/PHYSICS/21188 | 2 |
# | /lhcb/data/2008/RAW/LHCb/PHYSICS/21192 | 2 |
# | /lhcb/data/2008/RAW/RICH2/ALICE/21933  | 2 |
# | /lhcb/data/2008/RAW/RICH2/ALICE/21936  | 2 |
# | /lhcb/data/2008/RAW/RICH2/ALICE/21937  | 2 |
# | /lhcb/data/2008/RAW/RICH2/ALICE/21938  | 2 |
# +----------------------------------------+---+
# that's why we need the specific mysql collate


class DirectoryMetadata(Base):
    __tablename__ = "dump_directory_metadata"

    Name = Column(String(255), primary_key=True)
    production = Column(Integer)
    filetype = Column(String(255))
    online_stream = Column(String(255))
    maybe_eventtype = Column(Integer)
    ConfigName = Column(String(255))
    ConfigVersion = Column(String(255))
    Description = Column(String(255))
    ProcPath = Column(String(255))
    EventTypeID = Column(String(255))

    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_bin"}


async def returnValueOrRaiseAsync(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return returnValueOrRaise(await loop.run_in_executor(None, func, *args, **kwargs))


async def get_prod_data_info():
    """
    Dump the DirectoryUsage table from the DFC for production
    data only.
    We get:
    * directory name
    * storage Element ('FakeSE' for logicial size)
    * size in bytes
    * number of files
    """
    columns = ["Name", "SEName", "SESize", "SEFiles"]
    query = """
    select Name, SEName, du.SESize, du.SEFiles
    from FC_DirectoryList d
    USE INDEX (Name)
    JOIN FC_DirectoryUsage du on d.DirID = du.DirID
    JOIN FC_StorageElements s on du.SEID = s.SEID
    where (Name not like '/lhcb/user/%');
    """
    query = dedent(query.strip())
    return columns, await returnValueOrRaiseAsync(FileCatalogDB()._query, query)


async def get_user_data_info():
    # This takes ~30 minutes to run so we don't run it for now
    columns = ["SEName", "SESize", "SEFiles"]
    query = """
    select SEName, sum(du.SESize), sum(du.SEFiles)
    from FC_DirectoryList d
    JOIN FC_DirectoryUsage du on d.DirID = du.DirID
    JOIN FC_StorageElements s on du.SEID = s.SEID
    where (Name like '/lhcb/user/%') group by SEName;
    """
    query = dedent(query.strip())
    return columns, await returnValueOrRaiseAsync(FileCatalogDB()._query, query)


async def get_bk_metadata() -> tuple[list, list]:
    """
    Dump the production informations from the Bookkeeping:
    * ConfigName: MC, LHCb ...
    * ConfigVersion:2016, Collision18, ...
    * Description: Condition description (Mag polarity, Velo position)
    * ProcPath: Real Data/Reco18 ...
    * EventTypeID: 90700000, 90800000, ...
    * filetype: ALLSTREAM.DST, RAW...
    * production: id of the production, (negative if run number)

    Something like:
    * ('MC', '2016', 'Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8',
    'Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged',
    15266005, 'ALLSTREAMS.MDST', 63445)
    * ('LHCb', 'Collision18', 'Beam6500GeV-VeloClosed-MagDown',
    'Real Data/Reco18/Stripping34/AnaProd-v1r2053-collision_B02DstarpDmKS',
    90000000, 'B02DSTARPDMKS.ROOT', 250478)
    * ('LHCb', 'Collision24', 'Beam2680GeV-VeloClosed-MagUp',
    'Real Data', 95200000, 'RAW', -309550)
    """
    columns = ["ConfigName", "ConfigVersion", "Description", "ProcPath", "EventTypeID", "filetype", "production"]
    query = """
    with procpaths (procpath, id) as (
        SELECT distinct SUBSTR(SYS_CONNECT_BY_PATH(name, '/'), 2), id
        FROM processing
        START WITH id in (select distinct id from processing where parentid is NULL)
        CONNECT BY NOCYCLE PRIOR id=parentid
    ), condesc (daqid, simid, description) as (
        SELECT distinct DAQPERIODID, NULL, DESCRIPTION FROM data_taking_conditions
        UNION
        SELECT distinct NULL, simid, simdescription FROM simulationConditions
    )
    select
        c.configname, c.configversion, condesc.description, procpaths.procpath,
        eventtypes.eventtypeid, ftypes.name as filetype, cont.production
    from productionscontainer cont
    inner join configurations c on cont.configurationid=c.configurationid
    inner join condesc on condesc.daqid=cont.DAQPERIODID or condesc.simid=cont.simid
    inner join procpaths on cont.processingid=procpaths.id
    inner join productionoutputfiles prodoutfiles on prodoutfiles.production=cont.production
    inner join filetypes ftypes on prodoutfiles.filetypeId=ftypes.filetypeid
    inner join eventTypes on eventTypes.EventTypeId=prodoutfiles.eventtypeid
    group by c.configname, c.configversion, condesc.description, procpaths.procpath,
        eventtypes.eventtypeid, ftypes.name, cont.production
    """
    query = dedent(query.strip())
    return columns, await returnValueOrRaiseAsync(OracleBookkeepingDB().dbR_.query, query)


@lru_cache(maxsize=4096)
def se_name_to_type(name: str) -> tuple[str, str]:
    """
    Parses the storage name to return the site and type
    """
    if name.endswith("-EOS"):
        name = name[: -len("-EOS")]
    for t in ["BUFFER", "RAW", "MC-DST", "RDST", "ARCHIVE", "DST", "ANAPROD", "DAQ-EXPORT", "FAILOVER"]:
        if name.endswith(t):
            se_type = t
            se_site = name[: -len(se_type)].strip("-_")
            break
    else:
        se_type = "OTHER"
        # We have a bunch of weird SE's at CERN
        se_site = "CERN" if name.startswith("CERN") else name
    return (se_site, se_type)


@lru_cache(maxsize=4096)
def normalise_eventtype(x: int) -> int:
    """
    Normalizes the event type to group the calibration production event type, eg 90000001 to 90000000
    """
    if not np.isnan(x) and str(int(x)).endswith("1"):
        x = int(str(int(x))[:-1] + "0")
    return x


def find_matching_event_type_row(group):
    """Reduce a group with multiple event types to only the
    one corrosponding to this directory LFN.
    """
    se_name, name = group.name
    # If there is only one entry then there is no mapping to fix
    # e.g. MC where there is only one event type per production
    # e.g. Sprucing where each online stream becomes a different production
    if len(group) == 1:
        return group.iloc[0]
    if len(group["EventTypeID"]) != group["EventTypeID"].nunique():
        raise NotImplementedError(name)
    matches = group["maybe_eventtype"] == group["EventTypeID"]
    if sum(matches) == 0:
        if not group["EventTypeID"].astype(str).str.startswith("9").all():
            raise NotImplementedError("This correction only makes sense for real data")
        # In Run 1 and Run 2 sending to castor instead of offline resulted in an event type ending in a 1
        # See if we get matches after correcting for this
        matches = group["maybe_eventtype"].apply(normalise_eventtype) == group["EventTypeID"].apply(normalise_eventtype)
    if sum(matches) != 1:
        # These corrospond to a tiny fraction of data which is weirdly inconsistent for historical reasons
        # Let them just pick the first match in the group
        if re.search("(?:/FEST/|/2012/RAW/(?:BEAMGAS|HLT1|CALIB)/|/2017/RAW/TEST_MARKUS_CALIB/)", name):
            return group.iloc[0]
        # # TODO: These files are in the DFC but not in the BKK
        if re.search(
            (
                "/(?:133379|133380|133386|133382|133381|133383|"
                "133385|133384|133387|133388|133389|133392|133390|"
                "133391|133394|133395|133393|133398|133399|133400|133396|133397)$"
            ),
            name,
        ):
            return group.iloc[0]
        # If it isn't a known issue, it's better to crash than do the wrong thing
        raise NotImplementedError(name, len(group))
    return group[matches].iloc[0]


def summarise_space(df, group_cols):
    result = nested_defaultdict()
    for _, row in df.groupby(group_cols, dropna=False)["SESize"].sum().reset_index().iterrows():
        result_row = result
        for k in group_cols[:-1]:
            if pd.isna(row[k]) or row[k] == "Unknown":
                if not result["Unknown"]:
                    result["Unknown"] = 0
                result["Unknown"] += int(row["SESize"])
                break
            if k == "ProcPath":
                for k2 in row[k].split("/"):
                    result_row = result_row[k2]
            else:
                result_row = result_row[row[k]]
        else:
            key = row[group_cols[-1]]
            if key in result_row:
                raise NotImplementedError(row)
            result_row[key] = row["SESize"]
    return result2tree(result)


def result2tree(x):
    if isinstance(x, dict):
        return {"children": [{"name": k} | result2tree(v) for k, v in x.items()]}
    elif isinstance(x, int):
        return {"size": x}
    else:
        raise NotImplementedError(x)


def uploadToS3(endpoint_url, bucket_name, access_key, secret_key):
    """
    Uploads to S3 the json data as well as the index.html
    """
    log = gLogger.getSubLogger("uploadToS3")
    log.info("Uploading to S3")
    start_time = time.time()
    s3_client = boto3.client(
        "s3", endpoint_url=endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )

    try:
        s3_client.upload_file(
            "/tmp/storage.json.zst",
            bucket_name,
            "storage-usage/storage.json.zst",
            ExtraArgs={"ACL": "public-read", "ContentType": "application/zstd"},
        )

    except ClientError as e:
        log.exception("Failed to upload storage.json.zst ", lException=e)

    try:
        s3_client.upload_file(
            "/tmp/storage.csv.zst",
            bucket_name,
            "storage-usage/storage.csv.zst",
            ExtraArgs={"ACL": "public-read", "ContentType": "application/zstd"},
        )

    except ClientError as e:
        log.exception("Failed to upload storage.json.zst ", lException=e)

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key="storage-usage/index.html",
            Body=INDEX_HTML,
            ContentType="text/html",
            ACL="public-read",
        )

    except Exception as e:
        log.exception("Failed to upload index.html", lException=e)
    log.info("Upload duration", f"{time.time() - start_time:.2f} secs")


def sendToOpenSearch(df: pd.DataFrame, hosts: str, http_auth: tuple[str, str]):
    """
    Sends the data to OpenSearch
    """
    log = gLogger.getSubLogger("sendToOpenSearch")
    log.info("Sending to OpenSearch")
    start_time = time.time()

    fields = {
        "SEName": {"type": "keyword"},
        "Name": {"type": "keyword"},
        "SESize": {"type": "long"},
        "SEFiles": {"type": "long"},
        "SESite": {"type": "keyword"},
        "SEType": {"type": "keyword"},
        "IsDisk": {"type": "boolean"},
        "production": {"type": "long"},
        "filetype": {"type": "keyword"},
        "maybe_eventtype": {"type": "long"},
        "online_stream": {"type": "keyword"},
        "ConfigName": {"type": "keyword"},
        "ConfigVersion": {"type": "keyword"},
        "Description": {"type": "keyword"},
        "ProcPath": {"type": "keyword"},
        "EventTypeID": {"type": "keyword"},
        "timestamp": {"type": "date"},
    }

    # Create an OpenSearch client
    client = OpenSearch(
        hosts=hosts,
        http_auth=http_auth,
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )

    index_prefix = "lhcb_storageusage_index_"

    template_body = {
        "template": {"mappings": {"properties": fields}},
        "index_patterns": [f"{index_prefix}*"],
        "priority": 5,
    }
    result = client.indices.put_index_template(name=index_prefix, body=template_body)
    assert result["acknowledged"]

    from datetime import datetime, timezone

    utc_now = datetime.now(tz=timezone.utc)
    timestamp = utc_now.strftime("%Y-%m-%dT%H:%M")
    as_date = utc_now.isocalendar()
    index_timestamp = f"{as_date[0]}-{as_date[1]}"

    data = df.reset_index(drop=True).to_dict("records")

    actual_index = f"{index_prefix}{index_timestamp}"
    for entry in data:
        # entry.pop("Unnamed: 0")

        entry["_index"] = actual_index
        entry["_id"] = f"{entry['SEName']}_{entry['Name']}_{timestamp}"
        entry["timestamp"] = utc_now

    succeeded = []
    failed = []
    for success, item in helpers.parallel_bulk(
        client,
        actions=data,
        chunk_size=500,
        raise_on_error=False,
        raise_on_exception=False,
        max_chunk_bytes=20 * 1024 * 1024,
        request_timeout=60,
    ):

        if success:
            succeeded.append(item)
        else:
            failed.append(item)

    if len(failed) > 0:
        log.error("There were errors: ", f"{len(failed)}")
        for item in failed:
            log.error(f"    {item}")

    if len(succeeded) > 0:
        log.info("Bulk-inserted", f"{len(succeeded)} items.")
    log.info("Upload duration", f"{time.time() - start_time:.2f} secs")
    return S_OK()


class StorageUsageDumpAgent(AgentModule):

    def initialize(self):
        self.workDirectory = self.am_getWorkDirectory()
        self.s3_access_key = self.am_getOption("S3_access_key")
        self.s3_secret_key = self.am_getOption("S3_secret_key")
        self.s3_bucket_name = self.am_getOption("S3_bucket_name", S3_BUCKET_NAME)
        self.s3_endpoint_url = self.am_getOption("S3_endpoint_url", S3_ENDPOINT_URL)
        self.os_endpoint_url = self.am_getOption("OS_endpoint_url", OS_ENDPOINT_URL)
        self.os_username = gConfig.getValue("/Systems/NoSQLDatabases/User")
        self.os_password = gConfig.getValue("/Systems/NoSQLDatabases/Password")

        sql_db_params = returnValueOrRaise(getDBParameters("DataManagement/StorageUsageDB"))
        self.db_host = sql_db_params["Host"]
        self.db_port = sql_db_params["Port"]
        self.db_user = sql_db_params["User"]
        self.db_password = sql_db_params["Password"]
        self.db_name = sql_db_params["DBName"]

        # Sanity check: make sure that there are no duplicate event types
        if len(STREAM_TO_EVENTTYPE) != len(set(STREAM_TO_EVENTTYPE.values())):
            return S_ERROR("Duplicated event types !")

        return S_OK()

    def execute(self):
        asyncio.run(self.do_the_dump())

        return S_OK()

    async def do_the_dump(self):

        prod_data_info, bk_metadata = await asyncio.gather(
            get_prod_data_info(),
            get_bk_metadata(),
        )

        dfc_df = pd.DataFrame(prod_data_info[1], columns=prod_data_info[0])
        expected_total_size = dfc_df["SESize"].sum()
        expected_total_files = dfc_df["SEFiles"].sum()

        dfc_df["SESite"], dfc_df["SEType"] = zip(*dfc_df["SEName"].apply(se_name_to_type))
        dfc_df["IsDisk"] = ~dfc_df["SEType"].isin(TAPE_STORAGE_TYPES)

        # Find the bad rows
        bad_rows = dfc_df["Name"].str.contains(rf"^(?:{'|'.join(BAD_PREFIXES)})")

        # dfc_df_bad = dfc_df[bad_rows].reset_index(drop=True)
        # dfc_df = dfc_df[~bad_rows].reset_index(drop=True)
        dfc_df_bad = dfc_df[bad_rows]
        dfc_df = dfc_df[~bad_rows]

        # Dump the info about the bad rows
        for bad_prefix in BAD_PREFIXES:
            tmp_bad_rows = dfc_df_bad["Name"].str.startswith(bad_prefix)
            self.log.info(
                "Summary for bad prefix",
                (
                    f"{bad_prefix=}, rows: {np.count_nonzero(tmp_bad_rows)}, "
                    f"size: {dfc_df_bad.loc[tmp_bad_rows & (dfc_df_bad['SEName'] != 'FakeSE')]['SESize'].sum() / 1000**4}"
                ),
            )

        ### Treat the RAW data
        # /lhcb/data/<year>/RAW/<online stream>/<partition>/<config version>/<run number>
        # e.g. /lhcb/data/2016/RAW/FULL/LHCb/COLLISION16/173627

        raw_rows = dfc_df["Name"].str.startswith("/lhcb/data") & dfc_df["Name"].str.contains("/RAW/")

        # 173627 is the run number, -173627 is the production number
        dfc_df.loc[raw_rows, "production"] = -pd.to_numeric(dfc_df[raw_rows]["Name"].str.split("/", expand=True)[8])

        # In principle, this can only be RAW
        dfc_df.loc[raw_rows, "filetype"] = dfc_df.loc[raw_rows, "Name"].str.split("/", expand=True)[4]

        dfc_df.loc[raw_rows, "online_stream"] = dfc_df.loc[raw_rows, "Name"].str.split("/", expand=True)[5]

        # Add the event type name
        dfc_df.loc[raw_rows, "maybe_eventtype"] = dfc_df.loc[raw_rows, "online_stream"].apply(STREAM_TO_EVENTTYPE.get)

        # sanity: all raw files should have an event type
        if not dict(dfc_df.loc[raw_rows, "filetype"].value_counts()) == {"RAW": np.count_nonzero(raw_rows)}:
            raise NotImplementedError()

        ####### Treat the rows which are not RAW

        # e.g. /lhcb/MC/2017/PKTAUTAU.STRIP.DST/00230562/0000

        # 230562 is the production number
        dfc_df.loc[~raw_rows, "production"] = pd.to_numeric(dfc_df[~raw_rows]["Name"].str.split("/", expand=True)[5])

        dfc_df.loc[~raw_rows, "filetype"] = dfc_df.loc[~raw_rows, "Name"].str.split("/", expand=True)[4]

        bk_df = pd.DataFrame(bk_metadata[1], columns=bk_metadata[0])

        # Join the DFC info together with the BK info
        # dfc_df will map to multiple values in bk_df for real data due to different eventtypes (i.e. streams)
        df = dfc_df.merge(bk_df, on=["production", "filetype"], how="left", validate="many_to_many")

        # Replace Nan with 0.0 or Unknown

        group_cols = list(bk_df.columns)
        group_cols.pop(group_cols.index("production"))

        # The original version was filtering on ConfigName being Nan,  but we get the same result whn doing it no matter what
        # df.loc[pd.isnull(df["ConfigName"])] = df.loc[pd.isnull(df["ConfigName"])].fillna(
        #     {k: "Unknown" if df.dtypes[k].type == np.object_ else 0 for k in group_cols}
        # )
        df.fillna({k: "Unknown" if df.dtypes[k].type == np.object_ else 0 for k in group_cols}, inplace=True)

        df["EventTypeID"] = df["EventTypeID"].astype(int)

        raw_rows = df["Name"].str.contains("/RAW/")

        # In dfc_df ["SEName", "Name"] is unique, but when joining
        # on bk_df we made duplicates due to real data having
        # multiple event types (i.e. streams) for a given
        # production (i.e. -run number) and filetype (e.g. RAW)
        df_tmp = (
            df.loc[raw_rows]
            .groupby(["SEName", "Name"])
            .apply(find_matching_event_type_row, include_groups=False)
            .reset_index()
        )

        df = pd.concat([df_tmp, df.loc[~raw_rows]]).reset_index(drop=True)

        df = pd.concat([df, dfc_df_bad])

        # Redo it because dfc_df_bad wasn't there then
        df.fillna(
            {
                k: "Unknown" if df.dtypes[k].type == np.object_ else 0
                for k in group_cols + ["online_stream", "maybe_eventtype", "Description", "production"]
            },
            inplace=True,
        )

        # This somehow explodes the memory....

        # for cat in ("SEName", "SESite", "SEType", "online_stream", "ConfigName"):
        #     df[cat] = df[cat].astype("category")
        # for cat in ("SESize", "SEFiles", "EventTypeID"):
        #     df[cat] = pd.to_numeric(df[cat], downcast="unsigned")

        # for cat in ("production",):
        #     df[cat] = df[cat].astype(int)

        if len(df) != len(df[["SEName", "Name"]].drop_duplicates()):
            raise NotImplementedError("Something is very wrong")
        if expected_total_files != df["SEFiles"].sum():
            raise NotImplementedError()
        if expected_total_size != df["SESize"].sum():
            raise NotImplementedError()

        df.to_csv("/tmp/storage.csv.zst", index=False)
        result = {
            "groupings": [
                {
                    "name": "Logical vs Disk vs Tape",
                    "groups": [
                        {
                            "title": "Logical space",
                            "id": "logical",
                            "data": summarise_space(df[df["SEName"] == "FakeSE"], group_cols),
                        },
                        {
                            "title": "Physical space - Disk",
                            "id": "physical-disk",
                            "data": summarise_space(df[(df["SEName"] != "FakeSE") & df["IsDisk"]], group_cols),
                        },
                        {
                            "title": "Physical space - Tape",
                            "id": "physical-tape",
                            "data": summarise_space(df[(df["SEName"] != "FakeSE") & ~df["IsDisk"]], group_cols),
                        },
                        {
                            "title": "Physical space",
                            "id": "physical",
                            "data": summarise_space(df[df["SEName"] != "FakeSE"], group_cols),
                        },
                    ],
                },
                {
                    "name": "Physical by SE type",
                    "groups": [
                        {
                            "title": se_type,
                            "id": se_type.lower(),
                            "data": summarise_space(
                                df[(df["SEName"] != "FakeSE") & (df["SEType"] == se_type)], group_cols
                            ),
                        }
                        for se_type in df["SEType"].unique()
                    ],
                },
                {
                    "name": "Physical by SE site (disk)",
                    "groups": [
                        {
                            "title": se_site,
                            "id": se_site.lower(),
                            "data": summarise_space(
                                df[df["IsDisk"] & (df["SEName"] != "FakeSE") & (df["SESite"] == se_site)], group_cols
                            ),
                        }
                        for se_site in sorted(
                            df["SESite"].unique(), key=lambda x: df[df["SESite"] == x]["SESize"].sum(), reverse=True
                        )
                        if se_site != "FakeSE"
                    ],
                },
                {
                    "name": "Physical by SE site (tape)",
                    "groups": [
                        {
                            "title": se_site,
                            "id": se_site.lower(),
                            "data": summarise_space(
                                df[~df["IsDisk"] & (df["SEName"] != "FakeSE") & (df["SESite"] == se_site)], group_cols
                            ),
                        }
                        for se_site in sorted(
                            df["SESite"].unique(), key=lambda x: df[df["SESite"] == x]["SESize"].sum(), reverse=True
                        )
                        if se_site != "FakeSE"
                    ],
                },
            ],
            "last-updated": datetime.now(tz=timezone.utc).isoformat(),
        }

        path = Path("/tmp/storage.json.zst")
        path.write_bytes(zstandard.compress(json.dumps(result).encode()))

        uploadToS3(
            endpoint_url=self.s3_endpoint_url,
            bucket_name="lhcbdirac",
            access_key=self.s3_access_key,
            secret_key=self.s3_secret_key,
        )

        engine = create_engine(
            f"mysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}",
            echo=False,
        )
        Base.metadata.create_all(engine)

        # df.to_csv("/home/dirac/df.csv")
        await asyncio.gather(
            returnValueOrRaiseAsync(
                partial(sendToOpenSearch, df, self.os_endpoint_url, (self.os_username, self.os_password))
            ),
            returnValueOrRaiseAsync(
                partial(
                    directory_metadata_to_sql,
                    df,
                    db_host=self.db_host,
                    db_name=self.db_name,
                    db_user=self.db_user,
                    db_password=self.db_password,
                    db_port=self.db_port,
                    engine=engine,
                )
            ),
            returnValueOrRaiseAsync(
                partial(
                    storage_summary_to_sql,
                    df,
                    db_host=self.db_host,
                    db_name=self.db_name,
                    db_user=self.db_user,
                    db_password=self.db_password,
                    db_port=self.db_port,
                    engine=engine,
                )
            ),
        )


INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Storage Usage Visualization</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      background-color: #1e1e1e;
      color: #e0e0e0;
    }
    h1, h2 {
      color: #e0e0e0;
      text-align: center;
    }
    h1 {
      margin: 0;
    }
    a {
      color: #8888ff;
    }
    #heading {
      width: 100%;
      position: sticky;
      top: 0;
      background-color: #333333;
      color: #e0e0e0;
      padding: 10px 0;
    }
    #heading #container {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    #breadcrumbs {
      margin: 10px;
      text-align: center;
    }
    #breadcrumbs span + span::before {
      content: " / ";
      color: #e0e0e0;
      margin: 0 5px;
    }
    #reset {
      margin: 10px;
      display: block;
      margin-left: auto;
      margin-right: auto;
      background-color: #555555;
      color: #ffffff;
      border: 1px solid #888888;
    }
    select {
      background-color: #555555;
      color: #ffffff;
    }
    .container {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-around;
      width: 100%;
    }
    .tooltip {
      position: absolute;
      visibility: hidden;
      padding: 8px;
      border-radius: 4px;
      background: #444444;
      color: #ffffff;
    }

    /* Modal styles */
    #loading-modal {
      display: flex;
      justify-content: center;
      align-items: center;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5);
      z-index: 1000;
      visibility: visible;
      opacity: 1;
      transition: opacity 0.5s ease, visibility 0.5s ease;
    }
    #loading-modal.hidden {
      visibility: hidden;
      opacity: 0;
    }
    #loading-content {
      background-color: #333333;
      color: #ffffff;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .spinner {
      border-top: 4px solid #8888ff;
      border: 4px solid rgba(255, 255, 255, 0.1);
      border-radius: 50%;
      margin: 1em;
      width: 40px;
      height: 40px;
      animation: spin 1s linear infinite;
    }
    .view-option {
      display: inline-block;
      margin: 0 10px;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div id="loading-modal">
    <div id="loading-content">
      <div class="spinner"></div>
      <p>Loading, please wait...</p>
    </div>
  </div>

  <div id="heading">
    <h1>Storage Usage Visualization</h1>
    <div id="breadcrumbs"></div>
    <button id="reset">Reset breadcrumbs</button>
    <div style="text-align: center; margin-top: 10px;">
      <div class="view-option">
        <label for="grouping-select">Choose split:</label>
        <select id="grouping-select"></select>
      </div>
      <div class="view-option">
        <label for="hide-conditions">Hide conditions:</label>
        <input type="checkbox" id="hide-conditions">
      </div>
    </div>
    <div style="text-align: center;">
      Mouse over a segment for details. Click to zoom in.
      Last updated: <span id="last-updated-time"></span>
    </div>
  </div>
  <div id="charts" class="container">
  </div>
  <div id="tooltip" class="tooltip"></div>

  <script src="https://cdn.jsdelivr.net/npm/fzstd@0.1.1/umd/index.js"></script>
  <script src="https://d3js.org/d3.v6.min.js"></script>
  <script src="script.js"></script>
</body>
</html>
"""


def directory_metadata_to_sql(
    df, *, db_user: str, db_password: str, db_host: str, db_port: str, db_name: str, engine: Engine
):
    log = gLogger.getLocalSubLogger("directory_metadata_to_sql")
    log.info("Writing directory metadata to database")
    start_time = time.time()

    df = df[df["SEName"] == "FakeSE"][
        [
            "Name",
            "production",
            "filetype",
            "online_stream",
            "maybe_eventtype",
            "ConfigName",
            "ConfigVersion",
            "Description",
            "ProcPath",
            "EventTypeID",
        ]
    ].drop_duplicates()

    # Create the database and table
    # engine = create_engine(
    #     f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    #     echo=False,
    # )
    # Base.metadata.create_all(engine)

    # Assuming 'engine' is your database connection
    with engine.connect() as conn:
        conn.execute(delete(DirectoryMetadata))
        # Base.metadata.drop_all(engine, tables=[DirectoryMetadata.__table__])
        # conn.execute(text(f"TRUNCATE TABLE {DirectoryMetadata.__tablename__}"))
        df.to_sql(
            DirectoryMetadata.__tablename__,
            conn,
            index=False,
            method="multi",
            chunksize=10000,
            if_exists="append",
        )
        new_comment = json.dumps({"LastUpdate": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")})
        conn.execute(text(f"ALTER TABLE {DirectoryMetadata.__tablename__} COMMENT = '{new_comment}';"))

    log.info("Upload duration", f"{time.time() - start_time:.2f} secs")
    return S_OK()


def storage_summary_to_sql(
    df, *, db_user: str, db_password: str, db_host: str, db_port: str, db_name: str, engine: Engine
):
    log = gLogger.getLocalSubLogger("storage_summary_to_sql")
    log.info("Writing storage summary to database")
    start_time = time.time()

    df = df[
        [
            "SEName",
            "SESize",
            "SEFiles",
            "SESite",
            "SEType",
            "IsDisk",
        ]
    ]

    df_size = df[["SEName", "SESize", "SEFiles"]].groupby("SEName").sum()
    df_meta = df[["SEName", "SESite", "IsDisk", "SEType"]].drop_duplicates().set_index("SEName")
    df_summary = df_size.merge(df_meta, on="SEName").reset_index()

    # # Create the database and table
    # engine = create_engine(
    #     f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    #     echo=False,
    # )
    # Base.metadata.create_all(engine)

    # Assuming 'engine' is your database connection
    with engine.connect() as conn:
        conn.execute(delete(StorageSummary))
        df_summary.to_sql(
            StorageSummary.__tablename__,
            conn,
            index=False,
            method="multi",
            chunksize=10000,
            if_exists="append",
        )
        new_comment = json.dumps({"LastUpdate": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")})
        conn.execute(text(f"ALTER TABLE {StorageSummary.__tablename__} COMMENT = '{new_comment}';"))

    log.info("Upload duration", f"{time.time() - start_time:.2f} secs")
    return S_OK()
