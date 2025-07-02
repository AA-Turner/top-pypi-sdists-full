from typing import Any, cast, Dict, List, Optional, Union
import uuid

from anyscale._private.workload import WorkloadSDK
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    CreateInternalProductionJob,
    InternalProductionJob,
    ProductionJobConfig,
)
from anyscale.client.openapi_client.models.create_job_queue_config import (
    CreateJobQueueConfig,
)
from anyscale.client.openapi_client.models.job_queue_spec import JobQueueSpec
from anyscale.client.openapi_client.models.production_job import ProductionJob
from anyscale.client.openapi_client.models.ray_runtime_env_config import (
    RayRuntimeEnvConfig,
)
from anyscale.compute_config.models import ComputeConfig
from anyscale.job.models import (
    JobConfig,
    JobLogMode,
    JobQueueConfig,
    JobRunState,
    JobRunStatus,
    JobState,
    JobStatus,
)
from anyscale.sdk.anyscale_client.models import Job
from anyscale.sdk.anyscale_client.models.ha_job_states import HaJobStates
from anyscale.sdk.anyscale_client.models.job_status import JobStatus as BackendJobStatus
from anyscale.utils.runtime_env import parse_requirements_file


logger = BlockLogger()

HA_JOB_STATE_TO_JOB_STATE = {
    HaJobStates.UPDATING: JobState.RUNNING,
    HaJobStates.RUNNING: JobState.RUNNING,
    HaJobStates.RESTARTING: JobState.RUNNING,
    HaJobStates.CLEANING_UP: JobState.RUNNING,
    HaJobStates.PENDING: JobState.STARTING,
    HaJobStates.AWAITING_CLUSTER_START: JobState.STARTING,
    HaJobStates.SUCCESS: JobState.SUCCEEDED,
    HaJobStates.ERRORED: JobState.FAILED,
    HaJobStates.TERMINATED: JobState.FAILED,
    HaJobStates.BROKEN: JobState.FAILED,
    HaJobStates.OUT_OF_RETRIES: JobState.FAILED,
}

TERMINAL_HA_JOB_STATES = [
    HaJobStates.SUCCESS,
    HaJobStates.TERMINATED,
    HaJobStates.OUT_OF_RETRIES,
]


