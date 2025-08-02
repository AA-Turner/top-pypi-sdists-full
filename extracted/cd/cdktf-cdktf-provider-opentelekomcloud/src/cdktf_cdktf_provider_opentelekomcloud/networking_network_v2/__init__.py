r'''
# `opentelekomcloud_networking_network_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_networking_network_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2).
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


class NetworkingNetworkV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingNetworkV2.NetworkingNetworkV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2 opentelekomcloud_networking_network_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        admin_state_up: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        segments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkingNetworkV2Segments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        shared: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkingNetworkV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2 opentelekomcloud_networking_network_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#admin_state_up NetworkingNetworkV2#admin_state_up}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#id NetworkingNetworkV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#name NetworkingNetworkV2#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#region NetworkingNetworkV2#region}.
        :param segments: segments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#segments NetworkingNetworkV2#segments}
        :param shared: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#shared NetworkingNetworkV2#shared}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#tenant_id NetworkingNetworkV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#timeouts NetworkingNetworkV2#timeouts}
        :param value_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#value_specs NetworkingNetworkV2#value_specs}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7258d99a6778ee033ef04f35e5df34523d5e659dc94c672d31a6afb39f5bf66d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkingNetworkV2Config(
            admin_state_up=admin_state_up,
            id=id,
            name=name,
            region=region,
            segments=segments,
            shared=shared,
            tenant_id=tenant_id,
            timeouts=timeouts,
            value_specs=value_specs,
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
        '''Generates CDKTF code for importing a NetworkingNetworkV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkingNetworkV2 to import.
        :param import_from_id: The id of the existing NetworkingNetworkV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkingNetworkV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa36829f848e984ff6c685da59fa65c8cc6e3850f35a4a80a0f0a409c874cc1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSegments")
    def put_segments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkingNetworkV2Segments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071d491179a4ca2f262db1306931446581b58effad2ca28809f8ecefa3bbb3ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSegments", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#create NetworkingNetworkV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#delete NetworkingNetworkV2#delete}.
        '''
        value = NetworkingNetworkV2Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminStateUp")
    def reset_admin_state_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminStateUp", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSegments")
    def reset_segments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegments", []))

    @jsii.member(jsii_name="resetShared")
    def reset_shared(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShared", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValueSpecs")
    def reset_value_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueSpecs", []))

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
    @jsii.member(jsii_name="segments")
    def segments(self) -> "NetworkingNetworkV2SegmentsList":
        return typing.cast("NetworkingNetworkV2SegmentsList", jsii.get(self, "segments"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkingNetworkV2TimeoutsOutputReference":
        return typing.cast("NetworkingNetworkV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUpInput")
    def admin_state_up_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminStateUpInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentsInput")
    def segments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingNetworkV2Segments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingNetworkV2Segments"]]], jsii.get(self, "segmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedInput")
    def shared_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkingNetworkV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkingNetworkV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="valueSpecsInput")
    def value_specs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "valueSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminStateUp"))

    @admin_state_up.setter
    def admin_state_up(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cee035d34f2ec0569b85b373fa68a6a0214b0147a7c74595bf3c492dc5c3afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminStateUp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9117461ac15e50f65b69e4ad6bcb2302a3278be40e7f9bffc4ad900a973e8d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73fd7fed7ba013e0e0a4afc5b04b960e515ce9835e97c2996d2c9d21cc0f335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3150972319f2a399cb0409bef69c48a934143496d51c8ddfbd8a7f4eaee3ed9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shared")
    def shared(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shared"))

    @shared.setter
    def shared(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e972d9d65acf6b8f9a59a02b9d7ea586cc6e05e406c242d540128bf96441cc69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shared", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5881e6a1a89fdc2a46036648593198f9777b125127738cb03832582cc62f468d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueSpecs")
    def value_specs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "valueSpecs"))

    @value_specs.setter
    def value_specs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5866690a765ddac38480efdfb1fb0de4ecebd0a12866adbc6f72ab6e4aaa9bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueSpecs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.networkingNetworkV2.NetworkingNetworkV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "admin_state_up": "adminStateUp",
        "id": "id",
        "name": "name",
        "region": "region",
        "segments": "segments",
        "shared": "shared",
        "tenant_id": "tenantId",
        "timeouts": "timeouts",
        "value_specs": "valueSpecs",
    },
)
class NetworkingNetworkV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        admin_state_up: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        segments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkingNetworkV2Segments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        shared: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkingNetworkV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#admin_state_up NetworkingNetworkV2#admin_state_up}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#id NetworkingNetworkV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#name NetworkingNetworkV2#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#region NetworkingNetworkV2#region}.
        :param segments: segments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#segments NetworkingNetworkV2#segments}
        :param shared: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#shared NetworkingNetworkV2#shared}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#tenant_id NetworkingNetworkV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#timeouts NetworkingNetworkV2#timeouts}
        :param value_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#value_specs NetworkingNetworkV2#value_specs}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkingNetworkV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a068117f21e7d3bb495f047789682252bf65510e19b893c85c64f9ebeb8a57)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument admin_state_up", value=admin_state_up, expected_type=type_hints["admin_state_up"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument segments", value=segments, expected_type=type_hints["segments"])
            check_type(argname="argument shared", value=shared, expected_type=type_hints["shared"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument value_specs", value=value_specs, expected_type=type_hints["value_specs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if admin_state_up is not None:
            self._values["admin_state_up"] = admin_state_up
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if segments is not None:
            self._values["segments"] = segments
        if shared is not None:
            self._values["shared"] = shared
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if value_specs is not None:
            self._values["value_specs"] = value_specs

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
    def admin_state_up(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#admin_state_up NetworkingNetworkV2#admin_state_up}.'''
        result = self._values.get("admin_state_up")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#id NetworkingNetworkV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#name NetworkingNetworkV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#region NetworkingNetworkV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingNetworkV2Segments"]]]:
        '''segments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#segments NetworkingNetworkV2#segments}
        '''
        result = self._values.get("segments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkingNetworkV2Segments"]]], result)

    @builtins.property
    def shared(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#shared NetworkingNetworkV2#shared}.'''
        result = self._values.get("shared")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#tenant_id NetworkingNetworkV2#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkingNetworkV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#timeouts NetworkingNetworkV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkingNetworkV2Timeouts"], result)

    @builtins.property
    def value_specs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#value_specs NetworkingNetworkV2#value_specs}.'''
        result = self._values.get("value_specs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingNetworkV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.networkingNetworkV2.NetworkingNetworkV2Segments",
    jsii_struct_bases=[],
    name_mapping={
        "network_type": "networkType",
        "physical_network": "physicalNetwork",
        "segmentation_id": "segmentationId",
    },
)
class NetworkingNetworkV2Segments:
    def __init__(
        self,
        *,
        network_type: typing.Optional[builtins.str] = None,
        physical_network: typing.Optional[builtins.str] = None,
        segmentation_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param network_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#network_type NetworkingNetworkV2#network_type}.
        :param physical_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#physical_network NetworkingNetworkV2#physical_network}.
        :param segmentation_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#segmentation_id NetworkingNetworkV2#segmentation_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f428778df48fae7f2ccf84ccdff9b5a0f73fdfe222bc0432ab8cb46242f48b)
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument physical_network", value=physical_network, expected_type=type_hints["physical_network"])
            check_type(argname="argument segmentation_id", value=segmentation_id, expected_type=type_hints["segmentation_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network_type is not None:
            self._values["network_type"] = network_type
        if physical_network is not None:
            self._values["physical_network"] = physical_network
        if segmentation_id is not None:
            self._values["segmentation_id"] = segmentation_id

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#network_type NetworkingNetworkV2#network_type}.'''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_network(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#physical_network NetworkingNetworkV2#physical_network}.'''
        result = self._values.get("physical_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segmentation_id(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#segmentation_id NetworkingNetworkV2#segmentation_id}.'''
        result = self._values.get("segmentation_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingNetworkV2Segments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkingNetworkV2SegmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingNetworkV2.NetworkingNetworkV2SegmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52df9f2bdc258f1eeea04343e4702a326eb26cf35d78543bcd3c842041b64a2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkingNetworkV2SegmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c41c57ca5527f0ee0a304af7100872d702b3718f802f3b6efaebe3397164399)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkingNetworkV2SegmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa38d753023a34f124e0890931c31b84c8d4be17f2be4971165b264bd68b0e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c701c33b36496038069bd0a93fe8b9f2395bb60fd6acd22071562c55dbbc916)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d53519c2c2a8529ee00757128cb7bdf66388917c9d6f6cb190159f2a17d97a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingNetworkV2Segments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingNetworkV2Segments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingNetworkV2Segments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587313c18bc5d28bb16c52bcd283f16d535b1b4200ceb6d164f600b6b58e806a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkingNetworkV2SegmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingNetworkV2.NetworkingNetworkV2SegmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfd7a3d342745ae2c5898ab7211aee1ab3f20e785b3d6cf0a9f283da5ddbc3e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetworkType")
    def reset_network_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkType", []))

    @jsii.member(jsii_name="resetPhysicalNetwork")
    def reset_physical_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhysicalNetwork", []))

    @jsii.member(jsii_name="resetSegmentationId")
    def reset_segmentation_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegmentationId", []))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalNetworkInput")
    def physical_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "physicalNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentationIdInput")
    def segmentation_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "segmentationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a9e4cbdaf1795ec3516182cf80cc4039f344a5d72cc72df6cb653ab446cc45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="physicalNetwork")
    def physical_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "physicalNetwork"))

    @physical_network.setter
    def physical_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b4d0081266a255584f262f39d1b795e0609a4c4fe490fa03073a0c50a74a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="segmentationId")
    def segmentation_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "segmentationId"))

    @segmentation_id.setter
    def segmentation_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16af9b526e7ac7cfd3ef36e7b296ce62bd5a07234bade6b6f3e47303222955ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingNetworkV2Segments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingNetworkV2Segments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingNetworkV2Segments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f1bceb48ae53b47ca39d9ae10d7442a83ec00e682a677ed39ffc17ac11a467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.networkingNetworkV2.NetworkingNetworkV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class NetworkingNetworkV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#create NetworkingNetworkV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#delete NetworkingNetworkV2#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6e2711b4c3c0b9647cfaa530e83e92152dece23baeaa5c50e5421608610db5)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#create NetworkingNetworkV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/networking_network_v2#delete NetworkingNetworkV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingNetworkV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkingNetworkV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.networkingNetworkV2.NetworkingNetworkV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4e9cf65975148638e014a9568ca433621041512660e7505260a6bc50ecf0820)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4dc2023f173c475d9c9e8666364e26b3b988c9417f0e4ecca6398188a99445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8194c64166156093d91ba31bba4afec77c5ab9f50c7f56bd94d926679b38f2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingNetworkV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingNetworkV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingNetworkV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e6dde00c8c31fab868caf52e47107ec97e57c899ae98028896d10e9b33877a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkingNetworkV2",
    "NetworkingNetworkV2Config",
    "NetworkingNetworkV2Segments",
    "NetworkingNetworkV2SegmentsList",
    "NetworkingNetworkV2SegmentsOutputReference",
    "NetworkingNetworkV2Timeouts",
    "NetworkingNetworkV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7258d99a6778ee033ef04f35e5df34523d5e659dc94c672d31a6afb39f5bf66d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    admin_state_up: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    segments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingNetworkV2Segments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    shared: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkingNetworkV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__5aa36829f848e984ff6c685da59fa65c8cc6e3850f35a4a80a0f0a409c874cc1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071d491179a4ca2f262db1306931446581b58effad2ca28809f8ecefa3bbb3ed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingNetworkV2Segments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cee035d34f2ec0569b85b373fa68a6a0214b0147a7c74595bf3c492dc5c3afd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9117461ac15e50f65b69e4ad6bcb2302a3278be40e7f9bffc4ad900a973e8d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73fd7fed7ba013e0e0a4afc5b04b960e515ce9835e97c2996d2c9d21cc0f335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3150972319f2a399cb0409bef69c48a934143496d51c8ddfbd8a7f4eaee3ed9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e972d9d65acf6b8f9a59a02b9d7ea586cc6e05e406c242d540128bf96441cc69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5881e6a1a89fdc2a46036648593198f9777b125127738cb03832582cc62f468d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5866690a765ddac38480efdfb1fb0de4ecebd0a12866adbc6f72ab6e4aaa9bb5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a068117f21e7d3bb495f047789682252bf65510e19b893c85c64f9ebeb8a57(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_state_up: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    segments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkingNetworkV2Segments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    shared: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkingNetworkV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    value_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f428778df48fae7f2ccf84ccdff9b5a0f73fdfe222bc0432ab8cb46242f48b(
    *,
    network_type: typing.Optional[builtins.str] = None,
    physical_network: typing.Optional[builtins.str] = None,
    segmentation_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52df9f2bdc258f1eeea04343e4702a326eb26cf35d78543bcd3c842041b64a2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c41c57ca5527f0ee0a304af7100872d702b3718f802f3b6efaebe3397164399(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa38d753023a34f124e0890931c31b84c8d4be17f2be4971165b264bd68b0e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c701c33b36496038069bd0a93fe8b9f2395bb60fd6acd22071562c55dbbc916(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d53519c2c2a8529ee00757128cb7bdf66388917c9d6f6cb190159f2a17d97a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587313c18bc5d28bb16c52bcd283f16d535b1b4200ceb6d164f600b6b58e806a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkingNetworkV2Segments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd7a3d342745ae2c5898ab7211aee1ab3f20e785b3d6cf0a9f283da5ddbc3e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a9e4cbdaf1795ec3516182cf80cc4039f344a5d72cc72df6cb653ab446cc45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b4d0081266a255584f262f39d1b795e0609a4c4fe490fa03073a0c50a74a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16af9b526e7ac7cfd3ef36e7b296ce62bd5a07234bade6b6f3e47303222955ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f1bceb48ae53b47ca39d9ae10d7442a83ec00e682a677ed39ffc17ac11a467(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingNetworkV2Segments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6e2711b4c3c0b9647cfaa530e83e92152dece23baeaa5c50e5421608610db5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e9cf65975148638e014a9568ca433621041512660e7505260a6bc50ecf0820(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4dc2023f173c475d9c9e8666364e26b3b988c9417f0e4ecca6398188a99445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8194c64166156093d91ba31bba4afec77c5ab9f50c7f56bd94d926679b38f2d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e6dde00c8c31fab868caf52e47107ec97e57c899ae98028896d10e9b33877a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingNetworkV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
