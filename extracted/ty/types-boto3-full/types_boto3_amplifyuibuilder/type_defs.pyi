"""
Type annotations for amplifyuibuilder service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_amplifyuibuilder.type_defs import GraphQLRenderConfigTypeDef

    data: GraphQLRenderConfigTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Union

from .literals import (
    CodegenGenericDataFieldDataTypeType,
    CodegenJobStatusType,
    FormActionTypeType,
    FormButtonsPositionType,
    FormDataSourceTypeType,
    GenericDataRelationshipTypeType,
    JSModuleType,
    JSScriptType,
    JSTargetType,
    LabelDecoratorType,
    SortDirectionType,
    StorageAccessLevelType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActionParametersOutputTypeDef",
    "ActionParametersPaginatorTypeDef",
    "ActionParametersTypeDef",
    "ActionParametersUnionTypeDef",
    "ApiConfigurationOutputTypeDef",
    "ApiConfigurationTypeDef",
    "ApiConfigurationUnionTypeDef",
    "CodegenDependencyTypeDef",
    "CodegenFeatureFlagsTypeDef",
    "CodegenGenericDataEnumOutputTypeDef",
    "CodegenGenericDataEnumTypeDef",
    "CodegenGenericDataEnumUnionTypeDef",
    "CodegenGenericDataFieldOutputTypeDef",
    "CodegenGenericDataFieldTypeDef",
    "CodegenGenericDataFieldUnionTypeDef",
    "CodegenGenericDataModelOutputTypeDef",
    "CodegenGenericDataModelTypeDef",
    "CodegenGenericDataModelUnionTypeDef",
    "CodegenGenericDataNonModelOutputTypeDef",
    "CodegenGenericDataNonModelTypeDef",
    "CodegenGenericDataNonModelUnionTypeDef",
    "CodegenGenericDataRelationshipTypeOutputTypeDef",
    "CodegenGenericDataRelationshipTypeTypeDef",
    "CodegenGenericDataRelationshipTypeUnionTypeDef",
    "CodegenJobAssetTypeDef",
    "CodegenJobGenericDataSchemaOutputTypeDef",
    "CodegenJobGenericDataSchemaTypeDef",
    "CodegenJobGenericDataSchemaUnionTypeDef",
    "CodegenJobRenderConfigOutputTypeDef",
    "CodegenJobRenderConfigTypeDef",
    "CodegenJobRenderConfigUnionTypeDef",
    "CodegenJobSummaryTypeDef",
    "CodegenJobTypeDef",
    "ComponentBindingPropertiesValueOutputTypeDef",
    "ComponentBindingPropertiesValuePaginatorTypeDef",
    "ComponentBindingPropertiesValuePropertiesOutputTypeDef",
    "ComponentBindingPropertiesValuePropertiesPaginatorTypeDef",
    "ComponentBindingPropertiesValuePropertiesTypeDef",
    "ComponentBindingPropertiesValuePropertiesUnionTypeDef",
    "ComponentBindingPropertiesValueTypeDef",
    "ComponentBindingPropertiesValueUnionTypeDef",
    "ComponentChildOutputTypeDef",
    "ComponentChildPaginatorTypeDef",
    "ComponentChildTypeDef",
    "ComponentChildUnionTypeDef",
    "ComponentConditionPropertyOutputTypeDef",
    "ComponentConditionPropertyPaginatorTypeDef",
    "ComponentConditionPropertyTypeDef",
    "ComponentConditionPropertyUnionTypeDef",
    "ComponentDataConfigurationOutputTypeDef",
    "ComponentDataConfigurationPaginatorTypeDef",
    "ComponentDataConfigurationTypeDef",
    "ComponentDataConfigurationUnionTypeDef",
    "ComponentEventOutputTypeDef",
    "ComponentEventPaginatorTypeDef",
    "ComponentEventTypeDef",
    "ComponentEventUnionTypeDef",
    "ComponentPaginatorTypeDef",
    "ComponentPropertyBindingPropertiesTypeDef",
    "ComponentPropertyOutputTypeDef",
    "ComponentPropertyPaginatorTypeDef",
    "ComponentPropertyTypeDef",
    "ComponentPropertyUnionTypeDef",
    "ComponentSummaryTypeDef",
    "ComponentTypeDef",
    "ComponentVariantOutputTypeDef",
    "ComponentVariantTypeDef",
    "ComponentVariantUnionTypeDef",
    "CreateComponentDataTypeDef",
    "CreateComponentRequestTypeDef",
    "CreateComponentResponseTypeDef",
    "CreateFormDataTypeDef",
    "CreateFormRequestTypeDef",
    "CreateFormResponseTypeDef",
    "CreateThemeDataTypeDef",
    "CreateThemeRequestTypeDef",
    "CreateThemeResponseTypeDef",
    "DeleteComponentRequestTypeDef",
    "DeleteFormRequestTypeDef",
    "DeleteThemeRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExchangeCodeForTokenRequestBodyTypeDef",
    "ExchangeCodeForTokenRequestTypeDef",
    "ExchangeCodeForTokenResponseTypeDef",
    "ExportComponentsRequestPaginateTypeDef",
    "ExportComponentsRequestTypeDef",
    "ExportComponentsResponsePaginatorTypeDef",
    "ExportComponentsResponseTypeDef",
    "ExportFormsRequestPaginateTypeDef",
    "ExportFormsRequestTypeDef",
    "ExportFormsResponsePaginatorTypeDef",
    "ExportFormsResponseTypeDef",
    "ExportThemesRequestPaginateTypeDef",
    "ExportThemesRequestTypeDef",
    "ExportThemesResponsePaginatorTypeDef",
    "ExportThemesResponseTypeDef",
    "FieldConfigOutputTypeDef",
    "FieldConfigPaginatorTypeDef",
    "FieldConfigTypeDef",
    "FieldConfigUnionTypeDef",
    "FieldInputConfigOutputTypeDef",
    "FieldInputConfigPaginatorTypeDef",
    "FieldInputConfigTypeDef",
    "FieldInputConfigUnionTypeDef",
    "FieldPositionTypeDef",
    "FieldValidationConfigurationOutputTypeDef",
    "FieldValidationConfigurationTypeDef",
    "FieldValidationConfigurationUnionTypeDef",
    "FileUploaderFieldConfigOutputTypeDef",
    "FileUploaderFieldConfigTypeDef",
    "FileUploaderFieldConfigUnionTypeDef",
    "FormBindingElementTypeDef",
    "FormButtonTypeDef",
    "FormCTATypeDef",
    "FormDataTypeConfigTypeDef",
    "FormInputBindingPropertiesValuePropertiesTypeDef",
    "FormInputBindingPropertiesValueTypeDef",
    "FormInputValuePropertyBindingPropertiesTypeDef",
    "FormInputValuePropertyOutputTypeDef",
    "FormInputValuePropertyPaginatorTypeDef",
    "FormInputValuePropertyTypeDef",
    "FormInputValuePropertyUnionTypeDef",
    "FormPaginatorTypeDef",
    "FormStyleConfigTypeDef",
    "FormStyleTypeDef",
    "FormSummaryTypeDef",
    "FormTypeDef",
    "GetCodegenJobRequestTypeDef",
    "GetCodegenJobResponseTypeDef",
    "GetComponentRequestTypeDef",
    "GetComponentResponseTypeDef",
    "GetFormRequestTypeDef",
    "GetFormResponseTypeDef",
    "GetMetadataRequestTypeDef",
    "GetMetadataResponseTypeDef",
    "GetThemeRequestTypeDef",
    "GetThemeResponseTypeDef",
    "GraphQLRenderConfigTypeDef",
    "ListCodegenJobsRequestPaginateTypeDef",
    "ListCodegenJobsRequestTypeDef",
    "ListCodegenJobsResponseTypeDef",
    "ListComponentsRequestPaginateTypeDef",
    "ListComponentsRequestTypeDef",
    "ListComponentsResponseTypeDef",
    "ListFormsRequestPaginateTypeDef",
    "ListFormsRequestTypeDef",
    "ListFormsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListThemesRequestPaginateTypeDef",
    "ListThemesRequestTypeDef",
    "ListThemesResponseTypeDef",
    "MutationActionSetStateParameterOutputTypeDef",
    "MutationActionSetStateParameterPaginatorTypeDef",
    "MutationActionSetStateParameterTypeDef",
    "MutationActionSetStateParameterUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PredicateOutputTypeDef",
    "PredicatePaginatorTypeDef",
    "PredicateTypeDef",
    "PredicateUnionTypeDef",
    "PutMetadataFlagBodyTypeDef",
    "PutMetadataFlagRequestTypeDef",
    "ReactStartCodegenJobDataOutputTypeDef",
    "ReactStartCodegenJobDataTypeDef",
    "ReactStartCodegenJobDataUnionTypeDef",
    "RefreshTokenRequestBodyTypeDef",
    "RefreshTokenRequestTypeDef",
    "RefreshTokenResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SectionalElementTypeDef",
    "SortPropertyTypeDef",
    "StartCodegenJobDataTypeDef",
    "StartCodegenJobRequestTypeDef",
    "StartCodegenJobResponseTypeDef",
    "TagResourceRequestTypeDef",
    "ThemePaginatorTypeDef",
    "ThemeSummaryTypeDef",
    "ThemeTypeDef",
    "ThemeValueOutputTypeDef",
    "ThemeValuePaginatorTypeDef",
    "ThemeValueTypeDef",
    "ThemeValueUnionTypeDef",
    "ThemeValuesOutputTypeDef",
    "ThemeValuesPaginatorTypeDef",
    "ThemeValuesTypeDef",
    "ThemeValuesUnionTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateComponentDataTypeDef",
    "UpdateComponentRequestTypeDef",
    "UpdateComponentResponseTypeDef",
    "UpdateFormDataTypeDef",
    "UpdateFormRequestTypeDef",
    "UpdateFormResponseTypeDef",
    "UpdateThemeDataTypeDef",
    "UpdateThemeRequestTypeDef",
    "UpdateThemeResponseTypeDef",
    "ValueMappingOutputTypeDef",
    "ValueMappingPaginatorTypeDef",
    "ValueMappingTypeDef",
    "ValueMappingUnionTypeDef",
    "ValueMappingsOutputTypeDef",
    "ValueMappingsPaginatorTypeDef",
    "ValueMappingsTypeDef",
    "ValueMappingsUnionTypeDef",
)

class GraphQLRenderConfigTypeDef(TypedDict):
    typesFilePath: str
    queriesFilePath: str
    mutationsFilePath: str
    subscriptionsFilePath: str
    fragmentsFilePath: str

class CodegenDependencyTypeDef(TypedDict):
    name: NotRequired[str]
    supportedVersion: NotRequired[str]
    isSemVer: NotRequired[bool]
    reason: NotRequired[str]

class CodegenFeatureFlagsTypeDef(TypedDict):
    isRelationshipSupported: NotRequired[bool]
    isNonModelSupported: NotRequired[bool]

class CodegenGenericDataEnumOutputTypeDef(TypedDict):
    values: List[str]

class CodegenGenericDataEnumTypeDef(TypedDict):
    values: Sequence[str]

CodegenGenericDataRelationshipTypeOutputTypeDef = TypedDict(
    "CodegenGenericDataRelationshipTypeOutputTypeDef",
    {
        "type": GenericDataRelationshipTypeType,
        "relatedModelName": str,
        "relatedModelFields": NotRequired[List[str]],
        "canUnlinkAssociatedModel": NotRequired[bool],
        "relatedJoinFieldName": NotRequired[str],
        "relatedJoinTableName": NotRequired[str],
        "belongsToFieldOnRelatedModel": NotRequired[str],
        "associatedFields": NotRequired[List[str]],
        "isHasManyIndex": NotRequired[bool],
    },
)
CodegenGenericDataRelationshipTypeTypeDef = TypedDict(
    "CodegenGenericDataRelationshipTypeTypeDef",
    {
        "type": GenericDataRelationshipTypeType,
        "relatedModelName": str,
        "relatedModelFields": NotRequired[Sequence[str]],
        "canUnlinkAssociatedModel": NotRequired[bool],
        "relatedJoinFieldName": NotRequired[str],
        "relatedJoinTableName": NotRequired[str],
        "belongsToFieldOnRelatedModel": NotRequired[str],
        "associatedFields": NotRequired[Sequence[str]],
        "isHasManyIndex": NotRequired[bool],
    },
)

class CodegenJobAssetTypeDef(TypedDict):
    downloadUrl: NotRequired[str]

CodegenJobSummaryTypeDef = TypedDict(
    "CodegenJobSummaryTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "createdAt": NotRequired[datetime],
        "modifiedAt": NotRequired[datetime],
    },
)
PredicateOutputTypeDef = TypedDict(
    "PredicateOutputTypeDef",
    {
        "or": NotRequired[List[Dict[str, Any]]],
        "and": NotRequired[List[Dict[str, Any]]],
        "field": NotRequired[str],
        "operator": NotRequired[str],
        "operand": NotRequired[str],
        "operandType": NotRequired[str],
    },
)
PredicatePaginatorTypeDef = TypedDict(
    "PredicatePaginatorTypeDef",
    {
        "or": NotRequired[List[Dict[str, Any]]],
        "and": NotRequired[List[Dict[str, Any]]],
        "field": NotRequired[str],
        "operator": NotRequired[str],
        "operand": NotRequired[str],
        "operandType": NotRequired[str],
    },
)
ComponentConditionPropertyOutputTypeDef = TypedDict(
    "ComponentConditionPropertyOutputTypeDef",
    {
        "property": NotRequired[str],
        "field": NotRequired[str],
        "operator": NotRequired[str],
        "operand": NotRequired[str],
        "then": NotRequired[Dict[str, Any]],
        "else": NotRequired[Dict[str, Any]],
        "operandType": NotRequired[str],
    },
)
ComponentConditionPropertyPaginatorTypeDef = TypedDict(
    "ComponentConditionPropertyPaginatorTypeDef",
    {
        "property": NotRequired[str],
        "field": NotRequired[str],
        "operator": NotRequired[str],
        "operand": NotRequired[str],
        "then": NotRequired[Dict[str, Any]],
        "else": NotRequired[Dict[str, Any]],
        "operandType": NotRequired[str],
    },
)
ComponentConditionPropertyTypeDef = TypedDict(
    "ComponentConditionPropertyTypeDef",
    {
        "property": NotRequired[str],
        "field": NotRequired[str],
        "operator": NotRequired[str],
        "operand": NotRequired[str],
        "then": NotRequired[Mapping[str, Any]],
        "else": NotRequired[Mapping[str, Any]],
        "operandType": NotRequired[str],
    },
)

class SortPropertyTypeDef(TypedDict):
    field: str
    direction: SortDirectionType

class ComponentVariantOutputTypeDef(TypedDict):
    variantValues: NotRequired[Dict[str, str]]
    overrides: NotRequired[Dict[str, Dict[str, str]]]

ComponentPropertyBindingPropertiesTypeDef = TypedDict(
    "ComponentPropertyBindingPropertiesTypeDef",
    {
        "property": str,
        "field": NotRequired[str],
    },
)
FormBindingElementTypeDef = TypedDict(
    "FormBindingElementTypeDef",
    {
        "element": str,
        "property": str,
    },
)
ComponentSummaryTypeDef = TypedDict(
    "ComponentSummaryTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
        "componentType": str,
    },
)

class ComponentVariantTypeDef(TypedDict):
    variantValues: NotRequired[Mapping[str, str]]
    overrides: NotRequired[Mapping[str, Mapping[str, str]]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class FormDataTypeConfigTypeDef(TypedDict):
    dataSourceType: FormDataSourceTypeType
    dataTypeName: str

DeleteComponentRequestTypeDef = TypedDict(
    "DeleteComponentRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)
DeleteFormRequestTypeDef = TypedDict(
    "DeleteFormRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)
DeleteThemeRequestTypeDef = TypedDict(
    "DeleteThemeRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)

class ExchangeCodeForTokenRequestBodyTypeDef(TypedDict):
    code: str
    redirectUri: str
    clientId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ExportComponentsRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    nextToken: NotRequired[str]

class ExportFormsRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    nextToken: NotRequired[str]

class ExportThemesRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    nextToken: NotRequired[str]

class FieldPositionTypeDef(TypedDict):
    fixed: NotRequired[Literal["first"]]
    rightOf: NotRequired[str]
    below: NotRequired[str]

FieldValidationConfigurationOutputTypeDef = TypedDict(
    "FieldValidationConfigurationOutputTypeDef",
    {
        "type": str,
        "strValues": NotRequired[List[str]],
        "numValues": NotRequired[List[int]],
        "validationMessage": NotRequired[str],
    },
)

class FileUploaderFieldConfigOutputTypeDef(TypedDict):
    accessLevel: StorageAccessLevelType
    acceptedFileTypes: List[str]
    showThumbnails: NotRequired[bool]
    isResumable: NotRequired[bool]
    maxFileCount: NotRequired[int]
    maxSize: NotRequired[int]

FieldValidationConfigurationTypeDef = TypedDict(
    "FieldValidationConfigurationTypeDef",
    {
        "type": str,
        "strValues": NotRequired[Sequence[str]],
        "numValues": NotRequired[Sequence[int]],
        "validationMessage": NotRequired[str],
    },
)

class FileUploaderFieldConfigTypeDef(TypedDict):
    accessLevel: StorageAccessLevelType
    acceptedFileTypes: Sequence[str]
    showThumbnails: NotRequired[bool]
    isResumable: NotRequired[bool]
    maxFileCount: NotRequired[int]
    maxSize: NotRequired[int]

class FormInputBindingPropertiesValuePropertiesTypeDef(TypedDict):
    model: NotRequired[str]

FormInputValuePropertyBindingPropertiesTypeDef = TypedDict(
    "FormInputValuePropertyBindingPropertiesTypeDef",
    {
        "property": str,
        "field": NotRequired[str],
    },
)

class FormStyleConfigTypeDef(TypedDict):
    tokenReference: NotRequired[str]
    value: NotRequired[str]

GetCodegenJobRequestTypeDef = TypedDict(
    "GetCodegenJobRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)
GetComponentRequestTypeDef = TypedDict(
    "GetComponentRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)
GetFormRequestTypeDef = TypedDict(
    "GetFormRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)

class GetMetadataRequestTypeDef(TypedDict):
    appId: str
    environmentName: str

GetThemeRequestTypeDef = TypedDict(
    "GetThemeRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
    },
)

class ListCodegenJobsRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListComponentsRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListFormsRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class ListThemesRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ThemeSummaryTypeDef = TypedDict(
    "ThemeSummaryTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
    },
)
PredicateTypeDef = TypedDict(
    "PredicateTypeDef",
    {
        "or": NotRequired[Sequence[Mapping[str, Any]]],
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "field": NotRequired[str],
        "operator": NotRequired[str],
        "operand": NotRequired[str],
        "operandType": NotRequired[str],
    },
)

class PutMetadataFlagBodyTypeDef(TypedDict):
    newValue: str

class RefreshTokenRequestBodyTypeDef(TypedDict):
    token: str
    clientId: NotRequired[str]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class ThemeValueOutputTypeDef(TypedDict):
    value: NotRequired[str]
    children: NotRequired[List[Dict[str, Any]]]

class ThemeValuePaginatorTypeDef(TypedDict):
    value: NotRequired[str]
    children: NotRequired[List[Dict[str, Any]]]

class ThemeValueTypeDef(TypedDict):
    value: NotRequired[str]
    children: NotRequired[Sequence[Mapping[str, Any]]]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class ApiConfigurationOutputTypeDef(TypedDict):
    graphQLConfig: NotRequired[GraphQLRenderConfigTypeDef]
    dataStoreConfig: NotRequired[Dict[str, Any]]
    noApiConfig: NotRequired[Dict[str, Any]]

class ApiConfigurationTypeDef(TypedDict):
    graphQLConfig: NotRequired[GraphQLRenderConfigTypeDef]
    dataStoreConfig: NotRequired[Mapping[str, Any]]
    noApiConfig: NotRequired[Mapping[str, Any]]

CodegenGenericDataEnumUnionTypeDef = Union[
    CodegenGenericDataEnumTypeDef, CodegenGenericDataEnumOutputTypeDef
]

class CodegenGenericDataFieldOutputTypeDef(TypedDict):
    dataType: CodegenGenericDataFieldDataTypeType
    dataTypeValue: str
    required: bool
    readOnly: bool
    isArray: bool
    relationship: NotRequired[CodegenGenericDataRelationshipTypeOutputTypeDef]

CodegenGenericDataRelationshipTypeUnionTypeDef = Union[
    CodegenGenericDataRelationshipTypeTypeDef, CodegenGenericDataRelationshipTypeOutputTypeDef
]

class ComponentBindingPropertiesValuePropertiesOutputTypeDef(TypedDict):
    model: NotRequired[str]
    field: NotRequired[str]
    predicates: NotRequired[List[PredicateOutputTypeDef]]
    userAttribute: NotRequired[str]
    bucket: NotRequired[str]
    key: NotRequired[str]
    defaultValue: NotRequired[str]
    slotName: NotRequired[str]

class ComponentBindingPropertiesValuePropertiesPaginatorTypeDef(TypedDict):
    model: NotRequired[str]
    field: NotRequired[str]
    predicates: NotRequired[List[PredicatePaginatorTypeDef]]
    userAttribute: NotRequired[str]
    bucket: NotRequired[str]
    key: NotRequired[str]
    defaultValue: NotRequired[str]
    slotName: NotRequired[str]

ComponentConditionPropertyUnionTypeDef = Union[
    ComponentConditionPropertyTypeDef, ComponentConditionPropertyOutputTypeDef
]

class ComponentDataConfigurationOutputTypeDef(TypedDict):
    model: str
    sort: NotRequired[List[SortPropertyTypeDef]]
    predicate: NotRequired[PredicateOutputTypeDef]
    identifiers: NotRequired[List[str]]

class ComponentDataConfigurationPaginatorTypeDef(TypedDict):
    model: str
    sort: NotRequired[List[SortPropertyTypeDef]]
    predicate: NotRequired[PredicatePaginatorTypeDef]
    identifiers: NotRequired[List[str]]

ComponentPropertyOutputTypeDef = TypedDict(
    "ComponentPropertyOutputTypeDef",
    {
        "value": NotRequired[str],
        "bindingProperties": NotRequired[ComponentPropertyBindingPropertiesTypeDef],
        "collectionBindingProperties": NotRequired[ComponentPropertyBindingPropertiesTypeDef],
        "defaultValue": NotRequired[str],
        "model": NotRequired[str],
        "bindings": NotRequired[Dict[str, FormBindingElementTypeDef]],
        "event": NotRequired[str],
        "userAttribute": NotRequired[str],
        "concat": NotRequired[List[Dict[str, Any]]],
        "condition": NotRequired[ComponentConditionPropertyOutputTypeDef],
        "configured": NotRequired[bool],
        "type": NotRequired[str],
        "importedValue": NotRequired[str],
        "componentName": NotRequired[str],
        "property": NotRequired[str],
    },
)
ComponentPropertyPaginatorTypeDef = TypedDict(
    "ComponentPropertyPaginatorTypeDef",
    {
        "value": NotRequired[str],
        "bindingProperties": NotRequired[ComponentPropertyBindingPropertiesTypeDef],
        "collectionBindingProperties": NotRequired[ComponentPropertyBindingPropertiesTypeDef],
        "defaultValue": NotRequired[str],
        "model": NotRequired[str],
        "bindings": NotRequired[Dict[str, FormBindingElementTypeDef]],
        "event": NotRequired[str],
        "userAttribute": NotRequired[str],
        "concat": NotRequired[List[Dict[str, Any]]],
        "condition": NotRequired[ComponentConditionPropertyPaginatorTypeDef],
        "configured": NotRequired[bool],
        "type": NotRequired[str],
        "importedValue": NotRequired[str],
        "componentName": NotRequired[str],
        "property": NotRequired[str],
    },
)
ComponentVariantUnionTypeDef = Union[ComponentVariantTypeDef, ComponentVariantOutputTypeDef]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ExchangeCodeForTokenResponseTypeDef(TypedDict):
    accessToken: str
    expiresIn: int
    refreshToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetMetadataResponseTypeDef(TypedDict):
    features: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListCodegenJobsResponseTypeDef(TypedDict):
    entities: List[CodegenJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListComponentsResponseTypeDef(TypedDict):
    entities: List[ComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RefreshTokenResponseTypeDef(TypedDict):
    accessToken: str
    expiresIn: int
    ResponseMetadata: ResponseMetadataTypeDef

FormSummaryTypeDef = TypedDict(
    "FormSummaryTypeDef",
    {
        "appId": str,
        "dataType": FormDataTypeConfigTypeDef,
        "environmentName": str,
        "formActionType": FormActionTypeType,
        "id": str,
        "name": str,
    },
)

class ExchangeCodeForTokenRequestTypeDef(TypedDict):
    provider: Literal["figma"]
    request: ExchangeCodeForTokenRequestBodyTypeDef

class ExportComponentsRequestPaginateTypeDef(TypedDict):
    appId: str
    environmentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ExportFormsRequestPaginateTypeDef(TypedDict):
    appId: str
    environmentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ExportThemesRequestPaginateTypeDef(TypedDict):
    appId: str
    environmentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCodegenJobsRequestPaginateTypeDef(TypedDict):
    appId: str
    environmentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComponentsRequestPaginateTypeDef(TypedDict):
    appId: str
    environmentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFormsRequestPaginateTypeDef(TypedDict):
    appId: str
    environmentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListThemesRequestPaginateTypeDef(TypedDict):
    appId: str
    environmentName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class FormButtonTypeDef(TypedDict):
    excluded: NotRequired[bool]
    children: NotRequired[str]
    position: NotRequired[FieldPositionTypeDef]

SectionalElementTypeDef = TypedDict(
    "SectionalElementTypeDef",
    {
        "type": str,
        "position": NotRequired[FieldPositionTypeDef],
        "text": NotRequired[str],
        "level": NotRequired[int],
        "orientation": NotRequired[str],
        "excluded": NotRequired[bool],
    },
)
FieldValidationConfigurationUnionTypeDef = Union[
    FieldValidationConfigurationTypeDef, FieldValidationConfigurationOutputTypeDef
]
FileUploaderFieldConfigUnionTypeDef = Union[
    FileUploaderFieldConfigTypeDef, FileUploaderFieldConfigOutputTypeDef
]
FormInputBindingPropertiesValueTypeDef = TypedDict(
    "FormInputBindingPropertiesValueTypeDef",
    {
        "type": NotRequired[str],
        "bindingProperties": NotRequired[FormInputBindingPropertiesValuePropertiesTypeDef],
    },
)

class FormInputValuePropertyOutputTypeDef(TypedDict):
    value: NotRequired[str]
    bindingProperties: NotRequired[FormInputValuePropertyBindingPropertiesTypeDef]
    concat: NotRequired[List[Dict[str, Any]]]

class FormInputValuePropertyPaginatorTypeDef(TypedDict):
    value: NotRequired[str]
    bindingProperties: NotRequired[FormInputValuePropertyBindingPropertiesTypeDef]
    concat: NotRequired[List[Dict[str, Any]]]

class FormInputValuePropertyTypeDef(TypedDict):
    value: NotRequired[str]
    bindingProperties: NotRequired[FormInputValuePropertyBindingPropertiesTypeDef]
    concat: NotRequired[Sequence[Mapping[str, Any]]]

class FormStyleTypeDef(TypedDict):
    horizontalGap: NotRequired[FormStyleConfigTypeDef]
    verticalGap: NotRequired[FormStyleConfigTypeDef]
    outerPadding: NotRequired[FormStyleConfigTypeDef]

class ListThemesResponseTypeDef(TypedDict):
    entities: List[ThemeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

PredicateUnionTypeDef = Union[PredicateTypeDef, PredicateOutputTypeDef]

class PutMetadataFlagRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    featureName: str
    body: PutMetadataFlagBodyTypeDef

class RefreshTokenRequestTypeDef(TypedDict):
    provider: Literal["figma"]
    refreshTokenBody: RefreshTokenRequestBodyTypeDef

class ThemeValuesOutputTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[ThemeValueOutputTypeDef]

class ThemeValuesPaginatorTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[ThemeValuePaginatorTypeDef]

ThemeValueUnionTypeDef = Union[ThemeValueTypeDef, ThemeValueOutputTypeDef]

class ReactStartCodegenJobDataOutputTypeDef(TypedDict):
    module: NotRequired[JSModuleType]
    target: NotRequired[JSTargetType]
    script: NotRequired[JSScriptType]
    renderTypeDeclarations: NotRequired[bool]
    inlineSourceMap: NotRequired[bool]
    apiConfiguration: NotRequired[ApiConfigurationOutputTypeDef]
    dependencies: NotRequired[Dict[str, str]]

ApiConfigurationUnionTypeDef = Union[ApiConfigurationTypeDef, ApiConfigurationOutputTypeDef]

class CodegenGenericDataModelOutputTypeDef(TypedDict):
    fields: Dict[str, CodegenGenericDataFieldOutputTypeDef]
    primaryKeys: List[str]
    isJoinTable: NotRequired[bool]

class CodegenGenericDataNonModelOutputTypeDef(TypedDict):
    fields: Dict[str, CodegenGenericDataFieldOutputTypeDef]

class CodegenGenericDataFieldTypeDef(TypedDict):
    dataType: CodegenGenericDataFieldDataTypeType
    dataTypeValue: str
    required: bool
    readOnly: bool
    isArray: bool
    relationship: NotRequired[CodegenGenericDataRelationshipTypeUnionTypeDef]

ComponentBindingPropertiesValueOutputTypeDef = TypedDict(
    "ComponentBindingPropertiesValueOutputTypeDef",
    {
        "type": NotRequired[str],
        "bindingProperties": NotRequired[ComponentBindingPropertiesValuePropertiesOutputTypeDef],
        "defaultValue": NotRequired[str],
    },
)
ComponentBindingPropertiesValuePaginatorTypeDef = TypedDict(
    "ComponentBindingPropertiesValuePaginatorTypeDef",
    {
        "type": NotRequired[str],
        "bindingProperties": NotRequired[ComponentBindingPropertiesValuePropertiesPaginatorTypeDef],
        "defaultValue": NotRequired[str],
    },
)
ComponentPropertyTypeDef = TypedDict(
    "ComponentPropertyTypeDef",
    {
        "value": NotRequired[str],
        "bindingProperties": NotRequired[ComponentPropertyBindingPropertiesTypeDef],
        "collectionBindingProperties": NotRequired[ComponentPropertyBindingPropertiesTypeDef],
        "defaultValue": NotRequired[str],
        "model": NotRequired[str],
        "bindings": NotRequired[Mapping[str, FormBindingElementTypeDef]],
        "event": NotRequired[str],
        "userAttribute": NotRequired[str],
        "concat": NotRequired[Sequence[Mapping[str, Any]]],
        "condition": NotRequired[ComponentConditionPropertyUnionTypeDef],
        "configured": NotRequired[bool],
        "type": NotRequired[str],
        "importedValue": NotRequired[str],
        "componentName": NotRequired[str],
        "property": NotRequired[str],
    },
)
MutationActionSetStateParameterOutputTypeDef = TypedDict(
    "MutationActionSetStateParameterOutputTypeDef",
    {
        "componentName": str,
        "property": str,
        "set": ComponentPropertyOutputTypeDef,
    },
)
MutationActionSetStateParameterPaginatorTypeDef = TypedDict(
    "MutationActionSetStateParameterPaginatorTypeDef",
    {
        "componentName": str,
        "property": str,
        "set": ComponentPropertyPaginatorTypeDef,
    },
)

class ListFormsResponseTypeDef(TypedDict):
    entities: List[FormSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FormCTATypeDef(TypedDict):
    position: NotRequired[FormButtonsPositionType]
    clear: NotRequired[FormButtonTypeDef]
    cancel: NotRequired[FormButtonTypeDef]
    submit: NotRequired[FormButtonTypeDef]

class ValueMappingOutputTypeDef(TypedDict):
    value: FormInputValuePropertyOutputTypeDef
    displayValue: NotRequired[FormInputValuePropertyOutputTypeDef]

class ValueMappingPaginatorTypeDef(TypedDict):
    value: FormInputValuePropertyPaginatorTypeDef
    displayValue: NotRequired[FormInputValuePropertyPaginatorTypeDef]

FormInputValuePropertyUnionTypeDef = Union[
    FormInputValuePropertyTypeDef, FormInputValuePropertyOutputTypeDef
]

class ComponentBindingPropertiesValuePropertiesTypeDef(TypedDict):
    model: NotRequired[str]
    field: NotRequired[str]
    predicates: NotRequired[Sequence[PredicateUnionTypeDef]]
    userAttribute: NotRequired[str]
    bucket: NotRequired[str]
    key: NotRequired[str]
    defaultValue: NotRequired[str]
    slotName: NotRequired[str]

class ComponentDataConfigurationTypeDef(TypedDict):
    model: str
    sort: NotRequired[Sequence[SortPropertyTypeDef]]
    predicate: NotRequired[PredicateUnionTypeDef]
    identifiers: NotRequired[Sequence[str]]

ThemeTypeDef = TypedDict(
    "ThemeTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
        "createdAt": datetime,
        "values": List[ThemeValuesOutputTypeDef],
        "modifiedAt": NotRequired[datetime],
        "overrides": NotRequired[List[ThemeValuesOutputTypeDef]],
        "tags": NotRequired[Dict[str, str]],
    },
)
ThemePaginatorTypeDef = TypedDict(
    "ThemePaginatorTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
        "createdAt": datetime,
        "values": List[ThemeValuesPaginatorTypeDef],
        "modifiedAt": NotRequired[datetime],
        "overrides": NotRequired[List[ThemeValuesPaginatorTypeDef]],
        "tags": NotRequired[Dict[str, str]],
    },
)

class ThemeValuesTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[ThemeValueUnionTypeDef]

class CodegenJobRenderConfigOutputTypeDef(TypedDict):
    react: NotRequired[ReactStartCodegenJobDataOutputTypeDef]

class ReactStartCodegenJobDataTypeDef(TypedDict):
    module: NotRequired[JSModuleType]
    target: NotRequired[JSTargetType]
    script: NotRequired[JSScriptType]
    renderTypeDeclarations: NotRequired[bool]
    inlineSourceMap: NotRequired[bool]
    apiConfiguration: NotRequired[ApiConfigurationUnionTypeDef]
    dependencies: NotRequired[Mapping[str, str]]

class CodegenJobGenericDataSchemaOutputTypeDef(TypedDict):
    dataSourceType: Literal["DataStore"]
    models: Dict[str, CodegenGenericDataModelOutputTypeDef]
    enums: Dict[str, CodegenGenericDataEnumOutputTypeDef]
    nonModels: Dict[str, CodegenGenericDataNonModelOutputTypeDef]

CodegenGenericDataFieldUnionTypeDef = Union[
    CodegenGenericDataFieldTypeDef, CodegenGenericDataFieldOutputTypeDef
]

class CodegenGenericDataModelTypeDef(TypedDict):
    fields: Mapping[str, CodegenGenericDataFieldTypeDef]
    primaryKeys: Sequence[str]
    isJoinTable: NotRequired[bool]

ComponentPropertyUnionTypeDef = Union[ComponentPropertyTypeDef, ComponentPropertyOutputTypeDef]
ActionParametersOutputTypeDef = TypedDict(
    "ActionParametersOutputTypeDef",
    {
        "type": NotRequired[ComponentPropertyOutputTypeDef],
        "url": NotRequired[ComponentPropertyOutputTypeDef],
        "anchor": NotRequired[ComponentPropertyOutputTypeDef],
        "target": NotRequired[ComponentPropertyOutputTypeDef],
        "global": NotRequired[ComponentPropertyOutputTypeDef],
        "model": NotRequired[str],
        "id": NotRequired[ComponentPropertyOutputTypeDef],
        "fields": NotRequired[Dict[str, ComponentPropertyOutputTypeDef]],
        "state": NotRequired[MutationActionSetStateParameterOutputTypeDef],
    },
)
ActionParametersPaginatorTypeDef = TypedDict(
    "ActionParametersPaginatorTypeDef",
    {
        "type": NotRequired[ComponentPropertyPaginatorTypeDef],
        "url": NotRequired[ComponentPropertyPaginatorTypeDef],
        "anchor": NotRequired[ComponentPropertyPaginatorTypeDef],
        "target": NotRequired[ComponentPropertyPaginatorTypeDef],
        "global": NotRequired[ComponentPropertyPaginatorTypeDef],
        "model": NotRequired[str],
        "id": NotRequired[ComponentPropertyPaginatorTypeDef],
        "fields": NotRequired[Dict[str, ComponentPropertyPaginatorTypeDef]],
        "state": NotRequired[MutationActionSetStateParameterPaginatorTypeDef],
    },
)

class ValueMappingsOutputTypeDef(TypedDict):
    values: List[ValueMappingOutputTypeDef]
    bindingProperties: NotRequired[Dict[str, FormInputBindingPropertiesValueTypeDef]]

class ValueMappingsPaginatorTypeDef(TypedDict):
    values: List[ValueMappingPaginatorTypeDef]
    bindingProperties: NotRequired[Dict[str, FormInputBindingPropertiesValueTypeDef]]

class ValueMappingTypeDef(TypedDict):
    value: FormInputValuePropertyUnionTypeDef
    displayValue: NotRequired[FormInputValuePropertyUnionTypeDef]

ComponentBindingPropertiesValuePropertiesUnionTypeDef = Union[
    ComponentBindingPropertiesValuePropertiesTypeDef,
    ComponentBindingPropertiesValuePropertiesOutputTypeDef,
]
ComponentDataConfigurationUnionTypeDef = Union[
    ComponentDataConfigurationTypeDef, ComponentDataConfigurationOutputTypeDef
]

class CreateThemeResponseTypeDef(TypedDict):
    entity: ThemeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportThemesResponseTypeDef(TypedDict):
    entities: List[ThemeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetThemeResponseTypeDef(TypedDict):
    theme: ThemeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateThemeResponseTypeDef(TypedDict):
    entity: ThemeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportThemesResponsePaginatorTypeDef(TypedDict):
    entities: List[ThemePaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ThemeValuesUnionTypeDef = Union[ThemeValuesTypeDef, ThemeValuesOutputTypeDef]
ReactStartCodegenJobDataUnionTypeDef = Union[
    ReactStartCodegenJobDataTypeDef, ReactStartCodegenJobDataOutputTypeDef
]
CodegenJobTypeDef = TypedDict(
    "CodegenJobTypeDef",
    {
        "id": str,
        "appId": str,
        "environmentName": str,
        "renderConfig": NotRequired[CodegenJobRenderConfigOutputTypeDef],
        "genericDataSchema": NotRequired[CodegenJobGenericDataSchemaOutputTypeDef],
        "autoGenerateForms": NotRequired[bool],
        "features": NotRequired[CodegenFeatureFlagsTypeDef],
        "status": NotRequired[CodegenJobStatusType],
        "statusMessage": NotRequired[str],
        "asset": NotRequired[CodegenJobAssetTypeDef],
        "tags": NotRequired[Dict[str, str]],
        "createdAt": NotRequired[datetime],
        "modifiedAt": NotRequired[datetime],
        "dependencies": NotRequired[List[CodegenDependencyTypeDef]],
    },
)

class CodegenGenericDataNonModelTypeDef(TypedDict):
    fields: Mapping[str, CodegenGenericDataFieldUnionTypeDef]

CodegenGenericDataModelUnionTypeDef = Union[
    CodegenGenericDataModelTypeDef, CodegenGenericDataModelOutputTypeDef
]
MutationActionSetStateParameterTypeDef = TypedDict(
    "MutationActionSetStateParameterTypeDef",
    {
        "componentName": str,
        "property": str,
        "set": ComponentPropertyUnionTypeDef,
    },
)

class ComponentEventOutputTypeDef(TypedDict):
    action: NotRequired[str]
    parameters: NotRequired[ActionParametersOutputTypeDef]
    bindingEvent: NotRequired[str]

class ComponentEventPaginatorTypeDef(TypedDict):
    action: NotRequired[str]
    parameters: NotRequired[ActionParametersPaginatorTypeDef]
    bindingEvent: NotRequired[str]

FieldInputConfigOutputTypeDef = TypedDict(
    "FieldInputConfigOutputTypeDef",
    {
        "type": str,
        "required": NotRequired[bool],
        "readOnly": NotRequired[bool],
        "placeholder": NotRequired[str],
        "defaultValue": NotRequired[str],
        "descriptiveText": NotRequired[str],
        "defaultChecked": NotRequired[bool],
        "defaultCountryCode": NotRequired[str],
        "valueMappings": NotRequired[ValueMappingsOutputTypeDef],
        "name": NotRequired[str],
        "minValue": NotRequired[float],
        "maxValue": NotRequired[float],
        "step": NotRequired[float],
        "value": NotRequired[str],
        "isArray": NotRequired[bool],
        "fileUploaderConfig": NotRequired[FileUploaderFieldConfigOutputTypeDef],
    },
)
FieldInputConfigPaginatorTypeDef = TypedDict(
    "FieldInputConfigPaginatorTypeDef",
    {
        "type": str,
        "required": NotRequired[bool],
        "readOnly": NotRequired[bool],
        "placeholder": NotRequired[str],
        "defaultValue": NotRequired[str],
        "descriptiveText": NotRequired[str],
        "defaultChecked": NotRequired[bool],
        "defaultCountryCode": NotRequired[str],
        "valueMappings": NotRequired[ValueMappingsPaginatorTypeDef],
        "name": NotRequired[str],
        "minValue": NotRequired[float],
        "maxValue": NotRequired[float],
        "step": NotRequired[float],
        "value": NotRequired[str],
        "isArray": NotRequired[bool],
        "fileUploaderConfig": NotRequired[FileUploaderFieldConfigOutputTypeDef],
    },
)
ValueMappingUnionTypeDef = Union[ValueMappingTypeDef, ValueMappingOutputTypeDef]
ComponentBindingPropertiesValueTypeDef = TypedDict(
    "ComponentBindingPropertiesValueTypeDef",
    {
        "type": NotRequired[str],
        "bindingProperties": NotRequired[ComponentBindingPropertiesValuePropertiesUnionTypeDef],
        "defaultValue": NotRequired[str],
    },
)

class CreateThemeDataTypeDef(TypedDict):
    name: str
    values: Sequence[ThemeValuesUnionTypeDef]
    overrides: NotRequired[Sequence[ThemeValuesTypeDef]]
    tags: NotRequired[Mapping[str, str]]

UpdateThemeDataTypeDef = TypedDict(
    "UpdateThemeDataTypeDef",
    {
        "values": Sequence[ThemeValuesUnionTypeDef],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "overrides": NotRequired[Sequence[ThemeValuesTypeDef]],
    },
)

class CodegenJobRenderConfigTypeDef(TypedDict):
    react: NotRequired[ReactStartCodegenJobDataUnionTypeDef]

class GetCodegenJobResponseTypeDef(TypedDict):
    job: CodegenJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartCodegenJobResponseTypeDef(TypedDict):
    entity: CodegenJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

CodegenGenericDataNonModelUnionTypeDef = Union[
    CodegenGenericDataNonModelTypeDef, CodegenGenericDataNonModelOutputTypeDef
]
MutationActionSetStateParameterUnionTypeDef = Union[
    MutationActionSetStateParameterTypeDef, MutationActionSetStateParameterOutputTypeDef
]

class ComponentChildOutputTypeDef(TypedDict):
    componentType: str
    name: str
    properties: Dict[str, ComponentPropertyOutputTypeDef]
    children: NotRequired[List[Dict[str, Any]]]
    events: NotRequired[Dict[str, ComponentEventOutputTypeDef]]
    sourceId: NotRequired[str]

class ComponentChildPaginatorTypeDef(TypedDict):
    componentType: str
    name: str
    properties: Dict[str, ComponentPropertyPaginatorTypeDef]
    children: NotRequired[List[Dict[str, Any]]]
    events: NotRequired[Dict[str, ComponentEventPaginatorTypeDef]]
    sourceId: NotRequired[str]

class FieldConfigOutputTypeDef(TypedDict):
    label: NotRequired[str]
    position: NotRequired[FieldPositionTypeDef]
    excluded: NotRequired[bool]
    inputType: NotRequired[FieldInputConfigOutputTypeDef]
    validations: NotRequired[List[FieldValidationConfigurationOutputTypeDef]]

class FieldConfigPaginatorTypeDef(TypedDict):
    label: NotRequired[str]
    position: NotRequired[FieldPositionTypeDef]
    excluded: NotRequired[bool]
    inputType: NotRequired[FieldInputConfigPaginatorTypeDef]
    validations: NotRequired[List[FieldValidationConfigurationOutputTypeDef]]

class ValueMappingsTypeDef(TypedDict):
    values: Sequence[ValueMappingUnionTypeDef]
    bindingProperties: NotRequired[Mapping[str, FormInputBindingPropertiesValueTypeDef]]

ComponentBindingPropertiesValueUnionTypeDef = Union[
    ComponentBindingPropertiesValueTypeDef, ComponentBindingPropertiesValueOutputTypeDef
]

class CreateThemeRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    themeToCreate: CreateThemeDataTypeDef
    clientToken: NotRequired[str]

UpdateThemeRequestTypeDef = TypedDict(
    "UpdateThemeRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "updatedTheme": UpdateThemeDataTypeDef,
        "clientToken": NotRequired[str],
    },
)
CodegenJobRenderConfigUnionTypeDef = Union[
    CodegenJobRenderConfigTypeDef, CodegenJobRenderConfigOutputTypeDef
]

class CodegenJobGenericDataSchemaTypeDef(TypedDict):
    dataSourceType: Literal["DataStore"]
    models: Mapping[str, CodegenGenericDataModelUnionTypeDef]
    enums: Mapping[str, CodegenGenericDataEnumUnionTypeDef]
    nonModels: Mapping[str, CodegenGenericDataNonModelUnionTypeDef]

ActionParametersTypeDef = TypedDict(
    "ActionParametersTypeDef",
    {
        "type": NotRequired[ComponentPropertyUnionTypeDef],
        "url": NotRequired[ComponentPropertyUnionTypeDef],
        "anchor": NotRequired[ComponentPropertyUnionTypeDef],
        "target": NotRequired[ComponentPropertyUnionTypeDef],
        "global": NotRequired[ComponentPropertyUnionTypeDef],
        "model": NotRequired[str],
        "id": NotRequired[ComponentPropertyUnionTypeDef],
        "fields": NotRequired[Mapping[str, ComponentPropertyTypeDef]],
        "state": NotRequired[MutationActionSetStateParameterUnionTypeDef],
    },
)
ComponentTypeDef = TypedDict(
    "ComponentTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
        "componentType": str,
        "properties": Dict[str, ComponentPropertyOutputTypeDef],
        "variants": List[ComponentVariantOutputTypeDef],
        "overrides": Dict[str, Dict[str, str]],
        "bindingProperties": Dict[str, ComponentBindingPropertiesValueOutputTypeDef],
        "createdAt": datetime,
        "sourceId": NotRequired[str],
        "children": NotRequired[List[ComponentChildOutputTypeDef]],
        "collectionProperties": NotRequired[Dict[str, ComponentDataConfigurationOutputTypeDef]],
        "modifiedAt": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "events": NotRequired[Dict[str, ComponentEventOutputTypeDef]],
        "schemaVersion": NotRequired[str],
    },
)
ComponentPaginatorTypeDef = TypedDict(
    "ComponentPaginatorTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
        "componentType": str,
        "properties": Dict[str, ComponentPropertyPaginatorTypeDef],
        "variants": List[ComponentVariantOutputTypeDef],
        "overrides": Dict[str, Dict[str, str]],
        "bindingProperties": Dict[str, ComponentBindingPropertiesValuePaginatorTypeDef],
        "createdAt": datetime,
        "sourceId": NotRequired[str],
        "children": NotRequired[List[ComponentChildPaginatorTypeDef]],
        "collectionProperties": NotRequired[Dict[str, ComponentDataConfigurationPaginatorTypeDef]],
        "modifiedAt": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "events": NotRequired[Dict[str, ComponentEventPaginatorTypeDef]],
        "schemaVersion": NotRequired[str],
    },
)
FormTypeDef = TypedDict(
    "FormTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
        "formActionType": FormActionTypeType,
        "style": FormStyleTypeDef,
        "dataType": FormDataTypeConfigTypeDef,
        "fields": Dict[str, FieldConfigOutputTypeDef],
        "sectionalElements": Dict[str, SectionalElementTypeDef],
        "schemaVersion": str,
        "tags": NotRequired[Dict[str, str]],
        "cta": NotRequired[FormCTATypeDef],
        "labelDecorator": NotRequired[LabelDecoratorType],
    },
)
FormPaginatorTypeDef = TypedDict(
    "FormPaginatorTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "name": str,
        "formActionType": FormActionTypeType,
        "style": FormStyleTypeDef,
        "dataType": FormDataTypeConfigTypeDef,
        "fields": Dict[str, FieldConfigPaginatorTypeDef],
        "sectionalElements": Dict[str, SectionalElementTypeDef],
        "schemaVersion": str,
        "tags": NotRequired[Dict[str, str]],
        "cta": NotRequired[FormCTATypeDef],
        "labelDecorator": NotRequired[LabelDecoratorType],
    },
)
ValueMappingsUnionTypeDef = Union[ValueMappingsTypeDef, ValueMappingsOutputTypeDef]
CodegenJobGenericDataSchemaUnionTypeDef = Union[
    CodegenJobGenericDataSchemaTypeDef, CodegenJobGenericDataSchemaOutputTypeDef
]
ActionParametersUnionTypeDef = Union[ActionParametersTypeDef, ActionParametersOutputTypeDef]

class CreateComponentResponseTypeDef(TypedDict):
    entity: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportComponentsResponseTypeDef(TypedDict):
    entities: List[ComponentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetComponentResponseTypeDef(TypedDict):
    component: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateComponentResponseTypeDef(TypedDict):
    entity: ComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportComponentsResponsePaginatorTypeDef(TypedDict):
    entities: List[ComponentPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateFormResponseTypeDef(TypedDict):
    entity: FormTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportFormsResponseTypeDef(TypedDict):
    entities: List[FormTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetFormResponseTypeDef(TypedDict):
    form: FormTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFormResponseTypeDef(TypedDict):
    entity: FormTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExportFormsResponsePaginatorTypeDef(TypedDict):
    entities: List[FormPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

FieldInputConfigTypeDef = TypedDict(
    "FieldInputConfigTypeDef",
    {
        "type": str,
        "required": NotRequired[bool],
        "readOnly": NotRequired[bool],
        "placeholder": NotRequired[str],
        "defaultValue": NotRequired[str],
        "descriptiveText": NotRequired[str],
        "defaultChecked": NotRequired[bool],
        "defaultCountryCode": NotRequired[str],
        "valueMappings": NotRequired[ValueMappingsUnionTypeDef],
        "name": NotRequired[str],
        "minValue": NotRequired[float],
        "maxValue": NotRequired[float],
        "step": NotRequired[float],
        "value": NotRequired[str],
        "isArray": NotRequired[bool],
        "fileUploaderConfig": NotRequired[FileUploaderFieldConfigUnionTypeDef],
    },
)

class StartCodegenJobDataTypeDef(TypedDict):
    renderConfig: CodegenJobRenderConfigUnionTypeDef
    genericDataSchema: NotRequired[CodegenJobGenericDataSchemaUnionTypeDef]
    autoGenerateForms: NotRequired[bool]
    features: NotRequired[CodegenFeatureFlagsTypeDef]
    tags: NotRequired[Mapping[str, str]]

class ComponentEventTypeDef(TypedDict):
    action: NotRequired[str]
    parameters: NotRequired[ActionParametersUnionTypeDef]
    bindingEvent: NotRequired[str]

FieldInputConfigUnionTypeDef = Union[FieldInputConfigTypeDef, FieldInputConfigOutputTypeDef]

class StartCodegenJobRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    codegenJobToCreate: StartCodegenJobDataTypeDef
    clientToken: NotRequired[str]

class ComponentChildTypeDef(TypedDict):
    componentType: str
    name: str
    properties: Mapping[str, ComponentPropertyTypeDef]
    children: NotRequired[Sequence[Mapping[str, Any]]]
    events: NotRequired[Mapping[str, ComponentEventTypeDef]]
    sourceId: NotRequired[str]

ComponentEventUnionTypeDef = Union[ComponentEventTypeDef, ComponentEventOutputTypeDef]

class FieldConfigTypeDef(TypedDict):
    label: NotRequired[str]
    position: NotRequired[FieldPositionTypeDef]
    excluded: NotRequired[bool]
    inputType: NotRequired[FieldInputConfigUnionTypeDef]
    validations: NotRequired[Sequence[FieldValidationConfigurationUnionTypeDef]]

ComponentChildUnionTypeDef = Union[ComponentChildTypeDef, ComponentChildOutputTypeDef]
FieldConfigUnionTypeDef = Union[FieldConfigTypeDef, FieldConfigOutputTypeDef]

class CreateComponentDataTypeDef(TypedDict):
    name: str
    componentType: str
    properties: Mapping[str, ComponentPropertyUnionTypeDef]
    variants: Sequence[ComponentVariantUnionTypeDef]
    overrides: Mapping[str, Mapping[str, str]]
    bindingProperties: Mapping[str, ComponentBindingPropertiesValueUnionTypeDef]
    sourceId: NotRequired[str]
    children: NotRequired[Sequence[ComponentChildUnionTypeDef]]
    collectionProperties: NotRequired[Mapping[str, ComponentDataConfigurationUnionTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    events: NotRequired[Mapping[str, ComponentEventUnionTypeDef]]
    schemaVersion: NotRequired[str]

UpdateComponentDataTypeDef = TypedDict(
    "UpdateComponentDataTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "sourceId": NotRequired[str],
        "componentType": NotRequired[str],
        "properties": NotRequired[Mapping[str, ComponentPropertyUnionTypeDef]],
        "children": NotRequired[Sequence[ComponentChildUnionTypeDef]],
        "variants": NotRequired[Sequence[ComponentVariantUnionTypeDef]],
        "overrides": NotRequired[Mapping[str, Mapping[str, str]]],
        "bindingProperties": NotRequired[Mapping[str, ComponentBindingPropertiesValueUnionTypeDef]],
        "collectionProperties": NotRequired[Mapping[str, ComponentDataConfigurationUnionTypeDef]],
        "events": NotRequired[Mapping[str, ComponentEventUnionTypeDef]],
        "schemaVersion": NotRequired[str],
    },
)

class CreateFormDataTypeDef(TypedDict):
    name: str
    dataType: FormDataTypeConfigTypeDef
    formActionType: FormActionTypeType
    fields: Mapping[str, FieldConfigUnionTypeDef]
    style: FormStyleTypeDef
    sectionalElements: Mapping[str, SectionalElementTypeDef]
    schemaVersion: str
    cta: NotRequired[FormCTATypeDef]
    tags: NotRequired[Mapping[str, str]]
    labelDecorator: NotRequired[LabelDecoratorType]

class UpdateFormDataTypeDef(TypedDict):
    name: NotRequired[str]
    dataType: NotRequired[FormDataTypeConfigTypeDef]
    formActionType: NotRequired[FormActionTypeType]
    fields: NotRequired[Mapping[str, FieldConfigUnionTypeDef]]
    style: NotRequired[FormStyleTypeDef]
    sectionalElements: NotRequired[Mapping[str, SectionalElementTypeDef]]
    schemaVersion: NotRequired[str]
    cta: NotRequired[FormCTATypeDef]
    labelDecorator: NotRequired[LabelDecoratorType]

class CreateComponentRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    componentToCreate: CreateComponentDataTypeDef
    clientToken: NotRequired[str]

UpdateComponentRequestTypeDef = TypedDict(
    "UpdateComponentRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "updatedComponent": UpdateComponentDataTypeDef,
        "clientToken": NotRequired[str],
    },
)

class CreateFormRequestTypeDef(TypedDict):
    appId: str
    environmentName: str
    formToCreate: CreateFormDataTypeDef
    clientToken: NotRequired[str]

UpdateFormRequestTypeDef = TypedDict(
    "UpdateFormRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "id": str,
        "updatedForm": UpdateFormDataTypeDef,
        "clientToken": NotRequired[str],
    },
)
