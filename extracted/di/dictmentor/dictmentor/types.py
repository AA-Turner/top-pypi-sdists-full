"""Contains custom datatypes."""

from typing import Union, IO, Dict, Any, Tuple

AugmentedDict = Dict[Any, Any]


NonAugmentedDict = Dict[Any, Any]


ExtensionConfig = Dict[str, Any]


NodeKeyVal = Tuple[str, Any]


Version = str


# A valid yaml might be
# 1. a str containing yaml data
# 2. a filepath pointing to a yaml file
# 3. a stream containing yaml data
YamlDocument = Union[str, IO[bytes]]
