r'''
# `opentelekomcloud_as_lifecycle_hook_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_as_lifecycle_hook_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1).
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


class AsLifecycleHookV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.asLifecycleHookV1.AsLifecycleHookV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1 opentelekomcloud_as_lifecycle_hook_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        notification_topic_urn: builtins.str,
        scaling_group_id: builtins.str,
        scaling_lifecycle_hook_name: builtins.str,
        scaling_lifecycle_hook_type: builtins.str,
        default_result: typing.Optional[builtins.str] = None,
        default_timeout: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1 opentelekomcloud_as_lifecycle_hook_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param notification_topic_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#notification_topic_urn AsLifecycleHookV1#notification_topic_urn}.
        :param scaling_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_group_id AsLifecycleHookV1#scaling_group_id}.
        :param scaling_lifecycle_hook_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_lifecycle_hook_name AsLifecycleHookV1#scaling_lifecycle_hook_name}.
        :param scaling_lifecycle_hook_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_lifecycle_hook_type AsLifecycleHookV1#scaling_lifecycle_hook_type}.
        :param default_result: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#default_result AsLifecycleHookV1#default_result}.
        :param default_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#default_timeout AsLifecycleHookV1#default_timeout}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#id AsLifecycleHookV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#notification_metadata AsLifecycleHookV1#notification_metadata}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9edd41b263fc6a53d76e5932c49e4eef63477cfb7b9297fa8d3d39430df2a0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AsLifecycleHookV1Config(
            notification_topic_urn=notification_topic_urn,
            scaling_group_id=scaling_group_id,
            scaling_lifecycle_hook_name=scaling_lifecycle_hook_name,
            scaling_lifecycle_hook_type=scaling_lifecycle_hook_type,
            default_result=default_result,
            default_timeout=default_timeout,
            id=id,
            notification_metadata=notification_metadata,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a AsLifecycleHookV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AsLifecycleHookV1 to import.
        :param import_from_id: The id of the existing AsLifecycleHookV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AsLifecycleHookV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2267dee570c9723928dbad38019ab09f7127c41b7c300713e46e6965e179d7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDefaultResult")
    def reset_default_result(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResult", []))

    @jsii.member(jsii_name="resetDefaultTimeout")
    def reset_default_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTimeout", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotificationMetadata")
    def reset_notification_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationMetadata", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="notificationTopicName")
    def notification_topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationTopicName"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="defaultResultInput")
    def default_result_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultResultInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTimeoutInput")
    def default_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationMetadataInput")
    def notification_metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationTopicUrnInput")
    def notification_topic_urn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTopicUrnInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingGroupIdInput")
    def scaling_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingLifecycleHookNameInput")
    def scaling_lifecycle_hook_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingLifecycleHookNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingLifecycleHookTypeInput")
    def scaling_lifecycle_hook_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingLifecycleHookTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResult")
    def default_result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultResult"))

    @default_result.setter
    def default_result(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574817ea817453516b230d3b68dc9eb6a7e5a425db32a0a6610ca45935bc9548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTimeout")
    def default_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTimeout"))

    @default_timeout.setter
    def default_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57ec0f533c3295856b7af72d303e8356dcfb86abc0839d8404869577a8c72cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf5531cbe6f180896549b1b59e6e66a1e96933be5d1cb16b320fe7006572e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationMetadata")
    def notification_metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationMetadata"))

    @notification_metadata.setter
    def notification_metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a056f55b2dce2256446f191943f08ffc684dfc9bd4600c84f1b27a7bd2b9e76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationTopicUrn")
    def notification_topic_urn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationTopicUrn"))

    @notification_topic_urn.setter
    def notification_topic_urn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf1e31578ac9939515f602ab516682b5bd8e348cedd4775ab10ac8f000387d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationTopicUrn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingGroupId")
    def scaling_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingGroupId"))

    @scaling_group_id.setter
    def scaling_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fab7bb6633b777fa4dcc6b3c051c29397140a486dfa50da5989fcec923d1611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingLifecycleHookName")
    def scaling_lifecycle_hook_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingLifecycleHookName"))

    @scaling_lifecycle_hook_name.setter
    def scaling_lifecycle_hook_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cfb1dd0c1962a59839b59c23120ec487a72fdcd4ac4288a91d122b4f030a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingLifecycleHookName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingLifecycleHookType")
    def scaling_lifecycle_hook_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingLifecycleHookType"))

    @scaling_lifecycle_hook_type.setter
    def scaling_lifecycle_hook_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c3045d880dd60558556469f1edc20903f4624a8dd8ce3bcbe7570fd7585cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingLifecycleHookType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.asLifecycleHookV1.AsLifecycleHookV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "notification_topic_urn": "notificationTopicUrn",
        "scaling_group_id": "scalingGroupId",
        "scaling_lifecycle_hook_name": "scalingLifecycleHookName",
        "scaling_lifecycle_hook_type": "scalingLifecycleHookType",
        "default_result": "defaultResult",
        "default_timeout": "defaultTimeout",
        "id": "id",
        "notification_metadata": "notificationMetadata",
    },
)
class AsLifecycleHookV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        notification_topic_urn: builtins.str,
        scaling_group_id: builtins.str,
        scaling_lifecycle_hook_name: builtins.str,
        scaling_lifecycle_hook_type: builtins.str,
        default_result: typing.Optional[builtins.str] = None,
        default_timeout: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param notification_topic_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#notification_topic_urn AsLifecycleHookV1#notification_topic_urn}.
        :param scaling_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_group_id AsLifecycleHookV1#scaling_group_id}.
        :param scaling_lifecycle_hook_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_lifecycle_hook_name AsLifecycleHookV1#scaling_lifecycle_hook_name}.
        :param scaling_lifecycle_hook_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_lifecycle_hook_type AsLifecycleHookV1#scaling_lifecycle_hook_type}.
        :param default_result: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#default_result AsLifecycleHookV1#default_result}.
        :param default_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#default_timeout AsLifecycleHookV1#default_timeout}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#id AsLifecycleHookV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#notification_metadata AsLifecycleHookV1#notification_metadata}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a90bfceea5bfebdcc30c41c20f8c992d9c1fa75278b4fd556f848a7b6e1ac7d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument notification_topic_urn", value=notification_topic_urn, expected_type=type_hints["notification_topic_urn"])
            check_type(argname="argument scaling_group_id", value=scaling_group_id, expected_type=type_hints["scaling_group_id"])
            check_type(argname="argument scaling_lifecycle_hook_name", value=scaling_lifecycle_hook_name, expected_type=type_hints["scaling_lifecycle_hook_name"])
            check_type(argname="argument scaling_lifecycle_hook_type", value=scaling_lifecycle_hook_type, expected_type=type_hints["scaling_lifecycle_hook_type"])
            check_type(argname="argument default_result", value=default_result, expected_type=type_hints["default_result"])
            check_type(argname="argument default_timeout", value=default_timeout, expected_type=type_hints["default_timeout"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_metadata", value=notification_metadata, expected_type=type_hints["notification_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notification_topic_urn": notification_topic_urn,
            "scaling_group_id": scaling_group_id,
            "scaling_lifecycle_hook_name": scaling_lifecycle_hook_name,
            "scaling_lifecycle_hook_type": scaling_lifecycle_hook_type,
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
        if default_result is not None:
            self._values["default_result"] = default_result
        if default_timeout is not None:
            self._values["default_timeout"] = default_timeout
        if id is not None:
            self._values["id"] = id
        if notification_metadata is not None:
            self._values["notification_metadata"] = notification_metadata

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
    def notification_topic_urn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#notification_topic_urn AsLifecycleHookV1#notification_topic_urn}.'''
        result = self._values.get("notification_topic_urn")
        assert result is not None, "Required property 'notification_topic_urn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_group_id AsLifecycleHookV1#scaling_group_id}.'''
        result = self._values.get("scaling_group_id")
        assert result is not None, "Required property 'scaling_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_lifecycle_hook_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_lifecycle_hook_name AsLifecycleHookV1#scaling_lifecycle_hook_name}.'''
        result = self._values.get("scaling_lifecycle_hook_name")
        assert result is not None, "Required property 'scaling_lifecycle_hook_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_lifecycle_hook_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#scaling_lifecycle_hook_type AsLifecycleHookV1#scaling_lifecycle_hook_type}.'''
        result = self._values.get("scaling_lifecycle_hook_type")
        assert result is not None, "Required property 'scaling_lifecycle_hook_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_result(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#default_result AsLifecycleHookV1#default_result}.'''
        result = self._values.get("default_result")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#default_timeout AsLifecycleHookV1#default_timeout}.'''
        result = self._values.get("default_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#id AsLifecycleHookV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_metadata(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/as_lifecycle_hook_v1#notification_metadata AsLifecycleHookV1#notification_metadata}.'''
        result = self._values.get("notification_metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AsLifecycleHookV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AsLifecycleHookV1",
    "AsLifecycleHookV1Config",
]

publication.publish()

def _typecheckingstub__a9edd41b263fc6a53d76e5932c49e4eef63477cfb7b9297fa8d3d39430df2a0e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    notification_topic_urn: builtins.str,
    scaling_group_id: builtins.str,
    scaling_lifecycle_hook_name: builtins.str,
    scaling_lifecycle_hook_type: builtins.str,
    default_result: typing.Optional[builtins.str] = None,
    default_timeout: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    notification_metadata: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d2267dee570c9723928dbad38019ab09f7127c41b7c300713e46e6965e179d7d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574817ea817453516b230d3b68dc9eb6a7e5a425db32a0a6610ca45935bc9548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57ec0f533c3295856b7af72d303e8356dcfb86abc0839d8404869577a8c72cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf5531cbe6f180896549b1b59e6e66a1e96933be5d1cb16b320fe7006572e96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a056f55b2dce2256446f191943f08ffc684dfc9bd4600c84f1b27a7bd2b9e76f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf1e31578ac9939515f602ab516682b5bd8e348cedd4775ab10ac8f000387d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fab7bb6633b777fa4dcc6b3c051c29397140a486dfa50da5989fcec923d1611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cfb1dd0c1962a59839b59c23120ec487a72fdcd4ac4288a91d122b4f030a63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c3045d880dd60558556469f1edc20903f4624a8dd8ce3bcbe7570fd7585cac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a90bfceea5bfebdcc30c41c20f8c992d9c1fa75278b4fd556f848a7b6e1ac7d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    notification_topic_urn: builtins.str,
    scaling_group_id: builtins.str,
    scaling_lifecycle_hook_name: builtins.str,
    scaling_lifecycle_hook_type: builtins.str,
    default_result: typing.Optional[builtins.str] = None,
    default_timeout: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    notification_metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
