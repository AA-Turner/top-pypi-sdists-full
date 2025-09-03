from __future__ import annotations

import json
from typing import List, Any

import betterproto

import yaml
from pydantic.v1 import root_validator, BaseModel
from pydantic_yaml import to_yaml_str


from bigeye_sdk.bigconfig_validation.validation_context import register_validation_error
from bigeye_sdk.bigconfig_validation.validation_functions import safe_split_dict_entry_lines
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import INVALID_DECLARED_ATTRIBUTE_ERRMSG, \
    NO_POSSIBLE_MATCH_ERRMSG, POSSIBLE_MATCH_ERRMSG, FORMATTING_ERRMSG, UNKNOWN_SERIALIZATION_ERROR
from bigeye_sdk.functions.search_and_match_functions import fuzzy_match

from bigeye_sdk.log import get_logger

log = get_logger(__name__)


class YamlModelWithValidatorContext(BaseModel):
    @classmethod
    def register_validation_error(cls, error_lines: List[str], error_message: str,
                                  error_context_lines: List[str] = None):
        """
        Appends a validation error to the _Validator_Context by instantiating a ValidationError.
        Args:
            error_lines: lines of the exact error
            error_context_lines: lines of the broader section of yaml containing error
            error_message: error message to log as a warning.

        Returns: None

        """
        register_validation_error(cls=cls, error_lines=error_lines,
                                  error_context_lines=error_context_lines, error_message=error_message)

    @classmethod
    def is_default_value(cls, attrib_name: str, value: Any):
        ref = cls()
        default_value = getattr(ref, attrib_name)
        return value == default_value

    def get_error_lines(self) -> List[str]:
        """
        Returns object serialized to yaml and split to lines.  Used to search files.
        Returns: List of yaml string lines.

        """
        data = self.json(exclude_unset=True, exclude_defaults=True,
                         exclude_none=True, indent=True)
        return yaml.safe_dump(json.loads(data)).splitlines()

    @root_validator(pre=True)
    def verify_all_attributes_valid(cls, values):
        expected_attribs = cls.__fields__.keys()
        unexpected_attribs = {}
        return_values = {}

        for attrib_name, attrib_value in values.items():
            if attrib_name in expected_attribs or attrib_name == 'type':
                return_values[attrib_name] = attrib_value
            else:
                unexpected_attribs[attrib_name] = attrib_value
                # The matching logic needs to be much more precise, based on how we're setting values below.
                # min_match_score was originally at 50.
                # TODO: Possible refactor. This breaks, if attribute names are too similar.
                possible_matches = fuzzy_match(search_string=attrib_name, contents=list(expected_attribs),
                                               min_match_score=80)
                if possible_matches:
                    pms = [i[1] for i in possible_matches]
                    possible_match_message = POSSIBLE_MATCH_ERRMSG.format(possible_matches=", ".join(pms))
                else:
                    possible_match_message = NO_POSSIBLE_MATCH_ERRMSG

                error_message = INVALID_DECLARED_ATTRIBUTE_ERRMSG.format(cls_name=cls.__name__, err_attrib=attrib_name,
                                                                         match_message=possible_match_message)
                errlns = safe_split_dict_entry_lines(attrib_name, attrib_value)
                cls.register_validation_error(error_lines=errlns,
                                              error_message=error_message)
                # Currently, this takes a "match" from possible_matches and sets its value to the current value
                # of the unexpected attribute that caused the else to invoke. Which breaks, if attribute names are too similar.
                # May need to refactor, along with the above.
                for err_attrib, match in possible_matches:
                    return_values[match] = attrib_value

        return return_values

    @classmethod
    def _register_invalid_type_validation_error(cls, attribute: str, attribute_value: Any, expected_type: str):
        # error_context_lines = yaml.safe_dump(values, indent=True).split('\n'),
        errlns = safe_split_dict_entry_lines(attribute, attribute_value)
        cls.register_validation_error(
            error_lines=errlns,
            error_message=FORMATTING_ERRMSG.format(
                s=f'`{attribute}` attribute expects a {expected_type} but type {attribute_value.__class__.__name__} '
                  f'was received')
        )

    @classmethod
    def _register_erroneous_attribute(cls, attribute: str, attribute_value: Any, expected_attributes: List[str]):
        possible_matches = fuzzy_match(search_string=attribute, contents=list(expected_attributes),
                                       min_match_score=50)
        if possible_matches:
            pms = [i[1] for i in possible_matches]
            possible_match_message = POSSIBLE_MATCH_ERRMSG.format(possible_matches=", ".join(pms))
        else:
            possible_match_message = NO_POSSIBLE_MATCH_ERRMSG

        error_message = INVALID_DECLARED_ATTRIBUTE_ERRMSG.format(cls_name=cls.__name__, err_attrib=attribute,
                                                                 match_message=possible_match_message)
        errlns = safe_split_dict_entry_lines(attribute, attribute_value)
        cls.register_validation_error(error_lines=errlns,
                                      error_message=error_message)

    @classmethod
    def validate_yaml(cls, values: dict):
        """
        Iterates raw inbound yaml and captures errors.
        Args:
            values: raw values as dict

        Returns: raw values as dict

        Raises: AttributeTypeException when an error exists.  Will not infer defaults.
        """
        for attribute, attribute_value in values.items():
            expected_attribs = list(cls.__fields__.keys())
            expected_attribute = cls.__fields__.get(attribute)

            if not expected_attribute:
                """unexpected attribute"""
                cls._register_erroneous_attribute(attribute=attribute, attribute_value=attribute_value,
                                                  expected_attributes=expected_attribs)
            else:
                expects_list = expected_attribute.outer_type_.__name__ == 'List' \
                               or expected_attribute.outer_type_.__name__ == 'list'
                expects_object = not expects_list and expected_attribute.is_complex()
                expected_type = expected_attribute.type_

                try:
                    if expects_list and not isinstance(attribute_value, list):
                        """Validating that we have a list when one is needed."""
                        cls._register_invalid_type_validation_error(attribute=attribute,
                                                                    attribute_value=attribute_value,
                                                                    expected_type=expected_attribute.outer_type_)
                    elif expects_object and not isinstance(attribute_value, dict):
                        cls._register_invalid_type_validation_error(attribute=attribute,
                                                                    attribute_value=attribute_value,
                                                                    expected_type=expected_attribute.outer_type_)

                    elif expects_list and isinstance(attribute_value, list):
                        """Validating that we have a list when one is needed."""
                        for i in attribute_value:
                            if (issubclass(expected_type, YamlModelWithValidatorContext)
                                or issubclass(expected_type, betterproto.Message)) and isinstance(i, dict):
                                has_error = True
                                cls._register_invalid_type_validation_error(attribute=attribute,
                                                                            attribute_value=attribute_value,
                                                                            expected_type=expected_type.__name__)
                            elif isinstance(i, dict):
                                """Lists of complex objects."""
                                expected_type(**i)
                            else:
                                "list of simple objects"
                                expected_type(i)
                    elif expects_object and isinstance(attribute_value, dict):
                        """Complex objects"""
                        expected_type(**i)
                    else:
                        expected_type(i)
                except:
                    cls.register_validation_error(error_lines=safe_split_dict_entry_lines(attribute, attribute_value),
                                                  error_message=UNKNOWN_SERIALIZATION_ERROR.format(
                                                      raw_value=attribute_value)
                                                  )

        return values
