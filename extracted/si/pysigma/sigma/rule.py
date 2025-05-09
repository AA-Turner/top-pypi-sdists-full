from dataclasses import InitVar, dataclass, field
import dataclasses
from typing import Any, Dict, Optional, Tuple, Union, Sequence, List, Mapping, Type
from uuid import UUID
from enum import Enum, auto
from datetime import date, datetime
import yaml
import re
import sigma
from sigma.types import SigmaType, SigmaNull, SigmaString, SigmaNumber, sigma_type
from sigma.modifiers import (
    SigmaModifier,
    SigmaRegularExpressionModifier,
    modifier_mapping,
    reverse_modifier_mapping,
    SigmaValueModifier,
    SigmaListModifier,
)
from sigma.conditions import (
    SigmaCondition,
    ConditionAND,
    ConditionOR,
    ConditionFieldEqualsValueExpression,
    ConditionValueExpression,
    ParentChainMixin,
)
from sigma.processing.tracking import ProcessingItemTrackingMixin
import sigma.exceptions as sigma_exceptions
from sigma.exceptions import (
    SigmaRuleLocation,
    SigmaTypeError,
    SigmaError,
)


class EnumLowercaseStringMixin:
    def __str__(self) -> str:
        return self.name.lower()


class SigmaStatus(EnumLowercaseStringMixin, Enum):
    UNSUPPORTED = auto()
    DEPRECATED = auto()
    EXPERIMENTAL = auto()
    TEST = auto()
    STABLE = auto()

    def __eq__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value == other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __ge__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value >= other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __gt__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value > other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __ne__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value != other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __le__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value <= other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __lt__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value < other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __hash__(self):
        return self.value.__hash__()


class SigmaLevel(EnumLowercaseStringMixin, Enum):
    INFORMATIONAL = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

    def __eq__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value == other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __ge__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value >= other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __gt__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value > other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __ne__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value != other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __le__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value <= other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __lt__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value < other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __hash__(self):
        return self.value.__hash__()


class SigmaRelatedType(EnumLowercaseStringMixin, Enum):
    CORRELATION = auto()
    DERIVED = auto()
    MERGED = auto()
    OBSOLETE = auto()
    RENAMED = auto()
    SIMILAR = auto()


@dataclass
class SigmaRelatedItem:
    id: UUID
    type: SigmaRelatedType

    @classmethod
    def from_dict(cls, value: dict) -> "SigmaRelatedItem":
        """Returns Related item from dict with fields."""
        try:
            id = UUID(value["id"])
        except ValueError:
            raise sigma_exceptions.SigmaRelatedError(f"Sigma related identifier must be an UUID")

        try:
            type = SigmaRelatedType[value["type"].upper()]
        except:
            raise sigma_exceptions.SigmaRelatedError(
                f"{value['type']} is not a Sigma related valid type"
            )

        return cls(
            id,
            type,
        )


@dataclass
class SigmaRelated:
    related: List[Type[SigmaRelatedItem]]

    @classmethod
    def from_dict(cls, val: list) -> "SigmaRelated":
        """Returns Related object from dict with fields."""

        list_ret = []
        for v in val:
            if not "id" in v.keys():
                raise sigma_exceptions.SigmaRelatedError("Sigma related must have an id field")
            elif not "type" in v.keys():
                raise sigma_exceptions.SigmaRelatedError("Sigma related must have a type field")
            else:
                list_ret.append(SigmaRelatedItem.from_dict(v))  # should rise the SigmaRelatedError

        return cls(list_ret)


@dataclass(unsafe_hash=True)
class SigmaRuleTag:
    namespace: str
    name: str
    source: Optional[SigmaRuleLocation] = field(default=None, compare=False)

    @classmethod
    def from_str(cls, tag: str, source: Optional[SigmaRuleLocation] = None) -> "SigmaRuleTag":
        """Build SigmaRuleTag class from plain text tag string."""
        try:
            ns, n = tag.split(".", maxsplit=1)
        except ValueError:
            raise sigma_exceptions.SigmaValueError(
                "Sigma tag must start with namespace separated with dot from remaining tag."
            )
        return cls(ns, n)

    def __str__(self) -> str:
        return f"{self.namespace}.{self.name}"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return other == self.__str__()
        elif type(self) is type(other):
            return self.name == other.name and self.namespace == other.namespace


