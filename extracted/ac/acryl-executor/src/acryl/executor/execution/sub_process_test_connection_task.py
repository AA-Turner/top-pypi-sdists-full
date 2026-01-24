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
import logging
import os
import subprocess
import sys
from collections import deque
from pathlib import Path

from datahub.masking.bootstrap import initialize_secret_masking, shutdown_secret_masking
from datahub.masking.masking_filter import SecretMaskingFilter
from datahub.masking.secret_registry import SecretRegistry

from acryl.executor.common.config import ConfigModel
from acryl.executor.context.execution_context import ExecutionContext
from acryl.executor.context.executor_context import ExecutorContext
from acryl.executor.execution.runner import (
    LogHolder,
    SubprocessRunner,
    VenvConfig,
    setup_venv,
)
from acryl.executor.execution.sub_process_task_common import (
    SubProcessRecipeTaskArgs,
    SubProcessTaskUtil,
)
from acryl.executor.execution.task import Task, TaskError

logger = logging.getLogger(__name__)


class SubProcessTestConnectionTaskConfig(ConfigModel):
    tmp_dir: str = "/tmp/datahub/ingest"


class SubProcessTestConnectionTaskArgs(SubProcessRecipeTaskArgs):
    pass


class SubProcessTestConnectionTask(Task):
    config: SubProcessTestConnectionTaskConfig
    tmp_dir: str  # Location where tmp files will be written (recipes)
    ctx: ExecutorContext

    @classmethod
    def create(cls, config: dict, ctx: ExecutorContext) -> "Task":
        config_parsed = SubProcessTestConnectionTaskConfig.model_validate(config)
        return cls(config_parsed, ctx)

    def __init__(
        self, config: SubProcessTestConnectionTaskConfig, ctx: ExecutorContext
    ):
        self.config = config
        self.tmp_dir = config.tmp_dir
        self.ctx = ctx

    async def execute(self, args: dict, ctx: ExecutionContext) -> None:
        exec_id = ctx.exec_id  # The unique execution id.

        exec_out_dir = f"{self.tmp_dir}/{exec_id}"

        # 0. Validate arguments
        validated_args = SubProcessTestConnectionTaskArgs.model_validate(args)

        # 1. Resolve the recipe (combine it with others)
        recipe: dict
        secret_names: list[str]
        secrets_to_cleanup: set[str]
        recipe, secret_names, secrets_to_cleanup = SubProcessTaskUtil._resolve_recipe(
            validated_args.recipe, execution_ctx=ctx, executor_ctx=self.ctx
        )
        plugin: str = SubProcessTaskUtil._get_plugin_from_recipe(recipe)

        # 2. Write recipe file to local FS (requires write permissions to /tmp directory)
        recipe_file_path = SubProcessTaskUtil._write_recipe_to_file(
            exec_out_dir, recipe
        )

        # Prepare or resolve venv in Python (minimal change)
        venv_config = VenvConfig(
            version=validated_args.version,
            main_plugin=plugin,
            extra_pip_requirements=validated_args.extra_pip_requirements,
            extra_pip_plugins=validated_args.extra_pip_plugins,
            extra_env_vars=validated_args.extra_env_vars,
        )
        venv_setup_logs = LogHolder()
        venv_runner = SubprocessRunner(logs=venv_setup_logs)
        try:
            venv_ref = await setup_venv(
                venv_config=venv_config,
                runner=venv_runner,
                tmp_dir=Path(exec_out_dir),
            )
        except Exception as e:
            error_msg = SubProcessTaskUtil.format_subprocess_error(e)
            raise TaskError(f"Failed to set up virtual environment: {error_msg}") from e

        # 3. Spin off subprocess to run the test-connection script with venv path
        command_script: str = "run_test_connection_with_masking.py"
        report_out_file: str = f"{exec_out_dir}/connection_report.json"
        stdout_lines: deque = deque(maxlen=SubProcessTaskUtil.MAX_LOG_LINES)

        # Prepare environment for subprocess
        subprocess_env = {
            **validated_args.get_combined_env_vars(),
            **venv_ref.extra_envs(),
            "VENV_PATH": str(venv_ref.venv_loc),
        }

        # Enable secret masking in subprocess
        subprocess_env["DATAHUB_ENABLE_SECRET_MASKING"] = "true"

        # Pass the list of secret names to subprocess for targeted registration
        if secret_names:
            subprocess_env["DATAHUB_SECRET_NAMES"] = ",".join(secret_names)

        # Register secrets in parent process for masking subprocess stdout
        # The subprocess will register them too for its own logging
        if secret_names:
            try:
                initialize_secret_masking(force=True)
                registry = SecretRegistry.get_instance()
                for secret_name in secret_names:
                    secret_value = os.environ.get(secret_name)
                    if secret_value:
                        registry.register_secret(secret_name, secret_value)
                logger.info(
                    f"[TEST_CONNECTION] Registered {registry.get_count()} secret(s) in parent process"
                )
            except Exception as e:
                logger.warning(
                    f"[TEST_CONNECTION] Failed to register secrets in parent: {e}"
                )

        ingest_process = subprocess.Popen(
            [
                command_script,
                str(venv_ref.venv_loc),
                recipe_file_path,
                report_out_file,
            ],
            env=subprocess_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        try:
            # Create masking filter for subprocess stdout
            masking_filter = None
            if secret_names:
                try:
                    registry = SecretRegistry.get_instance()
                    if registry and registry.get_count() > 0:
                        masking_filter = SecretMaskingFilter(registry)
                        logger.info(
                            f"[TEST_CONNECTION] Created masking filter with {registry.get_count()} secret(s)"
                        )
                except Exception as e:
                    logger.warning(
                        f"[TEST_CONNECTION] Failed to create masking filter: {e}"
                    )

            while ingest_process.poll() is None:
                assert ingest_process.stdout
                line = ingest_process.stdout.readline()

                # Mask secrets before writing to stdout
                masked_line = masking_filter.mask_text(line) if masking_filter else line
                sys.stdout.write(masked_line)
                stdout_lines.append(masked_line)
                await asyncio.sleep(0)

            return_code = ingest_process.poll()

        except asyncio.CancelledError:
            # Terminate the running child process
            ingest_process.terminate()
            raise

        finally:
            if os.path.exists(report_out_file):
                with open(report_out_file) as structured_report_fp:
                    report_content = structured_report_fp.read()

                    # Mask secrets in structured report before setting it
                    # This catches secrets in error messages from subprocess (e.g., Snowflake errors)
                    try:
                        registry = SecretRegistry.get_instance()
                        if registry and registry.get_count() > 0:
                            # Use DataHub's masking to mask the structured report
                            temp_filter = SecretMaskingFilter(registry)
                            report_content = temp_filter.mask_text(report_content)
                    except Exception:
                        # If masking fails, continue with unmasked report
                        # Better to have the report than to fail completely
                        logger.warning(
                            "Failed to mask structured report, using original"
                        )

                    ctx.get_report().set_structured_report(report_content)

            ctx.get_report().set_logs(
                SubProcessTaskUtil._format_log_lines(stdout_lines)
            )

            # Cleanup by removing the exec out directory
            SubProcessTaskUtil._remove_directory(exec_out_dir)

            # Cleanup secrets from environment to prevent pollution
            # Only remove secrets we added, not ones already in environment
            for secret_name in secrets_to_cleanup:
                os.environ.pop(secret_name, None)

            # Shutdown DataHub masking framework to clean up resources
            try:
                shutdown_secret_masking()
            except Exception as e:
                logger.warning(f"Failed to shutdown secret masking: {e}")

        if return_code != 0:
            # Failed
            ctx.get_report().report_info("Failed to execute 'datahub test connection'")
            raise TaskError("Failed to execute 'datahub test connection'")

        # Report Successful execution
        ctx.get_report().report_info("Successfully executed 'datahub test connection'")

    def close(self) -> None:
        pass
