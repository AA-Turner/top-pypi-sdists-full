######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.19.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-02-11T23:40:09.154693                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.exceptions
    import metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine

from ._state_machine import LogLine as LogLine

class OuterboundsBackendUnhealthyException(Exception, metaclass=type):
    """
    Raised when the Outerbounds platform returns 5xx errors or is unreachable.
    
    Catch this to handle temporary platform outages gracefully. The request
    can typically be retried after a short delay.
    """
    def __init__(self, url: str, method: str, status_code: typing.Optional[int] = None, text: typing.Optional[str] = None, message: typing.Optional[str] = None):
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
    def __init__(self, url: str, method: str, status_code: int, text: str, message: typing.Optional[str] = None):
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
    def __init__(self, capsule_id: str, worker_id: str, logs: typing.Optional[typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.LogLine]] = None):
        ...
    def __str__(self):
        ...
    ...

class CapsuleReadinessException(CapsuleDeploymentException, metaclass=type):
    """
    Raised when capsule fails to meet readiness conditions within timeout.
    """
    def __init__(self, capsule_id: str, reason: typing.Optional[str] = None):
        ...
    def __str__(self):
        ...
    ...

class CapsuleConcurrentUpgradeException(CapsuleDeploymentException, metaclass=type):
    """
    Raised when a concurrent upgrade invalidates the current deployment.
    """
    def __init__(self, capsule_id: str, expected_version: str, actual_version: str, modified_by: typing.Optional[str] = None, modified_at: typing.Optional[str] = None):
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
    def __init__(self, app_id: str, worker_id: str, logs: typing.Optional[typing.List] = None):
        ...
    def __str__(self):
        ...
    ...

class AppReadinessException(AppDeploymentException, metaclass=type):
    """
    Raised when the app does not become ready within `max_wait_time`.
    
    This typically means workers are still starting up or stuck in a pending state.
    Use `deployed_app.logs()` or `deployed_app.replicas()` to investigate.
    Consider increasing `max_wait_time` if your app has a slow startup.
    """
    def __init__(self, app_id: str, reason: typing.Optional[str] = None):
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
    def __init__(self, app_id: str, upgrader: typing.Optional[str] = None):
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
    def __init__(self, app_id: str, expected_version: str, actual_version: str, modified_by: typing.Optional[str] = None, modified_at: typing.Optional[str] = None):
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