@dataclass(frozen=True)
class SigmaLogSource:
    category: Optional[str] = field(default=None)
    product: Optional[str] = field(default=None)
    service: Optional[str] = field(default=None)
    definition: Optional[str] = field(default=None)
    source: Optional[SigmaRuleLocation] = field(default=None, compare=False)
    custom_attributes: Optional[Dict[str, Any]] = field(default=None, compare=False)

    def __post_init__(self):
        """Ensures that log source is not empty."""
        if self.category is None and self.product is None and self.service is None:
            raise sigma_exceptions.SigmaLogsourceError(
                "Sigma log source can't be empty", source=self.source
            )
        if self.category and not isinstance(self.category, str):
            raise sigma_exceptions.SigmaLogsourceError(
                "Sigma log source category must be string", source=self.source
            )
        if self.product and not isinstance(self.product, str):
            raise sigma_exceptions.SigmaLogsourceError(
                "Sigma log source product must be string", source=self.source
            )
        if self.service and not isinstance(self.service, str):
            raise sigma_exceptions.SigmaLogsourceError(
                "Sigma log source service must be string", source=self.source
            )
        if self.definition and not isinstance(self.definition, str):
            raise sigma_exceptions.SigmaLogsourceError(
                "Sigma log source definition must be string", source=self.source
            )

    @classmethod
    def from_dict(
        cls, logsource: dict, source: Optional[SigmaRuleLocation] = None
    ) -> "SigmaLogSource":
        """Returns SigmaLogSource object from dict with fields."""
        custom_attributes = {
            k: v for k, v in logsource.items() if k not in set(cls.__dataclass_fields__.keys())
        }

        return cls(
            logsource.get("category"),
            logsource.get("product"),
            logsource.get("service"),
            logsource.get("definition"),
            source,
            custom_attributes if len(custom_attributes) > 0 else None,
        )

    def to_dict(self) -> dict:
        return {
            field.name: str(value)
            for field in dataclasses.fields(self)
            if (value := self.__getattribute__(field.name)) is not None
        }

    def __contains__(self, other: "SigmaLogSource") -> bool:
        """
        Matching of log source specifications. A log source contains another one if:

        * Both log sources are equal
        * The log source specifies less attributes than the other and the specified attributes are equal
        """
        if not isinstance(other, self.__class__):
            raise TypeError(
                "Containment check only allowed between log sources", source=self.source
            )

        if self == other:
            return True

        return (
            (self.category is None or self.category == other.category)
            and (self.product is None or self.product == other.product)
            and (self.service is None or self.service == other.service)
        )


