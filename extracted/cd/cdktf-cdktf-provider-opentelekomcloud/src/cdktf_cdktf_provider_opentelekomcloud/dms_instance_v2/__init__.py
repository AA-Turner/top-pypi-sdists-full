r'''
# `opentelekomcloud_dms_instance_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dms_instance_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2).
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


class DmsInstanceV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsInstanceV2.DmsInstanceV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2 opentelekomcloud_dms_instance_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        available_zones: typing.Sequence[builtins.str],
        engine: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        product_id: builtins.str,
        security_group_id: builtins.str,
        storage_space: jsii.Number,
        storage_spec_code: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        access_user: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disk_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_encrypted_key: typing.Optional[builtins.str] = None,
        enable_publicip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        partition_num: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        public_bandwidth: typing.Optional[jsii.Number] = None,
        publicip_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        retention_policy: typing.Optional[builtins.str] = None,
        specification: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DmsInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2 opentelekomcloud_dms_instance_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#available_zones DmsInstanceV2#available_zones}.
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#engine DmsInstanceV2#engine}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#engine_version DmsInstanceV2#engine_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#name DmsInstanceV2#name}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#product_id DmsInstanceV2#product_id}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#security_group_id DmsInstanceV2#security_group_id}.
        :param storage_space: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#storage_space DmsInstanceV2#storage_space}.
        :param storage_spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#storage_spec_code DmsInstanceV2#storage_spec_code}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#subnet_id DmsInstanceV2#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#vpc_id DmsInstanceV2#vpc_id}.
        :param access_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#access_user DmsInstanceV2#access_user}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#description DmsInstanceV2#description}.
        :param disk_encrypted_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#disk_encrypted_enable DmsInstanceV2#disk_encrypted_enable}.
        :param disk_encrypted_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#disk_encrypted_key DmsInstanceV2#disk_encrypted_key}.
        :param enable_publicip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#enable_publicip DmsInstanceV2#enable_publicip}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#id DmsInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#maintain_begin DmsInstanceV2#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#maintain_end DmsInstanceV2#maintain_end}.
        :param partition_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#partition_num DmsInstanceV2#partition_num}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#password DmsInstanceV2#password}.
        :param public_bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#public_bandwidth DmsInstanceV2#public_bandwidth}.
        :param publicip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#publicip_id DmsInstanceV2#publicip_id}.
        :param retention_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#retention_policy DmsInstanceV2#retention_policy}.
        :param specification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#specification DmsInstanceV2#specification}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#tags DmsInstanceV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#timeouts DmsInstanceV2#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b578e6d0598fb1ba884d572177084b3d087b7452a5845681921980f5a1cdcf2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DmsInstanceV2Config(
            available_zones=available_zones,
            engine=engine,
            engine_version=engine_version,
            name=name,
            product_id=product_id,
            security_group_id=security_group_id,
            storage_space=storage_space,
            storage_spec_code=storage_spec_code,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            access_user=access_user,
            description=description,
            disk_encrypted_enable=disk_encrypted_enable,
            disk_encrypted_key=disk_encrypted_key,
            enable_publicip=enable_publicip,
            id=id,
            maintain_begin=maintain_begin,
            maintain_end=maintain_end,
            partition_num=partition_num,
            password=password,
            public_bandwidth=public_bandwidth,
            publicip_id=publicip_id,
            retention_policy=retention_policy,
            specification=specification,
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
        '''Generates CDKTF code for importing a DmsInstanceV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DmsInstanceV2 to import.
        :param import_from_id: The id of the existing DmsInstanceV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DmsInstanceV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff057b7386e49c584a2e25886dddc7578dce002a8421aea75e91db442423bec9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#create DmsInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#delete DmsInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#update DmsInstanceV2#update}.
        '''
        value = DmsInstanceV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessUser")
    def reset_access_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessUser", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiskEncryptedEnable")
    def reset_disk_encrypted_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptedEnable", []))

    @jsii.member(jsii_name="resetDiskEncryptedKey")
    def reset_disk_encrypted_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptedKey", []))

    @jsii.member(jsii_name="resetEnablePublicip")
    def reset_enable_publicip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePublicip", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintainBegin")
    def reset_maintain_begin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainBegin", []))

    @jsii.member(jsii_name="resetMaintainEnd")
    def reset_maintain_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainEnd", []))

    @jsii.member(jsii_name="resetPartitionNum")
    def reset_partition_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionNum", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPublicBandwidth")
    def reset_public_bandwidth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicBandwidth", []))

    @jsii.member(jsii_name="resetPublicipId")
    def reset_publicip_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicipId", []))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetSpecification")
    def reset_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecification", []))

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
    @jsii.member(jsii_name="connectAddress")
    def connect_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectAddress"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="nodeNum")
    def node_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeNum"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="publicAccessEnabled")
    def public_access_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicAccessEnabled"))

    @builtins.property
    @jsii.member(jsii_name="publicConnectAddress")
    def public_connect_address(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicConnectAddress"))

    @builtins.property
    @jsii.member(jsii_name="resourceSpecCode")
    def resource_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSpecCode"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupName"))

    @builtins.property
    @jsii.member(jsii_name="sslEnable")
    def ssl_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "sslEnable"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @builtins.property
    @jsii.member(jsii_name="subnetCidr")
    def subnet_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetCidr"))

    @builtins.property
    @jsii.member(jsii_name="subnetName")
    def subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetName"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DmsInstanceV2TimeoutsOutputReference":
        return typing.cast("DmsInstanceV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="totalStorageSpace")
    def total_storage_space(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalStorageSpace"))

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
    @jsii.member(jsii_name="vpcName")
    def vpc_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcName"))

    @builtins.property
    @jsii.member(jsii_name="accessUserInput")
    def access_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessUserInput"))

    @builtins.property
    @jsii.member(jsii_name="availableZonesInput")
    def available_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availableZonesInput"))

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
    @jsii.member(jsii_name="enablePublicipInput")
    def enable_publicip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePublicipInput"))

    @builtins.property
    @jsii.member(jsii_name="engineInput")
    def engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineInput"))

    @builtins.property
    @jsii.member(jsii_name="engineVersionInput")
    def engine_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="partitionNumInput")
    def partition_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "partitionNumInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="productIdInput")
    def product_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicBandwidthInput")
    def public_bandwidth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "publicBandwidthInput"))

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
    @jsii.member(jsii_name="specificationInput")
    def specification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "specificationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSpaceInput")
    def storage_space_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageSpaceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSpecCodeInput")
    def storage_spec_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageSpecCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DmsInstanceV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DmsInstanceV2Timeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e40ef368377d620571f406a4381da20ba435cf456183d08aa266fce5425fba3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableZones")
    def available_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableZones"))

    @available_zones.setter
    def available_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714296e06f3d6f580d0f4cd2c20a78d71e0b77eab3bc20ba77ea29976a65a4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec29581610a3fdc6bbd66835347bf8595def38d7f11883c2a4f957346a6818ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26b1b6204ed4c8c3a9b3ad6c5ce7a0f2fb85b1a418b2ad3845654702b7612c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptedEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptedKey")
    def disk_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptedKey"))

    @disk_encrypted_key.setter
    def disk_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eaa8a73a69cfb53be3b9346bcd90578ea8eaf255c03f0c537373eeaba1db393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptedKey", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__919348c6f1b7bc4dc1d9d352918a7d7ba26ffeb317782efef2ad72e0e921f04d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePublicip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2cd16521a78bdfa7ed5cc2b4f8af4cd5ddc7461343689fefc40140d1528d313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfbba8afcd8ca405071e5fc632597d38c09a38861883eff801f5f001e435a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4904ca03529b32d9e898b3a703e26af85262759ca21b80af2734d16777d80644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainBegin")
    def maintain_begin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainBegin"))

    @maintain_begin.setter
    def maintain_begin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036a2a65db1c3f0fa823220415d58d67c0a9afb39db5f41dd0f2c7bbc0c42f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainBegin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainEnd")
    def maintain_end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainEnd"))

    @maintain_end.setter
    def maintain_end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a823ed7d6765435315aaefcb08894360be1e5860ae60f25e05c7cebfaecac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d04e8df3cac3290bf7d250c26fb1620b7b2997bedd98d3426ff2a087d7caf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionNum")
    def partition_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "partitionNum"))

    @partition_num.setter
    def partition_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939240f296a3ebe4cdc3ed6a44072349ab63a03a9b50f05614ef240e6726d578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0d393bd9024ebf4fa5b924845485d27d1dff9a69cc82afd309e24f8438b720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f60984c67da317774a13da2b9648e457be96957e877900bcfb5ef2cf1233b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicBandwidth")
    def public_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "publicBandwidth"))

    @public_bandwidth.setter
    def public_bandwidth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002c9638160c5f4761b8abcfd2e337f0ace23d0df4b20d40b7b77a2810e93a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicBandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicipId")
    def publicip_id(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicipId"))

    @publicip_id.setter
    def publicip_id(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ba70f0c2fda0d5a7cd7d34f70a878f2b85c77865f678cb931cff3929b8bece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicipId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionPolicy"))

    @retention_policy.setter
    def retention_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbba527978bfde29595e74e46ebed6124bf331d04f50ba36fe41e99569dda693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1548bfab81d4ff94a65e382d63c8be8e7ede3529b15ab023b9bde93a9a41f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="specification")
    def specification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specification"))

    @specification.setter
    def specification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74edec1d7c9d4f9ed86d16b42983aa7813d9ef0652ac6410c05d92a06e5ca9c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSpace")
    def storage_space(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageSpace"))

    @storage_space.setter
    def storage_space(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054dd20e4d83fb31f60d428a61273c3eb5209c552f7cda14e5777579f7969de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSpace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSpecCode")
    def storage_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSpecCode"))

    @storage_spec_code.setter
    def storage_spec_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd44526a5f90c6eeab5108d3d034d8bd1d2d89187375453922d159f1063bd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSpecCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dbd5e4ca1d6870c0bf233dad64eea01f3937abd558ca3d24470a380b262ce42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac30f4aea25637ceb46c42520da08a29ca0f5b172e3f11a20356d9f9a639730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cdd7d6bd2069f7068347ec422cb8384dd32e7bfed991d433a90fc45075ae07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsInstanceV2.DmsInstanceV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "available_zones": "availableZones",
        "engine": "engine",
        "engine_version": "engineVersion",
        "name": "name",
        "product_id": "productId",
        "security_group_id": "securityGroupId",
        "storage_space": "storageSpace",
        "storage_spec_code": "storageSpecCode",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "access_user": "accessUser",
        "description": "description",
        "disk_encrypted_enable": "diskEncryptedEnable",
        "disk_encrypted_key": "diskEncryptedKey",
        "enable_publicip": "enablePublicip",
        "id": "id",
        "maintain_begin": "maintainBegin",
        "maintain_end": "maintainEnd",
        "partition_num": "partitionNum",
        "password": "password",
        "public_bandwidth": "publicBandwidth",
        "publicip_id": "publicipId",
        "retention_policy": "retentionPolicy",
        "specification": "specification",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class DmsInstanceV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        available_zones: typing.Sequence[builtins.str],
        engine: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        product_id: builtins.str,
        security_group_id: builtins.str,
        storage_space: jsii.Number,
        storage_spec_code: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        access_user: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disk_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_encrypted_key: typing.Optional[builtins.str] = None,
        enable_publicip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        partition_num: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        public_bandwidth: typing.Optional[jsii.Number] = None,
        publicip_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        retention_policy: typing.Optional[builtins.str] = None,
        specification: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DmsInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#available_zones DmsInstanceV2#available_zones}.
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#engine DmsInstanceV2#engine}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#engine_version DmsInstanceV2#engine_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#name DmsInstanceV2#name}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#product_id DmsInstanceV2#product_id}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#security_group_id DmsInstanceV2#security_group_id}.
        :param storage_space: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#storage_space DmsInstanceV2#storage_space}.
        :param storage_spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#storage_spec_code DmsInstanceV2#storage_spec_code}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#subnet_id DmsInstanceV2#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#vpc_id DmsInstanceV2#vpc_id}.
        :param access_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#access_user DmsInstanceV2#access_user}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#description DmsInstanceV2#description}.
        :param disk_encrypted_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#disk_encrypted_enable DmsInstanceV2#disk_encrypted_enable}.
        :param disk_encrypted_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#disk_encrypted_key DmsInstanceV2#disk_encrypted_key}.
        :param enable_publicip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#enable_publicip DmsInstanceV2#enable_publicip}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#id DmsInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#maintain_begin DmsInstanceV2#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#maintain_end DmsInstanceV2#maintain_end}.
        :param partition_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#partition_num DmsInstanceV2#partition_num}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#password DmsInstanceV2#password}.
        :param public_bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#public_bandwidth DmsInstanceV2#public_bandwidth}.
        :param publicip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#publicip_id DmsInstanceV2#publicip_id}.
        :param retention_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#retention_policy DmsInstanceV2#retention_policy}.
        :param specification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#specification DmsInstanceV2#specification}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#tags DmsInstanceV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#timeouts DmsInstanceV2#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DmsInstanceV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4d5176bc9fbf5c31979dfcceae44c6c404a88d7f9f242b5b32a521c88ec381)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument available_zones", value=available_zones, expected_type=type_hints["available_zones"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument storage_space", value=storage_space, expected_type=type_hints["storage_space"])
            check_type(argname="argument storage_spec_code", value=storage_spec_code, expected_type=type_hints["storage_spec_code"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument access_user", value=access_user, expected_type=type_hints["access_user"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk_encrypted_enable", value=disk_encrypted_enable, expected_type=type_hints["disk_encrypted_enable"])
            check_type(argname="argument disk_encrypted_key", value=disk_encrypted_key, expected_type=type_hints["disk_encrypted_key"])
            check_type(argname="argument enable_publicip", value=enable_publicip, expected_type=type_hints["enable_publicip"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintain_begin", value=maintain_begin, expected_type=type_hints["maintain_begin"])
            check_type(argname="argument maintain_end", value=maintain_end, expected_type=type_hints["maintain_end"])
            check_type(argname="argument partition_num", value=partition_num, expected_type=type_hints["partition_num"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument public_bandwidth", value=public_bandwidth, expected_type=type_hints["public_bandwidth"])
            check_type(argname="argument publicip_id", value=publicip_id, expected_type=type_hints["publicip_id"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument specification", value=specification, expected_type=type_hints["specification"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "available_zones": available_zones,
            "engine": engine,
            "engine_version": engine_version,
            "name": name,
            "product_id": product_id,
            "security_group_id": security_group_id,
            "storage_space": storage_space,
            "storage_spec_code": storage_spec_code,
            "subnet_id": subnet_id,
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
        if description is not None:
            self._values["description"] = description
        if disk_encrypted_enable is not None:
            self._values["disk_encrypted_enable"] = disk_encrypted_enable
        if disk_encrypted_key is not None:
            self._values["disk_encrypted_key"] = disk_encrypted_key
        if enable_publicip is not None:
            self._values["enable_publicip"] = enable_publicip
        if id is not None:
            self._values["id"] = id
        if maintain_begin is not None:
            self._values["maintain_begin"] = maintain_begin
        if maintain_end is not None:
            self._values["maintain_end"] = maintain_end
        if partition_num is not None:
            self._values["partition_num"] = partition_num
        if password is not None:
            self._values["password"] = password
        if public_bandwidth is not None:
            self._values["public_bandwidth"] = public_bandwidth
        if publicip_id is not None:
            self._values["publicip_id"] = publicip_id
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if specification is not None:
            self._values["specification"] = specification
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
    def available_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#available_zones DmsInstanceV2#available_zones}.'''
        result = self._values.get("available_zones")
        assert result is not None, "Required property 'available_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def engine(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#engine DmsInstanceV2#engine}.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#engine_version DmsInstanceV2#engine_version}.'''
        result = self._values.get("engine_version")
        assert result is not None, "Required property 'engine_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#name DmsInstanceV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#product_id DmsInstanceV2#product_id}.'''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#security_group_id DmsInstanceV2#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_space(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#storage_space DmsInstanceV2#storage_space}.'''
        result = self._values.get("storage_space")
        assert result is not None, "Required property 'storage_space' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage_spec_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#storage_spec_code DmsInstanceV2#storage_spec_code}.'''
        result = self._values.get("storage_spec_code")
        assert result is not None, "Required property 'storage_spec_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#subnet_id DmsInstanceV2#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#vpc_id DmsInstanceV2#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#access_user DmsInstanceV2#access_user}.'''
        result = self._values.get("access_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#description DmsInstanceV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encrypted_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#disk_encrypted_enable DmsInstanceV2#disk_encrypted_enable}.'''
        result = self._values.get("disk_encrypted_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#disk_encrypted_key DmsInstanceV2#disk_encrypted_key}.'''
        result = self._values.get("disk_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_publicip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#enable_publicip DmsInstanceV2#enable_publicip}.'''
        result = self._values.get("enable_publicip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#id DmsInstanceV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_begin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#maintain_begin DmsInstanceV2#maintain_begin}.'''
        result = self._values.get("maintain_begin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#maintain_end DmsInstanceV2#maintain_end}.'''
        result = self._values.get("maintain_end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#partition_num DmsInstanceV2#partition_num}.'''
        result = self._values.get("partition_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#password DmsInstanceV2#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_bandwidth(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#public_bandwidth DmsInstanceV2#public_bandwidth}.'''
        result = self._values.get("public_bandwidth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def publicip_id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#publicip_id DmsInstanceV2#publicip_id}.'''
        result = self._values.get("publicip_id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#retention_policy DmsInstanceV2#retention_policy}.'''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def specification(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#specification DmsInstanceV2#specification}.'''
        result = self._values.get("specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#tags DmsInstanceV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DmsInstanceV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#timeouts DmsInstanceV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DmsInstanceV2Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsInstanceV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsInstanceV2.DmsInstanceV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DmsInstanceV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#create DmsInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#delete DmsInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#update DmsInstanceV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f6848b544104db28de07288aa739f99edd8be46a78d2f28dc2555d3e75a4fe)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#create DmsInstanceV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#delete DmsInstanceV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_instance_v2#update DmsInstanceV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsInstanceV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsInstanceV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsInstanceV2.DmsInstanceV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60abd4ae860eec6a0119d1271253218ec3a26708144266a347d311a8ab5a817a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7edfe06bf5f4dfc40c82f7a10abd709b7af67f6971f7e69a215cd8b14a0ce32a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4e43ee62acf7cbe42c763dac5285521556721dda4c80b2d04fa4e87a6cacc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc889c72505e86298b4ff3bec596daf0a3fa6267bf718fc90634f59ed1bd06d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsInstanceV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsInstanceV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsInstanceV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6c44bd75f0685e74f85b6ca911a873258866bec8e22d8006a90e60ef196195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DmsInstanceV2",
    "DmsInstanceV2Config",
    "DmsInstanceV2Timeouts",
    "DmsInstanceV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3b578e6d0598fb1ba884d572177084b3d087b7452a5845681921980f5a1cdcf2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    available_zones: typing.Sequence[builtins.str],
    engine: builtins.str,
    engine_version: builtins.str,
    name: builtins.str,
    product_id: builtins.str,
    security_group_id: builtins.str,
    storage_space: jsii.Number,
    storage_spec_code: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    access_user: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disk_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_encrypted_key: typing.Optional[builtins.str] = None,
    enable_publicip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    partition_num: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    public_bandwidth: typing.Optional[jsii.Number] = None,
    publicip_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    retention_policy: typing.Optional[builtins.str] = None,
    specification: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DmsInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ff057b7386e49c584a2e25886dddc7578dce002a8421aea75e91db442423bec9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40ef368377d620571f406a4381da20ba435cf456183d08aa266fce5425fba3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714296e06f3d6f580d0f4cd2c20a78d71e0b77eab3bc20ba77ea29976a65a4ff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec29581610a3fdc6bbd66835347bf8595def38d7f11883c2a4f957346a6818ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b1b6204ed4c8c3a9b3ad6c5ce7a0f2fb85b1a418b2ad3845654702b7612c62(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eaa8a73a69cfb53be3b9346bcd90578ea8eaf255c03f0c537373eeaba1db393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919348c6f1b7bc4dc1d9d352918a7d7ba26ffeb317782efef2ad72e0e921f04d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2cd16521a78bdfa7ed5cc2b4f8af4cd5ddc7461343689fefc40140d1528d313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfbba8afcd8ca405071e5fc632597d38c09a38861883eff801f5f001e435a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4904ca03529b32d9e898b3a703e26af85262759ca21b80af2734d16777d80644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036a2a65db1c3f0fa823220415d58d67c0a9afb39db5f41dd0f2c7bbc0c42f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a823ed7d6765435315aaefcb08894360be1e5860ae60f25e05c7cebfaecac7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d04e8df3cac3290bf7d250c26fb1620b7b2997bedd98d3426ff2a087d7caf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939240f296a3ebe4cdc3ed6a44072349ab63a03a9b50f05614ef240e6726d578(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0d393bd9024ebf4fa5b924845485d27d1dff9a69cc82afd309e24f8438b720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f60984c67da317774a13da2b9648e457be96957e877900bcfb5ef2cf1233b3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002c9638160c5f4761b8abcfd2e337f0ace23d0df4b20d40b7b77a2810e93a43(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ba70f0c2fda0d5a7cd7d34f70a878f2b85c77865f678cb931cff3929b8bece(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbba527978bfde29595e74e46ebed6124bf331d04f50ba36fe41e99569dda693(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1548bfab81d4ff94a65e382d63c8be8e7ede3529b15ab023b9bde93a9a41f0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74edec1d7c9d4f9ed86d16b42983aa7813d9ef0652ac6410c05d92a06e5ca9c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054dd20e4d83fb31f60d428a61273c3eb5209c552f7cda14e5777579f7969de2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd44526a5f90c6eeab5108d3d034d8bd1d2d89187375453922d159f1063bd7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dbd5e4ca1d6870c0bf233dad64eea01f3937abd558ca3d24470a380b262ce42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac30f4aea25637ceb46c42520da08a29ca0f5b172e3f11a20356d9f9a639730(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cdd7d6bd2069f7068347ec422cb8384dd32e7bfed991d433a90fc45075ae07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4d5176bc9fbf5c31979dfcceae44c6c404a88d7f9f242b5b32a521c88ec381(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    available_zones: typing.Sequence[builtins.str],
    engine: builtins.str,
    engine_version: builtins.str,
    name: builtins.str,
    product_id: builtins.str,
    security_group_id: builtins.str,
    storage_space: jsii.Number,
    storage_spec_code: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    access_user: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disk_encrypted_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_encrypted_key: typing.Optional[builtins.str] = None,
    enable_publicip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    partition_num: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    public_bandwidth: typing.Optional[jsii.Number] = None,
    publicip_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    retention_policy: typing.Optional[builtins.str] = None,
    specification: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DmsInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f6848b544104db28de07288aa739f99edd8be46a78d2f28dc2555d3e75a4fe(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60abd4ae860eec6a0119d1271253218ec3a26708144266a347d311a8ab5a817a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7edfe06bf5f4dfc40c82f7a10abd709b7af67f6971f7e69a215cd8b14a0ce32a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4e43ee62acf7cbe42c763dac5285521556721dda4c80b2d04fa4e87a6cacc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc889c72505e86298b4ff3bec596daf0a3fa6267bf718fc90634f59ed1bd06d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6c44bd75f0685e74f85b6ca911a873258866bec8e22d8006a90e60ef196195(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsInstanceV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
