"""
Anonymous CLI usage telemetry for Fivetran CLIs.

Best-effort and fire-and-forget: a command's exit code or output is never
affected by anything in this module, and sending an event never blocks the
command on network I/O. The HTTP call runs in a detached child process (see
Telemetry._spawn_detached_sender()), not in this process or a thread — a thread would die
with this short-lived CLI process before the request completes, while a
detached subprocess survives it.
"""

import json
import os
import platform
import subprocess
import sys
import time
import uuid
from contextlib import contextmanager
from importlib import resources

# Standard cross-tool opt-out signal (https://consoledonottrack.com).
DO_NOT_TRACK_ENV_VAR = "DO_NOT_TRACK"
# Preference and anonymous actor id are stored in the tool's JSON config file.
CONFIG_ENABLED_KEY = "is_telemetry_enabled"
CONFIG_ACTOR_ID_KEY = "actor_id"
UTF_8 = "utf-8"


def _load_sender_script():
    """Source of the detached sender (_sender.py), passed to the child as `python -I -c <source>`.

    It's delivered inline rather than run with `python -m fivetran_cli_telemetry._sender` because
    `-I` implies `-s` and `-P`, which strip the user site-packages and the cwd from sys.path — so
    `-m` would fail to import the package under `pip install --user` or a source checkout and
    silently drop telemetry. Passing the source inline needs no import at all. Returns "" (a no-op
    script) if the source can't be read, so a read failure can never break telemetry.
    """
    try:
        return resources.files(__package__).joinpath("_sender.py").read_text(encoding=UTF_8)
    except Exception:
        return ""


# Read once at import; see _load_sender_script for why the source is sent inline.
_SENDER_SCRIPT = _load_sender_script()


class ConfigUnreadableError(Exception):
    """The config file exists but can't be read or isn't a JSON object, so it must be left untouched."""