@dataclass
class SigmaDetectionItem(ProcessingItemTrackingMixin, ParentChainMixin):
    """
    Single Sigma detection definition

    A detection consists of:
    * an optional field name
    * a list of value modifiers that can also be empty
    * the mandatory value or a list of values (internally it's always a list of values)

    By default all values are OR-linked but the 'all' modifier can be used to override this
    behavior.

    If the `auto_modifiers` parameter is set to False, modifiers are not automatically applied to
    the values. This shouldn't normally be used, but only in test scenarios.
    """

    field: Optional[str]  # if None, this is a keyword argument not bound to a field
    modifiers: List[Type[SigmaModifier]]
    value: List[SigmaType]
    value_linking: Union[Type[ConditionAND], Type[ConditionOR]] = ConditionOR
    source: Optional[SigmaRuleLocation] = field(default=None, compare=False)
    original_value: Optional[SigmaType] = field(
        init=False, repr=False, hash=False, compare=False
    )  # Copy of original values for conversion back to data structures (and YAML/JSON)
    auto_modifiers: InitVar[bool] = True

    def __post_init__(self, auto_modifiers):
        if not isinstance(self.value, list):  # value cleanup: it has to be a list!
            self.value = [self.value]
        self.value = [  # value cleanup: convert plain values into SigmaType's
            sigma_type(v) if not isinstance(v, SigmaType) else v for v in self.value
        ]

        self.original_value = self.value.copy()  # Create a copy of original values
        if auto_modifiers:
            self.apply_modifiers()

    def apply_modifiers(self):
        """
        Applies modifiers to detection and values
        """
        applied_modifiers = list()
        for modifier in self.modifiers:
            modifier_instance = modifier(self, applied_modifiers, self.source)
            if isinstance(
                modifier_instance, SigmaValueModifier
            ):  # Value modifiers are applied to each value separately
                self.value = [item for val in self.value for item in modifier_instance.apply(val)]
            elif isinstance(
                modifier_instance, SigmaListModifier
            ):  # List modifiers are applied to the whole value list at once
                self.value = modifier_instance.apply(self.value)
            else:  # pragma: no cover
                raise TypeError(
                    "Instance of SigmaValueModifier or SigmaListModifier was expected",
                    source=self.source,
                )  # This should only happen if wrong mapping is defined, therefore no test for this case
            applied_modifiers.append(modifier)

    @classmethod
    def from_mapping(
        cls,
        key: Optional[str],
        val: Union[
            List[Union[int, float, str]],
            Union[int, float, str],
            None,
        ],
        source: Optional[SigmaRuleLocation] = None,
    ) -> "SigmaDetectionItem":
        """
        Constructs SigmaDetectionItem object from a mapping between field name containing
        modifiers and a value. This also supports keys containing only value modifiers
        which results in a keyword detection.

        The value accepts plain values as well as lists of values and resolves them into
        the value list always contained in a SigmaDetectionItem instance.
        """
        if key is None:  # no key at all means pure keyword detection without value modifiers
            field = None
            modifier_ids = list()
        else:  # key-value detection
            field, *modifier_ids = key.split("|")
            if field == "":
                field = None

        try:
            modifiers = [modifier_mapping[mod_id] for mod_id in modifier_ids]
        except KeyError as e:
            raise sigma_exceptions.SigmaModifierError(f"Unknown modifier {str(e)}", source=source)

        if isinstance(val, (int, float, str)):  # value is plain, convert into single element list
            val = [val]
        elif val is None:
            val = [None]

        # Map Python types to Sigma typing classes
        val = [
            (
                SigmaString.from_str(v)
                if SigmaRegularExpressionModifier in modifiers
                else sigma_type(v)
            )
            for v in val
        ]

        return cls(field, modifiers, val, source=source)

    @classmethod
    def from_value(
        cls,
        val: Union[
            List[Union[int, str]],
            Union[int, str],
        ],
        source: Optional[SigmaRuleLocation] = None,
    ) -> "SigmaDetectionItem":
        """Convenience method for from_mapping(None, value)."""
        return cls.from_mapping(None, val, source=source)

    def disable_conversion_to_plain(self):
        """
        Mark detection item as not convertible to plain data type. This is required in cases where
        the value and original value get out of sync, e.g. because transformation are applied and
        conversion with to_plain() would yield an outdated state.
        """
        self.original_value = None

    def to_plain(self) -> Union[Dict[str, Union[str, int, None]], List[str]]:
        """
        Convert detection item into plain Python type, that can be:

        * a plain value if it is a single plain keyword value.
        * a list of values if it is a list of keyword values
        * a dict in all other cases (detection item bound to field or keyword with modifiers)
        """
        if self.original_value is None:
            raise sigma_exceptions.SigmaValueError(
                f"Detection item { str(self) } can't be converted to plain data type anymore because the current value is not in sync with original value anymore, e.g. by applying transformations.",
                source=self.source,
            )

        if len(self.original_value) > 1:
            value = [
                (
                    value.to_plain(True)
                    if isinstance(value, SigmaString)
                    and SigmaRegularExpressionModifier in self.modifiers
                    else value.to_plain()
                )
                for value in self.original_value
            ]
        else:
            value = (
                self.original_value[0].to_plain(True)
                if isinstance(self.original_value[0], SigmaString)
                and SigmaRegularExpressionModifier in self.modifiers
                else self.original_value[0].to_plain()
            )

        if (
            self.is_keyword() and len(self.modifiers) == 0
        ):  # detection item is keyword detection and has no modifiers: return list of values
            return value
        else:
            field_name = (
                self.field or ""
            )  # field name is empty in case of keyword detection items with modifiers
            modifier_ids = [  # list of modifier identifiers from reverse mapping
                reverse_modifier_mapping[modifier.__name__] for modifier in self.modifiers
            ]
            if len(modifier_ids) > 0:
                modifiers_prefix = "|"
            else:
                modifiers_prefix = ""
            return {field_name + modifiers_prefix + "|".join(modifier_ids): value}

    def postprocess(
        self,
        detections: "SigmaDetections",
        parent: Optional["sigma.condition.ConditionItem"] = None,
    ) -> Union[
        ConditionAND,
        ConditionOR,
        ConditionFieldEqualsValueExpression,
        ConditionValueExpression,
    ]:
        super().postprocess(detections, parent)
        if len(self.value) == 0:  # no value: map to none type
            if self.field is None:
                raise sigma_exceptions.SigmaConditionError(
                    "Null value must be bound to a field", source=self.source
                )
            else:
                return ConditionFieldEqualsValueExpression(self.field, SigmaNull()).postprocess(
                    detections, self, self.source
                )
        if len(self.value) == 1:  # single value: return key/value or value-only expression
            if self.field is None:
                return ConditionValueExpression(self.value[0]).postprocess(
                    detections, self, self.source
                )
            else:
                return ConditionFieldEqualsValueExpression(self.field, self.value[0]).postprocess(
                    detections, self, self.source
                )
        else:  # more than one value, return logically linked values or an "in" expression
            if self.field is None:  # no field - only values
                cond = self.value_linking([ConditionValueExpression(v) for v in self.value])
            else:  # with field - field/value pairs
                cond = self.value_linking(
                    [ConditionFieldEqualsValueExpression(self.field, v) for v in self.value]
                )
            cond.postprocess(detections, parent, self.source)
            return cond

    def is_keyword(self) -> bool:
        """Returns True if detection item is a keyword detection without field reference."""
        return self.field is None


