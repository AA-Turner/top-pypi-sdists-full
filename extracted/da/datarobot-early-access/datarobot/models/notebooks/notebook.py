#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import datetime
from io import IOBase
from typing import Any, Dict, List, Optional

from mypy_extensions import TypedDict
from pytz import utc
import trafaret as t

from datarobot.errors import InvalidUsageError
from datarobot.mixins.browser_mixin import BrowserMixin
from datarobot.models.api_object import APIObject
from datarobot.models.notebooks.enums import (
    KernelExecutionStatus,
    KernelSpec,
    ManualRunType,
    NotebookPermissions,
    NotebookStatus,
    NotebookType,
    ScheduleStatus,
    SessionType,
)
from datarobot.models.notebooks.exceptions import KernelNotAssignedError
from datarobot.models.notebooks.execution_environment import ExecutionEnvironment
from datarobot.models.notebooks.kernel import NotebookKernel
from datarobot.models.notebooks.revision import CreateRevisionPayload, NotebookRevision
from datarobot.models.notebooks.scheduled_job import NotebookScheduledJob
from datarobot.models.notebooks.session import (
    CloneRepositorySchema,
    NotebookExecutionStatus,
    NotebookSession,
    StartSessionParameters,
    StartSessionPayload,
)
from datarobot.models.notebooks.settings import notebook_settings_trafaret, NotebookSettings
from datarobot.models.notebooks.user import notebook_activity_trafaret, NotebookActivity
from datarobot.models.use_cases.utils import resolve_use_cases, UseCaseLike
from datarobot.utils import assert_single_parameter
from datarobot.utils.pagination import unpaginate


class ManualRunPayload(TypedDict, total=False):
    notebook_id: str
    manual_run_type: ManualRunType
    title: Optional[str]
    notebook_path: Optional[str]
    parameters: Optional[List[StartSessionParameters]]


