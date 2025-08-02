from sidecar.utils import Utils


class SandboxError:
    def __init__(self, time: str, code: str, message: str):
        self.message = message
        self.code = code
        self.time = time

    @staticmethod
    def FailedDownloadingAppArtifactToSidecar(app_name: str) -> 'SandboxError':
        return SandboxError(message=f'An error occurred while downloading artifacts for {app_name}. '
                                    f'Make sure the artifacts reside in your artifact repository',
                            code=ErrorCodes.ARTIFACTS_DOWNLOAD_FAILED,
                            time=Utils.get_utc_now_in_isoformat())

    @staticmethod
    def TimeoutDownloadingAppArtifactToSidecar(app_name: str) -> 'SandboxError':
        return SandboxError(message=f'Missing artifacts for {app_name}. '
                                    f'Make sure the artifacts in your artifact repository',
                            code=ErrorCodes.ARTIFACTS_DOWNLOAD_TIMEOUT,
                            time=Utils.get_utc_now_in_isoformat())

    @staticmethod
    def PrivateHealthcheckFailed(app_name: str) -> 'SandboxError':
        return SandboxError(message=f'Deployment verification failed for {app_name}. '
                                    f'Timeout was reached while running health-check on one or more instances',
                            code=ErrorCodes.PRIVATE_HEALTHCHECK_FAILED,
                            time=Utils.get_utc_now_in_isoformat())

    @staticmethod
    def PublicHealthcheckFailed(app_name: str) -> 'SandboxError':
        return SandboxError(message=f'Deployment verification failed for {app_name}. '
                                    f'Timeout was reached while running health-check with the application’s public IP address',
                            code=ErrorCodes.PUBLIC_HEALTHCHECK_FAILED,
                            time=Utils.get_utc_now_in_isoformat())

    @staticmethod
    def from_dict(d: dict) -> 'SandboxError':
        return SandboxError(message=str(d["message"]),
                            code=str(d["code"]),
                            time=str(d["time"]))

    def to_dict(self) -> dict:
        return {"message": self.message,
                "code": self.code,
                "time": self.time}


class ErrorCodes:
    ARTIFACTS_DOWNLOAD_FAILED = "ARTIFACTS_DOWNLOAD_FAILED"
    ARTIFACTS_DOWNLOAD_TIMEOUT = "ARTIFACTS_DOWNLOAD_TIMEOUT"
    ENDING_FAILED = "ENDING_FAILED"
    PRIVATE_HEALTHCHECK_FAILED = 'APP_INSTANCE_HEALTHCHECK_FAILED'
    PUBLIC_HEALTHCHECK_FAILED = 'PUBLIC_HEALTHCHECK_FAILED'

