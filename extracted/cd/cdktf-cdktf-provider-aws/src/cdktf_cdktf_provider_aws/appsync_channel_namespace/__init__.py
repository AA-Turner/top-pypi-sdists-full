r'''
# `aws_appsync_channel_namespace`

Refer to the Terraform Registry for docs: [`aws_appsync_channel_namespace`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace).
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


class AppsyncChannelNamespace(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespace",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace aws_appsync_channel_namespace}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        name: builtins.str,
        code_handlers: typing.Optional[builtins.str] = None,
        handler_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        publish_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespacePublishAuthMode", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        subscribe_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceSubscribeAuthMode", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace aws_appsync_channel_namespace} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#api_id AppsyncChannelNamespace#api_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#name AppsyncChannelNamespace#name}.
        :param code_handlers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#code_handlers AppsyncChannelNamespace#code_handlers}.
        :param handler_configs: handler_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#handler_configs AppsyncChannelNamespace#handler_configs}
        :param publish_auth_mode: publish_auth_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#publish_auth_mode AppsyncChannelNamespace#publish_auth_mode}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#region AppsyncChannelNamespace#region}
        :param subscribe_auth_mode: subscribe_auth_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#subscribe_auth_mode AppsyncChannelNamespace#subscribe_auth_mode}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#tags AppsyncChannelNamespace#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ae5d646cfc9d39060a8a2625e97b294f77304672e76679994a700290f88130)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AppsyncChannelNamespaceConfig(
            api_id=api_id,
            name=name,
            code_handlers=code_handlers,
            handler_configs=handler_configs,
            publish_auth_mode=publish_auth_mode,
            region=region,
            subscribe_auth_mode=subscribe_auth_mode,
            tags=tags,
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
        '''Generates CDKTF code for importing a AppsyncChannelNamespace resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppsyncChannelNamespace to import.
        :param import_from_id: The id of the existing AppsyncChannelNamespace that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppsyncChannelNamespace to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65464f75bb2ab18b61576d831561e7d6b1a7a9fdbfa433b39cd350faee36d7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHandlerConfigs")
    def put_handler_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039ca61bcc876faf2d6e64f9923a034295e534bd65df7e05d7ce3bd59f7829f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHandlerConfigs", [value]))

    @jsii.member(jsii_name="putPublishAuthMode")
    def put_publish_auth_mode(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespacePublishAuthMode", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c75864829f7178b2d4682acd0b7d7812e11c218ed8f7fbf015a966e2caccf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPublishAuthMode", [value]))

    @jsii.member(jsii_name="putSubscribeAuthMode")
    def put_subscribe_auth_mode(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceSubscribeAuthMode", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53189adcc548e464b2793873f18f75212b1da5f031eb52fa8439939f7665e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubscribeAuthMode", [value]))

    @jsii.member(jsii_name="resetCodeHandlers")
    def reset_code_handlers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeHandlers", []))

    @jsii.member(jsii_name="resetHandlerConfigs")
    def reset_handler_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandlerConfigs", []))

    @jsii.member(jsii_name="resetPublishAuthMode")
    def reset_publish_auth_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishAuthMode", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSubscribeAuthMode")
    def reset_subscribe_auth_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscribeAuthMode", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="channelNamespaceArn")
    def channel_namespace_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelNamespaceArn"))

    @builtins.property
    @jsii.member(jsii_name="handlerConfigs")
    def handler_configs(self) -> "AppsyncChannelNamespaceHandlerConfigsList":
        return typing.cast("AppsyncChannelNamespaceHandlerConfigsList", jsii.get(self, "handlerConfigs"))

    @builtins.property
    @jsii.member(jsii_name="publishAuthMode")
    def publish_auth_mode(self) -> "AppsyncChannelNamespacePublishAuthModeList":
        return typing.cast("AppsyncChannelNamespacePublishAuthModeList", jsii.get(self, "publishAuthMode"))

    @builtins.property
    @jsii.member(jsii_name="subscribeAuthMode")
    def subscribe_auth_mode(self) -> "AppsyncChannelNamespaceSubscribeAuthModeList":
        return typing.cast("AppsyncChannelNamespaceSubscribeAuthModeList", jsii.get(self, "subscribeAuthMode"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="apiIdInput")
    def api_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiIdInput"))

    @builtins.property
    @jsii.member(jsii_name="codeHandlersInput")
    def code_handlers_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeHandlersInput"))

    @builtins.property
    @jsii.member(jsii_name="handlerConfigsInput")
    def handler_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigs"]]], jsii.get(self, "handlerConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publishAuthModeInput")
    def publish_auth_mode_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespacePublishAuthMode"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespacePublishAuthMode"]]], jsii.get(self, "publishAuthModeInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="subscribeAuthModeInput")
    def subscribe_auth_mode_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceSubscribeAuthMode"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceSubscribeAuthMode"]]], jsii.get(self, "subscribeAuthModeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b613f0d0df34db0676c5a7e381bcdd58ab2100eb9122c13b340dadb1223530a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeHandlers")
    def code_handlers(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codeHandlers"))

    @code_handlers.setter
    def code_handlers(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e9cedcf65ae876fc195d146f8a80699a11b71287cbc2750752665ffa99156e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeHandlers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83686ab1f0686fd10212d7149fe52265ec3a44e25eab4412d807767764dc8ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e68cfc068b63b396dcdc801835cfac256c23dda115b1144fedbf076b3792a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc4953e25231a9ee420af0cdfd72e4c5e4338c8488e898e11b36468784a8410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_id": "apiId",
        "name": "name",
        "code_handlers": "codeHandlers",
        "handler_configs": "handlerConfigs",
        "publish_auth_mode": "publishAuthMode",
        "region": "region",
        "subscribe_auth_mode": "subscribeAuthMode",
        "tags": "tags",
    },
)
class AppsyncChannelNamespaceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_id: builtins.str,
        name: builtins.str,
        code_handlers: typing.Optional[builtins.str] = None,
        handler_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        publish_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespacePublishAuthMode", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        subscribe_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceSubscribeAuthMode", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#api_id AppsyncChannelNamespace#api_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#name AppsyncChannelNamespace#name}.
        :param code_handlers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#code_handlers AppsyncChannelNamespace#code_handlers}.
        :param handler_configs: handler_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#handler_configs AppsyncChannelNamespace#handler_configs}
        :param publish_auth_mode: publish_auth_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#publish_auth_mode AppsyncChannelNamespace#publish_auth_mode}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#region AppsyncChannelNamespace#region}
        :param subscribe_auth_mode: subscribe_auth_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#subscribe_auth_mode AppsyncChannelNamespace#subscribe_auth_mode}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#tags AppsyncChannelNamespace#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76dfd36e5401718aa955580f29dff1523d7e47a308df1f740003c547160bbab)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument code_handlers", value=code_handlers, expected_type=type_hints["code_handlers"])
            check_type(argname="argument handler_configs", value=handler_configs, expected_type=type_hints["handler_configs"])
            check_type(argname="argument publish_auth_mode", value=publish_auth_mode, expected_type=type_hints["publish_auth_mode"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument subscribe_auth_mode", value=subscribe_auth_mode, expected_type=type_hints["subscribe_auth_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
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
        if code_handlers is not None:
            self._values["code_handlers"] = code_handlers
        if handler_configs is not None:
            self._values["handler_configs"] = handler_configs
        if publish_auth_mode is not None:
            self._values["publish_auth_mode"] = publish_auth_mode
        if region is not None:
            self._values["region"] = region
        if subscribe_auth_mode is not None:
            self._values["subscribe_auth_mode"] = subscribe_auth_mode
        if tags is not None:
            self._values["tags"] = tags

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
    def api_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#api_id AppsyncChannelNamespace#api_id}.'''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#name AppsyncChannelNamespace#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code_handlers(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#code_handlers AppsyncChannelNamespace#code_handlers}.'''
        result = self._values.get("code_handlers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handler_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigs"]]]:
        '''handler_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#handler_configs AppsyncChannelNamespace#handler_configs}
        '''
        result = self._values.get("handler_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigs"]]], result)

    @builtins.property
    def publish_auth_mode(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespacePublishAuthMode"]]]:
        '''publish_auth_mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#publish_auth_mode AppsyncChannelNamespace#publish_auth_mode}
        '''
        result = self._values.get("publish_auth_mode")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespacePublishAuthMode"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#region AppsyncChannelNamespace#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscribe_auth_mode(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceSubscribeAuthMode"]]]:
        '''subscribe_auth_mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#subscribe_auth_mode AppsyncChannelNamespace#subscribe_auth_mode}
        '''
        result = self._values.get("subscribe_auth_mode")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceSubscribeAuthMode"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#tags AppsyncChannelNamespace#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigs",
    jsii_struct_bases=[],
    name_mapping={"on_publish": "onPublish", "on_subscribe": "onSubscribe"},
)
class AppsyncChannelNamespaceHandlerConfigs:
    def __init__(
        self,
        *,
        on_publish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigsOnPublish", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_subscribe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigsOnSubscribe", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param on_publish: on_publish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#on_publish AppsyncChannelNamespace#on_publish}
        :param on_subscribe: on_subscribe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#on_subscribe AppsyncChannelNamespace#on_subscribe}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65ecd40498140dd37803bcae465bc5b731e16929200692bedb1c9438cc71d73)
            check_type(argname="argument on_publish", value=on_publish, expected_type=type_hints["on_publish"])
            check_type(argname="argument on_subscribe", value=on_subscribe, expected_type=type_hints["on_subscribe"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_publish is not None:
            self._values["on_publish"] = on_publish
        if on_subscribe is not None:
            self._values["on_subscribe"] = on_subscribe

    @builtins.property
    def on_publish(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnPublish"]]]:
        '''on_publish block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#on_publish AppsyncChannelNamespace#on_publish}
        '''
        result = self._values.get("on_publish")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnPublish"]]], result)

    @builtins.property
    def on_subscribe(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnSubscribe"]]]:
        '''on_subscribe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#on_subscribe AppsyncChannelNamespace#on_subscribe}
        '''
        result = self._values.get("on_subscribe")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnSubscribe"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceHandlerConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncChannelNamespaceHandlerConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04bae3c252b6dbca205129aaf805926aa2da618976494c13795cdade99ea7a0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespaceHandlerConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac24b297032b7e1774f4bdf2b55475a52e6824e7d3ad408543d469b6ec454720)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespaceHandlerConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee2711c517f9bd134bcb02e957eb11ec5ed6d20751ccffd984e77d000b8f3f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc804a429dbe00b80b432536fdb8f5163ef7356cc45c60527d8fccbb1a6cbbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97816615162e6e6ad0c7bc664d577c1701619d37d8f9f5064515b188f3254bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495e09224d62d9a7c32ce07ed06cba0f995c3dc17342699f90d9aa6a723629af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublish",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior", "integration": "integration"},
)
class AppsyncChannelNamespaceHandlerConfigsOnPublish:
    def __init__(
        self,
        *,
        behavior: builtins.str,
        integration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#behavior AppsyncChannelNamespace#behavior}.
        :param integration: integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#integration AppsyncChannelNamespace#integration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4003a0ce180cf850e8ae8b72fa1db2d60cee3d8052f393fbcb8c9c23a0c6b77)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
        }
        if integration is not None:
            self._values["integration"] = integration

    @builtins.property
    def behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#behavior AppsyncChannelNamespace#behavior}.'''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration"]]]:
        '''integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#integration AppsyncChannelNamespace#integration}
        '''
        result = self._values.get("integration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceHandlerConfigsOnPublish(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_name": "dataSourceName",
        "lambda_config": "lambdaConfig",
    },
)
class AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration:
    def __init__(
        self,
        *,
        data_source_name: builtins.str,
        lambda_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#data_source_name AppsyncChannelNamespace#data_source_name}.
        :param lambda_config: lambda_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#lambda_config AppsyncChannelNamespace#lambda_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f8fedbfb4edbb57b815da01876fbdb11442c59f6e8fafd10e17d8b1344b1fdf)
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_name": data_source_name,
        }
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config

    @builtins.property
    def data_source_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#data_source_name AppsyncChannelNamespace#data_source_name}.'''
        result = self._values.get("data_source_name")
        assert result is not None, "Required property 'data_source_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig"]]]:
        '''lambda_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#lambda_config AppsyncChannelNamespace#lambda_config}
        '''
        result = self._values.get("lambda_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig",
    jsii_struct_bases=[],
    name_mapping={"invoke_type": "invokeType"},
)
class AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig:
    def __init__(self, *, invoke_type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param invoke_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#invoke_type AppsyncChannelNamespace#invoke_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48231af654eeee0b5d1f46fdd6840bed1e12f0781ea1cdc248dfb33afea87f74)
            check_type(argname="argument invoke_type", value=invoke_type, expected_type=type_hints["invoke_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if invoke_type is not None:
            self._values["invoke_type"] = invoke_type

    @builtins.property
    def invoke_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#invoke_type AppsyncChannelNamespace#invoke_type}.'''
        result = self._values.get("invoke_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71517eff6cd6e16bb235c201ecbca82a590f3b1b637ee9fc189e0008ec0ebe01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d71d522bf4eb5e295a76ea23de9ec89f5a8437d081f3fee9f2374317469818c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c49866517e34136968dc7a95fe128ad975a2c700de634fa160c0b5bf8c898e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dd55fd010caa7a09c300b0429393ff830f9661cde70e986a6496d89057db24c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fa853a514815942e7ccd632d5b16f2775284cf724fd096d76d6bfa47dbb7fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764c9da3aa13273f103e8d6fb2e0f3eb3beb96ec3fa80bb8faba755fd53ab540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c93011337d3df6a799ae4c0363d4956e3f183c045f7cdf20e901a33215165f35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInvokeType")
    def reset_invoke_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvokeType", []))

    @builtins.property
    @jsii.member(jsii_name="invokeTypeInput")
    def invoke_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invokeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="invokeType")
    def invoke_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invokeType"))

    @invoke_type.setter
    def invoke_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d1238b798d719c0c97a5d0e0e844e12f6b02c21cbbafff27c90037e300c1a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invokeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e3934a0854cecc0accab127a2da03d151116c8bb8983360e84e39edb28d134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3cabff9ff34f2c0be1b91a2f55b4bb1231b50ea5c8ddc8041874a740f5a9e71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c23f0813a2f6f3a90b38d67206a2cba46c98658e9690b1f8d610117719237a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43829e22a2b67390246df2967c91bbb425d351c15c60f5688aca4bc54370360)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b43c4ca3688fe25b74fbc12cf8d35420c0e69dc3064c9b1067d217d1b12f0e28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71ec3146eccf9c5515f603ddf50b1e4c3dcc79106b7c2949906149831e876d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c884e3d99c1076642e14587701cc1dd75d75c8e8644d87a8bc898d718e442edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61011cb53c81cd962ffc2395ba352835849519e3c18ee30044010324bda77a17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLambdaConfig")
    def put_lambda_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ea37ef09adb9d6ebf207458b7738f4073614886464602c8a494fc668f2921d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambdaConfig", [value]))

    @jsii.member(jsii_name="resetLambdaConfig")
    def reset_lambda_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaConfig", []))

    @builtins.property
    @jsii.member(jsii_name="lambdaConfig")
    def lambda_config(
        self,
    ) -> AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigList:
        return typing.cast(AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigList, jsii.get(self, "lambdaConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceNameInput")
    def data_source_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaConfigInput")
    def lambda_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]]], jsii.get(self, "lambdaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @data_source_name.setter
    def data_source_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f632e3e0803a8d125ff0fd07c5692ace2dde10fd2866e994bfc3275e6a85f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d87f499962091a53b5929db5357bca212d2b4c6d588f08015d7fca760b68841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnPublishList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublishList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cec9ea7d4e0eafc7c6e636f0a1ff67ac42a7eed0cdd3b02be36edb53c98fe0b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespaceHandlerConfigsOnPublishOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0fcbb84f2cea857613ce6cd04e5891eb408dbe0dd49da79ba6ef408ec9ed7fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespaceHandlerConfigsOnPublishOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5520a6831f6c6681982f89297315c56f558effc6a8499b18dd49995793e1d90f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b1192b09791668e13370bce15e5707c2f6ca5e2f094b003a8befda382d092e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2af9957a814181b0e24b0f7b842b056ff0b164c95df3c80dbd40f497292b6765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublish]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublish]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublish]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef3dd4f61de8bd0ef97e3ec310b0fd1ff47a62f2bda5312b51761a05620f275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnPublishOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnPublishOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__245244f7bb297c3212fc00c2fe511df0a8db58701f5393f5a5da68d8be4a9aa5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIntegration")
    def put_integration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef684f9c0ef71893c4388de358245d80f2c7d1130359fb1ef7af2fb05f126da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIntegration", [value]))

    @jsii.member(jsii_name="resetIntegration")
    def reset_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegration", []))

    @builtins.property
    @jsii.member(jsii_name="integration")
    def integration(
        self,
    ) -> AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationList:
        return typing.cast(AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationList, jsii.get(self, "integration"))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationInput")
    def integration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]]], jsii.get(self, "integrationInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c8ff381d7c67bec5324228c27a89d0c14d07ee3f567f79ff14e12fc3a59890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublish]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublish]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublish]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e295ab3897cf45bccdd392d368bbbf7af8795644462523961dddaf1a2a8b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribe",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior", "integration": "integration"},
)
class AppsyncChannelNamespaceHandlerConfigsOnSubscribe:
    def __init__(
        self,
        *,
        behavior: builtins.str,
        integration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#behavior AppsyncChannelNamespace#behavior}.
        :param integration: integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#integration AppsyncChannelNamespace#integration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc7ccb8c732eee5a5ff43025c59cc996aab66caccb7d94629f1797ed092f2f4)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
        }
        if integration is not None:
            self._values["integration"] = integration

    @builtins.property
    def behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#behavior AppsyncChannelNamespace#behavior}.'''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration"]]]:
        '''integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#integration AppsyncChannelNamespace#integration}
        '''
        result = self._values.get("integration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceHandlerConfigsOnSubscribe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_name": "dataSourceName",
        "lambda_config": "lambdaConfig",
    },
)
class AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration:
    def __init__(
        self,
        *,
        data_source_name: builtins.str,
        lambda_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#data_source_name AppsyncChannelNamespace#data_source_name}.
        :param lambda_config: lambda_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#lambda_config AppsyncChannelNamespace#lambda_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21dcfc1705387540bcdeff4ebb1b0b368d398de4b7e6f702c301a6413ced771c)
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_name": data_source_name,
        }
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config

    @builtins.property
    def data_source_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#data_source_name AppsyncChannelNamespace#data_source_name}.'''
        result = self._values.get("data_source_name")
        assert result is not None, "Required property 'data_source_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig"]]]:
        '''lambda_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#lambda_config AppsyncChannelNamespace#lambda_config}
        '''
        result = self._values.get("lambda_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig",
    jsii_struct_bases=[],
    name_mapping={"invoke_type": "invokeType"},
)
class AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig:
    def __init__(self, *, invoke_type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param invoke_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#invoke_type AppsyncChannelNamespace#invoke_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffcc0918befa865d54828386676c5112fcd11ec7648f7365bba43aab880db21)
            check_type(argname="argument invoke_type", value=invoke_type, expected_type=type_hints["invoke_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if invoke_type is not None:
            self._values["invoke_type"] = invoke_type

    @builtins.property
    def invoke_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#invoke_type AppsyncChannelNamespace#invoke_type}.'''
        result = self._values.get("invoke_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f444084c39ea506117fb1b70811c3a6bd16c8ecab31c821b0f82d176af4d51f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b94318cbb1d8a7784b690c92c52ac50cf602d4d607a7fb90d6907aa4e4e962)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1027652e4d23d10db07ab50bf6015abc6e575c5001df87b2d0d8f551dc61a4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84aada62d43fdde72eefa8e1b6d343317bc605583b21ef12418c77c4ebff7ed4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d1ec3d0387b6bbb984255fed6e1738eb56ac4338c9d4d95b43122c687a99c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304183da7b87c369194ecaedbe19ea265292da2ac2586fe9022c6261b950d369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a664d6aa1409e105a7b741ee2aaf1b97a0134da7942316eb8d94907bac8a9024)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInvokeType")
    def reset_invoke_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvokeType", []))

    @builtins.property
    @jsii.member(jsii_name="invokeTypeInput")
    def invoke_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invokeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="invokeType")
    def invoke_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invokeType"))

    @invoke_type.setter
    def invoke_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb857d0291236245b7dc340765835f286ee4ce2be0ebfed0159685a4229972c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invokeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1dd701f0f7ffdc438baaec27612d29b3d9a3a1052ddc532adbc1f1b819cbd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__791dc99a43c4509b36fb84ad6b5ea3deedfd21402d7ea610b3fdb0f653d757d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e79898633097e4c4cf5c3e73bcb8b9f6e0492238defe44cfda19eea2340c54a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f6b984cf0d2388d5adbb3eb9a78043dec8c60d6289ebddf4beb4d735a583a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__853c7816631502a7ecce6cf3392e1e8b900ecfe75ae7bd4e641655b99366050f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65a268edf1827f067ee45b3421e3c4ebd05c66845cdc419a000bf4e246ff72a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d47e9d69b7b0c4b25ce57b89ab8d8810a3671c231defc6d417df8168f18602c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86b183c0804b818bafd0ce8f319ac77a35b89427c98ad1b9f9ea55765fe5706b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLambdaConfig")
    def put_lambda_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74e0c3697daea33fda6cfebb7b59f89cb1ca9a149dfce6f8ed90a071f64249a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambdaConfig", [value]))

    @jsii.member(jsii_name="resetLambdaConfig")
    def reset_lambda_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaConfig", []))

    @builtins.property
    @jsii.member(jsii_name="lambdaConfig")
    def lambda_config(
        self,
    ) -> AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigList:
        return typing.cast(AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigList, jsii.get(self, "lambdaConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceNameInput")
    def data_source_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaConfigInput")
    def lambda_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]]], jsii.get(self, "lambdaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @data_source_name.setter
    def data_source_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfafa46f4bc8eb9195b3d5f14261e713d56df7e85e4146496e4960fc85f0743a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43558941ddc01354699729e77d503e77f2ba7ab67805aed2dd5de9bd8ae0151e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnSubscribeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0d8395458fc498a71c205d68310689342e2277eeab0768a40d90a2d243ab28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespaceHandlerConfigsOnSubscribeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbf89a5baf67a19eabeaa46d0052b238f644eaa335a9ff6dfa3cc81eb62d830)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespaceHandlerConfigsOnSubscribeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a9c6c000c3d233c68a199ae7ba2d19d28cabcf4ebcba354682be65c007d716)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1906e2747d1484de1b740c59bb643725a7918daebad2a12f94e19b473d89b9d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89493bf60d6741dc5e6ebe24629214f9427b4bed34fafd47b77c064ece0f7927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribe]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribe]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a0097b5b80d492e2ecb864321a56be349e02ca49982f1662c0e890902fc565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOnSubscribeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOnSubscribeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8029ff6d0993d8f5a0c3b531ab2f3a8e54d18eceb7fb52e1ec213d775ab5075b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIntegration")
    def put_integration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0119d99859e673d7f6de569edc5f668b12547c1e220b837ef8e82b3e2ea0966c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIntegration", [value]))

    @jsii.member(jsii_name="resetIntegration")
    def reset_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegration", []))

    @builtins.property
    @jsii.member(jsii_name="integration")
    def integration(
        self,
    ) -> AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationList:
        return typing.cast(AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationList, jsii.get(self, "integration"))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationInput")
    def integration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]]], jsii.get(self, "integrationInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb32484f6c7e5e9efe8512c77d7bf4844426eae817bf48d289c795a70a3fc41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribe]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribe]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribe]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0167ac0c85f8070f0278812016bad6dbda98a528833ad5bf9b499ad33e388c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceHandlerConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceHandlerConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f880a3801492389b93e1c49631e883869bcc8513af366d4b7d568becfe077d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOnPublish")
    def put_on_publish(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublish, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c88385f6cd0a51ce1ff0ae9e8729bb8e02cf7a032081b5eb0f6ad89f889edfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOnPublish", [value]))

    @jsii.member(jsii_name="putOnSubscribe")
    def put_on_subscribe(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribe, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0877c4d9bd79c4b344388a12ad51f27a5c7942d21ae67474e7de2e7c44be8317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOnSubscribe", [value]))

    @jsii.member(jsii_name="resetOnPublish")
    def reset_on_publish(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPublish", []))

    @jsii.member(jsii_name="resetOnSubscribe")
    def reset_on_subscribe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnSubscribe", []))

    @builtins.property
    @jsii.member(jsii_name="onPublish")
    def on_publish(self) -> AppsyncChannelNamespaceHandlerConfigsOnPublishList:
        return typing.cast(AppsyncChannelNamespaceHandlerConfigsOnPublishList, jsii.get(self, "onPublish"))

    @builtins.property
    @jsii.member(jsii_name="onSubscribe")
    def on_subscribe(self) -> AppsyncChannelNamespaceHandlerConfigsOnSubscribeList:
        return typing.cast(AppsyncChannelNamespaceHandlerConfigsOnSubscribeList, jsii.get(self, "onSubscribe"))

    @builtins.property
    @jsii.member(jsii_name="onPublishInput")
    def on_publish_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublish]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublish]]], jsii.get(self, "onPublishInput"))

    @builtins.property
    @jsii.member(jsii_name="onSubscribeInput")
    def on_subscribe_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribe]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribe]]], jsii.get(self, "onSubscribeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306de20f3b4945bc18c535fce1e2aacdeb1b7b407fdca1217ee910e16cd7121e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespacePublishAuthMode",
    jsii_struct_bases=[],
    name_mapping={"auth_type": "authType"},
)
class AppsyncChannelNamespacePublishAuthMode:
    def __init__(self, *, auth_type: builtins.str) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#auth_type AppsyncChannelNamespace#auth_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec95cb4588d3800bd202e8ca4b070a9b05145d58e1f40550c6a9fa0492708d37)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
        }

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#auth_type AppsyncChannelNamespace#auth_type}.'''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespacePublishAuthMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncChannelNamespacePublishAuthModeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespacePublishAuthModeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcc311d3ad898efe40479d3bcff4bde8bb75597972fa2e4ffddf25e19b4e7292)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespacePublishAuthModeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad313ed3b907350c3870f96d5649878021de370148240c6f5aef058a2d9de3ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespacePublishAuthModeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3714d28da2e55c7ef72b789f660bbfcb3bca25302f2e66c616568361369ff986)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c6f9cf6102cd413bd1eb48d13d502b3c346fb70022e792f00261005351efdf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67b77f74a92169253ec4aac1cf4cd94934aa22044f6796b325d358b583413de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespacePublishAuthMode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespacePublishAuthMode]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespacePublishAuthMode]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa74e2c3bd43ed128d4a4e8b793287f806eb22377dedc1f41fd56eedd9e5c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespacePublishAuthModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespacePublishAuthModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b61ade004f227bcb2d55f8835fa1da11bf2ae63cca5c388b83c05a358e40e82e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fada15c843bb18654e7d2588d689b260220a230228d3e043f9aaad2d0a61d46e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespacePublishAuthMode]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespacePublishAuthMode]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespacePublishAuthMode]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372759874b08f2c88d739f182f06226bf48d1f21c3f16cf2c019628d29cc9300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceSubscribeAuthMode",
    jsii_struct_bases=[],
    name_mapping={"auth_type": "authType"},
)
class AppsyncChannelNamespaceSubscribeAuthMode:
    def __init__(self, *, auth_type: builtins.str) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#auth_type AppsyncChannelNamespace#auth_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__658a9348444c76097fb4fc1d105ba8be31d604e780065ffa713fc707afa17eb0)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
        }

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_channel_namespace#auth_type AppsyncChannelNamespace#auth_type}.'''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncChannelNamespaceSubscribeAuthMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncChannelNamespaceSubscribeAuthModeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceSubscribeAuthModeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__870046db99aee907f3a6468d951163124e0ada69f773b2678e446b76c587d048)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncChannelNamespaceSubscribeAuthModeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1c318538b537ecd0f787a341a2ba6e4112ca945a8a95f86e4c602736d9dc61)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncChannelNamespaceSubscribeAuthModeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6829e00ad440be0cedbb7c393fda7a82953ec03eeb3786eb782c54929ef3b676)
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
            type_hints = typing.get_type_hints(_typecheckingstub__929a312dbf47ba9437e469a20cadd7874c15342a2afc3b97df018af9a65fdd0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__310f447bd2960901e5f505b53aacd27062b07c36836db6b73a67267e074e578e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceSubscribeAuthMode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceSubscribeAuthMode]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceSubscribeAuthMode]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae894a12a307e2501f0fd7d496e7c6876d399488626f3c73cbc9af836bd42909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncChannelNamespaceSubscribeAuthModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncChannelNamespace.AppsyncChannelNamespaceSubscribeAuthModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c97e3822a41827aafdb479153a7bbd85746c3b98d871fad8f47b68eb4a52c7ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ffd5832b004b91f739d160b40d98aeaecd308013cc59bedfe0ba7ff44492eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceSubscribeAuthMode]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceSubscribeAuthMode]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceSubscribeAuthMode]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45babb8a30ad9c1e04fc61d081dea4e925565655388e051b025027c278e62dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppsyncChannelNamespace",
    "AppsyncChannelNamespaceConfig",
    "AppsyncChannelNamespaceHandlerConfigs",
    "AppsyncChannelNamespaceHandlerConfigsList",
    "AppsyncChannelNamespaceHandlerConfigsOnPublish",
    "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration",
    "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig",
    "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigList",
    "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfigOutputReference",
    "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationList",
    "AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationOutputReference",
    "AppsyncChannelNamespaceHandlerConfigsOnPublishList",
    "AppsyncChannelNamespaceHandlerConfigsOnPublishOutputReference",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribe",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigList",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfigOutputReference",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationList",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationOutputReference",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribeList",
    "AppsyncChannelNamespaceHandlerConfigsOnSubscribeOutputReference",
    "AppsyncChannelNamespaceHandlerConfigsOutputReference",
    "AppsyncChannelNamespacePublishAuthMode",
    "AppsyncChannelNamespacePublishAuthModeList",
    "AppsyncChannelNamespacePublishAuthModeOutputReference",
    "AppsyncChannelNamespaceSubscribeAuthMode",
    "AppsyncChannelNamespaceSubscribeAuthModeList",
    "AppsyncChannelNamespaceSubscribeAuthModeOutputReference",
]