class PrivateJobSDK(WorkloadSDK):
    _POLLING_INTERVAL_SECONDS = 10.0

    def _populate_runtime_env(
        self,
        config: JobConfig,
        *,
        autopopulate_in_workspace: bool = True,
        cloud_id: Optional[str] = None,
        workspace_requirements_path: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Populates a runtime_env from the config.

        Local directories specified in the 'working_dir' will be uploaded and
        replaced with the resulting remote URIs.

        Requirements files will be loaded and populated into the 'pip' field.

        If autopopulate_from_workspace is passed and this code is running inside a
        workspace, the following defaults will be applied:
            - 'working_dir' will be set to '.'.
            - 'pip' will be set to the workspace-managed requirements file.
        """
        runtime_env: Dict[str, Any] = {}
        [runtime_env] = self.override_and_upload_local_dirs(
            [runtime_env],
            working_dir_override=config.working_dir,
            excludes_override=config.excludes,
            cloud_id=cloud_id,
            autopopulate_in_workspace=autopopulate_in_workspace,
            additional_py_modules=config.py_modules,
            py_executable_override=config.py_executable,
        )
        [runtime_env] = self.override_and_load_requirements_files(
            [runtime_env],
            requirements_override=config.requirements,
            workspace_requirements_path=workspace_requirements_path,
        )
        [runtime_env] = self.update_env_vars(
            [runtime_env], env_vars_updates=config.env_vars,
        )

        return runtime_env or None

    def get_default_name(self) -> str:
        """Get a default name for the job.

        If running inside a workspace, this is generated from the workspace name,
        else it generates a random name.
        """
        # TODO(edoakes): generate two random words instead of UUID here.
        name = f"job-{self.get_current_workspace_name() or str(uuid.uuid4())}"
        self.logger.info(f"No name was specified, using default: '{name}'.")
        return name

    def job_config_to_internal_prod_job_conf(
        self, config: JobConfig, name: str, cloud_id: str, compute_config_id: str,
    ) -> ProductionJobConfig:
        build_id = None
        if config.containerfile is not None:
            build_id = self._image_sdk.build_image_from_containerfile(
                name=f"image-for-job-{name}",
                containerfile=self.get_containerfile_contents(config.containerfile),
                ray_version=config.ray_version,
            )
        elif config.image_uri is not None:
            build_id = self._image_sdk.registery_image(
                image_uri=config.image_uri,
                registry_login_secret=config.registry_login_secret,
                ray_version=config.ray_version,
            )

        if self._image_sdk.enable_image_build_for_tracked_requirements:
            requirements_path_to_be_populated_in_runtime_env = None
            requirements_path = self.client.get_workspace_requirements_path()
            if requirements_path is not None:
                requirements = parse_requirements_file(requirements_path)
                if requirements:
                    build_id = self._image_sdk.build_image_from_requirements(
                        name=f"image-for-job-{name}",
                        base_build_id=self.client.get_default_build_id(),
                        requirements=requirements,
                    )
        else:
            requirements_path_to_be_populated_in_runtime_env = (
                self.client.get_workspace_requirements_path()
            )

        if build_id is None:
            build_id = self.client.get_default_build_id()

        env_vars_from_workspace = self.client.get_workspace_env_vars()
        if env_vars_from_workspace:
            if config.env_vars:
                # the precedence should be cli > workspace
                env_vars_from_workspace.update(config.env_vars)
                config = config.options(env_vars=env_vars_from_workspace)
            else:
                config = config.options(env_vars=env_vars_from_workspace)

        runtime_env = self._populate_runtime_env(
            config,
            cloud_id=cloud_id,
            workspace_requirements_path=requirements_path_to_be_populated_in_runtime_env,
        )

        return ProductionJobConfig(
            entrypoint=config.entrypoint,
            runtime_env=runtime_env,
            build_id=build_id,
            compute_config_id=compute_config_id,
            max_retries=config.max_retries,
            timeout_s=config.timeout_s,
        )

    def create_job_queue_config(
        self, provided_job_queue_config: JobQueueConfig
    ) -> CreateJobQueueConfig:
        job_queue_spec: Optional[JobQueueSpec] = None

        provided_job_queue_spec = provided_job_queue_config.job_queue_spec

        if provided_job_queue_spec:
            compute_config_id = (
                self._resolve_compute_config_id(provided_job_queue_spec.compute_config)
                if provided_job_queue_spec.compute_config
                else None
            )

            job_queue_spec = JobQueueSpec(
                job_queue_name=provided_job_queue_spec.name,
                execution_mode=provided_job_queue_spec.execution_mode,
                compute_config_id=compute_config_id,
                max_concurrency=provided_job_queue_spec.max_concurrency,
                idle_timeout_sec=provided_job_queue_spec.idle_timeout_s,
                auto_termination_threshold_job_count=provided_job_queue_spec.auto_termination_threshold_job_count,
            )

        job_queue_config = CreateJobQueueConfig(
            priority=provided_job_queue_config.priority,
            target_job_queue_name=provided_job_queue_config.target_job_queue_name,
            job_queue_spec=job_queue_spec,
        )
        return job_queue_config

    def submit(self, config: JobConfig) -> str:
        name = config.name or self.get_default_name()
        compute_config_id, cloud_id = self.resolve_compute_config_and_cloud_id(
            compute_config=config.compute_config, cloud=config.cloud
        )

        project_id = self.client.get_project_id(
            parent_cloud_id=cloud_id, name=config.project
        )

        prod_job_config = self.job_config_to_internal_prod_job_conf(
            config=config,
            name=name,
            cloud_id=cloud_id,
            compute_config_id=compute_config_id,
        )

        job_queue_config: Optional[CreateJobQueueConfig] = None

        provided_job_queue_config = config.job_queue_config

        if provided_job_queue_config:
            job_queue_config = self.create_job_queue_config(provided_job_queue_config)

        job: InternalProductionJob = self.client.submit_job(
            CreateInternalProductionJob(
                name=name,
                project_id=project_id,
                workspace_id=self.client.get_current_workspace_id(),
                config=prod_job_config,
                job_queue_config=job_queue_config,
            )
        )

        self.logger.info(f"Job '{job.name}' submitted, ID: '{job.id}'.")
        self.logger.info(
            f"View the job in the UI: {self.client.get_job_ui_url(job.id)}"
        )
        return job.id

    _BACKEND_JOB_STATUS_TO_JOB_RUN_STATE = {
        BackendJobStatus.RUNNING: JobRunState.RUNNING,
        BackendJobStatus.COMPLETED: JobRunState.SUCCEEDED,
        BackendJobStatus.PENDING: JobRunState.STARTING,
        BackendJobStatus.STOPPED: JobRunState.FAILED,
        BackendJobStatus.SUCCEEDED: JobRunState.SUCCEEDED,
        BackendJobStatus.FAILED: JobRunState.FAILED,
        BackendJobStatus.UNKNOWN: JobRunState.UNKNOWN,
    }

    def _job_state_from_job_model(self, model: ProductionJob) -> JobState:
        ha_state = model.state.current_state if model.state else None
        return cast(JobState, HA_JOB_STATE_TO_JOB_STATE.get(ha_state, JobState.UNKNOWN))

    def _job_run_model_to_job_run_status(self, run: Job) -> JobRunStatus:
        state = self._BACKEND_JOB_STATUS_TO_JOB_RUN_STATE.get(
            run.status, JobRunState.UNKNOWN
        )
        return JobRunStatus(name=run.name, state=state)

    def prod_job_config_to_job_config(
        self, prod_job_config: ProductionJobConfig, name: str, project: str,
    ) -> JobConfig:
        runtime_env_config: RayRuntimeEnvConfig = prod_job_config.runtime_env if prod_job_config else None
        compute_config = self.get_user_facing_compute_config(
            prod_job_config.compute_config_id
        )
        return JobConfig(
            name=name,
            compute_config=compute_config,
            requirements=runtime_env_config.pip if runtime_env_config else None,
            working_dir=runtime_env_config.working_dir if runtime_env_config else None,
            env_vars=runtime_env_config.env_vars if runtime_env_config else None,
            py_executable=runtime_env_config.py_executable
            if runtime_env_config
            else None,
            entrypoint=prod_job_config.entrypoint,
            cloud=compute_config.cloud
            if compute_config and isinstance(compute_config, ComputeConfig)
            else None,
            max_retries=prod_job_config.max_retries
            if prod_job_config.max_retries is not None
            else -1,
            project=project,
        )

    def _job_model_to_status(self, model: ProductionJob, runs: List[Job]) -> JobStatus:
        state = self._job_state_from_job_model(model)
        project_model = self.client.get_project(model.project_id)
        project = (
            project_model.name
            if project_model is not None and project_model.name != "default"
            else None
        )

        prod_job_config: ProductionJobConfig = model.config
        config = self.prod_job_config_to_job_config(
            prod_job_config=prod_job_config, name=model.name, project=project
        )
        runs = [self._job_run_model_to_job_run_status(run) for run in runs]

        return JobStatus(
            name=model.name,
            id=model.id,
            state=state,
            runs=runs,
            config=config,
            creator_id=model.creator_id,
        )

    def _resolve_to_job_model(
        self,
        *,
        name: Optional[str] = None,
        job_id: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> ProductionJob:
        if name is None and job_id is None:
            raise ValueError("One of 'name' or 'job_id' must be provided.")

        if name is not None and job_id is not None:
            raise ValueError("Only one of 'name' or 'job_id' can be provided.")

        if job_id is not None and (cloud is not None or project is not None):
            raise ValueError("'cloud' and 'project' should only be used with 'name'.")

        model: Optional[ProductionJob] = self.client.get_job(
            name=name, job_id=job_id, cloud=cloud, project=project
        )
        if model is None:
            if name is not None:
                raise RuntimeError(f"Job with name '{name}' was not found.")
            else:
                raise RuntimeError(f"Job with ID '{job_id}' was not found.")

        return model

    def status(
        self,
        *,
        name: Optional[str] = None,
        job_id: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> JobStatus:
        job_model = self._resolve_to_job_model(
            name=name, job_id=job_id, cloud=cloud, project=project
        )
        runs = self.client.get_job_runs(job_model.id)
        return self._job_model_to_status(model=job_model, runs=runs)

    def terminate(
        self,
        *,
        job_id: Optional[str] = None,
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        job_model = self._resolve_to_job_model(
            name=name, job_id=job_id, cloud=cloud, project=project
        )
        self.client.terminate_job(job_model.id)
        self.logger.info(f"Marked job '{job_model.name}' for termination")
        return job_model.id

    def archive(
        self,
        *,
        job_id: Optional[str] = None,
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        job_model = self._resolve_to_job_model(
            name=name, job_id=job_id, cloud=cloud, project=project
        )

        ha_state = job_model.state.current_state if job_model.state else None
        if ha_state not in TERMINAL_HA_JOB_STATES:
            raise RuntimeError(
                f"Job with ID '{job_model.id}' has not reached a terminal state and cannot be archived."
            )

        self.client.archive_job(job_model.id)
        self.logger.info(f"Job {job_model.id} is successfully archived.")
        return job_model.id

    def wait(
        self,
        *,
        name: Optional[str] = None,
        job_id: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        state: Union[str, JobState] = JobState.SUCCEEDED,
        timeout_s: float = 1800,
        interval_s: float = _POLLING_INTERVAL_SECONDS,
    ):
        if not isinstance(timeout_s, (int, float)):
            raise TypeError("timeout_s must be a float")
        if timeout_s <= 0:
            raise ValueError("timeout_s must be >= 0")

        if not isinstance(interval_s, (int, float)):
            raise TypeError("interval_s must be a float")
        if interval_s <= 0:
            raise ValueError("interval_s must be >= 0")

        if not isinstance(state, JobState):
            raise TypeError("'state' must be a JobState.")

        job_id_or_name = job_id or name
        job_model = self._resolve_to_job_model(
            name=name, job_id=job_id, cloud=cloud, project=project
        )
        curr_state = self._job_state_from_job_model(job_model)

        self.logger.info(
            f"Waiting for job '{job_id_or_name}' to reach target state {state}, currently in state: {curr_state}"
        )
        for _ in self.timer.poll(timeout_s=timeout_s, interval_s=interval_s):
            job_model = self._resolve_to_job_model(
                name=name, job_id=job_id, cloud=cloud, project=project
            )
            new_state = self._job_state_from_job_model(job_model)

            if new_state != curr_state:
                self.logger.info(
                    f"Job '{job_id_or_name}' transitioned from {curr_state} to {new_state}"
                )
                curr_state = new_state

            if curr_state == state:
                self.logger.info(
                    f"Job '{job_id_or_name}' reached target state, exiting"
                )
                break

            if JobState.is_terminal(curr_state):
                raise RuntimeError(
                    f"Job '{job_id_or_name}' reached terminal state '{curr_state}', and will not reach '{state}'."
                )
        else:
            raise TimeoutError(
                f"Job '{job_id_or_name}' did not reach target state {state} within {timeout_s}s. Last seen state: {curr_state}."
            )

    def _resolve_job_run_id(
        self,
        *,
        job_id: Optional[str] = None,
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        run: Optional[str] = None,
    ) -> str:
        job_model = self._resolve_to_job_model(
            name=name, job_id=job_id, cloud=cloud, project=project
        )

        last_job_run_id = job_model.last_job_run_id
        if last_job_run_id is None:
            return ""
        if run is None:
            job_run_id = last_job_run_id
        else:
            runs: List[Job] = self.client.get_job_runs(job_model.id)
            for job_run in runs:
                if job_run.name == run:
                    job_run_id = job_run.id
                    break
            else:
                raise ValueError(
                    f"Job run '{run}' was not found for job '{job_id or name}'."
                )

        return job_run_id

    def get_logs(
        self,
        *,
        job_id: Optional[str] = None,
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        run: Optional[str] = None,
        mode: Union[str, JobLogMode] = JobLogMode.TAIL,
        max_lines: Optional[int] = None,
    ) -> str:
        if max_lines is not None:
            if not isinstance(max_lines, int):
                raise TypeError("max_lines must be an int")
            if max_lines <= 0:
                raise ValueError("max_lines must be > 0")

        job_run_id = self._resolve_job_run_id(
            job_id=job_id, name=name, cloud=cloud, project=project, run=run
        )

        head = mode == JobLogMode.HEAD
        return self.client.logs_for_job_run(
            job_run_id=job_run_id, head=head, max_lines=max_lines
        )
