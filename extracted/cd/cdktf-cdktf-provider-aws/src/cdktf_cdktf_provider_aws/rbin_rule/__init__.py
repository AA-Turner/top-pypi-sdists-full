r'''
# `aws_rbin_rule`

Refer to the Terraform Registry for docs: [`aws_rbin_rule`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule).
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


class RbinRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule aws_rbin_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        resource_type: builtins.str,
        retention_period: typing.Union["RbinRuleRetentionPeriod", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        lock_configuration: typing.Optional[typing.Union["RbinRuleLockConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleResourceTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RbinRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule aws_rbin_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_type RbinRule#resource_type}.
        :param retention_period: retention_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period RbinRule#retention_period}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#description RbinRule#description}.
        :param lock_configuration: lock_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#lock_configuration RbinRule#lock_configuration}
        :param resource_tags: resource_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_tags RbinRule#resource_tags}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#tags RbinRule#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#tags_all RbinRule#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#timeouts RbinRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862f5b21e7ecd8c002ae1fa2bcaf35d8ef9faeb598eef2ffc5c7b1769c344429)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = RbinRuleConfig(
            resource_type=resource_type,
            retention_period=retention_period,
            description=description,
            lock_configuration=lock_configuration,
            resource_tags=resource_tags,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a RbinRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RbinRule to import.
        :param import_from_id: The id of the existing RbinRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RbinRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87da966b34eca3fcc4155c4c49d8c728878761bc29825d6747dd5e6036dda6c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLockConfiguration")
    def put_lock_configuration(
        self,
        *,
        unlock_delay: typing.Union["RbinRuleLockConfigurationUnlockDelay", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param unlock_delay: unlock_delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay RbinRule#unlock_delay}
        '''
        value = RbinRuleLockConfiguration(unlock_delay=unlock_delay)

        return typing.cast(None, jsii.invoke(self, "putLockConfiguration", [value]))

    @jsii.member(jsii_name="putResourceTags")
    def put_resource_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleResourceTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c37bf585384160b7e38725a227d228f8267b8610dd6785a0a5e73dc11ea495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceTags", [value]))

    @jsii.member(jsii_name="putRetentionPeriod")
    def put_retention_period(
        self,
        *,
        retention_period_unit: builtins.str,
        retention_period_value: jsii.Number,
    ) -> None:
        '''
        :param retention_period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period_unit RbinRule#retention_period_unit}.
        :param retention_period_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period_value RbinRule#retention_period_value}.
        '''
        value = RbinRuleRetentionPeriod(
            retention_period_unit=retention_period_unit,
            retention_period_value=retention_period_value,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPeriod", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#create RbinRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#delete RbinRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#update RbinRule#update}.
        '''
        value = RbinRuleTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLockConfiguration")
    def reset_lock_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockConfiguration", []))

    @jsii.member(jsii_name="resetResourceTags")
    def reset_resource_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTags", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lockConfiguration")
    def lock_configuration(self) -> "RbinRuleLockConfigurationOutputReference":
        return typing.cast("RbinRuleLockConfigurationOutputReference", jsii.get(self, "lockConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="lockEndTime")
    def lock_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockEndTime"))

    @builtins.property
    @jsii.member(jsii_name="lockState")
    def lock_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockState"))

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(self) -> "RbinRuleResourceTagsList":
        return typing.cast("RbinRuleResourceTagsList", jsii.get(self, "resourceTags"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> "RbinRuleRetentionPeriodOutputReference":
        return typing.cast("RbinRuleRetentionPeriodOutputReference", jsii.get(self, "retentionPeriod"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RbinRuleTimeoutsOutputReference":
        return typing.cast("RbinRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="lockConfigurationInput")
    def lock_configuration_input(self) -> typing.Optional["RbinRuleLockConfiguration"]:
        return typing.cast(typing.Optional["RbinRuleLockConfiguration"], jsii.get(self, "lockConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagsInput")
    def resource_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleResourceTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleResourceTags"]]], jsii.get(self, "resourceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInput")
    def retention_period_input(self) -> typing.Optional["RbinRuleRetentionPeriod"]:
        return typing.cast(typing.Optional["RbinRuleRetentionPeriod"], jsii.get(self, "retentionPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RbinRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RbinRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac254495707773f4e22b51ce19cecfa18b8f519a9dd414e3e96b9701340b400c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6666f3d4468fb259d8b22b3d883ee4e0d11861a992afb46661ab93b1a9ed889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c387898d6bdcebb089b66cfb6132089e0cff0b9446fabfe9f3dea29452f4597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e3a91dde0e4c35c9c09dc868a55fdf2962841205eaeb4285254ffe8a4680f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "resource_type": "resourceType",
        "retention_period": "retentionPeriod",
        "description": "description",
        "lock_configuration": "lockConfiguration",
        "resource_tags": "resourceTags",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class RbinRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        resource_type: builtins.str,
        retention_period: typing.Union["RbinRuleRetentionPeriod", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        lock_configuration: typing.Optional[typing.Union["RbinRuleLockConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RbinRuleResourceTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RbinRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_type RbinRule#resource_type}.
        :param retention_period: retention_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period RbinRule#retention_period}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#description RbinRule#description}.
        :param lock_configuration: lock_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#lock_configuration RbinRule#lock_configuration}
        :param resource_tags: resource_tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_tags RbinRule#resource_tags}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#tags RbinRule#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#tags_all RbinRule#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#timeouts RbinRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(retention_period, dict):
            retention_period = RbinRuleRetentionPeriod(**retention_period)
        if isinstance(lock_configuration, dict):
            lock_configuration = RbinRuleLockConfiguration(**lock_configuration)
        if isinstance(timeouts, dict):
            timeouts = RbinRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7127948cd669b2b3980482475feb1f21f793c74b4016934b072da5d7662782fb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument lock_configuration", value=lock_configuration, expected_type=type_hints["lock_configuration"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_type": resource_type,
            "retention_period": retention_period,
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
        if description is not None:
            self._values["description"] = description
        if lock_configuration is not None:
            self._values["lock_configuration"] = lock_configuration
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
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
    def resource_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_type RbinRule#resource_type}.'''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_period(self) -> "RbinRuleRetentionPeriod":
        '''retention_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period RbinRule#retention_period}
        '''
        result = self._values.get("retention_period")
        assert result is not None, "Required property 'retention_period' is missing"
        return typing.cast("RbinRuleRetentionPeriod", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#description RbinRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_configuration(self) -> typing.Optional["RbinRuleLockConfiguration"]:
        '''lock_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#lock_configuration RbinRule#lock_configuration}
        '''
        result = self._values.get("lock_configuration")
        return typing.cast(typing.Optional["RbinRuleLockConfiguration"], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleResourceTags"]]]:
        '''resource_tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_tags RbinRule#resource_tags}
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RbinRuleResourceTags"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#tags RbinRule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#tags_all RbinRule#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RbinRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#timeouts RbinRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RbinRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleLockConfiguration",
    jsii_struct_bases=[],
    name_mapping={"unlock_delay": "unlockDelay"},
)
class RbinRuleLockConfiguration:
    def __init__(
        self,
        *,
        unlock_delay: typing.Union["RbinRuleLockConfigurationUnlockDelay", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param unlock_delay: unlock_delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay RbinRule#unlock_delay}
        '''
        if isinstance(unlock_delay, dict):
            unlock_delay = RbinRuleLockConfigurationUnlockDelay(**unlock_delay)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef330ef524cfb776b61b12cf1459f14f7a37ae3517e9a0c539506bdeb8ab228)
            check_type(argname="argument unlock_delay", value=unlock_delay, expected_type=type_hints["unlock_delay"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unlock_delay": unlock_delay,
        }

    @builtins.property
    def unlock_delay(self) -> "RbinRuleLockConfigurationUnlockDelay":
        '''unlock_delay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay RbinRule#unlock_delay}
        '''
        result = self._values.get("unlock_delay")
        assert result is not None, "Required property 'unlock_delay' is missing"
        return typing.cast("RbinRuleLockConfigurationUnlockDelay", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleLockConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleLockConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleLockConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__faf31e86be3d7398c898df0933d37847ee943399217ce9e0d384c06e9b1c4bd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUnlockDelay")
    def put_unlock_delay(
        self,
        *,
        unlock_delay_unit: builtins.str,
        unlock_delay_value: jsii.Number,
    ) -> None:
        '''
        :param unlock_delay_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay_unit RbinRule#unlock_delay_unit}.
        :param unlock_delay_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay_value RbinRule#unlock_delay_value}.
        '''
        value = RbinRuleLockConfigurationUnlockDelay(
            unlock_delay_unit=unlock_delay_unit, unlock_delay_value=unlock_delay_value
        )

        return typing.cast(None, jsii.invoke(self, "putUnlockDelay", [value]))

    @builtins.property
    @jsii.member(jsii_name="unlockDelay")
    def unlock_delay(self) -> "RbinRuleLockConfigurationUnlockDelayOutputReference":
        return typing.cast("RbinRuleLockConfigurationUnlockDelayOutputReference", jsii.get(self, "unlockDelay"))

    @builtins.property
    @jsii.member(jsii_name="unlockDelayInput")
    def unlock_delay_input(
        self,
    ) -> typing.Optional["RbinRuleLockConfigurationUnlockDelay"]:
        return typing.cast(typing.Optional["RbinRuleLockConfigurationUnlockDelay"], jsii.get(self, "unlockDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RbinRuleLockConfiguration]:
        return typing.cast(typing.Optional[RbinRuleLockConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RbinRuleLockConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a67b42fce436511b45a97a82a058b96ee2b203ef2585fe55e3a62ce52c275b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleLockConfigurationUnlockDelay",
    jsii_struct_bases=[],
    name_mapping={
        "unlock_delay_unit": "unlockDelayUnit",
        "unlock_delay_value": "unlockDelayValue",
    },
)
class RbinRuleLockConfigurationUnlockDelay:
    def __init__(
        self,
        *,
        unlock_delay_unit: builtins.str,
        unlock_delay_value: jsii.Number,
    ) -> None:
        '''
        :param unlock_delay_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay_unit RbinRule#unlock_delay_unit}.
        :param unlock_delay_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay_value RbinRule#unlock_delay_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57151adf5b8f0247bd68c8a634f9897648f1e36b342e9c7b217bcf6a651a5434)
            check_type(argname="argument unlock_delay_unit", value=unlock_delay_unit, expected_type=type_hints["unlock_delay_unit"])
            check_type(argname="argument unlock_delay_value", value=unlock_delay_value, expected_type=type_hints["unlock_delay_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unlock_delay_unit": unlock_delay_unit,
            "unlock_delay_value": unlock_delay_value,
        }

    @builtins.property
    def unlock_delay_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay_unit RbinRule#unlock_delay_unit}.'''
        result = self._values.get("unlock_delay_unit")
        assert result is not None, "Required property 'unlock_delay_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unlock_delay_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#unlock_delay_value RbinRule#unlock_delay_value}.'''
        result = self._values.get("unlock_delay_value")
        assert result is not None, "Required property 'unlock_delay_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleLockConfigurationUnlockDelay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleLockConfigurationUnlockDelayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleLockConfigurationUnlockDelayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de43a5e14f8b38fd0db100e4cbb1602a5da1dd7fa40045df48c575e62ca96b8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="unlockDelayUnitInput")
    def unlock_delay_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unlockDelayUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="unlockDelayValueInput")
    def unlock_delay_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unlockDelayValueInput"))

    @builtins.property
    @jsii.member(jsii_name="unlockDelayUnit")
    def unlock_delay_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unlockDelayUnit"))

    @unlock_delay_unit.setter
    def unlock_delay_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88dc0dfed5d8fe50d049ff0c54172a84ee75f689ec57c4957f5d68ef16696b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unlockDelayUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unlockDelayValue")
    def unlock_delay_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unlockDelayValue"))

    @unlock_delay_value.setter
    def unlock_delay_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac668e22791edd1640321715cb605cb0bfc8fde158e686dc61c8612b3e6e4b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unlockDelayValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RbinRuleLockConfigurationUnlockDelay]:
        return typing.cast(typing.Optional[RbinRuleLockConfigurationUnlockDelay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RbinRuleLockConfigurationUnlockDelay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a090b0f8cd9c87886a728ecbd35335d100e02ffda053821a37fcf9e08f3f554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleResourceTags",
    jsii_struct_bases=[],
    name_mapping={
        "resource_tag_key": "resourceTagKey",
        "resource_tag_value": "resourceTagValue",
    },
)
class RbinRuleResourceTags:
    def __init__(
        self,
        *,
        resource_tag_key: builtins.str,
        resource_tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_tag_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_tag_key RbinRule#resource_tag_key}.
        :param resource_tag_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_tag_value RbinRule#resource_tag_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92823db25c66d0a74fbea75e14007373c049c0bb359de8ab70e1789fcb97966b)
            check_type(argname="argument resource_tag_key", value=resource_tag_key, expected_type=type_hints["resource_tag_key"])
            check_type(argname="argument resource_tag_value", value=resource_tag_value, expected_type=type_hints["resource_tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_tag_key": resource_tag_key,
        }
        if resource_tag_value is not None:
            self._values["resource_tag_value"] = resource_tag_value

    @builtins.property
    def resource_tag_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_tag_key RbinRule#resource_tag_key}.'''
        result = self._values.get("resource_tag_key")
        assert result is not None, "Required property 'resource_tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_tag_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#resource_tag_value RbinRule#resource_tag_value}.'''
        result = self._values.get("resource_tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleResourceTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleResourceTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleResourceTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4e3de7ce6409b82881ff9d9cd7b1fea2670517f9db36732a8eba60d57cc07fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RbinRuleResourceTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e22e2271fbffed6480c2304dfd6b4751031140adaf5cd282f3e089d80b42a78)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RbinRuleResourceTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a822cbeb9b3703ee486c77107627fb0f61b8d1d32ab4121c34252d89c58c5927)
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
            type_hints = typing.get_type_hints(_typecheckingstub__202ac035f57074d1b421ae252f8e61e45df7f74b9eb153c8aaa705191279beb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4148a25bdaf699e2ecb641f24b5b76d91c785a78f1cb7a45b49b366f9aa7832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleResourceTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleResourceTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleResourceTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9831e2e864f508a37e00b4a5a12745593e02af7cd6ea25c3abd3912140633f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RbinRuleResourceTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleResourceTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90ddf8da55c26d983178c5db5dd55b11bd554b2ecd8cb42b7619d89cd8ee0629)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetResourceTagValue")
    def reset_resource_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="resourceTagKeyInput")
    def resource_tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagValueInput")
    def resource_tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagKey")
    def resource_tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceTagKey"))

    @resource_tag_key.setter
    def resource_tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bdfc5129d39d8a46289c6e4d99cdf790e101e160de613b17727d5487832d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTagValue")
    def resource_tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceTagValue"))

    @resource_tag_value.setter
    def resource_tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903ca5e906a34cb172f59df03060aadb9bea9d8c015f3ef08500ea69782faf8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleResourceTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleResourceTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleResourceTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da3b0645f67c07f342611a539c9988eb7fc4015c0f1ac80d90299cf81c4b801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleRetentionPeriod",
    jsii_struct_bases=[],
    name_mapping={
        "retention_period_unit": "retentionPeriodUnit",
        "retention_period_value": "retentionPeriodValue",
    },
)
class RbinRuleRetentionPeriod:
    def __init__(
        self,
        *,
        retention_period_unit: builtins.str,
        retention_period_value: jsii.Number,
    ) -> None:
        '''
        :param retention_period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period_unit RbinRule#retention_period_unit}.
        :param retention_period_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period_value RbinRule#retention_period_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca158db9cb6bd49472dc30eb9320461de5a33b6969b168cf9c6896672159dc4)
            check_type(argname="argument retention_period_unit", value=retention_period_unit, expected_type=type_hints["retention_period_unit"])
            check_type(argname="argument retention_period_value", value=retention_period_value, expected_type=type_hints["retention_period_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retention_period_unit": retention_period_unit,
            "retention_period_value": retention_period_value,
        }

    @builtins.property
    def retention_period_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period_unit RbinRule#retention_period_unit}.'''
        result = self._values.get("retention_period_unit")
        assert result is not None, "Required property 'retention_period_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_period_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#retention_period_value RbinRule#retention_period_value}.'''
        result = self._values.get("retention_period_value")
        assert result is not None, "Required property 'retention_period_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleRetentionPeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleRetentionPeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleRetentionPeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__676cdf949a2f69888f423cd16b9e6566c3e1fa19345a5eb2987bf661cd2539d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodUnitInput")
    def retention_period_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPeriodUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodValueInput")
    def retention_period_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodValueInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodUnit")
    def retention_period_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionPeriodUnit"))

    @retention_period_unit.setter
    def retention_period_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a010e7a3699a8053267d5345453e8cd140336ff127904085d5e267752e2462b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodValue")
    def retention_period_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodValue"))

    @retention_period_value.setter
    def retention_period_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c983c8fe3f8452daab6bf239a2053ded79d5b66199b523d25332bc9f45d670a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RbinRuleRetentionPeriod]:
        return typing.cast(typing.Optional[RbinRuleRetentionPeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RbinRuleRetentionPeriod]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de19dc942a0d1f3b05d57772a5907a86a36bdb9c4a2cb63d751738df24374d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class RbinRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#create RbinRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#delete RbinRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#update RbinRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7ac7b598a9f0bc201ba602bf97064e19bc05fe9e3c8acf26d6cbc04b8362d7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#create RbinRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#delete RbinRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/rbin_rule#update RbinRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RbinRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RbinRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.rbinRule.RbinRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba6a9431387077b76e0a33daf0356e78e6a8e8a0f58f2ceab56dac6159fdb21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb3d4a0b0ff3b37dc9e1fa9a1432bb6f7fb40ff0cc6c2d1d27d74bd9354ac1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f2e4f7d24cd8c7b4f159e676e6098cbdc385bbdee14b196028e87540f4cb61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe170bce7779fcc61486caf0403b6fe20df201ef166ffb62f66124e44ad4ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702d4b4e93bcf3082a34f51487facb15d5d592c66ce038fdf98acb0944b56d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RbinRule",
    "RbinRuleConfig",
    "RbinRuleLockConfiguration",
    "RbinRuleLockConfigurationOutputReference",
    "RbinRuleLockConfigurationUnlockDelay",
    "RbinRuleLockConfigurationUnlockDelayOutputReference",
    "RbinRuleResourceTags",
    "RbinRuleResourceTagsList",
    "RbinRuleResourceTagsOutputReference",
    "RbinRuleRetentionPeriod",
    "RbinRuleRetentionPeriodOutputReference",
    "RbinRuleTimeouts",
    "RbinRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__862f5b21e7ecd8c002ae1fa2bcaf35d8ef9faeb598eef2ffc5c7b1769c344429(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    resource_type: builtins.str,
    retention_period: typing.Union[RbinRuleRetentionPeriod, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    lock_configuration: typing.Optional[typing.Union[RbinRuleLockConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleResourceTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RbinRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__87da966b34eca3fcc4155c4c49d8c728878761bc29825d6747dd5e6036dda6c7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c37bf585384160b7e38725a227d228f8267b8610dd6785a0a5e73dc11ea495(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleResourceTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac254495707773f4e22b51ce19cecfa18b8f519a9dd414e3e96b9701340b400c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6666f3d4468fb259d8b22b3d883ee4e0d11861a992afb46661ab93b1a9ed889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c387898d6bdcebb089b66cfb6132089e0cff0b9446fabfe9f3dea29452f4597(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e3a91dde0e4c35c9c09dc868a55fdf2962841205eaeb4285254ffe8a4680f8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7127948cd669b2b3980482475feb1f21f793c74b4016934b072da5d7662782fb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_type: builtins.str,
    retention_period: typing.Union[RbinRuleRetentionPeriod, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    lock_configuration: typing.Optional[typing.Union[RbinRuleLockConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RbinRuleResourceTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RbinRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef330ef524cfb776b61b12cf1459f14f7a37ae3517e9a0c539506bdeb8ab228(
    *,
    unlock_delay: typing.Union[RbinRuleLockConfigurationUnlockDelay, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf31e86be3d7398c898df0933d37847ee943399217ce9e0d384c06e9b1c4bd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a67b42fce436511b45a97a82a058b96ee2b203ef2585fe55e3a62ce52c275b5(
    value: typing.Optional[RbinRuleLockConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57151adf5b8f0247bd68c8a634f9897648f1e36b342e9c7b217bcf6a651a5434(
    *,
    unlock_delay_unit: builtins.str,
    unlock_delay_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de43a5e14f8b38fd0db100e4cbb1602a5da1dd7fa40045df48c575e62ca96b8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88dc0dfed5d8fe50d049ff0c54172a84ee75f689ec57c4957f5d68ef16696b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac668e22791edd1640321715cb605cb0bfc8fde158e686dc61c8612b3e6e4b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a090b0f8cd9c87886a728ecbd35335d100e02ffda053821a37fcf9e08f3f554(
    value: typing.Optional[RbinRuleLockConfigurationUnlockDelay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92823db25c66d0a74fbea75e14007373c049c0bb359de8ab70e1789fcb97966b(
    *,
    resource_tag_key: builtins.str,
    resource_tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e3de7ce6409b82881ff9d9cd7b1fea2670517f9db36732a8eba60d57cc07fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e22e2271fbffed6480c2304dfd6b4751031140adaf5cd282f3e089d80b42a78(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a822cbeb9b3703ee486c77107627fb0f61b8d1d32ab4121c34252d89c58c5927(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202ac035f57074d1b421ae252f8e61e45df7f74b9eb153c8aaa705191279beb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4148a25bdaf699e2ecb641f24b5b76d91c785a78f1cb7a45b49b366f9aa7832(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9831e2e864f508a37e00b4a5a12745593e02af7cd6ea25c3abd3912140633f64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RbinRuleResourceTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ddf8da55c26d983178c5db5dd55b11bd554b2ecd8cb42b7619d89cd8ee0629(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bdfc5129d39d8a46289c6e4d99cdf790e101e160de613b17727d5487832d41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903ca5e906a34cb172f59df03060aadb9bea9d8c015f3ef08500ea69782faf8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da3b0645f67c07f342611a539c9988eb7fc4015c0f1ac80d90299cf81c4b801(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleResourceTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca158db9cb6bd49472dc30eb9320461de5a33b6969b168cf9c6896672159dc4(
    *,
    retention_period_unit: builtins.str,
    retention_period_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676cdf949a2f69888f423cd16b9e6566c3e1fa19345a5eb2987bf661cd2539d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a010e7a3699a8053267d5345453e8cd140336ff127904085d5e267752e2462b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c983c8fe3f8452daab6bf239a2053ded79d5b66199b523d25332bc9f45d670a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de19dc942a0d1f3b05d57772a5907a86a36bdb9c4a2cb63d751738df24374d4c(
    value: typing.Optional[RbinRuleRetentionPeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7ac7b598a9f0bc201ba602bf97064e19bc05fe9e3c8acf26d6cbc04b8362d7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba6a9431387077b76e0a33daf0356e78e6a8e8a0f58f2ceab56dac6159fdb21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3d4a0b0ff3b37dc9e1fa9a1432bb6f7fb40ff0cc6c2d1d27d74bd9354ac1d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f2e4f7d24cd8c7b4f159e676e6098cbdc385bbdee14b196028e87540f4cb61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe170bce7779fcc61486caf0403b6fe20df201ef166ffb62f66124e44ad4ae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702d4b4e93bcf3082a34f51487facb15d5d592c66ce038fdf98acb0944b56d86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RbinRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
