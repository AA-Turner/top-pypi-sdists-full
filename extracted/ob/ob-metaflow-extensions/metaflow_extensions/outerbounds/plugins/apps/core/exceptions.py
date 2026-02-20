import json
from typing import Optional, List, Dict
from ._state_machine import LogLine


class OuterboundsBackendUnhealthyException(Exception):
    """
    Raised when the Outerbounds platform returns 5xx errors or is unreachable.

    Catch this to handle temporary platform outages gracefully. The request
    can typically be retried after a short delay.
    """

    def __init__(
        self,
        url: str,
        method: str,
        status_code: Optional[int] = None,
        text: Optional[str] = None,
        message: Optional[str] = None,
    ):
        self.url = url
        self.method = method
        self.status_code = status_code
        self.text = text
        self.message = message
        super().__init__(self.message)


class OuterboundsForbiddenException(Exception):
    """This exception is raised when access to an Outerbounds API is forbidden (HTTP 403)."""

    def __init__(
        self,
        url: str,
        method: str,
        text: str,
    ):
        self.url = url
        self.method = method
        self.text = text
        self.message = (
            f"Access forbidden (HTTP 403) when calling {url}. "
            "This typically means your credentials lack permission for this operation. "
            "Please verify that you outerbounds / metaflow configuration has access to the "
            "correct perimeter.\n"
            "If you believe this is an error, contact your Outerbounds administrator."
        )
        super().__init__(self.message)


class OuterboundsConfigurationException(Exception):
    """This exception is raised when Outerbounds configuration is missing or invalid."""

    def __init__(self, missing_config: str):
        self.missing_config = missing_config
        self.message = (
            f"Outerbounds configuration '{missing_config}' not found.\n\n"
            "If running locally:\n"
            "  - Run: outerbounds configure <magic-string-from-outerbounds-ui>\n"
            "If running remotely (e.g., in a Metaflow task):\n"
            "  - Ensure you have the Outerbounds distribution installed (pip install outerbounds)\n"
            "    and not the open-source Metaflow. The Outerbounds fork injects configuration\n"
            "    into remote tasks automatically which may not be present in open source metaflow.\n"
        )
        super().__init__(self.message)


class CapsuleApiException(Exception):
    def __init__(
        self,
        url: str,
        method: str,
        status_code: int,
        text: str,
        message: Optional[str] = None,
    ):
        self.url = url
        self.method = method
        self.status_code = status_code
        self.text = text
        self.message = message

    def __str__(self):
        return (
            f"CapsuleApiException: {self.url} [{self.method}]: Status Code: {self.status_code} \n\n {self.text}"
            + (f"\n\n {self.message}" if self.message else "")
        )


class CapsuleDeploymentException(Exception):
    """Base exception for all capsule deployment failures."""

    def __init__(
        self,
        capsule_id: str,
        message: str,
    ):
        self.capsule_id = capsule_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"CapsuleDeploymentException: [{self.capsule_id}] :: {self.message}"


class CapsuleCrashLoopException(CapsuleDeploymentException):
    """Raised when a worker enters CrashLoopBackOff or Failed state."""

    def __init__(
        self,
        capsule_id: str,
        worker_id: str,
        logs: Optional[List[LogLine]] = None,
    ):
        self.worker_id = worker_id
        self.logs = logs or []
        message = f"Worker ID ({worker_id}) is crashlooping. Please check the logs for more information."
        super().__init__(capsule_id, message)

    def __str__(self):
        return f"CapsuleCrashLoopException: [{self.capsule_id}] :: {self.message}"


