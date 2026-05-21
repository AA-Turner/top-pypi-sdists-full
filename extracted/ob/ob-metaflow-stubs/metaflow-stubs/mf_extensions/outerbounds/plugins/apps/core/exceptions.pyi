######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.29.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-05-21T04:04:58.856124                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.exceptions

from ._state_machine import LogLine as LogLine

class OuterboundsBackendUnhealthyException(Exception, metaclass=type):
    """
    Raised when the Outerbounds platform returns 5xx errors or is unreachable.
    
    Catch this to handle temporary platform outages gracefully. The request
    can typically be retried after a short delay.
    """
    def __init__(self, url: str, method: str, status_code: typing.Union[int, None] = None, text: typing.Union[str, None] = None, message: typing.Union[str, None] = None):
        ...
    ...

class OuterboundsForbiddenException(Exception, metaclass=type):
    """
    This exception is raised when access to an Outerbounds API is forbidden (HTTP 403).
    """
    def __init__(self, url: str, method: str, text: str):
        ...
    ...

class OuterboundsConfigurationException(Exception, metaclass=type):
    """
    This exception is raised when Outerbounds configuration is missing or invalid.
    """
    def __init__(self, missing_config: str):
        ...
    ...

class CapsuleApiException(Exception, metaclass=type):
    def __init__(self, url: str, method: str, status_code: int, text: str, message: typing.Union[str, None] = None):
        ...
    def __str__(self):
        ...
    ...

class CapsuleDeploymentException(Exception, metaclass=type):
    """
    Base exception for all capsule deployment failures.
    """
    def __init__(self, capsule_id: str, message: str):
        ...
    def __str__(self):
        ...
    ...

class CapsuleCrashLoopException(CapsuleDeploymentException, metaclass=type):
    """
    Raised when a worker enters CrashLoopBackOff or Failed state.
    """
    def __init__(self, capsule_id: str, worker_id: str, logs: typing.Union[typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.LogLine], None] = None):
        ...
    def __str__(self):
        ...
    ...

class CapsuleReadinessException(CapsuleDeploymentException, metaclass=type):
    """
    Raised when capsule fails to meet readiness conditions within timeout.
    
    Carries raw diagnostic data so higher-level callers can decide how to
    present the failure reason.
    """
    def __init__(self, capsule_id: str, capsule_status: typing.Union[typing.Dict, None] = None, worker_semantic_status: typing.Union[typing.Dict, None] = None, readiness_condition: typing.Union[str, None] = None, min_replicas: typing.Union[int, None] = None, max_wait_time: typing.Union[int, None] = None, timed_out: bool = False):
        ...
    def __str__(self):
        ...
    ...

class CapsuleConcurrentUpgradeException(CapsuleDeploymentException, metaclass=type):
    """
    Raised when a concurrent upgrade invalidates the current deployment.
    """
    def __init__(self, capsule_id: str, expected_version: str, actual_version: str, modified_by: typing.Union[str, None] = None, modified_at: typing.Union[str, None] = None):
        ...
    def __str__(self):
        ...
    ...

class CapsuleDeletedDuringDeploymentException(CapsuleDeploymentException, metaclass=type):
    """
    Raised when a capsule is deleted while deployment is in progress.
    """
    def __init__(self, capsule_id: str):
        ...
    ...

class CodePackagingException(Exception, metaclass=type):
    """
    Exception raised when code packaging fails.
    """
    ...

class AppNotFoundException(Exception, metaclass=type):
    """
    Raised when attempting to access an app that does not exist.
    
    This can occur when calling methods on `DeployedApp` for an app that
    has been deleted or never existed.
    """
    ...

class AppCreationFailedException(Exception, metaclass=type):
    """
    Raised when the platform rejects an app deployment request.
    
    Common causes include invalid configuration, quota limits, or permission issues.
    Check `status_code` and `error_text` for details on why the request was rejected.
    """
    def __init__(self, app_name: str, status_code: int, error_text: str):
        ...
    def __str__(self):
        ...
    ...

class AppDeploymentException(Exception, metaclass=type):
    """
    Base exception for app deployment failures that occur after submission.
    
    All deployment exceptions provide a `deployed_app` property that returns
    a `DeployedApp` object, allowing you to inspect logs or app state even
    after a failure.
    """
    def __init__(self, app_id: str, message: str):
        ...
    def __str__(self):
        ...
    @property
    def deployed_app(self):
        """
        Returns a `DeployedApp` object for the failed deployment.
        Use this to inspect logs, replica status, or other details after catching
        the exception. For example: `e.deployed_app.logs()` to fetch recent logs.
        """
        ...
    ...

class AppCrashLoopException(AppDeploymentException, metaclass=type):
    """
    Raised when an app worker crashes repeatedly during startup.
    
    The `logs` attribute contains recent log lines from the failing worker,
    which typically reveal the cause (e.g., import errors, missing dependencies,
    or application exceptions). The `worker_id` identifies which replica failed.
    """
    def __init__(self, app_id: str, worker_id: str, logs: typing.Union[typing.List, None] = None):
        ...
    def __str__(self):
        ...
    ...

class AppReadinessException(AppDeploymentException, metaclass=type):
    """
    Raised when the app fails to become ready to serve traffic.
    
    This can happen for two reasons:
    
    1. **Timeout**: The deployment did not satisfy its ``readiness_condition``
       within ``max_wait_time`` seconds.  Workers may still be starting up,
       pulling images, or stuck in a pending state.
    2. **Traffic routing failure**: Workers reached the readiness condition but
       the platform did not assign a URL or mark the app as ready to serve.
    
    The ``reason`` attribute contains diagnostic details including the
    readiness condition that was requested, backend status flags, and a
    snapshot of worker counts (running / pending / crashlooping / failed).
    
    To investigate further, use ``deployed_app.logs()`` or
    ``deployed_app.replicas()``.  If the failure is a timeout, consider
    increasing ``max_wait_time``.  If workers crash shortly after startup,
    consider increasing ``readiness_wait_time`` to widen the post-readiness
    health-check window.
    """
    def __init__(self, app_id: str, reason: typing.Union[str, None] = None):
        ...
    def __str__(self):
        ...
    ...

class AppUpgradeInProgressException(AppDeploymentException, metaclass=type):
    """
    Raised when another deployment to this app is already running.
    
    This prevents conflicting concurrent deployments. Either wait for the
    existing deployment to complete, or use `force_upgrade=True` to take over.
    """
    def __init__(self, app_id: str, upgrader: typing.Union[str, None] = None):
        ...
    def __str__(self):
        ...
    ...

class AppConcurrentUpgradeException(AppDeploymentException, metaclass=type):
    """
    Raised when another deployment started while this one was in progress.
    
    The current deployment has been invalidated because someone else deployed
    a new version. Check `modified_by` to see who triggered the conflicting
    deployment. Use unique app names or coordinate deployments to avoid this.
    """
    def __init__(self, app_id: str, expected_version: str, actual_version: str, modified_by: typing.Union[str, None] = None, modified_at: typing.Union[str, None] = None):
        ...
    def __str__(self):
        ...
    ...

class AppDeletedDuringDeploymentException(AppDeploymentException, metaclass=type):
    """
    Raised when the app was deleted while this deployment was waiting for readiness.
    
    Another process or user deleted the app before deployment completed.
    """
    def __init__(self, app_id: str):
        ...
    def __str__(self):
        ...
    ...

