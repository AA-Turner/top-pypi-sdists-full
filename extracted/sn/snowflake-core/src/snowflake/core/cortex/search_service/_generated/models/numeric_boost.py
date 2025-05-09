# coding: utf-8
"""
    Cortex Search REST API.

    OpenAPI 3.0 specification for the Cortex Search REST API  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Contact: support@snowflake.com
    Generated by: https://openapi-generator.tech

    Do not edit this file manually.
"""

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from typing import Union

from pydantic import BaseModel, ConfigDict, StrictFloat, StrictInt, StrictStr

from typing import Any, ClassVar, Dict, List, Optional, Union


class NumericBoost(BaseModel):
    """A model object representing the NumericBoost resource.

    Constructs an object of type NumericBoost with the provided properties.

    Parameters
    __________
    column : str
        Column to apply this function to.
    weight : float, optional
        Weight to apply for boosting this numerical column. It will be normalized across all scored columns specified in the scoring config so that all weights sum to 1. If a weight is not provided, the weight defaults to 1 pre-normalization.
    """

    column: StrictStr

    weight: Optional[Union[StrictFloat, StrictInt]] = None

    __properties = ["column", "weight"]

    class Config:
        populate_by_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias."""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> NumericBoost:
        """Create an instance of NumericBoost from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    def to_dict(
        self,
        hide_readonly_properties: bool = False,
    ) -> dict[str, Any]:
        """Returns the dictionary representation of the model using alias."""

        exclude_properties = set()

        if hide_readonly_properties:
            exclude_properties.update({})

        _dict = dict(
            self._iter(to_dict=True,
                       by_alias=True,
                       exclude=exclude_properties,
                       exclude_none=True))

        return _dict

    def to_dict_without_readonly_properties(self) -> dict[str, Any]:
        """Return the dictionary representation of the model without readonly properties."""
        return self.to_dict(hide_readonly_properties=True)

    @classmethod
    def from_dict(cls, obj: dict) -> NumericBoost:
        """Create an instance of NumericBoost from a dict."""

        if obj is None:
            return None

        if type(obj) is not dict:
            return NumericBoost.parse_obj(obj)

        _obj = NumericBoost.parse_obj({
            "column": obj.get("column"),
            "weight": obj.get("weight"),
        })

        return _obj


from typing import Optional, List, Dict


class NumericBoostModel():

    def __init__(
        self,
        column: str,
        # optional properties
        weight: Optional[float] = None,
    ):
        """A model object representing the NumericBoost resource.

        Constructs an object of type NumericBoost with the provided properties.

        Parameters
        __________
        column : str
            Column to apply this function to.
        weight : float, optional
            Weight to apply for boosting this numerical column. It will be normalized across all scored columns specified in the scoring config so that all weights sum to 1. If a weight is not provided, the weight defaults to 1 pre-normalization.
        """

        self.column = column
        self.weight = weight

    __properties = ["column", "weight"]

    def __repr__(self) -> str:
        return repr(self._to_model())

    def _to_model(self):
        return NumericBoost(
            column=self.column,
            weight=self.weight,
        )

    @classmethod
    def _from_model(cls, model) -> NumericBoostModel:
        return NumericBoostModel(
            column=model.column,
            weight=model.weight,
        )

    def to_dict(self):
        """Creates a dictionary of the properties from a NumericBoost.

        This method constructs a dictionary with the key-value entries corresponding to the properties of the NumericBoost object.

        Returns
        _______
        dict
            A dictionary object created using the input model.
        """
        return self._to_model().to_dict()

    @classmethod
    def from_dict(cls, obj: dict) -> NumericBoostModel:
        """Creates an instance of NumericBoost from a dict.

        This method constructs a NumericBoost object from a dictionary with the key-value pairs of its properties.

        Parameters
        ----------
        obj : dict
            A dictionary whose keys and values correspond to the properties of the resource object.

        Returns
        _______
        NumericBoost
            A NumericBoost object created using the input dictionary; this will fail if the required properties are missing.
        """
        return cls._from_model(NumericBoost.from_dict(obj))


NumericBoost._model_class = NumericBoostModel
