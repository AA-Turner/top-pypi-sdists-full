"""
No-op validator that does not validate the runtime_path for a specified language.
"""

import logging

from aws_lambda_builders.architecture import ARM64, X86_64
from aws_lambda_builders.exceptions import UnsupportedArchitectureError, UnsupportedRuntimeError

LOG = logging.getLogger(__name__)

SUPPORTED_RUNTIMES = {
    "nodejs16.x": [ARM64, X86_64],
    "nodejs18.x": [ARM64, X86_64],
    "nodejs20.x": [ARM64, X86_64],
    "nodejs22.x": [ARM64, X86_64],
    "python3.8": [ARM64, X86_64],
    "python3.9": [ARM64, X86_64],
    "python3.10": [ARM64, X86_64],
    "python3.11": [ARM64, X86_64],
    "python3.12": [ARM64, X86_64],
    "python3.13": [ARM64, X86_64],
    "ruby3.2": [ARM64, X86_64],
    "ruby3.3": [ARM64, X86_64],
    "ruby3.4": [ARM64, X86_64],
    "java8": [ARM64, X86_64],
    "java11": [ARM64, X86_64],
    "java17": [ARM64, X86_64],
    "java21": [ARM64, X86_64],
    "go1.x": [ARM64, X86_64],
    "dotnet6": [ARM64, X86_64],
    "dotnet8": [ARM64, X86_64],
    "provided": [ARM64, X86_64],
}


class RuntimeValidator(object):
    def __init__(self, runtime, architecture):
        """

        Parameters
        ----------
        runtime : str
            name of the AWS Lambda runtime that you are building for. This is sent to the builder for
            informational purposes.
        architecture : str
            Architecture for which the build will be based on in AWS lambda
        """
        self.runtime = runtime
        self._runtime_path = None
        self.architecture = architecture

    def validate(self, runtime_path):
        """
        Parameters
        ----------
        runtime_path : str
            runtime to check eg: /usr/bin/runtime

        Returns
        -------
        str
            runtime to check eg: /usr/bin/runtime

        Raises
        ------
        UnsupportedRuntimeError
            Raised when runtime provided is not support.

        UnsupportedArchitectureError
            Raised when runtime is not compatible with architecture
        """
        runtime_architectures = SUPPORTED_RUNTIMES.get(self.runtime, None)

        if not runtime_architectures:
            raise UnsupportedRuntimeError(runtime=self.runtime)
        if self.architecture not in runtime_architectures:
            raise UnsupportedArchitectureError(runtime=self.runtime, architecture=self.architecture)

        self._runtime_path = runtime_path
        return runtime_path