@dataclass
class SigmaDetection(ParentChainMixin):
    """
    A detection is a set of atomic event definitions represented by SigmaDetectionItem instances. SigmaDetectionItems
    of a SigmaDetection are OR-linked.

    A detection can be defined by:

    1. a mapping between field/value pairs that all should appear in matched events.
    2. a plain value
    3. a list of plain values or mappings defined and matched as in 1 where at least one of the items should appear in matched events.
    """

    detection_items: List[Union[SigmaDetectionItem, "SigmaDetection"]]
    source: Optional[SigmaRuleLocation] = field(default=None, compare=False)
    item_linking: Union[Type[ConditionAND], Type[ConditionOR]] = field(default=None)

    def __post_init__(self):
        """Check detection validity."""
        if len(self.detection_items) == 0:
            raise sigma_exceptions.SigmaDetectionError("Detection is empty", source=self.source)

        if self.item_linking is None:
            type_set = {type(item) for item in self.detection_items}
            if SigmaDetectionItem in type_set:
                self.item_linking = ConditionAND
            else:
                self.item_linking = ConditionOR

    @classmethod
    def from_definition(
        cls,
        definition: Union[Mapping, Sequence, str, int],
        source: Optional[SigmaRuleLocation] = None,
    ) -> "SigmaDetection":
        """Instantiate an appropriate SigmaDetection object from a parsed Sigma detection definition."""
        if isinstance(definition, Mapping):  # key-value-definition (case 1)
            return cls(
                detection_items=[
                    SigmaDetectionItem.from_mapping(key, val, source)
                    for key, val in definition.items()
                ],
                source=source,
            )
        elif isinstance(definition, (str, int)):  # plain value (case 2)
            return cls(
                detection_items=[SigmaDetectionItem.from_value(definition, source)],
                source=source,
            )
        elif isinstance(definition, Sequence):  # list of items (case 3)
            if {type(item) for item in definition}.issubset(
                {str, int}
            ):  # list of values: create one detection item containing all values
                return cls(
                    detection_items=[SigmaDetectionItem.from_value(definition, source)],
                    source=source,
                )
            else:
                return cls(
                    detection_items=[
                        SigmaDetection.from_definition(
                            item, source
                        )  # nested SigmaDetection in other cases
                        for item in definition
                    ],
                    source=source,
                )

    def to_plain(self) -> Union[Dict[str, Union[str, int, None]], List[str]]:
        """Returns a dictionary or list representation of the detection."""
        detection_items = [  # first convert all detection items into a Python representation.
            detection_item.to_plain() for detection_item in self.detection_items
        ]
        # Filter out where to_plain() returns None, which causes merging errors.
        # We will have to handle the condition as well in conditions.py
        detection_items = [
            detection_item for detection_item in detection_items if detection_item is not None
        ]
        detection_items_types = {  # create set of types for decision what has to be returned
            type(detection_item) for detection_item in detection_items
        }

        if len(detection_items) == 0:  # pragma: no cover
            return None  # This case is caught by the post init check, so it shouldn't happen.
        if len(detection_items) == 1:  # Only one detection item? Return it as result.
            return detection_items[0]
        else:  # More than one detection item, it depends now on the types
            if dict in detection_items_types and len(detection_items_types) > 1:
                # Merging dicts with other types isn't possibly, at least not in a simple way.
                # This case can appear in a programmatically instantiated detection, but can't be
                # expressed in a data structure, because there might be only a list or a map.
                # In the future (if there's a need) a possibility would be to collect such items
                # under null or empty keys, but for today I want to keep this simple and simply bail
                # out.
                raise sigma_exceptions.SigmaValueError(
                    "Can't convert detection into plain value because it contains mixed detection item types.",
                    source=self.source,
                )
            elif detection_items_types == {dict}:  # only dict's, merge them together
                merged = dict()
                # Count key appearance for later all modifier addition
                key_count = dict()
                # The following double loop (the second one is no real one, as it operates on a
                # single element dict) merges keys (not fields!) into the merged dict.
                for detection_item_converted, detection_item in zip(
                    detection_items, self.detection_items
                ):
                    for k, v in detection_item_converted.items():
                        if k not in merged:  # key doesn't exists in merged dict: just add
                            merged[k] = v
                        else:  # key collision, now things get complicated...
                            if "|all" in k:  # key contains 'all' modifier
                                if not isinstance(
                                    merged[k], list
                                ):  # make list from existing all-modified value if it's a plain value
                                    merged[k] = [merged[k]]

                                if isinstance(v, list):  # merging two and-linked lists is possible
                                    merged[k].extend(v)
                                else:
                                    merged[k].append(v)
                            else:  # key collision without all modifier: trying to merge both keys into one and-linked key
                                ev = merged[k]  # already existing value

                                # Value normalization: extract value from single-valued lists
                                if isinstance(ev, list) and len(ev) == 1:
                                    ev = ev[0]
                                if isinstance(v, list) and len(v) == 1:
                                    v = v[0]

                                # Still lists? Merging lists is not allowed
                                if isinstance(ev, list) or isinstance(v, list):
                                    raise sigma_exceptions.SigmaValueError(
                                        f"Can't merge value lists '{k}' into one item due to different logical linking.",
                                        source=self.source,
                                    )

                                vs = [ev, v]  # The new merged value

                                ak = k + "|all"
                                if (
                                    ak in merged
                                ):  # 'all' key already exist, append to this key if possible
                                    if not isinstance(
                                        merged[ak], list
                                    ):  # ensure that existing 'all' key is a list
                                        merged[ak] = [av]
                                    av = merged[ak]
                                    av.extend(vs)
                                else:  # create new 'all' key from both existing keys
                                    merged[ak] = vs
                                del merged[k]

                return {
                    k: (v[0] if isinstance(v, list) and len(v) == 1 else v)
                    for k, v in merged.items()
                }
            else:  # only lists and plain values, merge them into one list
                merged = list()
                for detection_item_converted in detection_items:
                    if isinstance(
                        detection_item_converted, list
                    ):  # if item is a list, extend result list with it.
                        merged.extend(detection_item_converted)
                    else:
                        merged.append(
                            detection_item_converted
                        )  # if item is a plain value, append it to list
                return merged

    def postprocess(
        self,
        detections: "SigmaDetections",
        parent: Optional["sigma.condition.ConditionItem"] = None,
    ) -> Union[ConditionAND, ConditionOR]:
        """Convert detection item into condition tree element"""
        super().postprocess(detections, parent)
        items = [
            detection_item.postprocess(detections, self) for detection_item in self.detection_items
        ]
        if len(items) == 1:  # no boolean linking required, directly return single element
            return items[0]
        elif len(items) > 1:
            condition = self.item_linking(items)
            condition.postprocess(detections, parent, self.source)
            return condition

    def add_applied_processing_item(
        self, processing_item: Optional["sigma.processing.pipeline.ProcessingItem"]
    ):
        """Propagate processing item to all contained detection items."""
        for detection_item in self.detection_items:
            detection_item.add_applied_processing_item(processing_item)


