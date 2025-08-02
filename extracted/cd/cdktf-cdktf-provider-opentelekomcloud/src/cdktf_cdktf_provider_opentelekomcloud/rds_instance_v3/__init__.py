r'''
# `opentelekomcloud_rds_instance_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_rds_instance_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3).
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


class RdsInstanceV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3 opentelekomcloud_rds_instance_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: typing.Sequence[builtins.str],
        db: typing.Union["RdsInstanceV3Db", typing.Dict[builtins.str, typing.Any]],
        flavor: builtins.str,
        name: builtins.str,
        security_group_id: builtins.str,
        subnet_id: builtins.str,
        volume: typing.Union["RdsInstanceV3Volume", typing.Dict[builtins.str, typing.Any]],
        vpc_id: builtins.str,
        backup_strategy: typing.Optional[typing.Union["RdsInstanceV3BackupStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        ha_replication_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lower_case_table_names: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        param_group_id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        restore_from_backup: typing.Optional[typing.Union["RdsInstanceV3RestoreFromBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_point: typing.Optional[typing.Union["RdsInstanceV3RestorePoint", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RdsInstanceV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3 opentelekomcloud_rds_instance_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#availability_zone RdsInstanceV3#availability_zone}.
        :param db: db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#db RdsInstanceV3#db}
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#flavor RdsInstanceV3#flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#name RdsInstanceV3#name}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#security_group_id RdsInstanceV3#security_group_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#subnet_id RdsInstanceV3#subnet_id}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#volume RdsInstanceV3#volume}
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#vpc_id RdsInstanceV3#vpc_id}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_strategy RdsInstanceV3#backup_strategy}
        :param ha_replication_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#ha_replication_mode RdsInstanceV3#ha_replication_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#id RdsInstanceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lower_case_table_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#lower_case_table_names RdsInstanceV3#lower_case_table_names}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#parameters RdsInstanceV3#parameters}.
        :param param_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#param_group_id RdsInstanceV3#param_group_id}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#private_ip RdsInstanceV3#private_ip}.
        :param public_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#public_ips RdsInstanceV3#public_ips}.
        :param restore_from_backup: restore_from_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_from_backup RdsInstanceV3#restore_from_backup}
        :param restore_point: restore_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_point RdsInstanceV3#restore_point}
        :param ssl_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#ssl_enable RdsInstanceV3#ssl_enable}.
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#tag RdsInstanceV3#tag}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#tags RdsInstanceV3#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#timeouts RdsInstanceV3#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d11077d95f43a5d8efbd86796e6035458973a1817e04c6b2605533066c503e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RdsInstanceV3Config(
            availability_zone=availability_zone,
            db=db,
            flavor=flavor,
            name=name,
            security_group_id=security_group_id,
            subnet_id=subnet_id,
            volume=volume,
            vpc_id=vpc_id,
            backup_strategy=backup_strategy,
            ha_replication_mode=ha_replication_mode,
            id=id,
            lower_case_table_names=lower_case_table_names,
            parameters=parameters,
            param_group_id=param_group_id,
            private_ip=private_ip,
            public_ips=public_ips,
            restore_from_backup=restore_from_backup,
            restore_point=restore_point,
            ssl_enable=ssl_enable,
            tag=tag,
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
        '''Generates CDKTF code for importing a RdsInstanceV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RdsInstanceV3 to import.
        :param import_from_id: The id of the existing RdsInstanceV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RdsInstanceV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45defa5a684950ddba7cd59e1e05da42cfe64a982fb8f872f9556d45d4d09b28)
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
        period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#start_time RdsInstanceV3#start_time}.
        :param keep_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#keep_days RdsInstanceV3#keep_days}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#period RdsInstanceV3#period}.
        '''
        value = RdsInstanceV3BackupStrategy(
            start_time=start_time, keep_days=keep_days, period=period
        )

        return typing.cast(None, jsii.invoke(self, "putBackupStrategy", [value]))

    @jsii.member(jsii_name="putDb")
    def put_db(
        self,
        *,
        password: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#password RdsInstanceV3#password}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#port RdsInstanceV3#port}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#version RdsInstanceV3#version}.
        '''
        value = RdsInstanceV3Db(
            password=password, port=port, type=type, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putDb", [value]))

    @jsii.member(jsii_name="putRestoreFromBackup")
    def put_restore_from_backup(
        self,
        *,
        source_instance_id: builtins.str,
        type: builtins.str,
        backup_id: typing.Optional[builtins.str] = None,
        restore_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#source_instance_id RdsInstanceV3#source_instance_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.
        :param backup_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.
        :param restore_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.
        '''
        value = RdsInstanceV3RestoreFromBackup(
            source_instance_id=source_instance_id,
            type=type,
            backup_id=backup_id,
            restore_time=restore_time,
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreFromBackup", [value]))

    @jsii.member(jsii_name="putRestorePoint")
    def put_restore_point(
        self,
        *,
        instance_id: builtins.str,
        backup_id: typing.Optional[builtins.str] = None,
        restore_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#instance_id RdsInstanceV3#instance_id}.
        :param backup_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.
        :param restore_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.
        '''
        value = RdsInstanceV3RestorePoint(
            instance_id=instance_id, backup_id=backup_id, restore_time=restore_time
        )

        return typing.cast(None, jsii.invoke(self, "putRestorePoint", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#create RdsInstanceV3#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#update RdsInstanceV3#update}.
        '''
        value = RdsInstanceV3Timeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(
        self,
        *,
        size: jsii.Number,
        type: builtins.str,
        disk_encryption_id: typing.Optional[builtins.str] = None,
        limit_size: typing.Optional[jsii.Number] = None,
        trigger_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#size RdsInstanceV3#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.
        :param disk_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#disk_encryption_id RdsInstanceV3#disk_encryption_id}.
        :param limit_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#limit_size RdsInstanceV3#limit_size}.
        :param trigger_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#trigger_threshold RdsInstanceV3#trigger_threshold}.
        '''
        value = RdsInstanceV3Volume(
            size=size,
            type=type,
            disk_encryption_id=disk_encryption_id,
            limit_size=limit_size,
            trigger_threshold=trigger_threshold,
        )

        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetBackupStrategy")
    def reset_backup_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupStrategy", []))

    @jsii.member(jsii_name="resetHaReplicationMode")
    def reset_ha_replication_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaReplicationMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLowerCaseTableNames")
    def reset_lower_case_table_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLowerCaseTableNames", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetParamGroupId")
    def reset_param_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParamGroupId", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetPublicIps")
    def reset_public_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIps", []))

    @jsii.member(jsii_name="resetRestoreFromBackup")
    def reset_restore_from_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreFromBackup", []))

    @jsii.member(jsii_name="resetRestorePoint")
    def reset_restore_point(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestorePoint", []))

    @jsii.member(jsii_name="resetSslEnable")
    def reset_ssl_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslEnable", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

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
    @jsii.member(jsii_name="autoscalingEnabled")
    def autoscaling_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autoscalingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="backupStrategy")
    def backup_strategy(self) -> "RdsInstanceV3BackupStrategyOutputReference":
        return typing.cast("RdsInstanceV3BackupStrategyOutputReference", jsii.get(self, "backupStrategy"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="db")
    def db(self) -> "RdsInstanceV3DbOutputReference":
        return typing.cast("RdsInstanceV3DbOutputReference", jsii.get(self, "db"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> "RdsInstanceV3NodesList":
        return typing.cast("RdsInstanceV3NodesList", jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="privateIps")
    def private_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateIps"))

    @builtins.property
    @jsii.member(jsii_name="restoredBackupId")
    def restored_backup_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restoredBackupId"))

    @builtins.property
    @jsii.member(jsii_name="restoreFromBackup")
    def restore_from_backup(self) -> "RdsInstanceV3RestoreFromBackupOutputReference":
        return typing.cast("RdsInstanceV3RestoreFromBackupOutputReference", jsii.get(self, "restoreFromBackup"))

    @builtins.property
    @jsii.member(jsii_name="restorePoint")
    def restore_point(self) -> "RdsInstanceV3RestorePointOutputReference":
        return typing.cast("RdsInstanceV3RestorePointOutputReference", jsii.get(self, "restorePoint"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RdsInstanceV3TimeoutsOutputReference":
        return typing.cast("RdsInstanceV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "RdsInstanceV3VolumeOutputReference":
        return typing.cast("RdsInstanceV3VolumeOutputReference", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="backupStrategyInput")
    def backup_strategy_input(self) -> typing.Optional["RdsInstanceV3BackupStrategy"]:
        return typing.cast(typing.Optional["RdsInstanceV3BackupStrategy"], jsii.get(self, "backupStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="dbInput")
    def db_input(self) -> typing.Optional["RdsInstanceV3Db"]:
        return typing.cast(typing.Optional["RdsInstanceV3Db"], jsii.get(self, "dbInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="haReplicationModeInput")
    def ha_replication_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haReplicationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lowerCaseTableNamesInput")
    def lower_case_table_names_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lowerCaseTableNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="paramGroupIdInput")
    def param_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "paramGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpsInput")
    def public_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreFromBackupInput")
    def restore_from_backup_input(
        self,
    ) -> typing.Optional["RdsInstanceV3RestoreFromBackup"]:
        return typing.cast(typing.Optional["RdsInstanceV3RestoreFromBackup"], jsii.get(self, "restoreFromBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePointInput")
    def restore_point_input(self) -> typing.Optional["RdsInstanceV3RestorePoint"]:
        return typing.cast(typing.Optional["RdsInstanceV3RestorePoint"], jsii.get(self, "restorePointInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sslEnableInput")
    def ssl_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RdsInstanceV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RdsInstanceV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(self) -> typing.Optional["RdsInstanceV3Volume"]:
        return typing.cast(typing.Optional["RdsInstanceV3Volume"], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395cd56eb983dc58ed83e1c8538ebd164c66af969075ab3f27ea97cc39b1a740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bed72449afc49acf090d1b7e3fe24042b761596afc34d6042d896208b7788ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="haReplicationMode")
    def ha_replication_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haReplicationMode"))

    @ha_replication_mode.setter
    def ha_replication_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb09d07396aa8808da0a13bdaff02271ca94cc1bcfafa45e29c3fc2874ef788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haReplicationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1021e267c34e83b4b285df87f24e3b1d5ea2246145be633f2797addb9243e721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lowerCaseTableNames")
    def lower_case_table_names(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lowerCaseTableNames"))

    @lower_case_table_names.setter
    def lower_case_table_names(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367a9b3a6e282c608e8a6b1acd357876463fb27c54d4320d97b86c3b29677b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lowerCaseTableNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a36e4dc6cf7c19988ec634e67e493874b1e7dd8c9eb2a3416b6131c913c22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06336b6cfafe18f7fed1e724d370145762f1e58911370d1e2e3d1000133a90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paramGroupId")
    def param_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paramGroupId"))

    @param_group_id.setter
    def param_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81eb703377a6048c15d15038b8d8823973ab277ebf74d70c9fd0078e953a70a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paramGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f9215f542f9de71f580035b2985711e70e417c1933906180cc9e2a8b18a5ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIps")
    def public_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIps"))

    @public_ips.setter
    def public_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d8e6b887b46646d58247b396597a26faeca824d1eae0dc58fa22f5e47797e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f679c48ccaf12c9dfd12d640ebae644aca94b82ec28dc88b3dc72eeb62d8040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__49aa1b001baad74fb3e79bb150ac9c2de32022d7885bddbc2708f100a02f8a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e382b865bb39b398e7806aed2cf41804a97078fc07387a5a4d102ded89e540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5607d312c72ea82ebae1364c3a03aaafb228ad84910014e5d6ea8fb13100a879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1d5c26a9214a651f19b0e1147d03ba2a45e38d5eeac2d463f751ad8a291575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62a49f53049f4549c3f57d9f08049564ba2bc1c9df31f2773d77d3d10914367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3BackupStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "start_time": "startTime",
        "keep_days": "keepDays",
        "period": "period",
    },
)
class RdsInstanceV3BackupStrategy:
    def __init__(
        self,
        *,
        start_time: builtins.str,
        keep_days: typing.Optional[jsii.Number] = None,
        period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#start_time RdsInstanceV3#start_time}.
        :param keep_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#keep_days RdsInstanceV3#keep_days}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#period RdsInstanceV3#period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b7f9f0c40e5bda291877fe2e0925d7edaad5d2a9fe59197aa3a1791d103cda)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument keep_days", value=keep_days, expected_type=type_hints["keep_days"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_time": start_time,
        }
        if keep_days is not None:
            self._values["keep_days"] = keep_days
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#start_time RdsInstanceV3#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keep_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#keep_days RdsInstanceV3#keep_days}.'''
        result = self._values.get("keep_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#period RdsInstanceV3#period}.'''
        result = self._values.get("period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3BackupStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3BackupStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3BackupStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9936d1ffac2b08d7e906ef170e9ad9c989a5a6ce9711630b8200f01dafdba8f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeepDays")
    def reset_keep_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepDays", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__641a1b352d2bb6a907f0e99477e74e52591ebab0f80f9c89f3851f311c78c82e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8506bab36ae7e3c8373a783c63f33e032b86e4d8bf6b73f4a9e2be4a61fc50b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687a33e811b83cb78042eca15648316088208256081cd6f90f1f8b6219ab7c17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3BackupStrategy]:
        return typing.cast(typing.Optional[RdsInstanceV3BackupStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RdsInstanceV3BackupStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beae2da3e086902a879448a58009499133f965e527fd45a169dd0fde2cef112c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Config",
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
        "db": "db",
        "flavor": "flavor",
        "name": "name",
        "security_group_id": "securityGroupId",
        "subnet_id": "subnetId",
        "volume": "volume",
        "vpc_id": "vpcId",
        "backup_strategy": "backupStrategy",
        "ha_replication_mode": "haReplicationMode",
        "id": "id",
        "lower_case_table_names": "lowerCaseTableNames",
        "parameters": "parameters",
        "param_group_id": "paramGroupId",
        "private_ip": "privateIp",
        "public_ips": "publicIps",
        "restore_from_backup": "restoreFromBackup",
        "restore_point": "restorePoint",
        "ssl_enable": "sslEnable",
        "tag": "tag",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class RdsInstanceV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone: typing.Sequence[builtins.str],
        db: typing.Union["RdsInstanceV3Db", typing.Dict[builtins.str, typing.Any]],
        flavor: builtins.str,
        name: builtins.str,
        security_group_id: builtins.str,
        subnet_id: builtins.str,
        volume: typing.Union["RdsInstanceV3Volume", typing.Dict[builtins.str, typing.Any]],
        vpc_id: builtins.str,
        backup_strategy: typing.Optional[typing.Union[RdsInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
        ha_replication_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lower_case_table_names: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        param_group_id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        restore_from_backup: typing.Optional[typing.Union["RdsInstanceV3RestoreFromBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_point: typing.Optional[typing.Union["RdsInstanceV3RestorePoint", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RdsInstanceV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#availability_zone RdsInstanceV3#availability_zone}.
        :param db: db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#db RdsInstanceV3#db}
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#flavor RdsInstanceV3#flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#name RdsInstanceV3#name}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#security_group_id RdsInstanceV3#security_group_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#subnet_id RdsInstanceV3#subnet_id}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#volume RdsInstanceV3#volume}
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#vpc_id RdsInstanceV3#vpc_id}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_strategy RdsInstanceV3#backup_strategy}
        :param ha_replication_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#ha_replication_mode RdsInstanceV3#ha_replication_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#id RdsInstanceV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lower_case_table_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#lower_case_table_names RdsInstanceV3#lower_case_table_names}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#parameters RdsInstanceV3#parameters}.
        :param param_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#param_group_id RdsInstanceV3#param_group_id}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#private_ip RdsInstanceV3#private_ip}.
        :param public_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#public_ips RdsInstanceV3#public_ips}.
        :param restore_from_backup: restore_from_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_from_backup RdsInstanceV3#restore_from_backup}
        :param restore_point: restore_point block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_point RdsInstanceV3#restore_point}
        :param ssl_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#ssl_enable RdsInstanceV3#ssl_enable}.
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#tag RdsInstanceV3#tag}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#tags RdsInstanceV3#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#timeouts RdsInstanceV3#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(db, dict):
            db = RdsInstanceV3Db(**db)
        if isinstance(volume, dict):
            volume = RdsInstanceV3Volume(**volume)
        if isinstance(backup_strategy, dict):
            backup_strategy = RdsInstanceV3BackupStrategy(**backup_strategy)
        if isinstance(restore_from_backup, dict):
            restore_from_backup = RdsInstanceV3RestoreFromBackup(**restore_from_backup)
        if isinstance(restore_point, dict):
            restore_point = RdsInstanceV3RestorePoint(**restore_point)
        if isinstance(timeouts, dict):
            timeouts = RdsInstanceV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1447ac4d568926e7615fef338c99245031ae279e2366f5850aaa92901574f5a2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument db", value=db, expected_type=type_hints["db"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument backup_strategy", value=backup_strategy, expected_type=type_hints["backup_strategy"])
            check_type(argname="argument ha_replication_mode", value=ha_replication_mode, expected_type=type_hints["ha_replication_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lower_case_table_names", value=lower_case_table_names, expected_type=type_hints["lower_case_table_names"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument param_group_id", value=param_group_id, expected_type=type_hints["param_group_id"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument public_ips", value=public_ips, expected_type=type_hints["public_ips"])
            check_type(argname="argument restore_from_backup", value=restore_from_backup, expected_type=type_hints["restore_from_backup"])
            check_type(argname="argument restore_point", value=restore_point, expected_type=type_hints["restore_point"])
            check_type(argname="argument ssl_enable", value=ssl_enable, expected_type=type_hints["ssl_enable"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "db": db,
            "flavor": flavor,
            "name": name,
            "security_group_id": security_group_id,
            "subnet_id": subnet_id,
            "volume": volume,
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
        if ha_replication_mode is not None:
            self._values["ha_replication_mode"] = ha_replication_mode
        if id is not None:
            self._values["id"] = id
        if lower_case_table_names is not None:
            self._values["lower_case_table_names"] = lower_case_table_names
        if parameters is not None:
            self._values["parameters"] = parameters
        if param_group_id is not None:
            self._values["param_group_id"] = param_group_id
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if public_ips is not None:
            self._values["public_ips"] = public_ips
        if restore_from_backup is not None:
            self._values["restore_from_backup"] = restore_from_backup
        if restore_point is not None:
            self._values["restore_point"] = restore_point
        if ssl_enable is not None:
            self._values["ssl_enable"] = ssl_enable
        if tag is not None:
            self._values["tag"] = tag
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
    def availability_zone(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#availability_zone RdsInstanceV3#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def db(self) -> "RdsInstanceV3Db":
        '''db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#db RdsInstanceV3#db}
        '''
        result = self._values.get("db")
        assert result is not None, "Required property 'db' is missing"
        return typing.cast("RdsInstanceV3Db", result)

    @builtins.property
    def flavor(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#flavor RdsInstanceV3#flavor}.'''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#name RdsInstanceV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#security_group_id RdsInstanceV3#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#subnet_id RdsInstanceV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume(self) -> "RdsInstanceV3Volume":
        '''volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#volume RdsInstanceV3#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast("RdsInstanceV3Volume", result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#vpc_id RdsInstanceV3#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_strategy(self) -> typing.Optional[RdsInstanceV3BackupStrategy]:
        '''backup_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_strategy RdsInstanceV3#backup_strategy}
        '''
        result = self._values.get("backup_strategy")
        return typing.cast(typing.Optional[RdsInstanceV3BackupStrategy], result)

    @builtins.property
    def ha_replication_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#ha_replication_mode RdsInstanceV3#ha_replication_mode}.'''
        result = self._values.get("ha_replication_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#id RdsInstanceV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lower_case_table_names(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#lower_case_table_names RdsInstanceV3#lower_case_table_names}.'''
        result = self._values.get("lower_case_table_names")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#parameters RdsInstanceV3#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def param_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#param_group_id RdsInstanceV3#param_group_id}.'''
        result = self._values.get("param_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#private_ip RdsInstanceV3#private_ip}.'''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#public_ips RdsInstanceV3#public_ips}.'''
        result = self._values.get("public_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def restore_from_backup(self) -> typing.Optional["RdsInstanceV3RestoreFromBackup"]:
        '''restore_from_backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_from_backup RdsInstanceV3#restore_from_backup}
        '''
        result = self._values.get("restore_from_backup")
        return typing.cast(typing.Optional["RdsInstanceV3RestoreFromBackup"], result)

    @builtins.property
    def restore_point(self) -> typing.Optional["RdsInstanceV3RestorePoint"]:
        '''restore_point block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_point RdsInstanceV3#restore_point}
        '''
        result = self._values.get("restore_point")
        return typing.cast(typing.Optional["RdsInstanceV3RestorePoint"], result)

    @builtins.property
    def ssl_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#ssl_enable RdsInstanceV3#ssl_enable}.'''
        result = self._values.get("ssl_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#tag RdsInstanceV3#tag}.'''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#tags RdsInstanceV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RdsInstanceV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#timeouts RdsInstanceV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RdsInstanceV3Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Db",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "port": "port",
        "type": "type",
        "version": "version",
    },
)
class RdsInstanceV3Db:
    def __init__(
        self,
        *,
        password: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#password RdsInstanceV3#password}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#port RdsInstanceV3#port}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#version RdsInstanceV3#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b410d106d80c4b057b931cb8917197a304194dffa3f541453e48a84b6bbbbe5b)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
        }
        if port is not None:
            self._values["port"] = port
        if type is not None:
            self._values["type"] = type
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#password RdsInstanceV3#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#port RdsInstanceV3#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#version RdsInstanceV3#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Db(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3DbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3DbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b24d2a465dae2b7e2081d3f2def048d6a6021a2b8bf37d698d199faa53c5f522)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00371010b040a0ec5c56cf3e57f1488954af066b7987398183c059fdce6322d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfa352e271182d87b51a8fc5bab95b208c103b459e033e05225cd6b67033e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc9ef9c0a27d961f5bf3af13fee28b54b604bfbf2a08bcb90cd6945fdbf43e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2536d2f1fa338f64496068806c583b2275ea771bf39bf84692fe5bab52790975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3Db]:
        return typing.cast(typing.Optional[RdsInstanceV3Db], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV3Db]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83088c7d08a3b64dbc1d989c84cf1adfd61145b9e7ab9f3732e82180c654a219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Nodes",
    jsii_struct_bases=[],
    name_mapping={},
)
class RdsInstanceV3Nodes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Nodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3NodesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3NodesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd98b9aaa713e63555a17ec63086829cb5599f56547e1dc4a57c70ad8143854a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RdsInstanceV3NodesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2986ea56c2930a1a263273595277ece1fb2124da7702bae3cdf34f359d9fc219)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RdsInstanceV3NodesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0796e4f640e2738fd3f7fd242cd61b15b77b77f4b78eb525070fba48b262b42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43d5470f520a932301f2d592dd924ca570c34bc2d555fa0acc62aa9ce8329ea2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3d977d64294177aed169ae2b2351d4e532e3b7cc1f69439a71b924248efdbd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RdsInstanceV3NodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3NodesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1b20d019b65219807ff0fee72069cdb19daaa133f1b5820e0cf47aba384736d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3Nodes]:
        return typing.cast(typing.Optional[RdsInstanceV3Nodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV3Nodes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc51e6fe0706197a26dc6cbfe9e80b3d7ffd49b391ab9512ce06a793a0b4a1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3RestoreFromBackup",
    jsii_struct_bases=[],
    name_mapping={
        "source_instance_id": "sourceInstanceId",
        "type": "type",
        "backup_id": "backupId",
        "restore_time": "restoreTime",
    },
)
class RdsInstanceV3RestoreFromBackup:
    def __init__(
        self,
        *,
        source_instance_id: builtins.str,
        type: builtins.str,
        backup_id: typing.Optional[builtins.str] = None,
        restore_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param source_instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#source_instance_id RdsInstanceV3#source_instance_id}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.
        :param backup_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.
        :param restore_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5dddbd7b9b44b3eb2114cbeabbe7dc6686452e02b257923798e1d33828870e6)
            check_type(argname="argument source_instance_id", value=source_instance_id, expected_type=type_hints["source_instance_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument backup_id", value=backup_id, expected_type=type_hints["backup_id"])
            check_type(argname="argument restore_time", value=restore_time, expected_type=type_hints["restore_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_instance_id": source_instance_id,
            "type": type,
        }
        if backup_id is not None:
            self._values["backup_id"] = backup_id
        if restore_time is not None:
            self._values["restore_time"] = restore_time

    @builtins.property
    def source_instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#source_instance_id RdsInstanceV3#source_instance_id}.'''
        result = self._values.get("source_instance_id")
        assert result is not None, "Required property 'source_instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.'''
        result = self._values.get("backup_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.'''
        result = self._values.get("restore_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3RestoreFromBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3RestoreFromBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3RestoreFromBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cdda02908ab47b8964fb23f7c92cb8b38278357dbc6fbf12b3347a69baecd11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackupId")
    def reset_backup_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupId", []))

    @jsii.member(jsii_name="resetRestoreTime")
    def reset_restore_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreTime", []))

    @builtins.property
    @jsii.member(jsii_name="backupIdInput")
    def backup_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreTimeInput")
    def restore_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "restoreTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceIdInput")
    def source_instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInstanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupId")
    def backup_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupId"))

    @backup_id.setter
    def backup_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd0e5e7d48d629d8a93ddc8cfbd750764f4023573d95c0e4753a556b012190b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restoreTime")
    def restore_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "restoreTime"))

    @restore_time.setter
    def restore_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52fc14799dc79afd0268afccadf0301343ca512173544c0da5325eedad5f6c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceId")
    def source_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstanceId"))

    @source_instance_id.setter
    def source_instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a75413c37d970b6286a13ec8aba7625018f30509b49a4c24795abe78854845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceInstanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9429856b55a87f276d30eebfe07e37bd2aeb65c1ead02a3ca620578c2a8abb8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3RestoreFromBackup]:
        return typing.cast(typing.Optional[RdsInstanceV3RestoreFromBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RdsInstanceV3RestoreFromBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5737e5bce7f3cdd9a60623ce260d11195669cc2f425da9c6c749b35b18f0390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3RestorePoint",
    jsii_struct_bases=[],
    name_mapping={
        "instance_id": "instanceId",
        "backup_id": "backupId",
        "restore_time": "restoreTime",
    },
)
class RdsInstanceV3RestorePoint:
    def __init__(
        self,
        *,
        instance_id: builtins.str,
        backup_id: typing.Optional[builtins.str] = None,
        restore_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#instance_id RdsInstanceV3#instance_id}.
        :param backup_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.
        :param restore_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b9e9753a653b236faa474d96d56c9e95507653ea0a5e20b84425c93d9a9909)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument backup_id", value=backup_id, expected_type=type_hints["backup_id"])
            check_type(argname="argument restore_time", value=restore_time, expected_type=type_hints["restore_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_id": instance_id,
        }
        if backup_id is not None:
            self._values["backup_id"] = backup_id
        if restore_time is not None:
            self._values["restore_time"] = restore_time

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#instance_id RdsInstanceV3#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#backup_id RdsInstanceV3#backup_id}.'''
        result = self._values.get("backup_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#restore_time RdsInstanceV3#restore_time}.'''
        result = self._values.get("restore_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3RestorePoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3RestorePointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3RestorePointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2452dc81b0186a115265bd1a8c76da7a7c1c429091471b06e9840f10dbf2f73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackupId")
    def reset_backup_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupId", []))

    @jsii.member(jsii_name="resetRestoreTime")
    def reset_restore_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreTime", []))

    @builtins.property
    @jsii.member(jsii_name="backupIdInput")
    def backup_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreTimeInput")
    def restore_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "restoreTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupId")
    def backup_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupId"))

    @backup_id.setter
    def backup_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57ca007f4aa3dfefcff8b34f3299815b1118d4fa093370d31bc189ff5ddb2df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ce428ff2a31f65497ee286b0bd9bafc00436fef56fa2842524e3225c4fe19c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restoreTime")
    def restore_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "restoreTime"))

    @restore_time.setter
    def restore_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1adae3274f2cb9a62e11510d47861c8acaf5c5c6b734dec6a96f2646ea8bd1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3RestorePoint]:
        return typing.cast(typing.Optional[RdsInstanceV3RestorePoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV3RestorePoint]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693e4ede86669840dc960af46c12fa4a02b6968e76d4df3d3ea9351c93ea18cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class RdsInstanceV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#create RdsInstanceV3#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#update RdsInstanceV3#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c39c3c7b022515b3b624a766be24f33766fc3f363246a9f1ac25b035bba725)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#create RdsInstanceV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#update RdsInstanceV3#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__697017be9d9b5951ceedf76cf2b42c11de37222b390817f5499be9525182a048)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__09049bcbe9ea9667b7b1ad4b6b22ad3e6499378bb3dd58fe9aab35de3f6042c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503920472e54d05f082ea5e871290499b087fa3586f2723f57fc6dcd67e33b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RdsInstanceV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RdsInstanceV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RdsInstanceV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f596cfe81adacf8b73b94bee63e0a24fab4a426692296686846cae4900d77e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3Volume",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "type": "type",
        "disk_encryption_id": "diskEncryptionId",
        "limit_size": "limitSize",
        "trigger_threshold": "triggerThreshold",
    },
)
class RdsInstanceV3Volume:
    def __init__(
        self,
        *,
        size: jsii.Number,
        type: builtins.str,
        disk_encryption_id: typing.Optional[builtins.str] = None,
        limit_size: typing.Optional[jsii.Number] = None,
        trigger_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#size RdsInstanceV3#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.
        :param disk_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#disk_encryption_id RdsInstanceV3#disk_encryption_id}.
        :param limit_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#limit_size RdsInstanceV3#limit_size}.
        :param trigger_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#trigger_threshold RdsInstanceV3#trigger_threshold}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1899b18b7cec9b1905f6a98fbb36e3d674bfa8df5b5c8957e7f112c0a0844fa8)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument disk_encryption_id", value=disk_encryption_id, expected_type=type_hints["disk_encryption_id"])
            check_type(argname="argument limit_size", value=limit_size, expected_type=type_hints["limit_size"])
            check_type(argname="argument trigger_threshold", value=trigger_threshold, expected_type=type_hints["trigger_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size": size,
            "type": type,
        }
        if disk_encryption_id is not None:
            self._values["disk_encryption_id"] = disk_encryption_id
        if limit_size is not None:
            self._values["limit_size"] = limit_size
        if trigger_threshold is not None:
            self._values["trigger_threshold"] = trigger_threshold

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#size RdsInstanceV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#type RdsInstanceV3#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_encryption_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#disk_encryption_id RdsInstanceV3#disk_encryption_id}.'''
        result = self._values.get("disk_encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#limit_size RdsInstanceV3#limit_size}.'''
        result = self._values.get("limit_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trigger_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v3#trigger_threshold RdsInstanceV3#trigger_threshold}.'''
        result = self._values.get("trigger_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV3Volume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV3VolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV3.RdsInstanceV3VolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d549a4bedcb83ba1f94de4196db53627f86ad14e5273489df61411a28233b8c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskEncryptionId")
    def reset_disk_encryption_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionId", []))

    @jsii.member(jsii_name="resetLimitSize")
    def reset_limit_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimitSize", []))

    @jsii.member(jsii_name="resetTriggerThreshold")
    def reset_trigger_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionIdInput")
    def disk_encryption_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="limitSizeInput")
    def limit_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerThresholdInput")
    def trigger_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "triggerThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionId")
    def disk_encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionId"))

    @disk_encryption_id.setter
    def disk_encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823410e779101d07a64063db81df3f0aa11bde3bc71d1bc87b20bac0ed0e1f3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limitSize")
    def limit_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limitSize"))

    @limit_size.setter
    def limit_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fff7cd2b69a6b8181d99755eeae0ef18d777067d4407b371739acccbddf2bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limitSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fe6989c1cdd8a7666bb3fba5ac1ebcb9409061b8ed1d0b24358270f0110084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerThreshold")
    def trigger_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "triggerThreshold"))

    @trigger_threshold.setter
    def trigger_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fbd8cb8a9ced40e7387dfecd1b73a693e26b4ffcacae7f531b4c52c90efc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d08d42683f67ad85fc8b69916714688eb188d55de5390f037da20507547fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV3Volume]:
        return typing.cast(typing.Optional[RdsInstanceV3Volume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV3Volume]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a2ce43fa496ed6997d3f6641500b58212f1e2f7c5250a23766f5739d3714c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RdsInstanceV3",
    "RdsInstanceV3BackupStrategy",
    "RdsInstanceV3BackupStrategyOutputReference",
    "RdsInstanceV3Config",
    "RdsInstanceV3Db",
    "RdsInstanceV3DbOutputReference",
    "RdsInstanceV3Nodes",
    "RdsInstanceV3NodesList",
    "RdsInstanceV3NodesOutputReference",
    "RdsInstanceV3RestoreFromBackup",
    "RdsInstanceV3RestoreFromBackupOutputReference",
    "RdsInstanceV3RestorePoint",
    "RdsInstanceV3RestorePointOutputReference",
    "RdsInstanceV3Timeouts",
    "RdsInstanceV3TimeoutsOutputReference",
    "RdsInstanceV3Volume",
    "RdsInstanceV3VolumeOutputReference",
]

publication.publish()

def _typecheckingstub__88d11077d95f43a5d8efbd86796e6035458973a1817e04c6b2605533066c503e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: typing.Sequence[builtins.str],
    db: typing.Union[RdsInstanceV3Db, typing.Dict[builtins.str, typing.Any]],
    flavor: builtins.str,
    name: builtins.str,
    security_group_id: builtins.str,
    subnet_id: builtins.str,
    volume: typing.Union[RdsInstanceV3Volume, typing.Dict[builtins.str, typing.Any]],
    vpc_id: builtins.str,
    backup_strategy: typing.Optional[typing.Union[RdsInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    ha_replication_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lower_case_table_names: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    param_group_id: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    restore_from_backup: typing.Optional[typing.Union[RdsInstanceV3RestoreFromBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_point: typing.Optional[typing.Union[RdsInstanceV3RestorePoint, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RdsInstanceV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__45defa5a684950ddba7cd59e1e05da42cfe64a982fb8f872f9556d45d4d09b28(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395cd56eb983dc58ed83e1c8538ebd164c66af969075ab3f27ea97cc39b1a740(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bed72449afc49acf090d1b7e3fe24042b761596afc34d6042d896208b7788ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb09d07396aa8808da0a13bdaff02271ca94cc1bcfafa45e29c3fc2874ef788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1021e267c34e83b4b285df87f24e3b1d5ea2246145be633f2797addb9243e721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367a9b3a6e282c608e8a6b1acd357876463fb27c54d4320d97b86c3b29677b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a36e4dc6cf7c19988ec634e67e493874b1e7dd8c9eb2a3416b6131c913c22b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06336b6cfafe18f7fed1e724d370145762f1e58911370d1e2e3d1000133a90a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81eb703377a6048c15d15038b8d8823973ab277ebf74d70c9fd0078e953a70a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f9215f542f9de71f580035b2985711e70e417c1933906180cc9e2a8b18a5ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d8e6b887b46646d58247b396597a26faeca824d1eae0dc58fa22f5e47797e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f679c48ccaf12c9dfd12d640ebae644aca94b82ec28dc88b3dc72eeb62d8040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49aa1b001baad74fb3e79bb150ac9c2de32022d7885bddbc2708f100a02f8a86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e382b865bb39b398e7806aed2cf41804a97078fc07387a5a4d102ded89e540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5607d312c72ea82ebae1364c3a03aaafb228ad84910014e5d6ea8fb13100a879(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1d5c26a9214a651f19b0e1147d03ba2a45e38d5eeac2d463f751ad8a291575(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62a49f53049f4549c3f57d9f08049564ba2bc1c9df31f2773d77d3d10914367(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b7f9f0c40e5bda291877fe2e0925d7edaad5d2a9fe59197aa3a1791d103cda(
    *,
    start_time: builtins.str,
    keep_days: typing.Optional[jsii.Number] = None,
    period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9936d1ffac2b08d7e906ef170e9ad9c989a5a6ce9711630b8200f01dafdba8f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641a1b352d2bb6a907f0e99477e74e52591ebab0f80f9c89f3851f311c78c82e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8506bab36ae7e3c8373a783c63f33e032b86e4d8bf6b73f4a9e2be4a61fc50b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687a33e811b83cb78042eca15648316088208256081cd6f90f1f8b6219ab7c17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beae2da3e086902a879448a58009499133f965e527fd45a169dd0fde2cef112c(
    value: typing.Optional[RdsInstanceV3BackupStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1447ac4d568926e7615fef338c99245031ae279e2366f5850aaa92901574f5a2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: typing.Sequence[builtins.str],
    db: typing.Union[RdsInstanceV3Db, typing.Dict[builtins.str, typing.Any]],
    flavor: builtins.str,
    name: builtins.str,
    security_group_id: builtins.str,
    subnet_id: builtins.str,
    volume: typing.Union[RdsInstanceV3Volume, typing.Dict[builtins.str, typing.Any]],
    vpc_id: builtins.str,
    backup_strategy: typing.Optional[typing.Union[RdsInstanceV3BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    ha_replication_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lower_case_table_names: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    param_group_id: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    restore_from_backup: typing.Optional[typing.Union[RdsInstanceV3RestoreFromBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_point: typing.Optional[typing.Union[RdsInstanceV3RestorePoint, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RdsInstanceV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b410d106d80c4b057b931cb8917197a304194dffa3f541453e48a84b6bbbbe5b(
    *,
    password: builtins.str,
    port: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24d2a465dae2b7e2081d3f2def048d6a6021a2b8bf37d698d199faa53c5f522(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00371010b040a0ec5c56cf3e57f1488954af066b7987398183c059fdce6322d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfa352e271182d87b51a8fc5bab95b208c103b459e033e05225cd6b67033e8c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc9ef9c0a27d961f5bf3af13fee28b54b604bfbf2a08bcb90cd6945fdbf43e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2536d2f1fa338f64496068806c583b2275ea771bf39bf84692fe5bab52790975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83088c7d08a3b64dbc1d989c84cf1adfd61145b9e7ab9f3732e82180c654a219(
    value: typing.Optional[RdsInstanceV3Db],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd98b9aaa713e63555a17ec63086829cb5599f56547e1dc4a57c70ad8143854a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2986ea56c2930a1a263273595277ece1fb2124da7702bae3cdf34f359d9fc219(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0796e4f640e2738fd3f7fd242cd61b15b77b77f4b78eb525070fba48b262b42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d5470f520a932301f2d592dd924ca570c34bc2d555fa0acc62aa9ce8329ea2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d977d64294177aed169ae2b2351d4e532e3b7cc1f69439a71b924248efdbd7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b20d019b65219807ff0fee72069cdb19daaa133f1b5820e0cf47aba384736d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc51e6fe0706197a26dc6cbfe9e80b3d7ffd49b391ab9512ce06a793a0b4a1a0(
    value: typing.Optional[RdsInstanceV3Nodes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dddbd7b9b44b3eb2114cbeabbe7dc6686452e02b257923798e1d33828870e6(
    *,
    source_instance_id: builtins.str,
    type: builtins.str,
    backup_id: typing.Optional[builtins.str] = None,
    restore_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdda02908ab47b8964fb23f7c92cb8b38278357dbc6fbf12b3347a69baecd11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd0e5e7d48d629d8a93ddc8cfbd750764f4023573d95c0e4753a556b012190b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52fc14799dc79afd0268afccadf0301343ca512173544c0da5325eedad5f6c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a75413c37d970b6286a13ec8aba7625018f30509b49a4c24795abe78854845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9429856b55a87f276d30eebfe07e37bd2aeb65c1ead02a3ca620578c2a8abb8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5737e5bce7f3cdd9a60623ce260d11195669cc2f425da9c6c749b35b18f0390(
    value: typing.Optional[RdsInstanceV3RestoreFromBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b9e9753a653b236faa474d96d56c9e95507653ea0a5e20b84425c93d9a9909(
    *,
    instance_id: builtins.str,
    backup_id: typing.Optional[builtins.str] = None,
    restore_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2452dc81b0186a115265bd1a8c76da7a7c1c429091471b06e9840f10dbf2f73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57ca007f4aa3dfefcff8b34f3299815b1118d4fa093370d31bc189ff5ddb2df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ce428ff2a31f65497ee286b0bd9bafc00436fef56fa2842524e3225c4fe19c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1adae3274f2cb9a62e11510d47861c8acaf5c5c6b734dec6a96f2646ea8bd1f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693e4ede86669840dc960af46c12fa4a02b6968e76d4df3d3ea9351c93ea18cf(
    value: typing.Optional[RdsInstanceV3RestorePoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c39c3c7b022515b3b624a766be24f33766fc3f363246a9f1ac25b035bba725(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697017be9d9b5951ceedf76cf2b42c11de37222b390817f5499be9525182a048(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09049bcbe9ea9667b7b1ad4b6b22ad3e6499378bb3dd58fe9aab35de3f6042c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503920472e54d05f082ea5e871290499b087fa3586f2723f57fc6dcd67e33b3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f596cfe81adacf8b73b94bee63e0a24fab4a426692296686846cae4900d77e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RdsInstanceV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1899b18b7cec9b1905f6a98fbb36e3d674bfa8df5b5c8957e7f112c0a0844fa8(
    *,
    size: jsii.Number,
    type: builtins.str,
    disk_encryption_id: typing.Optional[builtins.str] = None,
    limit_size: typing.Optional[jsii.Number] = None,
    trigger_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d549a4bedcb83ba1f94de4196db53627f86ad14e5273489df61411a28233b8c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823410e779101d07a64063db81df3f0aa11bde3bc71d1bc87b20bac0ed0e1f3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fff7cd2b69a6b8181d99755eeae0ef18d777067d4407b371739acccbddf2bc5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fe6989c1cdd8a7666bb3fba5ac1ebcb9409061b8ed1d0b24358270f0110084(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fbd8cb8a9ced40e7387dfecd1b73a693e26b4ffcacae7f531b4c52c90efc5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d08d42683f67ad85fc8b69916714688eb188d55de5390f037da20507547fd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a2ce43fa496ed6997d3f6641500b58212f1e2f7c5250a23766f5739d3714c7(
    value: typing.Optional[RdsInstanceV3Volume],
) -> None:
    """Type checking stubs"""
    pass
