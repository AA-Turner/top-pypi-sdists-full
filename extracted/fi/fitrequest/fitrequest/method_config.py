import logging
from enum import Enum
from functools import cached_property
from typing import Any

import httpx
import jinja2
import jinja2.meta
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Self

from fitrequest.errors import (
    LIMIT_REQUEST_LINE,
    UnexpectedNoneBaseURLError,
    UrlRequestTooLongError,
)
from fitrequest.fit_var import ValidFitVar
from fitrequest.method_decorator import ValidMethodDecorator
from fitrequest.method_models import FlattenedModelSignature
from fitrequest.request_params import ValidParams
from fitrequest.response_model import ValidResponse
from fitrequest.templating import jinja_env
from fitrequest.utils import check_reserved_names, extract_method_params, format_url, string_varnames

logger = logging.getLogger(__name__)


class RequestVerb(str, Enum):
    delete = 'DELETE'
    get = 'GET'
    patch = 'PATCH'
    post = 'POST'
    put = 'PUT'


class MethodConfig(BaseModel):
    """Describes the configuration of ONE method. No the other method is declared: Explicit is better than implicit."""

    # method vars
    name: str
    """Name of the method that will be created."""

    save_method: bool = False
    """Boolean indicating if the method includes an extra argument ``filepath`` to write the response to a file."""

    async_method: bool = False
    """Boolean indicating whether the generated method is asynchronous."""

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

    request_verb: RequestVerb = RequestVerb.get
    """HTTP verb for the request, defined in the RequestVerb enumeration."""

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

    @property
    def docstring_varnames(self) -> set[str]:
        return string_varnames(jinja_env, self.docstring)

    @cached_property
    def endpoint_varnames(self) -> set[str]:
        return check_reserved_names(string_varnames(jinja_env, self.endpoint))

    @cached_property
    def params_signature(self) -> FlattenedModelSignature | None:
        return FlattenedModelSignature(model=self.params_model) if self.params_model else None

    @cached_property
    def signature(self) -> str:
        endpoint_sign = [f'{arg}: str' for arg in self.endpoint_varnames]
        request_sign = [f'raise_for_status: bool = {self.raise_for_status}', '**kwargs']
        save_sign = ['filepath: str'] if self.save_method else []
        params_sign = self.params_signature.signature if self.params_signature else []

        func_args_sign = ', '.join(['self', *endpoint_sign, *save_sign, *params_sign, *request_sign])
        return_type = 'None' if self.save_method else 'Any'
        return f'{self.name}({func_args_sign}) -> {return_type}'

    @property
    def url_template(self) -> jinja2.Template:
        return jinja_env.from_string(f'{self.base_url}/{self.endpoint}'.lstrip('/'))

    @cached_property
    def docstring_template(self) -> jinja2.Template:
        return jinja_env.from_string(self.docstring)

    @model_validator(mode='after')
    def validate_doctring(self) -> Self:
        if self.docstring_varnames:
            docstring_env = self.model_dump(exclude={'docstring_vars'}) | self.docstring_vars
            self.docstring = self.docstring_template.render(**docstring_env)
        return self

    def url(self, **kwargs) -> str:
        if self.base_url is None:
            raise UnexpectedNoneBaseURLError

        url = format_url(self.url_template.render(**kwargs))
        httpx_params = extract_method_params(httpx.request, kwargs)
        httpx_params.pop('method', None)
        httpx_params.pop('url', None)
        final_url = str(httpx.Request(method=self.request_verb, url=url, **httpx_params).url)

        if len(final_url) > LIMIT_REQUEST_LINE:
            raise UrlRequestTooLongError(final_url, len(final_url))
        return url
