from datetime import date, datetime
from typing import Dict, Optional, Union, Literal, List, Any
from uuid import UUID
from maleo_foundation.enums import BaseEnums

class BaseTypes:
    #* Any-related types
    ListOfAny = List[Any]
    OptionalAny = Optional[Any]

    #* Boolean-related types
    LiteralFalse = Literal[False]
    LiteralTrue = Literal[True]
    ListOfBools = List[bool]
    OptionalBoolean = Optional[bool]

    #* Float-related types
    ListOfFloats = List[float]
    OptionalFloat = Optional[float]
    OptionalListOfFloats = Optional[List[float]]

    #* Integer-related types
    ListOfIntegers = List[int]
    OptionalInteger = Optional[int]
    OptionalListOfIntegers = Optional[List[int]]

    #* String-related types
    ListOfStrings = List[str]
    OptionalString = Optional[str]
    OptionalListOfStrings = Optional[List[str]]

    #* Date-related types
    OptionalDate = Optional[date]

    #* Datetime-related types
    OptionalDatetime = Optional[datetime]

    #* Any Dict-related types
    StringToAnyDict = Dict[str, Any]
    OptionalStringToAnyDict = Optional[Dict[str, Any]]
    ListOfStringToAnyDict = List[Dict[str, Any]]
    OptionalListOfStringToAnyDict = Optional[List[Dict[str, Any]]]
    IntToAnyDict = Dict[int, Any]
    OptionalIntToAnyDict = Optional[Dict[int, Any]]
    ListOfIntToAnyDict = List[Dict[int, Any]]
    OptionalListOfIntToAnyDict = Optional[List[Dict[int, Any]]]

    #* String Dict-related types
    StringToStringDict = Dict[str, str]
    OptionalStringToStringDict = Optional[Dict[str, str]]
    ListOfStringToStringDict = List[Dict[str, str]]
    OptionalListOfStringToStringDict = Optional[List[Dict[str, str]]]
    IntToStringDict = Dict[int, str]
    OptionalIntToStringDict = Optional[Dict[int, str]]
    ListOfIntToStringDict = List[Dict[int, str]]
    OptionalListOfIntToStringDict = Optional[List[Dict[int, str]]]

    #* List Dict-related types
    StringToListOfStringDict = Dict[str, List[str]]
    OptionalStringToListOfStringDict = Optional[Dict[str, List[str]]]

    #* UUID-related types
    ListOfUUIDs = List[UUID]
    OptionalUUID = Optional[UUID]
    OptionalListOfUUIDs = Optional[List[UUID]]

    #* Statuses-related types
    ListOfStatuses = List[BaseEnums.StatusType]
    OptionalListOfStatuses = Optional[List[BaseEnums.StatusType]]

    #* Miscellanous types
    IdentifierValue = Union[int, UUID, str]
    ListOrDictOfAny = Union[List[Any], Dict[str, Any]]