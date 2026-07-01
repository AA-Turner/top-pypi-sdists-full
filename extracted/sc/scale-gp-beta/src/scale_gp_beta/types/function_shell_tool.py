# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .local_environment import LocalEnvironment
from .container_reference import ContainerReference
from .container_network_policy_disabled import ContainerNetworkPolicyDisabled
from .container_network_policy_allowlist import ContainerNetworkPolicyAllowlist

__all__ = [
    "FunctionShellTool",
    "Environment",
    "EnvironmentContainerAuto",
    "EnvironmentContainerAutoNetworkPolicy",
    "EnvironmentContainerAutoSkill",
    "EnvironmentContainerAutoSkillSkillReference",
    "EnvironmentContainerAutoSkillInlineSkill",
    "EnvironmentContainerAutoSkillInlineSkillSource",
]

EnvironmentContainerAutoNetworkPolicy: TypeAlias = Union[
    ContainerNetworkPolicyDisabled, ContainerNetworkPolicyAllowlist
]


class EnvironmentContainerAutoSkillSkillReference(BaseModel):
    skill_id: str

    type: Literal["skill_reference"]

    version: Optional[str] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EnvironmentContainerAutoSkillInlineSkillSource(BaseModel):
    """Inline skill payload"""

    data: str

    media_type: Literal["application/zip"]

    type: Literal["base64"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EnvironmentContainerAutoSkillInlineSkill(BaseModel):
    description: str

    name: str

    source: EnvironmentContainerAutoSkillInlineSkillSource
    """Inline skill payload"""

    type: Literal["inline"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


EnvironmentContainerAutoSkill: TypeAlias = Union[
    EnvironmentContainerAutoSkillSkillReference, EnvironmentContainerAutoSkillInlineSkill
]


class EnvironmentContainerAuto(BaseModel):
    type: Literal["container_auto"]

    file_ids: Optional[List[str]] = None

    memory_limit: Optional[Literal["1g", "4g", "16g", "64g"]] = None

    network_policy: Optional[EnvironmentContainerAutoNetworkPolicy] = None

    skills: Optional[List[EnvironmentContainerAutoSkill]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


Environment: TypeAlias = Union[EnvironmentContainerAuto, LocalEnvironment, ContainerReference]


class FunctionShellTool(BaseModel):
    """A tool that allows the model to execute shell commands."""

    type: Literal["shell"]

    environment: Optional[Environment] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
