r'''
# `azurerm_backup_policy_vm_workload`

Refer to the Terraform Registry for docs: [`azurerm_backup_policy_vm_workload`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload).
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


class BackupPolicyVmWorkload(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkload",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload azurerm_backup_policy_vm_workload}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        protection_policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPolicyVmWorkloadProtectionPolicy", typing.Dict[builtins.str, typing.Any]]]],
        recovery_vault_name: builtins.str,
        resource_group_name: builtins.str,
        settings: typing.Union["BackupPolicyVmWorkloadSettings", typing.Dict[builtins.str, typing.Any]],
        workload_type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BackupPolicyVmWorkloadTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload azurerm_backup_policy_vm_workload} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#name BackupPolicyVmWorkload#name}.
        :param protection_policy: protection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#protection_policy BackupPolicyVmWorkload#protection_policy}
        :param recovery_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#recovery_vault_name BackupPolicyVmWorkload#recovery_vault_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#resource_group_name BackupPolicyVmWorkload#resource_group_name}.
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#settings BackupPolicyVmWorkload#settings}
        :param workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#workload_type BackupPolicyVmWorkload#workload_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#id BackupPolicyVmWorkload#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#timeouts BackupPolicyVmWorkload#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55f9213c4df5bc2da429f2ec189f292b4cbb21d77cb04e457f3a6380a08d469)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BackupPolicyVmWorkloadConfig(
            name=name,
            protection_policy=protection_policy,
            recovery_vault_name=recovery_vault_name,
            resource_group_name=resource_group_name,
            settings=settings,
            workload_type=workload_type,
            id=id,
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
        '''Generates CDKTF code for importing a BackupPolicyVmWorkload resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BackupPolicyVmWorkload to import.
        :param import_from_id: The id of the existing BackupPolicyVmWorkload that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BackupPolicyVmWorkload to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15d0bf086a69a16d49b5662fbf9b82131861f096c6b7b6db7d697556329daf6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putProtectionPolicy")
    def put_protection_policy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPolicyVmWorkloadProtectionPolicy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e8808733f9bf907e7014f4ba091afb69aa3e5c310097bdc12c597f69eb7b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProtectionPolicy", [value]))

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        time_zone: builtins.str,
        compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#time_zone BackupPolicyVmWorkload#time_zone}.
        :param compression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#compression_enabled BackupPolicyVmWorkload#compression_enabled}.
        '''
        value = BackupPolicyVmWorkloadSettings(
            time_zone=time_zone, compression_enabled=compression_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#create BackupPolicyVmWorkload#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#delete BackupPolicyVmWorkload#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#read BackupPolicyVmWorkload#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#update BackupPolicyVmWorkload#update}.
        '''
        value = BackupPolicyVmWorkloadTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="protectionPolicy")
    def protection_policy(self) -> "BackupPolicyVmWorkloadProtectionPolicyList":
        return typing.cast("BackupPolicyVmWorkloadProtectionPolicyList", jsii.get(self, "protectionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "BackupPolicyVmWorkloadSettingsOutputReference":
        return typing.cast("BackupPolicyVmWorkloadSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BackupPolicyVmWorkloadTimeoutsOutputReference":
        return typing.cast("BackupPolicyVmWorkloadTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protectionPolicyInput")
    def protection_policy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPolicyVmWorkloadProtectionPolicy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPolicyVmWorkloadProtectionPolicy"]]], jsii.get(self, "protectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultNameInput")
    def recovery_vault_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryVaultNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(self) -> typing.Optional["BackupPolicyVmWorkloadSettings"]:
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BackupPolicyVmWorkloadTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BackupPolicyVmWorkloadTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadTypeInput")
    def workload_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323eb0bc5f7b12fa978070efabd83dbc921e6df217e67f91e760e3133bac690e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73272f7e53d6210a6d2baf625768fe7b8b19d9f776f7b0089a4f7a5680e217aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryVaultName")
    def recovery_vault_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryVaultName"))

    @recovery_vault_name.setter
    def recovery_vault_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bf92728588c2574d24b7cd451bb9b62097a6b41ec4f1d341e77cb1b5255c53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryVaultName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60d8c5b149a1e453bac162d6528a2db3aac40352359336fa765d95275ec876c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadType")
    def workload_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadType"))

    @workload_type.setter
    def workload_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7f3de1af0d0f59baa857141b00ac6910c999d3db7ad35d067a5fa062710b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "protection_policy": "protectionPolicy",
        "recovery_vault_name": "recoveryVaultName",
        "resource_group_name": "resourceGroupName",
        "settings": "settings",
        "workload_type": "workloadType",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class BackupPolicyVmWorkloadConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        protection_policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPolicyVmWorkloadProtectionPolicy", typing.Dict[builtins.str, typing.Any]]]],
        recovery_vault_name: builtins.str,
        resource_group_name: builtins.str,
        settings: typing.Union["BackupPolicyVmWorkloadSettings", typing.Dict[builtins.str, typing.Any]],
        workload_type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BackupPolicyVmWorkloadTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#name BackupPolicyVmWorkload#name}.
        :param protection_policy: protection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#protection_policy BackupPolicyVmWorkload#protection_policy}
        :param recovery_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#recovery_vault_name BackupPolicyVmWorkload#recovery_vault_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#resource_group_name BackupPolicyVmWorkload#resource_group_name}.
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#settings BackupPolicyVmWorkload#settings}
        :param workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#workload_type BackupPolicyVmWorkload#workload_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#id BackupPolicyVmWorkload#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#timeouts BackupPolicyVmWorkload#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(settings, dict):
            settings = BackupPolicyVmWorkloadSettings(**settings)
        if isinstance(timeouts, dict):
            timeouts = BackupPolicyVmWorkloadTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da657c8ac3fd2c47c0f8c0ab4b8606876977726ac4c8644e48f9cd7fb622f9be)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protection_policy", value=protection_policy, expected_type=type_hints["protection_policy"])
            check_type(argname="argument recovery_vault_name", value=recovery_vault_name, expected_type=type_hints["recovery_vault_name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument workload_type", value=workload_type, expected_type=type_hints["workload_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "protection_policy": protection_policy,
            "recovery_vault_name": recovery_vault_name,
            "resource_group_name": resource_group_name,
            "settings": settings,
            "workload_type": workload_type,
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#name BackupPolicyVmWorkload#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protection_policy(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPolicyVmWorkloadProtectionPolicy"]]:
        '''protection_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#protection_policy BackupPolicyVmWorkload#protection_policy}
        '''
        result = self._values.get("protection_policy")
        assert result is not None, "Required property 'protection_policy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPolicyVmWorkloadProtectionPolicy"]], result)

    @builtins.property
    def recovery_vault_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#recovery_vault_name BackupPolicyVmWorkload#recovery_vault_name}.'''
        result = self._values.get("recovery_vault_name")
        assert result is not None, "Required property 'recovery_vault_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#resource_group_name BackupPolicyVmWorkload#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def settings(self) -> "BackupPolicyVmWorkloadSettings":
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#settings BackupPolicyVmWorkload#settings}
        '''
        result = self._values.get("settings")
        assert result is not None, "Required property 'settings' is missing"
        return typing.cast("BackupPolicyVmWorkloadSettings", result)

    @builtins.property
    def workload_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#workload_type BackupPolicyVmWorkload#workload_type}.'''
        result = self._values.get("workload_type")
        assert result is not None, "Required property 'workload_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#id BackupPolicyVmWorkload#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BackupPolicyVmWorkloadTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#timeouts BackupPolicyVmWorkload#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "backup": "backup",
        "policy_type": "policyType",
        "retention_daily": "retentionDaily",
        "retention_monthly": "retentionMonthly",
        "retention_weekly": "retentionWeekly",
        "retention_yearly": "retentionYearly",
        "simple_retention": "simpleRetention",
    },
)
class BackupPolicyVmWorkloadProtectionPolicy:
    def __init__(
        self,
        *,
        backup: typing.Union["BackupPolicyVmWorkloadProtectionPolicyBackup", typing.Dict[builtins.str, typing.Any]],
        policy_type: builtins.str,
        retention_daily: typing.Optional[typing.Union["BackupPolicyVmWorkloadProtectionPolicyRetentionDaily", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_monthly: typing.Optional[typing.Union["BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_weekly: typing.Optional[typing.Union["BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_yearly: typing.Optional[typing.Union["BackupPolicyVmWorkloadProtectionPolicyRetentionYearly", typing.Dict[builtins.str, typing.Any]]] = None,
        simple_retention: typing.Optional[typing.Union["BackupPolicyVmWorkloadProtectionPolicySimpleRetention", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#backup BackupPolicyVmWorkload#backup}
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#policy_type BackupPolicyVmWorkload#policy_type}.
        :param retention_daily: retention_daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#retention_daily BackupPolicyVmWorkload#retention_daily}
        :param retention_monthly: retention_monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#retention_monthly BackupPolicyVmWorkload#retention_monthly}
        :param retention_weekly: retention_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#retention_weekly BackupPolicyVmWorkload#retention_weekly}
        :param retention_yearly: retention_yearly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#retention_yearly BackupPolicyVmWorkload#retention_yearly}
        :param simple_retention: simple_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#simple_retention BackupPolicyVmWorkload#simple_retention}
        '''
        if isinstance(backup, dict):
            backup = BackupPolicyVmWorkloadProtectionPolicyBackup(**backup)
        if isinstance(retention_daily, dict):
            retention_daily = BackupPolicyVmWorkloadProtectionPolicyRetentionDaily(**retention_daily)
        if isinstance(retention_monthly, dict):
            retention_monthly = BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly(**retention_monthly)
        if isinstance(retention_weekly, dict):
            retention_weekly = BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly(**retention_weekly)
        if isinstance(retention_yearly, dict):
            retention_yearly = BackupPolicyVmWorkloadProtectionPolicyRetentionYearly(**retention_yearly)
        if isinstance(simple_retention, dict):
            simple_retention = BackupPolicyVmWorkloadProtectionPolicySimpleRetention(**simple_retention)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4abb190e8b10e5d71e484af4cf0c46cc62c91ae5b10007d7d8e50d77ae22fc7)
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument retention_daily", value=retention_daily, expected_type=type_hints["retention_daily"])
            check_type(argname="argument retention_monthly", value=retention_monthly, expected_type=type_hints["retention_monthly"])
            check_type(argname="argument retention_weekly", value=retention_weekly, expected_type=type_hints["retention_weekly"])
            check_type(argname="argument retention_yearly", value=retention_yearly, expected_type=type_hints["retention_yearly"])
            check_type(argname="argument simple_retention", value=simple_retention, expected_type=type_hints["simple_retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup": backup,
            "policy_type": policy_type,
        }
        if retention_daily is not None:
            self._values["retention_daily"] = retention_daily
        if retention_monthly is not None:
            self._values["retention_monthly"] = retention_monthly
        if retention_weekly is not None:
            self._values["retention_weekly"] = retention_weekly
        if retention_yearly is not None:
            self._values["retention_yearly"] = retention_yearly
        if simple_retention is not None:
            self._values["simple_retention"] = simple_retention

    @builtins.property
    def backup(self) -> "BackupPolicyVmWorkloadProtectionPolicyBackup":
        '''backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#backup BackupPolicyVmWorkload#backup}
        '''
        result = self._values.get("backup")
        assert result is not None, "Required property 'backup' is missing"
        return typing.cast("BackupPolicyVmWorkloadProtectionPolicyBackup", result)

    @builtins.property
    def policy_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#policy_type BackupPolicyVmWorkload#policy_type}.'''
        result = self._values.get("policy_type")
        assert result is not None, "Required property 'policy_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_daily(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionDaily"]:
        '''retention_daily block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#retention_daily BackupPolicyVmWorkload#retention_daily}
        '''
        result = self._values.get("retention_daily")
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionDaily"], result)

    @builtins.property
    def retention_monthly(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly"]:
        '''retention_monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#retention_monthly BackupPolicyVmWorkload#retention_monthly}
        '''
        result = self._values.get("retention_monthly")
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly"], result)

    @builtins.property
    def retention_weekly(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly"]:
        '''retention_weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#retention_weekly BackupPolicyVmWorkload#retention_weekly}
        '''
        result = self._values.get("retention_weekly")
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly"], result)

    @builtins.property
    def retention_yearly(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionYearly"]:
        '''retention_yearly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#retention_yearly BackupPolicyVmWorkload#retention_yearly}
        '''
        result = self._values.get("retention_yearly")
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionYearly"], result)

    @builtins.property
    def simple_retention(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicySimpleRetention"]:
        '''simple_retention block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#simple_retention BackupPolicyVmWorkload#simple_retention}
        '''
        result = self._values.get("simple_retention")
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicySimpleRetention"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadProtectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyBackup",
    jsii_struct_bases=[],
    name_mapping={
        "frequency": "frequency",
        "frequency_in_minutes": "frequencyInMinutes",
        "time": "time",
        "weekdays": "weekdays",
    },
)
class BackupPolicyVmWorkloadProtectionPolicyBackup:
    def __init__(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        frequency_in_minutes: typing.Optional[jsii.Number] = None,
        time: typing.Optional[builtins.str] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#frequency BackupPolicyVmWorkload#frequency}.
        :param frequency_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#frequency_in_minutes BackupPolicyVmWorkload#frequency_in_minutes}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#time BackupPolicyVmWorkload#time}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa882f9cadcf2f643ced5afd2d92aea2d0a5311c01476397ba58e5563146382)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument frequency_in_minutes", value=frequency_in_minutes, expected_type=type_hints["frequency_in_minutes"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency
        if frequency_in_minutes is not None:
            self._values["frequency_in_minutes"] = frequency_in_minutes
        if time is not None:
            self._values["time"] = time
        if weekdays is not None:
            self._values["weekdays"] = weekdays

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#frequency BackupPolicyVmWorkload#frequency}.'''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frequency_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#frequency_in_minutes BackupPolicyVmWorkload#frequency_in_minutes}.'''
        result = self._values.get("frequency_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#time BackupPolicyVmWorkload#time}.'''
        result = self._values.get("time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadProtectionPolicyBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmWorkloadProtectionPolicyBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__546e8792820527177308d925580f6ce1357c0482007be6e9e8904fd55ef6eba1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetFrequencyInMinutes")
    def reset_frequency_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequencyInMinutes", []))

    @jsii.member(jsii_name="resetTime")
    def reset_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTime", []))

    @jsii.member(jsii_name="resetWeekdays")
    def reset_weekdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekdays", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInMinutesInput")
    def frequency_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f69697efb7a2d5338fffa93f101b770fd8a9a8f608dcfa7bb0c676425b9ee4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequencyInMinutes")
    def frequency_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInMinutes"))

    @frequency_in_minutes.setter
    def frequency_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c67c1ddf9f2bfc1c5a963d1aa18d713bf461398220ce847cc882e0f47ae3b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6beb867630e51e808f2b5ada5bcb787841657f29020373506348af96cc9c541f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a6188609e180441611eb84968e345bdbcf39f51475a3618e13e96145cd0a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupPolicyVmWorkloadProtectionPolicyBackup]:
        return typing.cast(typing.Optional[BackupPolicyVmWorkloadProtectionPolicyBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93622603d7279f2197be861310837b22a4f2c46d1eb597ed6c8726d300666207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPolicyVmWorkloadProtectionPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e55b0a142d4caab01f7aa5da8f518fb2155b5105937ad534a88b1797d50336aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BackupPolicyVmWorkloadProtectionPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6342a2990a3af9fa26566885d18b9ca7e0dbbc982b4e3823f4be3b0e7edd7fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPolicyVmWorkloadProtectionPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759646d48f5661a61696505bbc6e6922aeff44cc945e2d760b741a5dc4fb4e5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f10f409b7a627dbd23bbcd5044692bd1bcdadae974ec4931470bac5cb8c9574)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16b2c03811dbda4819f22a95d0982f817d8a78a1f70f861cb462dada2d0bbc8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPolicyVmWorkloadProtectionPolicy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPolicyVmWorkloadProtectionPolicy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPolicyVmWorkloadProtectionPolicy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792a035c303c5578549baabe747633b0987b46b69dd3f211584a156b9ff9483d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPolicyVmWorkloadProtectionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08336f59053abeeb04aa23b9be58a5881486d9bb8fdd17b007fccccae49abd84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBackup")
    def put_backup(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        frequency_in_minutes: typing.Optional[jsii.Number] = None,
        time: typing.Optional[builtins.str] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#frequency BackupPolicyVmWorkload#frequency}.
        :param frequency_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#frequency_in_minutes BackupPolicyVmWorkload#frequency_in_minutes}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#time BackupPolicyVmWorkload#time}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.
        '''
        value = BackupPolicyVmWorkloadProtectionPolicyBackup(
            frequency=frequency,
            frequency_in_minutes=frequency_in_minutes,
            time=time,
            weekdays=weekdays,
        )

        return typing.cast(None, jsii.invoke(self, "putBackup", [value]))

    @jsii.member(jsii_name="putRetentionDaily")
    def put_retention_daily(self, *, count: jsii.Number) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        '''
        value = BackupPolicyVmWorkloadProtectionPolicyRetentionDaily(count=count)

        return typing.cast(None, jsii.invoke(self, "putRetentionDaily", [value]))

    @jsii.member(jsii_name="putRetentionMonthly")
    def put_retention_monthly(
        self,
        *,
        count: jsii.Number,
        format_type: builtins.str,
        monthdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        :param format_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#format_type BackupPolicyVmWorkload#format_type}.
        :param monthdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#monthdays BackupPolicyVmWorkload#monthdays}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weeks BackupPolicyVmWorkload#weeks}.
        '''
        value = BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly(
            count=count,
            format_type=format_type,
            monthdays=monthdays,
            weekdays=weekdays,
            weeks=weeks,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionMonthly", [value]))

    @jsii.member(jsii_name="putRetentionWeekly")
    def put_retention_weekly(
        self,
        *,
        count: jsii.Number,
        weekdays: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.
        '''
        value = BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly(
            count=count, weekdays=weekdays
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionWeekly", [value]))

    @jsii.member(jsii_name="putRetentionYearly")
    def put_retention_yearly(
        self,
        *,
        count: jsii.Number,
        format_type: builtins.str,
        months: typing.Sequence[builtins.str],
        monthdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        :param format_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#format_type BackupPolicyVmWorkload#format_type}.
        :param months: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#months BackupPolicyVmWorkload#months}.
        :param monthdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#monthdays BackupPolicyVmWorkload#monthdays}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weeks BackupPolicyVmWorkload#weeks}.
        '''
        value = BackupPolicyVmWorkloadProtectionPolicyRetentionYearly(
            count=count,
            format_type=format_type,
            months=months,
            monthdays=monthdays,
            weekdays=weekdays,
            weeks=weeks,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionYearly", [value]))

    @jsii.member(jsii_name="putSimpleRetention")
    def put_simple_retention(self, *, count: jsii.Number) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        '''
        value = BackupPolicyVmWorkloadProtectionPolicySimpleRetention(count=count)

        return typing.cast(None, jsii.invoke(self, "putSimpleRetention", [value]))

    @jsii.member(jsii_name="resetRetentionDaily")
    def reset_retention_daily(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDaily", []))

    @jsii.member(jsii_name="resetRetentionMonthly")
    def reset_retention_monthly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionMonthly", []))

    @jsii.member(jsii_name="resetRetentionWeekly")
    def reset_retention_weekly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionWeekly", []))

    @jsii.member(jsii_name="resetRetentionYearly")
    def reset_retention_yearly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionYearly", []))

    @jsii.member(jsii_name="resetSimpleRetention")
    def reset_simple_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleRetention", []))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> BackupPolicyVmWorkloadProtectionPolicyBackupOutputReference:
        return typing.cast(BackupPolicyVmWorkloadProtectionPolicyBackupOutputReference, jsii.get(self, "backup"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaily")
    def retention_daily(
        self,
    ) -> "BackupPolicyVmWorkloadProtectionPolicyRetentionDailyOutputReference":
        return typing.cast("BackupPolicyVmWorkloadProtectionPolicyRetentionDailyOutputReference", jsii.get(self, "retentionDaily"))

    @builtins.property
    @jsii.member(jsii_name="retentionMonthly")
    def retention_monthly(
        self,
    ) -> "BackupPolicyVmWorkloadProtectionPolicyRetentionMonthlyOutputReference":
        return typing.cast("BackupPolicyVmWorkloadProtectionPolicyRetentionMonthlyOutputReference", jsii.get(self, "retentionMonthly"))

    @builtins.property
    @jsii.member(jsii_name="retentionWeekly")
    def retention_weekly(
        self,
    ) -> "BackupPolicyVmWorkloadProtectionPolicyRetentionWeeklyOutputReference":
        return typing.cast("BackupPolicyVmWorkloadProtectionPolicyRetentionWeeklyOutputReference", jsii.get(self, "retentionWeekly"))

    @builtins.property
    @jsii.member(jsii_name="retentionYearly")
    def retention_yearly(
        self,
    ) -> "BackupPolicyVmWorkloadProtectionPolicyRetentionYearlyOutputReference":
        return typing.cast("BackupPolicyVmWorkloadProtectionPolicyRetentionYearlyOutputReference", jsii.get(self, "retentionYearly"))

    @builtins.property
    @jsii.member(jsii_name="simpleRetention")
    def simple_retention(
        self,
    ) -> "BackupPolicyVmWorkloadProtectionPolicySimpleRetentionOutputReference":
        return typing.cast("BackupPolicyVmWorkloadProtectionPolicySimpleRetentionOutputReference", jsii.get(self, "simpleRetention"))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(
        self,
    ) -> typing.Optional[BackupPolicyVmWorkloadProtectionPolicyBackup]:
        return typing.cast(typing.Optional[BackupPolicyVmWorkloadProtectionPolicyBackup], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="policyTypeInput")
    def policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDailyInput")
    def retention_daily_input(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionDaily"]:
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionDaily"], jsii.get(self, "retentionDailyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionMonthlyInput")
    def retention_monthly_input(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly"]:
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly"], jsii.get(self, "retentionMonthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionWeeklyInput")
    def retention_weekly_input(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly"]:
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly"], jsii.get(self, "retentionWeeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionYearlyInput")
    def retention_yearly_input(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionYearly"]:
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicyRetentionYearly"], jsii.get(self, "retentionYearlyInput"))

    @builtins.property
    @jsii.member(jsii_name="simpleRetentionInput")
    def simple_retention_input(
        self,
    ) -> typing.Optional["BackupPolicyVmWorkloadProtectionPolicySimpleRetention"]:
        return typing.cast(typing.Optional["BackupPolicyVmWorkloadProtectionPolicySimpleRetention"], jsii.get(self, "simpleRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyType"))

    @policy_type.setter
    def policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547b47ac4b3f3bf45392093d9f7e7299762bd7b79780013172b3a17bdc3a2d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmWorkloadProtectionPolicy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmWorkloadProtectionPolicy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmWorkloadProtectionPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389721ec0ebadbc816c9c6eea3f672c8d1e36a53e041436314d5c9e8cf97b397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyRetentionDaily",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class BackupPolicyVmWorkloadProtectionPolicyRetentionDaily:
    def __init__(self, *, count: jsii.Number) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b8358e3ba0d9a525430343d2bc2ed1c6437cc0e2af40ea27051597f10e3068)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadProtectionPolicyRetentionDaily(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmWorkloadProtectionPolicyRetentionDailyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyRetentionDailyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94d783bf82aad2ef462dada68299fe222a7904b82d30315b789e1adfb2467955)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0fd4a0a2697a57af11dcfd9aefea2de376cb67098e4cb95a99bcdfb807355d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionDaily]:
        return typing.cast(typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionDaily], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionDaily],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc97c56e2097c016c871653834cf0176bec29f56ad2cc5a2d259f780c1b56a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "format_type": "formatType",
        "monthdays": "monthdays",
        "weekdays": "weekdays",
        "weeks": "weeks",
    },
)
class BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly:
    def __init__(
        self,
        *,
        count: jsii.Number,
        format_type: builtins.str,
        monthdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        :param format_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#format_type BackupPolicyVmWorkload#format_type}.
        :param monthdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#monthdays BackupPolicyVmWorkload#monthdays}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weeks BackupPolicyVmWorkload#weeks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a5fa223f67ec71233fa444483153bc6f3d0acf05ccbcd4baeb43cfc812c7169)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument format_type", value=format_type, expected_type=type_hints["format_type"])
            check_type(argname="argument monthdays", value=monthdays, expected_type=type_hints["monthdays"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
            check_type(argname="argument weeks", value=weeks, expected_type=type_hints["weeks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "format_type": format_type,
        }
        if monthdays is not None:
            self._values["monthdays"] = monthdays
        if weekdays is not None:
            self._values["weekdays"] = weekdays
        if weeks is not None:
            self._values["weeks"] = weeks

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def format_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#format_type BackupPolicyVmWorkload#format_type}.'''
        result = self._values.get("format_type")
        assert result is not None, "Required property 'format_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def monthdays(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#monthdays BackupPolicyVmWorkload#monthdays}.'''
        result = self._values.get("monthdays")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weeks BackupPolicyVmWorkload#weeks}.'''
        result = self._values.get("weeks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmWorkloadProtectionPolicyRetentionMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyRetentionMonthlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26c086653673f8a675c5a8521a9c943cf5fcdfb9c42ebc3a1532d51414ab1d00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMonthdays")
    def reset_monthdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthdays", []))

    @jsii.member(jsii_name="resetWeekdays")
    def reset_weekdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekdays", []))

    @jsii.member(jsii_name="resetWeeks")
    def reset_weeks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeks", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="formatTypeInput")
    def format_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="monthdaysInput")
    def monthdays_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "monthdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="weeksInput")
    def weeks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weeksInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130536e1525573a33a13a3a5491ba1f8880e9359293c276c894be3cee6cc0b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatType")
    def format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "formatType"))

    @format_type.setter
    def format_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ac716c9d841d896009abf1a22be14a991c834cb73dffd0ac25aa3a2db2ee0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthdays")
    def monthdays(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "monthdays"))

    @monthdays.setter
    def monthdays(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5ae54a2c2bc9cbdcea55e1a8da4da73375f6ed30d789d5c8f93b14cba85d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df5156ddd8f272dce08253e69e3e989e0f95d35c4699a66b9d754f5f1d7f645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeks")
    def weeks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeks"))

    @weeks.setter
    def weeks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1136c7fe2b0095ed6b3d93263757e8696b1fd8191c8bcee6bcc52d48c4ca7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly]:
        return typing.cast(typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21039742d34a7cd69cc18d064b421c9ee7100557118636ca00b88a08b714e6ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "weekdays": "weekdays"},
)
class BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly:
    def __init__(
        self,
        *,
        count: jsii.Number,
        weekdays: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b4d879b1056ba2c07790e6e21114f07baedbdcfc2e25f6dde3d35cc3f61d964)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "weekdays": weekdays,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def weekdays(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.'''
        result = self._values.get("weekdays")
        assert result is not None, "Required property 'weekdays' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmWorkloadProtectionPolicyRetentionWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyRetentionWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b03a84ea8be045f4d2932437302110dca061e2bf3655a3b505bbacb6d3bb4766)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c40be866b8acdd6c7b9cd9278b0a41398df36be3c026a2340a192053f7d3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996ac27cf9ad26895509f553199231fdcae6172280dcebf37c6c90d561cf7374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly]:
        return typing.cast(typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21df65d91414430cbe480bdaefb34faa7b380351929a2a272e3699d41288c4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyRetentionYearly",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "format_type": "formatType",
        "months": "months",
        "monthdays": "monthdays",
        "weekdays": "weekdays",
        "weeks": "weeks",
    },
)
class BackupPolicyVmWorkloadProtectionPolicyRetentionYearly:
    def __init__(
        self,
        *,
        count: jsii.Number,
        format_type: builtins.str,
        months: typing.Sequence[builtins.str],
        monthdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
        weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
        weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        :param format_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#format_type BackupPolicyVmWorkload#format_type}.
        :param months: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#months BackupPolicyVmWorkload#months}.
        :param monthdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#monthdays BackupPolicyVmWorkload#monthdays}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.
        :param weeks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weeks BackupPolicyVmWorkload#weeks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf261ea98814678e11de7dc24130b2d2d528b760f176bd23dd9e9aecc52e386)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument format_type", value=format_type, expected_type=type_hints["format_type"])
            check_type(argname="argument months", value=months, expected_type=type_hints["months"])
            check_type(argname="argument monthdays", value=monthdays, expected_type=type_hints["monthdays"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
            check_type(argname="argument weeks", value=weeks, expected_type=type_hints["weeks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "format_type": format_type,
            "months": months,
        }
        if monthdays is not None:
            self._values["monthdays"] = monthdays
        if weekdays is not None:
            self._values["weekdays"] = weekdays
        if weeks is not None:
            self._values["weeks"] = weeks

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def format_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#format_type BackupPolicyVmWorkload#format_type}.'''
        result = self._values.get("format_type")
        assert result is not None, "Required property 'format_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def months(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#months BackupPolicyVmWorkload#months}.'''
        result = self._values.get("months")
        assert result is not None, "Required property 'months' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def monthdays(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#monthdays BackupPolicyVmWorkload#monthdays}.'''
        result = self._values.get("monthdays")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weekdays BackupPolicyVmWorkload#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def weeks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#weeks BackupPolicyVmWorkload#weeks}.'''
        result = self._values.get("weeks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadProtectionPolicyRetentionYearly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmWorkloadProtectionPolicyRetentionYearlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicyRetentionYearlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6424c3074ba671cca5c0ba88c1325093fc71e2b81b9db8b6eb78f3496b0828c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMonthdays")
    def reset_monthdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthdays", []))

    @jsii.member(jsii_name="resetWeekdays")
    def reset_weekdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekdays", []))

    @jsii.member(jsii_name="resetWeeks")
    def reset_weeks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeks", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="formatTypeInput")
    def format_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="monthdaysInput")
    def monthdays_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "monthdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="monthsInput")
    def months_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monthsInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="weeksInput")
    def weeks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weeksInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d555b684100e1840ac8f4726ffc2ab6785ad74744e2e67b8bea6dd80e134da66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatType")
    def format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "formatType"))

    @format_type.setter
    def format_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5089b246a6b01a2b6cb8b934c0cf51463c90da5f8040f390a45a74781c974d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthdays")
    def monthdays(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "monthdays"))

    @monthdays.setter
    def monthdays(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557b2d813b258ef79e9a2d91a966b2a20674c94d17f91065678cc1b6be96c1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="months")
    def months(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "months"))

    @months.setter
    def months(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6be9bf0db4fa1a273102f474990241c5bd1aa0e55d9c296fdcdec19f1c2481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "months", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cffad35442cfdb5397ad179afead149e466e572b0f23877b772126488b6baa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeks")
    def weeks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeks"))

    @weeks.setter
    def weeks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805d4858c9563866768c6b5e788b2f75f5fdc0de908511c180a67fd985fe4a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionYearly]:
        return typing.cast(typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionYearly], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionYearly],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624039e17d008ed91cbfdd4671388fbb7f68ab44548a9f83417ecf5e8485f688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicySimpleRetention",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class BackupPolicyVmWorkloadProtectionPolicySimpleRetention:
    def __init__(self, *, count: jsii.Number) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f023ad94764ebc79b78a06a32153723709faf5978b010bc9e9e2735a666096)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#count BackupPolicyVmWorkload#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadProtectionPolicySimpleRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmWorkloadProtectionPolicySimpleRetentionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadProtectionPolicySimpleRetentionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fa227fda373a585787dff78942fe99c4b50e121074ffab84548846c8a5115a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82ce473fa706c6e3e0fdff91732b5dc1eb1e84c9f6347593d0c90e66ba011a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupPolicyVmWorkloadProtectionPolicySimpleRetention]:
        return typing.cast(typing.Optional[BackupPolicyVmWorkloadProtectionPolicySimpleRetention], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicySimpleRetention],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379998e996da04f1f5879b71c2aaea71d407fc12f94a383318d300f5f6a9f91b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadSettings",
    jsii_struct_bases=[],
    name_mapping={
        "time_zone": "timeZone",
        "compression_enabled": "compressionEnabled",
    },
)
class BackupPolicyVmWorkloadSettings:
    def __init__(
        self,
        *,
        time_zone: builtins.str,
        compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#time_zone BackupPolicyVmWorkload#time_zone}.
        :param compression_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#compression_enabled BackupPolicyVmWorkload#compression_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3193d54600e6cea01f045ce71ff324ca54a9e75c249d1cbc8550f42b0912136e)
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument compression_enabled", value=compression_enabled, expected_type=type_hints["compression_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time_zone": time_zone,
        }
        if compression_enabled is not None:
            self._values["compression_enabled"] = compression_enabled

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#time_zone BackupPolicyVmWorkload#time_zone}.'''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compression_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#compression_enabled BackupPolicyVmWorkload#compression_enabled}.'''
        result = self._values.get("compression_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmWorkloadSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a3e811f81c931340226b4c6b8e698a5b1d6d5f64ed9fc3d6a56a0cc055a19f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCompressionEnabled")
    def reset_compression_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="compressionEnabledInput")
    def compression_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "compressionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionEnabled")
    def compression_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "compressionEnabled"))

    @compression_enabled.setter
    def compression_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80cbdb5b56b55875d2492fa653cf683bd0f1ebacc02f104734b314a0a5c17ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3dad6c2763868cea7b3b9eb576c5ff29f5f3c36235502a18a4ffc308d05bec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPolicyVmWorkloadSettings]:
        return typing.cast(typing.Optional[BackupPolicyVmWorkloadSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPolicyVmWorkloadSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15eec151aff06cf8ef2d334fea7931a45fb9b77d3abe50e4a0009bf4872bef00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class BackupPolicyVmWorkloadTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#create BackupPolicyVmWorkload#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#delete BackupPolicyVmWorkload#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#read BackupPolicyVmWorkload#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#update BackupPolicyVmWorkload#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3caff7044dff67d583f1ed4d5a07455d642c33e085a1f33b7241a7cec038016e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#create BackupPolicyVmWorkload#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#delete BackupPolicyVmWorkload#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#read BackupPolicyVmWorkload#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/backup_policy_vm_workload#update BackupPolicyVmWorkload#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPolicyVmWorkloadTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPolicyVmWorkloadTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.backupPolicyVmWorkload.BackupPolicyVmWorkloadTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6926154be7b9ea69cbad39274acdc58fa21beafdcc87b587126929842276cc6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0f380e030f0931c9d5b382ac5cdeb68fd8a7deefdc3772fd086636789ed187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96393dd294a8ac2bdd011d881c47ac7e6c0db19bc252c7889105413d1abe8067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291a9bd4a3acfd4accc47e1896175dd8aec6e24aa1d3a173cb29e3dae24886d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c690c48024d9a79ec058624ee8e71dd4ad089f1b8cdd44cf82b60b59ee3d04f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmWorkloadTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmWorkloadTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmWorkloadTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7108a93f7930c96d7df5b9cc8ed557e770323ff773f4b71dd16840f2623e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BackupPolicyVmWorkload",
    "BackupPolicyVmWorkloadConfig",
    "BackupPolicyVmWorkloadProtectionPolicy",
    "BackupPolicyVmWorkloadProtectionPolicyBackup",
    "BackupPolicyVmWorkloadProtectionPolicyBackupOutputReference",
    "BackupPolicyVmWorkloadProtectionPolicyList",
    "BackupPolicyVmWorkloadProtectionPolicyOutputReference",
    "BackupPolicyVmWorkloadProtectionPolicyRetentionDaily",
    "BackupPolicyVmWorkloadProtectionPolicyRetentionDailyOutputReference",
    "BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly",
    "BackupPolicyVmWorkloadProtectionPolicyRetentionMonthlyOutputReference",
    "BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly",
    "BackupPolicyVmWorkloadProtectionPolicyRetentionWeeklyOutputReference",
    "BackupPolicyVmWorkloadProtectionPolicyRetentionYearly",
    "BackupPolicyVmWorkloadProtectionPolicyRetentionYearlyOutputReference",
    "BackupPolicyVmWorkloadProtectionPolicySimpleRetention",
    "BackupPolicyVmWorkloadProtectionPolicySimpleRetentionOutputReference",
    "BackupPolicyVmWorkloadSettings",
    "BackupPolicyVmWorkloadSettingsOutputReference",
    "BackupPolicyVmWorkloadTimeouts",
    "BackupPolicyVmWorkloadTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a55f9213c4df5bc2da429f2ec189f292b4cbb21d77cb04e457f3a6380a08d469(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    protection_policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPolicyVmWorkloadProtectionPolicy, typing.Dict[builtins.str, typing.Any]]]],
    recovery_vault_name: builtins.str,
    resource_group_name: builtins.str,
    settings: typing.Union[BackupPolicyVmWorkloadSettings, typing.Dict[builtins.str, typing.Any]],
    workload_type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BackupPolicyVmWorkloadTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d15d0bf086a69a16d49b5662fbf9b82131861f096c6b7b6db7d697556329daf6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e8808733f9bf907e7014f4ba091afb69aa3e5c310097bdc12c597f69eb7b39(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPolicyVmWorkloadProtectionPolicy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323eb0bc5f7b12fa978070efabd83dbc921e6df217e67f91e760e3133bac690e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73272f7e53d6210a6d2baf625768fe7b8b19d9f776f7b0089a4f7a5680e217aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bf92728588c2574d24b7cd451bb9b62097a6b41ec4f1d341e77cb1b5255c53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60d8c5b149a1e453bac162d6528a2db3aac40352359336fa765d95275ec876c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7f3de1af0d0f59baa857141b00ac6910c999d3db7ad35d067a5fa062710b86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da657c8ac3fd2c47c0f8c0ab4b8606876977726ac4c8644e48f9cd7fb622f9be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    protection_policy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPolicyVmWorkloadProtectionPolicy, typing.Dict[builtins.str, typing.Any]]]],
    recovery_vault_name: builtins.str,
    resource_group_name: builtins.str,
    settings: typing.Union[BackupPolicyVmWorkloadSettings, typing.Dict[builtins.str, typing.Any]],
    workload_type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BackupPolicyVmWorkloadTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4abb190e8b10e5d71e484af4cf0c46cc62c91ae5b10007d7d8e50d77ae22fc7(
    *,
    backup: typing.Union[BackupPolicyVmWorkloadProtectionPolicyBackup, typing.Dict[builtins.str, typing.Any]],
    policy_type: builtins.str,
    retention_daily: typing.Optional[typing.Union[BackupPolicyVmWorkloadProtectionPolicyRetentionDaily, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_monthly: typing.Optional[typing.Union[BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_weekly: typing.Optional[typing.Union[BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_yearly: typing.Optional[typing.Union[BackupPolicyVmWorkloadProtectionPolicyRetentionYearly, typing.Dict[builtins.str, typing.Any]]] = None,
    simple_retention: typing.Optional[typing.Union[BackupPolicyVmWorkloadProtectionPolicySimpleRetention, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa882f9cadcf2f643ced5afd2d92aea2d0a5311c01476397ba58e5563146382(
    *,
    frequency: typing.Optional[builtins.str] = None,
    frequency_in_minutes: typing.Optional[jsii.Number] = None,
    time: typing.Optional[builtins.str] = None,
    weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546e8792820527177308d925580f6ce1357c0482007be6e9e8904fd55ef6eba1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f69697efb7a2d5338fffa93f101b770fd8a9a8f608dcfa7bb0c676425b9ee4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c67c1ddf9f2bfc1c5a963d1aa18d713bf461398220ce847cc882e0f47ae3b65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6beb867630e51e808f2b5ada5bcb787841657f29020373506348af96cc9c541f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a6188609e180441611eb84968e345bdbcf39f51475a3618e13e96145cd0a60(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93622603d7279f2197be861310837b22a4f2c46d1eb597ed6c8726d300666207(
    value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55b0a142d4caab01f7aa5da8f518fb2155b5105937ad534a88b1797d50336aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6342a2990a3af9fa26566885d18b9ca7e0dbbc982b4e3823f4be3b0e7edd7fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759646d48f5661a61696505bbc6e6922aeff44cc945e2d760b741a5dc4fb4e5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f10f409b7a627dbd23bbcd5044692bd1bcdadae974ec4931470bac5cb8c9574(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b2c03811dbda4819f22a95d0982f817d8a78a1f70f861cb462dada2d0bbc8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792a035c303c5578549baabe747633b0987b46b69dd3f211584a156b9ff9483d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPolicyVmWorkloadProtectionPolicy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08336f59053abeeb04aa23b9be58a5881486d9bb8fdd17b007fccccae49abd84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547b47ac4b3f3bf45392093d9f7e7299762bd7b79780013172b3a17bdc3a2d47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389721ec0ebadbc816c9c6eea3f672c8d1e36a53e041436314d5c9e8cf97b397(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmWorkloadProtectionPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b8358e3ba0d9a525430343d2bc2ed1c6437cc0e2af40ea27051597f10e3068(
    *,
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d783bf82aad2ef462dada68299fe222a7904b82d30315b789e1adfb2467955(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0fd4a0a2697a57af11dcfd9aefea2de376cb67098e4cb95a99bcdfb807355d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc97c56e2097c016c871653834cf0176bec29f56ad2cc5a2d259f780c1b56a4b(
    value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionDaily],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5fa223f67ec71233fa444483153bc6f3d0acf05ccbcd4baeb43cfc812c7169(
    *,
    count: jsii.Number,
    format_type: builtins.str,
    monthdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
    weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c086653673f8a675c5a8521a9c943cf5fcdfb9c42ebc3a1532d51414ab1d00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130536e1525573a33a13a3a5491ba1f8880e9359293c276c894be3cee6cc0b67(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ac716c9d841d896009abf1a22be14a991c834cb73dffd0ac25aa3a2db2ee0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5ae54a2c2bc9cbdcea55e1a8da4da73375f6ed30d789d5c8f93b14cba85d34(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df5156ddd8f272dce08253e69e3e989e0f95d35c4699a66b9d754f5f1d7f645(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1136c7fe2b0095ed6b3d93263757e8696b1fd8191c8bcee6bcc52d48c4ca7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21039742d34a7cd69cc18d064b421c9ee7100557118636ca00b88a08b714e6ff(
    value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionMonthly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4d879b1056ba2c07790e6e21114f07baedbdcfc2e25f6dde3d35cc3f61d964(
    *,
    count: jsii.Number,
    weekdays: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03a84ea8be045f4d2932437302110dca061e2bf3655a3b505bbacb6d3bb4766(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c40be866b8acdd6c7b9cd9278b0a41398df36be3c026a2340a192053f7d3f6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996ac27cf9ad26895509f553199231fdcae6172280dcebf37c6c90d561cf7374(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21df65d91414430cbe480bdaefb34faa7b380351929a2a272e3699d41288c4be(
    value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionWeekly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf261ea98814678e11de7dc24130b2d2d528b760f176bd23dd9e9aecc52e386(
    *,
    count: jsii.Number,
    format_type: builtins.str,
    months: typing.Sequence[builtins.str],
    monthdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
    weekdays: typing.Optional[typing.Sequence[builtins.str]] = None,
    weeks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6424c3074ba671cca5c0ba88c1325093fc71e2b81b9db8b6eb78f3496b0828c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d555b684100e1840ac8f4726ffc2ab6785ad74744e2e67b8bea6dd80e134da66(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5089b246a6b01a2b6cb8b934c0cf51463c90da5f8040f390a45a74781c974d50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557b2d813b258ef79e9a2d91a966b2a20674c94d17f91065678cc1b6be96c1aa(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6be9bf0db4fa1a273102f474990241c5bd1aa0e55d9c296fdcdec19f1c2481(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cffad35442cfdb5397ad179afead149e466e572b0f23877b772126488b6baa4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805d4858c9563866768c6b5e788b2f75f5fdc0de908511c180a67fd985fe4a40(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624039e17d008ed91cbfdd4671388fbb7f68ab44548a9f83417ecf5e8485f688(
    value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicyRetentionYearly],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f023ad94764ebc79b78a06a32153723709faf5978b010bc9e9e2735a666096(
    *,
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa227fda373a585787dff78942fe99c4b50e121074ffab84548846c8a5115a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82ce473fa706c6e3e0fdff91732b5dc1eb1e84c9f6347593d0c90e66ba011a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379998e996da04f1f5879b71c2aaea71d407fc12f94a383318d300f5f6a9f91b(
    value: typing.Optional[BackupPolicyVmWorkloadProtectionPolicySimpleRetention],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3193d54600e6cea01f045ce71ff324ca54a9e75c249d1cbc8550f42b0912136e(
    *,
    time_zone: builtins.str,
    compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3e811f81c931340226b4c6b8e698a5b1d6d5f64ed9fc3d6a56a0cc055a19f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cbdb5b56b55875d2492fa653cf683bd0f1ebacc02f104734b314a0a5c17ea7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dad6c2763868cea7b3b9eb576c5ff29f5f3c36235502a18a4ffc308d05bec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15eec151aff06cf8ef2d334fea7931a45fb9b77d3abe50e4a0009bf4872bef00(
    value: typing.Optional[BackupPolicyVmWorkloadSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caff7044dff67d583f1ed4d5a07455d642c33e085a1f33b7241a7cec038016e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6926154be7b9ea69cbad39274acdc58fa21beafdcc87b587126929842276cc6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0f380e030f0931c9d5b382ac5cdeb68fd8a7deefdc3772fd086636789ed187(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96393dd294a8ac2bdd011d881c47ac7e6c0db19bc252c7889105413d1abe8067(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291a9bd4a3acfd4accc47e1896175dd8aec6e24aa1d3a173cb29e3dae24886d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c690c48024d9a79ec058624ee8e71dd4ad089f1b8cdd44cf82b60b59ee3d04f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7108a93f7930c96d7df5b9cc8ed557e770323ff773f4b71dd16840f2623e48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPolicyVmWorkloadTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
