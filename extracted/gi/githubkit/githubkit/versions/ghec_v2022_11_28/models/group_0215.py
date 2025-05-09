"""DO NOT EDIT THIS FILE!

This file is automatically @generated by githubkit using the follow command:

bash ./scripts/run-codegen.sh

See https://github.com/github/rest-api-description for more information.
"""

from __future__ import annotations

from typing import Union

from pydantic import Field

from githubkit.compat import GitHubModel, model_rebuild


class CustomPropertyValue(GitHubModel):
    """Custom Property Value

    Custom property name and associated value
    """

    property_name: str = Field(description="The name of the property")
    value: Union[str, list[str], None] = Field(
        description="The value assigned to the property"
    )


model_rebuild(CustomPropertyValue)

__all__ = ("CustomPropertyValue",)
