from dlt.extract.exceptions import DltResourceException


class TransformationException(DltResourceException):
    def __init__(self, resource_name: str, msg: str):
        super().__init__(resource_name, msg)


class TransformationTypeMismatch(TransformationException):
    def __init__(self, resource_name: str, msg: str):
        super().__init__(resource_name, msg)


class IncompatibleDatasetsException(TransformationException):
    def __init__(self, resource_name: str, msg: str):
        super().__init__(resource_name, msg)


class TransformationInvalidReturnTypeException(TransformationException):
    def __init__(self, resource_name: str, msg: str):
        super().__init__(resource_name, msg)


class UnboundDatasetArgument(TransformationException):
    def __init__(self, resource_name: str):
        super().__init__(resource_name, "Transformation has unbound Dataset(s) arguments")
