r'''
# `aws_backup_plan`

Refer to the Terraform Registry for docs: [`aws_backup_plan`](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan).
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


class BackupPlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan aws_backup_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRule", typing.Dict[builtins.str, typing.Any]]]],
        advanced_backup_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanAdvancedBackupSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scan_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanScanSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan aws_backup_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#name BackupPlan#name}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#rule BackupPlan#rule}
        :param advanced_backup_setting: advanced_backup_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#advanced_backup_setting BackupPlan#advanced_backup_setting}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#id BackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#region BackupPlan#region}
        :param scan_setting: scan_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scan_setting BackupPlan#scan_setting}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#tags BackupPlan#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#tags_all BackupPlan#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9979f5e54a053376e8436bc4239757c6c491cda68713f678d6cfc6e8b02743f5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BackupPlanConfig(
            name=name,
            rule=rule,
            advanced_backup_setting=advanced_backup_setting,
            id=id,
            region=region,
            scan_setting=scan_setting,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a BackupPlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BackupPlan to import.
        :param import_from_id: The id of the existing BackupPlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BackupPlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7183e80d6e6d4a7125cdf42d733a4d0958f99bd6c2bb034b989724a9126043d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedBackupSetting")
    def put_advanced_backup_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanAdvancedBackupSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37b7af5155f6608f16d98353349b7389d6347da4496c5954e3d67e5b6a675ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdvancedBackupSetting", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43dfa2074a7a607cdcdd63d8c3e1b3d34500c840d47117296eb0cad48114581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="putScanSetting")
    def put_scan_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanScanSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3660e2b223879a6db23b3ba48710a4d134b8b4866b3a9e8384f8b4f60cdf8561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScanSetting", [value]))

    @jsii.member(jsii_name="resetAdvancedBackupSetting")
    def reset_advanced_backup_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedBackupSetting", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScanSetting")
    def reset_scan_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanSetting", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="advancedBackupSetting")
    def advanced_backup_setting(self) -> "BackupPlanAdvancedBackupSettingList":
        return typing.cast("BackupPlanAdvancedBackupSettingList", jsii.get(self, "advancedBackupSetting"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "BackupPlanRuleList":
        return typing.cast("BackupPlanRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="scanSetting")
    def scan_setting(self) -> "BackupPlanScanSettingList":
        return typing.cast("BackupPlanScanSettingList", jsii.get(self, "scanSetting"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="advancedBackupSettingInput")
    def advanced_backup_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanAdvancedBackupSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanAdvancedBackupSetting"]]], jsii.get(self, "advancedBackupSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="scanSettingInput")
    def scan_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanScanSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanScanSetting"]]], jsii.get(self, "scanSettingInput"))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01382e476bdc7b6eda1be481c8aba8a165b4366423ac61cf18ee16665587294d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f503759d60b70d9eaf951fd706fe57359dceadbf50e93c6209a40defea829bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f843d3ec89b666cf51e3a390b6de3f9c80a9e22fdd1f5fbea1f7a4c3bcafdca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f614098e7cfd558729164da3e71f86f64a81843f0df4164f0de357a11f09f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b447b97f6adebd6ab93ff854c205b62585f5ca309b1acbf3e952a1b80f69446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanAdvancedBackupSetting",
    jsii_struct_bases=[],
    name_mapping={"backup_options": "backupOptions", "resource_type": "resourceType"},
)
class BackupPlanAdvancedBackupSetting:
    def __init__(
        self,
        *,
        backup_options: typing.Mapping[builtins.str, builtins.str],
        resource_type: builtins.str,
    ) -> None:
        '''
        :param backup_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#backup_options BackupPlan#backup_options}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#resource_type BackupPlan#resource_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df743c033151fece2a56c018e7e7255ae1030797bd7ba27945776c6fb051873a)
            check_type(argname="argument backup_options", value=backup_options, expected_type=type_hints["backup_options"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_options": backup_options,
            "resource_type": resource_type,
        }

    @builtins.property
    def backup_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#backup_options BackupPlan#backup_options}.'''
        result = self._values.get("backup_options")
        assert result is not None, "Required property 'backup_options' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#resource_type BackupPlan#resource_type}.'''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanAdvancedBackupSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanAdvancedBackupSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanAdvancedBackupSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d47291a847481362f96848183747d4eaea0a1fa5eb96bfd4cb3377bb9a728f62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BackupPlanAdvancedBackupSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f405803ee24ac2f953d3e57870f5195863cd662fae6a90c958219e3c0ef7fac7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanAdvancedBackupSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271832e23838b405149284727cb1659ee3848d64a697ca55337779f1e50c96f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1247ed3786ae7b622511dbcdce65b4aaf5235abbfbbdb1904ce190f8a6bd0abb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26a22a509374ff47938cc08f4bc339d79fb7adf56483f02fd2b68be4d75cf6b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2288aa073d914b7b524b018d04c524f23620db8bb6b41d54a1b28a795b9e9397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanAdvancedBackupSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanAdvancedBackupSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bc91b1b2f335d09c8456a4c1d351b6d7b5d01d394535d4bddccc52445e4d0e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="backupOptionsInput")
    def backup_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "backupOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupOptions")
    def backup_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "backupOptions"))

    @backup_options.setter
    def backup_options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4972770e8509c74767d4e8c6e082870a171f106a02ed8d57244c64906c260111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478e83905ff1651a4f561892b20f854411b96ff6484d4eb96ec5be3e5eec9a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanAdvancedBackupSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanAdvancedBackupSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanAdvancedBackupSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f0abc4f4c96c501e23bfed76c80f2654349a6c221f88ee3fe12c5ff18fe0c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanConfig",
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
        "rule": "rule",
        "advanced_backup_setting": "advancedBackupSetting",
        "id": "id",
        "region": "region",
        "scan_setting": "scanSetting",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class BackupPlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRule", typing.Dict[builtins.str, typing.Any]]]],
        advanced_backup_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanAdvancedBackupSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scan_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanScanSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#name BackupPlan#name}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#rule BackupPlan#rule}
        :param advanced_backup_setting: advanced_backup_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#advanced_backup_setting BackupPlan#advanced_backup_setting}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#id BackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#region BackupPlan#region}
        :param scan_setting: scan_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scan_setting BackupPlan#scan_setting}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#tags BackupPlan#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#tags_all BackupPlan#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a891f209cbb80eb2aa97a48d94bee2010af3e9315d8b7f5ee02f308c69f977cc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument advanced_backup_setting", value=advanced_backup_setting, expected_type=type_hints["advanced_backup_setting"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scan_setting", value=scan_setting, expected_type=type_hints["scan_setting"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "rule": rule,
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
        if advanced_backup_setting is not None:
            self._values["advanced_backup_setting"] = advanced_backup_setting
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if scan_setting is not None:
            self._values["scan_setting"] = scan_setting
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#name BackupPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#rule BackupPlan#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRule"]], result)

    @builtins.property
    def advanced_backup_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]]:
        '''advanced_backup_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#advanced_backup_setting BackupPlan#advanced_backup_setting}
        '''
        result = self._values.get("advanced_backup_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#id BackupPlan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#region BackupPlan#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scan_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanScanSetting"]]]:
        '''scan_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scan_setting BackupPlan#scan_setting}
        '''
        result = self._values.get("scan_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanScanSetting"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#tags BackupPlan#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#tags_all BackupPlan#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRule",
    jsii_struct_bases=[],
    name_mapping={
        "rule_name": "ruleName",
        "target_vault_name": "targetVaultName",
        "completion_window": "completionWindow",
        "copy_action": "copyAction",
        "enable_continuous_backup": "enableContinuousBackup",
        "lifecycle": "lifecycle",
        "recovery_point_tags": "recoveryPointTags",
        "scan_action": "scanAction",
        "schedule": "schedule",
        "schedule_expression_timezone": "scheduleExpressionTimezone",
        "start_window": "startWindow",
        "target_logically_air_gapped_backup_vault_arn": "targetLogicallyAirGappedBackupVaultArn",
    },
)
class BackupPlanRule:
    def __init__(
        self,
        *,
        rule_name: builtins.str,
        target_vault_name: builtins.str,
        completion_window: typing.Optional[jsii.Number] = None,
        copy_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRuleCopyAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_continuous_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lifecycle: typing.Optional[typing.Union["BackupPlanRuleLifecycle", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_point_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        scan_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRuleScanAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_expression_timezone: typing.Optional[builtins.str] = None,
        start_window: typing.Optional[jsii.Number] = None,
        target_logically_air_gapped_backup_vault_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#rule_name BackupPlan#rule_name}.
        :param target_vault_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#target_vault_name BackupPlan#target_vault_name}.
        :param completion_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#completion_window BackupPlan#completion_window}.
        :param copy_action: copy_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#copy_action BackupPlan#copy_action}
        :param enable_continuous_backup: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#enable_continuous_backup BackupPlan#enable_continuous_backup}.
        :param lifecycle: lifecycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#lifecycle BackupPlan#lifecycle}
        :param recovery_point_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#recovery_point_tags BackupPlan#recovery_point_tags}.
        :param scan_action: scan_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scan_action BackupPlan#scan_action}
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#schedule BackupPlan#schedule}.
        :param schedule_expression_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#schedule_expression_timezone BackupPlan#schedule_expression_timezone}.
        :param start_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#start_window BackupPlan#start_window}.
        :param target_logically_air_gapped_backup_vault_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#target_logically_air_gapped_backup_vault_arn BackupPlan#target_logically_air_gapped_backup_vault_arn}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = BackupPlanRuleLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e34b1fa0d72b472701d62e322e33c1ec30f442aded06787c49db49aad74623)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument target_vault_name", value=target_vault_name, expected_type=type_hints["target_vault_name"])
            check_type(argname="argument completion_window", value=completion_window, expected_type=type_hints["completion_window"])
            check_type(argname="argument copy_action", value=copy_action, expected_type=type_hints["copy_action"])
            check_type(argname="argument enable_continuous_backup", value=enable_continuous_backup, expected_type=type_hints["enable_continuous_backup"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument recovery_point_tags", value=recovery_point_tags, expected_type=type_hints["recovery_point_tags"])
            check_type(argname="argument scan_action", value=scan_action, expected_type=type_hints["scan_action"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument schedule_expression_timezone", value=schedule_expression_timezone, expected_type=type_hints["schedule_expression_timezone"])
            check_type(argname="argument start_window", value=start_window, expected_type=type_hints["start_window"])
            check_type(argname="argument target_logically_air_gapped_backup_vault_arn", value=target_logically_air_gapped_backup_vault_arn, expected_type=type_hints["target_logically_air_gapped_backup_vault_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
            "target_vault_name": target_vault_name,
        }
        if completion_window is not None:
            self._values["completion_window"] = completion_window
        if copy_action is not None:
            self._values["copy_action"] = copy_action
        if enable_continuous_backup is not None:
            self._values["enable_continuous_backup"] = enable_continuous_backup
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if recovery_point_tags is not None:
            self._values["recovery_point_tags"] = recovery_point_tags
        if scan_action is not None:
            self._values["scan_action"] = scan_action
        if schedule is not None:
            self._values["schedule"] = schedule
        if schedule_expression_timezone is not None:
            self._values["schedule_expression_timezone"] = schedule_expression_timezone
        if start_window is not None:
            self._values["start_window"] = start_window
        if target_logically_air_gapped_backup_vault_arn is not None:
            self._values["target_logically_air_gapped_backup_vault_arn"] = target_logically_air_gapped_backup_vault_arn

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#rule_name BackupPlan#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_vault_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#target_vault_name BackupPlan#target_vault_name}.'''
        result = self._values.get("target_vault_name")
        assert result is not None, "Required property 'target_vault_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def completion_window(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#completion_window BackupPlan#completion_window}.'''
        result = self._values.get("completion_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def copy_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleCopyAction"]]]:
        '''copy_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#copy_action BackupPlan#copy_action}
        '''
        result = self._values.get("copy_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleCopyAction"]]], result)

    @builtins.property
    def enable_continuous_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#enable_continuous_backup BackupPlan#enable_continuous_backup}.'''
        result = self._values.get("enable_continuous_backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional["BackupPlanRuleLifecycle"]:
        '''lifecycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#lifecycle BackupPlan#lifecycle}
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional["BackupPlanRuleLifecycle"], result)

    @builtins.property
    def recovery_point_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#recovery_point_tags BackupPlan#recovery_point_tags}.'''
        result = self._values.get("recovery_point_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def scan_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleScanAction"]]]:
        '''scan_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scan_action BackupPlan#scan_action}
        '''
        result = self._values.get("scan_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleScanAction"]]], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#schedule BackupPlan#schedule}.'''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression_timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#schedule_expression_timezone BackupPlan#schedule_expression_timezone}.'''
        result = self._values.get("schedule_expression_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_window(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#start_window BackupPlan#start_window}.'''
        result = self._values.get("start_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_logically_air_gapped_backup_vault_arn(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#target_logically_air_gapped_backup_vault_arn BackupPlan#target_logically_air_gapped_backup_vault_arn}.'''
        result = self._values.get("target_logically_air_gapped_backup_vault_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleCopyAction",
    jsii_struct_bases=[],
    name_mapping={
        "destination_vault_arn": "destinationVaultArn",
        "lifecycle": "lifecycle",
    },
)
class BackupPlanRuleCopyAction:
    def __init__(
        self,
        *,
        destination_vault_arn: builtins.str,
        lifecycle: typing.Optional[typing.Union["BackupPlanRuleCopyActionLifecycle", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination_vault_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#destination_vault_arn BackupPlan#destination_vault_arn}.
        :param lifecycle: lifecycle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#lifecycle BackupPlan#lifecycle}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = BackupPlanRuleCopyActionLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9054ccf9e58c637abc10af00c7bf8dbbe70b6a4ee95a9726f0bb4bbc0d1f28f)
            check_type(argname="argument destination_vault_arn", value=destination_vault_arn, expected_type=type_hints["destination_vault_arn"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_vault_arn": destination_vault_arn,
        }
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle

    @builtins.property
    def destination_vault_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#destination_vault_arn BackupPlan#destination_vault_arn}.'''
        result = self._values.get("destination_vault_arn")
        assert result is not None, "Required property 'destination_vault_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lifecycle(self) -> typing.Optional["BackupPlanRuleCopyActionLifecycle"]:
        '''lifecycle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#lifecycle BackupPlan#lifecycle}
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional["BackupPlanRuleCopyActionLifecycle"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleCopyAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleCopyActionLifecycle",
    jsii_struct_bases=[],
    name_mapping={
        "cold_storage_after": "coldStorageAfter",
        "delete_after": "deleteAfter",
        "opt_in_to_archive_for_supported_resources": "optInToArchiveForSupportedResources",
    },
)
class BackupPlanRuleCopyActionLifecycle:
    def __init__(
        self,
        *,
        cold_storage_after: typing.Optional[jsii.Number] = None,
        delete_after: typing.Optional[jsii.Number] = None,
        opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.
        :param delete_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.
        :param opt_in_to_archive_for_supported_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb7ecdc70bb243938f32dca7924f4e514d13ae0d71790c921a4baccc39abdc4)
            check_type(argname="argument cold_storage_after", value=cold_storage_after, expected_type=type_hints["cold_storage_after"])
            check_type(argname="argument delete_after", value=delete_after, expected_type=type_hints["delete_after"])
            check_type(argname="argument opt_in_to_archive_for_supported_resources", value=opt_in_to_archive_for_supported_resources, expected_type=type_hints["opt_in_to_archive_for_supported_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cold_storage_after is not None:
            self._values["cold_storage_after"] = cold_storage_after
        if delete_after is not None:
            self._values["delete_after"] = delete_after
        if opt_in_to_archive_for_supported_resources is not None:
            self._values["opt_in_to_archive_for_supported_resources"] = opt_in_to_archive_for_supported_resources

    @builtins.property
    def cold_storage_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.'''
        result = self._values.get("cold_storage_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.'''
        result = self._values.get("delete_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def opt_in_to_archive_for_supported_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.'''
        result = self._values.get("opt_in_to_archive_for_supported_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleCopyActionLifecycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanRuleCopyActionLifecycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleCopyActionLifecycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c662ff4237651d9a9932a16089a8f2300e809def0159358fb92f29f6b8f021e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetColdStorageAfter")
    def reset_cold_storage_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColdStorageAfter", []))

    @jsii.member(jsii_name="resetDeleteAfter")
    def reset_delete_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfter", []))

    @jsii.member(jsii_name="resetOptInToArchiveForSupportedResources")
    def reset_opt_in_to_archive_for_supported_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptInToArchiveForSupportedResources", []))

    @builtins.property
    @jsii.member(jsii_name="coldStorageAfterInput")
    def cold_storage_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coldStorageAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterInput")
    def delete_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="optInToArchiveForSupportedResourcesInput")
    def opt_in_to_archive_for_supported_resources_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optInToArchiveForSupportedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="coldStorageAfter")
    def cold_storage_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coldStorageAfter"))

    @cold_storage_after.setter
    def cold_storage_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c58924fcab4d43e1f48b125015e9eec29c32742e258828dc44496c813456b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coldStorageAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfter")
    def delete_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfter"))

    @delete_after.setter
    def delete_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbe9f299f3900b59229510df6637c3d8c75db22e0bbaaeb04086fd78be991e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optInToArchiveForSupportedResources")
    def opt_in_to_archive_for_supported_resources(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optInToArchiveForSupportedResources"))

    @opt_in_to_archive_for_supported_resources.setter
    def opt_in_to_archive_for_supported_resources(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9402f8cf6667e6008c88abe9b1ed75c6cd881f21b764fd832274782523d10a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optInToArchiveForSupportedResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPlanRuleCopyActionLifecycle]:
        return typing.cast(typing.Optional[BackupPlanRuleCopyActionLifecycle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupPlanRuleCopyActionLifecycle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fadc495f97cecd913a92029a9d12c2bc4736d2ee04ba6f72125cfa40dedfa69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleCopyActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleCopyActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b8f0a4fc5d2e812de77cf63e3599185bc34e0502989a485892a145d1741e549)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupPlanRuleCopyActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5069267b6cec77ef3937cf1f149ceec401d775aa717ba51cbb71d9d84fd78f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanRuleCopyActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafadc0a012816309ba93bc4f03a36545d3a6ef618ed96d132bd8e9fbd5b5fd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c05bbdc801c337fde075bdb932f659b66ce5a024a375162ea2051998e9150c86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f05e9dc8e797082476a7eee5a5fd25a6dc524d0ee8e79cd2d232a4330a3132ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b34f621ea1cf20cb21825b5a4bf14174007394308a0981aa5dbb98d13d0a8ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleCopyActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleCopyActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12a9ac2e07f5048fe5fb4725ea1ae6fb1878e00d729635fbcc4d75d111e27873)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLifecycle")
    def put_lifecycle(
        self,
        *,
        cold_storage_after: typing.Optional[jsii.Number] = None,
        delete_after: typing.Optional[jsii.Number] = None,
        opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.
        :param delete_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.
        :param opt_in_to_archive_for_supported_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.
        '''
        value = BackupPlanRuleCopyActionLifecycle(
            cold_storage_after=cold_storage_after,
            delete_after=delete_after,
            opt_in_to_archive_for_supported_resources=opt_in_to_archive_for_supported_resources,
        )

        return typing.cast(None, jsii.invoke(self, "putLifecycle", [value]))

    @jsii.member(jsii_name="resetLifecycle")
    def reset_lifecycle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycle", []))

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> BackupPlanRuleCopyActionLifecycleOutputReference:
        return typing.cast(BackupPlanRuleCopyActionLifecycleOutputReference, jsii.get(self, "lifecycle"))

    @builtins.property
    @jsii.member(jsii_name="destinationVaultArnInput")
    def destination_vault_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationVaultArnInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleInput")
    def lifecycle_input(self) -> typing.Optional[BackupPlanRuleCopyActionLifecycle]:
        return typing.cast(typing.Optional[BackupPlanRuleCopyActionLifecycle], jsii.get(self, "lifecycleInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationVaultArn")
    def destination_vault_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationVaultArn"))

    @destination_vault_arn.setter
    def destination_vault_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e14d73e68915c36e8cf0904aee8bae68b51b3b0628f442d606f128c76bd993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationVaultArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleCopyAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleCopyAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleCopyAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33038444ecb7712d911ded362d45472243a23772dc285cb387085b3ccbb67a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleLifecycle",
    jsii_struct_bases=[],
    name_mapping={
        "cold_storage_after": "coldStorageAfter",
        "delete_after": "deleteAfter",
        "opt_in_to_archive_for_supported_resources": "optInToArchiveForSupportedResources",
    },
)
class BackupPlanRuleLifecycle:
    def __init__(
        self,
        *,
        cold_storage_after: typing.Optional[jsii.Number] = None,
        delete_after: typing.Optional[jsii.Number] = None,
        opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.
        :param delete_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.
        :param opt_in_to_archive_for_supported_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8ea11b215000a780a7b06973f5bd904615f183e349e6d6e3bdacf4b2cc54b2)
            check_type(argname="argument cold_storage_after", value=cold_storage_after, expected_type=type_hints["cold_storage_after"])
            check_type(argname="argument delete_after", value=delete_after, expected_type=type_hints["delete_after"])
            check_type(argname="argument opt_in_to_archive_for_supported_resources", value=opt_in_to_archive_for_supported_resources, expected_type=type_hints["opt_in_to_archive_for_supported_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cold_storage_after is not None:
            self._values["cold_storage_after"] = cold_storage_after
        if delete_after is not None:
            self._values["delete_after"] = delete_after
        if opt_in_to_archive_for_supported_resources is not None:
            self._values["opt_in_to_archive_for_supported_resources"] = opt_in_to_archive_for_supported_resources

    @builtins.property
    def cold_storage_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.'''
        result = self._values.get("cold_storage_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_after(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.'''
        result = self._values.get("delete_after")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def opt_in_to_archive_for_supported_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.'''
        result = self._values.get("opt_in_to_archive_for_supported_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleLifecycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanRuleLifecycleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleLifecycleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b8b798e5cdafb7a8045ea92c22512cd2442cef3d8bce4fc26f4d8447c9869ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetColdStorageAfter")
    def reset_cold_storage_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColdStorageAfter", []))

    @jsii.member(jsii_name="resetDeleteAfter")
    def reset_delete_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfter", []))

    @jsii.member(jsii_name="resetOptInToArchiveForSupportedResources")
    def reset_opt_in_to_archive_for_supported_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptInToArchiveForSupportedResources", []))

    @builtins.property
    @jsii.member(jsii_name="coldStorageAfterInput")
    def cold_storage_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coldStorageAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterInput")
    def delete_after_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="optInToArchiveForSupportedResourcesInput")
    def opt_in_to_archive_for_supported_resources_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optInToArchiveForSupportedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="coldStorageAfter")
    def cold_storage_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coldStorageAfter"))

    @cold_storage_after.setter
    def cold_storage_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d3201f7acbf4a0c6049a713f8fa4dea942dc199240b1ad89116440e5cad13b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coldStorageAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteAfter")
    def delete_after(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deleteAfter"))

    @delete_after.setter
    def delete_after(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacb59d48c7b45d11a8fea7f5efd6cf93c68ff663ce865709d3dde5a6a5fd1a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optInToArchiveForSupportedResources")
    def opt_in_to_archive_for_supported_resources(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optInToArchiveForSupportedResources"))

    @opt_in_to_archive_for_supported_resources.setter
    def opt_in_to_archive_for_supported_resources(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d408b9982e994382a02fe8299e19c5751a43a990d69619e57415d56084aa4eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optInToArchiveForSupportedResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BackupPlanRuleLifecycle]:
        return typing.cast(typing.Optional[BackupPlanRuleLifecycle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BackupPlanRuleLifecycle]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856767666bb64a8da6c6c7e9eb0115b09fab3c4e38b3bfdeb43abf5897dafdbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a7d0d0dd830d41a2b515000f86a95287e2c65a213ac87f4415c73808f585314)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupPlanRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1844d2ce8c1e580dd171d88679440dbb219b9390991cf9776f950072f6c87e4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6050802970bc5d995db6dff317f667a5686bf015d73af61eee5514d4a19d39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__940d0bdfd2985ae0f7c378821a0552bf7997893a7e43f33ffe61e7ec2b7749bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e3956d473049a0938c41992b17309a20de5acbec48377a5b4dd0abbcfd4538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f7bbb9b74b30354e62063b779eb828164ad9d2532fcae6efad4de2ee4a0247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c531d90d1356b3ed40e51c5a1978e568b507296731b8e9e6f9fe980404a9e73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCopyAction")
    def put_copy_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleCopyAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff25f9d69486d06cf8b90a93ada17ac8e119a9da8a67f6e2f793543a1890837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCopyAction", [value]))

    @jsii.member(jsii_name="putLifecycle")
    def put_lifecycle(
        self,
        *,
        cold_storage_after: typing.Optional[jsii.Number] = None,
        delete_after: typing.Optional[jsii.Number] = None,
        opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#cold_storage_after BackupPlan#cold_storage_after}.
        :param delete_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#delete_after BackupPlan#delete_after}.
        :param opt_in_to_archive_for_supported_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#opt_in_to_archive_for_supported_resources BackupPlan#opt_in_to_archive_for_supported_resources}.
        '''
        value = BackupPlanRuleLifecycle(
            cold_storage_after=cold_storage_after,
            delete_after=delete_after,
            opt_in_to_archive_for_supported_resources=opt_in_to_archive_for_supported_resources,
        )

        return typing.cast(None, jsii.invoke(self, "putLifecycle", [value]))

    @jsii.member(jsii_name="putScanAction")
    def put_scan_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupPlanRuleScanAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560d2e3cc329c6200115816b383f2c869e3ad0a86efd7439c318cb3a18bb10a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScanAction", [value]))

    @jsii.member(jsii_name="resetCompletionWindow")
    def reset_completion_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompletionWindow", []))

    @jsii.member(jsii_name="resetCopyAction")
    def reset_copy_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyAction", []))

    @jsii.member(jsii_name="resetEnableContinuousBackup")
    def reset_enable_continuous_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableContinuousBackup", []))

    @jsii.member(jsii_name="resetLifecycle")
    def reset_lifecycle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycle", []))

    @jsii.member(jsii_name="resetRecoveryPointTags")
    def reset_recovery_point_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryPointTags", []))

    @jsii.member(jsii_name="resetScanAction")
    def reset_scan_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanAction", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetScheduleExpressionTimezone")
    def reset_schedule_expression_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleExpressionTimezone", []))

    @jsii.member(jsii_name="resetStartWindow")
    def reset_start_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartWindow", []))

    @jsii.member(jsii_name="resetTargetLogicallyAirGappedBackupVaultArn")
    def reset_target_logically_air_gapped_backup_vault_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetLogicallyAirGappedBackupVaultArn", []))

    @builtins.property
    @jsii.member(jsii_name="copyAction")
    def copy_action(self) -> BackupPlanRuleCopyActionList:
        return typing.cast(BackupPlanRuleCopyActionList, jsii.get(self, "copyAction"))

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> BackupPlanRuleLifecycleOutputReference:
        return typing.cast(BackupPlanRuleLifecycleOutputReference, jsii.get(self, "lifecycle"))

    @builtins.property
    @jsii.member(jsii_name="scanAction")
    def scan_action(self) -> "BackupPlanRuleScanActionList":
        return typing.cast("BackupPlanRuleScanActionList", jsii.get(self, "scanAction"))

    @builtins.property
    @jsii.member(jsii_name="completionWindowInput")
    def completion_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "completionWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="copyActionInput")
    def copy_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]], jsii.get(self, "copyActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableContinuousBackupInput")
    def enable_continuous_backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableContinuousBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleInput")
    def lifecycle_input(self) -> typing.Optional[BackupPlanRuleLifecycle]:
        return typing.cast(typing.Optional[BackupPlanRuleLifecycle], jsii.get(self, "lifecycleInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryPointTagsInput")
    def recovery_point_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "recoveryPointTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scanActionInput")
    def scan_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleScanAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupPlanRuleScanAction"]]], jsii.get(self, "scanActionInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleExpressionTimezoneInput")
    def schedule_expression_timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleExpressionTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="startWindowInput")
    def start_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="targetLogicallyAirGappedBackupVaultArnInput")
    def target_logically_air_gapped_backup_vault_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetLogicallyAirGappedBackupVaultArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetVaultNameInput")
    def target_vault_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetVaultNameInput"))

    @builtins.property
    @jsii.member(jsii_name="completionWindow")
    def completion_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "completionWindow"))

    @completion_window.setter
    def completion_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b56f73475b6c7d1959d214747f790d863e3c84c558245c29bd2ba9b0382484f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "completionWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableContinuousBackup")
    def enable_continuous_backup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableContinuousBackup"))

    @enable_continuous_backup.setter
    def enable_continuous_backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__582837cd777dfed0e74f2a14002e89ec643054b09766f6ace3b9c03568a6ab70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableContinuousBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryPointTags")
    def recovery_point_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "recoveryPointTags"))

    @recovery_point_tags.setter
    def recovery_point_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5b874fe3574b521aa2f219e647e0ab92aac75a532cbc2d01e22b7c67b67c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryPointTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d60b6a382f6d79f7fa735dc42b4884c964badbbef3e6b3e18befff58224a32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9d532b285b10c812c1a631d86e204376109839a104f8aa19fcebacbe8455c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleExpressionTimezone")
    def schedule_expression_timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleExpressionTimezone"))

    @schedule_expression_timezone.setter
    def schedule_expression_timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6defc5d81c4f09ad296eb6d7e46596cebcd1f741a3b848bd053b7dc4966e352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleExpressionTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startWindow")
    def start_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startWindow"))

    @start_window.setter
    def start_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3341b4e67790a5d32c2e850115a3dc66d4887e7cfc281efaa454d1b83e7161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetLogicallyAirGappedBackupVaultArn")
    def target_logically_air_gapped_backup_vault_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetLogicallyAirGappedBackupVaultArn"))

    @target_logically_air_gapped_backup_vault_arn.setter
    def target_logically_air_gapped_backup_vault_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a51d3042816760e27a0b1ca15c67c78efb6fd3e1c727463f9c647f57f9110a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetLogicallyAirGappedBackupVaultArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetVaultName")
    def target_vault_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetVaultName"))

    @target_vault_name.setter
    def target_vault_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fc27e206f6fc5d0511077cb142b1cf05847d352ebbc6d253137b9ae25268e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetVaultName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0987a14daa01658b8feb12d62180f1bc7e115aac99c93854eb3f19817d0a84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleScanAction",
    jsii_struct_bases=[],
    name_mapping={"malware_scanner": "malwareScanner", "scan_mode": "scanMode"},
)
class BackupPlanRuleScanAction:
    def __init__(
        self,
        *,
        malware_scanner: builtins.str,
        scan_mode: builtins.str,
    ) -> None:
        '''
        :param malware_scanner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#malware_scanner BackupPlan#malware_scanner}.
        :param scan_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scan_mode BackupPlan#scan_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2935de05fb6b87660c34dd0582eaa6a6626659f9bbf351ff3d97907e12b66f1b)
            check_type(argname="argument malware_scanner", value=malware_scanner, expected_type=type_hints["malware_scanner"])
            check_type(argname="argument scan_mode", value=scan_mode, expected_type=type_hints["scan_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "malware_scanner": malware_scanner,
            "scan_mode": scan_mode,
        }

    @builtins.property
    def malware_scanner(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#malware_scanner BackupPlan#malware_scanner}.'''
        result = self._values.get("malware_scanner")
        assert result is not None, "Required property 'malware_scanner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scan_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scan_mode BackupPlan#scan_mode}.'''
        result = self._values.get("scan_mode")
        assert result is not None, "Required property 'scan_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleScanAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanRuleScanActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleScanActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa4173e56dc67ad0e3a0441b1f3702e5151f9f40915d2776749c70c67709df5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupPlanRuleScanActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe2aa948e5337b1acdbf2a1d7eae838cb25388cddd933fa4c64ff0bbe48f246)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanRuleScanActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701165c026fc9405bd83d8ea4833cf7d4fc8f7c54050b875b378572d268f45e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fe05397426c20a9ccfe0e740df0a8e529cf3080a3113dc91d7a76db6f4d7571)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4974431911c9e19fd4bb476c68b7151abf8db73ac181175726c84b7ef04d56aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleScanAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleScanAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleScanAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335014d3e5e4abdb513ce5b57fd748dd8cf300a191403bb9c61a70c9b1efbaaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanRuleScanActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanRuleScanActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62d3199c3f5bfacfba10fa252b22953ad9384293ef22f32b53c6c9c611d7a968)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="malwareScannerInput")
    def malware_scanner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "malwareScannerInput"))

    @builtins.property
    @jsii.member(jsii_name="scanModeInput")
    def scan_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scanModeInput"))

    @builtins.property
    @jsii.member(jsii_name="malwareScanner")
    def malware_scanner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "malwareScanner"))

    @malware_scanner.setter
    def malware_scanner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b2188db7c6c92fddc8d2ac986d251b14f0c89d312715e4da5f5d90682cf8d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "malwareScanner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanMode")
    def scan_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanMode"))

    @scan_mode.setter
    def scan_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e859c68f3292f22352033b713ea5542c7d268fc5516ef5c04b611c8bb46ab48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleScanAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleScanAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleScanAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a180d62b2f7cfc8a3ac122d82e18588fcf61369b5a42330e236cb4e9d1e8a3a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanScanSetting",
    jsii_struct_bases=[],
    name_mapping={
        "malware_scanner": "malwareScanner",
        "resource_types": "resourceTypes",
        "scanner_role_arn": "scannerRoleArn",
    },
)
class BackupPlanScanSetting:
    def __init__(
        self,
        *,
        malware_scanner: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        scanner_role_arn: builtins.str,
    ) -> None:
        '''
        :param malware_scanner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#malware_scanner BackupPlan#malware_scanner}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#resource_types BackupPlan#resource_types}.
        :param scanner_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scanner_role_arn BackupPlan#scanner_role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a7240b66e724b26884611dafab1a4321bda3b0caf85dcca978c10f440540fb)
            check_type(argname="argument malware_scanner", value=malware_scanner, expected_type=type_hints["malware_scanner"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument scanner_role_arn", value=scanner_role_arn, expected_type=type_hints["scanner_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "malware_scanner": malware_scanner,
            "resource_types": resource_types,
            "scanner_role_arn": scanner_role_arn,
        }

    @builtins.property
    def malware_scanner(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#malware_scanner BackupPlan#malware_scanner}.'''
        result = self._values.get("malware_scanner")
        assert result is not None, "Required property 'malware_scanner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#resource_types BackupPlan#resource_types}.'''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def scanner_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/backup_plan#scanner_role_arn BackupPlan#scanner_role_arn}.'''
        result = self._values.get("scanner_role_arn")
        assert result is not None, "Required property 'scanner_role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanScanSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanScanSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanScanSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa089731b0da72d0ea8bae39f2951cd9eb07508568c4de698fe4dce9fc2911a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupPlanScanSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3559f6e71c2153357cf8c4afaa4fcfab8c2f66bcfa7f5823a73388c92e813e8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupPlanScanSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b226332bd76b37c7a5c984c1ce54a53e6604f89a00dd4f82468c7ba11efa9fd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3fd43040a8f00c130ee77130a8ec7270c38260570a6d6c7ddbae33aa4cf7b69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c14cfbfc26bee3755cfcd8c96961de3dfe7e6164ba601005583e4a9f1308610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanScanSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanScanSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanScanSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2a2d146ce781dadcbe1ce2e99a8ddc3d9d73840cd9e5139d9cfc678f306a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupPlanScanSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.backupPlan.BackupPlanScanSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dea56a03f5730205b7fa54cf34ff3fe515996f6805c2bbb3342e9c7d7a8f3d20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="malwareScannerInput")
    def malware_scanner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "malwareScannerInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="scannerRoleArnInput")
    def scanner_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scannerRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="malwareScanner")
    def malware_scanner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "malwareScanner"))

    @malware_scanner.setter
    def malware_scanner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05751be3733af3c9c6f418e59e1c3d88b965d9ffe4575af6c5442c5cea00f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "malwareScanner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2af9a867a81a0d2469d8c3092aae3c53e47edf4aeb0f7f6cb33d9fb7c1f0228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scannerRoleArn")
    def scanner_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scannerRoleArn"))

    @scanner_role_arn.setter
    def scanner_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaff8b0b0449bb28c79eaf1d564be8571849dd7393f0b8c8923ed3c20910d0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scannerRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanScanSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanScanSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanScanSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f5a055115970177f55e08f138ce9f53487621809671f121915ccc592ef4d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BackupPlan",
    "BackupPlanAdvancedBackupSetting",
    "BackupPlanAdvancedBackupSettingList",
    "BackupPlanAdvancedBackupSettingOutputReference",
    "BackupPlanConfig",
    "BackupPlanRule",
    "BackupPlanRuleCopyAction",
    "BackupPlanRuleCopyActionLifecycle",
    "BackupPlanRuleCopyActionLifecycleOutputReference",
    "BackupPlanRuleCopyActionList",
    "BackupPlanRuleCopyActionOutputReference",
    "BackupPlanRuleLifecycle",
    "BackupPlanRuleLifecycleOutputReference",
    "BackupPlanRuleList",
    "BackupPlanRuleOutputReference",
    "BackupPlanRuleScanAction",
    "BackupPlanRuleScanActionList",
    "BackupPlanRuleScanActionOutputReference",
    "BackupPlanScanSetting",
    "BackupPlanScanSettingList",
    "BackupPlanScanSettingOutputReference",
]

