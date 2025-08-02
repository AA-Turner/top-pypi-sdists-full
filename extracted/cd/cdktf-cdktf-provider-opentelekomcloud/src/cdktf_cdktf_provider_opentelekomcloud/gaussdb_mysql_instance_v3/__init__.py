r'''
# `opentelekomcloud_gaussdb_mysql_instance_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_gaussdb_mysql_instance_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3).
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


class GaussdbMysqlInstanceV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3 opentelekomcloud_gaussdb_mysql_instance_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        flavor: builtins.str,
        name: builtins.str,
        password: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        availability_zone_mode: typing.Optional[builtins.str] = None,
        backup_strategy: typing.Optional[typing.Union["GaussdbMysqlInstanceV3BackupStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        configuration_id: typing.Optional[builtins.str] = None,
        configuration_name: typing.Optional[builtins.str] = None,
        datastore: typing.Optional[typing.Union["GaussdbMysqlInstanceV3Datastore", typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_resource_id: typing.Optional[builtins.str] = None,
        dedicated_resource_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        master_availability_zone: typing.Optional[builtins.str] = None,
        read_replicas: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GaussdbMysqlInstanceV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3 opentelekomcloud_gaussdb_mysql_instance_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#flavor GaussdbMysqlInstanceV3#flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#name GaussdbMysqlInstanceV3#name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#password GaussdbMysqlInstanceV3#password}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#subnet_id GaussdbMysqlInstanceV3#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#vpc_id GaussdbMysqlInstanceV3#vpc_id}.
        :param availability_zone_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#availability_zone_mode GaussdbMysqlInstanceV3#availability_zone_mode}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#backup_strategy GaussdbMysqlInstanceV3#backup_strategy}
        :param configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#configuration_id GaussdbMysqlInstanceV3#configuration_id}.
        :param configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#configuration_name GaussdbMysqlInstanceV3#configuration_name}.
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#datastore GaussdbMysqlInstanceV3#datastore}
        :param dedicated_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#dedicated_resource_id GaussdbMysqlInstanceV3#dedicated_resource_id}.
        :param dedicated_resource_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#dedicated_resource_name GaussdbMysqlInstanceV3#dedicated_resource_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#id GaussdbMysqlInstanceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master_availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#master_availability_zone GaussdbMysqlInstanceV3#master_availability_zone}.
        :param read_replicas: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#read_replicas GaussdbMysqlInstanceV3#read_replicas}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#region GaussdbMysqlInstanceV3#region}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#security_group_id GaussdbMysqlInstanceV3#security_group_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#timeouts GaussdbMysqlInstanceV3#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#time_zone GaussdbMysqlInstanceV3#time_zone}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306d8caaecf5727b47e08e996069241bbd4ba440e326dda802ef162f51aa28f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GaussdbMysqlInstanceV3Config(
            flavor=flavor,
            name=name,
            password=password,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            availability_zone_mode=availability_zone_mode,
            backup_strategy=backup_strategy,
            configuration_id=configuration_id,
            configuration_name=configuration_name,
            datastore=datastore,
            dedicated_resource_id=dedicated_resource_id,
            dedicated_resource_name=dedicated_resource_name,
            id=id,
            master_availability_zone=master_availability_zone,
            read_replicas=read_replicas,
            region=region,
            security_group_id=security_group_id,
            timeouts=timeouts,
            time_zone=time_zone,
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
        '''Generates CDKTF code for importing a GaussdbMysqlInstanceV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GaussdbMysqlInstanceV3 to import.
        :param import_from_id: The id of the existing GaussdbMysqlInstanceV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GaussdbMysqlInstanceV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc8d3afdd6357ce03c8607f706947a577d5c99fdbef306ab33e43a5a8ab88fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupStrategy")
    def put_backup_strategy(
        self,
        *,
        start_time: builtins.str,
        keep_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#start_time GaussdbMysqlInstanceV3#start_time}.
        :param keep_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#keep_days GaussdbMysqlInstanceV3#keep_days}.
        '''
        value = GaussdbMysqlInstanceV3BackupStrategy(
            start_time=start_time, keep_days=keep_days
        )

        return typing.cast(None, jsii.invoke(self, "putBackupStrategy", [value]))

    @jsii.member(jsii_name="putDatastore")
    def put_datastore(self, *, engine: builtins.str, version: builtins.str) -> None:
        '''
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#engine GaussdbMysqlInstanceV3#engine}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#version GaussdbMysqlInstanceV3#version}.
        '''
        value = GaussdbMysqlInstanceV3Datastore(engine=engine, version=version)

        return typing.cast(None, jsii.invoke(self, "putDatastore", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#create GaussdbMysqlInstanceV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#delete GaussdbMysqlInstanceV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#update GaussdbMysqlInstanceV3#update}.
        '''
        value = GaussdbMysqlInstanceV3Timeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAvailabilityZoneMode")
    def reset_availability_zone_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZoneMode", []))

    @jsii.member(jsii_name="resetBackupStrategy")
    def reset_backup_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupStrategy", []))

    @jsii.member(jsii_name="resetConfigurationId")
    def reset_configuration_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigurationId", []))

    @jsii.member(jsii_name="resetConfigurationName")
    def reset_configuration_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigurationName", []))

    @jsii.member(jsii_name="resetDatastore")
    def reset_datastore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatastore", []))

    @jsii.member(jsii_name="resetDedicatedResourceId")
    def reset_dedicated_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedResourceId", []))

    @jsii.member(jsii_name="resetDedicatedResourceName")
    def reset_dedicated_resource_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedResourceName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMasterAvailabilityZone")
    def reset_master_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterAvailabilityZone", []))

    @jsii.member(jsii_name="resetReadReplicas")
    def reset_read_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadReplicas", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityGroupId")
    def reset_security_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

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
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @builtins.property
    @jsii.member(jsii_name="backupStrategy")
    def backup_strategy(self) -> "GaussdbMysqlInstanceV3BackupStrategyOutputReference":
        return typing.cast("GaussdbMysqlInstanceV3BackupStrategyOutputReference", jsii.get(self, "backupStrategy"))

    @builtins.property
    @jsii.member(jsii_name="chargingMode")
    def charging_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargingMode"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> "GaussdbMysqlInstanceV3DatastoreOutputReference":
        return typing.cast("GaussdbMysqlInstanceV3DatastoreOutputReference", jsii.get(self, "datastore"))

    @builtins.property
    @jsii.member(jsii_name="dbUserName")
    def db_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbUserName"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> "GaussdbMysqlInstanceV3NodesList":
        return typing.cast("GaussdbMysqlInstanceV3NodesList", jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="privateWriteIp")
    def private_write_ip(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateWriteIp"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GaussdbMysqlInstanceV3TimeoutsOutputReference":
        return typing.cast("GaussdbMysqlInstanceV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneModeInput")
    def availability_zone_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneModeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupStrategyInput")
    def backup_strategy_input(
        self,
    ) -> typing.Optional["GaussdbMysqlInstanceV3BackupStrategy"]:
        return typing.cast(typing.Optional["GaussdbMysqlInstanceV3BackupStrategy"], jsii.get(self, "backupStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationIdInput")
    def configuration_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationNameInput")
    def configuration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreInput")
    def datastore_input(self) -> typing.Optional["GaussdbMysqlInstanceV3Datastore"]:
        return typing.cast(typing.Optional["GaussdbMysqlInstanceV3Datastore"], jsii.get(self, "datastoreInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourceIdInput")
    def dedicated_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dedicatedResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourceNameInput")
    def dedicated_resource_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dedicatedResourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="masterAvailabilityZoneInput")
    def master_availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterAvailabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="readReplicasInput")
    def read_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GaussdbMysqlInstanceV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GaussdbMysqlInstanceV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneMode")
    def availability_zone_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneMode"))

    @availability_zone_mode.setter
    def availability_zone_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15349fda1b8e2ddf7bc92eb091fac150d75890f0a11b5a8ef9b7d24e0569b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZoneMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configurationId")
    def configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationId"))

    @configuration_id.setter
    def configuration_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be455a9f54e4f79d0bd85fcd8b0fa654459a0b73dc55dc4ef181e1a9e1ed2dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configurationName")
    def configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configurationName"))

    @configuration_name.setter
    def configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2021552a8e642f3c1996b7f5fb697ce0040cacf2a7d55b454af44fa8f975c719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourceId")
    def dedicated_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicatedResourceId"))

    @dedicated_resource_id.setter
    def dedicated_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3bc8b43def550001bd7b181e22d41ad067005b4ef27358e1fd931b8df60ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourceName")
    def dedicated_resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicatedResourceName"))

    @dedicated_resource_name.setter
    def dedicated_resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a040d9d04a69c9bd09cf624590ce825568baf590686291a192433b2b4f22af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedResourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b6a007ab20072e8237d7184180fd46cd3b1c845fb0d67f9aa96a3e8efe6fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20d0001123fd6a61f41668bb854f5ed95359967301b1b3f0921edbeddb554fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterAvailabilityZone")
    def master_availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterAvailabilityZone"))

    @master_availability_zone.setter
    def master_availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6572d949f33ae376f2dcd4e19978db389b17ba4b32ab13a11a3e6e698ba81d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterAvailabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63751d3831f79897225fd59b7499d17da461a1ef90815f3b4173f58e739fd2ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f105469293000134e5604e293af11837b076fbd58f8da99620c0a2433a666cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readReplicas")
    def read_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "readReplicas"))

    @read_replicas.setter
    def read_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bf98d061cec7ccab18f195b93c5117047183b33e9e624be9bc4e19c2af34d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb163800df0d62d0a80afb521350671164973a36734f0abf367fce3568e5064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f3b175f747599e5d63a94e9c21e8a111d51751b7e2dda7b40400f0e9d6a95c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddcdbbe1a410f5b99b429946cc7c1b940a20bb352946feffa373fc3acf19d9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee5b52ec1095c60a31695f26caf0485bd6435cf979c63697ab5cde740e8fd56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca685e356e517048de03dde5c4d0d26ea71bb9a6eadf530038551ab4b3de9b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3BackupStrategy",
    jsii_struct_bases=[],
    name_mapping={"start_time": "startTime", "keep_days": "keepDays"},
)
class GaussdbMysqlInstanceV3BackupStrategy:
    def __init__(
        self,
        *,
        start_time: builtins.str,
        keep_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#start_time GaussdbMysqlInstanceV3#start_time}.
        :param keep_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#keep_days GaussdbMysqlInstanceV3#keep_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d3a973b6cdfd4bf442aa75b9da42e18194c7484e17b9c79af1b5721186f728)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument keep_days", value=keep_days, expected_type=type_hints["keep_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_time": start_time,
        }
        if keep_days is not None:
            self._values["keep_days"] = keep_days

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#start_time GaussdbMysqlInstanceV3#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keep_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#keep_days GaussdbMysqlInstanceV3#keep_days}.'''
        result = self._values.get("keep_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GaussdbMysqlInstanceV3BackupStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GaussdbMysqlInstanceV3BackupStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3BackupStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__661d215e3e33642eed5f221c8489630e73258977a3fdcb1610b8b73bec154e14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeepDays")
    def reset_keep_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepDays", []))

    @builtins.property
    @jsii.member(jsii_name="keepDaysInput")
    def keep_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepDaysInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ee68c7abc5838213c0e32abedfbb453d74db6914b53acaa2504af55be4af30b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86397cd0202e5c1910355b5437fc1ca6728e274b1cb2019014dad83707898b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GaussdbMysqlInstanceV3BackupStrategy]:
        return typing.cast(typing.Optional[GaussdbMysqlInstanceV3BackupStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GaussdbMysqlInstanceV3BackupStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225384815152850ce667b72fa8807aec9c8e554be80cd15a097a7d52333a560e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "flavor": "flavor",
        "name": "name",
        "password": "password",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "availability_zone_mode": "availabilityZoneMode",
        "backup_strategy": "backupStrategy",
        "configuration_id": "configurationId",
        "configuration_name": "configurationName",
        "datastore": "datastore",
        "dedicated_resource_id": "dedicatedResourceId",
        "dedicated_resource_name": "dedicatedResourceName",
        "id": "id",
        "master_availability_zone": "masterAvailabilityZone",
        "read_replicas": "readReplicas",
        "region": "region",
        "security_group_id": "securityGroupId",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
    },
)
class GaussdbMysqlInstanceV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        flavor: builtins.str,
        name: builtins.str,
        password: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        availability_zone_mode: typing.Optional[builtins.str] = None,
        backup_strategy: typing.Optional[typing.Union[GaussdbMysqlInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
        configuration_id: typing.Optional[builtins.str] = None,
        configuration_name: typing.Optional[builtins.str] = None,
        datastore: typing.Optional[typing.Union["GaussdbMysqlInstanceV3Datastore", typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_resource_id: typing.Optional[builtins.str] = None,
        dedicated_resource_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        master_availability_zone: typing.Optional[builtins.str] = None,
        read_replicas: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GaussdbMysqlInstanceV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#flavor GaussdbMysqlInstanceV3#flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#name GaussdbMysqlInstanceV3#name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#password GaussdbMysqlInstanceV3#password}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#subnet_id GaussdbMysqlInstanceV3#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#vpc_id GaussdbMysqlInstanceV3#vpc_id}.
        :param availability_zone_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#availability_zone_mode GaussdbMysqlInstanceV3#availability_zone_mode}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#backup_strategy GaussdbMysqlInstanceV3#backup_strategy}
        :param configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#configuration_id GaussdbMysqlInstanceV3#configuration_id}.
        :param configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#configuration_name GaussdbMysqlInstanceV3#configuration_name}.
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#datastore GaussdbMysqlInstanceV3#datastore}
        :param dedicated_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#dedicated_resource_id GaussdbMysqlInstanceV3#dedicated_resource_id}.
        :param dedicated_resource_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#dedicated_resource_name GaussdbMysqlInstanceV3#dedicated_resource_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#id GaussdbMysqlInstanceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param master_availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#master_availability_zone GaussdbMysqlInstanceV3#master_availability_zone}.
        :param read_replicas: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#read_replicas GaussdbMysqlInstanceV3#read_replicas}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#region GaussdbMysqlInstanceV3#region}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#security_group_id GaussdbMysqlInstanceV3#security_group_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#timeouts GaussdbMysqlInstanceV3#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#time_zone GaussdbMysqlInstanceV3#time_zone}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup_strategy, dict):
            backup_strategy = GaussdbMysqlInstanceV3BackupStrategy(**backup_strategy)
        if isinstance(datastore, dict):
            datastore = GaussdbMysqlInstanceV3Datastore(**datastore)
        if isinstance(timeouts, dict):
            timeouts = GaussdbMysqlInstanceV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b151c9525ad18e5dd2e76e470328c762192faf57cb7e9cc835dcf0b705a40c08)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument availability_zone_mode", value=availability_zone_mode, expected_type=type_hints["availability_zone_mode"])
            check_type(argname="argument backup_strategy", value=backup_strategy, expected_type=type_hints["backup_strategy"])
            check_type(argname="argument configuration_id", value=configuration_id, expected_type=type_hints["configuration_id"])
            check_type(argname="argument configuration_name", value=configuration_name, expected_type=type_hints["configuration_name"])
            check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
            check_type(argname="argument dedicated_resource_id", value=dedicated_resource_id, expected_type=type_hints["dedicated_resource_id"])
            check_type(argname="argument dedicated_resource_name", value=dedicated_resource_name, expected_type=type_hints["dedicated_resource_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument master_availability_zone", value=master_availability_zone, expected_type=type_hints["master_availability_zone"])
            check_type(argname="argument read_replicas", value=read_replicas, expected_type=type_hints["read_replicas"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "flavor": flavor,
            "name": name,
            "password": password,
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
        if availability_zone_mode is not None:
            self._values["availability_zone_mode"] = availability_zone_mode
        if backup_strategy is not None:
            self._values["backup_strategy"] = backup_strategy
        if configuration_id is not None:
            self._values["configuration_id"] = configuration_id
        if configuration_name is not None:
            self._values["configuration_name"] = configuration_name
        if datastore is not None:
            self._values["datastore"] = datastore
        if dedicated_resource_id is not None:
            self._values["dedicated_resource_id"] = dedicated_resource_id
        if dedicated_resource_name is not None:
            self._values["dedicated_resource_name"] = dedicated_resource_name
        if id is not None:
            self._values["id"] = id
        if master_availability_zone is not None:
            self._values["master_availability_zone"] = master_availability_zone
        if read_replicas is not None:
            self._values["read_replicas"] = read_replicas
        if region is not None:
            self._values["region"] = region
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if time_zone is not None:
            self._values["time_zone"] = time_zone

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
    def flavor(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#flavor GaussdbMysqlInstanceV3#flavor}.'''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#name GaussdbMysqlInstanceV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#password GaussdbMysqlInstanceV3#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#subnet_id GaussdbMysqlInstanceV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#vpc_id GaussdbMysqlInstanceV3#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_zone_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#availability_zone_mode GaussdbMysqlInstanceV3#availability_zone_mode}.'''
        result = self._values.get("availability_zone_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_strategy(self) -> typing.Optional[GaussdbMysqlInstanceV3BackupStrategy]:
        '''backup_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#backup_strategy GaussdbMysqlInstanceV3#backup_strategy}
        '''
        result = self._values.get("backup_strategy")
        return typing.cast(typing.Optional[GaussdbMysqlInstanceV3BackupStrategy], result)

    @builtins.property
    def configuration_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#configuration_id GaussdbMysqlInstanceV3#configuration_id}.'''
        result = self._values.get("configuration_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#configuration_name GaussdbMysqlInstanceV3#configuration_name}.'''
        result = self._values.get("configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datastore(self) -> typing.Optional["GaussdbMysqlInstanceV3Datastore"]:
        '''datastore block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#datastore GaussdbMysqlInstanceV3#datastore}
        '''
        result = self._values.get("datastore")
        return typing.cast(typing.Optional["GaussdbMysqlInstanceV3Datastore"], result)

    @builtins.property
    def dedicated_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#dedicated_resource_id GaussdbMysqlInstanceV3#dedicated_resource_id}.'''
        result = self._values.get("dedicated_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dedicated_resource_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#dedicated_resource_name GaussdbMysqlInstanceV3#dedicated_resource_name}.'''
        result = self._values.get("dedicated_resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#id GaussdbMysqlInstanceV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#master_availability_zone GaussdbMysqlInstanceV3#master_availability_zone}.'''
        result = self._values.get("master_availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_replicas(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#read_replicas GaussdbMysqlInstanceV3#read_replicas}.'''
        result = self._values.get("read_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#region GaussdbMysqlInstanceV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#security_group_id GaussdbMysqlInstanceV3#security_group_id}.'''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GaussdbMysqlInstanceV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#timeouts GaussdbMysqlInstanceV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GaussdbMysqlInstanceV3Timeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#time_zone GaussdbMysqlInstanceV3#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GaussdbMysqlInstanceV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3Datastore",
    jsii_struct_bases=[],
    name_mapping={"engine": "engine", "version": "version"},
)
class GaussdbMysqlInstanceV3Datastore:
    def __init__(self, *, engine: builtins.str, version: builtins.str) -> None:
        '''
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#engine GaussdbMysqlInstanceV3#engine}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#version GaussdbMysqlInstanceV3#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da542f2444f46133eaff1e171136040cf758298e30c847ff97e9aa83134502f)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
            "version": version,
        }

    @builtins.property
    def engine(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#engine GaussdbMysqlInstanceV3#engine}.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#version GaussdbMysqlInstanceV3#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GaussdbMysqlInstanceV3Datastore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GaussdbMysqlInstanceV3DatastoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3DatastoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b7e15219cfbd1978e522ca334cb9b40a36ab5988d3ad5dd0509bddd78dcfe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="engineInput")
    def engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f236cc39755554dbdeab72cc7a30b01cb7ca1fe59aa0bb9a332c1033d403707a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b19b849de7cb4c5984b30b37372d8b38386e04d43074b28627f9aa9c53bbce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GaussdbMysqlInstanceV3Datastore]:
        return typing.cast(typing.Optional[GaussdbMysqlInstanceV3Datastore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GaussdbMysqlInstanceV3Datastore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b408b8e25cbcb1ced1857d480d8ef0ebb9ec9843a6f1843cdc00cbc19ee2418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3Nodes",
    jsii_struct_bases=[],
    name_mapping={},
)
class GaussdbMysqlInstanceV3Nodes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GaussdbMysqlInstanceV3Nodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GaussdbMysqlInstanceV3NodesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3NodesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99088de6ede1b9c0256cae24f94444e4a9df36e5669e7fd182f8889b12f47867)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GaussdbMysqlInstanceV3NodesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fd91065d3e0de8bf45533fcf34e86f045ffeb2165add3a9600e9168dd16d76)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GaussdbMysqlInstanceV3NodesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af284df70639f0110f4d1ec87d012f2708010b9c3fdcacd8e9a9bcf496b2cfa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fca02662488f386dbdae1efc36f6d296b17cf9544370ace3da5e50a082fbe31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a0437d2c69c989d185a7235f907d5c621b3dfb268db5cc9d12a410cdd690da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GaussdbMysqlInstanceV3NodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3NodesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a280afe6c03fff9231658c88991da4832bedc21ac0726bf4775deae4cdfb7f3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="azCode")
    def az_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azCode"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="flavorRef")
    def flavor_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorRef"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="maxConnections")
    def max_connections(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxConnections"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="needRestart")
    def need_restart(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "needRestart"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="privateReadIps")
    def private_read_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateReadIps"))

    @builtins.property
    @jsii.member(jsii_name="ram")
    def ram(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ram"))

    @builtins.property
    @jsii.member(jsii_name="regionCode")
    def region_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionCode"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="vcpus")
    def vcpus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcpus"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GaussdbMysqlInstanceV3Nodes]:
        return typing.cast(typing.Optional[GaussdbMysqlInstanceV3Nodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GaussdbMysqlInstanceV3Nodes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2851b939e86000e6c1ef1deef73110ad8cc0be3d26e39d082e8d02992295854b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GaussdbMysqlInstanceV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#create GaussdbMysqlInstanceV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#delete GaussdbMysqlInstanceV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#update GaussdbMysqlInstanceV3#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c033e996e8df1abce1911909ab547f56b2664e2e41ca619a45520a453d7b58cc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#create GaussdbMysqlInstanceV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#delete GaussdbMysqlInstanceV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/gaussdb_mysql_instance_v3#update GaussdbMysqlInstanceV3#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GaussdbMysqlInstanceV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GaussdbMysqlInstanceV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.gaussdbMysqlInstanceV3.GaussdbMysqlInstanceV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f64ee7ab89d8591849b32ee97b67dbab2e1e77e538e7b4b4be48c2f726e11e0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e771db3a35909dfb09025a583420fe0379b3c3428b76372981f7fce22a7bf7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6e2788d73e60f50211dab6dd010a568f4539c081f35415b2588f8848db9738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7f314e490a7832a917e7d6f8ca286f407f45b0a7d5fdf33739465e183719e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GaussdbMysqlInstanceV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GaussdbMysqlInstanceV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GaussdbMysqlInstanceV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c20021494efbc1a677ff60dd105b01915802b4885f3faa28df165ea66c27a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GaussdbMysqlInstanceV3",
    "GaussdbMysqlInstanceV3BackupStrategy",
    "GaussdbMysqlInstanceV3BackupStrategyOutputReference",
    "GaussdbMysqlInstanceV3Config",
    "GaussdbMysqlInstanceV3Datastore",
    "GaussdbMysqlInstanceV3DatastoreOutputReference",
    "GaussdbMysqlInstanceV3Nodes",
    "GaussdbMysqlInstanceV3NodesList",
    "GaussdbMysqlInstanceV3NodesOutputReference",
    "GaussdbMysqlInstanceV3Timeouts",
    "GaussdbMysqlInstanceV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__306d8caaecf5727b47e08e996069241bbd4ba440e326dda802ef162f51aa28f4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    flavor: builtins.str,
    name: builtins.str,
    password: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    availability_zone_mode: typing.Optional[builtins.str] = None,
    backup_strategy: typing.Optional[typing.Union[GaussdbMysqlInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    configuration_id: typing.Optional[builtins.str] = None,
    configuration_name: typing.Optional[builtins.str] = None,
    datastore: typing.Optional[typing.Union[GaussdbMysqlInstanceV3Datastore, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_resource_id: typing.Optional[builtins.str] = None,
    dedicated_resource_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    master_availability_zone: typing.Optional[builtins.str] = None,
    read_replicas: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GaussdbMysqlInstanceV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__abc8d3afdd6357ce03c8607f706947a577d5c99fdbef306ab33e43a5a8ab88fe(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15349fda1b8e2ddf7bc92eb091fac150d75890f0a11b5a8ef9b7d24e0569b06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be455a9f54e4f79d0bd85fcd8b0fa654459a0b73dc55dc4ef181e1a9e1ed2dfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2021552a8e642f3c1996b7f5fb697ce0040cacf2a7d55b454af44fa8f975c719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3bc8b43def550001bd7b181e22d41ad067005b4ef27358e1fd931b8df60ee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a040d9d04a69c9bd09cf624590ce825568baf590686291a192433b2b4f22af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b6a007ab20072e8237d7184180fd46cd3b1c845fb0d67f9aa96a3e8efe6fbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20d0001123fd6a61f41668bb854f5ed95359967301b1b3f0921edbeddb554fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6572d949f33ae376f2dcd4e19978db389b17ba4b32ab13a11a3e6e698ba81d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63751d3831f79897225fd59b7499d17da461a1ef90815f3b4173f58e739fd2ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f105469293000134e5604e293af11837b076fbd58f8da99620c0a2433a666cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bf98d061cec7ccab18f195b93c5117047183b33e9e624be9bc4e19c2af34d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb163800df0d62d0a80afb521350671164973a36734f0abf367fce3568e5064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f3b175f747599e5d63a94e9c21e8a111d51751b7e2dda7b40400f0e9d6a95c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcdbbe1a410f5b99b429946cc7c1b940a20bb352946feffa373fc3acf19d9e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee5b52ec1095c60a31695f26caf0485bd6435cf979c63697ab5cde740e8fd56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca685e356e517048de03dde5c4d0d26ea71bb9a6eadf530038551ab4b3de9b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d3a973b6cdfd4bf442aa75b9da42e18194c7484e17b9c79af1b5721186f728(
    *,
    start_time: builtins.str,
    keep_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661d215e3e33642eed5f221c8489630e73258977a3fdcb1610b8b73bec154e14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee68c7abc5838213c0e32abedfbb453d74db6914b53acaa2504af55be4af30b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86397cd0202e5c1910355b5437fc1ca6728e274b1cb2019014dad83707898b52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225384815152850ce667b72fa8807aec9c8e554be80cd15a097a7d52333a560e(
    value: typing.Optional[GaussdbMysqlInstanceV3BackupStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b151c9525ad18e5dd2e76e470328c762192faf57cb7e9cc835dcf0b705a40c08(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    flavor: builtins.str,
    name: builtins.str,
    password: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    availability_zone_mode: typing.Optional[builtins.str] = None,
    backup_strategy: typing.Optional[typing.Union[GaussdbMysqlInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    configuration_id: typing.Optional[builtins.str] = None,
    configuration_name: typing.Optional[builtins.str] = None,
    datastore: typing.Optional[typing.Union[GaussdbMysqlInstanceV3Datastore, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_resource_id: typing.Optional[builtins.str] = None,
    dedicated_resource_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    master_availability_zone: typing.Optional[builtins.str] = None,
    read_replicas: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GaussdbMysqlInstanceV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da542f2444f46133eaff1e171136040cf758298e30c847ff97e9aa83134502f(
    *,
    engine: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b7e15219cfbd1978e522ca334cb9b40a36ab5988d3ad5dd0509bddd78dcfe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f236cc39755554dbdeab72cc7a30b01cb7ca1fe59aa0bb9a332c1033d403707a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b19b849de7cb4c5984b30b37372d8b38386e04d43074b28627f9aa9c53bbce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b408b8e25cbcb1ced1857d480d8ef0ebb9ec9843a6f1843cdc00cbc19ee2418(
    value: typing.Optional[GaussdbMysqlInstanceV3Datastore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99088de6ede1b9c0256cae24f94444e4a9df36e5669e7fd182f8889b12f47867(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fd91065d3e0de8bf45533fcf34e86f045ffeb2165add3a9600e9168dd16d76(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af284df70639f0110f4d1ec87d012f2708010b9c3fdcacd8e9a9bcf496b2cfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fca02662488f386dbdae1efc36f6d296b17cf9544370ace3da5e50a082fbe31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0437d2c69c989d185a7235f907d5c621b3dfb268db5cc9d12a410cdd690da1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a280afe6c03fff9231658c88991da4832bedc21ac0726bf4775deae4cdfb7f3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2851b939e86000e6c1ef1deef73110ad8cc0be3d26e39d082e8d02992295854b(
    value: typing.Optional[GaussdbMysqlInstanceV3Nodes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c033e996e8df1abce1911909ab547f56b2664e2e41ca619a45520a453d7b58cc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64ee7ab89d8591849b32ee97b67dbab2e1e77e538e7b4b4be48c2f726e11e0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e771db3a35909dfb09025a583420fe0379b3c3428b76372981f7fce22a7bf7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6e2788d73e60f50211dab6dd010a568f4539c081f35415b2588f8848db9738(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7f314e490a7832a917e7d6f8ca286f407f45b0a7d5fdf33739465e183719e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c20021494efbc1a677ff60dd105b01915802b4885f3faa28df165ea66c27a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GaussdbMysqlInstanceV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
