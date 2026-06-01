try:from typing import TypedDict,NotRequired
except ImportError:from typing_extensions import TypedDict,NotRequired
class GlobalFilterConfig(TypedDict):remove_regexes:NotRequired[list[str]]
class EncryptionConfig(TypedDict):enabled:NotRequired[bool];encryption_keys_file:NotRequired[str];exclude_regexes:NotRequired[list[str]]
class ObfuscationConfig(TypedDict):exclude_regexes:NotRequired[list[str]];custom_patches:NotRequired[bool];remove_literal_statements:NotRequired[bool];remove_annotations:NotRequired[bool]
class ProtectorConfig(TypedDict):global_filter:NotRequired[GlobalFilterConfig];encryption:NotRequired[EncryptionConfig];obfuscation:NotRequired[ObfuscationConfig]