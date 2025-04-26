import sys
from importlib.metadata import version
from typing import Dict, Union

from opentelemetry.sdk.resources import Resource, ResourceDetector
from opentelemetry.semconv.resource import ResourceAttributes
from psutil import Process

Attributes = Dict[str, Union[str, bool, int, float]]


__version__ = version("opentelemetry_resourcedetector_process")


class ProcessResourceDetector(ResourceDetector):
    """Detects OpenTelemetry Resource attributes for an operating system process,
    providing the `process.*` attributes"""

    def detect(self) -> Resource:
        python_version = sys.implementation.version
        python_version_string = ".".join(
            map(
                str,
                python_version[:3]
                if python_version.releaselevel == "final" and not python_version.serial
                else python_version,
            )
        )

        process = Process()
        with process.oneshot():
            command_line = process.cmdline()
            command, *arguments = command_line
            attributes: Attributes = {
                # https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/resource/semantic_conventions/process.md#python-runtimes
                ResourceAttributes.PROCESS_RUNTIME_NAME: sys.implementation.name,
                ResourceAttributes.PROCESS_RUNTIME_VERSION: python_version_string,
                ResourceAttributes.PROCESS_RUNTIME_DESCRIPTION: sys.version,
                # https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/resource/semantic_conventions/process.md#process
                ResourceAttributes.PROCESS_PID: process.pid,
                ResourceAttributes.PROCESS_EXECUTABLE_NAME: process.name(),
                ResourceAttributes.PROCESS_EXECUTABLE_PATH: process.exe(),
                ResourceAttributes.PROCESS_COMMAND_LINE: ' '.join(command_line),
                ResourceAttributes.PROCESS_COMMAND: command,
                ResourceAttributes.PROCESS_COMMAND_ARGS: ' '.join(arguments),
                ResourceAttributes.PROCESS_OWNER: process.username(),
            }

        return Resource.create(attributes)
