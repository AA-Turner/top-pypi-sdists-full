import io
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from threading import Timer
from typing import Any, Dict, List, Optional, Union, cast

import pandas as pd
import redshift_connector
import snowflake.connector

if sys.version_info.minor != 6:
    from domino_data.data_sources import DatasourceConfig, SnowflakeConfig, _Object

from .domino_api import AppInfo, IDominoApi
from .settings import settings


class Result:
    def to_pandas(self):
        pass


class SnowflakeResult(Result):
    def __init__(self, cs):
        self.cs = cs

    def to_pandas(self):
        try:
            return self.cs.fetch_pandas_all()
        except snowflake.connector.errors.NotSupportedError:
            names = [x.name for x in self.cs.description]
            return pd.DataFrame(self.cs.fetchall(), columns=names)


class DataSource:
    override: Optional[DatasourceConfig] = None

    def query(self, q):
        pass

    def update(self, config: DatasourceConfig):
        self.override = config


class SnowflakeDataSource(DataSource):
    def __init__(self, cs):
        self.cs = cs
        self.datasource_type = "SnowflakeConfig"
        self.config = {}

    def query(self, q):
        if self.override:
            override = cast(SnowflakeConfig, self.override)
            self.cs.execute(f"USE SCHEMA {override.database}.{override.schema}")
        self.cs.execute(q)
        return SnowflakeResult(self.cs)


class RedshiftResult(Result):
    def __init__(self, df):
        self.df = df

    def to_pandas(self):
        return self.df


class RedshiftDataSource(DataSource):
    def __init__(self, cs):
        self.cs = cs
        self.datasource_type = "RedshiftConfig"
        self.config = {"database": "dev"}

    def query(self, q):
        try:
            self.cs.execute(q)
            return RedshiftResult(self.cs.fetch_dataframe() if self.cs.redshift_rowcount > -1 else None)
        finally:
            self.cs.execute("ABORT")


class S3DataSource(DataSource):
    delay = 3.0

    def __init__(self):
        self.datasource_type = "S3Config"

    def list_objects(self):
        time.sleep(self.delay)
        return [
            _Object(
                datasource=self,  # type: ignore
                key=key,
            )
            for key in ["1/foo.txt", "titanic.csv"]
        ]

    def download_fileobj(self, key: str, fileobj):
        with urllib.request.urlopen("https://vve589t3tspu.s3.us-west-2.amazonaws.com/titanic.csv") as f:
            fileobj.write(f.read())

    def get(self, key: str):
        buffer = io.BytesIO()
        self.download_fileobj(key, buffer)
        return buffer.getvalue()


class ADLSDataSource(DataSource):
    delay = 3.0

    def __init__(self):
        self.datasource_type = "ADLSConfig"

    def list_objects(self):
        time.sleep(self.delay)
        return [
            _Object(
                datasource=self,  # type: ignore
                key=key,
            )
            for key in ["1/foo.txt", "StormEvents.csv"]
        ]

    def download_fileobj(self, key: str, fileobj):
        with urllib.request.urlopen("https://kustosamples.blob.core.windows.net/samplefiles/StormEvents.csv") as f:
            fileobj.write(f.read())

    def get(self, key: str):
        buffer = io.BytesIO()
        self.download_fileobj(key, buffer)
        return buffer.getvalue()


class DataSourceClient:
    def get_datasource(self, name):
        if "snowflake" in name.lower():
            ctx = snowflake.connector.connect(user=settings.snowflake_user, password=settings.snowflake_password, account=settings.snowflake_account)
            cs = ctx.cursor()
            return SnowflakeDataSource(cs)
        if "redshift" in name.lower():
            conn = redshift_connector.connect(
                host=settings.redshift_host,
                database="dev",
                user=settings.redshift_user,
                password=settings.redshift_password,
            )
            return RedshiftDataSource(conn.cursor())
        if "s3" in name.lower():
            return S3DataSource()
        if "adls" in name.lower():
            return ADLSDataSource()


