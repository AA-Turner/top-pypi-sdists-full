import os
import sys
import threading
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, cast

from typing_extensions import TypedDict

from domino_code_assist import util

from .domino_api_mock_data import available_hardware
from .settings import settings

host = settings.domino_alternative_api_host or settings.domino_api_host

_domino_api = None
_lock = threading.Lock()


class AppInfo(TypedDict):
    created: str
    lastUpdated: str
    runningCommitId: str
    openUrl: str
    latestAppVersionId: str
    id: str
    hardwareTierId: str
    status: str


class LogLine(TypedDict):
    timestamp: int  # e.g. 1672151560992
    logType: str  # stderr/stdout/prepareoutput
    log: str  # single line
    size: int  # e.g. 18


def get_domino_api():
    global _domino_api

    with _lock:
        if not _domino_api:
            api_class = settings.domino_api_class
            if api_class:
                import importlib

                module, class_ = api_class.split(":")
                DominoApiClass = getattr(importlib.import_module(module), class_)
                _domino_api = DominoApiClass()
            elif util.in_dev_mode():
                from .domino_lab_mock import MockDominoApi

                _domino_api = MockDominoApi()
            elif sys.version_info.minor == 6:
                from .py36 import Py36DominoApi

                _domino_api = Py36DominoApi()
            else:
                _domino_api = DominoApi()
    return _domino_api


class IDominoApi(ABC):
    @abstractmethod
    def get_datasource_list(self):
        pass

    @abstractmethod
    def get_datasource_names(self) -> List[str]:
        pass

    @abstractmethod
    def sync(self, commit_message: str):
        pass

    @abstractmethod
    def get_app_status(self) -> Optional[str]:
        pass

    @abstractmethod
    def app_publish(self, hardwareTierId: Optional[str]):
        pass

    @abstractmethod
    def app_unpublish(self):
        pass

    @abstractmethod
    def get_app_id(self) -> Optional[str]:
        pass

    def get_default_hardware_tier_id(self):
        return "small-k8s"

    @abstractmethod
    def get_user_info(self) -> Optional[dict]:
        pass

    @abstractmethod
    def get_domino_version(self) -> str:
        pass

    @abstractmethod
    def sync_files(self, commit_message: str) -> Dict[str, Any]:
        pass

    def get_client_version(self) -> str:
        return "0.0"

    @abstractmethod
    def get_app_info(self) -> List[AppInfo]:
        pass

    def get_app_log(self) -> List[LogLine]:
        return [
            {"timestamp": 1672151702389, "logType": "prepareoutput", "log": "Checking for local changes...", "size": 29},
            {"timestamp": 1672151560992, "logType": "stdout", "log": "Using curl at curl", "size": 18},
            {"timestamp": 1672151561051, "logType": "stdout", "log": "Preparing working directory.", "size": 28},
        ] * 100

    @abstractmethod
    def get_useable_environments(self):
        pass

    @abstractmethod
    def get_current_environment_id(self):
        pass

    def get_experiments(self):
        return [
            {
                "experiment_id": "17",
                "name": "popular-fish-163",
                "artifact_location": "mlflow-artifacts:/mlflow",
                "lifecycle_stage": "active",
                "last_update_time": 1682528255165,
                "creation_time": 1682528255165,
                "tags": [{"key": "mlflow.domino.project", "value": "DCA-latest"}],
            },
            {
                "experiment_id": "16",
                "name": "gaudy-donkey-172",
                "artifact_location": "mlflow-artifacts:/mlflow",
                "lifecycle_stage": "active",
                "last_update_time": 1682514840966,
                "creation_time": 1682514840966,
                "tags": [{"key": "mlflow.domino.project", "value": "DCA-latest"}],
            },
        ]

    def get_current_hardware(self):
        return

    def get_available_hardware(self):
        return available_hardware


