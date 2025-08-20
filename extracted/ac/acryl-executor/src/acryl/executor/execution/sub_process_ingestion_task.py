# Copyright 2021 Acryl Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import asyncio.exceptions
import logging
import os
import signal
import tarfile
from asyncio import tasks
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import IO, Any, Optional

from acryl.executor.cloud_utils.cloud_copier import CloudCopier
from acryl.executor.cloud_utils.executor_credentials import ExecutorCredentials
from acryl.executor.cloud_utils.s3_cloud_copier import S3CloudCopier
from acryl.executor.common.config import ConfigModel
from acryl.executor.context.execution_context import ExecutionContext
from acryl.executor.context.executor_context import ExecutorContext
from acryl.executor.execution.runner import (
    LogHolder,
    SubprocessRunner,
    VenvConfig,
    VenvReference,
    setup_venv,
)
from acryl.executor.execution.sub_process_task_common import (
    SubProcessRecipeTaskArgs,
    SubProcessTaskUtil,
)
from acryl.executor.execution.task import Task, TaskError

logger = logging.getLogger(__name__)

ARTIFACTS_DIR_NAME = "artifacts"

DATAHUB_CLOUD_LOG_BUCKET_ENV_VAR = "DATAHUB_CLOUD_LOG_BUCKET"
DATAHUB_CLOUD_LOG_PATH_ENV_VAR = "DATAHUB_CLOUD_LOG_PATH"


class SubProcessIngestionTaskConfig(ConfigModel):
    tmp_dir: str = "/tmp/datahub/ingest"
    log_dir: str = "/tmp/datahub/logs"
    heartbeat_time_seconds: int = 2
    max_log_lines: int = SubProcessTaskUtil.MAX_LOG_LINES
    # The following are optional and only used for uploading logs to S3
    cloud_log_bucket: Optional[str] = os.environ.get(DATAHUB_CLOUD_LOG_BUCKET_ENV_VAR)
    cloud_log_path: Optional[str] = os.environ.get(DATAHUB_CLOUD_LOG_PATH_ENV_VAR, "")


class SubProcessIngestionTaskArgs(SubProcessRecipeTaskArgs):
    debug_mode: str = "false"  # Expected values are "true" or "false".


