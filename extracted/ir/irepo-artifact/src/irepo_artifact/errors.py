"""Errors deliberately contain no signed URLs or server response bodies."""

from copy import deepcopy


class ArtifactError(Exception):
    """Base error; raw responses are available explicitly, never in str/repr."""

    def __init__(self, *args, artifacts_response=None, manifest_response=None):
        super().__init__(*args)
        self.artifacts_response = artifacts_response
        self.manifest_response = manifest_response

    def clone(self):
        """Copy error data without invoking subclass-specific constructors.

        Subclasses with state outside __dict__ should override this method.
        Traceback/context are intentionally not shared between Job results.
        """
        cloned = BaseException.__new__(type(self))
        memo = {id(self): cloned}
        BaseException.__init__(cloned, *deepcopy(self.args, memo))
        cloned.__dict__.update(deepcopy(self.__dict__, memo))
        return cloned


class AccessDenied(ArtifactError):
    """AP rejected access."""


class ArtifactNotFound(ArtifactError):
    """Job or artifact is missing."""


class NoMatchingFiles(ArtifactError):
    """Manifest contains no matching files."""


class ProtocolError(ArtifactError):
    """AP response does not satisfy the artifact protocol."""


class ConfigurationError(ArtifactError):
    """Invalid client configuration or request options."""


class DownloadError(ArtifactError):
    """Artifact transfer failed."""


class HTTPStatusError(DownloadError):
    def __init__(self, status: int):
        self.status = status
        super().__init__(f"artifact download returned HTTP {status}")


class NetworkError(DownloadError):
    """Remote connectivity or interrupted transfer; eligible for fallback."""
