NAME_PARAMETER = {
    "default": None,
    "doc": "An Idem name of the resource",
    "param_type": "str",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

RESOURCE_ID_PARAMETER = {
    "default": None,
    "doc": "An identifier of the resource in the provider",
    "param_type": "str",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

OLD_TAGS_PARAMETER = {
    "default": None,
    "doc": "Dict in the format of {tag-key: tag-value}",
    "param_type": "dict",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

NEW_TAGS_PARAMETER = {
    "default": None,
    "doc": "Dict in the format of {tag-key: tag-value}",
    "param_type": "dict",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

TAGS_PARAMETER = {
    "default": None,
    "doc": """Dict in the format of {tag-key: tag-value} or List of tags in the format of [{"Key": tag-key, "Value": tag-value}] to associate with the VPC. Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode characters. May not begin with aws:.
            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256 Unicode characters.""",
    "param_type": "Dict[str, Any] or List",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

RAW_RESOURCE_PARAMETER = {
    "default": None,
    "doc": "The raw representation of the resource in the provider",
    "param_type": "dict",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}
