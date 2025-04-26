class Error(Exception):
    '''
    Base class for all controlled exceptions raised by the CDK.

    If possible, please do not raise this exception. Instead, choose one of its
    descendants. If none of the existing ones has a meaningful name for a new
    error condition that has to be accounted for, better create it.

    When used as context managers, connectors capture any other possible errors,
    and wrap them as bare Error exceptions with the original one as their cause.
    '''

class TinybirdClientError(Error):
    '''
    Superclass of all errors raised by the tb client
    '''

class UnknownConnectorError(Error):
    '''
    Raised by `connector_for()` if it gets passed an unknown connector name.
    '''
    def __init__(self, name):
        super().__init__(f'Unknown connector name {name}')

class UnsupportedFormatError(Error):
    '''
    Raised by connectors, by contract, if they are asked to export to a format
    they do not support.
    '''
    def __init__(self, fmt):
        super().__init__(f'Unsupported format {fmt}')

class MissingConfiguration(Error):
    '''
    Raised by config.get() when a required environment variable is unset.
    '''
    def __init__(self, name):
        super().__init__(f'{name} is required')

class JobError(TinybirdClientError):
    '''
    Raised by the Tinybird client when a job it is waiting for has `error`
    status.
    '''
    def __init__(self, error_message, job_id):
        self.message = error_message
        self.job_id = job_id
        super().__init__(f'Job {job_id} error: {error_message}')

class RateLimitedForTooLongError(TinybirdClientError):
    '''
    Raised by the Tinybird client if it accumulates one hour of consecutive
    waits for the same rate-limited request.
    '''
    def __init__(self, max_rate_limit_retry_s):
        super().__init__(f'Rate-limited retries exceeded {max_rate_limit_retry_s} seconds')

class HTTPError(TinybirdClientError):
    '''
    Raised by the Tinybird client performs an unsuccessful request that is not
    retried.
    '''
    def __init__(self, method, response, error_message, job_response):
        self.status_code = response.status_code
        self.url = response.url
        self.message = error_message
        self.job_response = job_response
        super().__init__(f'{response.status_code} code for {method} {response.url}: {error_message}')

class UnsupportedCloudServiceSchemeError(Error):
    '''
    Raised by cloud URL parsing if given the URL of an unknown provider.
    '''
    def __init__(self, scheme):
        super().__init__(f'The cloud service scheme {scheme} is unsupported')

class UnsupportedCloudServiceError(Error):
    '''
    Raised by `client_for()` if it gets passed the name of an unsupported cloud
    provider.
    '''
    def __init__(self, service):
        super().__init__(f'The cloud service {service} is unsupported')

class ExternalDatasourceError(Error):
    '''
    Raised by the external datasource
    '''
    def __init__(self, message: str):
        self.message = message.replace('\n', ' ')

class SnowflakeConnectionError(Error):
    '''
    Raised when snowflake connector throws an exception
    '''
    def __init__(self, message: str):
        self.message = message.replace('\n', ' ')
