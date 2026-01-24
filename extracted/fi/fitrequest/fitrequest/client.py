from fitrequest.class_factory import ClassFactory
from fitrequest.client_base import FitRequestBase


class FitRequest(FitRequestBase, metaclass=ClassFactory):
    """
    This class serves as a configuration for declaring ``fitrequest`` methods,
    providing an alternative to directly using ``FitConfig``.
    It allows you to use the ``@fit`` decorator to define these methods.

    Keep in mind that the attributes ``method_docstring`` and ``method_config_list``
    are exclusively for generating methods. These attributes are discarded during the final class generation.

    Attributes like ``client_name``, ``version``, ``base_url``, and ``auth`` are transformed into read-only properties.
    """

    client_name: str

    version: str

    base_url: str | None

    auth: dict | None

    method_docstring: str

    method_config_list: list[dict]
