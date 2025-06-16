# SPDX-FileCopyrightText: (c) 2021 Arteom iG (rtmigo.github.io)
# SPDX-License-Identifier: MIT

from subprocess import CompletedProcess
from typing import Optional


class ChkpkgException(Exception):
    def __init__(self,
                 message: Optional[str] = None,
                 inner: Optional[BaseException] = None):
        super().__init__(message)
        self.inner = inner

    def __str__(self):
        return "\n".join(
            [super().__str__()]
            + [f"inner: {self.inner}"] if self.inner else [])


class CompletedProcessError(ChkpkgException):
    def __init__(self,
                 message: Optional[str] = None,
                 inner: Optional[BaseException] = None,
                 process: Optional[CompletedProcess] = None):
        super().__init__(message=message, inner=inner)
        self.process = process

    def __str__(self):
        return "\n".join([
            super().__str__(),
            f"process: {self.process}"
        ])


class TwineCheckFailed(CompletedProcessError):
    pass


class FailedToInstallPackage(ChkpkgException):
    pass


class CannotInitializeEnvironment(ChkpkgException):
    pass


class CodeExecutionFailed(CompletedProcessError):
    pass


class PytypedNotFound(ChkpkgException):
    pass