@dataclass
class SigmaDetections:
    """Sigma detection section including named detections and condition."""

    detections: Dict[str, SigmaDetection]
    condition: List[str]
    source: Optional[SigmaRuleLocation] = field(default=None, compare=False)

    def __post_init__(self):
        """Detections sanity checks"""
        if self.detections == dict():
            raise sigma_exceptions.SigmaDetectionError(
                "No detections defined in Sigma rule", source=self.source
            )
        self.parsed_condition = [SigmaCondition(cond, self, self.source) for cond in self.condition]

    @classmethod
    def from_dict(
        cls, detections: dict, source: Optional[SigmaRuleLocation] = None
    ) -> "SigmaDetections":
        try:
            if isinstance(detections["condition"], list):
                condition = detections["condition"]
            else:
                condition = [detections["condition"]]
        except KeyError:
            raise sigma_exceptions.SigmaConditionError(
                "Sigma rule must contain at least one condition", source=source
            )

        return cls(
            detections={
                name: SigmaDetection.from_definition(definition, source)
                for name, definition in detections.items()
                if name not in ("condition",)
            },
            condition=condition,
            source=source,
        )

    def to_dict(self) -> dict:
        detections = {
            identifier: detection.to_plain() for identifier, detection in self.detections.items()
        }
        if len(self.condition) > 1:
            condition = self.condition
        else:
            condition = self.condition[0]

        return {
            **detections,
            "condition": condition,
        }

    def __getitem__(self, key: str) -> SigmaDetection:
        """Get detection by name"""
        return self.detections[key]


class SigmaYAMLLoader(yaml.SafeLoader):
    """Custom YAML loader implementing additional functionality for Sigma."""

    def construct_mapping(self, node, deep=...):
        keys = set()
        for k, v in node.value:
            key = self.construct_object(k, deep=deep)
            if key in keys:
                raise yaml.error.YAMLError("Duplicate key '{k}'")
            else:
                keys.add(key)

        return super().construct_mapping(node, deep)


