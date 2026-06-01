class PicselliaError(Exception):
    """Base class for exceptions."""

    def __init__(self, message="Something went wrong"):
        """
        Arguments:
            message (str): Informative message about the exception.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class AuthenticationError(PicselliaError):
    """Raised by picsellia-tf2 package"""

    pass


class BadConfigurationContinuousTrainingError(PicselliaError):
    """Raised when a setup of continuous training is not well configured"""

    pass


class BadRequestError(PicselliaError):
    """Indicates a malformed or unsupported query. This can be the result of either client
    or server side query validation."""

    pass


class RequestTooLargeError(PicselliaError):
    """Request is too large and server do not allow it. You might want to retry with a smaller query or payload"""

    pass


class BadGatewayError(PicselliaError):
    """Picsellia is unavailable at the moment"""

    pass


class TooManyRequestError(PicselliaError):
    """Raised when too much request are done to the server."""

    pass


class ContextSourceNotDefined(PicselliaError):
    """Raised if experiment of a ModelContext is not defined"""

    pass


class ContextDataNotDefined(PicselliaError):
    """Raised if dataset of a ModelContext is not defined"""

    pass


class DistantStorageError(PicselliaError):
    """Raised when an upload or a download from S3 storage went wrong"""

    pass


class UploadError(PicselliaError):
    """Raised when an upload went wrong"""

    def __init__(self, message: str, path: str, parent: Exception | None):
        super().__init__(message)
        self.path = path
        self.parent = parent


class UnprocessableData(UploadError):
    """Raised when a data could not be processed by our services"""

    def __init__(self, data):
        super().__init__(
            message=f"{data.filename} could not be processed by our services.",
            path=data.filename,
            parent=None,
        )


class DownloadError(PicselliaError):
    """Raised when a download went wrong"""

    pass


class FileNotFoundException(PicselliaError):
    """Raised when a file is not found"""

    pass


class ForbiddenError(PicselliaError):
    """Raised when your token does not match to any known token"""

    pass


class InsufficientResourcesError(PicselliaError):
    """Raised when your token does not match to any known token"""

    pass


class InternalServerError(PicselliaError):
    """Raised when Picsellia threw an unusual InternalServerError"""

    pass


class MonitorError(PicselliaError):
    """Raised when a prediction could not have been monitored by Oracle"""

    pass


class NetworkError(PicselliaError):
    """Raised when an HTTPError occurs."""

    pass


class NoBaseExperimentError(PicselliaError):
    """Raised when exception has no base experiment"""

    pass


class NoBaseModelVersionError(PicselliaError):
    """Raised when exception has no base model"""

    pass


class NoConnectorFound(PicselliaError):
    """Raised if connection object is not pointed to any organization"""

    pass


class NoDataError(PicselliaError):
    """Raised when you try to retrieve data from an empty datalake"""

    pass


class NoShadowModel(PicselliaError):
    """Raised when there is no shadow model for a deployment"""

    pass


class NothingDoneError(PicselliaError):
    """Raised when something should have been done but nothing happened"""

    pass


class PredictionError(PicselliaError):
    """Raised when a prediction could not have been done"""

    pass


class ResourceConflictError(PicselliaError):
    """Exception raised when a given resource already exists."""

    pass


class ResourceLockedError(PicselliaError):
    """Exception raised when a resource is locked, and you're trying to create, update or delete a linked resource"""

    pass


class ResourceNotFoundError(PicselliaError):
    """Exception raised when a given resource is not found."""

    pass


class UnauthorizedError(PicselliaError):
    """Raised when your token does not match to any known token"""

    pass


class UndefinedObjectError(PicselliaError):
    """Raised when Dao is initialized without id"""

    pass


class AnnotationFileIncoherentTypeException(PicselliaError):
    """Raised when annotation file can't be imported in a dataset due to its type"""

    pass


class UnparsableAnnotationFileException(PicselliaError):
    """Raised when annotation file is unparsable"""

    pass


class UploadFailed(PicselliaError):
    """Raised when an upload of a file has failed"""

    pass


class WaitingAttemptsTimeout(PicselliaError):
    """Raised when a job.wait_for_status is taking too much attempts"""

    pass


class WrongJobVersionError(PicselliaError):
    """Raised when a user attenmpt to use a JobV2 method on a legacy job"""

    pass


class IllegalJobTransitionError(PicselliaError):
    """Raised when you try to change a job status to an incoherent one"""

    pass


class NotSupportedJobVersionError(PicselliaError):
    """Raised when you try to use an unsupported job version"""

    pass


class NoUrlAvailable(PicselliaError):
    """Raised on download when no url could be retrieved from platform"""

    pass


class ContentTypeUnknown(PicselliaError):
    """Raised when content type is not known on monitor"""

    pass


class MonitoringConnectionError(PicselliaError):
    """Raised when a call to Oracle or Serving is returning a 50X"""

    pass
