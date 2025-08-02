r'''
# `opentelekomcloud_dcs_instance_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dcs_instance_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1).
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


class DcsInstanceV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1 opentelekomcloud_dcs_instance_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        available_zones: typing.Sequence[builtins.str],
        capacity: jsii.Number,
        engine: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        product_id: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        backup_at: typing.Optional[typing.Sequence[jsii.Number]] = None,
        backup_policy: typing.Optional[typing.Union["DcsInstanceV1BackupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        backup_type: typing.Optional[builtins.str] = None,
        begin_at: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV1Configuration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_whitelist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        period_type: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        save_days: typing.Optional[jsii.Number] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DcsInstanceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        whitelist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV1WhitelistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1 opentelekomcloud_dcs_instance_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#available_zones DcsInstanceV1#available_zones}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#capacity DcsInstanceV1#capacity}.
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#engine DcsInstanceV1#engine}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#engine_version DcsInstanceV1#engine_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#name DcsInstanceV1#name}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#product_id DcsInstanceV1#product_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#subnet_id DcsInstanceV1#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#vpc_id DcsInstanceV1#vpc_id}.
        :param backup_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_at DcsInstanceV1#backup_at}.
        :param backup_policy: backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_policy DcsInstanceV1#backup_policy}
        :param backup_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_type DcsInstanceV1#backup_type}.
        :param begin_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#begin_at DcsInstanceV1#begin_at}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#configuration DcsInstanceV1#configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#description DcsInstanceV1#description}.
        :param enable_whitelist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#enable_whitelist DcsInstanceV1#enable_whitelist}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#id DcsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#maintain_begin DcsInstanceV1#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#maintain_end DcsInstanceV1#maintain_end}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#password DcsInstanceV1#password}.
        :param period_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#period_type DcsInstanceV1#period_type}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#private_ip DcsInstanceV1#private_ip}.
        :param save_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#save_days DcsInstanceV1#save_days}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#security_group_id DcsInstanceV1#security_group_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#tags DcsInstanceV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#timeouts DcsInstanceV1#timeouts}
        :param whitelist: whitelist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#whitelist DcsInstanceV1#whitelist}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2558ba568435cc3294e150e69c3db0ec918d64515dbd88489ab13fff95f92d5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DcsInstanceV1Config(
            available_zones=available_zones,
            capacity=capacity,
            engine=engine,
            engine_version=engine_version,
            name=name,
            product_id=product_id,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            backup_at=backup_at,
            backup_policy=backup_policy,
            backup_type=backup_type,
            begin_at=begin_at,
            configuration=configuration,
            description=description,
            enable_whitelist=enable_whitelist,
            id=id,
            maintain_begin=maintain_begin,
            maintain_end=maintain_end,
            password=password,
            period_type=period_type,
            private_ip=private_ip,
            save_days=save_days,
            security_group_id=security_group_id,
            tags=tags,
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
        '''Generates CDKTF code for importing a DcsInstanceV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DcsInstanceV1 to import.
        :param import_from_id: The id of the existing DcsInstanceV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DcsInstanceV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__884a673e312ff6a94432e53c510f4388d84af553855a7152e45f0a7087dc3868)
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
        period_type: builtins.str,
        backup_type: typing.Optional[builtins.str] = None,
        save_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_at DcsInstanceV1#backup_at}.
        :param begin_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#begin_at DcsInstanceV1#begin_at}.
        :param period_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#period_type DcsInstanceV1#period_type}.
        :param backup_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_type DcsInstanceV1#backup_type}.
        :param save_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#save_days DcsInstanceV1#save_days}.
        '''
        value = DcsInstanceV1BackupPolicy(
            backup_at=backup_at,
            begin_at=begin_at,
            period_type=period_type,
            backup_type=backup_type,
            save_days=save_days,
        )

        return typing.cast(None, jsii.invoke(self, "putBackupPolicy", [value]))

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV1Configuration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced834ccd9563044d33d3566f6fe9f61d26b3cf368346578e5f96e1c6c89d661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#create DcsInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#delete DcsInstanceV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#update DcsInstanceV1#update}.
        '''
        value = DcsInstanceV1Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWhitelist")
    def put_whitelist(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV1WhitelistStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a689bf3987e12f9cfd9a2bee8ced95aa3377cb2d29c03b68e12f59b2b78811b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWhitelist", [value]))

    @jsii.member(jsii_name="resetBackupAt")
    def reset_backup_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupAt", []))

    @jsii.member(jsii_name="resetBackupPolicy")
    def reset_backup_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupPolicy", []))

    @jsii.member(jsii_name="resetBackupType")
    def reset_backup_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupType", []))

    @jsii.member(jsii_name="resetBeginAt")
    def reset_begin_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBeginAt", []))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableWhitelist")
    def reset_enable_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableWhitelist", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintainBegin")
    def reset_maintain_begin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainBegin", []))

    @jsii.member(jsii_name="resetMaintainEnd")
    def reset_maintain_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainEnd", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPeriodType")
    def reset_period_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodType", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetSaveDays")
    def reset_save_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaveDays", []))

    @jsii.member(jsii_name="resetSecurityGroupId")
    def reset_security_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    def backup_policy(self) -> "DcsInstanceV1BackupPolicyOutputReference":
        return typing.cast("DcsInstanceV1BackupPolicyOutputReference", jsii.get(self, "backupPolicy"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "DcsInstanceV1ConfigurationList":
        return typing.cast("DcsInstanceV1ConfigurationList", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="internalVersion")
    def internal_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalVersion"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @builtins.property
    @jsii.member(jsii_name="maxMemory")
    def max_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMemory"))

    @builtins.property
    @jsii.member(jsii_name="noPasswordAccess")
    def no_password_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noPasswordAccess"))

    @builtins.property
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderId"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="resourceSpecCode")
    def resource_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSpecCode"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupName"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="subnetName")
    def subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetName"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DcsInstanceV1TimeoutsOutputReference":
        return typing.cast("DcsInstanceV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def whitelist(self) -> "DcsInstanceV1WhitelistStructList":
        return typing.cast("DcsInstanceV1WhitelistStructList", jsii.get(self, "whitelist"))

    @builtins.property
    @jsii.member(jsii_name="availableZonesInput")
    def available_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availableZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="backupAtInput")
    def backup_at_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "backupAtInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicyInput")
    def backup_policy_input(self) -> typing.Optional["DcsInstanceV1BackupPolicy"]:
        return typing.cast(typing.Optional["DcsInstanceV1BackupPolicy"], jsii.get(self, "backupPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="backupTypeInput")
    def backup_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="beginAtInput")
    def begin_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "beginAtInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV1Configuration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV1Configuration"]]], jsii.get(self, "configurationInput"))

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
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="periodTypeInput")
    def period_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="productIdInput")
    def product_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productIdInput"))

    @builtins.property
    @jsii.member(jsii_name="saveDaysInput")
    def save_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "saveDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DcsInstanceV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DcsInstanceV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="whitelistInput")
    def whitelist_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV1WhitelistStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV1WhitelistStruct"]]], jsii.get(self, "whitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="availableZones")
    def available_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableZones"))

    @available_zones.setter
    def available_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09661441c484a8e9e3e27f66ef9c02907d2887877a493a48f4b37b237990a4b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupAt")
    def backup_at(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "backupAt"))

    @backup_at.setter
    def backup_at(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99cbfbd2538dcd7202ee1eb6a91e37baff2cc30e23fbf454ffb5ee40d658585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupType")
    def backup_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupType"))

    @backup_type.setter
    def backup_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7a425d20ba86cae2c265a7c7229817a8e69dcedd439ffbea34d9d4b4127ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="beginAt")
    def begin_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "beginAt"))

    @begin_at.setter
    def begin_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6d1d73c678797ce9cf5b8a767e9c409e9422e1cb557c4496334f731a133987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beginAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fb42cb9711661d8dbf888039e070549c725751628d1781ab2356bcb078d910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68175f41ea21fe57a533a47419000d638850dc29e5636966ef31428ee641564)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eb91d38a139f15d0dd0cb56ec6a1c33e0abb4d571eda310970aaad275cf3c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableWhitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915155b4ac5a8e21dfd21d3c36948eae558a4991e9e53807d12d178c33e07cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d64888b578d05866f96df9d4ae59d0967e6863646ffe3115ec56aa2632b00f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d269eb884eb6b381957fe41460c0b3c9d154a5970a24c83da98c5f9fd4ef267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainBegin")
    def maintain_begin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainBegin"))

    @maintain_begin.setter
    def maintain_begin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1812991ffc8aa53fa2f096a3e57249d0220da31da0181463834d49ac0ed3a9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainBegin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainEnd")
    def maintain_end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainEnd"))

    @maintain_end.setter
    def maintain_end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7353ba15781ec0d5bcc66f2f5165f1fabd69ea81a176292300d557bd424419ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439303dd9e390e67b1477db535c87240ffb8a511f8ba37a77e0a40e431899d54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb3f6df63ff6819398010c1a0ead6e58d653e6665c09d5bb73827761b0bd58a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodType")
    def period_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "periodType"))

    @period_type.setter
    def period_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34af601ef2c3c12eff71b9e5edad45ba6f1e951675abf5424bf0032a8eaa465b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04e2e00123fb34a0742837a911f698a0e51431cbb0e6619f956d6ef87c37b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91202c93658ed81c8b246e9d9de8733fcb0550f2d9fca9f1dbafcf8fff34d17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saveDays")
    def save_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "saveDays"))

    @save_days.setter
    def save_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5354c1a77a7c2de48e41cd2db4316dd4bd72618636039198a337d806e58f204e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saveDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562457117f48a318c55d76a5dc01d8df47d254302904a5048a3281acb02d6120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6980eb34958d375d15e53f3d13d25f02f409b0fa4255c2b9242312385890d4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a101395ca5b2aee081d03aa319edc4da377b9a1aadf0aadd4fd6efae4f8b5399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4eba495d1a142fbd0b3d879cdb5b3f2aa04f6332a3805ab79f38afa79f66be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1BackupPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "backup_at": "backupAt",
        "begin_at": "beginAt",
        "period_type": "periodType",
        "backup_type": "backupType",
        "save_days": "saveDays",
    },
)
class DcsInstanceV1BackupPolicy:
    def __init__(
        self,
        *,
        backup_at: typing.Sequence[jsii.Number],
        begin_at: builtins.str,
        period_type: builtins.str,
        backup_type: typing.Optional[builtins.str] = None,
        save_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_at DcsInstanceV1#backup_at}.
        :param begin_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#begin_at DcsInstanceV1#begin_at}.
        :param period_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#period_type DcsInstanceV1#period_type}.
        :param backup_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_type DcsInstanceV1#backup_type}.
        :param save_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#save_days DcsInstanceV1#save_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f7f978ec511b0f4bea7d9920076d2cb252d7349d817e924ef54071961bf79a)
            check_type(argname="argument backup_at", value=backup_at, expected_type=type_hints["backup_at"])
            check_type(argname="argument begin_at", value=begin_at, expected_type=type_hints["begin_at"])
            check_type(argname="argument period_type", value=period_type, expected_type=type_hints["period_type"])
            check_type(argname="argument backup_type", value=backup_type, expected_type=type_hints["backup_type"])
            check_type(argname="argument save_days", value=save_days, expected_type=type_hints["save_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_at": backup_at,
            "begin_at": begin_at,
            "period_type": period_type,
        }
        if backup_type is not None:
            self._values["backup_type"] = backup_type
        if save_days is not None:
            self._values["save_days"] = save_days

    @builtins.property
    def backup_at(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_at DcsInstanceV1#backup_at}.'''
        result = self._values.get("backup_at")
        assert result is not None, "Required property 'backup_at' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def begin_at(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#begin_at DcsInstanceV1#begin_at}.'''
        result = self._values.get("begin_at")
        assert result is not None, "Required property 'begin_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#period_type DcsInstanceV1#period_type}.'''
        result = self._values.get("period_type")
        assert result is not None, "Required property 'period_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_type DcsInstanceV1#backup_type}.'''
        result = self._values.get("backup_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def save_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#save_days DcsInstanceV1#save_days}.'''
        result = self._values.get("save_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV1BackupPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV1BackupPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1BackupPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87fc906527ff81b69ea5ba143376d36d7a8230899783311046c200385b1fe686)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackupType")
    def reset_backup_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupType", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__271b95ce36fd22116155f5196d4e212c371074e84cf1cee08d9bc19d88ee5eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupType")
    def backup_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupType"))

    @backup_type.setter
    def backup_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fab6f9bec66cfbb7db287760722dd2d5d867cfc931887e73f4d42922b166695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="beginAt")
    def begin_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "beginAt"))

    @begin_at.setter
    def begin_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1449b936946c258b9f8ccbef660e0cbfb2d86667d4cb234c5f551f4799719d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beginAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodType")
    def period_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "periodType"))

    @period_type.setter
    def period_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2586f75fa7be1dd8857a7081e19e091deba228c496517da040402db79cd041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saveDays")
    def save_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "saveDays"))

    @save_days.setter
    def save_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a5bdf193a4a52861ff9b18eb093a32c9bf16700df30473f5cf59c853288461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saveDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DcsInstanceV1BackupPolicy]:
        return typing.cast(typing.Optional[DcsInstanceV1BackupPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DcsInstanceV1BackupPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8842505f7f1eb059c950c94589919e26c9945bc40e3c7c593a9abf40a0102f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1Config",
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
        "capacity": "capacity",
        "engine": "engine",
        "engine_version": "engineVersion",
        "name": "name",
        "product_id": "productId",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "backup_at": "backupAt",
        "backup_policy": "backupPolicy",
        "backup_type": "backupType",
        "begin_at": "beginAt",
        "configuration": "configuration",
        "description": "description",
        "enable_whitelist": "enableWhitelist",
        "id": "id",
        "maintain_begin": "maintainBegin",
        "maintain_end": "maintainEnd",
        "password": "password",
        "period_type": "periodType",
        "private_ip": "privateIp",
        "save_days": "saveDays",
        "security_group_id": "securityGroupId",
        "tags": "tags",
        "timeouts": "timeouts",
        "whitelist": "whitelist",
    },
)
class DcsInstanceV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity: jsii.Number,
        engine: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        product_id: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        backup_at: typing.Optional[typing.Sequence[jsii.Number]] = None,
        backup_policy: typing.Optional[typing.Union[DcsInstanceV1BackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        backup_type: typing.Optional[builtins.str] = None,
        begin_at: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV1Configuration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_whitelist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        maintain_end: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        period_type: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        save_days: typing.Optional[jsii.Number] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DcsInstanceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        whitelist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DcsInstanceV1WhitelistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param available_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#available_zones DcsInstanceV1#available_zones}.
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#capacity DcsInstanceV1#capacity}.
        :param engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#engine DcsInstanceV1#engine}.
        :param engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#engine_version DcsInstanceV1#engine_version}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#name DcsInstanceV1#name}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#product_id DcsInstanceV1#product_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#subnet_id DcsInstanceV1#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#vpc_id DcsInstanceV1#vpc_id}.
        :param backup_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_at DcsInstanceV1#backup_at}.
        :param backup_policy: backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_policy DcsInstanceV1#backup_policy}
        :param backup_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_type DcsInstanceV1#backup_type}.
        :param begin_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#begin_at DcsInstanceV1#begin_at}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#configuration DcsInstanceV1#configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#description DcsInstanceV1#description}.
        :param enable_whitelist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#enable_whitelist DcsInstanceV1#enable_whitelist}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#id DcsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#maintain_begin DcsInstanceV1#maintain_begin}.
        :param maintain_end: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#maintain_end DcsInstanceV1#maintain_end}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#password DcsInstanceV1#password}.
        :param period_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#period_type DcsInstanceV1#period_type}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#private_ip DcsInstanceV1#private_ip}.
        :param save_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#save_days DcsInstanceV1#save_days}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#security_group_id DcsInstanceV1#security_group_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#tags DcsInstanceV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#timeouts DcsInstanceV1#timeouts}
        :param whitelist: whitelist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#whitelist DcsInstanceV1#whitelist}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup_policy, dict):
            backup_policy = DcsInstanceV1BackupPolicy(**backup_policy)
        if isinstance(timeouts, dict):
            timeouts = DcsInstanceV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8286082d94fb8e3791b48c64c74dbffbaf54a2bfd2181977d8c91c21b35f696)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument available_zones", value=available_zones, expected_type=type_hints["available_zones"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument backup_at", value=backup_at, expected_type=type_hints["backup_at"])
            check_type(argname="argument backup_policy", value=backup_policy, expected_type=type_hints["backup_policy"])
            check_type(argname="argument backup_type", value=backup_type, expected_type=type_hints["backup_type"])
            check_type(argname="argument begin_at", value=begin_at, expected_type=type_hints["begin_at"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_whitelist", value=enable_whitelist, expected_type=type_hints["enable_whitelist"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintain_begin", value=maintain_begin, expected_type=type_hints["maintain_begin"])
            check_type(argname="argument maintain_end", value=maintain_end, expected_type=type_hints["maintain_end"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument period_type", value=period_type, expected_type=type_hints["period_type"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument save_days", value=save_days, expected_type=type_hints["save_days"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument whitelist", value=whitelist, expected_type=type_hints["whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "available_zones": available_zones,
            "capacity": capacity,
            "engine": engine,
            "engine_version": engine_version,
            "name": name,
            "product_id": product_id,
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
        if backup_at is not None:
            self._values["backup_at"] = backup_at
        if backup_policy is not None:
            self._values["backup_policy"] = backup_policy
        if backup_type is not None:
            self._values["backup_type"] = backup_type
        if begin_at is not None:
            self._values["begin_at"] = begin_at
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if enable_whitelist is not None:
            self._values["enable_whitelist"] = enable_whitelist
        if id is not None:
            self._values["id"] = id
        if maintain_begin is not None:
            self._values["maintain_begin"] = maintain_begin
        if maintain_end is not None:
            self._values["maintain_end"] = maintain_end
        if password is not None:
            self._values["password"] = password
        if period_type is not None:
            self._values["period_type"] = period_type
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if save_days is not None:
            self._values["save_days"] = save_days
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id
        if tags is not None:
            self._values["tags"] = tags
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
    def available_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#available_zones DcsInstanceV1#available_zones}.'''
        result = self._values.get("available_zones")
        assert result is not None, "Required property 'available_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def capacity(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#capacity DcsInstanceV1#capacity}.'''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def engine(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#engine DcsInstanceV1#engine}.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#engine_version DcsInstanceV1#engine_version}.'''
        result = self._values.get("engine_version")
        assert result is not None, "Required property 'engine_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#name DcsInstanceV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#product_id DcsInstanceV1#product_id}.'''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#subnet_id DcsInstanceV1#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#vpc_id DcsInstanceV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_at(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_at DcsInstanceV1#backup_at}.'''
        result = self._values.get("backup_at")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def backup_policy(self) -> typing.Optional[DcsInstanceV1BackupPolicy]:
        '''backup_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_policy DcsInstanceV1#backup_policy}
        '''
        result = self._values.get("backup_policy")
        return typing.cast(typing.Optional[DcsInstanceV1BackupPolicy], result)

    @builtins.property
    def backup_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#backup_type DcsInstanceV1#backup_type}.'''
        result = self._values.get("backup_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def begin_at(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#begin_at DcsInstanceV1#begin_at}.'''
        result = self._values.get("begin_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV1Configuration"]]]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#configuration DcsInstanceV1#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV1Configuration"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#description DcsInstanceV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_whitelist(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#enable_whitelist DcsInstanceV1#enable_whitelist}.'''
        result = self._values.get("enable_whitelist")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#id DcsInstanceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_begin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#maintain_begin DcsInstanceV1#maintain_begin}.'''
        result = self._values.get("maintain_begin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_end(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#maintain_end DcsInstanceV1#maintain_end}.'''
        result = self._values.get("maintain_end")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#password DcsInstanceV1#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def period_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#period_type DcsInstanceV1#period_type}.'''
        result = self._values.get("period_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#private_ip DcsInstanceV1#private_ip}.'''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def save_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#save_days DcsInstanceV1#save_days}.'''
        result = self._values.get("save_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#security_group_id DcsInstanceV1#security_group_id}.'''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#tags DcsInstanceV1#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DcsInstanceV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#timeouts DcsInstanceV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DcsInstanceV1Timeouts"], result)

    @builtins.property
    def whitelist(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV1WhitelistStruct"]]]:
        '''whitelist block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#whitelist DcsInstanceV1#whitelist}
        '''
        result = self._values.get("whitelist")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DcsInstanceV1WhitelistStruct"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1Configuration",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_id": "parameterId",
        "parameter_name": "parameterName",
        "parameter_value": "parameterValue",
    },
)
class DcsInstanceV1Configuration:
    def __init__(
        self,
        *,
        parameter_id: builtins.str,
        parameter_name: builtins.str,
        parameter_value: builtins.str,
    ) -> None:
        '''
        :param parameter_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#parameter_id DcsInstanceV1#parameter_id}.
        :param parameter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#parameter_name DcsInstanceV1#parameter_name}.
        :param parameter_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#parameter_value DcsInstanceV1#parameter_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31fff96239829549f4d63a03d73680614e233efc480db0ad6708166332843c0)
            check_type(argname="argument parameter_id", value=parameter_id, expected_type=type_hints["parameter_id"])
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_id": parameter_id,
            "parameter_name": parameter_name,
            "parameter_value": parameter_value,
        }

    @builtins.property
    def parameter_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#parameter_id DcsInstanceV1#parameter_id}.'''
        result = self._values.get("parameter_id")
        assert result is not None, "Required property 'parameter_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#parameter_name DcsInstanceV1#parameter_name}.'''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#parameter_value DcsInstanceV1#parameter_value}.'''
        result = self._values.get("parameter_value")
        assert result is not None, "Required property 'parameter_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV1Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV1ConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1ConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38be030d7295365b1a69cf341be901adee63494139802bcf86c7514733911e69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DcsInstanceV1ConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db519a592d306661c6a79abdd9e8acf92bd3bd330c467f01d7d32e407501a291)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DcsInstanceV1ConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb1543b1ae0cff2a18c5ec48df9ea8acef71022dea77ae506fdbc4f18f6d0f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac4d93a0f564a1aaa6c172917de9677e324592843f2413c380852db4db4adc5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13778e4aeb7e84580ed9e5c12f68f3612e9819c90632be0e3156ed7dc37ad774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV1Configuration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV1Configuration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV1Configuration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd94020602bdf45a0beefe08089aa52a86422aeef542fd52523babdc8066b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DcsInstanceV1ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1ConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df163464d56561252276c55d6d319dde944feee1b708f3dca07292b7fd0fd077)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="parameterIdInput")
    def parameter_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterNameInput")
    def parameter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterValueInput")
    def parameter_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterValueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterId")
    def parameter_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterId"))

    @parameter_id.setter
    def parameter_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32bfcaf087a6875d932c8feab288d384555c2ba6611e4b86cf5e26d93480050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @parameter_name.setter
    def parameter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d75f59b35733982d653a5057c38ee6516df0831d5b5920a0fe442fd4cab0d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterValue"))

    @parameter_value.setter
    def parameter_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89eff1b27c07a22bc3733a4efac2c4fb9bf0a8a6fba9f060448353a977da56c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1Configuration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1Configuration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1Configuration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1edf191a1b4455260efd317fd47ef03310761a3470ef348619ba63dc15a8f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DcsInstanceV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#create DcsInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#delete DcsInstanceV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#update DcsInstanceV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e2d2c8a9c95055b9378c053145ec6cbd957665453b3b64f3871d55e9054227)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#create DcsInstanceV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#delete DcsInstanceV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#update DcsInstanceV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8956aaf822222aaaf57f3ce9fdf028b5c0b03eefef91b1ef116a8cf520387a50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55919dc748e123418dc5c359cd154f3ac763dddaed2464846263ccb6117b7765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1494b90eb6f2e526fc7d05f653b101755aadbe3bcec9012804a42577781f27f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78f9a60783ebf03ed4ade95f68bb1ffbfa7632dfc5667025b3a93b1db8ed5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c624a6a4b226abc5e8776607524713ccb541a30469ead4a93b0aafc51dc3d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1WhitelistStruct",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName", "ip_list": "ipList"},
)
class DcsInstanceV1WhitelistStruct:
    def __init__(
        self,
        *,
        group_name: builtins.str,
        ip_list: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#group_name DcsInstanceV1#group_name}.
        :param ip_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#ip_list DcsInstanceV1#ip_list}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7304a4fec9176eb5d7a97d937078507da933280ee69151fbad408f83c2a839)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument ip_list", value=ip_list, expected_type=type_hints["ip_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_name": group_name,
            "ip_list": ip_list,
        }

    @builtins.property
    def group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#group_name DcsInstanceV1#group_name}.'''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_list(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dcs_instance_v1#ip_list DcsInstanceV1#ip_list}.'''
        result = self._values.get("ip_list")
        assert result is not None, "Required property 'ip_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DcsInstanceV1WhitelistStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DcsInstanceV1WhitelistStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1WhitelistStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4febdd2ada5e7924ad4b731c7e41ce98e54f226ee3484af61391e9f6e0211bc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DcsInstanceV1WhitelistStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859e9470e9f1d012f34479d430d7bf0342fe167c0150a905efd713cfb04114fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DcsInstanceV1WhitelistStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969f4a7dacb2ed56dfa446d2f2756bace26f8cad5a7e574335a8a2abe6ed8085)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd8ff31dbf60c803b726b23b4efdcc5bf380a79788660f2414c90d31226da5a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a79f9f888a15a93e929d3ce8a5d72eefea4799eeff2b672742bce4c3f6b941df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV1WhitelistStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV1WhitelistStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV1WhitelistStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1acb34b2adb436dab7c1b8f338de5fb1a473f709c4de97148867e43d61babe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DcsInstanceV1WhitelistStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dcsInstanceV1.DcsInstanceV1WhitelistStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8664194b31ba993160c9c61ec20295df4a941e657ffc3621308e7b6cc3a64fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39b5982ef91ad059e1ddba2ef701d3cabd2013a53724951f5a222e480db72750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipList")
    def ip_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipList"))

    @ip_list.setter
    def ip_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7f680b9daeea36c156e0ade70851ae7746cd5df077cb9a63b02348088de249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1WhitelistStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1WhitelistStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1WhitelistStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0ce9545710ba6cbe5b5766cfab9565b2a9a1b85ec336b6242c7e5d82d45651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DcsInstanceV1",
    "DcsInstanceV1BackupPolicy",
    "DcsInstanceV1BackupPolicyOutputReference",
    "DcsInstanceV1Config",
    "DcsInstanceV1Configuration",
    "DcsInstanceV1ConfigurationList",
    "DcsInstanceV1ConfigurationOutputReference",
    "DcsInstanceV1Timeouts",
    "DcsInstanceV1TimeoutsOutputReference",
    "DcsInstanceV1WhitelistStruct",
    "DcsInstanceV1WhitelistStructList",
    "DcsInstanceV1WhitelistStructOutputReference",
]

