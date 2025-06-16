import os
import re
import time
import math
import shlex
import atexit

from metaflow import util
from metaflow.mflog import (
    BASH_SAVE_LOGS,
    bash_capture_logs,
    export_mflog_env_vars,
    tail_logs,
    get_log_tailer,
)

from .nvct import NVCTClient, NVCTTask, NVCTRequest
from .exceptions import (
    NvctKilledException,
    NvctExecutionException,
    NvctTaskFailedException,
)

# Constants for Metaflow logs
LOGS_DIR = "$PWD/.logs"
STDOUT_FILE = "mflog_stdout"
STDERR_FILE = "mflog_stderr"
STDOUT_PATH = os.path.join(LOGS_DIR, STDOUT_FILE)
STDERR_PATH = os.path.join(LOGS_DIR, STDERR_FILE)
NVCT_WRAPPER = "/usr/local/bin/nvct-wrapper.sh"


class NvctRunner:
    def __init__(
        self,
        metadata,
        datastore,
        environment,
        gpu_type,
        instance_type,
        backend,
        ngc_api_key,
    ):
        self.metadata = metadata
        self.datastore = datastore
        self.environment = environment
        self.gpu_type = gpu_type
        self.instance_type = instance_type
        self.backend = backend
        self._ngc_api_key = ngc_api_key
        self.client = None
        self.task = None
        atexit.register(lambda: self.task.cancel() if hasattr(self, "task") else None)

    def launch_task(
        self,
        step_name,
        step_cli,
        task_spec,
        code_package_sha,
        code_package_url,
        code_package_ds,
        env={},
        max_runtime="PT7H",  # <8H allowed for GFN backend
        max_queued="PT120H",  # 5 days
    ):
        mflog_expr = export_mflog_env_vars(
            datastore_type=code_package_ds,
            stdout_path=STDOUT_PATH,
            stderr_path=STDERR_PATH,
            **task_spec,
        )
        init_cmds = self.environment.get_package_commands(
            code_package_url, code_package_ds
        )
        init_expr = " && ".join(init_cmds)
        step_expr = bash_capture_logs(
            " && ".join(
                self.environment.bootstrap_commands(step_name, code_package_ds)
                + [step_cli]
            )
        )
        cmd_str = "mkdir -p %s && %s && %s && %s; c=$?; %s; exit $c" % (
            LOGS_DIR,
            mflog_expr,
            init_expr,
            step_expr,
            BASH_SAVE_LOGS,
        )

        # Add optional initialization script execution
        cmd_str = (
            '${METAFLOW_INIT_SCRIPT:+eval \\"${METAFLOW_INIT_SCRIPT}\\"} && %s'
            % cmd_str
        )

        cmd_str = shlex.split('bash -c "%s"' % cmd_str)[-1]

        def modify_python_c(match):
            content = match.group(1)
            # Escape double quotes within the python -c command
            content = content.replace('"', r"\"")
            # Replace outermost double quotes with single quotes
            return 'python -c "%s"' % content

        # Convert python -c single quotes to double quotes
        cmd_str = re.sub(r"python -c '(.*?)'", modify_python_c, cmd_str)
        cmd_str = cmd_str.replace("'", '"')
        # Create the final command with outer single quotes to pass to NVCT wrapper
        nvct_cmd = f"{NVCT_WRAPPER} bash -c '{cmd_str}'"

        flow_name = task_spec.get("flow_name")
        run_id = task_spec.get("run_id")
        task_id = task_spec.get("task_id")
        retry_count = task_spec.get("retry_count")
        task_name = f"{flow_name}-{run_id}-{step_name}-{task_id}-{retry_count}"

        if self.backend != "GFN":
            # if maxRuntimeDuration exceeds 8 hours for a Task on the GFN backend,
            # the request will be rejected.
            # (https://docs.nvidia.com/cloud-functions/user-guide/latest/cloud-function/tasks.html#create-task)
            ## thus, if it is non GFN backend, we increase it to 3 days
            max_runtime = "PT72H"

        request = (
            NVCTRequest(task_name)
            .container_image("nvcr.io/zhxkmsaasxhw/nvct-base:2.0-jovyan")
            .container_args(nvct_cmd)
            .gpu(
                gpu=self.gpu_type,
                instance_type=self.instance_type,
                backend=self.backend,
            )
            .max_runtime(max_runtime)
            .max_queued(max_queued)
        )

        for k, v in env.items():
            if v is not None:
                request.env(k, str(v))

        self.client = NVCTClient(self._ngc_api_key)
        self.task = NVCTTask(self.client, request.to_dict())

        self.task.submit()
        return self.task.id

    def wait_for_completion(self, stdout_location, stderr_location, echo=None):
        if not self.task:
            raise NvctExecutionException("No task has been launched")

        def update_delay(secs_since_start):
            # this sigmoid function reaches
            # - 0.1 after 11 minutes
            # - 0.5 after 15 minutes
            # - 1.0 after 23 minutes
            # in other words, the user will see very frequent updates
            # during the first 10 minutes
            sigmoid = 1.0 / (1.0 + math.exp(-0.01 * secs_since_start + 9.0))
            return 0.5 + sigmoid * 30.0

        def wait_for_launch(task):
            status = task.status
            echo(
                "Task is starting (%s)..." % status,
                "stderr",
                _id=task.id,
            )

            t = time.time()
            start_time = time.time()
            while task.is_waiting:
                new_status = task.status
                if status != new_status or (time.time() - t) > 30:
                    status = new_status
                    echo(
                        "Task is starting (%s)..." % status,
                        "stderr",
                        _id=task.id,
                    )
                    t = time.time()
                time.sleep(update_delay(time.time() - start_time))

        _make_prefix = lambda: b"[%s] " % util.to_bytes(self.task.id)
        stdout_tail = get_log_tailer(stdout_location, self.datastore.TYPE)
        stderr_tail = get_log_tailer(stderr_location, self.datastore.TYPE)

        # 1) Loop until the job has started
        wait_for_launch(self.task)

        echo(
            "Task is starting (%s)..." % self.task.status,
            "stderr",
            _id=self.task.id,
        )

        # 2) Tail logs until the job has finished
        tail_logs(
            prefix=_make_prefix(),
            stdout_tail=stdout_tail,
            stderr_tail=stderr_tail,
            echo=echo,
            has_log_updates=lambda: self.task.is_running,
        )

        if self.task.has_failed:
            raise NvctTaskFailedException(
                f"Task failed with status: {self.task.status}. This could be a transient error. Use @retry to retry."
            )
        else:
            if self.task.is_running:
                # Kill the job if it is still running by throwing an exception.
                raise NvctKilledException("Task failed!")
            echo(
                f"Task finished with status: {self.task.status}",
                "stderr",
                _id=self.task.id,
            )
