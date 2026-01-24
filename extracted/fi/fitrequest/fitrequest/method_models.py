from functools import cached_property
from typing import Any, Literal

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from fitrequest.errors import MissingRequiredArgumentError
from fitrequest.utils import is_basemodel_subclass

#: Global dictionnary used to map ``json/yaml`` declared models to actual python models.
environment_models = {}


class AttrSignature(BaseModel):
    """Represents the signature of the attribute."""

    name: str
    annotation: str
    alias: str | None = None
    attr_type: Literal['arg', 'kwarg']
    default_value: str | None = None

    @property
    def signature(self) -> str:
        """
        Dumps flattened signature of the attribute.
        These names are intended for use in the method signature and will not include any aliases.
        """
        if self.attr_type == 'arg':
            return f'{self.name}: {self.annotation}'
        return f'{self.name}: {self.annotation} = {self.default_value}'

    @property
    def param_name(self) -> str:
        """Return the name used in the request params."""
        return self.alias or self.name


class FlattenedModelSignature(BaseModel):
    """
    Represents flattened model signatures, simplifying nested Pydantic models into straightforward method signatures.

    This class flattens model structures to create simple signatures that are easy to handle with command-line tools.
    However, it has limitations: it does not support complex signatures
    involving unions (``Model | dict | None``) or lists (``list[Model]``).
    """

    model: type[BaseModel]

    def nested_signatures(self, prefix: str, alias_prefix: str) -> list[AttrSignature]:
        """
        Update the names of attributes by appending the specified `prefix`,
        indicating this model represents a nested structure within another model.
        """
        for attr_sign in (signatures := self.attr_signatures):
            attr_sign.alias = f'{alias_prefix}_{attr_sign.param_name}'
            attr_sign.name = f'{prefix}_{attr_sign.name}'

            if attr_sign.alias == attr_sign.name:
                attr_sign.alias = None

        return signatures

    @property
    def params_varnames(self) -> set[str]:
        """
        Return the names of all flattened attributes.
        These names are intended for the `params` field of the `httpx` request.
        When provided, they will use the alias instead of the attribute name.
        """
        return {attr.param_name for attr in self.attr_signatures}

    @cached_property
    def signature_varnames(self) -> set[str]:
        """
        Return the names of all flattened attributes.
        These names are intended for the generated method signature, where aliases are ignored.
        """
        return {attr.name for attr in self.attr_signatures}

    def alias_of(self, attr_name: str) -> str:
        """Return the alias for the specified attribute name. If no alias is found, return the original name."""
        return self.attr_signatures_dict[attr_name].alias or attr_name

    def value_of(self, attr_name: str, value: Any) -> Any:
        """
        If the provided value type is ``FieldInfo``, return the value generated from that class,
        which is configured using either the ``default`` or ``default_factory`` field.
        """
        if isinstance(value, FieldInfo):
            if value.is_required():
                raise MissingRequiredArgumentError(attr_name)

            return value.get_default(call_default_factory=True)

        return value

    @cached_property
    def attr_signatures_dict(self) -> dict[str, AttrSignature]:
        """Similar to attr_signatures, but organized in a dictionary where the keys are the attribute names."""
        return {attr.name: attr for attr in self.attr_signatures}

    @cached_property
    def attr_signatures(self) -> list[AttrSignature]:
        """
        Creates a flattened representation of the model's attributes suitable for fitrequest method signatures.
        The returned list is ordered with positional arguments (args) first, followed by keyword arguments (kwargs),
        following Python method signature conventions.
        If use_alias is enabled, the Pydantic alias specified in ``Field(alias=<alias>)``
        will be used instead of the attribute name.
        """

        attr_signature_list = []

        for field, info in self.model.model_fields.items():
            # Get nested pydantic model signature (reccursive)
            if is_basemodel_subclass(info.annotation):
                nested_model = FlattenedModelSignature(model=info.annotation)
                attr_signature_list.extend(nested_model.nested_signatures(field, info.alias or field))
                continue

            # Get orther types signature
            if 'class' in (field_type := str(info.annotation)):
                field_type = info.annotation.__qualname__

            if not info.is_required():
                default_value = info.get_default(call_default_factory=True)
                attr_signature_list.append(
                    AttrSignature(
                        name=field,
                        alias=info.alias,
                        annotation=field_type,
                        attr_type='kwarg',
                        default_value=repr(default_value),
                    )
                )
            else:
                attr_signature_list.append(
                    AttrSignature(name=field, alias=info.alias, annotation=field_type, attr_type='arg')
                )

        # Sort all positional parameters first followed by keyword parameters.
        args_signature_list = filter(lambda x: x.attr_type == 'arg', attr_signature_list)
        kwargs_signature_list = filter(lambda x: x.attr_type == 'kwarg', attr_signature_list)
        return [
            *sorted(args_signature_list, key=lambda x: x.name),
            *sorted(kwargs_signature_list, key=lambda x: x.name),
        ]

    @cached_property
    def signature(self) -> list[str]:
        """
        Returns a flattened list of signatures for all attributes of the model.
        These names are intended for use in the method signature and will not include any aliases.
        """
        return [attr_sign.signature for attr_sign in self.attr_signatures]