class CapsuleReadinessException(CapsuleDeploymentException):
    """Raised when capsule fails to meet readiness conditions within timeout.

    Carries raw diagnostic data so higher-level callers can decide how to
    present the failure reason.
    """

    def __init__(
        self,
        capsule_id: str,
        capsule_status: Optional[Dict] = None,
        worker_semantic_status: Optional[Dict] = None,
        readiness_condition: Optional[str] = None,
        min_replicas: Optional[int] = None,
        max_wait_time: Optional[int] = None,
        timed_out: bool = False,
    ):
        self.capsule_status = capsule_status
        self.worker_semantic_status = worker_semantic_status
        self.readiness_condition = readiness_condition
        self.min_replicas = min_replicas
        self.max_wait_time = max_wait_time
        self.timed_out = timed_out
        message = f"Capsule {capsule_id} failed to be ready to serve traffic"
        super().__init__(capsule_id, message)

    def __str__(self):
        return f"CapsuleReadinessException: [{self.capsule_id}] :: {self.message}"


class CapsuleConcurrentUpgradeException(CapsuleDeploymentException):
    """Raised when a concurrent upgrade invalidates the current deployment."""

    def __init__(
        self,
        capsule_id: str,
        expected_version: str,
        actual_version: str,
        modified_by: Optional[str] = None,
        modified_at: Optional[str] = None,
    ):
        self.expected_version = expected_version
        self.actual_version = actual_version
        self.modified_by = modified_by
        self.modified_at = modified_at
        message = (
            f"A capsule upgrade was triggered outside current deployment instance. "
            f"Expected version: {expected_version}, actual version: {actual_version}"
        )
        if modified_by:
            message += f". Modified by: {modified_by}"
        if modified_at:
            message += f" at {modified_at}"
        super().__init__(capsule_id, message)

    def __str__(self):
        return (
            f"CapsuleConcurrentUpgradeException: [{self.capsule_id}] :: {self.message}"
        )


class CapsuleDeletedDuringDeploymentException(CapsuleDeploymentException):
    """Raised when a capsule is deleted while deployment is in progress."""

    def __init__(self, capsule_id: str):
        super().__init__(capsule_id, "Capsule was deleted during deployment")


class CodePackagingException(Exception):
    """Exception raised when code packaging fails."""

    pass


class AppNotFoundException(Exception):
    """
    Raised when attempting to access an app that does not exist.

    This can occur when calling methods on `DeployedApp` for an app that
    has been deleted or never existed.
    """

    pass


class AppCreationFailedException(Exception):
    """
    Raised when the platform rejects an app deployment request.

    Common causes include invalid configuration, quota limits, or permission issues.
    Check `status_code` and `error_text` for details on why the request was rejected.
    """

    def __init__(
        self,
        app_name: str,
        status_code: int,
        error_text: str,
    ):
        self.status_code = status_code
        self.error_text = error_text
        message = f"Failed to submit app deployment: HTTP {status_code} - {error_text}"
        if status_code == 400:
            # 400 = validation error; the app configuration is invalid and must be fixed.
            message = "Invalid app deployment configuration submitted: "
            try:
                reason_for_failure = json.loads(error_text).get("message", error_text)
            except json.JSONDecodeError:
                reason_for_failure = error_text
            message += reason_for_failure
            message += (
                "\n\nCheck your config file or CLI parameters if deploying via CLI, "
                "or AppDeployer parameters if deploying programmatically."
            )

        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"AppCreationFailedException: {self.message}"


class AppDeploymentException(Exception):
    """
    Base exception for app deployment failures that occur after submission.

    All deployment exceptions provide a `deployed_app` property that returns
    a `DeployedApp` object, allowing you to inspect logs or app state even
    after a failure.
    """

    def __init__(self, app_id: str, message: str):
        self.app_id = app_id
        self.message = message
        self._deployed_app = None
        super().__init__(self.message)

    def __str__(self):
        return f"AppDeploymentException: [{self.app_id}] :: {self.message}"

    @property
    def deployed_app(self):
        """
        Returns a `DeployedApp` object for the failed deployment.
        Use this to inspect logs, replica status, or other details after catching
        the exception. For example: `e.deployed_app.logs()` to fetch recent logs.
        """
        from .deployer import DeployedApp

        return DeployedApp._from_capsule_id(self.app_id)


