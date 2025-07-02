r'''
# `azurerm_hpc_cache_nfs_target`

Refer to the Terraform Registry for docs: [`azurerm_hpc_cache_nfs_target`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target).
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


class HpcCacheNfsTarget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCacheNfsTarget.HpcCacheNfsTarget",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target azurerm_hpc_cache_nfs_target}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cache_name: builtins.str,
        name: builtins.str,
        namespace_junction: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HpcCacheNfsTargetNamespaceJunction", typing.Dict[builtins.str, typing.Any]]]],
        resource_group_name: builtins.str,
        target_host_name: builtins.str,
        usage_model: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["HpcCacheNfsTargetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        verification_timer_in_seconds: typing.Optional[jsii.Number] = None,
        write_back_timer_in_seconds: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target azurerm_hpc_cache_nfs_target} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cache_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#cache_name HpcCacheNfsTarget#cache_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#name HpcCacheNfsTarget#name}.
        :param namespace_junction: namespace_junction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#namespace_junction HpcCacheNfsTarget#namespace_junction}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#resource_group_name HpcCacheNfsTarget#resource_group_name}.
        :param target_host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#target_host_name HpcCacheNfsTarget#target_host_name}.
        :param usage_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#usage_model HpcCacheNfsTarget#usage_model}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#id HpcCacheNfsTarget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#timeouts HpcCacheNfsTarget#timeouts}
        :param verification_timer_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#verification_timer_in_seconds HpcCacheNfsTarget#verification_timer_in_seconds}.
        :param write_back_timer_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#write_back_timer_in_seconds HpcCacheNfsTarget#write_back_timer_in_seconds}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24696c3f0207aba6f14a74c1371a8e0a83bf3ccd18311ff8a96f0ca67d99c26)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HpcCacheNfsTargetConfig(
            cache_name=cache_name,
            name=name,
            namespace_junction=namespace_junction,
            resource_group_name=resource_group_name,
            target_host_name=target_host_name,
            usage_model=usage_model,
            id=id,
            timeouts=timeouts,
            verification_timer_in_seconds=verification_timer_in_seconds,
            write_back_timer_in_seconds=write_back_timer_in_seconds,
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
        '''Generates CDKTF code for importing a HpcCacheNfsTarget resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HpcCacheNfsTarget to import.
        :param import_from_id: The id of the existing HpcCacheNfsTarget that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HpcCacheNfsTarget to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c311feba8ca86cfc5399dfab9a219722ef9a19bafd7fc60d8769518a4626782f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putNamespaceJunction")
    def put_namespace_junction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HpcCacheNfsTargetNamespaceJunction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da937143ee18642add39c330307f280fff170eb7787d761b4414f7f125b468e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamespaceJunction", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#create HpcCacheNfsTarget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#delete HpcCacheNfsTarget#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#read HpcCacheNfsTarget#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#update HpcCacheNfsTarget#update}.
        '''
        value = HpcCacheNfsTargetTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVerificationTimerInSeconds")
    def reset_verification_timer_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerificationTimerInSeconds", []))

    @jsii.member(jsii_name="resetWriteBackTimerInSeconds")
    def reset_write_back_timer_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteBackTimerInSeconds", []))

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
    @jsii.member(jsii_name="namespaceJunction")
    def namespace_junction(self) -> "HpcCacheNfsTargetNamespaceJunctionList":
        return typing.cast("HpcCacheNfsTargetNamespaceJunctionList", jsii.get(self, "namespaceJunction"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HpcCacheNfsTargetTimeoutsOutputReference":
        return typing.cast("HpcCacheNfsTargetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cacheNameInput")
    def cache_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceJunctionInput")
    def namespace_junction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HpcCacheNfsTargetNamespaceJunction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HpcCacheNfsTargetNamespaceJunction"]]], jsii.get(self, "namespaceJunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetHostNameInput")
    def target_host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetHostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HpcCacheNfsTargetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HpcCacheNfsTargetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usageModelInput")
    def usage_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageModelInput"))

    @builtins.property
    @jsii.member(jsii_name="verificationTimerInSecondsInput")
    def verification_timer_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "verificationTimerInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="writeBackTimerInSecondsInput")
    def write_back_timer_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "writeBackTimerInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheName")
    def cache_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheName"))

    @cache_name.setter
    def cache_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32af978ddde69824f8a19e1c7de158c32510dcc84c0c18609f4fc89b4a16fee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47244ee67c56ab6fc2da9c516b1aeae684b7059d351cba7d2085b59c9879ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eaf4cd34283d4decaf63aa5427466091244dfd56aef162ff10c8a716e3c62d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e12430d5be139da9f4fc6959f4c3bb668727eb07cd1d66636fa343bf30a8a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetHostName")
    def target_host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetHostName"))

    @target_host_name.setter
    def target_host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d1dae7189be325717f5ba9715c526b132573acbf85b5070b16115af812814f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetHostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usageModel")
    def usage_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usageModel"))

    @usage_model.setter
    def usage_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ec9392869451b51e4f0f015c064785a1de61c42ff69595fc77c0088d7710fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usageModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verificationTimerInSeconds")
    def verification_timer_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "verificationTimerInSeconds"))

    @verification_timer_in_seconds.setter
    def verification_timer_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c928f73f2262b9f97485745e5335104a7aeaf3d1b6dfea1c5ae04b380d9a4944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verificationTimerInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeBackTimerInSeconds")
    def write_back_timer_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "writeBackTimerInSeconds"))

    @write_back_timer_in_seconds.setter
    def write_back_timer_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449c5b193ad42a97838a46c1772675e8eb1cd16f7724e6993425a2cfff3179e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeBackTimerInSeconds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCacheNfsTarget.HpcCacheNfsTargetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cache_name": "cacheName",
        "name": "name",
        "namespace_junction": "namespaceJunction",
        "resource_group_name": "resourceGroupName",
        "target_host_name": "targetHostName",
        "usage_model": "usageModel",
        "id": "id",
        "timeouts": "timeouts",
        "verification_timer_in_seconds": "verificationTimerInSeconds",
        "write_back_timer_in_seconds": "writeBackTimerInSeconds",
    },
)
class HpcCacheNfsTargetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cache_name: builtins.str,
        name: builtins.str,
        namespace_junction: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HpcCacheNfsTargetNamespaceJunction", typing.Dict[builtins.str, typing.Any]]]],
        resource_group_name: builtins.str,
        target_host_name: builtins.str,
        usage_model: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["HpcCacheNfsTargetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        verification_timer_in_seconds: typing.Optional[jsii.Number] = None,
        write_back_timer_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cache_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#cache_name HpcCacheNfsTarget#cache_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#name HpcCacheNfsTarget#name}.
        :param namespace_junction: namespace_junction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#namespace_junction HpcCacheNfsTarget#namespace_junction}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#resource_group_name HpcCacheNfsTarget#resource_group_name}.
        :param target_host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#target_host_name HpcCacheNfsTarget#target_host_name}.
        :param usage_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#usage_model HpcCacheNfsTarget#usage_model}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#id HpcCacheNfsTarget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#timeouts HpcCacheNfsTarget#timeouts}
        :param verification_timer_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#verification_timer_in_seconds HpcCacheNfsTarget#verification_timer_in_seconds}.
        :param write_back_timer_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#write_back_timer_in_seconds HpcCacheNfsTarget#write_back_timer_in_seconds}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = HpcCacheNfsTargetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac08562dc0eb1d2ca885ebf55d89f71a47d6a31f937fb421236beb5056d4f7d9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cache_name", value=cache_name, expected_type=type_hints["cache_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_junction", value=namespace_junction, expected_type=type_hints["namespace_junction"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument target_host_name", value=target_host_name, expected_type=type_hints["target_host_name"])
            check_type(argname="argument usage_model", value=usage_model, expected_type=type_hints["usage_model"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument verification_timer_in_seconds", value=verification_timer_in_seconds, expected_type=type_hints["verification_timer_in_seconds"])
            check_type(argname="argument write_back_timer_in_seconds", value=write_back_timer_in_seconds, expected_type=type_hints["write_back_timer_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_name": cache_name,
            "name": name,
            "namespace_junction": namespace_junction,
            "resource_group_name": resource_group_name,
            "target_host_name": target_host_name,
            "usage_model": usage_model,
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
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if verification_timer_in_seconds is not None:
            self._values["verification_timer_in_seconds"] = verification_timer_in_seconds
        if write_back_timer_in_seconds is not None:
            self._values["write_back_timer_in_seconds"] = write_back_timer_in_seconds

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
    def cache_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#cache_name HpcCacheNfsTarget#cache_name}.'''
        result = self._values.get("cache_name")
        assert result is not None, "Required property 'cache_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#name HpcCacheNfsTarget#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_junction(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HpcCacheNfsTargetNamespaceJunction"]]:
        '''namespace_junction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#namespace_junction HpcCacheNfsTarget#namespace_junction}
        '''
        result = self._values.get("namespace_junction")
        assert result is not None, "Required property 'namespace_junction' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HpcCacheNfsTargetNamespaceJunction"]], result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#resource_group_name HpcCacheNfsTarget#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#target_host_name HpcCacheNfsTarget#target_host_name}.'''
        result = self._values.get("target_host_name")
        assert result is not None, "Required property 'target_host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def usage_model(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#usage_model HpcCacheNfsTarget#usage_model}.'''
        result = self._values.get("usage_model")
        assert result is not None, "Required property 'usage_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#id HpcCacheNfsTarget#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HpcCacheNfsTargetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#timeouts HpcCacheNfsTarget#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HpcCacheNfsTargetTimeouts"], result)

    @builtins.property
    def verification_timer_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#verification_timer_in_seconds HpcCacheNfsTarget#verification_timer_in_seconds}.'''
        result = self._values.get("verification_timer_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_back_timer_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#write_back_timer_in_seconds HpcCacheNfsTarget#write_back_timer_in_seconds}.'''
        result = self._values.get("write_back_timer_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheNfsTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCacheNfsTarget.HpcCacheNfsTargetNamespaceJunction",
    jsii_struct_bases=[],
    name_mapping={
        "namespace_path": "namespacePath",
        "nfs_export": "nfsExport",
        "access_policy_name": "accessPolicyName",
        "target_path": "targetPath",
    },
)
class HpcCacheNfsTargetNamespaceJunction:
    def __init__(
        self,
        *,
        namespace_path: builtins.str,
        nfs_export: builtins.str,
        access_policy_name: typing.Optional[builtins.str] = None,
        target_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#namespace_path HpcCacheNfsTarget#namespace_path}.
        :param nfs_export: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#nfs_export HpcCacheNfsTarget#nfs_export}.
        :param access_policy_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#access_policy_name HpcCacheNfsTarget#access_policy_name}.
        :param target_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#target_path HpcCacheNfsTarget#target_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8870600dd549d9f8d6173e7113bf6ee204c520ac9d1436003a1a4a89d128ad08)
            check_type(argname="argument namespace_path", value=namespace_path, expected_type=type_hints["namespace_path"])
            check_type(argname="argument nfs_export", value=nfs_export, expected_type=type_hints["nfs_export"])
            check_type(argname="argument access_policy_name", value=access_policy_name, expected_type=type_hints["access_policy_name"])
            check_type(argname="argument target_path", value=target_path, expected_type=type_hints["target_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_path": namespace_path,
            "nfs_export": nfs_export,
        }
        if access_policy_name is not None:
            self._values["access_policy_name"] = access_policy_name
        if target_path is not None:
            self._values["target_path"] = target_path

    @builtins.property
    def namespace_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#namespace_path HpcCacheNfsTarget#namespace_path}.'''
        result = self._values.get("namespace_path")
        assert result is not None, "Required property 'namespace_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nfs_export(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#nfs_export HpcCacheNfsTarget#nfs_export}.'''
        result = self._values.get("nfs_export")
        assert result is not None, "Required property 'nfs_export' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#access_policy_name HpcCacheNfsTarget#access_policy_name}.'''
        result = self._values.get("access_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#target_path HpcCacheNfsTarget#target_path}.'''
        result = self._values.get("target_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheNfsTargetNamespaceJunction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheNfsTargetNamespaceJunctionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCacheNfsTarget.HpcCacheNfsTargetNamespaceJunctionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e8540fbaecd4e6f471a99089cff478cf2a0d9a8fd11dd9d1f832d5cbc5aed6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HpcCacheNfsTargetNamespaceJunctionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87cc7aadf1ab81ea9ddb004be92b7293de032afdee440e17450ba6a8f5634d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HpcCacheNfsTargetNamespaceJunctionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21ebf94964251cdb22d5520455da09a604d47ab2f7cd0fe6e34f6c5a1c46532)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24eadad5e486ae289a51c3a9238b4cdf302a2c5a83e79756c02aa28066985c7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff2df57a4ab8860b841281c2385883029ca4cfa60b513135ec3288bdc63a0f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheNfsTargetNamespaceJunction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheNfsTargetNamespaceJunction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheNfsTargetNamespaceJunction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4d740048d114bb4f446b30deccd4bc83ff7e1858c1de26724cf028d8270660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HpcCacheNfsTargetNamespaceJunctionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCacheNfsTarget.HpcCacheNfsTargetNamespaceJunctionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aea2beccef4cb683943a77b0cfb01dfbcb5aff5523d32ed0df4a4ef8bcf5a93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessPolicyName")
    def reset_access_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessPolicyName", []))

    @jsii.member(jsii_name="resetTargetPath")
    def reset_target_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetPath", []))

    @builtins.property
    @jsii.member(jsii_name="accessPolicyNameInput")
    def access_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespacePathInput")
    def namespace_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespacePathInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsExportInput")
    def nfs_export_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nfsExportInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPathInput")
    def target_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetPathInput"))

    @builtins.property
    @jsii.member(jsii_name="accessPolicyName")
    def access_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessPolicyName"))

    @access_policy_name.setter
    def access_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ad12afa9c692554e7b1940112bdb03486fc73c1c9fa05124bc0075e7e4e288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPolicyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespacePath")
    def namespace_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespacePath"))

    @namespace_path.setter
    def namespace_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5f9e433e07010225f10dfef75fbae1281f4bf45ac11704c9e8a3616daff967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespacePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsExport")
    def nfs_export(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nfsExport"))

    @nfs_export.setter
    def nfs_export(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d44f9594655871439a8a065e2f50a30062cf4ac01728f989a82483ce69a1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsExport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPath")
    def target_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPath"))

    @target_path.setter
    def target_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e8d0c19221e6b70c54447a8fce4122f2e6bb8d3e2e9d3cf91420c52cf86847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheNfsTargetNamespaceJunction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheNfsTargetNamespaceJunction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheNfsTargetNamespaceJunction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42453287ed321660c876d65546f37bd9ec4ddcfe803b7180b4a2f5c7c5e35a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCacheNfsTarget.HpcCacheNfsTargetTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class HpcCacheNfsTargetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#create HpcCacheNfsTarget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#delete HpcCacheNfsTarget#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#read HpcCacheNfsTarget#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#update HpcCacheNfsTarget#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ae0c08bce4ba76f17288e5580424e311b5aea8e9717beac6abf87b8690ce11)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#create HpcCacheNfsTarget#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#delete HpcCacheNfsTarget#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#read HpcCacheNfsTarget#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache_nfs_target#update HpcCacheNfsTarget#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheNfsTargetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheNfsTargetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCacheNfsTarget.HpcCacheNfsTargetTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5cc8bb7273e510df0b3e48d109f6f06cecbdaf499e8a9fecaad2b1d63fc93b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47702d3e2a30242d203a7f899525f43e9ddd2c84b72754ecff072a321b8d5500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ae0bd912d6aaa698b3d128a84bbcde6ecdf87caf5acdd7637b3a4d1e31e8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb66289747a8d7f143cdfef86aeb44946c0396a640f62ef812caf7d4421c3647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d035218f3e7e6decb6d26ea696241d2420258959763180c3da62ce54ce45045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheNfsTargetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheNfsTargetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheNfsTargetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83678d25b4994b074272c94a5734ee36b16d58d7c009e559edd3909788977fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HpcCacheNfsTarget",
    "HpcCacheNfsTargetConfig",
    "HpcCacheNfsTargetNamespaceJunction",
    "HpcCacheNfsTargetNamespaceJunctionList",
    "HpcCacheNfsTargetNamespaceJunctionOutputReference",
    "HpcCacheNfsTargetTimeouts",
    "HpcCacheNfsTargetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b24696c3f0207aba6f14a74c1371a8e0a83bf3ccd18311ff8a96f0ca67d99c26(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cache_name: builtins.str,
    name: builtins.str,
    namespace_junction: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HpcCacheNfsTargetNamespaceJunction, typing.Dict[builtins.str, typing.Any]]]],
    resource_group_name: builtins.str,
    target_host_name: builtins.str,
    usage_model: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[HpcCacheNfsTargetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    verification_timer_in_seconds: typing.Optional[jsii.Number] = None,
    write_back_timer_in_seconds: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__c311feba8ca86cfc5399dfab9a219722ef9a19bafd7fc60d8769518a4626782f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da937143ee18642add39c330307f280fff170eb7787d761b4414f7f125b468e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HpcCacheNfsTargetNamespaceJunction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32af978ddde69824f8a19e1c7de158c32510dcc84c0c18609f4fc89b4a16fee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47244ee67c56ab6fc2da9c516b1aeae684b7059d351cba7d2085b59c9879ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eaf4cd34283d4decaf63aa5427466091244dfd56aef162ff10c8a716e3c62d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e12430d5be139da9f4fc6959f4c3bb668727eb07cd1d66636fa343bf30a8a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d1dae7189be325717f5ba9715c526b132573acbf85b5070b16115af812814f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ec9392869451b51e4f0f015c064785a1de61c42ff69595fc77c0088d7710fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c928f73f2262b9f97485745e5335104a7aeaf3d1b6dfea1c5ae04b380d9a4944(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449c5b193ad42a97838a46c1772675e8eb1cd16f7724e6993425a2cfff3179e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac08562dc0eb1d2ca885ebf55d89f71a47d6a31f937fb421236beb5056d4f7d9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_name: builtins.str,
    name: builtins.str,
    namespace_junction: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HpcCacheNfsTargetNamespaceJunction, typing.Dict[builtins.str, typing.Any]]]],
    resource_group_name: builtins.str,
    target_host_name: builtins.str,
    usage_model: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[HpcCacheNfsTargetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    verification_timer_in_seconds: typing.Optional[jsii.Number] = None,
    write_back_timer_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8870600dd549d9f8d6173e7113bf6ee204c520ac9d1436003a1a4a89d128ad08(
    *,
    namespace_path: builtins.str,
    nfs_export: builtins.str,
    access_policy_name: typing.Optional[builtins.str] = None,
    target_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8540fbaecd4e6f471a99089cff478cf2a0d9a8fd11dd9d1f832d5cbc5aed6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87cc7aadf1ab81ea9ddb004be92b7293de032afdee440e17450ba6a8f5634d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21ebf94964251cdb22d5520455da09a604d47ab2f7cd0fe6e34f6c5a1c46532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24eadad5e486ae289a51c3a9238b4cdf302a2c5a83e79756c02aa28066985c7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2df57a4ab8860b841281c2385883029ca4cfa60b513135ec3288bdc63a0f55(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4d740048d114bb4f446b30deccd4bc83ff7e1858c1de26724cf028d8270660(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheNfsTargetNamespaceJunction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aea2beccef4cb683943a77b0cfb01dfbcb5aff5523d32ed0df4a4ef8bcf5a93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ad12afa9c692554e7b1940112bdb03486fc73c1c9fa05124bc0075e7e4e288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5f9e433e07010225f10dfef75fbae1281f4bf45ac11704c9e8a3616daff967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d44f9594655871439a8a065e2f50a30062cf4ac01728f989a82483ce69a1fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e8d0c19221e6b70c54447a8fce4122f2e6bb8d3e2e9d3cf91420c52cf86847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42453287ed321660c876d65546f37bd9ec4ddcfe803b7180b4a2f5c7c5e35a84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheNfsTargetNamespaceJunction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ae0c08bce4ba76f17288e5580424e311b5aea8e9717beac6abf87b8690ce11(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5cc8bb7273e510df0b3e48d109f6f06cecbdaf499e8a9fecaad2b1d63fc93b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47702d3e2a30242d203a7f899525f43e9ddd2c84b72754ecff072a321b8d5500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ae0bd912d6aaa698b3d128a84bbcde6ecdf87caf5acdd7637b3a4d1e31e8bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb66289747a8d7f143cdfef86aeb44946c0396a640f62ef812caf7d4421c3647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d035218f3e7e6decb6d26ea696241d2420258959763180c3da62ce54ce45045(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83678d25b4994b074272c94a5734ee36b16d58d7c009e559edd3909788977fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheNfsTargetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