@dataclass
class SigmaRuleBase:
    title: str = ""
    id: Optional[UUID] = None
    name: Optional[str] = None
    taxonomy: str = "sigma"
    related: Optional[SigmaRelated] = None
    status: Optional[SigmaStatus] = None
    description: Optional[str] = None
    license: Optional[str] = None
    references: List[str] = field(default_factory=list)
    tags: List[SigmaRuleTag] = field(default_factory=list)
    author: Optional[str] = None
    date: Optional["datetime.date"] = None
    modified: Optional["datetime.date"] = None
    fields: List[str] = field(default_factory=list)
    falsepositives: List[str] = field(default_factory=list)
    level: Optional[SigmaLevel] = None
    scope: Optional[List[str]] = None

    errors: List[sigma_exceptions.SigmaError] = field(default_factory=list)
    source: Optional[SigmaRuleLocation] = field(default=None, compare=False)
    custom_attributes: Dict[str, Any] = field(compare=False, default_factory=dict)

    _backreferences: List["SigmaRuleBase"] = field(
        init=False, default_factory=list, repr=False, compare=False
    )
    _conversion_result: Optional[List[Any]] = field(
        init=False, default=None, repr=False, compare=False
    )
    _conversion_states: Optional[List["sigma.conversion.state.ConversionState"]] = field(
        init=False, default=None, repr=False, compare=False
    )
    _output: bool = field(init=False, default=True, repr=False, compare=False)

    def __post_init__(self):
        for field in ("references", "tags", "fields", "falsepositives"):
            if self.__getattribute__(field) is None:
                self.__setattr__(field, [])
        if self.id is not None and not isinstance(
            self.id, UUID
        ):  # Try to convert rule id into UUID object, but keep it if not possible
            try:
                self.id = UUID(self.id)
            except ValueError:
                pass

    @classmethod
    def from_dict(
        cls,
        rule: dict,
        collect_errors: bool = False,
        source: Optional[SigmaRuleLocation] = None,
    ) -> Tuple[dict, List[Exception]]:
        """
        Convert Sigma rule base parsed in dict structure into kwargs dict that can be passed to the
        class instantiation of an object derived from the SigmaRuleBase class and the errors list.
        This is intended to be called only by to_dict() methods for processing the general
        parameters defined in the base class.

        if collect_errors is set to False exceptions are collected in the errors property of the resulting
        SigmaRule object. Else the first recognized error is raised as exception.
        """
        errors = []

        def get_rule_as_date(name: str, exception_class) -> Optional[date]:
            """
            Accepted string based date formats are in range 1000-01-01 .. 3999-12-31:
              * XXXX-XX-XX                                 -- fully corresponds to yaml date format
              * XXXX/XX/XX, XXXX/XX/X, XXXX/X/XX, XXXX/X/X -- often occurs in the US-based sigmas
            Not accepted are ambiguous dates such as:
                2024-01-1, 24-1-24, 24/1/1, ...
            """
            nonlocal errors, rule, source
            result = rule.get(name)
            if (
                result is not None
                and not isinstance(result, date)
                and not isinstance(result, datetime)
            ):
                error = True
                try:
                    result = str(result)  # forcifully convert whatever the type is into string
                    accepted_regexps = (
                        "([1-3][0-9][0-9][0-9])-([01][0-9])-([0-3][0-9])",  # 1000-01-01 .. 3999-12-31
                        "([1-3][0-9][0-9][0-9])/([01]?[0-9])/([0-3]?[0-9])",  # 1000/1/1, 1000/01/01 .. 3999/12/31
                    )
                    for date_regexp in accepted_regexps:
                        matcher = re.fullmatch(date_regexp, result)
                        if matcher:
                            result = date(int(matcher[1]), int(matcher[2]), int(matcher[3]))
                            error = False
                            break
                except Exception:
                    pass
                if error:
                    errors.append(
                        exception_class(
                            f"Rule {name} '{ result }' is invalid, use yyyy-mm-dd", source=source
                        )
                    )
            return result

        # Rule identifier may be empty or must be valid UUID
        rule_id = rule.get("id")
        if rule_id is not None:
            try:
                rule_id = UUID(rule_id)
            except ValueError:
                errors.append(
                    sigma_exceptions.SigmaIdentifierError(
                        "Sigma rule identifier must be an UUID", source=source
                    )
                )

        # Rule name
        rule_name = rule.get("name")
        if rule_name is not None:
            if not isinstance(rule_name, str):
                errors.append(
                    sigma_exceptions.SigmaTypeError(
                        "Sigma rule name must be a string", source=source
                    )
                )
            else:
                if rule_name == "":
                    errors.append(
                        sigma_exceptions.SigmaNameError(
                            "Sigma rule name must not be empty", source=source
                        )
                    )
                else:
                    rule_name = rule_name

        # Rule taxonomy
        rule_taxonomy = rule.get("taxonomy", "sigma")
        if rule_taxonomy is not None:
            if not isinstance(rule_taxonomy, str):
                errors.append(
                    sigma_exceptions.SigmaTaxonomyError(
                        "Sigma rule taxonomy must be a string", source=source
                    )
                )
            else:
                if rule_taxonomy == "":
                    errors.append(
                        sigma_exceptions.SigmaTaxonomyError(
                            "Sigma rule taxonomy must not be empty", source=source
                        )
                    )
                else:
                    rule_taxonomy = rule_taxonomy

        # Rule related validation
        rule_related = rule.get("related")
        if rule_related is not None:
            if not isinstance(rule_related, list):
                errors.append(
                    sigma_exceptions.SigmaRelatedError(
                        "Sigma rule related must be a list", source=source
                    )
                )
            else:
                try:
                    rule_related = SigmaRelated.from_dict(rule_related)
                except sigma_exceptions.SigmaRelatedError as e:
                    errors.append(e)

        # Rule level validation
        rule_level = rule.get("level")
        if rule_level is not None:
            try:
                rule_level = SigmaLevel[rule_level.upper()]
            except KeyError:
                errors.append(
                    sigma_exceptions.SigmaLevelError(
                        f"'{ rule_level }' is not a valid Sigma rule level", source=source
                    )
                )

        # Rule status validation
        rule_status = rule.get("status")
        if rule_status is not None:
            if not isinstance(rule_status, str):
                errors.append(
                    sigma_exceptions.SigmaStatusError(
                        "Sigma rule status cannot be a list", source=source
                    )
                )
            else:
                try:
                    rule_status = SigmaStatus[rule_status.upper()]
                except KeyError:
                    errors.append(
                        sigma_exceptions.SigmaStatusError(
                            f"'{ rule_status }' is not a valid Sigma rule status", source=source
                        )
                    )

        # parse rule date if existing
        rule_date = get_rule_as_date("date", sigma_exceptions.SigmaDateError)

        # parse rule modified if existing
        rule_modified = get_rule_as_date("modified", sigma_exceptions.SigmaModifiedError)

        # Rule fields validation
        rule_fields = rule.get("fields")
        if rule_fields is not None and not isinstance(rule_fields, list):
            errors.append(
                sigma_exceptions.SigmaFieldsError(
                    "Sigma rule fields must be a list",
                    source=source,
                )
            )

        # Rule falsepositives validation
        rule_falsepositives = rule.get("falsepositives")
        if rule_falsepositives is not None and not isinstance(rule_falsepositives, list):
            errors.append(
                sigma_exceptions.SigmaFalsePositivesError(
                    "Sigma rule falsepositives must be a list",
                    source=source,
                )
            )

        # Rule author validation
        rule_author = rule.get("author")
        if rule_author is not None and not isinstance(rule_author, str):
            errors.append(
                sigma_exceptions.SigmaAuthorError(
                    "Sigma rule author must be a string",
                    source=source,
                )
            )

        # Rule description validation
        rule_description = rule.get("description")
        if rule_description is not None and not isinstance(rule_description, str):
            errors.append(
                sigma_exceptions.SigmaDescriptionError(
                    "Sigma rule description must be a string",
                    source=source,
                )
            )

        # Rule references validation
        rule_references = rule.get("references")
        if rule_references is not None and not isinstance(rule_references, list):
            errors.append(
                sigma_exceptions.SigmaReferencesError(
                    "Sigma rule references must be a list",
                    source=source,
                )
            )

        # Rule title validation
        rule_title = rule.get("title")
        if rule_title is None:
            errors.append(
                sigma_exceptions.SigmaTitleError(
                    "Sigma rule must have a title",
                    source=source,
                )
            )
        elif not isinstance(rule_title, str):
            errors.append(
                sigma_exceptions.SigmaTitleError(
                    "Sigma rule title must be a string",
                    source=source,
                )
            )
        elif len(rule_title) > 256:
            errors.append(
                sigma_exceptions.SigmaTitleError(
                    "Sigma rule title length must not exceed 256 characters",
                    source=source,
                )
            )

        # Rule scope validation
        rule_scope = rule.get("scope")
        if rule_scope is not None and not isinstance(rule_scope, list):
            errors.append(
                sigma_exceptions.SigmaScopeError(
                    "Sigma rule scope must be a list",
                    source=source,
                )
            )
        # Rule license validation
        rule_license = rule.get("license")
        if rule_license is not None and not isinstance(rule_license, str):
            errors.append(
                sigma_exceptions.SigmaLicenseError(
                    "Sigma rule license must be a string",
                    source=source,
                )
            )

        if not collect_errors and errors:
            raise errors[0]

        return (
            {
                "title": rule_title,
                "id": rule_id,
                "name": rule_name,
                "taxonomy": rule_taxonomy,
                "related": rule_related,
                "level": rule_level,
                "status": rule_status,
                "description": rule_description,
                "references": rule_references,
                "tags": [SigmaRuleTag.from_str(tag) for tag in rule.get("tags", list())],
                "author": rule_author,
                "date": rule_date,
                "modified": rule_modified,
                "fields": rule_fields,
                "falsepositives": rule_falsepositives,
                "scope": rule_scope,
                "license": rule_license,
                "source": source,
                "custom_attributes": {
                    k: v
                    for k, v in rule.items()
                    if k
                    not in set(cls.__dataclass_fields__.keys())
                    - {"errors", "source", "applied_processing_items"}
                },
            },
            errors,
        )

    @classmethod
    def from_yaml(cls, rule: str, collect_errors: bool = False) -> "SigmaRule":
        """Convert YAML input string with single document into SigmaRule object."""
        parsed_rule = yaml.load(rule, SigmaYAMLLoader)
        return cls.from_dict(parsed_rule, collect_errors)

    def to_dict(self) -> dict:
        """Convert rule object into dict."""
        d = {
            "title": self.title,
        }
        # Convert to string where possible
        for field in ("id", "status", "level", "author", "description", "name"):
            if (s := self.__getattribute__(field)) is not None:
                d[field] = str(s)

        # copy list of strings
        for field in ("references", "fields", "falsepositives"):
            if len(l := self.__getattribute__(field)) > 0:
                d[field] = l.copy()

        # the special cases
        if len(self.tags) > 0:
            d["tags"] = [str(tag) for tag in self.tags]
        if self.date is not None:
            d["date"] = self.date.isoformat()
        if self.modified is not None:
            d["modified"] = self.modified.isoformat()

        # custom attributes
        d.update(self.custom_attributes)

        return d

    def add_backreference(self, rule: "SigmaRuleBase"):
        """Add backreference to another rule."""
        self._backreferences.append(rule)

    def referenced_by(self, rule: "SigmaRuleBase") -> bool:
        """Check if rule is referenced by another rule."""
        return rule in self._backreferences

    def set_conversion_result(self, result: List[Any]):
        """Set conversion result."""
        self._conversion_result = result

    def get_conversion_result(self) -> List[Any]:
        """Get conversion result."""
        if self._conversion_result is None:
            raise sigma_exceptions.SigmaConversionError(
                self,
                "Conversion result not available",
            )
        return self._conversion_result

    def set_conversion_states(self, state: List["sigma.conversion.state.ConversionState"]):
        """Set conversion state."""
        self._conversion_states = state

    def get_conversion_states(self) -> List["sigma.conversion.state.ConversionState"]:
        """Get conversion state."""
        if self._conversion_states is None:
            raise sigma_exceptions.SigmaConversionError(
                self,
                "Conversion state not available",
            )
        return self._conversion_states

    def disable_output(self):
        """Disable output of rule."""
        self._output = False

    def __lt__(self, other: "SigmaRuleBase") -> bool:
        """Sort rules by backreference. A rule referenced by another rule is smaller."""
        return self.referenced_by(other)


