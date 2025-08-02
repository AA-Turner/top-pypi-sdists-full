r'''
# `opentelekomcloud_csbs_backup_policy_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_csbs_backup_policy_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1).
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


class CsbsBackupPolicyV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1 opentelekomcloud_csbs_backup_policy_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[builtins.str, typing.Any]]]],
        scheduled_operation: typing.Union["CsbsBackupPolicyV1ScheduledOperation", typing.Dict[builtins.str, typing.Any]],
        common: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        provider_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CsbsBackupPolicyV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1 opentelekomcloud_csbs_backup_policy_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param resource: resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#resource CsbsBackupPolicyV1#resource}
        :param scheduled_operation: scheduled_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#scheduled_operation CsbsBackupPolicyV1#scheduled_operation}
        :param common: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#common CsbsBackupPolicyV1#common}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param provider_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#provider_id CsbsBackupPolicyV1#provider_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#region CsbsBackupPolicyV1#region}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#tags CsbsBackupPolicyV1#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#timeouts CsbsBackupPolicyV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2176930865d48c19e8e76d405878141891a773a4381b5c194e2178c3f2a9123f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CsbsBackupPolicyV1Config(
            name=name,
            resource=resource,
            scheduled_operation=scheduled_operation,
            common=common,
            description=description,
            id=id,
            provider_id=provider_id,
            region=region,
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
        '''Generates CDKTF code for importing a CsbsBackupPolicyV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CsbsBackupPolicyV1 to import.
        :param import_from_id: The id of the existing CsbsBackupPolicyV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CsbsBackupPolicyV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9aaeb35b9886f9d8b78fd71b62bcfc4ddb8bd681a06962c80012c6c8bc5852)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putResource")
    def put_resource(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec81385c7df0b75378a88f6eea88ac5892aa6a0d3ddd2dd5c6c2c0c52eba9630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResource", [value]))

    @jsii.member(jsii_name="putScheduledOperation")
    def put_scheduled_operation(
        self,
        *,
        operation_type: builtins.str,
        trigger_pattern: builtins.str,
        day_backups: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_backups: typing.Optional[jsii.Number] = None,
        month_backups: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        permanent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_duration_days: typing.Optional[jsii.Number] = None,
        timezone: typing.Optional[builtins.str] = None,
        week_backups: typing.Optional[jsii.Number] = None,
        year_backups: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#operation_type CsbsBackupPolicyV1#operation_type}.
        :param trigger_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#trigger_pattern CsbsBackupPolicyV1#trigger_pattern}.
        :param day_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#day_backups CsbsBackupPolicyV1#day_backups}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#enabled CsbsBackupPolicyV1#enabled}.
        :param max_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#max_backups CsbsBackupPolicyV1#max_backups}.
        :param month_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#month_backups CsbsBackupPolicyV1#month_backups}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param permanent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#permanent CsbsBackupPolicyV1#permanent}.
        :param retention_duration_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#retention_duration_days CsbsBackupPolicyV1#retention_duration_days}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#timezone CsbsBackupPolicyV1#timezone}.
        :param week_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#week_backups CsbsBackupPolicyV1#week_backups}.
        :param year_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#year_backups CsbsBackupPolicyV1#year_backups}.
        '''
        value = CsbsBackupPolicyV1ScheduledOperation(
            operation_type=operation_type,
            trigger_pattern=trigger_pattern,
            day_backups=day_backups,
            description=description,
            enabled=enabled,
            max_backups=max_backups,
            month_backups=month_backups,
            name=name,
            permanent=permanent,
            retention_duration_days=retention_duration_days,
            timezone=timezone,
            week_backups=week_backups,
            year_backups=year_backups,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduledOperation", [value]))

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d8162d60b26177b66826cf7908bb95c9ebd81a52edfad209f5dd91402aac53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#create CsbsBackupPolicyV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#delete CsbsBackupPolicyV1#delete}.
        '''
        value = CsbsBackupPolicyV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCommon")
    def reset_common(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommon", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProviderId")
    def reset_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> "CsbsBackupPolicyV1ResourceList":
        return typing.cast("CsbsBackupPolicyV1ResourceList", jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="scheduledOperation")
    def scheduled_operation(
        self,
    ) -> "CsbsBackupPolicyV1ScheduledOperationOutputReference":
        return typing.cast("CsbsBackupPolicyV1ScheduledOperationOutputReference", jsii.get(self, "scheduledOperation"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "CsbsBackupPolicyV1TagsList":
        return typing.cast("CsbsBackupPolicyV1TagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CsbsBackupPolicyV1TimeoutsOutputReference":
        return typing.cast("CsbsBackupPolicyV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="commonInput")
    def common_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "commonInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerIdInput")
    def provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsbsBackupPolicyV1Resource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsbsBackupPolicyV1Resource"]]], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledOperationInput")
    def scheduled_operation_input(
        self,
    ) -> typing.Optional["CsbsBackupPolicyV1ScheduledOperation"]:
        return typing.cast(typing.Optional["CsbsBackupPolicyV1ScheduledOperation"], jsii.get(self, "scheduledOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsbsBackupPolicyV1Tags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsbsBackupPolicyV1Tags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CsbsBackupPolicyV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CsbsBackupPolicyV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="common")
    def common(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "common"))

    @common.setter
    def common(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6187949e0776e747159311d574c409e88fef3838e2075e54d12b3f091944cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "common", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40cdca7d7dbbad31dfe6bf10744d583201627e147ed1f10ddd73a8677caf5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775dda0af18955d991c6d6faf91bd7f0b664251bead6e8742203a7834f902d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71092525a8f33a0abd8c91ab8bdd1cb13a8790c032fbd6e8bda10245a1629523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @provider_id.setter
    def provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a49eda6f93370cd1e27e9fce63d85f361d8646fd99ac4c58f9434934d295e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c398479c846da95977cf9819bedaa3b20746dd4109c4a28db1e8cd65710020b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1Config",
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
        "resource": "resource",
        "scheduled_operation": "scheduledOperation",
        "common": "common",
        "description": "description",
        "id": "id",
        "provider_id": "providerId",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class CsbsBackupPolicyV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        resource: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Resource", typing.Dict[builtins.str, typing.Any]]]],
        scheduled_operation: typing.Union["CsbsBackupPolicyV1ScheduledOperation", typing.Dict[builtins.str, typing.Any]],
        common: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        provider_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CsbsBackupPolicyV1Tags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CsbsBackupPolicyV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param resource: resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#resource CsbsBackupPolicyV1#resource}
        :param scheduled_operation: scheduled_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#scheduled_operation CsbsBackupPolicyV1#scheduled_operation}
        :param common: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#common CsbsBackupPolicyV1#common}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param provider_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#provider_id CsbsBackupPolicyV1#provider_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#region CsbsBackupPolicyV1#region}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#tags CsbsBackupPolicyV1#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#timeouts CsbsBackupPolicyV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scheduled_operation, dict):
            scheduled_operation = CsbsBackupPolicyV1ScheduledOperation(**scheduled_operation)
        if isinstance(timeouts, dict):
            timeouts = CsbsBackupPolicyV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0901e5bfed5a38c228881121f7070ded4692e6d3c6a5a26d04a6afa5fa5dcac1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument scheduled_operation", value=scheduled_operation, expected_type=type_hints["scheduled_operation"])
            check_type(argname="argument common", value=common, expected_type=type_hints["common"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument provider_id", value=provider_id, expected_type=type_hints["provider_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource": resource,
            "scheduled_operation": scheduled_operation,
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
        if common is not None:
            self._values["common"] = common
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if provider_id is not None:
            self._values["provider_id"] = provider_id
        if region is not None:
            self._values["region"] = region
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsbsBackupPolicyV1Resource"]]:
        '''resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#resource CsbsBackupPolicyV1#resource}
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsbsBackupPolicyV1Resource"]], result)

    @builtins.property
    def scheduled_operation(self) -> "CsbsBackupPolicyV1ScheduledOperation":
        '''scheduled_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#scheduled_operation CsbsBackupPolicyV1#scheduled_operation}
        '''
        result = self._values.get("scheduled_operation")
        assert result is not None, "Required property 'scheduled_operation' is missing"
        return typing.cast("CsbsBackupPolicyV1ScheduledOperation", result)

    @builtins.property
    def common(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#common CsbsBackupPolicyV1#common}.'''
        result = self._values.get("common")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#provider_id CsbsBackupPolicyV1#provider_id}.'''
        result = self._values.get("provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#region CsbsBackupPolicyV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsbsBackupPolicyV1Tags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#tags CsbsBackupPolicyV1#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsbsBackupPolicyV1Tags"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CsbsBackupPolicyV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#timeouts CsbsBackupPolicyV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CsbsBackupPolicyV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1Resource",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name", "type": "type"},
)
class CsbsBackupPolicyV1Resource:
    def __init__(
        self,
        *,
        id: builtins.str,
        name: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#type CsbsBackupPolicyV1#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79470287a3674d6d7e7e5f45851b41a47b64c9311da2ad397964ff9e527c27cc)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "name": name,
            "type": type,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#id CsbsBackupPolicyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#type CsbsBackupPolicyV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1Resource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsbsBackupPolicyV1ResourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1ResourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__929fe78f286c7f6cc7f736ffab03a6e46f48fc4e479fbc6ef6836a90f2b2c6ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CsbsBackupPolicyV1ResourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381b154c4371061bf5ac9c0e48fa0480435abeb54bb32ed60e791ca95957453e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CsbsBackupPolicyV1ResourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08322041a4b49d19084c3ba7eed15ff1246cc18b12518526f662319756bab436)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b49f85b0eb9cfa046e300b1402abe5003cb924315a6dcfd92053b8d9d6122bbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29e19862bc06e214686b866978a5d5974a850ebc75f36991fc13d21688c2ed3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsbsBackupPolicyV1Resource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsbsBackupPolicyV1Resource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsbsBackupPolicyV1Resource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5eca2cfb6a2cb9309e26718496d4aa0f5f9cae88222aa2c97b8a3d7a26003b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CsbsBackupPolicyV1ResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1ResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__941ef7efb4d7eee9c4a80abfd13ef107b7bee55f24b2a900d8d61b390ff90291)
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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc7cf51879cf1bd3530922680c2b4fc003774f197d7419e2c7dd8240b0d6948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc1973d72c1339000c46f4b1cbda7f749cee309d944fc23466edd5d143b264e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0653981282f2ac7ef4443479e48087787bcb502125ac46e81a0150dd6a85d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Resource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Resource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Resource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f5d8beb7d84b436633beaddcfa0f83b13233c96b1c4f7cf31d3501215fd659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1ScheduledOperation",
    jsii_struct_bases=[],
    name_mapping={
        "operation_type": "operationType",
        "trigger_pattern": "triggerPattern",
        "day_backups": "dayBackups",
        "description": "description",
        "enabled": "enabled",
        "max_backups": "maxBackups",
        "month_backups": "monthBackups",
        "name": "name",
        "permanent": "permanent",
        "retention_duration_days": "retentionDurationDays",
        "timezone": "timezone",
        "week_backups": "weekBackups",
        "year_backups": "yearBackups",
    },
)
class CsbsBackupPolicyV1ScheduledOperation:
    def __init__(
        self,
        *,
        operation_type: builtins.str,
        trigger_pattern: builtins.str,
        day_backups: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_backups: typing.Optional[jsii.Number] = None,
        month_backups: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        permanent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_duration_days: typing.Optional[jsii.Number] = None,
        timezone: typing.Optional[builtins.str] = None,
        week_backups: typing.Optional[jsii.Number] = None,
        year_backups: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#operation_type CsbsBackupPolicyV1#operation_type}.
        :param trigger_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#trigger_pattern CsbsBackupPolicyV1#trigger_pattern}.
        :param day_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#day_backups CsbsBackupPolicyV1#day_backups}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#enabled CsbsBackupPolicyV1#enabled}.
        :param max_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#max_backups CsbsBackupPolicyV1#max_backups}.
        :param month_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#month_backups CsbsBackupPolicyV1#month_backups}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.
        :param permanent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#permanent CsbsBackupPolicyV1#permanent}.
        :param retention_duration_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#retention_duration_days CsbsBackupPolicyV1#retention_duration_days}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#timezone CsbsBackupPolicyV1#timezone}.
        :param week_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#week_backups CsbsBackupPolicyV1#week_backups}.
        :param year_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#year_backups CsbsBackupPolicyV1#year_backups}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cebe4836951c2306532358871cc303cfd0088a4a67e78ae14ec259d67da534)
            check_type(argname="argument operation_type", value=operation_type, expected_type=type_hints["operation_type"])
            check_type(argname="argument trigger_pattern", value=trigger_pattern, expected_type=type_hints["trigger_pattern"])
            check_type(argname="argument day_backups", value=day_backups, expected_type=type_hints["day_backups"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_backups", value=max_backups, expected_type=type_hints["max_backups"])
            check_type(argname="argument month_backups", value=month_backups, expected_type=type_hints["month_backups"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permanent", value=permanent, expected_type=type_hints["permanent"])
            check_type(argname="argument retention_duration_days", value=retention_duration_days, expected_type=type_hints["retention_duration_days"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument week_backups", value=week_backups, expected_type=type_hints["week_backups"])
            check_type(argname="argument year_backups", value=year_backups, expected_type=type_hints["year_backups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operation_type": operation_type,
            "trigger_pattern": trigger_pattern,
        }
        if day_backups is not None:
            self._values["day_backups"] = day_backups
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_backups is not None:
            self._values["max_backups"] = max_backups
        if month_backups is not None:
            self._values["month_backups"] = month_backups
        if name is not None:
            self._values["name"] = name
        if permanent is not None:
            self._values["permanent"] = permanent
        if retention_duration_days is not None:
            self._values["retention_duration_days"] = retention_duration_days
        if timezone is not None:
            self._values["timezone"] = timezone
        if week_backups is not None:
            self._values["week_backups"] = week_backups
        if year_backups is not None:
            self._values["year_backups"] = year_backups

    @builtins.property
    def operation_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#operation_type CsbsBackupPolicyV1#operation_type}.'''
        result = self._values.get("operation_type")
        assert result is not None, "Required property 'operation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#trigger_pattern CsbsBackupPolicyV1#trigger_pattern}.'''
        result = self._values.get("trigger_pattern")
        assert result is not None, "Required property 'trigger_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def day_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#day_backups CsbsBackupPolicyV1#day_backups}.'''
        result = self._values.get("day_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#description CsbsBackupPolicyV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#enabled CsbsBackupPolicyV1#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#max_backups CsbsBackupPolicyV1#max_backups}.'''
        result = self._values.get("max_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#month_backups CsbsBackupPolicyV1#month_backups}.'''
        result = self._values.get("month_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#name CsbsBackupPolicyV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permanent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#permanent CsbsBackupPolicyV1#permanent}.'''
        result = self._values.get("permanent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_duration_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#retention_duration_days CsbsBackupPolicyV1#retention_duration_days}.'''
        result = self._values.get("retention_duration_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#timezone CsbsBackupPolicyV1#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#week_backups CsbsBackupPolicyV1#week_backups}.'''
        result = self._values.get("week_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year_backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#year_backups CsbsBackupPolicyV1#year_backups}.'''
        result = self._values.get("year_backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1ScheduledOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsbsBackupPolicyV1ScheduledOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1ScheduledOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97f89e72d723f29cf4ee31f50ba3bcdf90ea64de03fd333d7b88a12ad6d96170)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDayBackups")
    def reset_day_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayBackups", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMaxBackups")
    def reset_max_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBackups", []))

    @jsii.member(jsii_name="resetMonthBackups")
    def reset_month_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthBackups", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPermanent")
    def reset_permanent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermanent", []))

    @jsii.member(jsii_name="resetRetentionDurationDays")
    def reset_retention_duration_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDurationDays", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @jsii.member(jsii_name="resetWeekBackups")
    def reset_week_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekBackups", []))

    @jsii.member(jsii_name="resetYearBackups")
    def reset_year_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYearBackups", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="triggerId")
    def trigger_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerId"))

    @builtins.property
    @jsii.member(jsii_name="triggerName")
    def trigger_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerName"))

    @builtins.property
    @jsii.member(jsii_name="triggerType")
    def trigger_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerType"))

    @builtins.property
    @jsii.member(jsii_name="dayBackupsInput")
    def day_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBackupsInput")
    def max_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="monthBackupsInput")
    def month_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="operationTypeInput")
    def operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="permanentInput")
    def permanent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permanentInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDurationDaysInput")
    def retention_duration_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDurationDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerPatternInput")
    def trigger_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="weekBackupsInput")
    def week_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="yearBackupsInput")
    def year_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="dayBackups")
    def day_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dayBackups"))

    @day_backups.setter
    def day_backups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a3ccc1f0c2e1416217f3c0f4937f54398ea407605e6900681cf0d8d1730ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f894a778b022a6d1e5fb07340e0575f4c00e58fbc0fe7ad7a8807bf6972e6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87dd4b0423a4cdfe987ff94a0d3ebbf0a70f2cfefdc25cd9cf849429eb907b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBackups")
    def max_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBackups"))

    @max_backups.setter
    def max_backups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a3a02d4741da71eebbdc6b6e8f93d4df56672b7cf4d10833bcef7d50415e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthBackups")
    def month_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthBackups"))

    @month_backups.setter
    def month_backups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41eaff5a3a64d7de2b1009c8247bc21c1713cde39ad47f811f1ddae321c3f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e26bedb2e2fcdd7a16c7859401ec729a3d61afc29d5013ccf01b944a8e32ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationType")
    def operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationType"))

    @operation_type.setter
    def operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f372cb8aa31e0ba4016af8cad5a775eede826ec042bb86e5cf55cb1fe16e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permanent")
    def permanent(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permanent"))

    @permanent.setter
    def permanent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f9ec7ad1c743155445702ddd05b624a60dee3b912e864f2afc730ea082e8c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionDurationDays")
    def retention_duration_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDurationDays"))

    @retention_duration_days.setter
    def retention_duration_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a6fdab1e80c7e271096151e43cb1c3933b81e271729c1528dc41c52281fbcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDurationDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4881383d20fa423d8fe80987aa2df109516a38fc69d1ff1f455dc50a7f48778f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerPattern")
    def trigger_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerPattern"))

    @trigger_pattern.setter
    def trigger_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5210a9bf628931d6302bb36cba551237a6e4bf68678570a778787c51517a8ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekBackups")
    def week_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekBackups"))

    @week_backups.setter
    def week_backups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db1998378568a9e4a899084ca9b6d946721c570b18995adfdab9c423097f83d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="yearBackups")
    def year_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "yearBackups"))

    @year_backups.setter
    def year_backups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7d8e48a708fde8cbb66bdbe3f22f6428c22f7f8e7f2f0e1912a128a7adb6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "yearBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CsbsBackupPolicyV1ScheduledOperation]:
        return typing.cast(typing.Optional[CsbsBackupPolicyV1ScheduledOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CsbsBackupPolicyV1ScheduledOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cd2bce04515bb1b11f7889cafbf7f19a492e68d9253dcd57b47835c7ced2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1Tags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class CsbsBackupPolicyV1Tags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#key CsbsBackupPolicyV1#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#value CsbsBackupPolicyV1#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571d61a1948a956422fce5ef7b8f5a7616b7e7f7c8f3fdeade9fe2a79a9e21ae)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#key CsbsBackupPolicyV1#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#value CsbsBackupPolicyV1#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1Tags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsbsBackupPolicyV1TagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1TagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6561977600fa8e3142dcc4ce15fcf6d285108910c63e3445a21538f8c295c9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CsbsBackupPolicyV1TagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b4b652d7a5fe812b29c0038ed532fbfa09ad27ac8f1c1404f973e72b3108c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CsbsBackupPolicyV1TagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa8ade08190036491e6d75c642014e7feb886ad3493c8738edb740e9a268d7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebf5834e8a2538aef31872680be3909ae2a6c7167964ba2f971159e7afdf0fe9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__523abd2d8c7aa90abdd611e062af102cc23b348278561028141c39f783e9f19c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsbsBackupPolicyV1Tags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsbsBackupPolicyV1Tags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsbsBackupPolicyV1Tags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10c0c713527352e275bcfe37023fd19f7212a5601f12ff0cca5e39f38b9e985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CsbsBackupPolicyV1TagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1TagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__570767b6ae7ccb5d987d3a13a259272f432ccf3dd5e75e96bc1f5b6d09e4362d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b31ad72e5a70416bc8609a1ffaf843342206b0928b8dc525e6e94a042dcce27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe6f0dd2d1df14c38aafd2e58a04461c27e95af11ebe7b61fa049d8849a3356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Tags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Tags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Tags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740c07a3684f805218eba13d1f48dd511fc64ff7dd76b0e6b373d1375714c55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CsbsBackupPolicyV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#create CsbsBackupPolicyV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#delete CsbsBackupPolicyV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383415edb0be9c3c322289fb1d04b1e14b72178dc510f2d096df41d0cab6fd19)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#create CsbsBackupPolicyV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/csbs_backup_policy_v1#delete CsbsBackupPolicyV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsbsBackupPolicyV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsbsBackupPolicyV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.csbsBackupPolicyV1.CsbsBackupPolicyV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7cd83a0c556859f95121bc939b3ebb3a20a3eaa67a4224f53d4fab44f9ab2bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c8ce21687ae1c264e9d1b8955771a3f7cdb94271ef86ea6b4704eb74f86d260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035821225d29cc93736f3f636ed08aef60d248cec486c334ae8554a5f2900bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318ad84b0056b1c2e4c776bc0f16ffb55f00e0b18ef6150672a036545a9f0dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CsbsBackupPolicyV1",
    "CsbsBackupPolicyV1Config",
    "CsbsBackupPolicyV1Resource",
    "CsbsBackupPolicyV1ResourceList",
    "CsbsBackupPolicyV1ResourceOutputReference",
    "CsbsBackupPolicyV1ScheduledOperation",
    "CsbsBackupPolicyV1ScheduledOperationOutputReference",
    "CsbsBackupPolicyV1Tags",
    "CsbsBackupPolicyV1TagsList",
    "CsbsBackupPolicyV1TagsOutputReference",
    "CsbsBackupPolicyV1Timeouts",
    "CsbsBackupPolicyV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2176930865d48c19e8e76d405878141891a773a4381b5c194e2178c3f2a9123f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    resource: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsbsBackupPolicyV1Resource, typing.Dict[builtins.str, typing.Any]]]],
    scheduled_operation: typing.Union[CsbsBackupPolicyV1ScheduledOperation, typing.Dict[builtins.str, typing.Any]],
    common: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    provider_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsbsBackupPolicyV1Tags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CsbsBackupPolicyV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ae9aaeb35b9886f9d8b78fd71b62bcfc4ddb8bd681a06962c80012c6c8bc5852(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec81385c7df0b75378a88f6eea88ac5892aa6a0d3ddd2dd5c6c2c0c52eba9630(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsbsBackupPolicyV1Resource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d8162d60b26177b66826cf7908bb95c9ebd81a52edfad209f5dd91402aac53(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsbsBackupPolicyV1Tags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6187949e0776e747159311d574c409e88fef3838e2075e54d12b3f091944cb4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40cdca7d7dbbad31dfe6bf10744d583201627e147ed1f10ddd73a8677caf5fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775dda0af18955d991c6d6faf91bd7f0b664251bead6e8742203a7834f902d4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71092525a8f33a0abd8c91ab8bdd1cb13a8790c032fbd6e8bda10245a1629523(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a49eda6f93370cd1e27e9fce63d85f361d8646fd99ac4c58f9434934d295e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c398479c846da95977cf9819bedaa3b20746dd4109c4a28db1e8cd65710020b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0901e5bfed5a38c228881121f7070ded4692e6d3c6a5a26d04a6afa5fa5dcac1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    resource: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsbsBackupPolicyV1Resource, typing.Dict[builtins.str, typing.Any]]]],
    scheduled_operation: typing.Union[CsbsBackupPolicyV1ScheduledOperation, typing.Dict[builtins.str, typing.Any]],
    common: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    provider_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsbsBackupPolicyV1Tags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CsbsBackupPolicyV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79470287a3674d6d7e7e5f45851b41a47b64c9311da2ad397964ff9e527c27cc(
    *,
    id: builtins.str,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929fe78f286c7f6cc7f736ffab03a6e46f48fc4e479fbc6ef6836a90f2b2c6ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381b154c4371061bf5ac9c0e48fa0480435abeb54bb32ed60e791ca95957453e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08322041a4b49d19084c3ba7eed15ff1246cc18b12518526f662319756bab436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49f85b0eb9cfa046e300b1402abe5003cb924315a6dcfd92053b8d9d6122bbb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e19862bc06e214686b866978a5d5974a850ebc75f36991fc13d21688c2ed3c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5eca2cfb6a2cb9309e26718496d4aa0f5f9cae88222aa2c97b8a3d7a26003b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsbsBackupPolicyV1Resource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941ef7efb4d7eee9c4a80abfd13ef107b7bee55f24b2a900d8d61b390ff90291(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc7cf51879cf1bd3530922680c2b4fc003774f197d7419e2c7dd8240b0d6948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc1973d72c1339000c46f4b1cbda7f749cee309d944fc23466edd5d143b264e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0653981282f2ac7ef4443479e48087787bcb502125ac46e81a0150dd6a85d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f5d8beb7d84b436633beaddcfa0f83b13233c96b1c4f7cf31d3501215fd659(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Resource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cebe4836951c2306532358871cc303cfd0088a4a67e78ae14ec259d67da534(
    *,
    operation_type: builtins.str,
    trigger_pattern: builtins.str,
    day_backups: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_backups: typing.Optional[jsii.Number] = None,
    month_backups: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    permanent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_duration_days: typing.Optional[jsii.Number] = None,
    timezone: typing.Optional[builtins.str] = None,
    week_backups: typing.Optional[jsii.Number] = None,
    year_backups: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f89e72d723f29cf4ee31f50ba3bcdf90ea64de03fd333d7b88a12ad6d96170(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a3ccc1f0c2e1416217f3c0f4937f54398ea407605e6900681cf0d8d1730ab3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f894a778b022a6d1e5fb07340e0575f4c00e58fbc0fe7ad7a8807bf6972e6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87dd4b0423a4cdfe987ff94a0d3ebbf0a70f2cfefdc25cd9cf849429eb907b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a3a02d4741da71eebbdc6b6e8f93d4df56672b7cf4d10833bcef7d50415e86(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41eaff5a3a64d7de2b1009c8247bc21c1713cde39ad47f811f1ddae321c3f6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e26bedb2e2fcdd7a16c7859401ec729a3d61afc29d5013ccf01b944a8e32ae1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f372cb8aa31e0ba4016af8cad5a775eede826ec042bb86e5cf55cb1fe16e2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f9ec7ad1c743155445702ddd05b624a60dee3b912e864f2afc730ea082e8c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a6fdab1e80c7e271096151e43cb1c3933b81e271729c1528dc41c52281fbcc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4881383d20fa423d8fe80987aa2df109516a38fc69d1ff1f455dc50a7f48778f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5210a9bf628931d6302bb36cba551237a6e4bf68678570a778787c51517a8ddb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db1998378568a9e4a899084ca9b6d946721c570b18995adfdab9c423097f83d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7d8e48a708fde8cbb66bdbe3f22f6428c22f7f8e7f2f0e1912a128a7adb6df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cd2bce04515bb1b11f7889cafbf7f19a492e68d9253dcd57b47835c7ced2f6(
    value: typing.Optional[CsbsBackupPolicyV1ScheduledOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571d61a1948a956422fce5ef7b8f5a7616b7e7f7c8f3fdeade9fe2a79a9e21ae(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6561977600fa8e3142dcc4ce15fcf6d285108910c63e3445a21538f8c295c9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b4b652d7a5fe812b29c0038ed532fbfa09ad27ac8f1c1404f973e72b3108c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa8ade08190036491e6d75c642014e7feb886ad3493c8738edb740e9a268d7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf5834e8a2538aef31872680be3909ae2a6c7167964ba2f971159e7afdf0fe9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523abd2d8c7aa90abdd611e062af102cc23b348278561028141c39f783e9f19c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10c0c713527352e275bcfe37023fd19f7212a5601f12ff0cca5e39f38b9e985(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsbsBackupPolicyV1Tags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570767b6ae7ccb5d987d3a13a259272f432ccf3dd5e75e96bc1f5b6d09e4362d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b31ad72e5a70416bc8609a1ffaf843342206b0928b8dc525e6e94a042dcce27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe6f0dd2d1df14c38aafd2e58a04461c27e95af11ebe7b61fa049d8849a3356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740c07a3684f805218eba13d1f48dd511fc64ff7dd76b0e6b373d1375714c55b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Tags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383415edb0be9c3c322289fb1d04b1e14b72178dc510f2d096df41d0cab6fd19(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7cd83a0c556859f95121bc939b3ebb3a20a3eaa67a4224f53d4fab44f9ab2bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8ce21687ae1c264e9d1b8955771a3f7cdb94271ef86ea6b4704eb74f86d260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035821225d29cc93736f3f636ed08aef60d248cec486c334ae8554a5f2900bc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318ad84b0056b1c2e4c776bc0f16ffb55f00e0b18ef6150672a036545a9f0dca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsbsBackupPolicyV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
