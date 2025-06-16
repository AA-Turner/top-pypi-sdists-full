import json
import os
import time
import threading
from urllib.request import HTTPError, Request, URLError, urlopen
from functools import wraps

from metaflow import util
from metaflow.mflog import (
    BASH_SAVE_LOGS,
    bash_capture_logs,
    export_mflog_env_vars,
    tail_logs,
    get_log_tailer,
)
from .exceptions import NvcfJobFailedException, NvcfPollingConnectionError

# Redirect structured logs to $PWD/.logs/
LOGS_DIR = "$PWD/.logs"
STDOUT_FILE = "mflog_stdout"
STDERR_FILE = "mflog_stderr"
STDOUT_PATH = os.path.join(LOGS_DIR, STDOUT_FILE)
STDERR_PATH = os.path.join(LOGS_DIR, STDERR_FILE)


def retry_on_status(status_codes=[500], max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            retries = 0

            # Determine retry limit upfront
            use_queue_timeout = 504 in status_codes
            if use_queue_timeout:
                poll_seconds = int(instance._poll_seconds)
                retry_limit = (
                    instance._queue_timeout + (poll_seconds - 1)
                ) // poll_seconds
                remainder = instance._queue_timeout % poll_seconds
                last_timeout = remainder if remainder != 0 else poll_seconds
            else:
                retry_limit = max_retries

            while retries < retry_limit:
                try:
                    return func(instance, *args, **kwargs)
                except HTTPError as e:
                    if e.code not in status_codes or retries >= retry_limit:
                        instance._status = JobStatus.FAILED
                        if e.code == 504 and retries >= retry_limit:
                            raise NvcfPollingConnectionError(
                                "Request timed out after all retries"
                            )
                        raise

                    if e.code == 504 and retries == retry_limit - 1:
                        instance._poll_seconds = str(last_timeout)

                    print(
                        f"[@nvidia] {'Queue timeout' if e.code == 504 else f'Received {e.code}'}, "
                        f"retrying ({retries + 1}/{retry_limit})... with poll seconds as {instance._poll_seconds}"
                    )

                    if e.code != 504:
                        time.sleep(delay)

                    retries += 1
                except URLError as e:
                    instance._status = JobStatus.FAILED
                    raise
            # final attempt
            return func(instance, *args, **kwargs)

        return wrapper

    return decorator


class Nvcf(object):
    def __init__(
        self, metadata, datastore, environment, function_id, ngc_api_key, queue_timeout
    ):
        self.metadata = metadata
        self.datastore = datastore
        self.environment = environment
        self._function_id = function_id
        self._ngc_api_key = ngc_api_key
        self._queue_timeout = queue_timeout

    def launch_job(
        self,
        step_name,
        step_cli,
        task_spec,
        code_package_sha,
        code_package_url,
        code_package_ds,
        env={},
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
        heartbeat_expr = f'python -m metaflow_extensions.outerbounds.plugins.nvcf.heartbeat_store "$MAIN_PID" {code_package_ds} nvcf_heartbeats & HEARTBEAT_PID=$!;'
        step_expr = bash_capture_logs(
            " && ".join(
                self.environment.bootstrap_commands(step_name, code_package_ds)
                + [step_cli + " & MAIN_PID=$!; " + heartbeat_expr + " wait $MAIN_PID"]
            )
        )

        # construct an entry point that
        # 1) initializes the mflog environment (mflog_expr)
        # 2) bootstraps a metaflow environment (init_expr)
        # 3) executes a task (step_expr)

        cmd_str = "mkdir -p %s && %s && %s && %s; " % (
            LOGS_DIR,
            mflog_expr,
            init_expr,
            step_expr,
        )
        # after the task has finished, we save its exit code (fail/success)
        # and persist the final logs. The whole entrypoint should exit
        # with the exit code (c) of the task.
        #
        # Note that if step_expr OOMs, this tail expression is never executed.
        # We lose the last logs in this scenario.
        cmd_str += (
            "c=$?; kill $HEARTBEAT_PID; wait $HEARTBEAT_PID; %s; exit $c"
            % BASH_SAVE_LOGS
        )
        cmd_str = (
            '${METAFLOW_INIT_SCRIPT:+eval \\"${METAFLOW_INIT_SCRIPT}\\"} && %s'
            % cmd_str
        )
        self.job = Job(
            'bash -c "%s"' % cmd_str,
            env,
            task_spec,
            self.datastore._storage_impl,
            self._function_id,
            self._ngc_api_key,
            self._queue_timeout,
        )
        self.job.submit()

    def wait(self, stdout_location, stderr_location, echo=None):
        def wait_for_launch(job):
            status = job._status
            echo(
                "Task status: %s..." % status,
                "stderr",
                _id=job.id,
            )

        prefix = b"[%s] " % util.to_bytes(self.job.id)
        stdout_tail = get_log_tailer(stdout_location, self.datastore.TYPE)
        stderr_tail = get_log_tailer(stderr_location, self.datastore.TYPE)

        # 1) Loop until the job has started
        wait_for_launch(self.job)

        # 2) Tail logs until the job has finished
        tail_logs(
            prefix=prefix,
            stdout_tail=stdout_tail,
            stderr_tail=stderr_tail,
            echo=echo,
            has_log_updates=lambda: self.job.is_running,
        )

        echo(
            "Task finished with exit code %s." % self.job.result.get("exit_code"),
            "stderr",
            _id=self.job.id,
        )
        if self.job.has_failed:
            raise NvcfJobFailedException(
                "This could be a transient error. Use @retry to retry."
            )


class JobStatus(object):
    CREATED = "CREATED"  # Job object created but not submitted
    SUBMITTED = "SUBMITTED"  # Job submitted to NVCF
    POLLED = "POLLED"  # Job has been successfully polled at least once
    SUCCESSFUL = "SUCCESSFUL"  # Job completed successfully
    FAILED = "FAILED"  # Job failed
    DISAPPEARED = "DISAPPEARED"  # Job disappeared from NVCF but was previously polled (likely successful)


terminal_states = [JobStatus.SUCCESSFUL, JobStatus.FAILED, JobStatus.DISAPPEARED]

nvcf_url = "https://api.nvcf.nvidia.com"
submit_endpoint = f"{nvcf_url}/v2/nvcf/pexec/functions"
result_endpoint = f"{nvcf_url}/v2/nvcf/pexec/status"


class Job(object):
    def __init__(
        self, command, env, task_spec, backend, function_id, ngc_api_key, queue_timeout
    ):
        self._payload = {
            "command": command,
            "env": {k: v for k, v in env.items() if v is not None},
        }
        self._result = {}
        self._function_id = function_id
        self._ngc_api_key = ngc_api_key
        self._queue_timeout = queue_timeout
        self._poll_seconds = "3600"

        # Initialize status and tracking variables
        self._status = JobStatus.CREATED
        self._last_poll_time = time.time()

        # State tracking for long polling
        self._long_polling_active = False
        self._poll_response = None

        flow_name = task_spec.get("flow_name")
        run_id = task_spec.get("run_id")
        step_name = task_spec.get("step_name")
        task_id = task_spec.get("task_id")
        retry_count = task_spec.get("retry_count")

        heartbeat_prefix = "/".join(
            (flow_name, str(run_id), step_name, str(task_id), str(retry_count))
        )

        ## import is done here to avoid the following warning:
        # RuntimeWarning: 'metaflow_extensions.outerbounds.plugins.nvcf.heartbeat_store' found in sys.modules
        # after import of package 'metaflow_extensions.outerbounds.plugins.nvcf', but prior to execution of
        # 'metaflow_extensions.outerbounds.plugins.nvcf.heartbeat_store'; this may result in unpredictable behaviour
        from metaflow_extensions.outerbounds.plugins.nvcf.heartbeat_store import (
            HeartbeatStore,
        )

        store = HeartbeatStore(
            main_pid=None,
            storage_backend=backend,
        )

        self.heartbeat_thread = threading.Thread(
            target=store.emit_heartbeat,
            args=(
                heartbeat_prefix,
                "nvcf_heartbeats",
            ),
            daemon=True,
        )
        self.heartbeat_thread.start()

    @retry_on_status(status_codes=[504])
    def submit(self):
        try:
            headers = {
                "Authorization": f"Bearer {self._ngc_api_key}",
                "Content-Type": "application/json",
                "nvcf-feature-enable-gateway-timeout": "true",
                "NVCF-POLL-SECONDS": self._poll_seconds,
            }
            request_data = json.dumps(self._payload).encode()
            request = Request(
                f"{submit_endpoint}/{self._function_id}",
                data=request_data,
                headers=headers,
            )
            response = urlopen(request)
            self._invocation_id = response.headers.get("NVCF-REQID")
            if response.getcode() == 200:
                data = json.loads(response.read())
                if data.get("exit_code") == 0:
                    self._status = JobStatus.SUCCESSFUL
                else:
                    self._status = JobStatus.FAILED
                self._result = data
            elif response.getcode() == 202:
                self._status = JobStatus.SUBMITTED
                # Start long polling immediately after receiving 202
                self._start_long_polling()
            else:
                self._status = JobStatus.FAILED
        except URLError:
            self._status = JobStatus.FAILED
            raise

    def _start_long_polling(self):
        if not self._long_polling_active:
            self._long_polling_active = True
            polling_thread = threading.Thread(target=self._long_poll_loop, daemon=True)
            polling_thread.start()

    def _long_poll_loop(self):
        while self._long_polling_active and self._status not in terminal_states:
            try:
                self._poll()
                # No sleep needed - the request itself will block for up to self._poll_seconds
            except Exception as e:
                print(f"[@nvidia] Long polling error: {e}")
                # Brief pause before retry on error
                time.sleep(1)

        self._long_polling_active = False

    @property
    def id(self):
        return self._invocation_id

    @property
    def is_running(self):
        # Job is running if it's in SUBMITTED or POLLED state
        return self._status in [JobStatus.SUBMITTED, JobStatus.POLLED]

    @property
    def has_failed(self):
        return self._status == JobStatus.FAILED

    @property
    def result(self):
        return self._result

    @retry_on_status(status_codes=[500], max_retries=3, delay=5)
    @retry_on_status(status_codes=[504])
    def _poll(self):
        try:
            # Implement rate limiting to prevent more than 1 request per second
            current_time = time.time()
            if (
                hasattr(self, "_last_poll_time")
                and current_time - self._last_poll_time < 1
            ):
                time.sleep(1 - (current_time - self._last_poll_time))

            headers = {
                "Authorization": f"Bearer {self._ngc_api_key}",
                "Content-Type": "application/json",
                "nvcf-feature-enable-gateway-timeout": "true",
                "NVCF-POLL-SECONDS": self._poll_seconds,
            }
            request = Request(
                f"{result_endpoint}/{self._invocation_id}", headers=headers
            )

            # Record time before making the request
            self._last_poll_time = time.time()

            response = urlopen(request)
            body = response.read()
            print(f"[@nvidia] polling status code: {response.getcode()}")

            if response.getcode() == 200:
                data = json.loads(body)
                if data.get("exit_code") == 0:
                    self._status = JobStatus.SUCCESSFUL
                else:
                    self._status = JobStatus.FAILED
                self._result = data
                self._long_polling_active = False  # Stop polling once job completes
            elif response.getcode() == 202:
                # Job is still running - status remains SUBMITTED or POLLED
                if self._status == JobStatus.SUBMITTED:
                    self._status = JobStatus.POLLED
            elif response.getcode() == 302:
                # Handle redirects for large responses or requests in different regions
                redirect_location = response.headers.get("Location")
                if redirect_location:
                    redirect_request = Request(redirect_location, headers=headers)
                    redirect_response = urlopen(redirect_request)
                    if redirect_response.getcode() == 200:
                        data = json.loads(redirect_response.read())
                        if data.get("exit_code") == 0:
                            self._status = JobStatus.SUCCESSFUL
                        else:
                            self._status = JobStatus.FAILED
                        self._result = data
                        self._long_polling_active = False
            else:
                print(
                    f"[@nvidia] Unexpected response code: {response.getcode()}. Please notify an Outerbounds support engineer if this error persists."
                )
                self._status = JobStatus.FAILED

        except HTTPError as e:
            if e.code == 404:
                # 404 interpretation depends on job lifecycle
                if self._status in [JobStatus.POLLED, JobStatus.SUBMITTED]:
                    # We've submitted or successfully polled this job before,
                    # so a 404 likely means it completed and was removed
                    self._status = JobStatus.DISAPPEARED
                    self._result = {"exit_code": 0}
                    print(
                        f"[@nvidia] 404 received for job that was previously tracked - assuming job completed"
                    )
                else:
                    # Job was never successfully tracked
                    print(
                        f"[@nvidia] 404 received for job that was never successfully tracked - treating as failure"
                    )
                    self._status = JobStatus.FAILED
                    raise NvcfPollingConnectionError(e)
            elif e.code in [500, 504]:
                # Don't set status to FAILED, just re-raise for retry decorator
                raise
            else:
                self._status = JobStatus.FAILED
                raise NvcfPollingConnectionError(e)
        except URLError as e:
            self._status = JobStatus.FAILED
            raise NvcfPollingConnectionError(e)
