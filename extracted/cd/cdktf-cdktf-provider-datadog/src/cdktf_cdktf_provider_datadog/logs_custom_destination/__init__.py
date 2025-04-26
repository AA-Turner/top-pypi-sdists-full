r'''
# `datadog_logs_custom_destination`

Refer to the Terraform Registry for docs: [`datadog_logs_custom_destination`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class LogsCustomDestination(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestination",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination datadog_logs_custom_destination}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        elasticsearch_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationElasticsearchDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_tags_restriction_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        forward_tags_restriction_list_type: typing.Optional[builtins.str] = None,
        http_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationHttpDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query: typing.Optional[builtins.str] = None,
        splunk_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationSplunkDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination datadog_logs_custom_destination} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The custom destination name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#name LogsCustomDestination#name}
        :param elasticsearch_destination: elasticsearch_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#elasticsearch_destination LogsCustomDestination#elasticsearch_destination}
        :param enabled: Whether logs matching this custom destination should be forwarded or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#enabled LogsCustomDestination#enabled}
        :param forward_tags: Whether tags from the forwarded logs should be forwarded or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags LogsCustomDestination#forward_tags}
        :param forward_tags_restriction_list: List of `tag keys <https://docs.datadoghq.com/getting_started/tagging/#define-tags>`_ to be filtered. An empty list represents no restriction is in place and either all or no tags will be forwarded depending on ``forward_tags_restriction_list_type`` parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags_restriction_list LogsCustomDestination#forward_tags_restriction_list}
        :param forward_tags_restriction_list_type: How the ``forward_tags_restriction_list`` parameter should be interpreted. If ``ALLOW_LIST``, then only tags whose keys on the forwarded logs match the ones on the restriction list are forwarded. ``BLOCK_LIST`` works the opposite way. It does not forward the tags matching the ones on the list. Valid values are ``ALLOW_LIST``, ``BLOCK_LIST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags_restriction_list_type LogsCustomDestination#forward_tags_restriction_list_type}
        :param http_destination: http_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#http_destination LogsCustomDestination#http_destination}
        :param query: The custom destination query filter. Logs matching this query are forwarded to the destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#query LogsCustomDestination#query}
        :param splunk_destination: splunk_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#splunk_destination LogsCustomDestination#splunk_destination}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffafdeb14f2844ef4b622cad794e55f9af27d5ab8587da4104ae365c7ccd270)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = LogsCustomDestinationConfig(
            name=name,
            elasticsearch_destination=elasticsearch_destination,
            enabled=enabled,
            forward_tags=forward_tags,
            forward_tags_restriction_list=forward_tags_restriction_list,
            forward_tags_restriction_list_type=forward_tags_restriction_list_type,
            http_destination=http_destination,
            query=query,
            splunk_destination=splunk_destination,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a LogsCustomDestination resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogsCustomDestination to import.
        :param import_from_id: The id of the existing LogsCustomDestination that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogsCustomDestination to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d934d2e9792235c8b3834b047d31eafceeb33f900e7d84b14a4f4d2a64d410)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putElasticsearchDestination")
    def put_elasticsearch_destination(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationElasticsearchDestination", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa089e60b92b4cbd820c192a455423a98866bd42ed12b1e05a2b31a9068b0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElasticsearchDestination", [value]))

    @jsii.member(jsii_name="putHttpDestination")
    def put_http_destination(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationHttpDestination", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15afeb22f4f48dca0011b06b0d2f719bd1a3f7cdb202b28f66d5f73b7778efff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpDestination", [value]))

    @jsii.member(jsii_name="putSplunkDestination")
    def put_splunk_destination(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationSplunkDestination", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe02f0abef9e5a9b6365bd87ed15e820135a0b7625c205b8b4c348721d2d0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSplunkDestination", [value]))

    @jsii.member(jsii_name="resetElasticsearchDestination")
    def reset_elasticsearch_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchDestination", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetForwardTags")
    def reset_forward_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardTags", []))

    @jsii.member(jsii_name="resetForwardTagsRestrictionList")
    def reset_forward_tags_restriction_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardTagsRestrictionList", []))

    @jsii.member(jsii_name="resetForwardTagsRestrictionListType")
    def reset_forward_tags_restriction_list_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardTagsRestrictionListType", []))

    @jsii.member(jsii_name="resetHttpDestination")
    def reset_http_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpDestination", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetSplunkDestination")
    def reset_splunk_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplunkDestination", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchDestination")
    def elasticsearch_destination(
        self,
    ) -> "LogsCustomDestinationElasticsearchDestinationList":
        return typing.cast("LogsCustomDestinationElasticsearchDestinationList", jsii.get(self, "elasticsearchDestination"))

    @builtins.property
    @jsii.member(jsii_name="httpDestination")
    def http_destination(self) -> "LogsCustomDestinationHttpDestinationList":
        return typing.cast("LogsCustomDestinationHttpDestinationList", jsii.get(self, "httpDestination"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="splunkDestination")
    def splunk_destination(self) -> "LogsCustomDestinationSplunkDestinationList":
        return typing.cast("LogsCustomDestinationSplunkDestinationList", jsii.get(self, "splunkDestination"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchDestinationInput")
    def elasticsearch_destination_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationElasticsearchDestination"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationElasticsearchDestination"]]], jsii.get(self, "elasticsearchDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardTagsInput")
    def forward_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forwardTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardTagsRestrictionListInput")
    def forward_tags_restriction_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forwardTagsRestrictionListInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardTagsRestrictionListTypeInput")
    def forward_tags_restriction_list_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardTagsRestrictionListTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="httpDestinationInput")
    def http_destination_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationHttpDestination"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationHttpDestination"]]], jsii.get(self, "httpDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="splunkDestinationInput")
    def splunk_destination_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationSplunkDestination"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationSplunkDestination"]]], jsii.get(self, "splunkDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4592ebe7e60b5b1c08adfc331419350980468ea886480df52c6bfa38dd26381c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardTags")
    def forward_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forwardTags"))

    @forward_tags.setter
    def forward_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bceb3f437cc72710144ec8e867f1554f975263f8644eddebe57e0ff1c23d07cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardTagsRestrictionList")
    def forward_tags_restriction_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forwardTagsRestrictionList"))

    @forward_tags_restriction_list.setter
    def forward_tags_restriction_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5019aeb2d819add2f090b7b2951cd64a75d3d6a7f1a15c1dbc3f144131868e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardTagsRestrictionList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardTagsRestrictionListType")
    def forward_tags_restriction_list_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardTagsRestrictionListType"))

    @forward_tags_restriction_list_type.setter
    def forward_tags_restriction_list_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d83274ce940872562712192a736cc31d6a0973110098a5224083b2e58df29c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardTagsRestrictionListType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87b2eb13dffb9a05861cd81f6b6af9616031867f28c3cf44b11e743390563f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21b43e2826bdb00f312271492ce726a0e96fdbdf06c924b2faffbc1ce4469be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "elasticsearch_destination": "elasticsearchDestination",
        "enabled": "enabled",
        "forward_tags": "forwardTags",
        "forward_tags_restriction_list": "forwardTagsRestrictionList",
        "forward_tags_restriction_list_type": "forwardTagsRestrictionListType",
        "http_destination": "httpDestination",
        "query": "query",
        "splunk_destination": "splunkDestination",
    },
)
class LogsCustomDestinationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
        elasticsearch_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationElasticsearchDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        forward_tags_restriction_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        forward_tags_restriction_list_type: typing.Optional[builtins.str] = None,
        http_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationHttpDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query: typing.Optional[builtins.str] = None,
        splunk_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationSplunkDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The custom destination name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#name LogsCustomDestination#name}
        :param elasticsearch_destination: elasticsearch_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#elasticsearch_destination LogsCustomDestination#elasticsearch_destination}
        :param enabled: Whether logs matching this custom destination should be forwarded or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#enabled LogsCustomDestination#enabled}
        :param forward_tags: Whether tags from the forwarded logs should be forwarded or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags LogsCustomDestination#forward_tags}
        :param forward_tags_restriction_list: List of `tag keys <https://docs.datadoghq.com/getting_started/tagging/#define-tags>`_ to be filtered. An empty list represents no restriction is in place and either all or no tags will be forwarded depending on ``forward_tags_restriction_list_type`` parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags_restriction_list LogsCustomDestination#forward_tags_restriction_list}
        :param forward_tags_restriction_list_type: How the ``forward_tags_restriction_list`` parameter should be interpreted. If ``ALLOW_LIST``, then only tags whose keys on the forwarded logs match the ones on the restriction list are forwarded. ``BLOCK_LIST`` works the opposite way. It does not forward the tags matching the ones on the list. Valid values are ``ALLOW_LIST``, ``BLOCK_LIST``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags_restriction_list_type LogsCustomDestination#forward_tags_restriction_list_type}
        :param http_destination: http_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#http_destination LogsCustomDestination#http_destination}
        :param query: The custom destination query filter. Logs matching this query are forwarded to the destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#query LogsCustomDestination#query}
        :param splunk_destination: splunk_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#splunk_destination LogsCustomDestination#splunk_destination}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c88721c3253c72502292d77707f3f95e1c1a5ae820385846a967e430c69f68f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument elasticsearch_destination", value=elasticsearch_destination, expected_type=type_hints["elasticsearch_destination"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument forward_tags", value=forward_tags, expected_type=type_hints["forward_tags"])
            check_type(argname="argument forward_tags_restriction_list", value=forward_tags_restriction_list, expected_type=type_hints["forward_tags_restriction_list"])
            check_type(argname="argument forward_tags_restriction_list_type", value=forward_tags_restriction_list_type, expected_type=type_hints["forward_tags_restriction_list_type"])
            check_type(argname="argument http_destination", value=http_destination, expected_type=type_hints["http_destination"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument splunk_destination", value=splunk_destination, expected_type=type_hints["splunk_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if elasticsearch_destination is not None:
            self._values["elasticsearch_destination"] = elasticsearch_destination
        if enabled is not None:
            self._values["enabled"] = enabled
        if forward_tags is not None:
            self._values["forward_tags"] = forward_tags
        if forward_tags_restriction_list is not None:
            self._values["forward_tags_restriction_list"] = forward_tags_restriction_list
        if forward_tags_restriction_list_type is not None:
            self._values["forward_tags_restriction_list_type"] = forward_tags_restriction_list_type
        if http_destination is not None:
            self._values["http_destination"] = http_destination
        if query is not None:
            self._values["query"] = query
        if splunk_destination is not None:
            self._values["splunk_destination"] = splunk_destination

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The custom destination name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#name LogsCustomDestination#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def elasticsearch_destination(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationElasticsearchDestination"]]]:
        '''elasticsearch_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#elasticsearch_destination LogsCustomDestination#elasticsearch_destination}
        '''
        result = self._values.get("elasticsearch_destination")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationElasticsearchDestination"]]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether logs matching this custom destination should be forwarded or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#enabled LogsCustomDestination#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether tags from the forwarded logs should be forwarded or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags LogsCustomDestination#forward_tags}
        '''
        result = self._values.get("forward_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def forward_tags_restriction_list(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''List of `tag keys <https://docs.datadoghq.com/getting_started/tagging/#define-tags>`_ to be filtered. 				An empty list represents no restriction is in place and either all or no tags will be 				forwarded depending on ``forward_tags_restriction_list_type`` parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags_restriction_list LogsCustomDestination#forward_tags_restriction_list}
        '''
        result = self._values.get("forward_tags_restriction_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def forward_tags_restriction_list_type(self) -> typing.Optional[builtins.str]:
        '''How the ``forward_tags_restriction_list`` parameter should be interpreted.

        If ``ALLOW_LIST``, then only tags whose keys on the forwarded logs match the ones on the restriction list
        are forwarded.
        ``BLOCK_LIST`` works the opposite way. It does not forward the tags matching the ones on the list. Valid values are ``ALLOW_LIST``, ``BLOCK_LIST``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#forward_tags_restriction_list_type LogsCustomDestination#forward_tags_restriction_list_type}
        '''
        result = self._values.get("forward_tags_restriction_list_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_destination(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationHttpDestination"]]]:
        '''http_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#http_destination LogsCustomDestination#http_destination}
        '''
        result = self._values.get("http_destination")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationHttpDestination"]]], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''The custom destination query filter. Logs matching this query are forwarded to the destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#query LogsCustomDestination#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def splunk_destination(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationSplunkDestination"]]]:
        '''splunk_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#splunk_destination LogsCustomDestination#splunk_destination}
        '''
        result = self._values.get("splunk_destination")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationSplunkDestination"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationElasticsearchDestination",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "index_name": "indexName",
        "basic_auth": "basicAuth",
        "index_rotation": "indexRotation",
    },
)
class LogsCustomDestinationElasticsearchDestination:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        index_name: builtins.str,
        basic_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationElasticsearchDestinationBasicAuth", typing.Dict[builtins.str, typing.Any]]]]] = None,
        index_rotation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint: The destination for which logs will be forwarded to. Must have HTTPS scheme. Forwarding back to Datadog is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#endpoint LogsCustomDestination#endpoint}
        :param index_name: Name of the Elasticsearch index (must follow `Elasticsearch's criteria <https://www.elastic.co/guide/en/elasticsearch/reference/8.11/indices-create-index.html#indices-create-api-path-params>`_). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#index_name LogsCustomDestination#index_name}
        :param basic_auth: basic_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#basic_auth LogsCustomDestination#basic_auth}
        :param index_rotation: Date pattern with US locale and UTC timezone to be appended to the index name after adding '-' (that is, '${index_name}-${indexPattern}'). You can customize the index rotation naming pattern by choosing one of these options: - Hourly: 'yyyy-MM-dd-HH' (as an example, it would render: '2022-10-19-09') - Daily: 'yyyy-MM-dd' (as an example, it would render: '2022-10-19') - Weekly: 'yyyy-'W'ww' (as an example, it would render: '2022-W42') - Monthly: 'yyyy-MM' (as an example, it would render: '2022-10') If this field is missing or is blank, it means that the index name will always be the same (that is, no rotation). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#index_rotation LogsCustomDestination#index_rotation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741caa8cc4e64b980452f4609d5bb56126270344c66315a0e7b16767fd918f9d)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument index_rotation", value=index_rotation, expected_type=type_hints["index_rotation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "index_name": index_name,
        }
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if index_rotation is not None:
            self._values["index_rotation"] = index_rotation

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''The destination for which logs will be forwarded to.

        Must have HTTPS scheme. Forwarding back to Datadog is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#endpoint LogsCustomDestination#endpoint}
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index_name(self) -> builtins.str:
        '''Name of the Elasticsearch index (must follow `Elasticsearch's criteria <https://www.elastic.co/guide/en/elasticsearch/reference/8.11/indices-create-index.html#indices-create-api-path-params>`_).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#index_name LogsCustomDestination#index_name}
        '''
        result = self._values.get("index_name")
        assert result is not None, "Required property 'index_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic_auth(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationElasticsearchDestinationBasicAuth"]]]:
        '''basic_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#basic_auth LogsCustomDestination#basic_auth}
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationElasticsearchDestinationBasicAuth"]]], result)

    @builtins.property
    def index_rotation(self) -> typing.Optional[builtins.str]:
        '''Date pattern with US locale and UTC timezone to be appended to the index name after adding '-' 							(that is, '${index_name}-${indexPattern}').

        You can customize the index rotation naming pattern by choosing one of these options:

        - Hourly: 'yyyy-MM-dd-HH' (as an example, it would render: '2022-10-19-09')
        - Daily: 'yyyy-MM-dd' (as an example, it would render: '2022-10-19')
        - Weekly: 'yyyy-'W'ww' (as an example, it would render: '2022-W42')
        - Monthly: 'yyyy-MM' (as an example, it would render: '2022-10')
          If this field is missing or is blank, it means that the index name will always be the same
          (that is, no rotation).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#index_rotation LogsCustomDestination#index_rotation}
        '''
        result = self._values.get("index_rotation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomDestinationElasticsearchDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationElasticsearchDestinationBasicAuth",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class LogsCustomDestinationElasticsearchDestinationBasicAuth:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: The password of the authentication. This field is not returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#password LogsCustomDestination#password}
        :param username: The username of the authentication. This field is not returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#username LogsCustomDestination#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b6c0229537ddd998fbff6bc39495545ac22678651c7ba9596231bb4f72404b6)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''The password of the authentication. This field is not returned by the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#password LogsCustomDestination#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username of the authentication. This field is not returned by the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#username LogsCustomDestination#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomDestinationElasticsearchDestinationBasicAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomDestinationElasticsearchDestinationBasicAuthList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationElasticsearchDestinationBasicAuthList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d032958f3f70d1b85eefe4799194e5c6b0428fd047e09b14edf7afbfc4a958ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomDestinationElasticsearchDestinationBasicAuthOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b854f495758a44b0349afb258fb617fa088dac6aa66eb0bbd51dda40a4642b3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomDestinationElasticsearchDestinationBasicAuthOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd9e6d437e18a4a4edd1f3b7cebd9d4b9b99d8f18bf8f33252ec26ff16c36131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157502acaa46a4c4080015432b658400c15685208ce7941fdb2c52e5af4e0a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c6a18685cb082c18030e2ff14410e08180145dc6d8a53ec5a64d39c4db47ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestinationBasicAuth]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestinationBasicAuth]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestinationBasicAuth]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed39ff8e0a18cf700670676200a58774fb8c209ef6dc6ce63160c62c71ae0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomDestinationElasticsearchDestinationBasicAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationElasticsearchDestinationBasicAuthOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5754669c7f9d814f1866a45be472a3f6d4e1f23e201831ff39c9c40fe6680d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd355697eeec69e0f076f8942872eba10638724a7623a9692347df253080e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a0f29096f9c69a86a484b4500b7fdcf349515ca39105e61c7c6916fa5d5547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationElasticsearchDestinationBasicAuth]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationElasticsearchDestinationBasicAuth]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationElasticsearchDestinationBasicAuth]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b37bc8da2b744790335be3b539c090be803256fcdc047c422b3eb7af5c92fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomDestinationElasticsearchDestinationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationElasticsearchDestinationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7503a34c11b4594c068d8ea4bc7eb76fcdeba61385c5ead114a5ada085d3d944)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomDestinationElasticsearchDestinationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6590a8095d2949ced5b73ab248f386463ceaed0297fe6db7d80199e7f8e64834)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomDestinationElasticsearchDestinationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e050d8b34080f7675c4409f79d2e180b8e10a3ffaababfd3e0a970f497142267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7553072c6385816677087f3c3959ee5914e7436da3ebb8f1d4b0110b67ca045f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6795384e4afcb8059b629e4730a64e65b0b6c3dc63c2b20efab1eafaf08af7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestination]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestination]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a8bd3d4a416e6119ef34d3c03ae01b26d75b9b827edd9e739f43f05e7fe0c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomDestinationElasticsearchDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationElasticsearchDestinationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878f41c080c13efd36e6c98698ca4d88bb5cd533d9b3305a699052b90dff565c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBasicAuth")
    def put_basic_auth(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationElasticsearchDestinationBasicAuth, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841277560373c7f9ce365ce1c6574dce71f2449ad382dfea5345dfdf38da58e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBasicAuth", [value]))

    @jsii.member(jsii_name="resetBasicAuth")
    def reset_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuth", []))

    @jsii.member(jsii_name="resetIndexRotation")
    def reset_index_rotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexRotation", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(self) -> LogsCustomDestinationElasticsearchDestinationBasicAuthList:
        return typing.cast(LogsCustomDestinationElasticsearchDestinationBasicAuthList, jsii.get(self, "basicAuth"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestinationBasicAuth]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestinationBasicAuth]]], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="indexNameInput")
    def index_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexNameInput"))

    @builtins.property
    @jsii.member(jsii_name="indexRotationInput")
    def index_rotation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexRotationInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342f83cdf7ba1a5c91a5b0738aaf3c1bf18e9bc82db2166c2aa72fc7dccc8f98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexName")
    def index_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexName"))

    @index_name.setter
    def index_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e07695f5a5ddb2977bdd2593dcafc57ecb3e3730688d554da810bf75e54dfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexRotation")
    def index_rotation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexRotation"))

    @index_rotation.setter
    def index_rotation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307f7926dc7642f56109e9cf3e6903335cfb9abc650526be25f398fea82a6ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexRotation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationElasticsearchDestination]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationElasticsearchDestination]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationElasticsearchDestination]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbeb5ae1dfbca06b0ff86ec68bf02302e711be4bf1a408bcca3cb7ff50a3d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestination",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "basic_auth": "basicAuth",
        "custom_header_auth": "customHeaderAuth",
    },
)
class LogsCustomDestinationHttpDestination:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        basic_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationHttpDestinationBasicAuth", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_header_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomDestinationHttpDestinationCustomHeaderAuth", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param endpoint: The destination for which logs will be forwarded to. Must have HTTPS scheme. Forwarding back to Datadog is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#endpoint LogsCustomDestination#endpoint}
        :param basic_auth: basic_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#basic_auth LogsCustomDestination#basic_auth}
        :param custom_header_auth: custom_header_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#custom_header_auth LogsCustomDestination#custom_header_auth}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0608feff39ac62abf5ef4d6a8bd7984c25d77e8dbf4309a08389978bd437b2ef)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument custom_header_auth", value=custom_header_auth, expected_type=type_hints["custom_header_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
        }
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if custom_header_auth is not None:
            self._values["custom_header_auth"] = custom_header_auth

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''The destination for which logs will be forwarded to.

        Must have HTTPS scheme. Forwarding back to Datadog is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#endpoint LogsCustomDestination#endpoint}
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic_auth(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationHttpDestinationBasicAuth"]]]:
        '''basic_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#basic_auth LogsCustomDestination#basic_auth}
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationHttpDestinationBasicAuth"]]], result)

    @builtins.property
    def custom_header_auth(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationHttpDestinationCustomHeaderAuth"]]]:
        '''custom_header_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#custom_header_auth LogsCustomDestination#custom_header_auth}
        '''
        result = self._values.get("custom_header_auth")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomDestinationHttpDestinationCustomHeaderAuth"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomDestinationHttpDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestinationBasicAuth",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class LogsCustomDestinationHttpDestinationBasicAuth:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: The password of the authentication. This field is not returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#password LogsCustomDestination#password}
        :param username: The username of the authentication. This field is not returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#username LogsCustomDestination#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c85b25194c200c2724c9c94bd8b8ffa2459f1b420a31601373adeb5d8262aa)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''The password of the authentication. This field is not returned by the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#password LogsCustomDestination#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username of the authentication. This field is not returned by the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#username LogsCustomDestination#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomDestinationHttpDestinationBasicAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomDestinationHttpDestinationBasicAuthList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestinationBasicAuthList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd73ff27ba901fd1e3e826a37b5c9954e6481919d020a43a96569f182aad4a94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomDestinationHttpDestinationBasicAuthOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfff52acda7627fa3c17f92afe93d79b17ec224ab17661ba8789b3feed26d0a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomDestinationHttpDestinationBasicAuthOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9848385a5f26b4ee81afba66dd1fa469f201aa7a58a1ab7166950cb779cff291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f39519f74b8e2b5541ac457187027414be700c91b97515c9ec47b9cf268737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a09234fa4c2d47befcda9bfbfd85326e260dcec59404364a00ab4747a33866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationBasicAuth]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationBasicAuth]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationBasicAuth]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f0a9a543deb8f6cef89e6569e4137c6f78214152d33e4ebd91b19aa361603a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomDestinationHttpDestinationBasicAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestinationBasicAuthOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fedd27001f4d7644c286aa7214e9f428d4cab91cbadf4ff19ad42de0c717618)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e159218df0715d57ce4196bb0b52ba91b92ef0a4d179f36054109ef695e5ebb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f5a0eb661103411b6dab23e29f1ab7aae7bd089921dc53cf496cbebd2719f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestinationBasicAuth]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestinationBasicAuth]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestinationBasicAuth]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988d752ce99fbfba2dc2d57153ad9cd1b51fce00e0675e8d10e21d55d047c6ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestinationCustomHeaderAuth",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class LogsCustomDestinationHttpDestinationCustomHeaderAuth:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
    ) -> None:
        '''
        :param header_name: The header name of the authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#header_name LogsCustomDestination#header_name}
        :param header_value: The header value of the authentication. This field is not returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#header_value LogsCustomDestination#header_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bea779e91bfcb4dd4cc14f5efe5d04bb10f75decb76a9e4b177c86e1375195)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "header_value": header_value,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The header name of the authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#header_name LogsCustomDestination#header_name}
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''The header value of the authentication. This field is not returned by the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#header_value LogsCustomDestination#header_value}
        '''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomDestinationHttpDestinationCustomHeaderAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomDestinationHttpDestinationCustomHeaderAuthList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestinationCustomHeaderAuthList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3048f6c21d930a7d5f46ccd3d54ad68996f40adc3e117d0359ba2bfe8be07bad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomDestinationHttpDestinationCustomHeaderAuthOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6392770c725425188386a022bc90f45e15a49426dff3e94e509ed6d52fd4e403)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomDestinationHttpDestinationCustomHeaderAuthOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e56ab18765addb5a67de0a19ffbe5137ff597af3fc2e4bbd8adbfb751f957f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c9840683001c481d06a38a5aac59323c48b9bbac2925ef2bb0ab22166bec7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026f0ac3c02ee247d4012b8e798e7760991e3e94131524774d8527d2c29827b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationCustomHeaderAuth]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationCustomHeaderAuth]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationCustomHeaderAuth]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a388f638da39d09af7405abf3e180dae4d349565b11d549d20da15e2d0f8c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomDestinationHttpDestinationCustomHeaderAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestinationCustomHeaderAuthOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810706f9a8470f078957929e87344b43b2a772bc1186db58724f533ed56c4f5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="headerValueInput")
    def header_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bc521c268bdcfd821ef6ff4406b5d03d78d8eee391f16101d94992a34957a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e1722ae00a5a01ed2bc5851982265350e44a119f98a54fc82d076a09a1a5e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestinationCustomHeaderAuth]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestinationCustomHeaderAuth]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestinationCustomHeaderAuth]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fbbfdd436548fddef9ef0276c1715134385e04784dbdbe720974b43e39b989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomDestinationHttpDestinationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestinationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77908b8020c2422545c0542a6ea69c8faab1e8d24a246696b5bcc0ac9de9f163)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomDestinationHttpDestinationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551a30c66807d1eb17021eb5d63b630f21d52c33c4f62e7507b8486510ae76b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomDestinationHttpDestinationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6561d175986716b2471c4434aea3f8f7d760a385b85b9be6dce7f6351b1a15c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bfb6abc4faf32d228209fee5a7561806e37e39d83a3afcc59352e5ae0073cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c7396a81ef66f2e4bd0ddf25a50c44b866930c159eae94ea20212e1e755a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestination]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestination]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5fabcbd740a72fc0505a60be7e2acf37179d4e66d4872deba767435846e371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomDestinationHttpDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationHttpDestinationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76473078b0a05be725aa8b56df4e8f9da230220ba4884901e793c75656d32f63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBasicAuth")
    def put_basic_auth(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestinationBasicAuth, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e691cf4c3f68aa99f374d9262c98ff0fa23968a39f820e7dd7a44998faea9693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBasicAuth", [value]))

    @jsii.member(jsii_name="putCustomHeaderAuth")
    def put_custom_header_auth(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestinationCustomHeaderAuth, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb32b6aa19ed11a34358228702600311daddde81aad0e1ad8b6ee997d93690e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomHeaderAuth", [value]))

    @jsii.member(jsii_name="resetBasicAuth")
    def reset_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuth", []))

    @jsii.member(jsii_name="resetCustomHeaderAuth")
    def reset_custom_header_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHeaderAuth", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(self) -> LogsCustomDestinationHttpDestinationBasicAuthList:
        return typing.cast(LogsCustomDestinationHttpDestinationBasicAuthList, jsii.get(self, "basicAuth"))

    @builtins.property
    @jsii.member(jsii_name="customHeaderAuth")
    def custom_header_auth(
        self,
    ) -> LogsCustomDestinationHttpDestinationCustomHeaderAuthList:
        return typing.cast(LogsCustomDestinationHttpDestinationCustomHeaderAuthList, jsii.get(self, "customHeaderAuth"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationBasicAuth]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationBasicAuth]]], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="customHeaderAuthInput")
    def custom_header_auth_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationCustomHeaderAuth]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationCustomHeaderAuth]]], jsii.get(self, "customHeaderAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90afa86232772b44d41d72831d802fdb3d99d112c04fbb2b9da43a350c81f57b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestination]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestination]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestination]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320b26680534811bf775911032437671e28925c1ab4da018f26d965920eb98a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationSplunkDestination",
    jsii_struct_bases=[],
    name_mapping={"access_token": "accessToken", "endpoint": "endpoint"},
)
class LogsCustomDestinationSplunkDestination:
    def __init__(self, *, access_token: builtins.str, endpoint: builtins.str) -> None:
        '''
        :param access_token: Access token of the Splunk HTTP Event Collector. This field is not returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#access_token LogsCustomDestination#access_token}
        :param endpoint: The destination for which logs will be forwarded to. Must have HTTPS scheme. Forwarding back to Datadog is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#endpoint LogsCustomDestination#endpoint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938e17c35d376e6b087b9e692329662652c68e562443fbb6389cffb557e21b81)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_token": access_token,
            "endpoint": endpoint,
        }

    @builtins.property
    def access_token(self) -> builtins.str:
        '''Access token of the Splunk HTTP Event Collector. This field is not returned by the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#access_token LogsCustomDestination#access_token}
        '''
        result = self._values.get("access_token")
        assert result is not None, "Required property 'access_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''The destination for which logs will be forwarded to.

        Must have HTTPS scheme. Forwarding back to Datadog is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_destination#endpoint LogsCustomDestination#endpoint}
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomDestinationSplunkDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomDestinationSplunkDestinationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationSplunkDestinationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30a26b9610a2efa905af68bf46d1660ccf516f1b8caa2d7711b86ad8995e97e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomDestinationSplunkDestinationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3c445677271b184a16a081cd415fb603e22cc7f94601932d4b835cb3e87adc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomDestinationSplunkDestinationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e59529a3cc5a941f37df73cc851e47146b4160f960861d5ef0f47283d6d52d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b4c7477aee7340619f3160935b79e7b45e52cf0feee15e6a7b06b118044e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78821d98be737f379379e916ba02e28e0c29adf5500493e63d0692e9a772eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationSplunkDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationSplunkDestination]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationSplunkDestination]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02900b52799407b857f5e3c42d2e1de2fc589e1517a214f6428fd12bf275dfef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomDestinationSplunkDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomDestination.LogsCustomDestinationSplunkDestinationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8a55f21ff1576d314af683dae215ad41509c583f45ebe3b5e33caf6a7d364f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2540287a9f9bbdb0c4b9311c284dbeae9fa4be52730061435c14d2fb548556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463a6b95e6909622401afbe6c1ba7ae8c88d6d42aa6ad68d1d539246e7f0d823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationSplunkDestination]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationSplunkDestination]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationSplunkDestination]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92820e86a863b65bce882c416727aed50104cf12431aa5239017f8ebdfdef084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LogsCustomDestination",
    "LogsCustomDestinationConfig",
    "LogsCustomDestinationElasticsearchDestination",
    "LogsCustomDestinationElasticsearchDestinationBasicAuth",
    "LogsCustomDestinationElasticsearchDestinationBasicAuthList",
    "LogsCustomDestinationElasticsearchDestinationBasicAuthOutputReference",
    "LogsCustomDestinationElasticsearchDestinationList",
    "LogsCustomDestinationElasticsearchDestinationOutputReference",
    "LogsCustomDestinationHttpDestination",
    "LogsCustomDestinationHttpDestinationBasicAuth",
    "LogsCustomDestinationHttpDestinationBasicAuthList",
    "LogsCustomDestinationHttpDestinationBasicAuthOutputReference",
    "LogsCustomDestinationHttpDestinationCustomHeaderAuth",
    "LogsCustomDestinationHttpDestinationCustomHeaderAuthList",
    "LogsCustomDestinationHttpDestinationCustomHeaderAuthOutputReference",
    "LogsCustomDestinationHttpDestinationList",
    "LogsCustomDestinationHttpDestinationOutputReference",
    "LogsCustomDestinationSplunkDestination",
    "LogsCustomDestinationSplunkDestinationList",
    "LogsCustomDestinationSplunkDestinationOutputReference",
]

