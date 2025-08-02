r'''
# `opentelekomcloud_dms_dedicated_instance_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dms_dedicated_instance_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2).
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


class DmsDedicatedInstanceV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsDedicatedInstanceV2.DmsDedicatedInstanceV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2 opentelekomcloud_dms_dedicated_instance_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        broker_num: jsii.Number,
        engine_version: builtins.str,
        flavor_id: builtins.str,
        name: builtins.str,
        network_id: builtins.str,
        security_group_id: builtins.str,
        storage_space: jsii.Number,
        storage_spec_code: builtins.str,
        vpc_id: builtins.str,
        access_user: typing.Optional[builtins.str] = None,
        arch_type: typing.Optional[builtins.str] = None,
        available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cross_vpc_accesses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DmsDedicatedInstanceV2CrossVpcAccesses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disk_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_encrypted_key: typing.Optional[builtins.str] = None,
        enabled_mechanisms: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_publicip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ipv6_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        new_tenant_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        publicip_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        retention_policy: typing.Optional[builtins.str] = None,
        security_protocol: typing.Optional[builtins.str] = None,
        ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DmsDedicatedInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2 opentelekomcloud_dms_dedicated_instance_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param broker_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#broker_num DmsDedicatedInstanceV2#broker_num}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#engine_version DmsDedicatedInstanceV2#engine_version}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#flavor_id DmsDedicatedInstanceV2#flavor_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#name DmsDedicatedInstanceV2#name}.
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#network_id DmsDedicatedInstanceV2#network_id}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#security_group_id DmsDedicatedInstanceV2#security_group_id}.
        :param storage_space: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#storage_space DmsDedicatedInstanceV2#storage_space}.
        :param storage_spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#storage_spec_code DmsDedicatedInstanceV2#storage_spec_code}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#vpc_id DmsDedicatedInstanceV2#vpc_id}.
        :param access_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#access_user DmsDedicatedInstanceV2#access_user}.
        :param arch_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#arch_type DmsDedicatedInstanceV2#arch_type}.
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#available_zones DmsDedicatedInstanceV2#available_zones}.
        :param cross_vpc_accesses: cross_vpc_accesses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#cross_vpc_accesses DmsDedicatedInstanceV2#cross_vpc_accesses}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#description DmsDedicatedInstanceV2#description}.
        :param disk_encrypted_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#disk_encrypted_enable DmsDedicatedInstanceV2#disk_encrypted_enable}.
        :param disk_encrypted_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#disk_encrypted_key DmsDedicatedInstanceV2#disk_encrypted_key}.
        :param enabled_mechanisms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#enabled_mechanisms DmsDedicatedInstanceV2#enabled_mechanisms}.
        :param enable_publicip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#enable_publicip DmsDedicatedInstanceV2#enable_publicip}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#id DmsDedicatedInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ipv6_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#ipv6_enable DmsDedicatedInstanceV2#ipv6_enable}.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#maintain_begin DmsDedicatedInstanceV2#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#maintain_end DmsDedicatedInstanceV2#maintain_end}.
        :param new_tenant_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#new_tenant_ips DmsDedicatedInstanceV2#new_tenant_ips}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#password DmsDedicatedInstanceV2#password}.
        :param publicip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#publicip_id DmsDedicatedInstanceV2#publicip_id}.
        :param retention_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#retention_policy DmsDedicatedInstanceV2#retention_policy}.
        :param security_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#security_protocol DmsDedicatedInstanceV2#security_protocol}.
        :param ssl_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#ssl_enable DmsDedicatedInstanceV2#ssl_enable}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#tags DmsDedicatedInstanceV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#timeouts DmsDedicatedInstanceV2#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb71df079517ca847a5db24c561d90a1023a35ec45c4049c7424bcb0af05ec8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DmsDedicatedInstanceV2Config(
            broker_num=broker_num,
            engine_version=engine_version,
            flavor_id=flavor_id,
            name=name,
            network_id=network_id,
            security_group_id=security_group_id,
            storage_space=storage_space,
            storage_spec_code=storage_spec_code,
            vpc_id=vpc_id,
            access_user=access_user,
            arch_type=arch_type,
            available_zones=available_zones,
            cross_vpc_accesses=cross_vpc_accesses,
            description=description,
            disk_encrypted_enable=disk_encrypted_enable,
            disk_encrypted_key=disk_encrypted_key,
            enabled_mechanisms=enabled_mechanisms,
            enable_publicip=enable_publicip,
            id=id,
            ipv6_enable=ipv6_enable,
            maintain_begin=maintain_begin,
            maintain_end=maintain_end,
            new_tenant_ips=new_tenant_ips,
            password=password,
            publicip_id=publicip_id,
            retention_policy=retention_policy,
            security_protocol=security_protocol,
            ssl_enable=ssl_enable,
            tags=tags,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a DmsDedicatedInstanceV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DmsDedicatedInstanceV2 to import.
        :param import_from_id: The id of the existing DmsDedicatedInstanceV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DmsDedicatedInstanceV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66dd84eb804e6d6209d6eef1edeb812ef6da949baa3189462a28581f3daf4592)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCrossVpcAccesses")
    def put_cross_vpc_accesses(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DmsDedicatedInstanceV2CrossVpcAccesses", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab24089974c6cb6250db3e7fd9a818bfebe7fa214a368dc0f494a88a013f77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCrossVpcAccesses", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#create DmsDedicatedInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#delete DmsDedicatedInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#update DmsDedicatedInstanceV2#update}.
        '''
        value = DmsDedicatedInstanceV2Timeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessUser")
    def reset_access_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessUser", []))

    @jsii.member(jsii_name="resetArchType")
    def reset_arch_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchType", []))

    @jsii.member(jsii_name="resetAvailableZones")
    def reset_available_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableZones", []))

    @jsii.member(jsii_name="resetCrossVpcAccesses")
    def reset_cross_vpc_accesses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossVpcAccesses", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiskEncryptedEnable")
    def reset_disk_encrypted_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptedEnable", []))

    @jsii.member(jsii_name="resetDiskEncryptedKey")
    def reset_disk_encrypted_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptedKey", []))

    @jsii.member(jsii_name="resetEnabledMechanisms")
    def reset_enabled_mechanisms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledMechanisms", []))

    @jsii.member(jsii_name="resetEnablePublicip")
    def reset_enable_publicip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePublicip", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpv6Enable")
    def reset_ipv6_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Enable", []))

    @jsii.member(jsii_name="resetMaintainBegin")
    def reset_maintain_begin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainBegin", []))

    @jsii.member(jsii_name="resetMaintainEnd")
    def reset_maintain_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainEnd", []))

    @jsii.member(jsii_name="resetNewTenantIps")
    def reset_new_tenant_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewTenantIps", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPublicipId")
    def reset_publicip_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicipId", []))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetSecurityProtocol")
    def reset_security_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProtocol", []))

    @jsii.member(jsii_name="resetSslEnable")
    def reset_ssl_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslEnable", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidth"))

    @builtins.property
    @jsii.member(jsii_name="certReplaced")
    def cert_replaced(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "certReplaced"))

    @builtins.property
    @jsii.member(jsii_name="connectAddress")
    def connect_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectAddress"))

    @builtins.property
    @jsii.member(jsii_name="connectorNodeNum")
    def connector_node_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectorNodeNum"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="crossVpcAccesses")
    def cross_vpc_accesses(self) -> "DmsDedicatedInstanceV2CrossVpcAccessesList":
        return typing.cast("DmsDedicatedInstanceV2CrossVpcAccessesList", jsii.get(self, "crossVpcAccesses"))

    @builtins.property
    @jsii.member(jsii_name="dumping")
    def dumping(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "dumping"))

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @builtins.property
    @jsii.member(jsii_name="nodeNum")
    def node_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeNum"))

    @builtins.property
    @jsii.member(jsii_name="partitionNum")
    def partition_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "partitionNum"))

    @builtins.property
    @jsii.member(jsii_name="podConnectAddress")
    def pod_connect_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podConnectAddress"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="publicBandwidth")
    def public_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "publicBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="resourceSpecCode")
    def resource_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSpecCode"))

    @builtins.property
    @jsii.member(jsii_name="sslTwoWayEnable")
    def ssl_two_way_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "sslTwoWayEnable"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DmsDedicatedInstanceV2TimeoutsOutputReference":
        return typing.cast("DmsDedicatedInstanceV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="usedStorageSpace")
    def used_storage_space(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedStorageSpace"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @builtins.property
    @jsii.member(jsii_name="accessUserInput")
    def access_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessUserInput"))

    @builtins.property
    @jsii.member(jsii_name="archTypeInput")
    def arch_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "archTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="availableZonesInput")
    def available_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availableZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="brokerNumInput")
    def broker_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "brokerNumInput"))

    @builtins.property
    @jsii.member(jsii_name="crossVpcAccessesInput")
    def cross_vpc_accesses_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsDedicatedInstanceV2CrossVpcAccesses"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsDedicatedInstanceV2CrossVpcAccesses"]]], jsii.get(self, "crossVpcAccessesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptedEnableInput")
    def disk_encrypted_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diskEncryptedEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptedKeyInput")
    def disk_encrypted_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledMechanismsInput")
    def enabled_mechanisms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enabledMechanismsInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePublicipInput")
    def enable_publicip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePublicipInput"))

    @builtins.property
    @jsii.member(jsii_name="engineVersionInput")
    def engine_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6EnableInput")
    def ipv6_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv6EnableInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainBeginInput")
    def maintain_begin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainBeginInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainEndInput")
    def maintain_end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainEndInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="newTenantIpsInput")
    def new_tenant_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "newTenantIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="publicipIdInput")
    def publicip_id_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicipIdInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProtocolInput")
    def security_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sslEnableInput")
    def ssl_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSpaceInput")
    def storage_space_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageSpaceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSpecCodeInput")
    def storage_spec_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageSpecCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DmsDedicatedInstanceV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DmsDedicatedInstanceV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessUser")
    def access_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessUser"))

    @access_user.setter
    def access_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b9e2c1e152cb2d70a6c9237088f4c2574afc43d12ac3f760369cdcf1d0e4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="archType")
    def arch_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "archType"))

    @arch_type.setter
    def arch_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106c005057636118ef4b162573e1e49063bbc2d2c89364ac367a680e338e6619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableZones")
    def available_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableZones"))

    @available_zones.setter
    def available_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc6edf5b308ac3af73a2add8d3501cdb23a9a143669f5d407cfadf9daecfb0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="brokerNum")
    def broker_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "brokerNum"))

    @broker_num.setter
    def broker_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5442eb11f1f01fe980f52529d12ffccfa3f720bac07c30766eb38a32543be3f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brokerNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a7af111bc74c9e656a3137d8cb5cf76254bb23ad5750ea82b043528a0e872b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptedEnable")
    def disk_encrypted_enable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diskEncryptedEnable"))

    @disk_encrypted_enable.setter
    def disk_encrypted_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c6e658cc695e6d66aaef410b0de9e04e3e0cb867be3ecc1ecb316d6b8c28b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptedEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptedKey")
    def disk_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptedKey"))

    @disk_encrypted_key.setter
    def disk_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112a2d9719cf7cd49751dd538570a6f49623fc26c86af8794a3a08d113af1e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabledMechanisms")
    def enabled_mechanisms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enabledMechanisms"))

    @enabled_mechanisms.setter
    def enabled_mechanisms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eed1e84aaaefb78dcb3854232ae82346b9810efe07a6b0128561c95fa124d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledMechanisms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePublicip")
    def enable_publicip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePublicip"))

    @enable_publicip.setter
    def enable_publicip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6acf2020762a11d670b1e0329150b5829e419105ac9ebf659964444b5ab1b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePublicip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f55f6fc63b5dd1d9e9dc42e7eaeb2c1c71d223f2f2d2811826149693a06012aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119293bb38606b63004d6f8f9424006409c3742938e61a8a0d60f4b0fd628fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1056b9558a59ff6007cedbd6cd68da8dfa425cb34f305ed9bc293e04cf5932c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Enable")
    def ipv6_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv6Enable"))

    @ipv6_enable.setter
    def ipv6_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477e182788922f4087e5e7db2456d385c582c8fcf227e1c8fbfd79a7e55c8eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainBegin")
    def maintain_begin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainBegin"))

    @maintain_begin.setter
    def maintain_begin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67e5c34c0b94ba801f15de1677caf163808c8999e63b3d84f06735927956ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainBegin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainEnd")
    def maintain_end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainEnd"))

    @maintain_end.setter
    def maintain_end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3765655a427272d914a93c922e8251c12daaca1147a3334249edaefae8a65609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7599772ae43da77518b918de6abfdd042b697ec2bed17ef978907036e87b5639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b74991207060d966f2c4dfc98bfa407a0f2f0bd2bac6fdf29a9a9043006f5c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newTenantIps")
    def new_tenant_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "newTenantIps"))

    @new_tenant_ips.setter
    def new_tenant_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0564ea626aa85420835747eaf64042e9057c5d9b2da932534c24260b30608c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newTenantIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3651befc37eea42ea9d659cd6c3bd641a53d01ef15e1b00ae59b5fbd5db67714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicipId")
    def publicip_id(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicipId"))

    @publicip_id.setter
    def publicip_id(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9ceb6aea4979c2feba0506fba7880cd82752739566550657e0cc59df867cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicipId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionPolicy"))

    @retention_policy.setter
    def retention_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044292e4106a326c6c5b9e91620012a8fccbcd5f4078646e732e57bf4d3c16ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b3be22f51a5c8b3d6be27e27a1f5334bcc3ebc4eaded3ea559ffe14d29923a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityProtocol")
    def security_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProtocol"))

    @security_protocol.setter
    def security_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37be3d9acab2861946a3905f0e30f4fe8b06e0ecbabbd1681511e655517631c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslEnable")
    def ssl_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sslEnable"))

    @ssl_enable.setter
    def ssl_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce78d60a312c84f4839be2916cecc1974f72f4ec89d3272a968859f693ece6fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSpace")
    def storage_space(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageSpace"))

    @storage_space.setter
    def storage_space(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642748e8c10b9b80e6f6adc7f1f06095aaac800ee3eb4957535cac53cb3ee3c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSpace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSpecCode")
    def storage_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSpecCode"))

    @storage_spec_code.setter
    def storage_spec_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf185d2dcea3a15dc42e32214325986d69b8e7bd5c9a8768206c38136262ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSpecCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0ef9c57bfeca7465783eb6b01bc945680661c419c2eb48bcdb3632d30f6ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91f1d48c3f69a8b67c1cae7bc228a1b44a5a8d687b275a91470b9da68659b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsDedicatedInstanceV2.DmsDedicatedInstanceV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "broker_num": "brokerNum",
        "engine_version": "engineVersion",
        "flavor_id": "flavorId",
        "name": "name",
        "network_id": "networkId",
        "security_group_id": "securityGroupId",
        "storage_space": "storageSpace",
        "storage_spec_code": "storageSpecCode",
        "vpc_id": "vpcId",
        "access_user": "accessUser",
        "arch_type": "archType",
        "available_zones": "availableZones",
        "cross_vpc_accesses": "crossVpcAccesses",
        "description": "description",
        "disk_encrypted_enable": "diskEncryptedEnable",
        "disk_encrypted_key": "diskEncryptedKey",
        "enabled_mechanisms": "enabledMechanisms",
        "enable_publicip": "enablePublicip",
        "id": "id",
        "ipv6_enable": "ipv6Enable",
        "maintain_begin": "maintainBegin",
        "maintain_end": "maintainEnd",
        "new_tenant_ips": "newTenantIps",
        "password": "password",
        "publicip_id": "publicipId",
        "retention_policy": "retentionPolicy",
        "security_protocol": "securityProtocol",
        "ssl_enable": "sslEnable",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class DmsDedicatedInstanceV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        broker_num: jsii.Number,
        engine_version: builtins.str,
        flavor_id: builtins.str,
        name: builtins.str,
        network_id: builtins.str,
        security_group_id: builtins.str,
        storage_space: jsii.Number,
        storage_spec_code: builtins.str,
        vpc_id: builtins.str,
        access_user: typing.Optional[builtins.str] = None,
        arch_type: typing.Optional[builtins.str] = None,
        available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cross_vpc_accesses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DmsDedicatedInstanceV2CrossVpcAccesses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disk_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_encrypted_key: typing.Optional[builtins.str] = None,
        enabled_mechanisms: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_publicip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ipv6_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        new_tenant_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        publicip_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        retention_policy: typing.Optional[builtins.str] = None,
        security_protocol: typing.Optional[builtins.str] = None,
        ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DmsDedicatedInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param broker_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#broker_num DmsDedicatedInstanceV2#broker_num}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#engine_version DmsDedicatedInstanceV2#engine_version}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#flavor_id DmsDedicatedInstanceV2#flavor_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#name DmsDedicatedInstanceV2#name}.
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#network_id DmsDedicatedInstanceV2#network_id}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#security_group_id DmsDedicatedInstanceV2#security_group_id}.
        :param storage_space: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#storage_space DmsDedicatedInstanceV2#storage_space}.
        :param storage_spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#storage_spec_code DmsDedicatedInstanceV2#storage_spec_code}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#vpc_id DmsDedicatedInstanceV2#vpc_id}.
        :param access_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#access_user DmsDedicatedInstanceV2#access_user}.
        :param arch_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#arch_type DmsDedicatedInstanceV2#arch_type}.
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#available_zones DmsDedicatedInstanceV2#available_zones}.
        :param cross_vpc_accesses: cross_vpc_accesses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#cross_vpc_accesses DmsDedicatedInstanceV2#cross_vpc_accesses}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#description DmsDedicatedInstanceV2#description}.
        :param disk_encrypted_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#disk_encrypted_enable DmsDedicatedInstanceV2#disk_encrypted_enable}.
        :param disk_encrypted_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#disk_encrypted_key DmsDedicatedInstanceV2#disk_encrypted_key}.
        :param enabled_mechanisms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#enabled_mechanisms DmsDedicatedInstanceV2#enabled_mechanisms}.
        :param enable_publicip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#enable_publicip DmsDedicatedInstanceV2#enable_publicip}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#id DmsDedicatedInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ipv6_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#ipv6_enable DmsDedicatedInstanceV2#ipv6_enable}.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#maintain_begin DmsDedicatedInstanceV2#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#maintain_end DmsDedicatedInstanceV2#maintain_end}.
        :param new_tenant_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#new_tenant_ips DmsDedicatedInstanceV2#new_tenant_ips}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#password DmsDedicatedInstanceV2#password}.
        :param publicip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#publicip_id DmsDedicatedInstanceV2#publicip_id}.
        :param retention_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#retention_policy DmsDedicatedInstanceV2#retention_policy}.
        :param security_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#security_protocol DmsDedicatedInstanceV2#security_protocol}.
        :param ssl_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#ssl_enable DmsDedicatedInstanceV2#ssl_enable}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#tags DmsDedicatedInstanceV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#timeouts DmsDedicatedInstanceV2#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DmsDedicatedInstanceV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69edd0722f50c74f5f3a7332a95462397feb8100ea374ed806c5027f462bbb18)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument broker_num", value=broker_num, expected_type=type_hints["broker_num"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument storage_space", value=storage_space, expected_type=type_hints["storage_space"])
            check_type(argname="argument storage_spec_code", value=storage_spec_code, expected_type=type_hints["storage_spec_code"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument access_user", value=access_user, expected_type=type_hints["access_user"])
            check_type(argname="argument arch_type", value=arch_type, expected_type=type_hints["arch_type"])
            check_type(argname="argument available_zones", value=available_zones, expected_type=type_hints["available_zones"])
            check_type(argname="argument cross_vpc_accesses", value=cross_vpc_accesses, expected_type=type_hints["cross_vpc_accesses"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk_encrypted_enable", value=disk_encrypted_enable, expected_type=type_hints["disk_encrypted_enable"])
            check_type(argname="argument disk_encrypted_key", value=disk_encrypted_key, expected_type=type_hints["disk_encrypted_key"])
            check_type(argname="argument enabled_mechanisms", value=enabled_mechanisms, expected_type=type_hints["enabled_mechanisms"])
            check_type(argname="argument enable_publicip", value=enable_publicip, expected_type=type_hints["enable_publicip"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ipv6_enable", value=ipv6_enable, expected_type=type_hints["ipv6_enable"])
            check_type(argname="argument maintain_begin", value=maintain_begin, expected_type=type_hints["maintain_begin"])
            check_type(argname="argument maintain_end", value=maintain_end, expected_type=type_hints["maintain_end"])
            check_type(argname="argument new_tenant_ips", value=new_tenant_ips, expected_type=type_hints["new_tenant_ips"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument publicip_id", value=publicip_id, expected_type=type_hints["publicip_id"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument security_protocol", value=security_protocol, expected_type=type_hints["security_protocol"])
            check_type(argname="argument ssl_enable", value=ssl_enable, expected_type=type_hints["ssl_enable"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "broker_num": broker_num,
            "engine_version": engine_version,
            "flavor_id": flavor_id,
            "name": name,
            "network_id": network_id,
            "security_group_id": security_group_id,
            "storage_space": storage_space,
            "storage_spec_code": storage_spec_code,
            "vpc_id": vpc_id,
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
        if access_user is not None:
            self._values["access_user"] = access_user
        if arch_type is not None:
            self._values["arch_type"] = arch_type
        if available_zones is not None:
            self._values["available_zones"] = available_zones
        if cross_vpc_accesses is not None:
            self._values["cross_vpc_accesses"] = cross_vpc_accesses
        if description is not None:
            self._values["description"] = description
        if disk_encrypted_enable is not None:
            self._values["disk_encrypted_enable"] = disk_encrypted_enable
        if disk_encrypted_key is not None:
            self._values["disk_encrypted_key"] = disk_encrypted_key
        if enabled_mechanisms is not None:
            self._values["enabled_mechanisms"] = enabled_mechanisms
        if enable_publicip is not None:
            self._values["enable_publicip"] = enable_publicip
        if id is not None:
            self._values["id"] = id
        if ipv6_enable is not None:
            self._values["ipv6_enable"] = ipv6_enable
        if maintain_begin is not None:
            self._values["maintain_begin"] = maintain_begin
        if maintain_end is not None:
            self._values["maintain_end"] = maintain_end
        if new_tenant_ips is not None:
            self._values["new_tenant_ips"] = new_tenant_ips
        if password is not None:
            self._values["password"] = password
        if publicip_id is not None:
            self._values["publicip_id"] = publicip_id
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if security_protocol is not None:
            self._values["security_protocol"] = security_protocol
        if ssl_enable is not None:
            self._values["ssl_enable"] = ssl_enable
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def broker_num(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#broker_num DmsDedicatedInstanceV2#broker_num}.'''
        result = self._values.get("broker_num")
        assert result is not None, "Required property 'broker_num' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def engine_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#engine_version DmsDedicatedInstanceV2#engine_version}.'''
        result = self._values.get("engine_version")
        assert result is not None, "Required property 'engine_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flavor_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#flavor_id DmsDedicatedInstanceV2#flavor_id}.'''
        result = self._values.get("flavor_id")
        assert result is not None, "Required property 'flavor_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#name DmsDedicatedInstanceV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#network_id DmsDedicatedInstanceV2#network_id}.'''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#security_group_id DmsDedicatedInstanceV2#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_space(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#storage_space DmsDedicatedInstanceV2#storage_space}.'''
        result = self._values.get("storage_space")
        assert result is not None, "Required property 'storage_space' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage_spec_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#storage_spec_code DmsDedicatedInstanceV2#storage_spec_code}.'''
        result = self._values.get("storage_spec_code")
        assert result is not None, "Required property 'storage_spec_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#vpc_id DmsDedicatedInstanceV2#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#access_user DmsDedicatedInstanceV2#access_user}.'''
        result = self._values.get("access_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def arch_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#arch_type DmsDedicatedInstanceV2#arch_type}.'''
        result = self._values.get("arch_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def available_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#available_zones DmsDedicatedInstanceV2#available_zones}.'''
        result = self._values.get("available_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cross_vpc_accesses(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsDedicatedInstanceV2CrossVpcAccesses"]]]:
        '''cross_vpc_accesses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#cross_vpc_accesses DmsDedicatedInstanceV2#cross_vpc_accesses}
        '''
        result = self._values.get("cross_vpc_accesses")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DmsDedicatedInstanceV2CrossVpcAccesses"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#description DmsDedicatedInstanceV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encrypted_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#disk_encrypted_enable DmsDedicatedInstanceV2#disk_encrypted_enable}.'''
        result = self._values.get("disk_encrypted_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#disk_encrypted_key DmsDedicatedInstanceV2#disk_encrypted_key}.'''
        result = self._values.get("disk_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled_mechanisms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#enabled_mechanisms DmsDedicatedInstanceV2#enabled_mechanisms}.'''
        result = self._values.get("enabled_mechanisms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_publicip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#enable_publicip DmsDedicatedInstanceV2#enable_publicip}.'''
        result = self._values.get("enable_publicip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#id DmsDedicatedInstanceV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#ipv6_enable DmsDedicatedInstanceV2#ipv6_enable}.'''
        result = self._values.get("ipv6_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maintain_begin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#maintain_begin DmsDedicatedInstanceV2#maintain_begin}.'''
        result = self._values.get("maintain_begin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#maintain_end DmsDedicatedInstanceV2#maintain_end}.'''
        result = self._values.get("maintain_end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def new_tenant_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#new_tenant_ips DmsDedicatedInstanceV2#new_tenant_ips}.'''
        result = self._values.get("new_tenant_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#password DmsDedicatedInstanceV2#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publicip_id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#publicip_id DmsDedicatedInstanceV2#publicip_id}.'''
        result = self._values.get("publicip_id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#retention_policy DmsDedicatedInstanceV2#retention_policy}.'''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#security_protocol DmsDedicatedInstanceV2#security_protocol}.'''
        result = self._values.get("security_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#ssl_enable DmsDedicatedInstanceV2#ssl_enable}.'''
        result = self._values.get("ssl_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#tags DmsDedicatedInstanceV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DmsDedicatedInstanceV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#timeouts DmsDedicatedInstanceV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DmsDedicatedInstanceV2Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsDedicatedInstanceV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsDedicatedInstanceV2.DmsDedicatedInstanceV2CrossVpcAccesses",
    jsii_struct_bases=[],
    name_mapping={"advertised_ip": "advertisedIp"},
)
class DmsDedicatedInstanceV2CrossVpcAccesses:
    def __init__(self, *, advertised_ip: typing.Optional[builtins.str] = None) -> None:
        '''
        :param advertised_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#advertised_ip DmsDedicatedInstanceV2#advertised_ip}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803c2cb821906fafe2ecf1091acbb2776765448fd5cc865a9b478acf9a85c620)
            check_type(argname="argument advertised_ip", value=advertised_ip, expected_type=type_hints["advertised_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advertised_ip is not None:
            self._values["advertised_ip"] = advertised_ip

    @builtins.property
    def advertised_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#advertised_ip DmsDedicatedInstanceV2#advertised_ip}.'''
        result = self._values.get("advertised_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsDedicatedInstanceV2CrossVpcAccesses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsDedicatedInstanceV2CrossVpcAccessesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsDedicatedInstanceV2.DmsDedicatedInstanceV2CrossVpcAccessesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2528187f11a4a9139ec9b63398b27017530f8a76ba7efa166878f02f0abefd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DmsDedicatedInstanceV2CrossVpcAccessesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd62cb21784d98635be86c13a8e14a062e62f9c712c9ba4b2accfa846019ce95)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DmsDedicatedInstanceV2CrossVpcAccessesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b1c8ef3a2a8d7c9317694511bcf63a911e9fe34057c15de0e50b6240f4aa97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bf0b6b48c2e81f5aa12b90c5628fdbfedb4a5f7321646c2976a4b028dd83d2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd95dc95c93250e96875a885cdac84ec22c0f182e930d5e55fa955602524eb03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsDedicatedInstanceV2CrossVpcAccesses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsDedicatedInstanceV2CrossVpcAccesses]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsDedicatedInstanceV2CrossVpcAccesses]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783d43c22684dd8cc03837e0a0217b5f37d8d5e06498dd544ce90ca32fd5e214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DmsDedicatedInstanceV2CrossVpcAccessesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsDedicatedInstanceV2.DmsDedicatedInstanceV2CrossVpcAccessesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__748900507b140b2a15eba501431aee73a76e2b5471dac4b9a598962abc2b02c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdvertisedIp")
    def reset_advertised_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedIp", []))

    @builtins.property
    @jsii.member(jsii_name="listenerIp")
    def listener_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listenerIp"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="portId")
    def port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portId"))

    @builtins.property
    @jsii.member(jsii_name="advertisedIpInput")
    def advertised_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "advertisedIpInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedIp")
    def advertised_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "advertisedIp"))

    @advertised_ip.setter
    def advertised_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b0514bd7be9f893e522ef7b5e19881acaa5e90981bf68fbe241ca5dee9a6b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsDedicatedInstanceV2CrossVpcAccesses]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsDedicatedInstanceV2CrossVpcAccesses]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsDedicatedInstanceV2CrossVpcAccesses]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8c6a8da73a1161939aff311b18ba932a1300b34eb17a39d40b9279808f0420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsDedicatedInstanceV2.DmsDedicatedInstanceV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DmsDedicatedInstanceV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#create DmsDedicatedInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#delete DmsDedicatedInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#update DmsDedicatedInstanceV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365f4eaf665e04c18adbee48a1d1f41c729a7fae96d6a29488f7e452c1550d21)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#create DmsDedicatedInstanceV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#delete DmsDedicatedInstanceV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_dedicated_instance_v2#update DmsDedicatedInstanceV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsDedicatedInstanceV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsDedicatedInstanceV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsDedicatedInstanceV2.DmsDedicatedInstanceV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56ee9e3626497195116ce4df9b984af2c3dabac79f93fda1898dd52fb97781a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9e719a357867ae0e3690953016bb06676910c28329089714b8e58e5c189d7472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664016c726f7fa4694556b1a5edfeb0278dad65aa7e5dd2ff128147025117fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2280ec99f64302e0a658d8ddebeda5941f803c430e5314483eab5603f5aadaf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsDedicatedInstanceV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsDedicatedInstanceV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsDedicatedInstanceV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f79ebc4d48724eb1f80fca3517301964131ef44f6c9b9268fd839ded900c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DmsDedicatedInstanceV2",
    "DmsDedicatedInstanceV2Config",
    "DmsDedicatedInstanceV2CrossVpcAccesses",
    "DmsDedicatedInstanceV2CrossVpcAccessesList",
    "DmsDedicatedInstanceV2CrossVpcAccessesOutputReference",
    "DmsDedicatedInstanceV2Timeouts",
    "DmsDedicatedInstanceV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2bb71df079517ca847a5db24c561d90a1023a35ec45c4049c7424bcb0af05ec8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    broker_num: jsii.Number,
    engine_version: builtins.str,
    flavor_id: builtins.str,
    name: builtins.str,
    network_id: builtins.str,
    security_group_id: builtins.str,
    storage_space: jsii.Number,
    storage_spec_code: builtins.str,
    vpc_id: builtins.str,
    access_user: typing.Optional[builtins.str] = None,
    arch_type: typing.Optional[builtins.str] = None,
    available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cross_vpc_accesses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsDedicatedInstanceV2CrossVpcAccesses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disk_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_encrypted_key: typing.Optional[builtins.str] = None,
    enabled_mechanisms: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_publicip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ipv6_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    new_tenant_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    publicip_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    retention_policy: typing.Optional[builtins.str] = None,
    security_protocol: typing.Optional[builtins.str] = None,
    ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DmsDedicatedInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__66dd84eb804e6d6209d6eef1edeb812ef6da949baa3189462a28581f3daf4592(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab24089974c6cb6250db3e7fd9a818bfebe7fa214a368dc0f494a88a013f77f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsDedicatedInstanceV2CrossVpcAccesses, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b9e2c1e152cb2d70a6c9237088f4c2574afc43d12ac3f760369cdcf1d0e4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106c005057636118ef4b162573e1e49063bbc2d2c89364ac367a680e338e6619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc6edf5b308ac3af73a2add8d3501cdb23a9a143669f5d407cfadf9daecfb0f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5442eb11f1f01fe980f52529d12ffccfa3f720bac07c30766eb38a32543be3f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a7af111bc74c9e656a3137d8cb5cf76254bb23ad5750ea82b043528a0e872b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c6e658cc695e6d66aaef410b0de9e04e3e0cb867be3ecc1ecb316d6b8c28b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112a2d9719cf7cd49751dd538570a6f49623fc26c86af8794a3a08d113af1e25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eed1e84aaaefb78dcb3854232ae82346b9810efe07a6b0128561c95fa124d6e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6acf2020762a11d670b1e0329150b5829e419105ac9ebf659964444b5ab1b33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55f6fc63b5dd1d9e9dc42e7eaeb2c1c71d223f2f2d2811826149693a06012aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119293bb38606b63004d6f8f9424006409c3742938e61a8a0d60f4b0fd628fcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1056b9558a59ff6007cedbd6cd68da8dfa425cb34f305ed9bc293e04cf5932c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477e182788922f4087e5e7db2456d385c582c8fcf227e1c8fbfd79a7e55c8eea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67e5c34c0b94ba801f15de1677caf163808c8999e63b3d84f06735927956ae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3765655a427272d914a93c922e8251c12daaca1147a3334249edaefae8a65609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7599772ae43da77518b918de6abfdd042b697ec2bed17ef978907036e87b5639(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b74991207060d966f2c4dfc98bfa407a0f2f0bd2bac6fdf29a9a9043006f5c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0564ea626aa85420835747eaf64042e9057c5d9b2da932534c24260b30608c5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3651befc37eea42ea9d659cd6c3bd641a53d01ef15e1b00ae59b5fbd5db67714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9ceb6aea4979c2feba0506fba7880cd82752739566550657e0cc59df867cc7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044292e4106a326c6c5b9e91620012a8fccbcd5f4078646e732e57bf4d3c16ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b3be22f51a5c8b3d6be27e27a1f5334bcc3ebc4eaded3ea559ffe14d29923a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37be3d9acab2861946a3905f0e30f4fe8b06e0ecbabbd1681511e655517631c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce78d60a312c84f4839be2916cecc1974f72f4ec89d3272a968859f693ece6fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642748e8c10b9b80e6f6adc7f1f06095aaac800ee3eb4957535cac53cb3ee3c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf185d2dcea3a15dc42e32214325986d69b8e7bd5c9a8768206c38136262ac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0ef9c57bfeca7465783eb6b01bc945680661c419c2eb48bcdb3632d30f6ea1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91f1d48c3f69a8b67c1cae7bc228a1b44a5a8d687b275a91470b9da68659b2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69edd0722f50c74f5f3a7332a95462397feb8100ea374ed806c5027f462bbb18(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    broker_num: jsii.Number,
    engine_version: builtins.str,
    flavor_id: builtins.str,
    name: builtins.str,
    network_id: builtins.str,
    security_group_id: builtins.str,
    storage_space: jsii.Number,
    storage_spec_code: builtins.str,
    vpc_id: builtins.str,
    access_user: typing.Optional[builtins.str] = None,
    arch_type: typing.Optional[builtins.str] = None,
    available_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cross_vpc_accesses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DmsDedicatedInstanceV2CrossVpcAccesses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disk_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_encrypted_key: typing.Optional[builtins.str] = None,
    enabled_mechanisms: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_publicip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ipv6_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    new_tenant_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    publicip_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    retention_policy: typing.Optional[builtins.str] = None,
    security_protocol: typing.Optional[builtins.str] = None,
    ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DmsDedicatedInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803c2cb821906fafe2ecf1091acbb2776765448fd5cc865a9b478acf9a85c620(
    *,
    advertised_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2528187f11a4a9139ec9b63398b27017530f8a76ba7efa166878f02f0abefd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd62cb21784d98635be86c13a8e14a062e62f9c712c9ba4b2accfa846019ce95(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b1c8ef3a2a8d7c9317694511bcf63a911e9fe34057c15de0e50b6240f4aa97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf0b6b48c2e81f5aa12b90c5628fdbfedb4a5f7321646c2976a4b028dd83d2c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd95dc95c93250e96875a885cdac84ec22c0f182e930d5e55fa955602524eb03(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783d43c22684dd8cc03837e0a0217b5f37d8d5e06498dd544ce90ca32fd5e214(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DmsDedicatedInstanceV2CrossVpcAccesses]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748900507b140b2a15eba501431aee73a76e2b5471dac4b9a598962abc2b02c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b0514bd7be9f893e522ef7b5e19881acaa5e90981bf68fbe241ca5dee9a6b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8c6a8da73a1161939aff311b18ba932a1300b34eb17a39d40b9279808f0420(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsDedicatedInstanceV2CrossVpcAccesses]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365f4eaf665e04c18adbee48a1d1f41c729a7fae96d6a29488f7e452c1550d21(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ee9e3626497195116ce4df9b984af2c3dabac79f93fda1898dd52fb97781a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e719a357867ae0e3690953016bb06676910c28329089714b8e58e5c189d7472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664016c726f7fa4694556b1a5edfeb0278dad65aa7e5dd2ff128147025117fc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2280ec99f64302e0a658d8ddebeda5941f803c430e5314483eab5603f5aadaf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f79ebc4d48724eb1f80fca3517301964131ef44f6c9b9268fd839ded900c39(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsDedicatedInstanceV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