class Notebook(APIObject, BrowserMixin):
    """
    Metadata for a DataRobot Notebook accessible to the user.

    Attributes
    ----------

    id : str
        The ID of the Notebook.
    name : str
        The name of the Notebook.
    type : NotebookType
        The type of the Notebook. Can be "plain" or "codespace".
    permissions : List[NotebookPermissions]
        The permissions the user has for the Notebook.
    tags : List[str]
        Any tags that have been added to the Notebook. Default is an empty list.
    created : NotebookActivity
        Information on when the Notebook was created and who created it.
    updated : NotebookActivity
        Information on when the Notebook was updated and who updated it.
    last_viewed : NotebookActivity
        Information on when the Notebook was last viewed and who viewed it.
    settings : NotebookSettings
        Information on global settings applied to the Notebook.
    org_id : Optional[str]
        The organization ID associated with the Notebook.
    tenant_id : Optional[str]
        The tenant ID associated with the Notebook.
    description : Optional[str]
        The description of the Notebook. Optional.
    session : Optional[NotebookSession]
        Metadata on the current status of the Notebook and its kernel. Optional.
    use_case_id : Optional[str]
        The ID of the Use Case the Notebook is associated with. Optional.
    use_case_name : Optional[str]
        The name of the Use Case the Notebook is associated with. Optional.
    has_schedule : bool
        Whether or not the notebook has a schedule.
    has_enabled_schedule : bool
        Whether or not the notebook has a currently enabled schedule.
    """

    _notebooks_path = "notebooks/"
    _scheduling_path = "notebookJobs/"
    _revisions_path = "notebookRevisions/"

    _session_subset_trafaret = t.Dict(
        {
            t.Key("status"): t.Enum(*list(NotebookStatus)),
            t.Key("notebook_id"): t.String,
            t.Key("user_id"): t.String,
            t.Key("started_at", optional=True): t.String,
            t.Key("session_type", optional=True): t.Enum(*list(SessionType)),
        }
    ).ignore_extra("*")

    _converter = t.Dict(
        {
            t.Key("id"): t.String,
            t.Key("name"): t.String,
            t.Key("type"): t.Enum(*list(NotebookType)),
            t.Key("description", optional=True): t.Or(t.String, t.Null),
            t.Key("permissions"): t.List(
                t.Enum(*list(NotebookPermissions)),
            ),
            t.Key("tags"): t.List(t.String),
            t.Key("created"): notebook_activity_trafaret,
            t.Key("updated", optional=True): notebook_activity_trafaret,
            t.Key("last_viewed"): notebook_activity_trafaret,
            t.Key("settings"): notebook_settings_trafaret,
            t.Key("org_id", optional=True): t.Or(t.String, t.Null),
            t.Key("tenant_id", optional=True): t.Or(t.String, t.Null),
            t.Key("session", optional=True): t.Or(_session_subset_trafaret, t.Null),
            t.Key("use_case_id", optional=True): t.Or(t.String, t.Null),
            t.Key("use_case_name", optional=True): t.Or(t.String, t.Null),
            t.Key("has_schedule"): t.Bool,
            t.Key("has_enabled_schedule"): t.Bool,
        }
    ).ignore_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        type: NotebookType,
        permissions: List[str],
        tags: List[str],
        created: Dict[str, Any],
        last_viewed: Dict[str, Any],
        settings: Dict[str, bool],
        has_schedule: bool,
        has_enabled_schedule: bool,
        updated: Optional[Dict[str, Any]] = None,
        org_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        description: Optional[str] = None,
        session: Optional[Dict[str, str]] = None,
        use_case_id: Optional[str] = None,
        use_case_name: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.permissions = [NotebookPermissions[permission] for permission in permissions]
        self.tags = tags
        self.created = NotebookActivity.from_server_data(created)
        self.updated = updated if not updated else NotebookActivity.from_server_data(updated)
        self.last_viewed = (
            last_viewed if not last_viewed else NotebookActivity.from_server_data(last_viewed)
        )
        self.settings = NotebookSettings.from_server_data(settings)
        self.org_id = org_id
        self.tenant_id = tenant_id
        self.session = session
        self.use_case_id = use_case_id
        self.use_case_name = use_case_name
        self.has_schedule = has_schedule
        self.has_enabled_schedule = has_enabled_schedule

    def __repr__(self) -> str:
        use_case_id_str = f", use_case_id={self.use_case_id}" if self.use_case_id else ""
        use_case_name_str = f", use_case_name={self.use_case_name}" if self.use_case_name else ""
        return (
            f'{self.__class__.__name__}(name="{self.name}", id={self.id}, type={self.type}'
            f"{use_case_id_str}{use_case_name_str})"
        )

    @property
    def is_standalone(self) -> bool:
        return self.type == NotebookType.STANDALONE

    @property
    def is_classic(self) -> bool:
        return self.is_standalone and self.use_case_id is None

    @property
    def is_codespace(self) -> bool:
        return self.type == NotebookType.CODESPACE

    def get_uri(self) -> str:
        """
        Returns
        -------
        url : str
            Permanent static hyperlink to this Notebook in its Use Case or standalone.
        """
        if self.use_case_id:
            return f"{self._client.domain}/usecases/{self.use_case_id}/notebooks/{self.id}"
        else:
            return f"{self._client.domain}/notebooks/{self.id}"

    @classmethod
    def get(cls, notebook_id: str) -> Notebook:
        """
        Retrieve a single notebook.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook you want to retrieve.

        Returns
        -------
        notebook : Notebook
            The requested notebook.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import Notebook

            notebook = Notebook.get(notebook_id='6556b00dcc4ea0bb7ea48121')
        """
        r_data = cls._client.get(f"{cls._notebooks_path}{notebook_id}/")
        return cls.from_server_data(r_data.json())

    def create_revision(
        self,
        name: Optional[str] = None,
        notebook_path: Optional[str] = None,
        is_auto: bool = False,
    ) -> NotebookRevision:
        """
        Create a new revision for the notebook.

        Parameters
        ----------
        name : Optional[str]
            The name of the revision. Optional.
        notebook_path : Optional[str]
            The path of the notebook to execute within the codespace. Required if notebook is in a codespace.
        is_auto : bool
            Indicates whether the revision was auto-saved versus a user interaction. Default is False.

        Returns
        -------
        notebook_revision : NotebookRevision
            Information about the created notebook revision.
        """
        return NotebookRevision.create(
            notebook_id=self.id,
            payload=CreateRevisionPayload(name=name, notebook_path=notebook_path, is_auto=is_auto),
        )

    def download_revision(
        self,
        revision_id: str,
        file_path: Optional[str] = None,
        filelike: Optional[IOBase] = None,
    ) -> None:
        """
        Downloads the notebook as a JSON (.ipynb) file for the specified revision.

        Parameters
        ----------
        file_path: string, optional
            The destination to write the file to.
        filelike: file, optional
            A file-like object to write to.  The object must be able to write bytes. The user is
            responsible for closing the object.

        Returns
        -------
        None

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import Notebook

            notebook = Notebook.get(notebook_id='6556b00dcc4ea0bb7ea48121')
            manual_run = notebook.run_as_job()
            revision_id = manual_run.wait_for_completion()
            notebook.download_revision(revision_id=revision_id, file_path="./results.ipynb")
        """
        assert_single_parameter(("filelike", "file_path"), filelike, file_path)

        response = self._client.get(f"{self._revisions_path}{self.id}/{revision_id}/toFile/")
        if file_path:
            with open(file_path, "wb") as f:
                f.write(response.content)
        if filelike:
            filelike.write(response.content)

    def delete(self) -> None:
        """
        Delete a single notebook

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import Notebook

            notebook = Notebook.get(notebook_id='6556b00dcc4ea0bb7ea48121')
            notebook.delete()
        """
        self._client.delete(f"{self._notebooks_path}{self.id}/")

    @classmethod
    def list(
        cls,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        order_by: Optional[str] = None,
        tags: Optional[List[str]] = None,
        owners: Optional[List[str]] = None,
        query: Optional[str] = None,
        use_cases: Optional[UseCaseLike] = None,
    ) -> List[Notebook]:
        """
        List all Notebooks available to the user.

        Parameters
        ----------
        created_before : Optional[str]
            List Notebooks created before a certain date. Optional.
        created_after : Optional[str]
            List Notebooks created after a certain date. Optional.
        order_by : Optional[str]
            Property to sort returned Notebooks. Optional.
            Supported properties are "name", "created", "updated", "tags", and "lastViewed".
            Prefix the attribute name with a dash to sort in descending order,
            e.g. order_by='-created'.
            By default, the order_by parameter is None.
        tags : Optional[List[str]]
            A list of tags that returned Notebooks should be associated with. Optional.
        owners : Optional[List[str]]
            A list of user IDs used to filter returned Notebooks.
            The respective users share ownership of the Notebooks. Optional.
        query : Optional[str]
            A specific regex query to use when filtering Notebooks. Optional.
        use_cases : Optional[UseCase or List[UseCase] or str or List[str]]
            Filters returned Notebooks by a specific Use Case or Cases. Accepts either the entity or the ID. Optional.
            If set to [None], the method filters the notebook's datasets by those not linked to a UseCase.

        Returns
        -------
        notebooks : List[Notebook]
            A list of Notebooks available to the user.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import Notebook

            notebooks = Notebook.list()
        """
        params = {
            "created_before": created_before,
            "created_after": created_after,
            "order_by": order_by,
            "tags": tags,
            "owners": owners,
            "query": query,
        }
        params = resolve_use_cases(use_cases=use_cases, params=params, use_case_key="use_case_id")
        r_data = unpaginate(f"{cls._notebooks_path}", params, cls._client)
        return [cls.from_server_data(data) for data in r_data]

    def is_running(self) -> bool:
        """
        Check if the notebook session is currently running.
        """
        return self.get_session_status() == NotebookStatus.RUNNING

    def get_session_status(self) -> NotebookStatus:
        """
        Get the status of the notebook session.
        """
        notebook_session = NotebookSession.get(self.id)
        return notebook_session.status

    def start_session(
        self,
        is_triggered_run: bool = False,
        parameters: Optional[List[StartSessionParameters]] = None,
        open_file_paths: Optional[List[str]] = None,
        clone_repository: Optional[CloneRepositorySchema] = None,
    ) -> NotebookSession:
        """
        Start a new session for the notebook.

        Parameters
        ----------
        is_triggered_run : bool
            Whether the session being started is considered an "interactive" or "triggered" session. Default is False.
        parameters : Optional[List[StartSessionParameters]]
            A list of dictionaries in the format {"name": "FOO", "value": "my_value"}  representing environment
            variables propagated to the notebook session.
        open_file_paths : Optional[List[str]]
            A list of file paths to open upon instantiation of the notebook session.
        clone_repository : Optional[CloneRepositorySchema]
            Information used to clone a remote repository as part of the environment setup flow.

        Returns
        -------
        notebook_session : NotebookSession
            The created notebook session.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import Notebook

            notebook = Notebook.get(notebook_id='6556b00dcc4ea0bb7ea48121')
            session = notebook.start_session()
        """
        return NotebookSession.start(
            notebook_id=self.id,
            payload=StartSessionPayload(
                is_triggered_run=is_triggered_run,
                parameters=parameters,
                open_file_paths=open_file_paths,
                clone_repository=clone_repository,
            ),
        )

    def stop_session(self) -> NotebookSession:
        """
        Stop the current session for the notebook.

        Returns
        -------
        notebook_session : NotebookSession
            The stopped notebook session.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import Notebook

            notebook = Notebook.get(notebook_id='6556b00dcc4ea0bb7ea48121')
            session = notebook.stop_session()
        """
        return NotebookSession.stop(notebook_id=self.id)

    def execute(
        self,
        notebook_path: Optional[str] = None,
        cell_ids: Optional[List[str]] = None,
    ) -> None:
        """
        Execute the notebook. Assumes session is already started.

        Parameters
        ----------
        notebook_path : Optional[str]
            The path of the notebook to execute within the Codespace. Required if the notebook is in a Codespace.
        cell_ids : Optional[List[str]]
            The list of cell IDs to execute for a notebook. Not supported if the notebook is in a Codespace. Optional.
            If not provided, the whole notebook will be executed.
        """
        if self.is_standalone:
            if notebook_path:
                raise InvalidUsageError(
                    "Notebook path is not required for standalone notebook execution."
                )
            NotebookSession.execute_notebook(notebook_id=self.id, cell_ids=cell_ids)
        elif self.is_codespace:
            if cell_ids:
                raise InvalidUsageError(
                    "Cell IDs cannot be passed for Codespace notebook execution."
                )
            if not notebook_path:
                raise InvalidUsageError(
                    "Notebook path is required for Codespace notebook execution."
                )
            # 1. Get execution environment in order to get runtime language
            execution_environment = ExecutionEnvironment.get(notebook_id=self.id)
            kernel_spec = KernelSpec.from_image_language(execution_environment.image.language)
            # 2. Create kernel
            kernel = NotebookKernel.create(notebook_id=self.id, kernel_spec=kernel_spec)
            # 3. Assign kernel to notebook
            kernel.assign_to_notebook(notebook_id=self.id, notebook_path=notebook_path)
            # 4. Get cellIds and the notebook content generation for specific notebook path in Codespace
            notebook_state = NotebookSession.get_codespace_notebook_state(
                notebook_id=self.id, notebook_path=notebook_path
            )
            # 5. Execute Codespace notebook
            NotebookSession.execute_codespace_notebook(
                notebook_id=self.id,
                notebook_path=notebook_path,
                generation=notebook_state.generation,
                cells=notebook_state.cells,
            )

    def get_execution_status(self) -> NotebookExecutionStatus:
        """
        Get the execution status information of the notebook.

        Returns
        -------
        execution_status : NotebookExecutionStatus
            The notebook execution status information.
        """
        return NotebookSession.get_execution_status(notebook_id=self.id)

    def is_finished_executing(  # type: ignore[return]
        self,
        notebook_path: Optional[str] = None,
    ) -> bool:
        """
        Check if the notebook is finished executing.

        Parameters
        ----------
        notebook_path : Optional[str]
            The path of the notebook the Codespace. Required only if the notebook is in a Codespace.
            Will raise an error if working with a standalone notebook.

        Returns
        -------
        is_finished_executing : bool
            Whether or not the notebook has finished executing.

        Raises
        ------
        InvalidUsageError
            If attempting to check if a standalone notebook has finished executing and incorrectly
            passing a notebook path.
            If attempting to check if a codespace notebook has finished executing without passing a
            notebook path.

        KernelNotAssignedError
            If attempting to check if a codespace notebook has finished executing but the notebook
            does not have a kernel assigned.
        """
        if self.is_standalone:
            if notebook_path:
                raise InvalidUsageError(
                    "Notebook path is not required when working with standalone notebooks."
                )
            return self.get_execution_status().status == KernelExecutionStatus.IDLE
        elif self.is_codespace:
            if not notebook_path:
                raise InvalidUsageError(
                    "Notebook path is required when working with codespace notebooks."
                )
            codespace_notebook_state = NotebookSession.get_codespace_notebook_state(
                notebook_id=self.id,
                notebook_path=notebook_path,
            )
            if not codespace_notebook_state.kernel_id:
                raise KernelNotAssignedError(
                    "A codespace notebook must have a kernel assigned if it is executing."
                )
            kernel = NotebookKernel.get(
                notebook_id=self.id,
                kernel_id=codespace_notebook_state.kernel_id,
            )
            return kernel.execution_state == KernelExecutionStatus.IDLE

    def run_as_job(
        self,
        title: Optional[str] = None,
        notebook_path: Optional[str] = None,
        parameters: Optional[List[StartSessionParameters]] = None,
        manual_run_type: ManualRunType = ManualRunType.MANUAL,
    ) -> NotebookScheduledJob:
        """
        Create a manual scheduled job that runs the notebook.

        Notes
        -----
        The notebook must be part of a Use Case.
        If the notebook is in a Codespace then notebook_path is required.

        Parameters
        ----------
        title : Optional[str]
            The title of the background job. Optional.

        notebook_path : Optional[str]
            The path of the notebook to execute within the Codespace. Required if notebook is in a Codespace.

        parameters : Optional[List[StartSessionParameters]]
            A list of dictionaries in the format {"name": "FOO", "value": "my_value"}  representing environment
            variables predefined in the notebook session. Optional.

        manual_run_type : Optional[ManualRunType]
            The type of manual run being triggered. Defaults to "manual" as opposed to "pipeline".

        Returns
        -------
        notebook_scheduled_job : NotebookScheduledJob
            The created notebook schedule job.

        Raises
        ------
        InvalidUsageError
            If attempting to create a manual scheduled run for a Codespace without a notebook path.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import Notebook

            notebook = Notebook.get(notebook_id='6556b00dcc4ea0bb7ea48121')
            manual_run = notebook.run_as_job()

            # Alternatively, with title and parameters:
            # manual_run = notebook.run_as_job(title="My Run", parameters=[{"name": "FOO", "value": "bar"}])

            revision_id = manual_run.wait_for_completion()
        """
        if self.is_classic:
            raise InvalidUsageError("Notebooks must be part of a Use Case to execute a manual run.")
        if self.is_codespace and not notebook_path:
            raise InvalidUsageError("Notebook path is required for Codespace notebooks.")
        if self.is_standalone and notebook_path:
            raise InvalidUsageError("Notebook path should not be used for standalone notebooks.")

        payload: ManualRunPayload = {
            "notebook_id": self.id,
            "manual_run_type": manual_run_type,
            "title": (
                title
                if title
                else f"{self.name} {datetime.now(tz=utc).strftime('%Y-%m-%d %H:%M (UTC)')}"
            ),
        }
        if notebook_path:
            payload["notebook_path"] = notebook_path
        if parameters:
            payload["parameters"] = parameters

        r_data = self._client.post(f"{self._scheduling_path}manualRun/", data=payload)
        return NotebookScheduledJob.from_server_data(r_data.json())

    def list_schedules(
        self,
        enabled_only: bool = False,
    ) -> List[NotebookScheduledJob]:
        """
        List all NotebookScheduledJobs associated with the notebook.

        Parameters
        ----------
        enabled_only : bool
            Whether or not to return only enabled schedules.

        Returns
        -------
        notebook_schedules : List[NotebookScheduledJob]
            A list of schedules for the notebook.

        Raises
        ------
        InvalidUsageError
            If attempting to list schedules for a notebook not associated with a Use Case.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import Notebook

            notebook = Notebook.get(notebook_id='6556b00dcc4ea0bb7ea48121')
            enabled_schedules = notebook.list_schedules(enabled_only=True)
        """
        if self.is_classic:
            raise InvalidUsageError(
                "Schedules are only available for notebooks associated with Use Cases."
            )
        return NotebookScheduledJob.list(
            notebook_ids=[self.id],
            statuses=[ScheduleStatus.ENABLED] if enabled_only else None,
        )