@dataclass
class SigmaRule(SigmaRuleBase, ProcessingItemTrackingMixin):
    """
    A single Sigma rule.
    """

    logsource: SigmaLogSource = field(default_factory=SigmaLogSource)
    detection: SigmaDetections = field(default_factory=SigmaDetections)

    @classmethod
    def from_dict(
        cls,
        rule: dict,
        collect_errors: bool = False,
        source: Optional[SigmaRuleLocation] = None,
    ) -> "SigmaRule":
        """
        Convert Sigma rule parsed in dict structure into SigmaRule object.

        if collect_errors is set to False exceptions are collected in the errors property of the resulting
        SigmaRule object. Else the first recognized error is raised as exception.
        """
        kwargs, errors = super().from_dict(rule, collect_errors, source)

        # parse log source
        logsource = None
        try:
            logsource = SigmaLogSource.from_dict(rule["logsource"], source)
        except KeyError:
            errors.append(
                sigma_exceptions.SigmaLogsourceError(
                    "Sigma rule must have a log source", source=source
                )
            )
        except AttributeError:
            errors.append(
                sigma_exceptions.SigmaLogsourceError(
                    "Sigma logsource must be a valid YAML map", source=source
                )
            )
        except SigmaError as e:
            errors.append(e)

        # parse detections
        detections = None
        try:
            detections = SigmaDetections.from_dict(rule["detection"], source)
        except KeyError:
            errors.append(
                sigma_exceptions.SigmaDetectionError(
                    "Sigma rule must have a detection definitions", source=source
                )
            )
        except SigmaError as e:
            errors.append(e)

        if not collect_errors and errors:
            raise errors[0]

        return cls(
            logsource=logsource,
            detection=detections,
            errors=errors,
            **kwargs,
        )

    def to_dict(self) -> dict:
        """Convert rule object into dict."""
        d = super().to_dict()
        d.update(
            {
                "logsource": self.logsource.to_dict(),
                "detection": self.detection.to_dict(),
            }
        )

        return d