class AppCrashLoopException(AppDeploymentException):
    """
    Raised when an app worker crashes repeatedly during startup.

    The `logs` attribute contains recent log lines from the failing worker,
    which typically reveal the cause (e.g., import errors, missing dependencies,
    or application exceptions). The `worker_id` identifies which replica failed.
    """

    def __init__(
        self,
        app_id: str,
        worker_id: str,
        logs: Optional[List] = None,
    ):
        self.worker_id = worker_id
        self.logs = logs or []
        message = f"Worker ({worker_id}) is crashlooping. Please check the logs for more information."
        super().__init__(app_id, message)

    def __str__(self):
        return f"AppCrashLoopException: [{self.app_id}] :: {self.message}"


class AppReadinessException(AppDeploymentException):
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

    def __init__(self, app_id: str, reason: Optional[str] = None):
        message = f"App {app_id} failed to be ready to serve traffic"
        if reason:
            message += f": {reason}"
        super().__init__(app_id, message)

    def __str__(self):
        return f"AppReadinessException: [{self.app_id}] :: {self.message}"


class AppUpgradeInProgressException(AppDeploymentException):
    """
    Raised when another deployment to this app is already running.

    This prevents conflicting concurrent deployments. Either wait for the
    existing deployment to complete, or use `force_upgrade=True` to take over.
    """

    def __init__(
        self,
        app_id: str,
        upgrader: Optional[str] = None,
    ):
        self.upgrader = upgrader
        if upgrader:
            message = (
                f"App {app_id} is currently being upgraded by {upgrader}. "
                "Use force_upgrade=True in AppDeployer to override."
            )
        else:
            message = (
                f"App {app_id} is currently being upgraded. "
                "Use force_upgrade=True in AppDeployer to override."
            )
        super().__init__(app_id, message)

    def __str__(self):
        return f"AppUpgradeInProgressException: [{self.app_id}] :: {self.message}"


class AppConcurrentUpgradeException(AppDeploymentException):
    """
    Raised when another deployment started while this one was in progress.

    The current deployment has been invalidated because someone else deployed
    a new version. Check `modified_by` to see who triggered the conflicting
    deployment. Use unique app names or coordinate deployments to avoid this.
    """

    def __init__(
        self,
        app_id: str,
        expected_version: str,
        actual_version: str,
        modified_by: Optional[str] = None,
        modified_at: Optional[str] = None,
    ):
        self.expected_version = expected_version
        self.actual_version = actual_version
        self.modified_by = modified_by
        self.modified_at = modified_at

        modifier_info = ""
        if modified_by:
            modifier_info = f" by '{modified_by}'"
            if modified_at:
                modifier_info += f" at {modified_at}"

        message = (
            f"Another deployment was triggered{modifier_info} while this deployment was in progress.\n\n"
            f"This deployment expected to be working with version '{expected_version}', but the app "
            f"is now at version '{actual_version}'. The current deployment has been invalidated.\n\n"
            "To avoid this in the future, you can either use a unique `name` for each deployment "
            "or coordinate deployments to ensure concurrent upgrades to the same app don't overlap."
        )
        super().__init__(app_id, message)

    def __str__(self):
        return f"AppConcurrentUpgradeException: [{self.app_id}] :: {self.message}"


class AppDeletedDuringDeploymentException(AppDeploymentException):
    """
    Raised when the app was deleted while this deployment was waiting for readiness.

    Another process or user deleted the app before deployment completed.
    """

    def __init__(self, app_id: str):
        message = (
            f"App '{app_id}' was deleted while this deployment was in progress.\n\n"
            "This can happen when another process or user deletes the app during deployment. "
            "Since apps can be programmatically created and deleted, concurrent operations "
            "may conflict. If you did not intend to delete this app, check for other processes "
            "or users that may be managing deployments in this perimeter."
        )
        super().__init__(app_id, message)

    def __str__(self):
        return f"AppDeletedDuringDeploymentException: [{self.app_id}] :: {self.message}"
