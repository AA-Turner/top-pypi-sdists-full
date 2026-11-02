import json
from collections.abc import Mapping, Sequence
from tempfile import TemporaryFile
from typing import IO, Literal

type ConfigurationValue = (
    bool
    | int
    | float
    | str
    | None
    | Sequence[ConfigurationValue]
    | Mapping[str, ConfigurationValue]
)
type Variables = Mapping[str, ConfigurationValue]
type BackendConfig = str | Mapping[str, ConfigurationValue]
type Environment = Mapping[str, str]
type StreamName = Literal["stdout"] | Literal["stderr"]
type StreamNames = set[StreamName]


class Result:
    def __init__(
        self, stdout: IO[str] | None = None, stderr: IO[str] | None = None
    ):
        self.stdout = stdout
        self.stderr = stderr


class Executor:
    def execute(
        self,
        command: Sequence[str],
        environment: Environment | None = None,
        stdout: IO[str] | None = None,
        stderr: IO[str] | None = None,
    ) -> None:
        raise NotImplementedError


def _captures(capture: StreamNames | None, stream: StreamName) -> bool:
    return capture is not None and stream in capture


def _capture_stream(
    capture: StreamNames | None, stream: StreamName
) -> IO[str] | None:
    if _captures(capture, stream):
        return TemporaryFile(mode="w+t")
    return None


class Terraform:
    def __init__(self, executor: Executor):
        self._executor = executor

    def init(
        self,
        chdir: str | None = None,
        backend_config: BackendConfig | None = None,
        reconfigure: bool = False,
        environment: Environment | None = None,
    ):
        base_command = self._build_base_command(chdir)
        command = (
            base_command
            + ["init"]
            + self._build_backend_config(backend_config)
        )

        if reconfigure:
            command = command + ["-reconfigure"]

        self._executor.execute(command, environment=environment)

    def validate(
        self,
        chdir: str | None = None,
        json: bool = False,
        environment: Environment | None = None,
    ):
        base_command = self._build_base_command(chdir)
        command = base_command + ["validate"]

        if json:
            command = command + ["-json"]

        self._executor.execute(command, environment=environment)

    def plan(
        self,
        chdir: str | None = None,
        vars: Variables | None = None,
        environment: Environment | None = None,
    ):
        base_command = self._build_base_command(chdir)
        command = base_command + ["plan"] + self._build_vars(vars)

        self._executor.execute(command, environment=environment)

    def apply(
        self,
        chdir: str | None = None,
        vars: Variables | None = None,
        autoapprove: bool = False,
        environment: Environment | None = None,
    ):
        base_command = self._build_base_command(chdir)
        autoapprove_flag = ["-auto-approve"] if autoapprove else []
        command = (
            base_command
            + ["apply"]
            + autoapprove_flag
            + self._build_vars(vars)
        )

        self._executor.execute(command, environment=environment)

    def destroy(
        self,
        chdir: str | None = None,
        vars: Variables | None = None,
        autoapprove: bool = False,
        environment: Environment | None = None,
    ):
        base_command = self._build_base_command(chdir)
        autoapprove_flag = ["-auto-approve"] if autoapprove else []
        command = (
            base_command
            + ["destroy"]
            + autoapprove_flag
            + self._build_vars(vars)
        )

        self._executor.execute(command, environment=environment)

    def select_workspace(
        self,
        workspace: str,
        chdir: str | None = None,
        or_create: bool = False,
        environment: Environment | None = None,
    ):
        base_command = self._build_base_command(chdir)
        command = base_command + ["workspace", "select"]

        if or_create:
            command = command + ["-or-create=true"]

        command = command + [workspace]

        self._executor.execute(command, environment=environment)

    def output(
        self,
        chdir: str | None = None,
        name: str | None = None,
        raw: bool = False,
        json: bool = False,
        environment: Environment | None = None,
        capture: StreamNames | None = None,
    ) -> Result:
        base_command = self._build_base_command(chdir)
        command = base_command + ["output"]

        if raw:
            command = command + ["-raw"]
        if json:
            command = command + ["-json"]
        if name is not None:
            command = command + [name]

        stdout = _capture_stream(capture, "stdout")
        stderr = _capture_stream(capture, "stderr")

        self._executor.execute(
            command,
            environment=environment,
            stdout=stdout,
            stderr=stderr,
        )

        if stdout is not None:
            stdout.seek(0)
        if stderr is not None:
            stderr.seek(0)

        return Result(stdout, stderr)

    @staticmethod
    def _build_base_command(chdir: str | None) -> list[str]:
        command = ["terraform"]

        if chdir is not None:
            return command + [f"-chdir={chdir}"]

        return command

    def _build_vars(self, variables: Variables | None) -> list[str]:
        if variables is None:
            return []

        return [
            self._format_configuration_value("-var", key, value)
            for key, value in variables.items()
        ]

    @staticmethod
    def _format_configuration_value(
        option_key: str, key: str, value: ConfigurationValue
    ) -> str:
        if isinstance(value, bool):
            return f'{option_key}="{key}={str(value).lower()}"'
        elif isinstance(value, str):
            return f'{option_key}="{key}={value}"'
        elif value is None:
            return f'{option_key}="{key}=null"'
        else:
            jsonified_value = (
                json.dumps(value).replace("\\", "\\\\").replace('"', r"\"")
            )
            return f'{option_key}="{key}={jsonified_value}"'

    def _build_backend_config(
        self, backend_config: BackendConfig | None
    ) -> list[str]:
        if backend_config is None:
            return []

        if isinstance(backend_config, str):
            return [f"-backend-config={backend_config}"]
        else:
            return [
                self._format_configuration_value("-backend-config", key, value)
                for key, value in backend_config.items()
            ]
