from collections.abc import Callable
from functools import reduce, wraps
from typing import Any

import httpx
from makefun import with_signature

from fitrequest.errors import UnrecognizedParametersError
from fitrequest.method_config import MethodConfig
from fitrequest.utils import extract_method_params


class Generator:
    @staticmethod
    def get_url_params(method_config: MethodConfig, **kwargs) -> dict:
        """
        Return the keyword arguments from ``kwargs`` that correspond to URL parameters.

        This involves merging the parameters found in the ``params`` keyword argument
        with those inferred directly from the method's signature.

        Parameters from the method signature have priority over any parameters specified
        in the ``params`` field of ``kwargs``.

        Additionally, replace any arguments with specified aliases using their corresponding replacements.
        """
        if (method_params := method_config.params_signature) is None:
            return {}

        return {
            'params': (
                kwargs.get('params', {})
                | {
                    method_params.alias_of(field): method_params.value_of(field, value)
                    for field, value in kwargs.items()
                    if field in method_params.signature_varnames
                }
            )
        }

    @staticmethod
    def unknown_params(method_config: MethodConfig, request_method_base: dict, **kwargs) -> set[str]:
        """
        Returns the collection of unexpected parameters found in the method arguments (kwargs).
        The only expected parameters are those reserved for ``fit_request``, ``httpx.Request``,
        the keyword ``self``, and URL parameters.
        """
        signature_params = method_config.params_signature.signature_varnames if method_config.params_signature else {}
        return set(kwargs).difference({'self', *signature_params, *request_method_base})

    @staticmethod
    def format_params(method_config: MethodConfig, **kwargs) -> dict:
        """Format and check params of generated method, raise on unrecognized arguments."""
        instance = kwargs['self']
        request_method = instance.session.request

        frozen_params = {'method_config': method_config, 'instance': instance}
        endpoint_params = {field: value for field, value in kwargs.items() if field in method_config.endpoint_varnames}

        # Filter out unknown args and freeze method_config argument
        request_method_params = (
            extract_method_params(httpx.request, kwargs)
            | extract_method_params(request_method, kwargs)
            | endpoint_params
            | frozen_params
        )

        if diff := Generator.unknown_params(method_config, request_method_params, **kwargs):
            raise UnrecognizedParametersError(
                method_name=method_config.name,
                unrecognized_arguments=diff,
            )
        return request_method_params | Generator.get_url_params(method_config, **kwargs)

    @classmethod
    def generate_method(cls, method_config: MethodConfig) -> Callable:
        """Generate method from configuration with correct signature."""
        # Add some common modules to makefun environment
        import datetime  # noqa: F401, PLC0415
        import enum  # noqa: F401, PLC0415
        import typing  # noqa: F401, PLC0415

        @with_signature(method_config.signature, doc=method_config.docstring)
        def generated_method(*args, **kwargs) -> Any:
            method_params = cls.format_params(method_config, **kwargs)
            return kwargs['self'].session.request(*args, **method_params)

        @with_signature(method_config.signature, doc=method_config.docstring)
        async def generated_async_method(*args, **kwargs) -> Any:
            method_params = cls.format_params(method_config, **kwargs)
            return await kwargs['self'].session.async_request(*args, **method_params)

        # Select between async/sync method, and apply decorators
        new_method = generated_async_method if method_config.async_method else generated_method
        new_method.fit_method = True
        decorators = reversed(method_config.decorators)
        return reduce(lambda func, decorator: wraps(func)(decorator(func)), [new_method, *decorators])
