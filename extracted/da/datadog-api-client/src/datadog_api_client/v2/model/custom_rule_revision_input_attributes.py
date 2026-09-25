# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    datetime,
    none_type,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.argument import Argument
    from datadog_api_client.v2.model.custom_rule_revision_attributes_category import (
        CustomRuleRevisionAttributesCategory,
    )
    from datadog_api_client.v2.model.language import Language
    from datadog_api_client.v2.model.custom_rule_revision_attributes_severity import (
        CustomRuleRevisionAttributesSeverity,
    )
    from datadog_api_client.v2.model.custom_rule_revision_test import CustomRuleRevisionTest


class CustomRuleRevisionInputAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.argument import Argument
        from datadog_api_client.v2.model.custom_rule_revision_attributes_category import (
            CustomRuleRevisionAttributesCategory,
        )
        from datadog_api_client.v2.model.language import Language
        from datadog_api_client.v2.model.custom_rule_revision_attributes_severity import (
            CustomRuleRevisionAttributesSeverity,
        )
        from datadog_api_client.v2.model.custom_rule_revision_test import CustomRuleRevisionTest

        return {
            "arguments": ([Argument], none_type),
            "category": (CustomRuleRevisionAttributesCategory,),
            "checksum": (str,),
            "code": (str,),
            "created_at": (datetime,),
            "created_by": (str,),
            "creation_message": (str,),
            "cve": (str, none_type),
            "cwe": (str, none_type),
            "description": (str,),
            "documentation_url": (str, none_type),
            "is_published": (bool,),
            "is_testing": (bool,),
            "language": (Language,),
            "severity": (CustomRuleRevisionAttributesSeverity,),
            "short_description": (str,),
            "should_use_ai_fix": (bool,),
            "tags": ([str], none_type),
            "tests": ([CustomRuleRevisionTest], none_type),
            "tree_sitter_query": (str,),
            "version_id": (int,),
        }

    attribute_map = {
        "arguments": "arguments",
        "category": "category",
        "checksum": "checksum",
        "code": "code",
        "created_at": "created_at",
        "created_by": "created_by",
        "creation_message": "creation_message",
        "cve": "cve",
        "cwe": "cwe",
        "description": "description",
        "documentation_url": "documentation_url",
        "is_published": "is_published",
        "is_testing": "is_testing",
        "language": "language",
        "severity": "severity",
        "short_description": "short_description",
        "should_use_ai_fix": "should_use_ai_fix",
        "tags": "tags",
        "tests": "tests",
        "tree_sitter_query": "tree_sitter_query",
        "version_id": "version_id",
    }
    read_only_vars = {
        "checksum",
        "created_at",
        "created_by",
        "version_id",
    }

    def __init__(
        self_,
        arguments: Union[List[Argument], none_type],
        category: CustomRuleRevisionAttributesCategory,
        code: str,
        creation_message: str,
        description: str,
        is_published: bool,
        is_testing: bool,
        language: Language,
        severity: CustomRuleRevisionAttributesSeverity,
        short_description: str,
        should_use_ai_fix: bool,
        tags: Union[List[str], none_type],
        tests: Union[List[CustomRuleRevisionTest], none_type],
        tree_sitter_query: str,
        checksum: Union[str, UnsetType] = unset,
        created_at: Union[datetime, UnsetType] = unset,
        created_by: Union[str, UnsetType] = unset,
        cve: Union[str, none_type, UnsetType] = unset,
        cwe: Union[str, none_type, UnsetType] = unset,
        documentation_url: Union[str, none_type, UnsetType] = unset,
        version_id: Union[int, UnsetType] = unset,
        **kwargs,
    ):
        """
        Input attributes for creating or updating a custom rule revision.

        :param arguments: Rule arguments
        :type arguments: [Argument], none_type

        :param category: Rule category
        :type category: CustomRuleRevisionAttributesCategory

        :param checksum: Code checksum. Derived by the API from ``code`` ; ignored on write.
        :type checksum: str, optional

        :param code: Rule code
        :type code: str

        :param created_at: Creation timestamp. Set by the API; ignored on write.
        :type created_at: datetime, optional

        :param created_by: Creator identifier. Set by the API from the caller; ignored on write.
        :type created_by: str, optional

        :param creation_message: Revision creation message
        :type creation_message: str

        :param cve: Associated CVE
        :type cve: str, none_type, optional

        :param cwe: Associated CWE
        :type cwe: str, none_type, optional

        :param description: Full description
        :type description: str

        :param documentation_url: Documentation URL
        :type documentation_url: str, none_type, optional

        :param is_published: Whether the revision is published
        :type is_published: bool

        :param is_testing: Whether this is a testing revision
        :type is_testing: bool

        :param language: Programming language
        :type language: Language

        :param severity: Rule severity
        :type severity: CustomRuleRevisionAttributesSeverity

        :param short_description: Short description
        :type short_description: str

        :param should_use_ai_fix: Whether to use AI for fixes
        :type should_use_ai_fix: bool

        :param tags: Rule tags
        :type tags: [str], none_type

        :param tests: Rule tests
        :type tests: [CustomRuleRevisionTest], none_type

        :param tree_sitter_query: Tree-sitter query
        :type tree_sitter_query: str

        :param version_id: Monotonically increasing version number of the revision. Assigned by the API; ignored on write.
        :type version_id: int, optional
        """
        if checksum is not unset:
            kwargs["checksum"] = checksum
        if created_at is not unset:
            kwargs["created_at"] = created_at
        if created_by is not unset:
            kwargs["created_by"] = created_by
        if cve is not unset:
            kwargs["cve"] = cve
        if cwe is not unset:
            kwargs["cwe"] = cwe
        if documentation_url is not unset:
            kwargs["documentation_url"] = documentation_url
        if version_id is not unset:
            kwargs["version_id"] = version_id
        super().__init__(kwargs)

        self_.arguments = arguments
        self_.category = category
        self_.code = code
        self_.creation_message = creation_message
        self_.description = description
        self_.is_published = is_published
        self_.is_testing = is_testing
        self_.language = language
        self_.severity = severity
        self_.short_description = short_description
        self_.should_use_ai_fix = should_use_ai_fix
        self_.tags = tags
        self_.tests = tests
        self_.tree_sitter_query = tree_sitter_query
