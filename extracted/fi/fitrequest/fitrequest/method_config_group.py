import logging
from importlib.metadata import PackageNotFoundError, version

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Self

from fitrequest.auth import Auth
from fitrequest.fit_var import ValidFitVar
from fitrequest.method_config import MethodConfig
from fitrequest.method_config_family import FamilyTemplates, MethodConfigFamily
from fitrequest.method_decorator import ValidMethodDecorator

logger = logging.getLogger(__name__)


class MethodConfigGroup(BaseModel):
    """Describes the configuration of a set of methods"""

    client_name: str
    """Name of the client."""

    version: str = ''
    """Version of the client. If not provided FitRequest tries to retrieve the version from the python package."""

    method_docstring: str = ''
    """
    Default Jinja template for the generated method.
    The default variable declaration ``{{my_var}}`` is replaced by ``{my_var}``.
    See: https://jinja.palletsprojects.com/en/stable/
    """

    method_decorators: list[ValidMethodDecorator] = Field(default_factory=list)
    """Default decorators applied to the generated method."""

    base_url: ValidFitVar = None
    """Default base URL for the generated method."""

    auth: Auth | None = None
    """Authentication object used by generated methods."""

    family_name_templates: FamilyTemplates | None = None
    """
    These name templates are used to generate family names.
    Be cautious when overriding these default values with custom templates,
    as doing so - especially if the custom templates do not utilize all the requested variables for naming -
    could lead to unexpected errors.

    Override these templates with care.
    """

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(default_factory=list)
    """List of ``MethodConfig`` and ``MethodConfigFamily`` objects representing the methods to be generated."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode='after')
    def update_family_templates(self) -> Self:
        """Update families with default group template."""
        if self.family_name_templates is not None:
            for family in self.method_config_list:
                if isinstance(family, MethodConfigFamily):
                    family.name_templates = self.family_name_templates

        return self

    @model_validator(mode='after')
    def validate_methods(self) -> Self:
        """
        Ensures the list contains only MethodConfig instances by expanding any
        MethodConfigFamily elements into their individual MethodConfig members.
        """
        validated_methods = []

        for item in self.method_config_list:
            if isinstance(item, MethodConfigFamily):
                validated_methods.extend(item.members)
            else:
                validated_methods.append(item)

        self.method_config_list = sorted(validated_methods, key=lambda x: x.name)
        return self

    @model_validator(mode='after')
    def update_method_vars(self) -> Self:
        """
        Update self and method_config variables with the priority below:
        1/ method_config vars
        2/ method_config_list vars
        """
        for method_config in self.method_config_list or []:
            method_config.base_url = method_config.base_url or self.base_url
            method_config.docstring = method_config.docstring or self.method_docstring
            method_config.decorators = method_config.decorators or self.method_decorators
            method_config.validate_doctring()
        return self

    @model_validator(mode='after')
    def validate_version(self) -> Self:
        if self.version:
            return self
        try:
            self.version = version(self.client_name)
        except PackageNotFoundError:
            logger.warning(
                'Cannot retrieve package version, either your package is not named '
                'as your client_name attribute, or it is not installed.',
                extra={'client_name': self.client_name},
            )
            self.version = '{version}'
        return self