@dataclass()
class MockDominoApi(IDominoApi):
    delay: float = 3.0
    data_list: Union[List, Exception] = field(
        default_factory=lambda: [
            {"name": "mario_test_snowflake", "dataSourceType": "SnowflakeConfig"},
            {"name": "mario_test_redshift", "dataSourceType": "RedshiftConfig"},
            {"name": "mario_test_big_query", "dataSourceType": "BigQueryConfig"},
            {"name": "mario_test_s3", "dataSourceType": "S3Config"},
            {"name": "test_adls", "dataSourceType": "ADLSConfig"},
            {"name": "mario_na", "dataSourceType": "NaConfig"},
        ]
    )
    data_sources: Union[List, Exception] = field(
        default_factory=lambda: ["mario_test_snowflake", "mario_test_redshift", "mario_test_big_query", "mario_test_s3", "test_adls"]
    )
    sync_return: Union[bool, Exception] = True
    app_status_delay = 0.1
    app_status: Union[str, Exception, None] = "Running"  # "Pending", "Preparing", "Running", "Stopped" or "Failed"
    app_publish_end_state: Union[str, Exception] = "Running"
    app_unpublish_end_state: Union[str, Exception] = "Stopped"
    app_id: Union[Optional[str], Exception] = "123"
    app_info: List[AppInfo] = field(
        default_factory=lambda: [
            {
                "created": "2022-10-17T11:48:58.606Z",
                "lastUpdated": "2022-10-17T11:48:58.606Z",
                "runningCommitId": "fe15cf09ac8fd55405141bbd81a8276b07d263a8",
                "openUrl": "some/url",
                "latestAppVersionId": "some/version",
                "id": "some/id",
                "hardwareTierId": "small-k8s",
                "status": "Running",
            }
        ]
    )
    current_environment_id: str = "632b014bde659c33feb8f748"
    default_environment_id: str = current_environment_id

    def get_datasource_list(self):
        time.sleep(self.delay)
        return self._return_or_raise(self.data_list)

    def get_datasource_names(self):
        time.sleep(self.delay)
        return self._return_or_raise(self.data_sources)

    def sync(self, commit_message: str):
        time.sleep(self.delay)
        return self._return_or_raise(self.sync_return)

    @staticmethod
    def _return_or_raise(value):
        if isinstance(value, Exception):
            raise value
        return value

    def get_app_status(self):
        time.sleep(self.app_status_delay)
        return self._return_or_raise(self.app_status)

    def app_publish(self, hardwareTierId=None):
        time.sleep(self.app_status_delay)

        self._return_or_raise(self.app_publish_end_state)
        self.app_status = "Pending"

        def set_preparing():
            self.app_status = "Preparing"

        Timer(self.delay, set_preparing).start()

        end_state = self.app_publish_end_state

        def set_end_state():
            self.app_status = end_state

        Timer(self.delay * 2, set_end_state).start()

    def app_unpublish(self):
        time.sleep(self.app_status_delay)

        self._return_or_raise(self.app_unpublish_end_state)

        end_state = self.app_unpublish_end_state

        def set_end_state():
            self.app_status = end_state

        Timer(self.delay, set_end_state).start()

    def get_app_id(self):
        return self._return_or_raise(self.app_id)

    def get_app_info(self) -> List[AppInfo]:
        time.sleep(self.delay)
        return self.app_info

    def get_user_info(self) -> Optional[dict]:
        return {
            "firstName": "John",
            "lastName": "Smith",
            "fullName": "John Smith",
            "userName": "johnsmith",
            "email": "johnsmith@example.com",
            "avatarUrl": "",
            "id": "1234567890b",
        }

    def get_domino_version(self) -> str:
        return "0.0"

    def sync_files(self, commit_message: str) -> Dict[str, Any]:
        return {"succeeded": True, "message": "Synchronizing files ..."}

    def get_useable_environments(self):
        time.sleep(self.delay)
        return {
            "currentlySelectedEnvironment": {
                "id": self.default_environment_id,
                "v2EnvironmentDetails": {
                    "latestRevision": 10,
                    "latestRevisionUrl": "/environments/revisions/6349a8044335d417d82b7036",
                    "latestRevisionStatus": "Succeeded",
                    "selectedRevision": 9,
                    "selectedRevisionUrl": "/environments/revisions/63487b044325d417d82b6d20",
                },
                "supportedClusters": [],
            },
            "environments": [
                {
                    "id": "632b014bde659c33feb8f748",
                    "archived": False,
                    "name": "Domino Standard Environment 5.2 + DCA + AutoML",
                    "version": 2,
                    "visibility": "Private",
                    "owner": {"id": "userid1", "username": "user1"},
                    "supportedClusters": [],
                },
                {
                    "id": "628560094906b439238b950f",
                    "archived": False,
                    "name": "PyCharm",
                    "version": 2,
                    "visibility": "Private",
                    "owner": {"id": "userid2", "username": "user2"},
                    "supportedClusters": [],
                },
                {
                    "id": "63582e044335d417d82b7c3b",
                    "archived": False,
                    "name": "Domino Standard 5.2 + DCA (0.3.1)",
                    "version": 2,
                    "visibility": "Private",
                    "owner": {"id": "userid3", "username": "user2"},
                    "supportedClusters": [],
                },
            ],
        }

    def get_current_environment_id(self) -> str:
        time.sleep(self.delay)
        return self.current_environment_id
