from ...plugins.apps.core.exceptions import (
    AppDeploymentException,
    AppCrashLoopException,
    AppReadinessException,
    AppConcurrentUpgradeException,
    AppUpgradeInProgressException,
    AppCreationFailedException,
    AppNotFoundException,
    AppDeletedDuringDeploymentException,
    OuterboundsBackendUnhealthyException,
)