publication.publish()

def _typecheckingstub__2558ba568435cc3294e150e69c3db0ec918d64515dbd88489ab13fff95f92d5b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    available_zones: typing.Sequence[builtins.str],
    capacity: jsii.Number,
    engine: builtins.str,
    engine_version: builtins.str,
    name: builtins.str,
    product_id: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    backup_at: typing.Optional[typing.Sequence[jsii.Number]] = None,
    backup_policy: typing.Optional[typing.Union[DcsInstanceV1BackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_type: typing.Optional[builtins.str] = None,
    begin_at: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV1Configuration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_whitelist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    period_type: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    save_days: typing.Optional[jsii.Number] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DcsInstanceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    whitelist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV1WhitelistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__884a673e312ff6a94432e53c510f4388d84af553855a7152e45f0a7087dc3868(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced834ccd9563044d33d3566f6fe9f61d26b3cf368346578e5f96e1c6c89d661(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV1Configuration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a689bf3987e12f9cfd9a2bee8ced95aa3377cb2d29c03b68e12f59b2b78811b5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV1WhitelistStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09661441c484a8e9e3e27f66ef9c02907d2887877a493a48f4b37b237990a4b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99cbfbd2538dcd7202ee1eb6a91e37baff2cc30e23fbf454ffb5ee40d658585(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7a425d20ba86cae2c265a7c7229817a8e69dcedd439ffbea34d9d4b4127ced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6d1d73c678797ce9cf5b8a767e9c409e9422e1cb557c4496334f731a133987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fb42cb9711661d8dbf888039e070549c725751628d1781ab2356bcb078d910(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68175f41ea21fe57a533a47419000d638850dc29e5636966ef31428ee641564(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb91d38a139f15d0dd0cb56ec6a1c33e0abb4d571eda310970aaad275cf3c1c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915155b4ac5a8e21dfd21d3c36948eae558a4991e9e53807d12d178c33e07cd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d64888b578d05866f96df9d4ae59d0967e6863646ffe3115ec56aa2632b00f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d269eb884eb6b381957fe41460c0b3c9d154a5970a24c83da98c5f9fd4ef267(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1812991ffc8aa53fa2f096a3e57249d0220da31da0181463834d49ac0ed3a9df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7353ba15781ec0d5bcc66f2f5165f1fabd69ea81a176292300d557bd424419ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439303dd9e390e67b1477db535c87240ffb8a511f8ba37a77e0a40e431899d54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb3f6df63ff6819398010c1a0ead6e58d653e6665c09d5bb73827761b0bd58a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34af601ef2c3c12eff71b9e5edad45ba6f1e951675abf5424bf0032a8eaa465b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04e2e00123fb34a0742837a911f698a0e51431cbb0e6619f956d6ef87c37b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91202c93658ed81c8b246e9d9de8733fcb0550f2d9fca9f1dbafcf8fff34d17a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5354c1a77a7c2de48e41cd2db4316dd4bd72618636039198a337d806e58f204e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562457117f48a318c55d76a5dc01d8df47d254302904a5048a3281acb02d6120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6980eb34958d375d15e53f3d13d25f02f409b0fa4255c2b9242312385890d4d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a101395ca5b2aee081d03aa319edc4da377b9a1aadf0aadd4fd6efae4f8b5399(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4eba495d1a142fbd0b3d879cdb5b3f2aa04f6332a3805ab79f38afa79f66be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f7f978ec511b0f4bea7d9920076d2cb252d7349d817e924ef54071961bf79a(
    *,
    backup_at: typing.Sequence[jsii.Number],
    begin_at: builtins.str,
    period_type: builtins.str,
    backup_type: typing.Optional[builtins.str] = None,
    save_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fc906527ff81b69ea5ba143376d36d7a8230899783311046c200385b1fe686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271b95ce36fd22116155f5196d4e212c371074e84cf1cee08d9bc19d88ee5eb6(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fab6f9bec66cfbb7db287760722dd2d5d867cfc931887e73f4d42922b166695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1449b936946c258b9f8ccbef660e0cbfb2d86667d4cb234c5f551f4799719d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2586f75fa7be1dd8857a7081e19e091deba228c496517da040402db79cd041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a5bdf193a4a52861ff9b18eb093a32c9bf16700df30473f5cf59c853288461(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8842505f7f1eb059c950c94589919e26c9945bc40e3c7c593a9abf40a0102f5(
    value: typing.Optional[DcsInstanceV1BackupPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8286082d94fb8e3791b48c64c74dbffbaf54a2bfd2181977d8c91c21b35f696(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    available_zones: typing.Sequence[builtins.str],
    capacity: jsii.Number,
    engine: builtins.str,
    engine_version: builtins.str,
    name: builtins.str,
    product_id: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    backup_at: typing.Optional[typing.Sequence[jsii.Number]] = None,
    backup_policy: typing.Optional[typing.Union[DcsInstanceV1BackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_type: typing.Optional[builtins.str] = None,
    begin_at: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV1Configuration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_whitelist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    maintain_end: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    period_type: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    save_days: typing.Optional[jsii.Number] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DcsInstanceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    whitelist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DcsInstanceV1WhitelistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31fff96239829549f4d63a03d73680614e233efc480db0ad6708166332843c0(
    *,
    parameter_id: builtins.str,
    parameter_name: builtins.str,
    parameter_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38be030d7295365b1a69cf341be901adee63494139802bcf86c7514733911e69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db519a592d306661c6a79abdd9e8acf92bd3bd330c467f01d7d32e407501a291(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb1543b1ae0cff2a18c5ec48df9ea8acef71022dea77ae506fdbc4f18f6d0f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4d93a0f564a1aaa6c172917de9677e324592843f2413c380852db4db4adc5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13778e4aeb7e84580ed9e5c12f68f3612e9819c90632be0e3156ed7dc37ad774(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd94020602bdf45a0beefe08089aa52a86422aeef542fd52523babdc8066b69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV1Configuration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df163464d56561252276c55d6d319dde944feee1b708f3dca07292b7fd0fd077(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32bfcaf087a6875d932c8feab288d384555c2ba6611e4b86cf5e26d93480050(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d75f59b35733982d653a5057c38ee6516df0831d5b5920a0fe442fd4cab0d97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89eff1b27c07a22bc3733a4efac2c4fb9bf0a8a6fba9f060448353a977da56c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1edf191a1b4455260efd317fd47ef03310761a3470ef348619ba63dc15a8f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1Configuration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e2d2c8a9c95055b9378c053145ec6cbd957665453b3b64f3871d55e9054227(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8956aaf822222aaaf57f3ce9fdf028b5c0b03eefef91b1ef116a8cf520387a50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55919dc748e123418dc5c359cd154f3ac763dddaed2464846263ccb6117b7765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1494b90eb6f2e526fc7d05f653b101755aadbe3bcec9012804a42577781f27f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78f9a60783ebf03ed4ade95f68bb1ffbfa7632dfc5667025b3a93b1db8ed5a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c624a6a4b226abc5e8776607524713ccb541a30469ead4a93b0aafc51dc3d76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7304a4fec9176eb5d7a97d937078507da933280ee69151fbad408f83c2a839(
    *,
    group_name: builtins.str,
    ip_list: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4febdd2ada5e7924ad4b731c7e41ce98e54f226ee3484af61391e9f6e0211bc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859e9470e9f1d012f34479d430d7bf0342fe167c0150a905efd713cfb04114fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969f4a7dacb2ed56dfa446d2f2756bace26f8cad5a7e574335a8a2abe6ed8085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8ff31dbf60c803b726b23b4efdcc5bf380a79788660f2414c90d31226da5a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79f9f888a15a93e929d3ce8a5d72eefea4799eeff2b672742bce4c3f6b941df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1acb34b2adb436dab7c1b8f338de5fb1a473f709c4de97148867e43d61babe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DcsInstanceV1WhitelistStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8664194b31ba993160c9c61ec20295df4a941e657ffc3621308e7b6cc3a64fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b5982ef91ad059e1ddba2ef701d3cabd2013a53724951f5a222e480db72750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7f680b9daeea36c156e0ade70851ae7746cd5df077cb9a63b02348088de249(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0ce9545710ba6cbe5b5766cfab9565b2a9a1b85ec336b6242c7e5d82d45651(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DcsInstanceV1WhitelistStruct]],
) -> None:
    """Type checking stubs"""
    pass
