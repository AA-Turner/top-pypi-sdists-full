r'''
# `opentelekomcloud_dds_instance_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dds_instance_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3).
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


class DdsInstanceV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3 opentelekomcloud_dds_instance_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        datastore: typing.Union["DdsInstanceV3Datastore", typing.Dict[builtins.str, typing.Any]],
        flavor: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DdsInstanceV3Flavor", typing.Dict[builtins.str, typing.Any]]]],
        mode: builtins.str,
        name: builtins.str,
        password: builtins.str,
        security_group_id: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        backup_strategy: typing.Optional[typing.Union["DdsInstanceV3BackupStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DdsInstanceV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3 opentelekomcloud_dds_instance_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#availability_zone DdsInstanceV3#availability_zone}.
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#datastore DdsInstanceV3#datastore}
        :param flavor: flavor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#flavor DdsInstanceV3#flavor}
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#mode DdsInstanceV3#mode}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#name DdsInstanceV3#name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#password DdsInstanceV3#password}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#security_group_id DdsInstanceV3#security_group_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#subnet_id DdsInstanceV3#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#vpc_id DdsInstanceV3#vpc_id}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#backup_strategy DdsInstanceV3#backup_strategy}
        :param disk_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#disk_encryption_id DdsInstanceV3#disk_encryption_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#id DdsInstanceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#port DdsInstanceV3#port}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#region DdsInstanceV3#region}.
        :param ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#ssl DdsInstanceV3#ssl}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#tags DdsInstanceV3#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#timeouts DdsInstanceV3#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c14e5d67a802a9b10336125420ad02f11c81c6ac7d2886ed39d20a77c842ec8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DdsInstanceV3Config(
            availability_zone=availability_zone,
            datastore=datastore,
            flavor=flavor,
            mode=mode,
            name=name,
            password=password,
            security_group_id=security_group_id,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            backup_strategy=backup_strategy,
            disk_encryption_id=disk_encryption_id,
            id=id,
            port=port,
            region=region,
            ssl=ssl,
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
        '''Generates CDKTF code for importing a DdsInstanceV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DdsInstanceV3 to import.
        :param import_from_id: The id of the existing DdsInstanceV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DdsInstanceV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e5358c7cb80398d68088dc29afe5157189794a7db01a89303b4b0cd9e52ab8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupStrategy")
    def put_backup_strategy(
        self,
        *,
        keep_days: jsii.Number,
        start_time: builtins.str,
        period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keep_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#keep_days DdsInstanceV3#keep_days}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#start_time DdsInstanceV3#start_time}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#period DdsInstanceV3#period}.
        '''
        value = DdsInstanceV3BackupStrategy(
            keep_days=keep_days, start_time=start_time, period=period
        )

        return typing.cast(None, jsii.invoke(self, "putBackupStrategy", [value]))

    @jsii.member(jsii_name="putDatastore")
    def put_datastore(
        self,
        *,
        type: builtins.str,
        version: builtins.str,
        storage_engine: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#type DdsInstanceV3#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#version DdsInstanceV3#version}.
        :param storage_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#storage_engine DdsInstanceV3#storage_engine}.
        '''
        value = DdsInstanceV3Datastore(
            type=type, version=version, storage_engine=storage_engine
        )

        return typing.cast(None, jsii.invoke(self, "putDatastore", [value]))

    @jsii.member(jsii_name="putFlavor")
    def put_flavor(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DdsInstanceV3Flavor", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f227db8d1538323e0e818f3491690546c59175bad16d8ccacde1668b154b1c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFlavor", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#create DdsInstanceV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#delete DdsInstanceV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#update DdsInstanceV3#update}.
        '''
        value = DdsInstanceV3Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackupStrategy")
    def reset_backup_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupStrategy", []))

    @jsii.member(jsii_name="resetDiskEncryptionId")
    def reset_disk_encryption_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSsl")
    def reset_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsl", []))

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
    @jsii.member(jsii_name="backupStrategy")
    def backup_strategy(self) -> "DdsInstanceV3BackupStrategyOutputReference":
        return typing.cast("DdsInstanceV3BackupStrategyOutputReference", jsii.get(self, "backupStrategy"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> "DdsInstanceV3DatastoreOutputReference":
        return typing.cast("DdsInstanceV3DatastoreOutputReference", jsii.get(self, "datastore"))

    @builtins.property
    @jsii.member(jsii_name="dbUsername")
    def db_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbUsername"))

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> "DdsInstanceV3FlavorList":
        return typing.cast("DdsInstanceV3FlavorList", jsii.get(self, "flavor"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> "DdsInstanceV3NodesList":
        return typing.cast("DdsInstanceV3NodesList", jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="payMode")
    def pay_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payMode"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DdsInstanceV3TimeoutsOutputReference":
        return typing.cast("DdsInstanceV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="backupStrategyInput")
    def backup_strategy_input(self) -> typing.Optional["DdsInstanceV3BackupStrategy"]:
        return typing.cast(typing.Optional["DdsInstanceV3BackupStrategy"], jsii.get(self, "backupStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreInput")
    def datastore_input(self) -> typing.Optional["DdsInstanceV3Datastore"]:
        return typing.cast(typing.Optional["DdsInstanceV3Datastore"], jsii.get(self, "datastoreInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionIdInput")
    def disk_encryption_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DdsInstanceV3Flavor"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DdsInstanceV3Flavor"]]], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sslInput")
    def ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DdsInstanceV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DdsInstanceV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41f05f951c8b6bd903962fe0a1fbcffbe5034ade18c62cdf59f77c14a481d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionId")
    def disk_encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionId"))

    @disk_encryption_id.setter
    def disk_encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3264bf9bf0b462cbe63aa85df3e2dcddea1567780309b8412f297dfd7fc88a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525f6a4b2ba29e2f2404bfd79a6b782edd183e874be637efd2e388891708f47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ffb44e946dc5f1e489585cfabead9ae220c26924956baf4bdfe747c50fcf4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01b14978f8f11bc4cd07cffa9449cd6c200f96b8332eb31ddf1c8a355a1058c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d2eec64b60433d06e9b04b42fe4b0dd38915c07b21b870d89c7bb8931a9317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e35185a21542e2b6c4f3a96dac9960d5e154bfbf5e64238c5fa1673a6857a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7501ae673be5fcd5c3479c34b383bf8f526de50ab9c906bf69bad9fd2bde414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268eb8bd91f862803d5758a4d1fa60763e2a407c7305e50d49de58230951e53b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ssl"))

    @ssl.setter
    def ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8204df635b780859d2b31cc4d971d50d529ec2cf43e3477c8c086cd7eb4567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5b12af3f36637e9ca3b7dc51c3abb162a684a70a2b40b2e1814a4ee723eada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c892a5c54849fe53fe9eb36cf8de1ddb647691ec6e136ee56eb87ab1d0251943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e54c704eb0f3c3712b6ab98089b98ab1bedeaaa43eef86b91227c53f3fa06e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3BackupStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "keep_days": "keepDays",
        "start_time": "startTime",
        "period": "period",
    },
)
class DdsInstanceV3BackupStrategy:
    def __init__(
        self,
        *,
        keep_days: jsii.Number,
        start_time: builtins.str,
        period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keep_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#keep_days DdsInstanceV3#keep_days}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#start_time DdsInstanceV3#start_time}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#period DdsInstanceV3#period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6e93246ea8681ebedbebe93d7d7470312fd36163070e1197ca7f8d4c5f1659)
            check_type(argname="argument keep_days", value=keep_days, expected_type=type_hints["keep_days"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keep_days": keep_days,
            "start_time": start_time,
        }
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def keep_days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#keep_days DdsInstanceV3#keep_days}.'''
        result = self._values.get("keep_days")
        assert result is not None, "Required property 'keep_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#start_time DdsInstanceV3#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#period DdsInstanceV3#period}.'''
        result = self._values.get("period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DdsInstanceV3BackupStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DdsInstanceV3BackupStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3BackupStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfd53f86a098a1b1f58071402c3231e965c3966e2bcd491ede5c677c02f6dbdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPeriod")
    def reset_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="keepDaysInput")
    def keep_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="keepDays")
    def keep_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepDays"))

    @keep_days.setter
    def keep_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f983ff8680743a91926c575a80fed9b93df68d52c8451c31053a24116802e9d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8340ee496eac1df3291aac7bf194bb7d23fba4781f48e77a1df17143a5ce4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb39460c4df39b74b152eddaa39fd6eea28e93a339fe97f8c7d857ed017d99d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DdsInstanceV3BackupStrategy]:
        return typing.cast(typing.Optional[DdsInstanceV3BackupStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DdsInstanceV3BackupStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd14a2c74d7a1a887d4196a4f167c7f9ab81a16ee30e268f9e715590ce4de90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone": "availabilityZone",
        "datastore": "datastore",
        "flavor": "flavor",
        "mode": "mode",
        "name": "name",
        "password": "password",
        "security_group_id": "securityGroupId",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "backup_strategy": "backupStrategy",
        "disk_encryption_id": "diskEncryptionId",
        "id": "id",
        "port": "port",
        "region": "region",
        "ssl": "ssl",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class DdsInstanceV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone: builtins.str,
        datastore: typing.Union["DdsInstanceV3Datastore", typing.Dict[builtins.str, typing.Any]],
        flavor: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DdsInstanceV3Flavor", typing.Dict[builtins.str, typing.Any]]]],
        mode: builtins.str,
        name: builtins.str,
        password: builtins.str,
        security_group_id: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        backup_strategy: typing.Optional[typing.Union[DdsInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DdsInstanceV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#availability_zone DdsInstanceV3#availability_zone}.
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#datastore DdsInstanceV3#datastore}
        :param flavor: flavor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#flavor DdsInstanceV3#flavor}
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#mode DdsInstanceV3#mode}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#name DdsInstanceV3#name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#password DdsInstanceV3#password}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#security_group_id DdsInstanceV3#security_group_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#subnet_id DdsInstanceV3#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#vpc_id DdsInstanceV3#vpc_id}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#backup_strategy DdsInstanceV3#backup_strategy}
        :param disk_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#disk_encryption_id DdsInstanceV3#disk_encryption_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#id DdsInstanceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#port DdsInstanceV3#port}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#region DdsInstanceV3#region}.
        :param ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#ssl DdsInstanceV3#ssl}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#tags DdsInstanceV3#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#timeouts DdsInstanceV3#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(datastore, dict):
            datastore = DdsInstanceV3Datastore(**datastore)
        if isinstance(backup_strategy, dict):
            backup_strategy = DdsInstanceV3BackupStrategy(**backup_strategy)
        if isinstance(timeouts, dict):
            timeouts = DdsInstanceV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6bd873e25e0971ef20465260431633a7f858a07b465f8fa2324c83d0e5b8a3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument backup_strategy", value=backup_strategy, expected_type=type_hints["backup_strategy"])
            check_type(argname="argument disk_encryption_id", value=disk_encryption_id, expected_type=type_hints["disk_encryption_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ssl", value=ssl, expected_type=type_hints["ssl"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "datastore": datastore,
            "flavor": flavor,
            "mode": mode,
            "name": name,
            "password": password,
            "security_group_id": security_group_id,
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
        if backup_strategy is not None:
            self._values["backup_strategy"] = backup_strategy
        if disk_encryption_id is not None:
            self._values["disk_encryption_id"] = disk_encryption_id
        if id is not None:
            self._values["id"] = id
        if port is not None:
            self._values["port"] = port
        if region is not None:
            self._values["region"] = region
        if ssl is not None:
            self._values["ssl"] = ssl
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
    def availability_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#availability_zone DdsInstanceV3#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datastore(self) -> "DdsInstanceV3Datastore":
        '''datastore block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#datastore DdsInstanceV3#datastore}
        '''
        result = self._values.get("datastore")
        assert result is not None, "Required property 'datastore' is missing"
        return typing.cast("DdsInstanceV3Datastore", result)

    @builtins.property
    def flavor(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DdsInstanceV3Flavor"]]:
        '''flavor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#flavor DdsInstanceV3#flavor}
        '''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DdsInstanceV3Flavor"]], result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#mode DdsInstanceV3#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#name DdsInstanceV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#password DdsInstanceV3#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#security_group_id DdsInstanceV3#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#subnet_id DdsInstanceV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#vpc_id DdsInstanceV3#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_strategy(self) -> typing.Optional[DdsInstanceV3BackupStrategy]:
        '''backup_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#backup_strategy DdsInstanceV3#backup_strategy}
        '''
        result = self._values.get("backup_strategy")
        return typing.cast(typing.Optional[DdsInstanceV3BackupStrategy], result)

    @builtins.property
    def disk_encryption_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#disk_encryption_id DdsInstanceV3#disk_encryption_id}.'''
        result = self._values.get("disk_encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#id DdsInstanceV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#port DdsInstanceV3#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#region DdsInstanceV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#ssl DdsInstanceV3#ssl}.'''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#tags DdsInstanceV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DdsInstanceV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#timeouts DdsInstanceV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DdsInstanceV3Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DdsInstanceV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3Datastore",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "version": "version",
        "storage_engine": "storageEngine",
    },
)
class DdsInstanceV3Datastore:
    def __init__(
        self,
        *,
        type: builtins.str,
        version: builtins.str,
        storage_engine: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#type DdsInstanceV3#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#version DdsInstanceV3#version}.
        :param storage_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#storage_engine DdsInstanceV3#storage_engine}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e8c96f4b1036d194319e8e825437fa2089b471ae5f58ae2e7cfa98d1ac8b9a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument storage_engine", value=storage_engine, expected_type=type_hints["storage_engine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "version": version,
        }
        if storage_engine is not None:
            self._values["storage_engine"] = storage_engine

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#type DdsInstanceV3#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#version DdsInstanceV3#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_engine(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#storage_engine DdsInstanceV3#storage_engine}.'''
        result = self._values.get("storage_engine")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DdsInstanceV3Datastore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DdsInstanceV3DatastoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3DatastoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fc56d9d55debdecc4fd8e2088b10038b81fffaf2fa89d1b366e73a6e43533ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStorageEngine")
    def reset_storage_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageEngine", []))

    @builtins.property
    @jsii.member(jsii_name="storageEngineInput")
    def storage_engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="storageEngine")
    def storage_engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageEngine"))

    @storage_engine.setter
    def storage_engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb9ff3e0a348c6244ba7ca7a3e0fc41c222a90ffc0dadc5658728ce07f810fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf0f5d604d68a9993c2cb13b12a34a0398a0b49783be4bd6f61e3a4345f2c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33277b6a403f371641eaba26037f320893f1922c208db6babf518cfec2fedc81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DdsInstanceV3Datastore]:
        return typing.cast(typing.Optional[DdsInstanceV3Datastore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DdsInstanceV3Datastore]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655d7b3a7026758e575d421bc7353ca13d5a50fef6943a7fad2a68b5bea27944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3Flavor",
    jsii_struct_bases=[],
    name_mapping={
        "num": "num",
        "spec_code": "specCode",
        "type": "type",
        "size": "size",
        "storage": "storage",
    },
)
class DdsInstanceV3Flavor:
    def __init__(
        self,
        *,
        num: jsii.Number,
        spec_code: builtins.str,
        type: builtins.str,
        size: typing.Optional[jsii.Number] = None,
        storage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#num DdsInstanceV3#num}.
        :param spec_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#spec_code DdsInstanceV3#spec_code}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#type DdsInstanceV3#type}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#size DdsInstanceV3#size}.
        :param storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#storage DdsInstanceV3#storage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e856a6704b25d053a5c0f0a1f1a9207d53f568acc7f396b9d48deb923ecd6cb)
            check_type(argname="argument num", value=num, expected_type=type_hints["num"])
            check_type(argname="argument spec_code", value=spec_code, expected_type=type_hints["spec_code"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "num": num,
            "spec_code": spec_code,
            "type": type,
        }
        if size is not None:
            self._values["size"] = size
        if storage is not None:
            self._values["storage"] = storage

    @builtins.property
    def num(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#num DdsInstanceV3#num}.'''
        result = self._values.get("num")
        assert result is not None, "Required property 'num' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def spec_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#spec_code DdsInstanceV3#spec_code}.'''
        result = self._values.get("spec_code")
        assert result is not None, "Required property 'spec_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#type DdsInstanceV3#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#size DdsInstanceV3#size}.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#storage DdsInstanceV3#storage}.'''
        result = self._values.get("storage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DdsInstanceV3Flavor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DdsInstanceV3FlavorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3FlavorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c73f275cec393fc5818b9f62647a8fab4aa57baf9590c2e620a52e9b254dba2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DdsInstanceV3FlavorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a2e61c8466f1daf760c142f8544dd3e8c5903551d0cd4c3e782aa23c952028)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DdsInstanceV3FlavorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ad96daaebab7b3d8505209f2e223144e995bf4700d7ed24087375d7d0b032d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5aad9c82968bcd4f74c16884285ebdcf636ee0981845915f2314cbe26b1358c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__444bab2014d2a39ced710ffcea76b1d7d64a227b5719794ab5c308a82ec69fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DdsInstanceV3Flavor]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DdsInstanceV3Flavor]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DdsInstanceV3Flavor]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcef48ee65777b0adc4b2fca11a51c1af17c2e4f1c35061fd4976cbf2702c77a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DdsInstanceV3FlavorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3FlavorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69eb0e849a06582f3eb2f72b3370468f2de22c46cb6b041196ea9f643b7522e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @builtins.property
    @jsii.member(jsii_name="numInput")
    def num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="specCodeInput")
    def spec_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "specCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="num")
    def num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "num"))

    @num.setter
    def num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0a11e1117210431c2bb41a46d93d51ad0d3b8f70619dd0a5711475cfa72734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "num", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40614db40e413703f00ca5dec4ba270e95e75679e52be03c484dcba0f3b6037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="specCode")
    def spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specCode"))

    @spec_code.setter
    def spec_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b8300f172c480f5d9877c37f5d4c122aef9c5302eb3f24d71b3f47d7a81c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storage"))

    @storage.setter
    def storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a92244cacf0f9bfcdd914f20f5f07d777a0b2306fd239887bfed7d6b777d207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2725bde6bbb43b9b8300990bf3f0c72c5da6c8cfc1e49c7751705d5bdd4e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DdsInstanceV3Flavor]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DdsInstanceV3Flavor]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DdsInstanceV3Flavor]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6772fdbff46a2bbffb46a0dd6f85641e296065e21bf72c8c2747b069b0de58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3Nodes",
    jsii_struct_bases=[],
    name_mapping={},
)
class DdsInstanceV3Nodes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DdsInstanceV3Nodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DdsInstanceV3NodesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3NodesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c827dab14cd9813c28df781b75822eed2cff4cb56ac7824bda2f63061fe27527)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DdsInstanceV3NodesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f28fdb6e710b86f77da760fc8b97ddfacc9fe6a7924bd93253f6b50e60519e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DdsInstanceV3NodesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41bc0a44e7d1bde10a823a1e9318a6714fda08a6f95b22c66beb0c3a67223717)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d818c902701977d9fbe6f26afafec991bf3f85cd7b725e2383dfd9eb9bf3acf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d05dfd6b359cff4d8dfe64329a5e0a61eea76cc964aa28350dc7577f6ce0d40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DdsInstanceV3NodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3NodesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__726d369d74683e0c42fc7b5bafd4c76d1ea492528239f76f9cae0dfb4d29b438)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DdsInstanceV3Nodes]:
        return typing.cast(typing.Optional[DdsInstanceV3Nodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DdsInstanceV3Nodes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c21acafc6cff0067fcd1efa0be9d268dba519f6fb293602acd92a6076e7bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DdsInstanceV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#create DdsInstanceV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#delete DdsInstanceV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#update DdsInstanceV3#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e72d9bb3ff9a0e80d75efc4ad459811ea31c91c2efa61611221b90708be8f8f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#create DdsInstanceV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#delete DdsInstanceV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dds_instance_v3#update DdsInstanceV3#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DdsInstanceV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DdsInstanceV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ddsInstanceV3.DdsInstanceV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a66be61e788c18a72578b2195f6261a03fb74fce0edc0d2e718fdb1a0409da0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91fad2565f18781a8a4740491412c7e1a56b17c07779ade1dc3c699d8cff2fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a9e09332a2b9dce73b54df0e1ac31b571da48b82f016a7abc3577060559e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9002838de68048fc8331ce14408371701fd6a6c8e5126ef5447adc3c5b9ac9ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DdsInstanceV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DdsInstanceV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DdsInstanceV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9d744d78a5c6b7f2150d15f953f0e1d56015fb593690313a44a6b816669135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DdsInstanceV3",
    "DdsInstanceV3BackupStrategy",
    "DdsInstanceV3BackupStrategyOutputReference",
    "DdsInstanceV3Config",
    "DdsInstanceV3Datastore",
    "DdsInstanceV3DatastoreOutputReference",
    "DdsInstanceV3Flavor",
    "DdsInstanceV3FlavorList",
    "DdsInstanceV3FlavorOutputReference",
    "DdsInstanceV3Nodes",
    "DdsInstanceV3NodesList",
    "DdsInstanceV3NodesOutputReference",
    "DdsInstanceV3Timeouts",
    "DdsInstanceV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6c14e5d67a802a9b10336125420ad02f11c81c6ac7d2886ed39d20a77c842ec8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: builtins.str,
    datastore: typing.Union[DdsInstanceV3Datastore, typing.Dict[builtins.str, typing.Any]],
    flavor: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DdsInstanceV3Flavor, typing.Dict[builtins.str, typing.Any]]]],
    mode: builtins.str,
    name: builtins.str,
    password: builtins.str,
    security_group_id: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    backup_strategy: typing.Optional[typing.Union[DdsInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DdsInstanceV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b5e5358c7cb80398d68088dc29afe5157189794a7db01a89303b4b0cd9e52ab8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f227db8d1538323e0e818f3491690546c59175bad16d8ccacde1668b154b1c1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DdsInstanceV3Flavor, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41f05f951c8b6bd903962fe0a1fbcffbe5034ade18c62cdf59f77c14a481d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3264bf9bf0b462cbe63aa85df3e2dcddea1567780309b8412f297dfd7fc88a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525f6a4b2ba29e2f2404bfd79a6b782edd183e874be637efd2e388891708f47a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ffb44e946dc5f1e489585cfabead9ae220c26924956baf4bdfe747c50fcf4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01b14978f8f11bc4cd07cffa9449cd6c200f96b8332eb31ddf1c8a355a1058c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d2eec64b60433d06e9b04b42fe4b0dd38915c07b21b870d89c7bb8931a9317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e35185a21542e2b6c4f3a96dac9960d5e154bfbf5e64238c5fa1673a6857a3a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7501ae673be5fcd5c3479c34b383bf8f526de50ab9c906bf69bad9fd2bde414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268eb8bd91f862803d5758a4d1fa60763e2a407c7305e50d49de58230951e53b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8204df635b780859d2b31cc4d971d50d529ec2cf43e3477c8c086cd7eb4567(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5b12af3f36637e9ca3b7dc51c3abb162a684a70a2b40b2e1814a4ee723eada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c892a5c54849fe53fe9eb36cf8de1ddb647691ec6e136ee56eb87ab1d0251943(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54c704eb0f3c3712b6ab98089b98ab1bedeaaa43eef86b91227c53f3fa06e33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6e93246ea8681ebedbebe93d7d7470312fd36163070e1197ca7f8d4c5f1659(
    *,
    keep_days: jsii.Number,
    start_time: builtins.str,
    period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd53f86a098a1b1f58071402c3231e965c3966e2bcd491ede5c677c02f6dbdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f983ff8680743a91926c575a80fed9b93df68d52c8451c31053a24116802e9d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8340ee496eac1df3291aac7bf194bb7d23fba4781f48e77a1df17143a5ce4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb39460c4df39b74b152eddaa39fd6eea28e93a339fe97f8c7d857ed017d99d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd14a2c74d7a1a887d4196a4f167c7f9ab81a16ee30e268f9e715590ce4de90(
    value: typing.Optional[DdsInstanceV3BackupStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6bd873e25e0971ef20465260431633a7f858a07b465f8fa2324c83d0e5b8a3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: builtins.str,
    datastore: typing.Union[DdsInstanceV3Datastore, typing.Dict[builtins.str, typing.Any]],
    flavor: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DdsInstanceV3Flavor, typing.Dict[builtins.str, typing.Any]]]],
    mode: builtins.str,
    name: builtins.str,
    password: builtins.str,
    security_group_id: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    backup_strategy: typing.Optional[typing.Union[DdsInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DdsInstanceV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e8c96f4b1036d194319e8e825437fa2089b471ae5f58ae2e7cfa98d1ac8b9a(
    *,
    type: builtins.str,
    version: builtins.str,
    storage_engine: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc56d9d55debdecc4fd8e2088b10038b81fffaf2fa89d1b366e73a6e43533ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb9ff3e0a348c6244ba7ca7a3e0fc41c222a90ffc0dadc5658728ce07f810fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf0f5d604d68a9993c2cb13b12a34a0398a0b49783be4bd6f61e3a4345f2c0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33277b6a403f371641eaba26037f320893f1922c208db6babf518cfec2fedc81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655d7b3a7026758e575d421bc7353ca13d5a50fef6943a7fad2a68b5bea27944(
    value: typing.Optional[DdsInstanceV3Datastore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e856a6704b25d053a5c0f0a1f1a9207d53f568acc7f396b9d48deb923ecd6cb(
    *,
    num: jsii.Number,
    spec_code: builtins.str,
    type: builtins.str,
    size: typing.Optional[jsii.Number] = None,
    storage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73f275cec393fc5818b9f62647a8fab4aa57baf9590c2e620a52e9b254dba2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a2e61c8466f1daf760c142f8544dd3e8c5903551d0cd4c3e782aa23c952028(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ad96daaebab7b3d8505209f2e223144e995bf4700d7ed24087375d7d0b032d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5aad9c82968bcd4f74c16884285ebdcf636ee0981845915f2314cbe26b1358c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444bab2014d2a39ced710ffcea76b1d7d64a227b5719794ab5c308a82ec69fad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcef48ee65777b0adc4b2fca11a51c1af17c2e4f1c35061fd4976cbf2702c77a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DdsInstanceV3Flavor]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69eb0e849a06582f3eb2f72b3370468f2de22c46cb6b041196ea9f643b7522e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0a11e1117210431c2bb41a46d93d51ad0d3b8f70619dd0a5711475cfa72734(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40614db40e413703f00ca5dec4ba270e95e75679e52be03c484dcba0f3b6037(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b8300f172c480f5d9877c37f5d4c122aef9c5302eb3f24d71b3f47d7a81c51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a92244cacf0f9bfcdd914f20f5f07d777a0b2306fd239887bfed7d6b777d207(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2725bde6bbb43b9b8300990bf3f0c72c5da6c8cfc1e49c7751705d5bdd4e04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6772fdbff46a2bbffb46a0dd6f85641e296065e21bf72c8c2747b069b0de58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DdsInstanceV3Flavor]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c827dab14cd9813c28df781b75822eed2cff4cb56ac7824bda2f63061fe27527(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f28fdb6e710b86f77da760fc8b97ddfacc9fe6a7924bd93253f6b50e60519e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41bc0a44e7d1bde10a823a1e9318a6714fda08a6f95b22c66beb0c3a67223717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d818c902701977d9fbe6f26afafec991bf3f85cd7b725e2383dfd9eb9bf3acf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d05dfd6b359cff4d8dfe64329a5e0a61eea76cc964aa28350dc7577f6ce0d40(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726d369d74683e0c42fc7b5bafd4c76d1ea492528239f76f9cae0dfb4d29b438(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c21acafc6cff0067fcd1efa0be9d268dba519f6fb293602acd92a6076e7bb0(
    value: typing.Optional[DdsInstanceV3Nodes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e72d9bb3ff9a0e80d75efc4ad459811ea31c91c2efa61611221b90708be8f8f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a66be61e788c18a72578b2195f6261a03fb74fce0edc0d2e718fdb1a0409da0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fad2565f18781a8a4740491412c7e1a56b17c07779ade1dc3c699d8cff2fe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a9e09332a2b9dce73b54df0e1ac31b571da48b82f016a7abc3577060559e3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9002838de68048fc8331ce14408371701fd6a6c8e5126ef5447adc3c5b9ac9ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9d744d78a5c6b7f2150d15f953f0e1d56015fb593690313a44a6b816669135(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DdsInstanceV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
