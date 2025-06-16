from metaflow.exception import MetaflowException
from .constants import SUPPORTABLE_GPU_TYPES


class NvcfJobFailedException(MetaflowException):
    headline = "[@nvidia] error"

    def __init__(self, msg):
        super(NvcfJobFailedException, self).__init__(msg)


class NvcfPollingConnectionError(MetaflowException):
    headline = "[@nvidia] polling error."

    def __init__(self, og_error_msg):
        msg = (
            "An error occurred while polling the job status. "
            "\n\nOriginal error message: %s" % (og_error_msg)
        )

        super(NvcfPollingConnectionError, self).__init__(msg)


class RequestedGPUTypeUnavailableException(MetaflowException):
    headline = "[@nvidia RequestedGPUTypeUnavailableException] GPU type unavailable."

    def __init__(self, requested_gpu_type):
        msg = (
            f"The requested GPU type @nvidia(..., gpu_type='{requested_gpu_type}') is not available. "
            f"Please choose from the following supported GPU types when using @nvidia: {SUPPORTABLE_GPU_TYPES}"
        )
        super(RequestedGPUTypeUnavailableException, self).__init__(msg)


class UnsupportedNvcfConfigurationException(MetaflowException):
    headline = (
        "[@nvidia UnsupportedNvcfConfigurationException] Unsupported GPU configuration"
    )

    def __init__(self, n_gpu, gpu_type, available_configurations, step):
        msg = f"The requested configuration of @nvidia(gpu={n_gpu}, gpu_type='{gpu_type}') for @step {step} is not available."
        if len(available_configurations) == 0:
            msg += (
                "\n\nNo configurations are available in your Outerbounds deployment."
                " Please contact Outerbounds support if you wish to use @nvidia."
            )
        else:
            msg += f"\n\nAvailable configurations for your deployment include: \n\t- {self._display(available_configurations)}"
            msg += "\n\nPlease contact Outerbounds support if you wish to use a configuration not listed above."
        super(UnsupportedNvcfConfigurationException, self).__init__(msg)

    def _display(self, configs):
        _available_decos = []
        for cfg in configs:
            n_gpu, gpu_type = cfg[0], cfg[1]
            _available_decos.append(f"@nvidia(gpu={n_gpu}, gpu_type='{gpu_type}')")
        return "\n\t- ".join(_available_decos)


class UnsupportedNvcfDatastoreException(MetaflowException):
    headline = "[@nvidia UnsupportedNvcfDatastoreException] Unsupported datastore"

    def __init__(self, ds_type):
        msg = (
            "The *@nvidia* decorator requires --datastore=s3 or --datastore=azure or --datastore=gs at the moment."
            f"Current datastore type: {ds_type}."
        )
        super(UnsupportedNvcfDatastoreException, self).__init__(msg)


class NvcfTimeoutTooShortException(MetaflowException):
    headline = "[@nvidia NvcfTimeoutTooShortException] Timeout too short"

    def __init__(self, step):
        msg = (
            "The timeout for step *{step}* should be at least 60 seconds for "
            "execution with @nvidia".format(step=step)
        )
        super(NvcfTimeoutTooShortException, self).__init__(msg)


class NvcfQueueTimeoutTooShortException(MetaflowException):
    headline = "[@nvidia NvcfQueueTimeoutTooShortException] Queue Timeout too short"

    def __init__(self, step):
        msg = (
            "The queue timeout for step *{step}* should be at least 60 seconds for "
            "execution with @nvidia".format(step=step)
        )
        super(NvcfQueueTimeoutTooShortException, self).__init__(msg)


class NvcfKilledException(MetaflowException):
    headline = "Nvidia job killed"