class SubProcessIngestionTask(Task):
    config: SubProcessIngestionTaskConfig
    tmp_dir: str  # Location where tmp files will be written (recipes)
    ctx: ExecutorContext

    @classmethod
    def create(cls, config: dict, ctx: ExecutorContext) -> "Task":
        return cls(SubProcessIngestionTaskConfig.parse_obj(config), ctx)

    def __init__(self, config: SubProcessIngestionTaskConfig, ctx: ExecutorContext):
        self.config = config
        self.tmp_dir = config.tmp_dir
        self.ctx = ctx

    @contextmanager
    def _temporary_log_level(self, level: int) -> Generator:
        """Temporarily change the log level for the current logger and its handlers."""
        original_levels: dict[Any, int] = {}
        try:
            original_levels[logger] = logger.level
            for handler in logger.handlers:
                original_levels[handler] = handler.level
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)

            yield
        finally:
            logger.setLevel(original_levels[logger])
            for handler in logger.handlers:
                if handler in original_levels:
                    handler.setLevel(original_levels[handler])

    def create_tar_from_dir(self, dir_path: str) -> Optional[Path]:
        logger.info(f"Creating tar archives for {dir_path}")
        base_name = os.path.basename(dir_path)
        has_files = False
        tar_file = Path(dir_path).joinpath(f"{base_name}.tgz")

        # We list dirs here to make sure the tar file itself won't be included in the tar file
        files = os.listdir(dir_path)
        with tarfile.open(tar_file, "w:gz") as tar:
            for item in files:
                item_path = os.path.join(dir_path, item)
                logger.info(f"Added to {base_name}.tgz: {item_path}")
                tar.add(item_path, arcname=item)
                has_files = True

        if not has_files:
            return None

        return tar_file

    def create_tar_archives(
        self, artifacts_path: str, cloud_copier: CloudCopier
    ) -> None:
        # Ensure the artifacts_path is absolute
        artifacts_path = os.path.abspath(artifacts_path)

        # Check if the base path exists and is a directory
        if not os.path.exists(artifacts_path) or not os.path.isdir(artifacts_path):
            raise ValueError(
                f"The provided path '{artifacts_path}' does not exist or is not a directory."
            )
        tars = []
        # Iterate over the items in the base directory
        for item in os.listdir(artifacts_path):
            item_path = os.path.join(artifacts_path, item)
            if os.path.isdir(item_path) and item != "artifacts":
                logger.debug(f"Initiate Creating tar archives for {item_path}")
                tar_file = self.create_tar_from_dir(item_path)
                if tar_file:
                    logger.info(f"Created archive: {tar_file}")
                    tars.append(tar_file)

        # Iterate over the items in the artifacts directory
        for item in os.listdir(os.path.join(artifacts_path, "artifacts")):
            item_path = os.path.join(artifacts_path, "artifacts", item)
            if os.path.isdir(item_path):
                logger.debug(f"Initiate Creating tar archives for {item_path}")
                tar_file = self.create_tar_from_dir(item_path)
                if tar_file:
                    logger.info(f"Created archive: {tar_file}")
                    tars.append(tar_file)

        # Create a single tar archive for the single files in the artifacts directory
        for item in os.listdir(os.path.join(artifacts_path, "artifacts")):
            item_path = os.path.join(artifacts_path, "artifacts", item)
            if os.path.isfile(item_path) and not item.endswith(".tgz"):
                tar_file = Path(item_path).with_suffix(".tgz")
                with tarfile.open(tar_file, "w:gz") as artifacts_tar:
                    # Add files directly under the base directory to the artifacts.tgz
                    artifacts_tar.add(item_path, arcname=item)
                    logger.debug(f"Added to {tar_file}: {item_path}")
                logger.info(f"Created archive: {tar_file}")
                tars.append(tar_file)

        for tar_to_upload in tars:
            try:
                relative_path = str(tar_to_upload).replace(artifacts_path, "")
                cloud_copier.upload(str(tar_to_upload), relative_path)
            except Exception:
                logger.exception(f"Failed to upload {tar_to_upload} to S3")
            finally:
                tar_to_upload.unlink()

    def _setup_directories(self, exec_id: str) -> tuple[str, str, str]:
        """Setup execution directories and return paths."""
        exec_out_dir = f"{self.tmp_dir}/{exec_id}"
        artifact_output_dir = f"{self.config.log_dir}/{exec_id}"
        mode = 0o755

        (Path(artifact_output_dir) / "executor-logs").mkdir(
            mode, parents=True, exist_ok=True
        )
        Path(artifact_output_dir).joinpath("artifacts").mkdir(
            mode, parents=True, exist_ok=True
        )

        return (
            exec_out_dir,
            artifact_output_dir,
            f"{artifact_output_dir}/artifacts/ingestion_report.json",
        )

    def _prepare_subprocess_environment(
        self,
        validated_args: SubProcessIngestionTaskArgs,
        exec_out_dir: str,
        artifact_output_dir: str,
    ) -> dict:
        """Prepare environment variables for subprocess."""
        subprocess_env = validated_args.get_combined_env_vars()
        subprocess_env["INGESTION_ARTIFACT_DIR"] = f"{artifact_output_dir}/artifacts"
        subprocess_env.setdefault("TMPDIR", exec_out_dir)
        return subprocess_env

    async def _setup_venv(
        self,
        validated_args: SubProcessIngestionTaskArgs,
        plugin: str,
        exec_out_dir: str,
        shared_logs: LogHolder,
    ) -> VenvReference:
        """Set up the virtual environment using Python utilities with shared logging."""
        # Create venv configuration from subprocess args
        venv_config = VenvConfig(
            version=validated_args.version,
            main_plugin=plugin,
            extra_pip_requirements=validated_args.extra_pip_requirements,
            extra_pip_plugins=validated_args.extra_pip_plugins,
            extra_env_vars=validated_args.extra_env_vars,
        )

        # Use shared LogHolder for venv setup - logs will appear in subprocess output
        venv_runner = SubprocessRunner(logs=shared_logs)

        logger.info(
            f"Setting up venv for plugin '{plugin}' with version '{validated_args.version}'"
        )

        # Add venv setup status to shared logs so it appears in subprocess output
        shared_logs.append(
            f"Setting up venv for plugin '{plugin}' with version '{validated_args.version}'\n"
        )

        if validated_args.should_use_bundled_venv():
            logger.info("Using Bundled startup (pre-built) venv")
            shared_logs.append("Using Bundled startup (pre-built) venv\n")
        else:
            logger.info("Creating dynamic venv - this may take a few minutes...")
            shared_logs.append(
                "Creating dynamic venv - this may take a few minutes...\n"
            )

        try:
            # Set up the venv using our Python utilities
            venv_ref = await setup_venv(
                venv_config=venv_config,
                runner=venv_runner,
                tmp_dir=Path(exec_out_dir),
            )

            logger.info(f"Venv ready at: {venv_ref.venv_loc}")
            shared_logs.append(f"✅ Venv ready at: {venv_ref.venv_loc}\n")

            return venv_ref

        except Exception as e:
            logger.error(f"Venv setup failed: {e}")
            shared_logs.append(f"❌ Venv setup failed: {e}\n")
            raise TaskError(f"Failed to set up virtual environment: {e}") from e

    async def _create_subprocess(
        self,
        validated_args: SubProcessIngestionTaskArgs,
        plugin: str,
        recipe_file_path: str,
        report_out_file: str,
        subprocess_env: dict,
        exec_out_dir: str,
        shared_logs: LogHolder,
    ) -> asyncio.subprocess.Process:
        """Create and return the ingestion subprocess."""
        # First, set up the venv using Python utilities with shared logging
        venv_ref = await self._setup_venv(
            validated_args, plugin, exec_out_dir, shared_logs
        )

        # Now create subprocess with simplified shell script (no log file needed!)
        command_script = "run_ingest.sh"
        debug_mode = validated_args.debug_mode

        # Log the execution mode
        if validated_args.should_use_bundled_venv():
            logger.info(
                f"Running ingestion with Bundled startup venv: {venv_ref.venv_loc}"
            )
        else:
            logger.info(f"Running ingestion with dynamic venv: {venv_ref.venv_loc}")

        # Prepare environment with venv information (no log file needed)
        venv_env = {
            **subprocess_env,
            **venv_ref.extra_envs(),
            "VENV_PATH": str(venv_ref.venv_loc),
        }

        return await asyncio.create_subprocess_exec(
            *[
                command_script,
                str(venv_ref.venv_loc),  # Pass venv path directly
                recipe_file_path,
                report_out_file,
                debug_mode,
                # No log file argument needed anymore!
            ],
            env=venv_env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            limit=SubProcessTaskUtil.SUBPROCESS_BUFFER_SIZE,
        )

    async def execute(self, args: dict, ctx: ExecutionContext) -> None:
        exec_id = ctx.exec_id  # The unique execution id.

        # 0. Validate arguments
        validated_args = SubProcessIngestionTaskArgs.parse_obj(args)

        # Set debug log level if debug_mode is "true"
        if validated_args.debug_mode == "true":
            with self._temporary_log_level(logging.DEBUG):
                logger.debug("Debug mode enabled - setting log level to DEBUG")
                await self._execute_with_debug(validated_args, ctx, exec_id)
        else:
            await self._execute_with_debug(validated_args, ctx, exec_id)

    async def _execute_with_debug(
        self,
        validated_args: SubProcessIngestionTaskArgs,
        ctx: ExecutionContext,
        exec_id: str,
    ) -> None:
        """Execute the ingestion task with the given arguments."""
        # 1. Resolve the recipe (combine it with others)
        recipe: dict = SubProcessTaskUtil._resolve_recipe(
            validated_args.recipe, ctx, self.ctx
        )
        plugin: str = SubProcessTaskUtil._get_plugin_from_recipe(recipe)

        # 2. Write recipe file to local FS (requires write permissions to /tmp directory)
        exec_out_dir, artifact_output_dir, report_out_file = self._setup_directories(
            exec_id
        )
        recipe_file_path = SubProcessTaskUtil._write_recipe_to_file(
            exec_out_dir, recipe
        )

        # 3. Prepare subprocess environment and create subprocess
        subprocess_env = self._prepare_subprocess_environment(
            validated_args, exec_out_dir, artifact_output_dir
        )
        logger.debug(f"Subprocess environment: {subprocess_env}")
        if DATAHUB_CLOUD_LOG_BUCKET_ENV_VAR in subprocess_env:
            self.config.cloud_log_bucket = subprocess_env[
                DATAHUB_CLOUD_LOG_BUCKET_ENV_VAR
            ]
        if DATAHUB_CLOUD_LOG_PATH_ENV_VAR in subprocess_env:
            self.config.cloud_log_path = subprocess_env[DATAHUB_CLOUD_LOG_PATH_ENV_VAR]
        logger.debug(f"Cloud log bucket: {self.config.cloud_log_bucket}")
        logger.debug(f"Cloud log path: {self.config.cloud_log_path}")

        # Create shared LogHolder for both venv setup and subprocess monitoring
        shared_logs = LogHolder(
            max_log_lines=self.config.max_log_lines,
            echo_to_stdout_prefix=f"[{exec_id} logs] ",
        )
        full_log_file = open(
            f"{artifact_output_dir}/executor-logs/ingestion-logs.log", "w"
        )

        logger.info(f"Starting ingestion subprocess for exec_id={exec_id} ({plugin})")
        ingest_process = await self._create_subprocess(
            validated_args,
            plugin,
            recipe_file_path,
            report_out_file,
            subprocess_env,
            exec_out_dir,
            shared_logs,
        )

        try:
            await self._monitor_subprocess(
                ingest_process, exec_id, ctx, shared_logs, full_log_file
            )
        finally:
            self._handle_subprocess_completion(
                ingest_process,
                ctx,
                report_out_file,
                artifact_output_dir,
                recipe,
                exec_out_dir,
                shared_logs,
            )

    async def _monitor_subprocess(
        self,
        ingest_process: asyncio.subprocess.Process,
        exec_id: str,
        ctx: ExecutionContext,
        shared_logs: LogHolder,
        full_log_file: IO[str],
    ) -> None:
        """Monitor subprocess execution with async tasks for output reading and progress reporting."""
        most_recent_log_ts: Optional[datetime] = None

        async def _read_output_lines() -> None:
            nonlocal most_recent_log_ts
            while True:
                assert ingest_process.stdout

                # We can't use the readline method directly.
                # When the readline method hits a LimitOverrunError, it will
                # discard the line or possibly the entire buffer.
                try:
                    line_bytes = await ingest_process.stdout.readuntil(b"\n")
                except asyncio.exceptions.CancelledError:
                    logger.info(
                        f"Got asyncio.CancelledError for exec_id={exec_id} - stopping log monitor"
                    )
                    break
                except asyncio.exceptions.IncompleteReadError as e:
                    # This happens when we reach the end of the stream.
                    line_bytes = e.partial
                except asyncio.exceptions.LimitOverrunError:
                    line_bytes = await ingest_process.stdout.read(
                        SubProcessTaskUtil.MAX_BYTES_PER_LINE
                    )

                # At this point, if line_bytes is empty, then we're at EOF.
                # If it ends with a newline, then we successfully read a line.
                # If it does not end with a newline, then we hit a LimitOverrunError
                # and it contains a partial line.

                if not line_bytes:
                    logger.info(
                        f"Got EOF from subprocess exec_id={exec_id} - stopping log monitor"
                    )
                    break
                line = line_bytes.decode("utf-8")

                most_recent_log_ts = datetime.now(tz=timezone.utc)

                full_log_file.write(line)

                # Use LogHolder's built-in functionality - it handles all the line management
                shared_logs.append(line)

                await asyncio.sleep(0)

        async def _report_progress() -> None:
            while True:
                if ingest_process.returncode is not None:
                    logger.info(
                        f"Detected subprocess return code {ingest_process.returncode}, "
                        f"exec_id={exec_id} - stopping logs reporting"
                    )
                    break

                await asyncio.sleep(self.config.heartbeat_time_seconds)

                # Report progress
                if ctx.request.progress_callback:
                    if most_recent_log_ts is None:
                        report = "No logs yet"
                    else:
                        report = SubProcessTaskUtil._format_log_lines(
                            shared_logs.get_lines()
                        )
                        current_time = datetime.now(tz=timezone.utc)
                        if most_recent_log_ts < current_time - timedelta(minutes=2):
                            message = (
                                f"WARNING: These logs appear to be stale. No new logs have been received since {most_recent_log_ts} ({(current_time - most_recent_log_ts).seconds} seconds ago). "
                                "However, the ingestion process still appears to be running and may complete normally."
                            )
                            report = f"{report}\n\n{message}"

                    # TODO maybe use the normal report field here?
                    logger.debug(f"Reporting in-progress for exec_id={exec_id}")
                    ctx.request.progress_callback(report)

                full_log_file.flush()
                await asyncio.sleep(0)

        async def _process_waiter() -> None:
            await ingest_process.wait()
            logger.info(f"Detected subprocess exited exec_id={exec_id}")

        read_output_task = asyncio.create_task(_read_output_lines())
        report_progress_task = asyncio.create_task(_report_progress())
        process_waiter_task = asyncio.create_task(_process_waiter())

        group = tasks.gather(
            read_output_task, report_progress_task, process_waiter_task
        )
        try:
            await group
        except (Exception, asyncio.exceptions.CancelledError) as e:
            # This could just be a normal cancellation or it could be that
            # one of the monitoring tasks threw an exception.
            # In this case, we should kill the subprocess and cancel the other tasks.
            ingest_process.terminate()

            # If the cause of the exception was a cancellation, then this is a no-op
            # because the gather method already propagates the cancellation.
            group.cancel()

            # ALL_COMPLETED means we wait for all tasks to finish, even if one of them
            # throws an exception. Set timeout to 60s to avoid hanging forever.
            _done, pending = await asyncio.wait(
                (
                    asyncio.create_task(ingest_process.wait()),
                    read_output_task,
                    report_progress_task,
                    process_waiter_task,
                ),
                timeout=60,
                return_when=asyncio.ALL_COMPLETED,
            )
            if pending:
                logger.info(f"Failed to cancel {len(pending)} tasks on cleanup.")
                ingest_process.kill()

            if isinstance(e, asyncio.CancelledError):
                # If it was a cancellation, then we re-raise.
                raise
            else:
                raise RuntimeError(
                    f"Something went wrong in the subprocess executor: {e}"
                ) from e
        finally:
            full_log_file.close()

    def _get_executor_credentials(self) -> Optional[dict]:
        """Get executor credentials from GraphQL API if DATAHUB_EXECUTOR_POOL_ID is present."""
        executor_pool_id = os.environ.get("DATAHUB_EXECUTOR_POOL_ID")
        if not executor_pool_id:
            return None

        credentials_client = ExecutorCredentials.from_environment()
        if not credentials_client:
            return None

        return credentials_client.get_executor_credentials(executor_pool_id)

    def _handle_subprocess_completion(
        self,
        ingest_process: asyncio.subprocess.Process,
        ctx: ExecutionContext,
        report_out_file: str,
        artifact_output_dir: str,
        recipe: dict,
        exec_out_dir: str,
        shared_logs: LogHolder,
    ) -> None:
        """Handle subprocess completion, including report processing and cleanup."""
        # Get executor credentials if available
        executor_credentials = self._get_executor_credentials()

        if os.path.exists(report_out_file):
            with open(report_out_file) as structured_report_fp:
                ctx.get_report().set_structured_report(structured_report_fp.read())

        if self.config.cloud_log_bucket:
            upload_time = datetime.now()
            partition = f"year={upload_time.strftime('%Y')}/month={upload_time.strftime('%m')}/day={upload_time.strftime('%d')}"
            try:
                path_to_upload = (
                    (self.config.cloud_log_path or "")
                    + "/"
                    + recipe.get("pipeline_name", "unknown_pipeline").replace(
                        "urn:li:dataHubIngestionSource:", ""
                    )
                    + "/"
                    + partition
                    + "/"
                    + ctx.exec_id
                )
                logger.debug(
                    f"Uploading logs to S3 bucket {self.config.cloud_log_bucket} with path {path_to_upload}"
                )

                # Create S3CloudCopier with executor credentials if available
                if executor_credentials:
                    cloud_copier = S3CloudCopier(
                        self.config.cloud_log_bucket,
                        path_to_upload,
                        aws_access_key_id=executor_credentials.get("access_key_id"),
                        aws_secret_access_key=executor_credentials.get(
                            "secret_access_key"
                        ),
                        aws_session_token=executor_credentials.get("session_token"),
                        region_name=executor_credentials.get("region"),
                    )
                else:
                    cloud_copier = S3CloudCopier(
                        self.config.cloud_log_bucket,
                        path_to_upload,
                    )
                self.create_tar_archives(artifact_output_dir, cloud_copier)
            except Exception:
                logging.exception("Failed to upload logs to S3")
        else:
            logger.debug("No S3 bucket configured, skipping log upload")

        ctx.get_report().set_logs(
            SubProcessTaskUtil._format_log_lines(shared_logs.get_lines())
        )

        # Cleanup by removing the recipe file
        SubProcessTaskUtil._remove_directory(exec_out_dir)

        return_code = ingest_process.returncode
        if return_code != 0:  # Failed
            if return_code and return_code < 0:
                try:
                    signal_name = signal.Signals(-return_code).name
                except ValueError:
                    signal_name = str(-return_code)
                ctx.get_report().report_error(
                    f"The ingestion process was killed by signal {signal_name} likely because it ran out of memory. "
                    "You can resolve this issue by allocating more memory to the datahub-actions container."
                )
            elif return_code == 137:
                ctx.get_report().report_error(
                    "The ingestion process was terminated with exit code 137, likely because it ran out of memory."
                    "You can resolve this issue by allocating more memory to the datahub-actions container."
                )
            else:
                ctx.get_report().report_info(
                    f"Failed to execute 'datahub ingest', exit code {return_code}"
                )
            raise TaskError("Failed to execute 'datahub ingest'")

        # Report Successful execution
        ctx.get_report().report_info("Successfully executed 'datahub ingest'")

    def close(self) -> None:
        pass