publication.publish()

def _typecheckingstub__cffafdeb14f2844ef4b622cad794e55f9af27d5ab8587da4104ae365c7ccd270(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    elasticsearch_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationElasticsearchDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_tags_restriction_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    forward_tags_restriction_list_type: typing.Optional[builtins.str] = None,
    http_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query: typing.Optional[builtins.str] = None,
    splunk_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationSplunkDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d934d2e9792235c8b3834b047d31eafceeb33f900e7d84b14a4f4d2a64d410(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa089e60b92b4cbd820c192a455423a98866bd42ed12b1e05a2b31a9068b0e0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationElasticsearchDestination, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15afeb22f4f48dca0011b06b0d2f719bd1a3f7cdb202b28f66d5f73b7778efff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestination, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe02f0abef9e5a9b6365bd87ed15e820135a0b7625c205b8b4c348721d2d0f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationSplunkDestination, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4592ebe7e60b5b1c08adfc331419350980468ea886480df52c6bfa38dd26381c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bceb3f437cc72710144ec8e867f1554f975263f8644eddebe57e0ff1c23d07cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5019aeb2d819add2f090b7b2951cd64a75d3d6a7f1a15c1dbc3f144131868e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d83274ce940872562712192a736cc31d6a0973110098a5224083b2e58df29c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87b2eb13dffb9a05861cd81f6b6af9616031867f28c3cf44b11e743390563f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21b43e2826bdb00f312271492ce726a0e96fdbdf06c924b2faffbc1ce4469be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c88721c3253c72502292d77707f3f95e1c1a5ae820385846a967e430c69f68f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    elasticsearch_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationElasticsearchDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    forward_tags_restriction_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    forward_tags_restriction_list_type: typing.Optional[builtins.str] = None,
    http_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query: typing.Optional[builtins.str] = None,
    splunk_destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationSplunkDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741caa8cc4e64b980452f4609d5bb56126270344c66315a0e7b16767fd918f9d(
    *,
    endpoint: builtins.str,
    index_name: builtins.str,
    basic_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationElasticsearchDestinationBasicAuth, typing.Dict[builtins.str, typing.Any]]]]] = None,
    index_rotation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6c0229537ddd998fbff6bc39495545ac22678651c7ba9596231bb4f72404b6(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d032958f3f70d1b85eefe4799194e5c6b0428fd047e09b14edf7afbfc4a958ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b854f495758a44b0349afb258fb617fa088dac6aa66eb0bbd51dda40a4642b3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9e6d437e18a4a4edd1f3b7cebd9d4b9b99d8f18bf8f33252ec26ff16c36131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157502acaa46a4c4080015432b658400c15685208ce7941fdb2c52e5af4e0a96(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c6a18685cb082c18030e2ff14410e08180145dc6d8a53ec5a64d39c4db47ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed39ff8e0a18cf700670676200a58774fb8c209ef6dc6ce63160c62c71ae0ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestinationBasicAuth]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5754669c7f9d814f1866a45be472a3f6d4e1f23e201831ff39c9c40fe6680d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd355697eeec69e0f076f8942872eba10638724a7623a9692347df253080e3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a0f29096f9c69a86a484b4500b7fdcf349515ca39105e61c7c6916fa5d5547(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b37bc8da2b744790335be3b539c090be803256fcdc047c422b3eb7af5c92fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationElasticsearchDestinationBasicAuth]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7503a34c11b4594c068d8ea4bc7eb76fcdeba61385c5ead114a5ada085d3d944(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6590a8095d2949ced5b73ab248f386463ceaed0297fe6db7d80199e7f8e64834(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e050d8b34080f7675c4409f79d2e180b8e10a3ffaababfd3e0a970f497142267(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7553072c6385816677087f3c3959ee5914e7436da3ebb8f1d4b0110b67ca045f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6795384e4afcb8059b629e4730a64e65b0b6c3dc63c2b20efab1eafaf08af7ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8bd3d4a416e6119ef34d3c03ae01b26d75b9b827edd9e739f43f05e7fe0c94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationElasticsearchDestination]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878f41c080c13efd36e6c98698ca4d88bb5cd533d9b3305a699052b90dff565c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841277560373c7f9ce365ce1c6574dce71f2449ad382dfea5345dfdf38da58e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationElasticsearchDestinationBasicAuth, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342f83cdf7ba1a5c91a5b0738aaf3c1bf18e9bc82db2166c2aa72fc7dccc8f98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e07695f5a5ddb2977bdd2593dcafc57ecb3e3730688d554da810bf75e54dfd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307f7926dc7642f56109e9cf3e6903335cfb9abc650526be25f398fea82a6ac7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbeb5ae1dfbca06b0ff86ec68bf02302e711be4bf1a408bcca3cb7ff50a3d64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationElasticsearchDestination]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0608feff39ac62abf5ef4d6a8bd7984c25d77e8dbf4309a08389978bd437b2ef(
    *,
    endpoint: builtins.str,
    basic_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestinationBasicAuth, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_header_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestinationCustomHeaderAuth, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c85b25194c200c2724c9c94bd8b8ffa2459f1b420a31601373adeb5d8262aa(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd73ff27ba901fd1e3e826a37b5c9954e6481919d020a43a96569f182aad4a94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfff52acda7627fa3c17f92afe93d79b17ec224ab17661ba8789b3feed26d0a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9848385a5f26b4ee81afba66dd1fa469f201aa7a58a1ab7166950cb779cff291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f39519f74b8e2b5541ac457187027414be700c91b97515c9ec47b9cf268737(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a09234fa4c2d47befcda9bfbfd85326e260dcec59404364a00ab4747a33866(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0a9a543deb8f6cef89e6569e4137c6f78214152d33e4ebd91b19aa361603a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationBasicAuth]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fedd27001f4d7644c286aa7214e9f428d4cab91cbadf4ff19ad42de0c717618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e159218df0715d57ce4196bb0b52ba91b92ef0a4d179f36054109ef695e5ebb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f5a0eb661103411b6dab23e29f1ab7aae7bd089921dc53cf496cbebd2719f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988d752ce99fbfba2dc2d57153ad9cd1b51fce00e0675e8d10e21d55d047c6ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestinationBasicAuth]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bea779e91bfcb4dd4cc14f5efe5d04bb10f75decb76a9e4b177c86e1375195(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3048f6c21d930a7d5f46ccd3d54ad68996f40adc3e117d0359ba2bfe8be07bad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6392770c725425188386a022bc90f45e15a49426dff3e94e509ed6d52fd4e403(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e56ab18765addb5a67de0a19ffbe5137ff597af3fc2e4bbd8adbfb751f957f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c9840683001c481d06a38a5aac59323c48b9bbac2925ef2bb0ab22166bec7b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026f0ac3c02ee247d4012b8e798e7760991e3e94131524774d8527d2c29827b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a388f638da39d09af7405abf3e180dae4d349565b11d549d20da15e2d0f8c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestinationCustomHeaderAuth]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810706f9a8470f078957929e87344b43b2a772bc1186db58724f533ed56c4f5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bc521c268bdcfd821ef6ff4406b5d03d78d8eee391f16101d94992a34957a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e1722ae00a5a01ed2bc5851982265350e44a119f98a54fc82d076a09a1a5e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fbbfdd436548fddef9ef0276c1715134385e04784dbdbe720974b43e39b989(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestinationCustomHeaderAuth]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77908b8020c2422545c0542a6ea69c8faab1e8d24a246696b5bcc0ac9de9f163(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551a30c66807d1eb17021eb5d63b630f21d52c33c4f62e7507b8486510ae76b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6561d175986716b2471c4434aea3f8f7d760a385b85b9be6dce7f6351b1a15c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bfb6abc4faf32d228209fee5a7561806e37e39d83a3afcc59352e5ae0073cb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c7396a81ef66f2e4bd0ddf25a50c44b866930c159eae94ea20212e1e755a60(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5fabcbd740a72fc0505a60be7e2acf37179d4e66d4872deba767435846e371(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationHttpDestination]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76473078b0a05be725aa8b56df4e8f9da230220ba4884901e793c75656d32f63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e691cf4c3f68aa99f374d9262c98ff0fa23968a39f820e7dd7a44998faea9693(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestinationBasicAuth, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb32b6aa19ed11a34358228702600311daddde81aad0e1ad8b6ee997d93690e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomDestinationHttpDestinationCustomHeaderAuth, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90afa86232772b44d41d72831d802fdb3d99d112c04fbb2b9da43a350c81f57b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320b26680534811bf775911032437671e28925c1ab4da018f26d965920eb98a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationHttpDestination]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938e17c35d376e6b087b9e692329662652c68e562443fbb6389cffb557e21b81(
    *,
    access_token: builtins.str,
    endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30a26b9610a2efa905af68bf46d1660ccf516f1b8caa2d7711b86ad8995e97e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3c445677271b184a16a081cd415fb603e22cc7f94601932d4b835cb3e87adc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e59529a3cc5a941f37df73cc851e47146b4160f960861d5ef0f47283d6d52d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b4c7477aee7340619f3160935b79e7b45e52cf0feee15e6a7b06b118044e18(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78821d98be737f379379e916ba02e28e0c29adf5500493e63d0692e9a772eda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02900b52799407b857f5e3c42d2e1de2fc589e1517a214f6428fd12bf275dfef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomDestinationSplunkDestination]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8a55f21ff1576d314af683dae215ad41509c583f45ebe3b5e33caf6a7d364f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2540287a9f9bbdb0c4b9311c284dbeae9fa4be52730061435c14d2fb548556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463a6b95e6909622401afbe6c1ba7ae8c88d6d42aa6ad68d1d539246e7f0d823(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92820e86a863b65bce882c416727aed50104cf12431aa5239017f8ebdfdef084(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomDestinationSplunkDestination]],
) -> None:
    """Type checking stubs"""
    pass
