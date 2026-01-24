import inspect
from collections.abc import Callable

from pydantic import BaseModel

from fitrequest.fit_config import FitConfig
from fitrequest.generator import Generator
from fitrequest.method_config import MethodConfig
from fitrequest.request_params import extract_params
from fitrequest.templating import jinja_env
from fitrequest.utils import is_basemodel_subclass, string_varnames


class ClassFactory(type):
    """Metaclass to create new FitRequest classes."""

    @classmethod
    def get_return_pydantic_model(cls, cls_func: Callable) -> type[BaseModel] | None:
        """
        Inspects the function's return annotation and returns the corresponding Pydantic model
        if the annotation is supported by fitrequest.

        Supported annotation types:
        - list[BaseModel]
        - BaseModel
        """
        return_ann = inspect.get_annotations(cls_func, eval_str=True).get('return')

        if return_ann is None:
            return None

        if (
            hasattr(return_ann, '__origin__')
            and isinstance(return_ann.__origin__, type(list))
            and len(return_ann.__args__) == 1
            and isinstance(return_ann.__args__[0], type(BaseModel))
        ):
            return return_ann.__args__[0]

        if is_basemodel_subclass(return_ann):
            return return_ann

        return None

    @classmethod
    def handle_fit_decorator(cls, cls_dict: dict) -> None:
        """
        Handle methods decorated with `@fit`. This function generates corresponding `fitrequest` methods
        and sets the `shared['generated_method']` attribute on each decorated method.
        The reason we cannot directly add the configuration to `method_config_list`
        is that there may be other decorators applied above `@fit`: any decorators above `@fit` would be ignored,
        leading to unexpected behavior.

        To address this, the `@fit` decorator has two roles:
        1. Marking the function as a "fit" method.
        2. Executing the generated method stored in `cls_func.shared['generated_method']`.

        The execution flow is as follows:
        1. The `@fit` decorator marks the function as a "fit" method.
        2. This function generates the corresponding `fitrequest` method and sets it in `shared['generated_method']`.
        3. The `@fit` decorator executes the generated method stored in `shared['generated_method']`.
        """
        for cls_func in cls_dict.values():
            if not (callable(cls_func) and hasattr(cls_func, 'fit_decorator')):
                continue

            decorator = cls_func.fit_decorator.dump()
            endpoint_varnames = string_varnames(jinja_env, decorator['endpoint'])

            config = decorator | {
                'name': cls_func.__name__,
                'docstring': cls_func.__doc__ or cls_dict.get('method_docstring', ''),
                'base_url': decorator.get('base_url') or cls_dict.get('base_url'),
                'async_method': inspect.iscoroutinefunction(cls_func),
                'response_model': cls.get_return_pydantic_model(cls_func),
                'params_model': extract_params(cls_func, endpoint_varnames),
            }
            method_config = MethodConfig(**config)
            cls_func.shared['generated_method'] = Generator.generate_method(method_config)
            cls_func.shared['method_config'] = method_config
            cls_func.__doc__ = method_config.docstring

    def __new__(cls, cls_name: str, supers: tuple, cls_dict: dict) -> type:
        """Generate new class were all fitrequest methods were generated."""

        cls_dict['method_config_list'] = cls_dict.get('method_config_list', [])

        # Generated fitrequest config
        config = FitConfig(
            class_name=cls_name,
            class_docstring=cls_dict.get('__doc__', ''),
            client_name=cls_dict.get('client_name', 'fitrequest'),
            version=cls_dict.get('version', ''),
            method_docstring=cls_dict.get('method_docstring', ''),
            base_url=cls_dict.get('base_url'),
            auth=cls_dict.get('auth'),
            method_config_list=cls_dict.get('method_config_list'),
        )

        # Handle @fit decorators
        cls.handle_fit_decorator(cls_dict)

        # Remove attributes with no meaningful purpose after the client is instantiated
        cls_dict.pop('method_docstring', None)
        cls_dict.pop('method_config_list', None)

        # Remove attributes replaced by read-only properties
        cls_dict.pop('client_name', None)
        cls_dict.pop('version', None)
        cls_dict.pop('base_url', None)
        cls_dict.pop('auth', None)

        # Create new type
        fit_attrs = (
            cls_dict
            | config.fit_methods
            | {
                '_client_name': config.client_name,
                '_version': config.version,
                '_base_url': str(config.base_url),
                '_auth': config.auth.model_dump(exclude_none=True) if config.auth else None,
            }
        )
        new_class = super().__new__(cls, cls_name, supers, fit_attrs)
        new_class.__doc__ = config.class_docstring
        return new_class
