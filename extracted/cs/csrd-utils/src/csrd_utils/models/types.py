"""Type aliases for recurring patterns across the compose package."""

#: Options map used by ``PresetRef`` and ``PresetDefinition``.
OptionsMap = dict[str, str]

#: Options map for augment descriptors — supports both scalar and list values
#: (e.g. delegate targets are ``list[str]``).
AugmentOptionsMap = dict[str, str | list[str]]