publication.publish()

def _typecheckingstub__9979f5e54a053376e8436bc4239757c6c491cda68713f678d6cfc6e8b02743f5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRule, typing.Dict[builtins.str, typing.Any]]]],
    advanced_backup_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanAdvancedBackupSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scan_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanScanSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__e7183e80d6e6d4a7125cdf42d733a4d0958f99bd6c2bb034b989724a9126043d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37b7af5155f6608f16d98353349b7389d6347da4496c5954e3d67e5b6a675ed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanAdvancedBackupSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43dfa2074a7a607cdcdd63d8c3e1b3d34500c840d47117296eb0cad48114581(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3660e2b223879a6db23b3ba48710a4d134b8b4866b3a9e8384f8b4f60cdf8561(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanScanSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01382e476bdc7b6eda1be481c8aba8a165b4366423ac61cf18ee16665587294d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f503759d60b70d9eaf951fd706fe57359dceadbf50e93c6209a40defea829bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f843d3ec89b666cf51e3a390b6de3f9c80a9e22fdd1f5fbea1f7a4c3bcafdca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f614098e7cfd558729164da3e71f86f64a81843f0df4164f0de357a11f09f47(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b447b97f6adebd6ab93ff854c205b62585f5ca309b1acbf3e952a1b80f69446(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df743c033151fece2a56c018e7e7255ae1030797bd7ba27945776c6fb051873a(
    *,
    backup_options: typing.Mapping[builtins.str, builtins.str],
    resource_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47291a847481362f96848183747d4eaea0a1fa5eb96bfd4cb3377bb9a728f62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f405803ee24ac2f953d3e57870f5195863cd662fae6a90c958219e3c0ef7fac7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271832e23838b405149284727cb1659ee3848d64a697ca55337779f1e50c96f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1247ed3786ae7b622511dbcdce65b4aaf5235abbfbbdb1904ce190f8a6bd0abb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a22a509374ff47938cc08f4bc339d79fb7adf56483f02fd2b68be4d75cf6b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2288aa073d914b7b524b018d04c524f23620db8bb6b41d54a1b28a795b9e9397(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanAdvancedBackupSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc91b1b2f335d09c8456a4c1d351b6d7b5d01d394535d4bddccc52445e4d0e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4972770e8509c74767d4e8c6e082870a171f106a02ed8d57244c64906c260111(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478e83905ff1651a4f561892b20f854411b96ff6484d4eb96ec5be3e5eec9a46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f0abc4f4c96c501e23bfed76c80f2654349a6c221f88ee3fe12c5ff18fe0c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanAdvancedBackupSetting]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a891f209cbb80eb2aa97a48d94bee2010af3e9315d8b7f5ee02f308c69f977cc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRule, typing.Dict[builtins.str, typing.Any]]]],
    advanced_backup_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanAdvancedBackupSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scan_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanScanSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e34b1fa0d72b472701d62e322e33c1ec30f442aded06787c49db49aad74623(
    *,
    rule_name: builtins.str,
    target_vault_name: builtins.str,
    completion_window: typing.Optional[jsii.Number] = None,
    copy_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleCopyAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_continuous_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lifecycle: typing.Optional[typing.Union[BackupPlanRuleLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_point_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    scan_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleScanAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    schedule_expression_timezone: typing.Optional[builtins.str] = None,
    start_window: typing.Optional[jsii.Number] = None,
    target_logically_air_gapped_backup_vault_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9054ccf9e58c637abc10af00c7bf8dbbe70b6a4ee95a9726f0bb4bbc0d1f28f(
    *,
    destination_vault_arn: builtins.str,
    lifecycle: typing.Optional[typing.Union[BackupPlanRuleCopyActionLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb7ecdc70bb243938f32dca7924f4e514d13ae0d71790c921a4baccc39abdc4(
    *,
    cold_storage_after: typing.Optional[jsii.Number] = None,
    delete_after: typing.Optional[jsii.Number] = None,
    opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c662ff4237651d9a9932a16089a8f2300e809def0159358fb92f29f6b8f021e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c58924fcab4d43e1f48b125015e9eec29c32742e258828dc44496c813456b94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbe9f299f3900b59229510df6637c3d8c75db22e0bbaaeb04086fd78be991e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9402f8cf6667e6008c88abe9b1ed75c6cd881f21b764fd832274782523d10a3b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fadc495f97cecd913a92029a9d12c2bc4736d2ee04ba6f72125cfa40dedfa69(
    value: typing.Optional[BackupPlanRuleCopyActionLifecycle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8f0a4fc5d2e812de77cf63e3599185bc34e0502989a485892a145d1741e549(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5069267b6cec77ef3937cf1f149ceec401d775aa717ba51cbb71d9d84fd78f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafadc0a012816309ba93bc4f03a36545d3a6ef618ed96d132bd8e9fbd5b5fd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05bbdc801c337fde075bdb932f659b66ce5a024a375162ea2051998e9150c86(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05e9dc8e797082476a7eee5a5fd25a6dc524d0ee8e79cd2d232a4330a3132ba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b34f621ea1cf20cb21825b5a4bf14174007394308a0981aa5dbb98d13d0a8ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleCopyAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a9ac2e07f5048fe5fb4725ea1ae6fb1878e00d729635fbcc4d75d111e27873(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e14d73e68915c36e8cf0904aee8bae68b51b3b0628f442d606f128c76bd993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33038444ecb7712d911ded362d45472243a23772dc285cb387085b3ccbb67a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleCopyAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8ea11b215000a780a7b06973f5bd904615f183e349e6d6e3bdacf4b2cc54b2(
    *,
    cold_storage_after: typing.Optional[jsii.Number] = None,
    delete_after: typing.Optional[jsii.Number] = None,
    opt_in_to_archive_for_supported_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8b798e5cdafb7a8045ea92c22512cd2442cef3d8bce4fc26f4d8447c9869ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d3201f7acbf4a0c6049a713f8fa4dea942dc199240b1ad89116440e5cad13b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacb59d48c7b45d11a8fea7f5efd6cf93c68ff663ce865709d3dde5a6a5fd1a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d408b9982e994382a02fe8299e19c5751a43a990d69619e57415d56084aa4eef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856767666bb64a8da6c6c7e9eb0115b09fab3c4e38b3bfdeb43abf5897dafdbd(
    value: typing.Optional[BackupPlanRuleLifecycle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7d0d0dd830d41a2b515000f86a95287e2c65a213ac87f4415c73808f585314(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1844d2ce8c1e580dd171d88679440dbb219b9390991cf9776f950072f6c87e4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6050802970bc5d995db6dff317f667a5686bf015d73af61eee5514d4a19d39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940d0bdfd2985ae0f7c378821a0552bf7997893a7e43f33ffe61e7ec2b7749bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e3956d473049a0938c41992b17309a20de5acbec48377a5b4dd0abbcfd4538(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f7bbb9b74b30354e62063b779eb828164ad9d2532fcae6efad4de2ee4a0247(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c531d90d1356b3ed40e51c5a1978e568b507296731b8e9e6f9fe980404a9e73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff25f9d69486d06cf8b90a93ada17ac8e119a9da8a67f6e2f793543a1890837(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleCopyAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560d2e3cc329c6200115816b383f2c869e3ad0a86efd7439c318cb3a18bb10a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupPlanRuleScanAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b56f73475b6c7d1959d214747f790d863e3c84c558245c29bd2ba9b0382484f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582837cd777dfed0e74f2a14002e89ec643054b09766f6ace3b9c03568a6ab70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5b874fe3574b521aa2f219e647e0ab92aac75a532cbc2d01e22b7c67b67c78(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d60b6a382f6d79f7fa735dc42b4884c964badbbef3e6b3e18befff58224a32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9d532b285b10c812c1a631d86e204376109839a104f8aa19fcebacbe8455c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6defc5d81c4f09ad296eb6d7e46596cebcd1f741a3b848bd053b7dc4966e352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3341b4e67790a5d32c2e850115a3dc66d4887e7cfc281efaa454d1b83e7161(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a51d3042816760e27a0b1ca15c67c78efb6fd3e1c727463f9c647f57f9110a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fc27e206f6fc5d0511077cb142b1cf05847d352ebbc6d253137b9ae25268e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0987a14daa01658b8feb12d62180f1bc7e115aac99c93854eb3f19817d0a84c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2935de05fb6b87660c34dd0582eaa6a6626659f9bbf351ff3d97907e12b66f1b(
    *,
    malware_scanner: builtins.str,
    scan_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4173e56dc67ad0e3a0441b1f3702e5151f9f40915d2776749c70c67709df5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe2aa948e5337b1acdbf2a1d7eae838cb25388cddd933fa4c64ff0bbe48f246(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701165c026fc9405bd83d8ea4833cf7d4fc8f7c54050b875b378572d268f45e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe05397426c20a9ccfe0e740df0a8e529cf3080a3113dc91d7a76db6f4d7571(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4974431911c9e19fd4bb476c68b7151abf8db73ac181175726c84b7ef04d56aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335014d3e5e4abdb513ce5b57fd748dd8cf300a191403bb9c61a70c9b1efbaaf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanRuleScanAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d3199c3f5bfacfba10fa252b22953ad9384293ef22f32b53c6c9c611d7a968(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b2188db7c6c92fddc8d2ac986d251b14f0c89d312715e4da5f5d90682cf8d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e859c68f3292f22352033b713ea5542c7d268fc5516ef5c04b611c8bb46ab48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a180d62b2f7cfc8a3ac122d82e18588fcf61369b5a42330e236cb4e9d1e8a3a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanRuleScanAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a7240b66e724b26884611dafab1a4321bda3b0caf85dcca978c10f440540fb(
    *,
    malware_scanner: builtins.str,
    resource_types: typing.Sequence[builtins.str],
    scanner_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa089731b0da72d0ea8bae39f2951cd9eb07508568c4de698fe4dce9fc2911a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3559f6e71c2153357cf8c4afaa4fcfab8c2f66bcfa7f5823a73388c92e813e8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b226332bd76b37c7a5c984c1ce54a53e6604f89a00dd4f82468c7ba11efa9fd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fd43040a8f00c130ee77130a8ec7270c38260570a6d6c7ddbae33aa4cf7b69(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c14cfbfc26bee3755cfcd8c96961de3dfe7e6164ba601005583e4a9f1308610(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2a2d146ce781dadcbe1ce2e99a8ddc3d9d73840cd9e5139d9cfc678f306a61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupPlanScanSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea56a03f5730205b7fa54cf34ff3fe515996f6805c2bbb3342e9c7d7a8f3d20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05751be3733af3c9c6f418e59e1c3d88b965d9ffe4575af6c5442c5cea00f5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2af9a867a81a0d2469d8c3092aae3c53e47edf4aeb0f7f6cb33d9fb7c1f0228(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaff8b0b0449bb28c79eaf1d564be8571849dd7393f0b8c8923ed3c20910d0a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f5a055115970177f55e08f138ce9f53487621809671f121915ccc592ef4d61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupPlanScanSetting]],
) -> None:
    """Type checking stubs"""
    pass
