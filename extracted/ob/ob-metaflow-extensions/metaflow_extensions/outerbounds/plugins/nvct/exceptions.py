from metaflow.exception import MetaflowException


class NvctExecutionException(MetaflowException):
    headline = "Nvct task couldn't be executed"


class NvctTaskFailedException(MetaflowException):
    headline = "Nvct task failed"


class NvctKilledException(MetaflowException):
    headline = "Nvct job killed"


class RequestedGPUTypeUnavailableException(MetaflowException):
    headline = "[@nvct RequestedGPUTypeUnavailableException] GPU type unavailable."

    def __init__(self, requested_gpu_type, available_gpus):
        msg = (
            f"The requested GPU type @nvct(..., gpu_type='{requested_gpu_type}') is not available. "
            f"Please choose from the following supported GPU types when using @nvct: {available_gpus}"
        )
        super(RequestedGPUTypeUnavailableException, self).__init__(msg)


class UnsupportedNvctConfigurationException(MetaflowException):
    headline = (
        "[@nvct UnsupportedNvctConfigurationException] Unsupported GPU configuration"
    )

    def __init__(self, n_gpu, gpu_type, available_configurations, step):
        msg = f"The requested configuration of @nvct(gpu={n_gpu}, gpu_type='{gpu_type}') for @step {step} is not available."
        if len(available_configurations) == 0:
            msg += (
                "\n\nNo configurations are available in your Outerbounds deployment."
                " Please contact Outerbounds support if you wish to use @nvct."
            )
        else:
            msg += f"\n\nAvailable configurations for your deployment with {gpu_type} include: \n\t- {self._display(gpu_type, available_configurations)}"
            msg += "\n\nPlease contact Outerbounds support if you wish to use a configuration not listed above."
        super(UnsupportedNvctConfigurationException, self).__init__(msg)

    def _display(self, gpu_type, configs):
        _available_decos = []
        for cfg in configs:
            n_gpu = cfg["n_gpus"]
            _available_decos.append(f"@nvct(gpu={n_gpu}, gpu_type='{gpu_type}')")
        return "\n\t- ".join(_available_decos)


class UnsupportedNvctDatastoreException(MetaflowException):
    headline = "[@nvct UnsupportedNvctDatastoreException] Unsupported datastore"

    def __init__(self, ds_type):
        msg = (
            "The *@nvct* decorator requires --datastore=s3 or --datastore=azure or --datastore=gs at the moment."
            f"Current datastore type: {ds_type}."
        )
        super(UnsupportedNvctDatastoreException, self).__init__(msg)


class NvctTimeoutTooShortException(MetaflowException):
    headline = "[@nvct NvctTimeoutTooShortException] Timeout too short"

    def __init__(self, step):
        msg = (
            "The timeout for step *{step}* should be at least 60 seconds for "
            "execution with @nvct".format(step=step)
        )
        super(NvctTimeoutTooShortException, self).__init__(msg)
