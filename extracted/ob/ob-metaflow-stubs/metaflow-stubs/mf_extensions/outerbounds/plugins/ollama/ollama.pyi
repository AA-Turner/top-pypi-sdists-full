######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.884036                                                            #
######################################################################################################

from __future__ import annotations

import enum
import typing
if typing.TYPE_CHECKING:
    import enum

from .exceptions import EmptyOllamaManifestCacheException as EmptyOllamaManifestCacheException
from .exceptions import EmptyOllamaBlobCacheException as EmptyOllamaBlobCacheException
from .exceptions import UnspecifiedRemoteStorageRootException as UnspecifiedRemoteStorageRootException

OLLAMA_SUFFIX: str

class ProcessStatus(object, metaclass=type):
    ...

class CircuitBreakerState(enum.Enum, metaclass=enum.EnumType):
    def __new__(cls, value):
        ...
    ...

class CircuitBreaker(object, metaclass=type):
    def __init__(self, failure_threshold, recovery_timeout, reset_timeout, debug = False, status_card = None):
        ...
    def record_success(self):
        ...
    def record_failure(self):
        ...
    def should_attempt_reset(self):
        """
        Check if we should attempt to reset/restart Ollama based on reset_timeout
        """
        ...
    def is_request_allowed(self):
        ...
    def get_status(self):
        ...
    ...

class TimeoutCommand(object, metaclass=type):
    def __init__(self, command, timeout, debug = False, **kwargs):
        ...
    def run(self):
        ...
    ...

class OllamaHealthChecker(object, metaclass=type):
    def __init__(self, ollama_url, circuit_breaker, ollama_manager, debug = False):
        ...
    def start(self):
        ...
    def stop(self):
        ...
    ...

class OllamaRequestInterceptor(object, metaclass=type):
    def __init__(self, circuit_breaker, debug = False):
        ...
    def install_protection(self):
        """
        Install request protection by monkey-patching the ollama package
        """
        ...
    def remove_protection(self):
        """
        Remove request protection by restoring original methods
        """
        ...
    ...

class OllamaManager(object, metaclass=type):
    """
    A process manager for Ollama runtimes.
    Implements interface @ollama([models=...], ...) has a local, remote, or managed backend.
    """
    def __init__(self, models, backend = 'local', flow_datastore_backend = None, remote_storage_root = None, force_pull = False, cache_update_policy = 'auto', force_cache_update = False, debug = False, circuit_breaker_config = None, timeout_config = None, status_card = None):
        ...
    def terminate_models(self, skip_push_check = None):
        """
        Terminate all processes gracefully and update cache.
        """
        ...
    def get_ollama_storage_root(self, backend):
        """
        Return the path to the root of the datastore.
        """
        ...
    ...