class DominoApi(IDominoApi):
    def get_datasource_list(self):
        project_id = settings.domino_project_id
        return self._get_domino_client().request_manager.get(f"{host}/v4/datasource/projects/{project_id}").json()

    def get_datasource_names(self):
        return [k["name"] for k in self.get_datasource_list()]

    def sync(self, commit_message: str):
        run_id = settings.domino_run_id
        project_owner = settings.domino_project_owner
        project_name = settings.domino_project_name
        response = self._get_domino_client().request_manager.post(
            f"{host}/u/{project_owner}/{project_name}/run/synchronizeRunWorkingDirectory/{run_id}",
            json={
                "uploadLocalChanges": True,
                "shouldSaveConflicts": False,
                "syncOperationInfo": {"syncOperationId": str(uuid.uuid4()), "syncOperationType": "onlyDfs"},
                "commitMessage": commit_message,
            },
        )
        return response.json()["succeeded"]

    def get_app_status(self):
        domino = self._get_domino_client()
        app_id = domino._app_id
        return domino._Domino__app_get_status(app_id)

    def app_publish(self, hardwareTierId=None):
        self._get_domino_client().app_publish(hardwareTierId=hardwareTierId)

    def app_unpublish(self):
        self._get_domino_client().app_unpublish()

    def get_app_id(self):
        return self._get_domino_client()._app_id

    def get_user_info(self):
        return self._get_domino_client().request_manager.get(f"{host}/v4/users/self").json()

    def get_domino_version(self) -> str:
        return self._get_domino_client()._version

    def sync_files(self, commit_message: str) -> Dict[str, Any]:
        api = self._get_domino_client()
        url_base = api._routes._build_project_url_private_api()
        return api.request_manager.post(
            f"{url_base}/run/synchronizeRunWorkingDirectory/{os.environ['DOMINO_RUN_ID']}",
            json={
                "uploadLocalChanges": True,
                "shouldSaveConflicts": False,
                "syncOperationInfo": {"syncOperationId": "0de13390-7ff2-4df8-a016-0512f227ce65", "syncOperationType": "onlyDfs"},
                "commitMessage": commit_message,
            },
        ).json()

    def get_client_version(self):
        from domino._version import __version__

        return __version__

    def get_app_info(self) -> List[AppInfo]:
        api = self._get_domino_client()
        project_id = api.project_id if hasattr(api, "project_id") else api._project_id
        url_str = api._routes.app_list(project_id)
        return cast(List[AppInfo], api.request_manager.get(url_str).json())

    _domino_client = None
    _lock = threading.Lock()

    def _get_domino_client(self):
        with self._lock:
            if not self._domino_client:
                project_owner = settings.domino_project_owner
                project_name = settings.domino_project_name

                # needed for python 3.6 support
                from domino import Domino

                self._domino_client = (
                    Domino(f"{project_owner}/{project_name}", host=settings.domino_alternative_api_host) if not util.in_dev_mode() else cast(Domino, None)
                )
        return self._domino_client

    def get_app_log(self) -> List[LogLine]:
        app_info = self.get_app_info()
        app_id = app_info[0]["latestAppVersionId"]
        return self._get_domino_client().request_manager.get(f"{host}/v4/modelProducts/apps/versions/{app_id}/realTimeLogs").json()["logContent"]

    def get_useable_environments(self):
        return self._get_domino_client()._routes.useable_environments_list()

    def get_current_environment_id(self):
        project_id = settings.domino_project_id
        run_id = settings.domino_run_id
        return (
            self._get_domino_client()
            .request_manager.get(f"{host}/v4/workspaces/{run_id}/runtimeExecutionDetails?projectId={project_id}")
            .json()["environment"]["environmentId"]
        )

    def get_experiments(self):
        project_id = settings.domino_project_id
        return (
            self._get_domino_client()
            .request_manager.post(
                f"{host}/api/2.0/mlflow/experiments/search", json={"max_results": 3000}, headers={"X-Domino-Mlflow-Data": f'{{ "projectId": "{project_id}" }}'}
            )
            .json()["experiments"]
        )

    def get_current_hardware(self):
        api = self._get_domino_client()
        url = api._routes.find_project_by_owner_name_and_project_name_url()
        return api.request_manager.get(url).json()

    def get_available_hardware(self):
        return self._get_domino_client().hardware_tiers_list().json()
