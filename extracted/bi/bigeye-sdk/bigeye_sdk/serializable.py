from __future__ import annotations

import abc
import json
import os
from dataclasses import asdict
from typing import TypeVar

import yaml
from pydantic.v1.dataclasses import dataclass
from pydantic.v1.json import pydantic_encoder

from bigeye_sdk.bigconfig_validation.validation_context import put_bigeye_yaml_file_to_ix, process_validation_errors, \
    get_validation_error_cnt, get_file_error_match_cnt
from bigeye_sdk.bigconfig_validation.validation_functions import safe_dump_dict
from bigeye_sdk.bigconfig_validation.yaml_model_base import YamlModelWithValidatorContext
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import INVALID_OBJECT_TYPE_ERRMSG, \
    POSSIBLE_MATCH_ERRMSG, NO_POSSIBLE_MATCH_ERRMSG, INVALID_OBJECT_ERRMSG
from bigeye_sdk.exceptions.exceptions import FileLoadException
from bigeye_sdk.functions.search_and_match_functions import fuzzy_match
from bigeye_sdk.log import get_logger

log = get_logger(__name__)

VALID_SUBTYPE = TypeVar('VALID_SUBTYPE', bound='PydanticSubtypeSerializable')


def contains_same_attributes(obj: dict, clazz: type(VALID_SUBTYPE)) -> bool:
    """
    Validates that all keys in dict are defined fields in the pydantic subtype class.
    Args:
        obj: an inbound dictionary.
        clazz: the pydantic subtype class to validate against.
    Returns: true if all keys in dictionary are defined fields in the pydantic subtype.  Further validation occurs
    during the instantiation of the class.
    """
    all_valid_attributes: bool = True
    attributes = clazz.__fields__.keys()
    for key in obj.keys():
        all_valid_attributes = all_valid_attributes and key in attributes

    return all_valid_attributes


class PydanticSubtypeSerializable(YamlModelWithValidatorContext):
    _subtypes_ = dict()
    type: str

    def __init_subclass__(cls, type=None):
        cls._subtypes_[type or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_real_type_

    @classmethod
    def _get_type_by_attribute(cls, data):
        for clazz in cls.__subclasses__():
            if contains_same_attributes(data, clazz):
                return clazz

        errlns = safe_dump_dict(data)
        errmessage = INVALID_OBJECT_ERRMSG.format(cls=cls.__name__, object=data)
        cls.register_validation_error(error_lines=errlns, error_message=errmessage)

    @classmethod
    def _convert_to_real_type_(cls, data):
        sub = None
        data_type: str = ""

        if issubclass(type(data), cls):
            """Failover if we receive an instance of an actual subclass"""
            return data
        elif isinstance(data, dict) and "type" in data:
            """Supporting backwards compatibility with object type declaration."""
            data_type = data.get("type")
            sub = cls._subtypes_.get(data_type)
        elif isinstance(data, dict) and "type" not in data:
            """supporting instances where no type is declared in raw object."""
            sub = cls._get_type_by_attribute(data)

        if sub:
            return sub(**data)
        else:
            errln = safe_dump_dict(data)

            if data_type:
                possible_matches = fuzzy_match(data_type, list(cls._subtypes_.keys()), 50)

                if possible_matches:
                    pms = [i[1] for i in possible_matches]
                    possible_match_message = POSSIBLE_MATCH_ERRMSG.format(possible_matches=", ".join(pms))
                else:
                    possible_match_message = NO_POSSIBLE_MATCH_ERRMSG
                PydanticSubtypeSerializable.register_validation_error(
                    error_lines=errln,
                    error_message=INVALID_OBJECT_TYPE_ERRMSG.format(data_type=data_type,
                                                                    match_message=possible_match_message)
                )
                if possible_matches:
                    data['type'] = possible_matches[0]

            return data

    @classmethod
    def parse_obj(cls, obj) -> FILE:
        return cls._convert_to_real_type_(obj)


FILE = TypeVar('FILE', bound='File')


class File(PydanticSubtypeSerializable):
    _exclude_defaults: bool = False


    def __str__(self):
        data = self.json(exclude_unset=True, exclude_none=True, indent=True)
        return yaml.safe_dump(json.loads(data),
                              default_flow_style=False, sort_keys=False)

    @classmethod
    def load(cls, file_name: str) -> FILE:

        log.info(f"Loading file: {file_name}")

        with open(file_name, 'r') as fin:
            data = yaml.safe_load(fin)

        try:
            if "type" in data:
                data_type = data.get("type")
                sub = cls._subtypes_.get(data_type)
                if not sub:
                    valid_types = {k: f"for class {v.__name__}" for k, v in cls._subtypes_.items() if
                                   k.endswith("_FILE")}
                    raise FileLoadException(
                        f"File type: {data_type} is not a valid type. Valid types are: {valid_types}")
                instance = sub(**data)
                put_bigeye_yaml_file_to_ix(file_name=file_name)
                return instance
            else:
                raise FileLoadException(
                    "File requires a type attribute. Try adding 'type: <VALID_FILE_TYPE>' to the file.")

        except Exception as e:
            """Processing validation errors if any exist and throw exception."""
            errmsg = f"{e.__class__.__name__}: \n{str(e)}"
            put_bigeye_yaml_file_to_ix(file_name=file_name)
            fixme_file_list = process_validation_errors()
            if get_file_error_match_cnt():
                log.info('Generating FixMe files.')
                errmsg = f'File is invalid.  File: {file_name};' \
                         f"\nErrors: \n{errmsg};" \
                         f'\nFIXME Files: {yaml.safe_dump(fixme_file_list)}'

            raise FileLoadException(errmsg)


    def save(self, output_path: str, default_file_name: str = None, custom_formatter=None) -> str:
        if os.path.isfile(output_path):
            output_path = output_path
        elif os.path.isdir(output_path):
            output_path = f'{output_path}/{default_file_name}.yml'

        with open(output_path, 'w') as fout:
            if custom_formatter:
                fout.writelines(custom_formatter(str(self)))
            else:
                fout.writelines(str(self))

        return output_path


BIGCONFIG_FILE = TypeVar('BIGCONFIG_FILE', bound='BigConfigFile')


class BigConfigFile(File):
    pass


@dataclass
class YamlSerializable(abc.ABC):
    @classmethod
    def load_from_file(cls, file: str):
        print(f'load_from_file class name: {cls.__name__}')
        with open(file, 'r') as fin:
            d = yaml.safe_load(fin)
            bsc = cls(**d)
            if bsc is None:
                raise Exception('Could not load from disk.')
            log.info(f'Loaded instance of {bsc.__class__.__name__} from disk: {file}')
            return bsc

    def to_dict(self, exclude_empty: bool = True):
        return asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v and exclude_empty})

    def save_to_file(self, file: str):
        j = json.dumps(self.to_dict(), indent=True, default=pydantic_encoder, sort_keys=False)
        d = json.loads(j)
        with open(file, 'w') as file:
            yaml.dump(d, file, sort_keys=False)
