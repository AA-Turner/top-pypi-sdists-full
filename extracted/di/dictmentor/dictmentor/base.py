"""Contains core classes."""
from typing import List, Iterable, cast, Optional, Any

from ruamel import yaml  # type: ignore

from .extensions import Extension, ExtensionContext
from .types import YamlDocument, NonAugmentedDict, AugmentedDict
from .utils import dict_find_pattern
from .validator import Validator


class DictMentor:
    """
    Augments a given dictionary by applying so called extensions.
    """

    def __init__(self, *extensions: Extension):
        self._extensions = []  # type: List[Extension]
        self._init_extensions([ext for ext in extensions])

    def _init_extensions(self, extensions: Iterable[Extension]) -> None:
        if extensions is None or not extensions:
            return

        if not Validator.is_real_iterable(extensions=extensions):
            extensions = [cast(Extension, extensions)]

        for ext in extensions:
            self.bind(ext)

    def bind(self, extension: Extension) -> 'DictMentor':
        """
        Add any predefined or custom extension.

        Args:
            extension: Extension to add to the processor.

        Returns:
            The DictMentor itself for chaining.
        """
        if not Extension.is_valid_extension(extension):
            raise ValueError("Cannot bind extension due to missing interface requirements")
        self._extensions.append(extension)

        return self

    def augment(self, dct: NonAugmentedDict,
                document: Optional[YamlDocument] = None) -> AugmentedDict:
        """
        Augments the given dictionary by using all the bound extensions.

        Args:
            dct: Dictionary to augment.
            document: The document the dictionary was loaded from.

        Returns:
            The augmented dictionary.
        """
        Validator.instance_of(dict, raise_ex=True, dct=dct)

        # Apply any configured loader
        for instance in self._extensions:
            nodes = list(dict_find_pattern(dct, **instance.config()))
            for parent, k, val in nodes:
                parent.pop(k)
                fragment = instance.apply(
                    ExtensionContext(
                        mentor=self,
                        document=document or dct,
                        dct=dct,
                        parent_node=parent,
                        node=(k, val)
                    )
                )
                if fragment is not None:
                    parent.update(fragment)

        return dct

    @classmethod
    def _load_plain_yaml(cls, _yaml: YamlDocument) -> Any:
        """
        Will just load the yaml without executing any extensions. You will get the plain dictionary
        without augmentation. It is equivalent to just perform `yaml.safe_load`. Besides that you
        can specify a stream, a file or just a string that contains yaml/json data.

        Examples:
            >>> jstr = '{"a":1, "b": {"c": 3, "d": "d"}}'
            >>> d = DictMentor._load_plain_yaml(jstr)
            >>> d['a'], d['b']['c'], d['b']['d']
            (1, 3, 'd')

        Args:
            yaml_: Whether a stream (e.g. file pointer), a file name of an existing file or string
                containing yaml/json data.

        Returns:
            Returns the yaml_ data as a python dictionary.
        """
        if Validator.is_stream(yaml_=_yaml):
            return yaml.safe_load(_yaml)
        if Validator.is_file(yaml_=_yaml):
            with open(_yaml) as fhandle:  # type: ignore
                return yaml.safe_load(fhandle)
        if Validator.instance_of(target_type=str, yaml_=_yaml):
            return yaml.safe_load(_yaml)

        raise TypeError("Argument '_yaml' is whether a stream, nor a file, nor a string")

    def load_yaml(self, _yaml: YamlDocument) -> AugmentedDict:
        """
        Loads a partial yaml and augments it. A partial yaml in this context is a yaml that is
        syntactically correct, but is not yet complete in terms of content.
        The yaml will be completed by augmenting with some external resources and/or executing so
        called extensions.

        Args:
            _yaml: Whether a stream (e.g. file pointer), a file name of an existing file or string
                containing yaml data.

        Returns:
            Returns the yaml data as an augmented python dictionary.
        """
        return self.augment(self._load_plain_yaml(_yaml), document=_yaml)
