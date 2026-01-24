import logging
from functools import cached_property
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from fitrequest.errors import HttpVerbNotProvidedError
from fitrequest.fit_var import ValidFitVar
from fitrequest.method_config import MethodConfig, RequestVerb
from fitrequest.method_decorator import ValidMethodDecorator
from fitrequest.request_params import ValidParams
from fitrequest.response_model import ValidResponse

logger = logging.getLogger(__name__)


class FamilyTemplates(BaseModel):
    basic: str = '{verb}_{base_name}'
    save: str = '{verb}_and_save_{base_name}'
    async_basic: str = 'async_{verb}_{base_name}'
    async_save: str = 'async_{verb}_and_save_{base_name}'


class MethodConfigFamily(BaseModel):
    """
    Defines the configuration for a family of methods. Each method in the family is derived from a base name and
    specific configuration options, such as verbs, asynchronous behavior, and save functionality. The generated
    method names follow a consistent naming pattern based on these options:

    - ``{verb}_{base_name}``
    - ``{verb}_and_save_{base_name}``           (if add_save_method is True)
    - ``async_{verb}_{base_name}``              (if add_async_method is True)
    - ``async_{verb}_and_save_{base_name}``     (if both add_async_method and add_save_method are True)
    """

    # family vars
    base_name: str
    """Base name of the methods that will be created."""

    add_verbs: list[RequestVerb] = Field(default_factory=lambda: [RequestVerb.get])
    """List of HTTP verbs, one method is created per verb."""

    add_save_method: bool = False
    """Boolean indicating if a *'save'* method is created."""

    add_async_method: bool = False
    """Boolean indicating if an asynchronous is created."""

    name_templates: FamilyTemplates = Field(default_factory=FamilyTemplates)
    """
    These name templates are used to generate family names.
    Be cautious when overriding these default values with custom templates,
    as doing so - especially if the custom templates do not utilize all the requested variables for naming -
    could lead to unexpected errors.

    Override these templates with care.
    """

    # method vars
    docstring: str = ''
    """
    Jinja template for the generated method (overrides default).
    The default variable declaration ``{{my_var}}`` is replaced by ``{my_var}``.
    See: https://jinja.palletsprojects.com/en/stable/
    """

    docstring_vars: dict[Any, Any] = Field(default_factory=dict)
    """Values of the docstring variables."""

    decorators: list[ValidMethodDecorator] = Field(default_factory=list)
    """Decorators applied to the generated method."""

    # url vars
    base_url: ValidFitVar = None
    """Base URL for the generated method (overrides default)."""

    endpoint: str
    """Endpoint of the request."""

    # request vars
    raise_for_status: bool = True
    """Whether to raise an exception for response status codes between 400 and 599."""

    json_path: str | None = None
    """
    JSON path string used to extract data from the received JSON response.
    See: https://pypi.org/project/jsonpath-ng/
    """

    response_model: ValidResponse = None
    """Pydantic model used to format the request's response."""

    params_model: ValidParams = None
    """
    Use a Pydantic model or list of fields to define allowed parameters for the request URL.
    If a Pydantic model is used, parameters will be type-checked and validated.
    The URL's parameters appear as arguments in the generated method.
    Note that custom params can still be provided, but those passed directly to the method have higher priority.
    """

    model_config = ConfigDict(extra='forbid', validate_default=True)

    @field_validator('add_verbs', mode='after')
    @classmethod
    def validate_verbs(cls, value: list[RequestVerb]) -> list[RequestVerb]:
        if not value:
            raise HttpVerbNotProvidedError
        return value

    @cached_property
    def members(self) -> list[MethodConfig]:
        """Return the corresponding list of ``MethodConfig`` models."""
        methods = []
        common_params = {
            'docstring': self.docstring,
            'docstring_vars': self.docstring_vars,
            'decorators': self.decorators,
            'base_url': self.base_url,
            'endpoint': self.endpoint,
            'raise_for_status': self.raise_for_status,
            'json_path': self.json_path,
            'response_model': self.response_model,
            'params_model': self.params_model,
        }

        for verb in self.add_verbs:
            verb_name = verb.value.lower()
            methods.append(
                MethodConfig(
                    name=self.name_templates.basic.format(verb=verb_name, base_name=self.base_name),
                    request_verb=verb,
                    **common_params,
                ),
            )

            if self.add_async_method:
                methods.append(
                    MethodConfig(
                        name=self.name_templates.async_basic.format(verb=verb_name, base_name=self.base_name),
                        request_verb=verb,
                        async_method=True,
                        **common_params,
                    ),
                )

            if self.add_save_method:
                methods.append(
                    MethodConfig(
                        name=self.name_templates.save.format(verb=verb_name, base_name=self.base_name),
                        request_verb=verb,
                        save_method=True,
                        **common_params,
                    ),
                )

            if self.add_async_method and self.add_save_method:
                methods.append(
                    MethodConfig(
                        name=self.name_templates.async_save.format(verb=verb_name, base_name=self.base_name),
                        request_verb=verb,
                        async_method=True,
                        save_method=True,
                        **common_params,
                    ),
                )

        return methods
