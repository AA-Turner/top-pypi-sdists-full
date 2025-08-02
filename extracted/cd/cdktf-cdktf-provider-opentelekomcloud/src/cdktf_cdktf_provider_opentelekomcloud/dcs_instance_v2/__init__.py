r'''
# `opentelekomcloud_dcs_instance_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dcs_instance_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2).
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


class DcsInstanceV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2 opentelekomcloud_dcs_instance_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zones: typing.Sequence[builtins.str],
        capacity: jsii.Number,
        engine: builtins.str,
        flavor: builtins.str,
        name: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        access_user: typing.Optional[builtins.str] = None,
        backup_policy: typing.Optional[typing.Union["DcsInstanceV2BackupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        deleted_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_whitelist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV2Parameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        private_ip: typing.Optional[builtins.str] = None,
        rename_commands: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        reserved_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DcsInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        whitelist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV2WhitelistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2 opentelekomcloud_dcs_instance_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#availability_zones DcsInstanceV2#availability_zones}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#capacity DcsInstanceV2#capacity}.
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#engine DcsInstanceV2#engine}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#flavor DcsInstanceV2#flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#name DcsInstanceV2#name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#subnet_id DcsInstanceV2#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#vpc_id DcsInstanceV2#vpc_id}.
        :param access_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#access_user DcsInstanceV2#access_user}.
        :param backup_policy: backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_policy DcsInstanceV2#backup_policy}
        :param deleted_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#deleted_nodes DcsInstanceV2#deleted_nodes}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#description DcsInstanceV2#description}.
        :param enable_whitelist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#enable_whitelist DcsInstanceV2#enable_whitelist}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#engine_version DcsInstanceV2#engine_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#id DcsInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#maintain_begin DcsInstanceV2#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#maintain_end DcsInstanceV2#maintain_end}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#parameters DcsInstanceV2#parameters}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#password DcsInstanceV2#password}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#port DcsInstanceV2#port}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#private_ip DcsInstanceV2#private_ip}.
        :param rename_commands: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#rename_commands DcsInstanceV2#rename_commands}.
        :param reserved_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#reserved_ips DcsInstanceV2#reserved_ips}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#security_group_id DcsInstanceV2#security_group_id}.
        :param ssl_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#ssl_enable DcsInstanceV2#ssl_enable}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#tags DcsInstanceV2#tags}.
        :param template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#template_id DcsInstanceV2#template_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#timeouts DcsInstanceV2#timeouts}
        :param whitelist: whitelist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#whitelist DcsInstanceV2#whitelist}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d54a59647e026a570986345860bd848c44384c442763ed3624512749938762)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DcsInstanceV2Config(
            availability_zones=availability_zones,
            capacity=capacity,
            engine=engine,
            flavor=flavor,
            name=name,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            access_user=access_user,
            backup_policy=backup_policy,
            deleted_nodes=deleted_nodes,
            description=description,
            enable_whitelist=enable_whitelist,
            engine_version=engine_version,
            id=id,
            maintain_begin=maintain_begin,
            maintain_end=maintain_end,
            parameters=parameters,
            password=password,
            port=port,
            private_ip=private_ip,
            rename_commands=rename_commands,
            reserved_ips=reserved_ips,
            security_group_id=security_group_id,
            ssl_enable=ssl_enable,
            tags=tags,
            template_id=template_id,
            timeouts=timeouts,
            whitelist=whitelist,
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
        '''Generates CDKTF code for importing a DcsInstanceV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DcsInstanceV2 to import.
        :param import_from_id: The id of the existing DcsInstanceV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DcsInstanceV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3082360ebb7832207d0e95a7691cf4297285692071540092d94b863639d16015)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupPolicy")
    def put_backup_policy(
        self,
        *,
        backup_at: typing.Sequence[jsii.Number],
        begin_at: builtins.str,
        backup_type: typing.Optional[builtins.str] = None,
        period_type: typing.Optional[builtins.str] = None,
        save_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_at DcsInstanceV2#backup_at}.
        :param begin_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#begin_at DcsInstanceV2#begin_at}.
        :param backup_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_type DcsInstanceV2#backup_type}.
        :param period_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#period_type DcsInstanceV2#period_type}.
        :param save_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#save_days DcsInstanceV2#save_days}.
        '''
        value = DcsInstanceV2BackupPolicy(
            backup_at=backup_at,
            begin_at=begin_at,
            backup_type=backup_type,
            period_type=period_type,
            save_days=save_days,
        )

        return typing.cast(None, jsii.invoke(self, "putBackupPolicy", [value]))

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV2Parameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f36d710c1c5f091e5aa541428c84dbf8c3fbc8a92f4a365d205a57168d138c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#create DcsInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#delete DcsInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#update DcsInstanceV2#update}.
        '''
        value = DcsInstanceV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWhitelist")
    def put_whitelist(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV2WhitelistStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a16c0d81c3a99dcd266c33906452605258acac0530c539d29b153ffa1cde22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWhitelist", [value]))

    @jsii.member(jsii_name="resetAccessUser")
    def reset_access_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessUser", []))

    @jsii.member(jsii_name="resetBackupPolicy")
    def reset_backup_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupPolicy", []))

    @jsii.member(jsii_name="resetDeletedNodes")
    def reset_deleted_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletedNodes", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableWhitelist")
    def reset_enable_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableWhitelist", []))

    @jsii.member(jsii_name="resetEngineVersion")
    def reset_engine_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngineVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintainBegin")
    def reset_maintain_begin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainBegin", []))

    @jsii.member(jsii_name="resetMaintainEnd")
    def reset_maintain_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainEnd", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetRenameCommands")
    def reset_rename_commands(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenameCommands", []))

    @jsii.member(jsii_name="resetReservedIps")
    def reset_reserved_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedIps", []))

    @jsii.member(jsii_name="resetSecurityGroupId")
    def reset_security_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupId", []))

    @jsii.member(jsii_name="resetSslEnable")
    def reset_ssl_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslEnable", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTemplateId")
    def reset_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWhitelist")
    def reset_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhitelist", []))

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
    @jsii.member(jsii_name="backupPolicy")
    def backup_policy(self) -> "DcsInstanceV2BackupPolicyOutputReference":
        return typing.cast("DcsInstanceV2BackupPolicyOutputReference", jsii.get(self, "backupPolicy"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthInfo")
    def bandwidth_info(self) -> "DcsInstanceV2BandwidthInfoList":
        return typing.cast("DcsInstanceV2BandwidthInfoList", jsii.get(self, "bandwidthInfo"))

    @builtins.property
    @jsii.member(jsii_name="cacheMode")
    def cache_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheMode"))

    @builtins.property
    @jsii.member(jsii_name="cpuType")
    def cpu_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuType"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="launchedAt")
    def launched_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchedAt"))

    @builtins.property
    @jsii.member(jsii_name="maxMemory")
    def max_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMemory"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "DcsInstanceV2ParametersList":
        return typing.cast("DcsInstanceV2ParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="productType")
    def product_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productType"))

    @builtins.property
    @jsii.member(jsii_name="readonlyDomainName")
    def readonly_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readonlyDomainName"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupName"))

    @builtins.property
    @jsii.member(jsii_name="shardingCount")
    def sharding_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardingCount"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

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
    def timeouts(self) -> "DcsInstanceV2TimeoutsOutputReference":
        return typing.cast("DcsInstanceV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="transparentClientIpEnable")
    def transparent_client_ip_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "transparentClientIpEnable"))

    @builtins.property
    @jsii.member(jsii_name="usedMemory")
    def used_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedMemory"))

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
    @jsii.member(jsii_name="whitelist")
    def whitelist(self) -> "DcsInstanceV2WhitelistStructList":
        return typing.cast("DcsInstanceV2WhitelistStructList", jsii.get(self, "whitelist"))

    @builtins.property
    @jsii.member(jsii_name="accessUserInput")
    def access_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessUserInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZonesInput")
    def availability_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicyInput")
    def backup_policy_input(self) -> typing.Optional["DcsInstanceV2BackupPolicy"]:
        return typing.cast(typing.Optional["DcsInstanceV2BackupPolicy"], jsii.get(self, "backupPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="deletedNodesInput")
    def deleted_nodes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deletedNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableWhitelistInput")
    def enable_whitelist_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="engineInput")
    def engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineInput"))

    @builtins.property
    @jsii.member(jsii_name="engineVersionInput")
    def engine_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

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
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV2Parameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV2Parameters"]]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="renameCommandsInput")
    def rename_commands_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "renameCommandsInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedIpsInput")
    def reserved_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "reservedIpsInput"))

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
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="templateIdInput")
    def template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DcsInstanceV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DcsInstanceV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="whitelistInput")
    def whitelist_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV2WhitelistStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV2WhitelistStruct"]]], jsii.get(self, "whitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="accessUser")
    def access_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessUser"))

    @access_user.setter
    def access_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076129195bd09122a22c704781c863d81407b30180ca65899b11cc01bc886d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f76af31de42b610d8d0e72c17288195869ec62e974f5c694820caa8d34c1de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca9eb33903fd74a0c76b9ae13752bf9a1a506ff176a6edf7d7801e01f782e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletedNodes")
    def deleted_nodes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deletedNodes"))

    @deleted_nodes.setter
    def deleted_nodes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503295888a8b577033bdd7791bc709ca40b5809234b5d4856bc103470f804831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletedNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6b65e9da3ff5c82e55a7f4ad6d41c4ba8a0cd1061e8b0f6df79daba7b48516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableWhitelist")
    def enable_whitelist(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableWhitelist"))

    @enable_whitelist.setter
    def enable_whitelist(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee70f13aaf86f4b1edcb74ad33a8b6a65ce32e3f4914d493cc1a06bcc62a2d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableWhitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c182c40b1346231ce42fec0b9b87d7cfdd3db72bb7984f9f5ca47112a69eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e5ddb1856ab49ec9924d0f0011514525970f8e8ee4c62f112b5c703c93eb93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547f9c55cd4f1818d7c1ec9aaa597837fb38c37aad869a390ddacbc083b5568e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f736656557cb816d86c9de41ac045c26de535e8d8ca35fb0366eee6d673bba3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainBegin")
    def maintain_begin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainBegin"))

    @maintain_begin.setter
    def maintain_begin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f369caa66980b80db8211b7e388c1420c2c76528dbfe3e5c446f32b2c2eb258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainBegin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainEnd")
    def maintain_end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainEnd"))

    @maintain_end.setter
    def maintain_end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9488e13ee41344e9514c75995b7351efb9338efa17f82f6bd66a39d1a413d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c3fcba7a3816aed885e53ea1b4181698d8aad09199a4456cb0b9fa7482153d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cde1c391ef96edfa6be2d98d4be429f593de02b15c0eb0a4466aaf6b3cf1bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6979c7734b860bc967647ae4f3ec96a6b94b0bc93210e3ca449f0c0f45c64c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f56c2063c42811dc7d14b7fb1f250600488e594d6f408be7697cc1fbb0ac9e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renameCommands")
    def rename_commands(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "renameCommands"))

    @rename_commands.setter
    def rename_commands(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83623bec29a50b41620da849abffe739c132ff7bd8a0018f6bfc048c3482b9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renameCommands", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIps")
    def reserved_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "reservedIps"))

    @reserved_ips.setter
    def reserved_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4ce51aacdf4aaed76512f306948618bc300ceecd57b26d45868dec5bd7c912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58e67808cf6e1fff688bc9f5c758c22ea7c616b8da6a856ca35764eebad372d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef67cc0f1322627b4d566b62c583c415b6377339eb18042909ab602c9ff51377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c64dd2c3c67abc492202f95620ff1a2ede7d6f8ade337069e4291e5db57614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f77d01b40b3a9457570943027b31fdd24663a343afdea00e86c966c07b36c96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateId"))

    @template_id.setter
    def template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35612a34b11af48294338a03ba954dbfabbcce928f82f5437a583b1d6a0b67ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87d19f2183a16afeb0440fbda85adea1b149f9344f57aeb35765f15f07d9ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2BackupPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "backup_at": "backupAt",
        "begin_at": "beginAt",
        "backup_type": "backupType",
        "period_type": "periodType",
        "save_days": "saveDays",
    },
)
class DcsInstanceV2BackupPolicy:
    def __init__(
        self,
        *,
        backup_at: typing.Sequence[jsii.Number],
        begin_at: builtins.str,
        backup_type: typing.Optional[builtins.str] = None,
        period_type: typing.Optional[builtins.str] = None,
        save_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_at DcsInstanceV2#backup_at}.
        :param begin_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#begin_at DcsInstanceV2#begin_at}.
        :param backup_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_type DcsInstanceV2#backup_type}.
        :param period_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#period_type DcsInstanceV2#period_type}.
        :param save_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#save_days DcsInstanceV2#save_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2462c70b4de1a03c0626b260f5793bc134fec589508d548085ceb65ef7e44d)
            check_type(argname="argument backup_at", value=backup_at, expected_type=type_hints["backup_at"])
            check_type(argname="argument begin_at", value=begin_at, expected_type=type_hints["begin_at"])
            check_type(argname="argument backup_type", value=backup_type, expected_type=type_hints["backup_type"])
            check_type(argname="argument period_type", value=period_type, expected_type=type_hints["period_type"])
            check_type(argname="argument save_days", value=save_days, expected_type=type_hints["save_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_at": backup_at,
            "begin_at": begin_at,
        }
        if backup_type is not None:
            self._values["backup_type"] = backup_type
        if period_type is not None:
            self._values["period_type"] = period_type
        if save_days is not None:
            self._values["save_days"] = save_days

    @builtins.property
    def backup_at(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_at DcsInstanceV2#backup_at}.'''
        result = self._values.get("backup_at")
        assert result is not None, "Required property 'backup_at' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def begin_at(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#begin_at DcsInstanceV2#begin_at}.'''
        result = self._values.get("begin_at")
        assert result is not None, "Required property 'begin_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_type DcsInstanceV2#backup_type}.'''
        result = self._values.get("backup_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#period_type DcsInstanceV2#period_type}.'''
        result = self._values.get("period_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def save_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#save_days DcsInstanceV2#save_days}.'''
        result = self._values.get("save_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV2BackupPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV2BackupPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2BackupPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2830113dfbf7bc9f0fb0615ded491a8f28b3e480e507c5dd380caf3847d816ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackupType")
    def reset_backup_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupType", []))

    @jsii.member(jsii_name="resetPeriodType")
    def reset_period_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodType", []))

    @jsii.member(jsii_name="resetSaveDays")
    def reset_save_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaveDays", []))

    @builtins.property
    @jsii.member(jsii_name="backupAtInput")
    def backup_at_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "backupAtInput"))

    @builtins.property
    @jsii.member(jsii_name="backupTypeInput")
    def backup_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="beginAtInput")
    def begin_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "beginAtInput"))

    @builtins.property
    @jsii.member(jsii_name="periodTypeInput")
    def period_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="saveDaysInput")
    def save_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "saveDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="backupAt")
    def backup_at(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "backupAt"))

    @backup_at.setter
    def backup_at(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de39381d95ac8df0e9761ee139eb46c3f504db2ea38863511dc0ccbe6c152078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupType")
    def backup_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupType"))

    @backup_type.setter
    def backup_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d554d9e28efa8f8316ef1ab944d9a58b7b80749e79d591e077f28ff12976794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="beginAt")
    def begin_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "beginAt"))

    @begin_at.setter
    def begin_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f20be94ff0d01f094c293d13770b3c6d71949687db5dedd85602ef33b607533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beginAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodType")
    def period_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "periodType"))

    @period_type.setter
    def period_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160796305c1f073436e3255615e116e57b46d7670d6be40b437e93081406ca65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saveDays")
    def save_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "saveDays"))

    @save_days.setter
    def save_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bf76281c74013dba05a1203d5691c8e878b4381fad40f260b593ec2a5eea84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saveDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DcsInstanceV2BackupPolicy]:
        return typing.cast(typing.Optional[DcsInstanceV2BackupPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DcsInstanceV2BackupPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd40a5435f8e5eb4efa6d53a0c3688a742e722df5c3575b40dd4ca00482f884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2BandwidthInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class DcsInstanceV2BandwidthInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV2BandwidthInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV2BandwidthInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2BandwidthInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a6d95045812bc5579baae1b2180aace9a774d1bea8b460af774b293f01daf40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DcsInstanceV2BandwidthInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9964904ff5d877d93a6e0f74ba5aff00ad62a29fee842e450a825280b49d0761)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DcsInstanceV2BandwidthInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aecaa139c9ef6d54b46290814f571002a389d8eb9120e751e80ffcf675cefd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30382244defbabfa1d07968b4e4264e1be72f16a82fc56751a8a25a455b973d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdc4c84c5a294f91e2e68adc048d4966f23a0b65e81ba414876e1fc68154b5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DcsInstanceV2BandwidthInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2BandwidthInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10d5fdff576270ff4281d77d61c9a908cde0ebbe2a497d4dada06468b5f61af5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidth"))

    @builtins.property
    @jsii.member(jsii_name="beginTime")
    def begin_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "beginTime"))

    @builtins.property
    @jsii.member(jsii_name="currentTime")
    def current_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentTime"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="expandCount")
    def expand_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expandCount"))

    @builtins.property
    @jsii.member(jsii_name="expandEffectTime")
    def expand_effect_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expandEffectTime"))

    @builtins.property
    @jsii.member(jsii_name="expandIntervalTime")
    def expand_interval_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expandIntervalTime"))

    @builtins.property
    @jsii.member(jsii_name="maxExpandCount")
    def max_expand_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxExpandCount"))

    @builtins.property
    @jsii.member(jsii_name="nextExpandTime")
    def next_expand_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextExpandTime"))

    @builtins.property
    @jsii.member(jsii_name="taskRunning")
    def task_running(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "taskRunning"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DcsInstanceV2BandwidthInfo]:
        return typing.cast(typing.Optional[DcsInstanceV2BandwidthInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DcsInstanceV2BandwidthInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9f24f48d304cc2f03434afe34b7756305656cfbdb2f26d4c6da68aa8c28f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zones": "availabilityZones",
        "capacity": "capacity",
        "engine": "engine",
        "flavor": "flavor",
        "name": "name",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "access_user": "accessUser",
        "backup_policy": "backupPolicy",
        "deleted_nodes": "deletedNodes",
        "description": "description",
        "enable_whitelist": "enableWhitelist",
        "engine_version": "engineVersion",
        "id": "id",
        "maintain_begin": "maintainBegin",
        "maintain_end": "maintainEnd",
        "parameters": "parameters",
        "password": "password",
        "port": "port",
        "private_ip": "privateIp",
        "rename_commands": "renameCommands",
        "reserved_ips": "reservedIps",
        "security_group_id": "securityGroupId",
        "ssl_enable": "sslEnable",
        "tags": "tags",
        "template_id": "templateId",
        "timeouts": "timeouts",
        "whitelist": "whitelist",
    },
)
class DcsInstanceV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zones: typing.Sequence[builtins.str],
        capacity: jsii.Number,
        engine: builtins.str,
        flavor: builtins.str,
        name: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        access_user: typing.Optional[builtins.str] = None,
        backup_policy: typing.Optional[typing.Union[DcsInstanceV2BackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        deleted_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_whitelist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV2Parameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        private_ip: typing.Optional[builtins.str] = None,
        rename_commands: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        reserved_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DcsInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        whitelist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV2WhitelistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#availability_zones DcsInstanceV2#availability_zones}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#capacity DcsInstanceV2#capacity}.
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#engine DcsInstanceV2#engine}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#flavor DcsInstanceV2#flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#name DcsInstanceV2#name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#subnet_id DcsInstanceV2#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#vpc_id DcsInstanceV2#vpc_id}.
        :param access_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#access_user DcsInstanceV2#access_user}.
        :param backup_policy: backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_policy DcsInstanceV2#backup_policy}
        :param deleted_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#deleted_nodes DcsInstanceV2#deleted_nodes}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#description DcsInstanceV2#description}.
        :param enable_whitelist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#enable_whitelist DcsInstanceV2#enable_whitelist}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#engine_version DcsInstanceV2#engine_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#id DcsInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#maintain_begin DcsInstanceV2#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#maintain_end DcsInstanceV2#maintain_end}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#parameters DcsInstanceV2#parameters}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#password DcsInstanceV2#password}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#port DcsInstanceV2#port}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#private_ip DcsInstanceV2#private_ip}.
        :param rename_commands: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#rename_commands DcsInstanceV2#rename_commands}.
        :param reserved_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#reserved_ips DcsInstanceV2#reserved_ips}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#security_group_id DcsInstanceV2#security_group_id}.
        :param ssl_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#ssl_enable DcsInstanceV2#ssl_enable}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#tags DcsInstanceV2#tags}.
        :param template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#template_id DcsInstanceV2#template_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#timeouts DcsInstanceV2#timeouts}
        :param whitelist: whitelist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#whitelist DcsInstanceV2#whitelist}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup_policy, dict):
            backup_policy = DcsInstanceV2BackupPolicy(**backup_policy)
        if isinstance(timeouts, dict):
            timeouts = DcsInstanceV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f679e3b1030ac48dbf4676be29b38d7e94dd587a8b7a85068c7c0a28b2ea9d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument access_user", value=access_user, expected_type=type_hints["access_user"])
            check_type(argname="argument backup_policy", value=backup_policy, expected_type=type_hints["backup_policy"])
            check_type(argname="argument deleted_nodes", value=deleted_nodes, expected_type=type_hints["deleted_nodes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_whitelist", value=enable_whitelist, expected_type=type_hints["enable_whitelist"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintain_begin", value=maintain_begin, expected_type=type_hints["maintain_begin"])
            check_type(argname="argument maintain_end", value=maintain_end, expected_type=type_hints["maintain_end"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument rename_commands", value=rename_commands, expected_type=type_hints["rename_commands"])
            check_type(argname="argument reserved_ips", value=reserved_ips, expected_type=type_hints["reserved_ips"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument ssl_enable", value=ssl_enable, expected_type=type_hints["ssl_enable"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument whitelist", value=whitelist, expected_type=type_hints["whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zones": availability_zones,
            "capacity": capacity,
            "engine": engine,
            "flavor": flavor,
            "name": name,
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
        if backup_policy is not None:
            self._values["backup_policy"] = backup_policy
        if deleted_nodes is not None:
            self._values["deleted_nodes"] = deleted_nodes
        if description is not None:
            self._values["description"] = description
        if enable_whitelist is not None:
            self._values["enable_whitelist"] = enable_whitelist
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if id is not None:
            self._values["id"] = id
        if maintain_begin is not None:
            self._values["maintain_begin"] = maintain_begin
        if maintain_end is not None:
            self._values["maintain_end"] = maintain_end
        if parameters is not None:
            self._values["parameters"] = parameters
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if rename_commands is not None:
            self._values["rename_commands"] = rename_commands
        if reserved_ips is not None:
            self._values["reserved_ips"] = reserved_ips
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id
        if ssl_enable is not None:
            self._values["ssl_enable"] = ssl_enable
        if tags is not None:
            self._values["tags"] = tags
        if template_id is not None:
            self._values["template_id"] = template_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if whitelist is not None:
            self._values["whitelist"] = whitelist

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
    def availability_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#availability_zones DcsInstanceV2#availability_zones}.'''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def capacity(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#capacity DcsInstanceV2#capacity}.'''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def engine(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#engine DcsInstanceV2#engine}.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flavor(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#flavor DcsInstanceV2#flavor}.'''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#name DcsInstanceV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#subnet_id DcsInstanceV2#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#vpc_id DcsInstanceV2#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#access_user DcsInstanceV2#access_user}.'''
        result = self._values.get("access_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_policy(self) -> typing.Optional[DcsInstanceV2BackupPolicy]:
        '''backup_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#backup_policy DcsInstanceV2#backup_policy}
        '''
        result = self._values.get("backup_policy")
        return typing.cast(typing.Optional[DcsInstanceV2BackupPolicy], result)

    @builtins.property
    def deleted_nodes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#deleted_nodes DcsInstanceV2#deleted_nodes}.'''
        result = self._values.get("deleted_nodes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#description DcsInstanceV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_whitelist(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#enable_whitelist DcsInstanceV2#enable_whitelist}.'''
        result = self._values.get("enable_whitelist")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#engine_version DcsInstanceV2#engine_version}.'''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#id DcsInstanceV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_begin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#maintain_begin DcsInstanceV2#maintain_begin}.'''
        result = self._values.get("maintain_begin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#maintain_end DcsInstanceV2#maintain_end}.'''
        result = self._values.get("maintain_end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV2Parameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#parameters DcsInstanceV2#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV2Parameters"]]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#password DcsInstanceV2#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#port DcsInstanceV2#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#private_ip DcsInstanceV2#private_ip}.'''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rename_commands(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#rename_commands DcsInstanceV2#rename_commands}.'''
        result = self._values.get("rename_commands")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def reserved_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#reserved_ips DcsInstanceV2#reserved_ips}.'''
        result = self._values.get("reserved_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#security_group_id DcsInstanceV2#security_group_id}.'''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#ssl_enable DcsInstanceV2#ssl_enable}.'''
        result = self._values.get("ssl_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#tags DcsInstanceV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def template_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#template_id DcsInstanceV2#template_id}.'''
        result = self._values.get("template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DcsInstanceV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#timeouts DcsInstanceV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DcsInstanceV2Timeouts"], result)

    @builtins.property
    def whitelist(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV2WhitelistStruct"]]]:
        '''whitelist block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#whitelist DcsInstanceV2#whitelist}
        '''
        result = self._values.get("whitelist")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV2WhitelistStruct"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2Parameters",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name", "value": "value"},
)
class DcsInstanceV2Parameters:
    def __init__(
        self,
        *,
        id: builtins.str,
        name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#id DcsInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#name DcsInstanceV2#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#value DcsInstanceV2#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea1e7e14e4ce4ee92cb352a5c09952306ea99563fdc12209069fb0b31a05249)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "name": name,
            "value": value,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#id DcsInstanceV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#name DcsInstanceV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#value DcsInstanceV2#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV2Parameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV2ParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2ParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6035576f4373b0bbc091c0d8cdfb8ec4566395164bdefc97de67aa8229a0ad5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DcsInstanceV2ParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9acd5aa2f66ec43d015350eb0a9c9f6f1ab201e40639cd435dbf510369f76159)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DcsInstanceV2ParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d50578d3859402d5996eb1a78ddf2e63bedd30f7808177d41eafd1763053b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d6adb6b5f7c1ad8e61538e4e10a228118d1ea0e19878b6e9929442e54f805d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8687c73159a784071d93a7f58303f34ece46df459f32b382806d175cfe28612d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV2Parameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV2Parameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV2Parameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff4aa3025326be500482d7281bc405e963c142b6a3914683c637f9ef62ea9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DcsInstanceV2ParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2ParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86589315ae45738311fb0ff50692fff95b78248f09f7f47c39972a2b6f3891af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__658ff81a59e94c85771aed70e8b2a7c334b2f66b873f79a341e3d3d47305ccc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466a7279b9760fbf2c579fefb38833b4f06908870625f97b8db9e021e8cbdcf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9527b3903edd15b0a849358d038e7e1e420a55b9caa46b153b50bf77c51135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2Parameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2Parameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2Parameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e02d675d833a004a7f857062285bd7333943ce60deabd0c068c6456bb109e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DcsInstanceV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#create DcsInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#delete DcsInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#update DcsInstanceV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c60e317b6aba90ef4b5ae775ad62c9883359eb541de0073b3f5747509915fba)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#create DcsInstanceV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#delete DcsInstanceV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#update DcsInstanceV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a57b54643948b91eee1bc7d3daa9cec0e3487e6a5ec4a928aa01e4d7f4b1f01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05d546b681113ab231c8bd84cdd931c94e49e9fba4a3d78b53b372aa36307697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67b31ff748d263eb6c689dc69a59c8ffcca417d17cd51313b7519d2f130a7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76471558ec411d7d61e6e99ccc8d6e70785b93fed920d2394f910e6d3da5fb4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa40037928304891472c8a2e3b13f5ce6552bf16e5010c17de312e6c78f4cdf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2WhitelistStruct",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName", "ip_list": "ipList"},
)
class DcsInstanceV2WhitelistStruct:
    def __init__(
        self,
        *,
        group_name: builtins.str,
        ip_list: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#group_name DcsInstanceV2#group_name}.
        :param ip_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#ip_list DcsInstanceV2#ip_list}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b524e56a904b7a5cf8ea7738a06e0fc0bf308f458b6a6848ad4f24b5956500)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument ip_list", value=ip_list, expected_type=type_hints["ip_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_name": group_name,
            "ip_list": ip_list,
        }

    @builtins.property
    def group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#group_name DcsInstanceV2#group_name}.'''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_list(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v2#ip_list DcsInstanceV2#ip_list}.'''
        result = self._values.get("ip_list")
        assert result is not None, "Required property 'ip_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV2WhitelistStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV2WhitelistStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2WhitelistStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c123f4f86327170308156781a44ceb03f4559a8d325da2b3b9077bc90800a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DcsInstanceV2WhitelistStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15508fe00f6d3dc48232675b2367654e5942b8a6861f68647bcd897db09a120)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DcsInstanceV2WhitelistStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de217c79a40fa077b54375d9a6d2637558567a571097c4b78ce628a6eb7fe5cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01640cdfe101c648aff4248a906aef689c052b7dca0c2809270ff78ca32cf98e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb4a6e06a57f90931887fa5717b2ad65a20c9b8f0ba21e753f652261bff1ca5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV2WhitelistStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV2WhitelistStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV2WhitelistStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440cde2078dd6bb709a1b47f2c4f9a4f86623abcca422af94ad3f0c9844ebbe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DcsInstanceV2WhitelistStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV2.DcsInstanceV2WhitelistStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04136b0d47035ded832dd8f247a045251e4fde55b8bd1da222dd073a07448672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="groupNameInput")
    def group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipListInput")
    def ip_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipListInput"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f789e594b66c9dc8a049a3dd654d52ca30d19d71794df9f1114153271175eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipList")
    def ip_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipList"))

    @ip_list.setter
    def ip_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d65b94ac4b53d437e3897e8f306b73c61a6d9bb6f529517f58d8767bcab2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2WhitelistStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2WhitelistStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2WhitelistStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1b1ab8e0ed0d1edf63ee3645340562df2f1a5a3ede871274d0c5c4ac5afbb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DcsInstanceV2",
    "DcsInstanceV2BackupPolicy",
    "DcsInstanceV2BackupPolicyOutputReference",
    "DcsInstanceV2BandwidthInfo",
    "DcsInstanceV2BandwidthInfoList",
    "DcsInstanceV2BandwidthInfoOutputReference",
    "DcsInstanceV2Config",
    "DcsInstanceV2Parameters",
    "DcsInstanceV2ParametersList",
    "DcsInstanceV2ParametersOutputReference",
    "DcsInstanceV2Timeouts",
    "DcsInstanceV2TimeoutsOutputReference",
    "DcsInstanceV2WhitelistStruct",
    "DcsInstanceV2WhitelistStructList",
    "DcsInstanceV2WhitelistStructOutputReference",
]

publication.publish()

def _typecheckingstub__28d54a59647e026a570986345860bd848c44384c442763ed3624512749938762(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zones: typing.Sequence[builtins.str],
    capacity: jsii.Number,
    engine: builtins.str,
    flavor: builtins.str,
    name: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    access_user: typing.Optional[builtins.str] = None,
    backup_policy: typing.Optional[typing.Union[DcsInstanceV2BackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    deleted_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_whitelist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV2Parameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    private_ip: typing.Optional[builtins.str] = None,
    rename_commands: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    reserved_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DcsInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    whitelist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV2WhitelistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__3082360ebb7832207d0e95a7691cf4297285692071540092d94b863639d16015(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f36d710c1c5f091e5aa541428c84dbf8c3fbc8a92f4a365d205a57168d138c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV2Parameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a16c0d81c3a99dcd266c33906452605258acac0530c539d29b153ffa1cde22(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV2WhitelistStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076129195bd09122a22c704781c863d81407b30180ca65899b11cc01bc886d79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f76af31de42b610d8d0e72c17288195869ec62e974f5c694820caa8d34c1de4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca9eb33903fd74a0c76b9ae13752bf9a1a506ff176a6edf7d7801e01f782e7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503295888a8b577033bdd7791bc709ca40b5809234b5d4856bc103470f804831(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6b65e9da3ff5c82e55a7f4ad6d41c4ba8a0cd1061e8b0f6df79daba7b48516(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee70f13aaf86f4b1edcb74ad33a8b6a65ce32e3f4914d493cc1a06bcc62a2d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c182c40b1346231ce42fec0b9b87d7cfdd3db72bb7984f9f5ca47112a69eb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e5ddb1856ab49ec9924d0f0011514525970f8e8ee4c62f112b5c703c93eb93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547f9c55cd4f1818d7c1ec9aaa597837fb38c37aad869a390ddacbc083b5568e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f736656557cb816d86c9de41ac045c26de535e8d8ca35fb0366eee6d673bba3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f369caa66980b80db8211b7e388c1420c2c76528dbfe3e5c446f32b2c2eb258(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9488e13ee41344e9514c75995b7351efb9338efa17f82f6bd66a39d1a413d1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c3fcba7a3816aed885e53ea1b4181698d8aad09199a4456cb0b9fa7482153d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cde1c391ef96edfa6be2d98d4be429f593de02b15c0eb0a4466aaf6b3cf1bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6979c7734b860bc967647ae4f3ec96a6b94b0bc93210e3ca449f0c0f45c64c78(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f56c2063c42811dc7d14b7fb1f250600488e594d6f408be7697cc1fbb0ac9e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83623bec29a50b41620da849abffe739c132ff7bd8a0018f6bfc048c3482b9bc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4ce51aacdf4aaed76512f306948618bc300ceecd57b26d45868dec5bd7c912(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58e67808cf6e1fff688bc9f5c758c22ea7c616b8da6a856ca35764eebad372d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef67cc0f1322627b4d566b62c583c415b6377339eb18042909ab602c9ff51377(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c64dd2c3c67abc492202f95620ff1a2ede7d6f8ade337069e4291e5db57614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f77d01b40b3a9457570943027b31fdd24663a343afdea00e86c966c07b36c96(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35612a34b11af48294338a03ba954dbfabbcce928f82f5437a583b1d6a0b67ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87d19f2183a16afeb0440fbda85adea1b149f9344f57aeb35765f15f07d9ebc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2462c70b4de1a03c0626b260f5793bc134fec589508d548085ceb65ef7e44d(
    *,
    backup_at: typing.Sequence[jsii.Number],
    begin_at: builtins.str,
    backup_type: typing.Optional[builtins.str] = None,
    period_type: typing.Optional[builtins.str] = None,
    save_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2830113dfbf7bc9f0fb0615ded491a8f28b3e480e507c5dd380caf3847d816ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de39381d95ac8df0e9761ee139eb46c3f504db2ea38863511dc0ccbe6c152078(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d554d9e28efa8f8316ef1ab944d9a58b7b80749e79d591e077f28ff12976794(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f20be94ff0d01f094c293d13770b3c6d71949687db5dedd85602ef33b607533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160796305c1f073436e3255615e116e57b46d7670d6be40b437e93081406ca65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bf76281c74013dba05a1203d5691c8e878b4381fad40f260b593ec2a5eea84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd40a5435f8e5eb4efa6d53a0c3688a742e722df5c3575b40dd4ca00482f884(
    value: typing.Optional[DcsInstanceV2BackupPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6d95045812bc5579baae1b2180aace9a774d1bea8b460af774b293f01daf40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9964904ff5d877d93a6e0f74ba5aff00ad62a29fee842e450a825280b49d0761(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aecaa139c9ef6d54b46290814f571002a389d8eb9120e751e80ffcf675cefd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30382244defbabfa1d07968b4e4264e1be72f16a82fc56751a8a25a455b973d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc4c84c5a294f91e2e68adc048d4966f23a0b65e81ba414876e1fc68154b5cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d5fdff576270ff4281d77d61c9a908cde0ebbe2a497d4dada06468b5f61af5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9f24f48d304cc2f03434afe34b7756305656cfbdb2f26d4c6da68aa8c28f3b(
    value: typing.Optional[DcsInstanceV2BandwidthInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f679e3b1030ac48dbf4676be29b38d7e94dd587a8b7a85068c7c0a28b2ea9d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zones: typing.Sequence[builtins.str],
    capacity: jsii.Number,
    engine: builtins.str,
    flavor: builtins.str,
    name: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    access_user: typing.Optional[builtins.str] = None,
    backup_policy: typing.Optional[typing.Union[DcsInstanceV2BackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    deleted_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_whitelist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV2Parameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    private_ip: typing.Optional[builtins.str] = None,
    rename_commands: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    reserved_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    ssl_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DcsInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    whitelist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV2WhitelistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea1e7e14e4ce4ee92cb352a5c09952306ea99563fdc12209069fb0b31a05249(
    *,
    id: builtins.str,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6035576f4373b0bbc091c0d8cdfb8ec4566395164bdefc97de67aa8229a0ad5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acd5aa2f66ec43d015350eb0a9c9f6f1ab201e40639cd435dbf510369f76159(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d50578d3859402d5996eb1a78ddf2e63bedd30f7808177d41eafd1763053b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6adb6b5f7c1ad8e61538e4e10a228118d1ea0e19878b6e9929442e54f805d3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8687c73159a784071d93a7f58303f34ece46df459f32b382806d175cfe28612d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff4aa3025326be500482d7281bc405e963c142b6a3914683c637f9ef62ea9e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV2Parameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86589315ae45738311fb0ff50692fff95b78248f09f7f47c39972a2b6f3891af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658ff81a59e94c85771aed70e8b2a7c334b2f66b873f79a341e3d3d47305ccc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466a7279b9760fbf2c579fefb38833b4f06908870625f97b8db9e021e8cbdcf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9527b3903edd15b0a849358d038e7e1e420a55b9caa46b153b50bf77c51135(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e02d675d833a004a7f857062285bd7333943ce60deabd0c068c6456bb109e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2Parameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c60e317b6aba90ef4b5ae775ad62c9883359eb541de0073b3f5747509915fba(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a57b54643948b91eee1bc7d3daa9cec0e3487e6a5ec4a928aa01e4d7f4b1f01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d546b681113ab231c8bd84cdd931c94e49e9fba4a3d78b53b372aa36307697(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67b31ff748d263eb6c689dc69a59c8ffcca417d17cd51313b7519d2f130a7c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76471558ec411d7d61e6e99ccc8d6e70785b93fed920d2394f910e6d3da5fb4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa40037928304891472c8a2e3b13f5ce6552bf16e5010c17de312e6c78f4cdf5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b524e56a904b7a5cf8ea7738a06e0fc0bf308f458b6a6848ad4f24b5956500(
    *,
    group_name: builtins.str,
    ip_list: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c123f4f86327170308156781a44ceb03f4559a8d325da2b3b9077bc90800a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15508fe00f6d3dc48232675b2367654e5942b8a6861f68647bcd897db09a120(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de217c79a40fa077b54375d9a6d2637558567a571097c4b78ce628a6eb7fe5cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01640cdfe101c648aff4248a906aef689c052b7dca0c2809270ff78ca32cf98e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4a6e06a57f90931887fa5717b2ad65a20c9b8f0ba21e753f652261bff1ca5f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440cde2078dd6bb709a1b47f2c4f9a4f86623abcca422af94ad3f0c9844ebbe4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV2WhitelistStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04136b0d47035ded832dd8f247a045251e4fde55b8bd1da222dd073a07448672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f789e594b66c9dc8a049a3dd654d52ca30d19d71794df9f1114153271175eb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d65b94ac4b53d437e3897e8f306b73c61a6d9bb6f529517f58d8767bcab2e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1b1ab8e0ed0d1edf63ee3645340562df2f1a5a3ede871274d0c5c4ac5afbb6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV2WhitelistStruct]],
) -> None:
    """Type checking stubs"""
    pass