class Telemetry:
    """Anonymous usage telemetry for one CLI tool.

    tool_name:   reported as `cli_tool` in every event.
    webhook_url: where events are POSTed; nothing is sent when empty.
    config_path: JSON file holding the opt-out preference and the anonymous actor id.
    log_fn:      called with the one-time telemetry notice text.
    """

    def __init__(self, tool_name, webhook_url, config_path, log_fn):
        self._tool_name = tool_name
        self._webhook_url = webhook_url
        self._config_path = config_path
        self._log_fn = log_fn
        self._notice_shown = False
        # HTTP status code of the most recent failing Fivetran API call in this process, recorded
        # via record_api_error() so track_cli_usage() can report it (e.g. 401) in place of the
        # generic exit code. A single CLI process runs exactly one command, so one value is
        # sufficient; track_cli_usage() resets it at the start of each command.
        self._api_error_status_code = None

    def record_api_error(self, status_code):
        """Record the HTTP status code of a failing Fivetran API call, so the running CLI
        command's telemetry reports that code instead of the generic exit code. Best-effort."""
        if isinstance(status_code, int):
            self._api_error_status_code = status_code

    def _reset_api_error(self):
        self._api_error_status_code = None

    @contextmanager
    def track_cli_usage(self, command, option_names, cli_version, track_duration=False):
        """Run a CLI command block and report its outcome via send_cli_usage.

        Replaces the exit-code bookkeeping that would otherwise be duplicated around each
        CLI command's body. When the command failed because of a Fivetran API call (recorded
        via record_api_error), the API's HTTP status code is reported as the exit code.
        """
        self._reset_api_error()
        exit_code = 0
        start_time = time.perf_counter() if track_duration else None
        try:
            yield
        except SystemExit as e:
            # SystemExit.code may be a message (sys.exit("msg")); report 1 as Python does, never the text.
            if e.code is None:
                exit_code = 0
            elif isinstance(e.code, int):
                exit_code = e.code
            else:
                exit_code = 1
            raise
        except KeyboardInterrupt:
            # 128 + SIGINT, the conventional shell exit code for Ctrl+C.
            exit_code = 130
            raise
        except BaseException:
            exit_code = 1
            raise
        finally:
            duration = (time.perf_counter() - start_time) if start_time is not None else 0
            # Prefer the API's HTTP status code when the command failed because of an API call.
            if self._api_error_status_code is not None and exit_code != 0:
                exit_code = self._api_error_status_code
            self.send_cli_usage(command, option_names, exit_code, cli_version, duration=duration)

    def send_cli_usage(self, command, option_names, exit_code, cli_version, duration=0, extra_fields=None):
        """Send CLI usage telemetry via a detached child process. Never raises — telemetry is best-effort.

        extra_fields: optional tool-specific fields added to the event (e.g. {"output_format": "json"}).

        A background thread would be killed as soon as this (short-lived) CLI process exits, so
        delivery would race the parent's shutdown. A detached subprocess keeps running
        independently of the parent and is unaffected by it exiting.
        """
        try:
            if not self.is_telemetry_enabled():
                return

            if not self._webhook_url:
                return

            payload = self._build_payload(command, option_names, exit_code, cli_version, duration, extra_fields)
            self._spawn_detached_sender(self._webhook_url, payload)
        except Exception:
            # Fire-and-forget: telemetry is best-effort and must never impact user workflows.
            pass

    def send_minimal_cli_usage(self, event_fields, cli_version, tool_name=None):
        """Send a one-off event: the shared identity fields (actor id, version, Python, OS,
        architecture) plus event_fields. Never raises — telemetry is best-effort.

        tool_name overrides the `cli_tool` this instance reports, for an event sent on behalf of
        another tool (e.g. a CLI recording that it handed a command over to a plugin).
        """
        try:
            if not self.is_telemetry_enabled():
                return

            if not self._webhook_url:
                return

            payload = {**self._identity_fields(cli_version, tool_name), **event_fields}
            self._spawn_detached_sender(self._webhook_url, payload)
        except Exception:
            # Fire-and-forget: telemetry is best-effort and must never impact user workflows.
            pass

    @staticmethod
    def _spawn_detached_sender(webhook_url, payload):
        payload_json = json.dumps(payload)
        popen_kwargs = {
            "stdin": subprocess.PIPE,
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "close_fds": True,
        }
        if os.name == "posix":
            popen_kwargs["start_new_session"] = True
        elif os.name == "nt":
            popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS

        # -I runs the child in isolated mode so a stray email.py/http.py/urllib.py in the
        # user's project directory can't shadow the stdlib modules the sender imports (python -c
        # otherwise prepends the current working directory to sys.path).
        # webhook_url/payload are sent over stdin rather than as command-line arguments so
        # that no user-controlled data ever becomes a subprocess argument.
        process = subprocess.Popen(
            [sys.executable, "-I", "-c", _SENDER_SCRIPT],
            **popen_kwargs,
        )
        process.stdin.write(f"{webhook_url}\n{payload_json}".encode("utf-8"))
        process.stdin.close()

    def is_telemetry_enabled(self):
        """Whether telemetry should be sent.

        Precedence: the DO_NOT_TRACK environment variable takes precedence over the
        `is_telemetry_enabled` preference saved in the local config file. When neither
        specifies a preference, telemetry defaults to enabled: the default is persisted to
        the config file (so the notice is shown only once) and a one-time notice tells the
        user how to opt out. Nothing is sent on that first run (this returns False); events
        start from the next run. This is the only time the CLI writes the telemetry
        preference automatically.
        """
        if self._notice_shown:
            return False

        do_not_track = self._do_not_track()
        if do_not_track is not None:
            return not do_not_track

        try:
            config = self._load_config()
        except ConfigUnreadableError:
            # Never overwrite a config we couldn't read (it may hold an opt-out): stay silent and off.
            return False
        preference = self._config_preference(config)
        if preference is not None:
            return preference

        config[CONFIG_ENABLED_KEY] = True
        self._ensure_actor_id_in_config(config)
        try:
            self._save_config(config)
        except OSError:
            # Determining the preference must still work even when the default can't be persisted.
            pass
        self._log_fn(
            "----------------\n"
            "Telemetry Notice\n"
            "----------------\n"
            f"{self._tool_name} collects anonymous usage statistics to help improve the CLI.\n"
            "No personal data, connector logic, credentials, or argument values are collected.\n"
            "\n"
            "To opt out:\n"
            f"  Set env var:  {DO_NOT_TRACK_ENV_VAR}=1\n"
            f"  Or set {CONFIG_ENABLED_KEY} to false in {self._config_path}\n"
            "\n"
            "Learn more: https://fivetran.com/docs/security-and-privacy/telemetry"
        )
        self._notice_shown = True
        # Send nothing on the run that shows the notice, so users can opt out before any event leaves.
        return False

    @staticmethod
    def _do_not_track():
        """Interpret the DO_NOT_TRACK environment variable.

        Returns True to opt out, False to opt in, or None when the variable is unset.
        Only the literal values "1"/"true" (case-insensitive) opt out.
        """
        value = os.getenv(DO_NOT_TRACK_ENV_VAR)
        if value is None:
            return None
        return value.strip().lower() in ("1", "true")

    @staticmethod
    def _config_preference(config):
        """The is_telemetry_enabled preference saved in the config, or None when the key is unset.

        Only an explicit false (JSON false, or the string "false" case-insensitively) disables
        telemetry. Any other value that is set counts as enabled, the same way anything other
        than DO_NOT_TRACK=1/true opts in. A set value is never overwritten by the default.
        """
        value = config.get(CONFIG_ENABLED_KEY)
        if value is None:
            return None
        if value is False or (isinstance(value, str) and value.strip().lower() == "false"):
            return False
        return True

    def _identity_fields(self, cli_version, tool_name=None):
        """Fields describing who and what is running, shared by every event."""
        return {
            "cli_tool": tool_name or self._tool_name,
            "actor_id": self._get_or_create_actor_id(),
            "cli_version": cli_version,
            "python_version": platform.python_version(),
            "os": platform.system().lower(),
            "architecture": platform.machine().lower(),
        }

    def _build_payload(self, command, option_names, exit_code, cli_version, duration=0, extra_fields=None):
        return {
            **self._identity_fields(cli_version),
            "command": command,
            "options": sorted(option_names),
            "status": "success" if exit_code == 0 else "failure",
            "exit_code": exit_code,
            "duration": round(duration, 3),
            **(extra_fields or {}),
        }

    @staticmethod
    def _ensure_actor_id_in_config(config):
        """Ensure a valid actor id exists in config, creating one if necessary. Modifies config in-place."""
        actor_id = config.get(CONFIG_ACTOR_ID_KEY)
        if isinstance(actor_id, str) and actor_id:
            return actor_id

        config[CONFIG_ACTOR_ID_KEY] = str(uuid.uuid4())
        return config[CONFIG_ACTOR_ID_KEY]

    def _get_or_create_actor_id(self):
        """Get or create the anonymous actor id from the config file, persisting it if created.

        Raises ConfigUnreadableError (leaving the file untouched) when an existing config can't be read.
        """
        config = self._load_config()
        actor_id = config.get(CONFIG_ACTOR_ID_KEY)
        if isinstance(actor_id, str) and actor_id:
            return actor_id

        # Only write when the actor id had to be created.
        actor_id = self._ensure_actor_id_in_config(config)
        self._save_config(config)
        return actor_id

    def _load_config(self):
        """The saved config, or {} when the file doesn't exist yet.

        Raises ConfigUnreadableError when the file exists but can't be read or parsed as a JSON
        object, so callers don't replace it with defaults.
        """
        try:
            with open(self._config_path, "r", encoding=UTF_8) as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}
        except (ValueError, OSError) as e:
            # ValueError covers JSONDecodeError and UnicodeDecodeError.
            raise ConfigUnreadableError(self._config_path) from e
        if not isinstance(data, dict):
            raise ConfigUnreadableError(self._config_path)
        return data

    def _save_config(self, config):
        os.makedirs(os.path.dirname(self._config_path), exist_ok=True)

        temp_path = f"{self._config_path}.{os.getpid()}.{uuid.uuid4()}.tmp"
        try:
            with open(temp_path, "w", encoding=UTF_8) as f:
                json.dump(config, f, sort_keys=True)
            os.replace(temp_path, self._config_path)
        except Exception:
            try:
                os.remove(temp_path)
            except OSError:
                pass
            raise