publication.publish()

def _typecheckingstub__b8ae5d646cfc9d39060a8a2625e97b294f77304672e76679994a700290f88130(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api_id: builtins.str,
    name: builtins.str,
    code_handlers: typing.Optional[builtins.str] = None,
    handler_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    publish_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespacePublishAuthMode, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    subscribe_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceSubscribeAuthMode, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__f65464f75bb2ab18b61576d831561e7d6b1a7a9fdbfa433b39cd350faee36d7f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039ca61bcc876faf2d6e64f9923a034295e534bd65df7e05d7ce3bd59f7829f4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c75864829f7178b2d4682acd0b7d7812e11c218ed8f7fbf015a966e2caccf0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespacePublishAuthMode, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53189adcc548e464b2793873f18f75212b1da5f031eb52fa8439939f7665e70(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceSubscribeAuthMode, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b613f0d0df34db0676c5a7e381bcdd58ab2100eb9122c13b340dadb1223530a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e9cedcf65ae876fc195d146f8a80699a11b71287cbc2750752665ffa99156e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83686ab1f0686fd10212d7149fe52265ec3a44e25eab4412d807767764dc8ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e68cfc068b63b396dcdc801835cfac256c23dda115b1144fedbf076b3792a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc4953e25231a9ee420af0cdfd72e4c5e4338c8488e898e11b36468784a8410(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76dfd36e5401718aa955580f29dff1523d7e47a308df1f740003c547160bbab(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_id: builtins.str,
    name: builtins.str,
    code_handlers: typing.Optional[builtins.str] = None,
    handler_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    publish_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespacePublishAuthMode, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    subscribe_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceSubscribeAuthMode, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65ecd40498140dd37803bcae465bc5b731e16929200692bedb1c9438cc71d73(
    *,
    on_publish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublish, typing.Dict[builtins.str, typing.Any]]]]] = None,
    on_subscribe: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribe, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bae3c252b6dbca205129aaf805926aa2da618976494c13795cdade99ea7a0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac24b297032b7e1774f4bdf2b55475a52e6824e7d3ad408543d469b6ec454720(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee2711c517f9bd134bcb02e957eb11ec5ed6d20751ccffd984e77d000b8f3f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc804a429dbe00b80b432536fdb8f5163ef7356cc45c60527d8fccbb1a6cbbe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97816615162e6e6ad0c7bc664d577c1701619d37d8f9f5064515b188f3254bc3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495e09224d62d9a7c32ce07ed06cba0f995c3dc17342699f90d9aa6a723629af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4003a0ce180cf850e8ae8b72fa1db2d60cee3d8052f393fbcb8c9c23a0c6b77(
    *,
    behavior: builtins.str,
    integration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8fedbfb4edbb57b815da01876fbdb11442c59f6e8fafd10e17d8b1344b1fdf(
    *,
    data_source_name: builtins.str,
    lambda_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48231af654eeee0b5d1f46fdd6840bed1e12f0781ea1cdc248dfb33afea87f74(
    *,
    invoke_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71517eff6cd6e16bb235c201ecbca82a590f3b1b637ee9fc189e0008ec0ebe01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d71d522bf4eb5e295a76ea23de9ec89f5a8437d081f3fee9f2374317469818c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c49866517e34136968dc7a95fe128ad975a2c700de634fa160c0b5bf8c898e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd55fd010caa7a09c300b0429393ff830f9661cde70e986a6496d89057db24c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa853a514815942e7ccd632d5b16f2775284cf724fd096d76d6bfa47dbb7fc3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764c9da3aa13273f103e8d6fb2e0f3eb3beb96ec3fa80bb8faba755fd53ab540(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93011337d3df6a799ae4c0363d4956e3f183c045f7cdf20e901a33215165f35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1238b798d719c0c97a5d0e0e844e12f6b02c21cbbafff27c90037e300c1a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e3934a0854cecc0accab127a2da03d151116c8bb8983360e84e39edb28d134(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3cabff9ff34f2c0be1b91a2f55b4bb1231b50ea5c8ddc8041874a740f5a9e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c23f0813a2f6f3a90b38d67206a2cba46c98658e9690b1f8d610117719237a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43829e22a2b67390246df2967c91bbb425d351c15c60f5688aca4bc54370360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43c4ca3688fe25b74fbc12cf8d35420c0e69dc3064c9b1067d217d1b12f0e28(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ec3146eccf9c5515f603ddf50b1e4c3dcc79106b7c2949906149831e876d62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c884e3d99c1076642e14587701cc1dd75d75c8e8644d87a8bc898d718e442edb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61011cb53c81cd962ffc2395ba352835849519e3c18ee30044010324bda77a17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ea37ef09adb9d6ebf207458b7738f4073614886464602c8a494fc668f2921d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegrationLambdaConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f632e3e0803a8d125ff0fd07c5692ace2dde10fd2866e994bfc3275e6a85f6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d87f499962091a53b5929db5357bca212d2b4c6d588f08015d7fca760b68841(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec9ea7d4e0eafc7c6e636f0a1ff67ac42a7eed0cdd3b02be36edb53c98fe0b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fcbb84f2cea857613ce6cd04e5891eb408dbe0dd49da79ba6ef408ec9ed7fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5520a6831f6c6681982f89297315c56f558effc6a8499b18dd49995793e1d90f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1192b09791668e13370bce15e5707c2f6ca5e2f094b003a8befda382d092e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af9957a814181b0e24b0f7b842b056ff0b164c95df3c80dbd40f497292b6765(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef3dd4f61de8bd0ef97e3ec310b0fd1ff47a62f2bda5312b51761a05620f275(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnPublish]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245244f7bb297c3212fc00c2fe511df0a8db58701f5393f5a5da68d8be4a9aa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef684f9c0ef71893c4388de358245d80f2c7d1130359fb1ef7af2fb05f126da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublishIntegration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c8ff381d7c67bec5324228c27a89d0c14d07ee3f567f79ff14e12fc3a59890(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e295ab3897cf45bccdd392d368bbbf7af8795644462523961dddaf1a2a8b55(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnPublish]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc7ccb8c732eee5a5ff43025c59cc996aab66caccb7d94629f1797ed092f2f4(
    *,
    behavior: builtins.str,
    integration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21dcfc1705387540bcdeff4ebb1b0b368d398de4b7e6f702c301a6413ced771c(
    *,
    data_source_name: builtins.str,
    lambda_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffcc0918befa865d54828386676c5112fcd11ec7648f7365bba43aab880db21(
    *,
    invoke_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f444084c39ea506117fb1b70811c3a6bd16c8ecab31c821b0f82d176af4d51f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b94318cbb1d8a7784b690c92c52ac50cf602d4d607a7fb90d6907aa4e4e962(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1027652e4d23d10db07ab50bf6015abc6e575c5001df87b2d0d8f551dc61a4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84aada62d43fdde72eefa8e1b6d343317bc605583b21ef12418c77c4ebff7ed4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1ec3d0387b6bbb984255fed6e1738eb56ac4338c9d4d95b43122c687a99c64(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304183da7b87c369194ecaedbe19ea265292da2ac2586fe9022c6261b950d369(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a664d6aa1409e105a7b741ee2aaf1b97a0134da7942316eb8d94907bac8a9024(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb857d0291236245b7dc340765835f286ee4ce2be0ebfed0159685a4229972c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1dd701f0f7ffdc438baaec27612d29b3d9a3a1052ddc532adbc1f1b819cbd1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791dc99a43c4509b36fb84ad6b5ea3deedfd21402d7ea610b3fdb0f653d757d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e79898633097e4c4cf5c3e73bcb8b9f6e0492238defe44cfda19eea2340c54a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f6b984cf0d2388d5adbb3eb9a78043dec8c60d6289ebddf4beb4d735a583a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853c7816631502a7ecce6cf3392e1e8b900ecfe75ae7bd4e641655b99366050f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a268edf1827f067ee45b3421e3c4ebd05c66845cdc419a000bf4e246ff72a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d47e9d69b7b0c4b25ce57b89ab8d8810a3671c231defc6d417df8168f18602c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b183c0804b818bafd0ce8f319ac77a35b89427c98ad1b9f9ea55765fe5706b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74e0c3697daea33fda6cfebb7b59f89cb1ca9a149dfce6f8ed90a071f64249a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegrationLambdaConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfafa46f4bc8eb9195b3d5f14261e713d56df7e85e4146496e4960fc85f0743a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43558941ddc01354699729e77d503e77f2ba7ab67805aed2dd5de9bd8ae0151e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0d8395458fc498a71c205d68310689342e2277eeab0768a40d90a2d243ab28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbf89a5baf67a19eabeaa46d0052b238f644eaa335a9ff6dfa3cc81eb62d830(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a9c6c000c3d233c68a199ae7ba2d19d28cabcf4ebcba354682be65c007d716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1906e2747d1484de1b740c59bb643725a7918daebad2a12f94e19b473d89b9d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89493bf60d6741dc5e6ebe24629214f9427b4bed34fafd47b77c064ece0f7927(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a0097b5b80d492e2ecb864321a56be349e02ca49982f1662c0e890902fc565(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceHandlerConfigsOnSubscribe]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8029ff6d0993d8f5a0c3b531ab2f3a8e54d18eceb7fb52e1ec213d775ab5075b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0119d99859e673d7f6de569edc5f668b12547c1e220b837ef8e82b3e2ea0966c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribeIntegration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb32484f6c7e5e9efe8512c77d7bf4844426eae817bf48d289c795a70a3fc41e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0167ac0c85f8070f0278812016bad6dbda98a528833ad5bf9b499ad33e388c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigsOnSubscribe]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f880a3801492389b93e1c49631e883869bcc8513af366d4b7d568becfe077d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c88385f6cd0a51ce1ff0ae9e8729bb8e02cf7a032081b5eb0f6ad89f889edfc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnPublish, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0877c4d9bd79c4b344388a12ad51f27a5c7942d21ae67474e7de2e7c44be8317(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncChannelNamespaceHandlerConfigsOnSubscribe, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306de20f3b4945bc18c535fce1e2aacdeb1b7b407fdca1217ee910e16cd7121e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceHandlerConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec95cb4588d3800bd202e8ca4b070a9b05145d58e1f40550c6a9fa0492708d37(
    *,
    auth_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc311d3ad898efe40479d3bcff4bde8bb75597972fa2e4ffddf25e19b4e7292(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad313ed3b907350c3870f96d5649878021de370148240c6f5aef058a2d9de3ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3714d28da2e55c7ef72b789f660bbfcb3bca25302f2e66c616568361369ff986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6f9cf6102cd413bd1eb48d13d502b3c346fb70022e792f00261005351efdf4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b77f74a92169253ec4aac1cf4cd94934aa22044f6796b325d358b583413de8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa74e2c3bd43ed128d4a4e8b793287f806eb22377dedc1f41fd56eedd9e5c3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespacePublishAuthMode]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61ade004f227bcb2d55f8835fa1da11bf2ae63cca5c388b83c05a358e40e82e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fada15c843bb18654e7d2588d689b260220a230228d3e043f9aaad2d0a61d46e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372759874b08f2c88d739f182f06226bf48d1f21c3f16cf2c019628d29cc9300(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespacePublishAuthMode]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658a9348444c76097fb4fc1d105ba8be31d604e780065ffa713fc707afa17eb0(
    *,
    auth_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__870046db99aee907f3a6468d951163124e0ada69f773b2678e446b76c587d048(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1c318538b537ecd0f787a341a2ba6e4112ca945a8a95f86e4c602736d9dc61(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6829e00ad440be0cedbb7c393fda7a82953ec03eeb3786eb782c54929ef3b676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929a312dbf47ba9437e469a20cadd7874c15342a2afc3b97df018af9a65fdd0a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310f447bd2960901e5f505b53aacd27062b07c36836db6b73a67267e074e578e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae894a12a307e2501f0fd7d496e7c6876d399488626f3c73cbc9af836bd42909(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncChannelNamespaceSubscribeAuthMode]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97e3822a41827aafdb479153a7bbd85746c3b98d871fad8f47b68eb4a52c7ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ffd5832b004b91f739d160b40d98aeaecd308013cc59bedfe0ba7ff44492eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45babb8a30ad9c1e04fc61d081dea4e925565655388e051b025027c278e62dd9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncChannelNamespaceSubscribeAuthMode]],
) -> None:
    """Type checking stubs"""
    pass
