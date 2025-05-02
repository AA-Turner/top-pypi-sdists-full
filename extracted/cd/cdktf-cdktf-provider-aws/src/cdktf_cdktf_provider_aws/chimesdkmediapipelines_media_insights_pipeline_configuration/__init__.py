r'''
# `aws_chimesdkmediapipelines_media_insights_pipeline_configuration`

Refer to the Terraform Registry for docs: [`aws_chimesdkmediapipelines_media_insights_pipeline_configuration`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration).
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


class ChimesdkmediapipelinesMediaInsightsPipelineConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration aws_chimesdkmediapipelines_media_insights_pipeline_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        elements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        resource_access_role_arn: builtins.str,
        real_time_alert_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration aws_chimesdkmediapipelines_media_insights_pipeline_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param elements: elements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#elements ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#elements}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#name}.
        :param resource_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#resource_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#resource_access_role_arn}.
        :param real_time_alert_configuration: real_time_alert_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#real_time_alert_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#real_time_alert_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags_all ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#timeouts ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa8b7c1b288db26f5f503b3326290886ed2ebc0657038bd3215bbd8048a4300)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig(
            elements=elements,
            name=name,
            resource_access_role_arn=resource_access_role_arn,
            real_time_alert_configuration=real_time_alert_configuration,
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
        '''Generates CDKTF code for importing a ChimesdkmediapipelinesMediaInsightsPipelineConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ChimesdkmediapipelinesMediaInsightsPipelineConfiguration to import.
        :param import_from_id: The id of the existing ChimesdkmediapipelinesMediaInsightsPipelineConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ChimesdkmediapipelinesMediaInsightsPipelineConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c79ad8fd91299c571793385bd9597e992db17a8cae9173dda4cad3872938fc0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putElements")
    def put_elements(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88251684cf501836da2199a21d345ca479a66d994bf0244805cda64b582dea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElements", [value]))

    @jsii.member(jsii_name="putRealTimeAlertConfiguration")
    def put_real_time_alert_configuration(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules", typing.Dict[builtins.str, typing.Any]]]],
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rules ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rules}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#disabled ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#disabled}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration(
            rules=rules, disabled=disabled
        )

        return typing.cast(None, jsii.invoke(self, "putRealTimeAlertConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#create ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#delete ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#update ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#update}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetRealTimeAlertConfiguration")
    def reset_real_time_alert_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealTimeAlertConfiguration", []))

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
    @jsii.member(jsii_name="elements")
    def elements(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList", jsii.get(self, "elements"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="realTimeAlertConfiguration")
    def real_time_alert_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference", jsii.get(self, "realTimeAlertConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="elementsInput")
    def elements_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements"]]], jsii.get(self, "elementsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="realTimeAlertConfigurationInput")
    def real_time_alert_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration"], jsii.get(self, "realTimeAlertConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceAccessRoleArnInput")
    def resource_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceAccessRoleArnInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c907cffed96dced25641d3490249f15f431b55fcd42125396be7af55a63753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceAccessRoleArn")
    def resource_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceAccessRoleArn"))

    @resource_access_role_arn.setter
    def resource_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad4497bf9c4b14405b7c8adf0f7c83dc4db834c6e4c69de20321338b44adfe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c345da0278a9dcd5ed788cb047e9ac27c7b585d2a215f01d5099c549a49307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b3b62f734eeada67de411869349f367e53a947c075ade6111fcc260f657ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "elements": "elements",
        "name": "name",
        "resource_access_role_arn": "resourceAccessRoleArn",
        "real_time_alert_configuration": "realTimeAlertConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        elements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        resource_access_role_arn: builtins.str,
        real_time_alert_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param elements: elements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#elements ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#elements}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#name}.
        :param resource_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#resource_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#resource_access_role_arn}.
        :param real_time_alert_configuration: real_time_alert_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#real_time_alert_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#real_time_alert_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags_all ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#timeouts ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(real_time_alert_configuration, dict):
            real_time_alert_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration(**real_time_alert_configuration)
        if isinstance(timeouts, dict):
            timeouts = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a43c2a778ff47a0f92d5bc26d983d258e7916e7cb812483fe16d21e260145d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument elements", value=elements, expected_type=type_hints["elements"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_access_role_arn", value=resource_access_role_arn, expected_type=type_hints["resource_access_role_arn"])
            check_type(argname="argument real_time_alert_configuration", value=real_time_alert_configuration, expected_type=type_hints["real_time_alert_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "elements": elements,
            "name": name,
            "resource_access_role_arn": resource_access_role_arn,
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
        if real_time_alert_configuration is not None:
            self._values["real_time_alert_configuration"] = real_time_alert_configuration
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
    def elements(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements"]]:
        '''elements block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#elements ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#elements}
        '''
        result = self._values.get("elements")
        assert result is not None, "Required property 'elements' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_access_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#resource_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#resource_access_role_arn}.'''
        result = self._values.get("resource_access_role_arn")
        assert result is not None, "Required property 'resource_access_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def real_time_alert_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration"]:
        '''real_time_alert_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#real_time_alert_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#real_time_alert_configuration}
        '''
        result = self._values.get("real_time_alert_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags_all ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#timeouts ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "amazon_transcribe_call_analytics_processor_configuration": "amazonTranscribeCallAnalyticsProcessorConfiguration",
        "amazon_transcribe_processor_configuration": "amazonTranscribeProcessorConfiguration",
        "kinesis_data_stream_sink_configuration": "kinesisDataStreamSinkConfiguration",
        "lambda_function_sink_configuration": "lambdaFunctionSinkConfiguration",
        "s3_recording_sink_configuration": "s3RecordingSinkConfiguration",
        "sns_topic_sink_configuration": "snsTopicSinkConfiguration",
        "sqs_queue_sink_configuration": "sqsQueueSinkConfiguration",
        "voice_analytics_processor_configuration": "voiceAnalyticsProcessorConfiguration",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements:
    def __init__(
        self,
        *,
        type: builtins.str,
        amazon_transcribe_call_analytics_processor_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        amazon_transcribe_processor_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_data_stream_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_recording_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sns_topic_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        voice_analytics_processor_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#type}.
        :param amazon_transcribe_call_analytics_processor_configuration: amazon_transcribe_call_analytics_processor_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#amazon_transcribe_call_analytics_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#amazon_transcribe_call_analytics_processor_configuration}
        :param amazon_transcribe_processor_configuration: amazon_transcribe_processor_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#amazon_transcribe_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#amazon_transcribe_processor_configuration}
        :param kinesis_data_stream_sink_configuration: kinesis_data_stream_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#kinesis_data_stream_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#kinesis_data_stream_sink_configuration}
        :param lambda_function_sink_configuration: lambda_function_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#lambda_function_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#lambda_function_sink_configuration}
        :param s3_recording_sink_configuration: s3_recording_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#s3_recording_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#s3_recording_sink_configuration}
        :param sns_topic_sink_configuration: sns_topic_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sns_topic_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sns_topic_sink_configuration}
        :param sqs_queue_sink_configuration: sqs_queue_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sqs_queue_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sqs_queue_sink_configuration}
        :param voice_analytics_processor_configuration: voice_analytics_processor_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_analytics_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_analytics_processor_configuration}
        '''
        if isinstance(amazon_transcribe_call_analytics_processor_configuration, dict):
            amazon_transcribe_call_analytics_processor_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration(**amazon_transcribe_call_analytics_processor_configuration)
        if isinstance(amazon_transcribe_processor_configuration, dict):
            amazon_transcribe_processor_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration(**amazon_transcribe_processor_configuration)
        if isinstance(kinesis_data_stream_sink_configuration, dict):
            kinesis_data_stream_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration(**kinesis_data_stream_sink_configuration)
        if isinstance(lambda_function_sink_configuration, dict):
            lambda_function_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration(**lambda_function_sink_configuration)
        if isinstance(s3_recording_sink_configuration, dict):
            s3_recording_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration(**s3_recording_sink_configuration)
        if isinstance(sns_topic_sink_configuration, dict):
            sns_topic_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration(**sns_topic_sink_configuration)
        if isinstance(sqs_queue_sink_configuration, dict):
            sqs_queue_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration(**sqs_queue_sink_configuration)
        if isinstance(voice_analytics_processor_configuration, dict):
            voice_analytics_processor_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration(**voice_analytics_processor_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1bdfe34057141e6e19d04c8c2be4978fb95a150480db73b8cd7b9228820b1c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument amazon_transcribe_call_analytics_processor_configuration", value=amazon_transcribe_call_analytics_processor_configuration, expected_type=type_hints["amazon_transcribe_call_analytics_processor_configuration"])
            check_type(argname="argument amazon_transcribe_processor_configuration", value=amazon_transcribe_processor_configuration, expected_type=type_hints["amazon_transcribe_processor_configuration"])
            check_type(argname="argument kinesis_data_stream_sink_configuration", value=kinesis_data_stream_sink_configuration, expected_type=type_hints["kinesis_data_stream_sink_configuration"])
            check_type(argname="argument lambda_function_sink_configuration", value=lambda_function_sink_configuration, expected_type=type_hints["lambda_function_sink_configuration"])
            check_type(argname="argument s3_recording_sink_configuration", value=s3_recording_sink_configuration, expected_type=type_hints["s3_recording_sink_configuration"])
            check_type(argname="argument sns_topic_sink_configuration", value=sns_topic_sink_configuration, expected_type=type_hints["sns_topic_sink_configuration"])
            check_type(argname="argument sqs_queue_sink_configuration", value=sqs_queue_sink_configuration, expected_type=type_hints["sqs_queue_sink_configuration"])
            check_type(argname="argument voice_analytics_processor_configuration", value=voice_analytics_processor_configuration, expected_type=type_hints["voice_analytics_processor_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if amazon_transcribe_call_analytics_processor_configuration is not None:
            self._values["amazon_transcribe_call_analytics_processor_configuration"] = amazon_transcribe_call_analytics_processor_configuration
        if amazon_transcribe_processor_configuration is not None:
            self._values["amazon_transcribe_processor_configuration"] = amazon_transcribe_processor_configuration
        if kinesis_data_stream_sink_configuration is not None:
            self._values["kinesis_data_stream_sink_configuration"] = kinesis_data_stream_sink_configuration
        if lambda_function_sink_configuration is not None:
            self._values["lambda_function_sink_configuration"] = lambda_function_sink_configuration
        if s3_recording_sink_configuration is not None:
            self._values["s3_recording_sink_configuration"] = s3_recording_sink_configuration
        if sns_topic_sink_configuration is not None:
            self._values["sns_topic_sink_configuration"] = sns_topic_sink_configuration
        if sqs_queue_sink_configuration is not None:
            self._values["sqs_queue_sink_configuration"] = sqs_queue_sink_configuration
        if voice_analytics_processor_configuration is not None:
            self._values["voice_analytics_processor_configuration"] = voice_analytics_processor_configuration

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def amazon_transcribe_call_analytics_processor_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration"]:
        '''amazon_transcribe_call_analytics_processor_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#amazon_transcribe_call_analytics_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#amazon_transcribe_call_analytics_processor_configuration}
        '''
        result = self._values.get("amazon_transcribe_call_analytics_processor_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration"], result)

    @builtins.property
    def amazon_transcribe_processor_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration"]:
        '''amazon_transcribe_processor_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#amazon_transcribe_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#amazon_transcribe_processor_configuration}
        '''
        result = self._values.get("amazon_transcribe_processor_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration"], result)

    @builtins.property
    def kinesis_data_stream_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration"]:
        '''kinesis_data_stream_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#kinesis_data_stream_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#kinesis_data_stream_sink_configuration}
        '''
        result = self._values.get("kinesis_data_stream_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration"], result)

    @builtins.property
    def lambda_function_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration"]:
        '''lambda_function_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#lambda_function_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#lambda_function_sink_configuration}
        '''
        result = self._values.get("lambda_function_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration"], result)

    @builtins.property
    def s3_recording_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration"]:
        '''s3_recording_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#s3_recording_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#s3_recording_sink_configuration}
        '''
        result = self._values.get("s3_recording_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration"], result)

    @builtins.property
    def sns_topic_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration"]:
        '''sns_topic_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sns_topic_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sns_topic_sink_configuration}
        '''
        result = self._values.get("sns_topic_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration"], result)

    @builtins.property
    def sqs_queue_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration"]:
        '''sqs_queue_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sqs_queue_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sqs_queue_sink_configuration}
        '''
        result = self._values.get("sqs_queue_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration"], result)

    @builtins.property
    def voice_analytics_processor_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration"]:
        '''voice_analytics_processor_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_analytics_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_analytics_processor_configuration}
        '''
        result = self._values.get("voice_analytics_processor_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "language_code": "languageCode",
        "call_analytics_stream_categories": "callAnalyticsStreamCategories",
        "content_identification_type": "contentIdentificationType",
        "content_redaction_type": "contentRedactionType",
        "enable_partial_results_stabilization": "enablePartialResultsStabilization",
        "filter_partial_results": "filterPartialResults",
        "language_model_name": "languageModelName",
        "partial_results_stability": "partialResultsStability",
        "pii_entity_types": "piiEntityTypes",
        "post_call_analytics_settings": "postCallAnalyticsSettings",
        "vocabulary_filter_method": "vocabularyFilterMethod",
        "vocabulary_filter_name": "vocabularyFilterName",
        "vocabulary_name": "vocabularyName",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration:
    def __init__(
        self,
        *,
        language_code: builtins.str,
        call_analytics_stream_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_identification_type: typing.Optional[builtins.str] = None,
        content_redaction_type: typing.Optional[builtins.str] = None,
        enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        post_call_analytics_settings: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        vocabulary_filter_method: typing.Optional[builtins.str] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.
        :param call_analytics_stream_categories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#call_analytics_stream_categories ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#call_analytics_stream_categories}.
        :param content_identification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.
        :param content_redaction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.
        :param enable_partial_results_stabilization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.
        :param filter_partial_results: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.
        :param language_model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.
        :param partial_results_stability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.
        :param pii_entity_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.
        :param post_call_analytics_settings: post_call_analytics_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#post_call_analytics_settings ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#post_call_analytics_settings}
        :param vocabulary_filter_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.
        :param vocabulary_filter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.
        :param vocabulary_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.
        '''
        if isinstance(post_call_analytics_settings, dict):
            post_call_analytics_settings = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings(**post_call_analytics_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8596c248f2eb5452c156c07215618acdac32c475d27f91c7c6875e27ddfa69e7)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument call_analytics_stream_categories", value=call_analytics_stream_categories, expected_type=type_hints["call_analytics_stream_categories"])
            check_type(argname="argument content_identification_type", value=content_identification_type, expected_type=type_hints["content_identification_type"])
            check_type(argname="argument content_redaction_type", value=content_redaction_type, expected_type=type_hints["content_redaction_type"])
            check_type(argname="argument enable_partial_results_stabilization", value=enable_partial_results_stabilization, expected_type=type_hints["enable_partial_results_stabilization"])
            check_type(argname="argument filter_partial_results", value=filter_partial_results, expected_type=type_hints["filter_partial_results"])
            check_type(argname="argument language_model_name", value=language_model_name, expected_type=type_hints["language_model_name"])
            check_type(argname="argument partial_results_stability", value=partial_results_stability, expected_type=type_hints["partial_results_stability"])
            check_type(argname="argument pii_entity_types", value=pii_entity_types, expected_type=type_hints["pii_entity_types"])
            check_type(argname="argument post_call_analytics_settings", value=post_call_analytics_settings, expected_type=type_hints["post_call_analytics_settings"])
            check_type(argname="argument vocabulary_filter_method", value=vocabulary_filter_method, expected_type=type_hints["vocabulary_filter_method"])
            check_type(argname="argument vocabulary_filter_name", value=vocabulary_filter_name, expected_type=type_hints["vocabulary_filter_name"])
            check_type(argname="argument vocabulary_name", value=vocabulary_name, expected_type=type_hints["vocabulary_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
        }
        if call_analytics_stream_categories is not None:
            self._values["call_analytics_stream_categories"] = call_analytics_stream_categories
        if content_identification_type is not None:
            self._values["content_identification_type"] = content_identification_type
        if content_redaction_type is not None:
            self._values["content_redaction_type"] = content_redaction_type
        if enable_partial_results_stabilization is not None:
            self._values["enable_partial_results_stabilization"] = enable_partial_results_stabilization
        if filter_partial_results is not None:
            self._values["filter_partial_results"] = filter_partial_results
        if language_model_name is not None:
            self._values["language_model_name"] = language_model_name
        if partial_results_stability is not None:
            self._values["partial_results_stability"] = partial_results_stability
        if pii_entity_types is not None:
            self._values["pii_entity_types"] = pii_entity_types
        if post_call_analytics_settings is not None:
            self._values["post_call_analytics_settings"] = post_call_analytics_settings
        if vocabulary_filter_method is not None:
            self._values["vocabulary_filter_method"] = vocabulary_filter_method
        if vocabulary_filter_name is not None:
            self._values["vocabulary_filter_name"] = vocabulary_filter_name
        if vocabulary_name is not None:
            self._values["vocabulary_name"] = vocabulary_name

    @builtins.property
    def language_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.'''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def call_analytics_stream_categories(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#call_analytics_stream_categories ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#call_analytics_stream_categories}.'''
        result = self._values.get("call_analytics_stream_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content_identification_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.'''
        result = self._values.get("content_identification_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_redaction_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.'''
        result = self._values.get("content_redaction_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_partial_results_stabilization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.'''
        result = self._values.get("enable_partial_results_stabilization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filter_partial_results(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.'''
        result = self._values.get("filter_partial_results")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def language_model_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.'''
        result = self._values.get("language_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partial_results_stability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.'''
        result = self._values.get("partial_results_stability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pii_entity_types(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.'''
        result = self._values.get("pii_entity_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_call_analytics_settings(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings"]:
        '''post_call_analytics_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#post_call_analytics_settings ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#post_call_analytics_settings}
        '''
        result = self._values.get("post_call_analytics_settings")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings"], result)

    @builtins.property
    def vocabulary_filter_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.'''
        result = self._values.get("vocabulary_filter_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_filter_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.'''
        result = self._values.get("vocabulary_filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.'''
        result = self._values.get("vocabulary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f75941048901685858c0a2d6f04932044fa72485705afc8278c09627cfc3aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostCallAnalyticsSettings")
    def put_post_call_analytics_settings(
        self,
        *,
        data_access_role_arn: builtins.str,
        output_location: builtins.str,
        content_redaction_output: typing.Optional[builtins.str] = None,
        output_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#data_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#data_access_role_arn}.
        :param output_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_location ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_location}.
        :param content_redaction_output: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_output ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_output}.
        :param output_encryption_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_encryption_kms_key_id ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_encryption_kms_key_id}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings(
            data_access_role_arn=data_access_role_arn,
            output_location=output_location,
            content_redaction_output=content_redaction_output,
            output_encryption_kms_key_id=output_encryption_kms_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putPostCallAnalyticsSettings", [value]))

    @jsii.member(jsii_name="resetCallAnalyticsStreamCategories")
    def reset_call_analytics_stream_categories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallAnalyticsStreamCategories", []))

    @jsii.member(jsii_name="resetContentIdentificationType")
    def reset_content_identification_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentIdentificationType", []))

    @jsii.member(jsii_name="resetContentRedactionType")
    def reset_content_redaction_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentRedactionType", []))

    @jsii.member(jsii_name="resetEnablePartialResultsStabilization")
    def reset_enable_partial_results_stabilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePartialResultsStabilization", []))

    @jsii.member(jsii_name="resetFilterPartialResults")
    def reset_filter_partial_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterPartialResults", []))

    @jsii.member(jsii_name="resetLanguageModelName")
    def reset_language_model_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageModelName", []))

    @jsii.member(jsii_name="resetPartialResultsStability")
    def reset_partial_results_stability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartialResultsStability", []))

    @jsii.member(jsii_name="resetPiiEntityTypes")
    def reset_pii_entity_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPiiEntityTypes", []))

    @jsii.member(jsii_name="resetPostCallAnalyticsSettings")
    def reset_post_call_analytics_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostCallAnalyticsSettings", []))

    @jsii.member(jsii_name="resetVocabularyFilterMethod")
    def reset_vocabulary_filter_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyFilterMethod", []))

    @jsii.member(jsii_name="resetVocabularyFilterName")
    def reset_vocabulary_filter_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyFilterName", []))

    @jsii.member(jsii_name="resetVocabularyName")
    def reset_vocabulary_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyName", []))

    @builtins.property
    @jsii.member(jsii_name="postCallAnalyticsSettings")
    def post_call_analytics_settings(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference", jsii.get(self, "postCallAnalyticsSettings"))

    @builtins.property
    @jsii.member(jsii_name="callAnalyticsStreamCategoriesInput")
    def call_analytics_stream_categories_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "callAnalyticsStreamCategoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="contentIdentificationTypeInput")
    def content_identification_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentIdentificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentRedactionTypeInput")
    def content_redaction_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentRedactionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePartialResultsStabilizationInput")
    def enable_partial_results_stabilization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePartialResultsStabilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterPartialResultsInput")
    def filter_partial_results_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filterPartialResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="languageModelNameInput")
    def language_model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageModelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="partialResultsStabilityInput")
    def partial_results_stability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partialResultsStabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="piiEntityTypesInput")
    def pii_entity_types_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "piiEntityTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="postCallAnalyticsSettingsInput")
    def post_call_analytics_settings_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings"], jsii.get(self, "postCallAnalyticsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterMethodInput")
    def vocabulary_filter_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterNameInput")
    def vocabulary_filter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyNameInput")
    def vocabulary_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="callAnalyticsStreamCategories")
    def call_analytics_stream_categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "callAnalyticsStreamCategories"))

    @call_analytics_stream_categories.setter
    def call_analytics_stream_categories(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a529ddb0b3cc0ed142bea462b1080e2d3675cb3790c0430a002a11941a9dd124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callAnalyticsStreamCategories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentIdentificationType")
    def content_identification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentIdentificationType"))

    @content_identification_type.setter
    def content_identification_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb5bffabd7e83f46ce4534501ed85c31fed02270f5d353ccbc66d07d21e5035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentIdentificationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentRedactionType")
    def content_redaction_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentRedactionType"))

    @content_redaction_type.setter
    def content_redaction_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24461617814b9ac127b61d6f2bda43525a55f54d81c16711964c1bc356971dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentRedactionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePartialResultsStabilization")
    def enable_partial_results_stabilization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePartialResultsStabilization"))

    @enable_partial_results_stabilization.setter
    def enable_partial_results_stabilization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075b43fca4487ffbd8a601e4f560a70e79e5b0d2468ec14395d70189ad1144c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePartialResultsStabilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterPartialResults")
    def filter_partial_results(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filterPartialResults"))

    @filter_partial_results.setter
    def filter_partial_results(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4078e374c823b68cc038121447d96cc41ca6f350074943c6cbf5cb295f2055e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPartialResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0f05778f9aace52f20ce376e86eefea605f8c546becad0290ded3dcc0028f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageModelName")
    def language_model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageModelName"))

    @language_model_name.setter
    def language_model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35c1f1377977509bf023ee7a2066d111e0cdc9843da23debd77f91d0854e7c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageModelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partialResultsStability")
    def partial_results_stability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partialResultsStability"))

    @partial_results_stability.setter
    def partial_results_stability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd9092d05edbf76373467c80f5130e4c2d1514101aef2dc89d28577918decae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partialResultsStability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="piiEntityTypes")
    def pii_entity_types(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "piiEntityTypes"))

    @pii_entity_types.setter
    def pii_entity_types(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7da26b477067afc3fce9b665c40f6cbecc7ff5959349d1c6c430a6a47e86a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "piiEntityTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterMethod")
    def vocabulary_filter_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterMethod"))

    @vocabulary_filter_method.setter
    def vocabulary_filter_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7bf2cac204457d789fab8a62e34cb528f4a39dff20692a57b286f73ad6f7a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterName")
    def vocabulary_filter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterName"))

    @vocabulary_filter_name.setter
    def vocabulary_filter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e302f0ad41801ec5959d8a70a57b6c2235e93ead2b99e40b4d4ced1945e50d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyName")
    def vocabulary_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyName"))

    @vocabulary_name.setter
    def vocabulary_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1601973212d01aa06057c8e90636a3e5a04c0e5aff15494c7aebefdd74ad46b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a20fb3c788f81316cc1d0a06c0cd060428bfa01255335102ee4d5bd1d363e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings",
    jsii_struct_bases=[],
    name_mapping={
        "data_access_role_arn": "dataAccessRoleArn",
        "output_location": "outputLocation",
        "content_redaction_output": "contentRedactionOutput",
        "output_encryption_kms_key_id": "outputEncryptionKmsKeyId",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings:
    def __init__(
        self,
        *,
        data_access_role_arn: builtins.str,
        output_location: builtins.str,
        content_redaction_output: typing.Optional[builtins.str] = None,
        output_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#data_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#data_access_role_arn}.
        :param output_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_location ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_location}.
        :param content_redaction_output: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_output ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_output}.
        :param output_encryption_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_encryption_kms_key_id ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_encryption_kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a46200f09fb43794ef1d9fd2161ae09dfc1d0e6b3bab0016590b61e38d6b39)
            check_type(argname="argument data_access_role_arn", value=data_access_role_arn, expected_type=type_hints["data_access_role_arn"])
            check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
            check_type(argname="argument content_redaction_output", value=content_redaction_output, expected_type=type_hints["content_redaction_output"])
            check_type(argname="argument output_encryption_kms_key_id", value=output_encryption_kms_key_id, expected_type=type_hints["output_encryption_kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_access_role_arn": data_access_role_arn,
            "output_location": output_location,
        }
        if content_redaction_output is not None:
            self._values["content_redaction_output"] = content_redaction_output
        if output_encryption_kms_key_id is not None:
            self._values["output_encryption_kms_key_id"] = output_encryption_kms_key_id

    @builtins.property
    def data_access_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#data_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#data_access_role_arn}.'''
        result = self._values.get("data_access_role_arn")
        assert result is not None, "Required property 'data_access_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_location ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_location}.'''
        result = self._values.get("output_location")
        assert result is not None, "Required property 'output_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_redaction_output(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_output ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_output}.'''
        result = self._values.get("content_redaction_output")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_encryption_kms_key_id ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_encryption_kms_key_id}.'''
        result = self._values.get("output_encryption_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce17813a92d1897dfea56d6554f5bda72473b727ebc4056bf65f61882e87f3bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContentRedactionOutput")
    def reset_content_redaction_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentRedactionOutput", []))

    @jsii.member(jsii_name="resetOutputEncryptionKmsKeyId")
    def reset_output_encryption_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputEncryptionKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="contentRedactionOutputInput")
    def content_redaction_output_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentRedactionOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="dataAccessRoleArnInput")
    def data_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataAccessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="outputEncryptionKmsKeyIdInput")
    def output_encryption_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputEncryptionKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="outputLocationInput")
    def output_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="contentRedactionOutput")
    def content_redaction_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentRedactionOutput"))

    @content_redaction_output.setter
    def content_redaction_output(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09690ca9003c31f63cb8c194e855aa9b0c2274e6864718e3262d01921f6730d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentRedactionOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessRoleArn")
    def data_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataAccessRoleArn"))

    @data_access_role_arn.setter
    def data_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb39826421d92c1bc4ad102d875976ee6d6cd10cf8ba3b49466c8757cd16e999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputEncryptionKmsKeyId")
    def output_encryption_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputEncryptionKmsKeyId"))

    @output_encryption_kms_key_id.setter
    def output_encryption_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb2cc97b19f3c9660b1088c18933ad61a8f142bc7160f70e48db7c29d99edff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputEncryptionKmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputLocation")
    def output_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputLocation"))

    @output_location.setter
    def output_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc1bb024355e5d475f8c97837efefe72775fae9833e6c6eb4dca9917c28ba96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fffd27b2a0197783e58ae2f78af67a1897a8799660f3c061ec1cc72efc30fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "language_code": "languageCode",
        "content_identification_type": "contentIdentificationType",
        "content_redaction_type": "contentRedactionType",
        "enable_partial_results_stabilization": "enablePartialResultsStabilization",
        "filter_partial_results": "filterPartialResults",
        "language_model_name": "languageModelName",
        "partial_results_stability": "partialResultsStability",
        "pii_entity_types": "piiEntityTypes",
        "show_speaker_label": "showSpeakerLabel",
        "vocabulary_filter_method": "vocabularyFilterMethod",
        "vocabulary_filter_name": "vocabularyFilterName",
        "vocabulary_name": "vocabularyName",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration:
    def __init__(
        self,
        *,
        language_code: builtins.str,
        content_identification_type: typing.Optional[builtins.str] = None,
        content_redaction_type: typing.Optional[builtins.str] = None,
        enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        show_speaker_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vocabulary_filter_method: typing.Optional[builtins.str] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.
        :param content_identification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.
        :param content_redaction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.
        :param enable_partial_results_stabilization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.
        :param filter_partial_results: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.
        :param language_model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.
        :param partial_results_stability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.
        :param pii_entity_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.
        :param show_speaker_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#show_speaker_label ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#show_speaker_label}.
        :param vocabulary_filter_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.
        :param vocabulary_filter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.
        :param vocabulary_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09fbf37f49c3812cc245192a4bde01575a26cec538ce168dc00b7b1d1544ea4)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument content_identification_type", value=content_identification_type, expected_type=type_hints["content_identification_type"])
            check_type(argname="argument content_redaction_type", value=content_redaction_type, expected_type=type_hints["content_redaction_type"])
            check_type(argname="argument enable_partial_results_stabilization", value=enable_partial_results_stabilization, expected_type=type_hints["enable_partial_results_stabilization"])
            check_type(argname="argument filter_partial_results", value=filter_partial_results, expected_type=type_hints["filter_partial_results"])
            check_type(argname="argument language_model_name", value=language_model_name, expected_type=type_hints["language_model_name"])
            check_type(argname="argument partial_results_stability", value=partial_results_stability, expected_type=type_hints["partial_results_stability"])
            check_type(argname="argument pii_entity_types", value=pii_entity_types, expected_type=type_hints["pii_entity_types"])
            check_type(argname="argument show_speaker_label", value=show_speaker_label, expected_type=type_hints["show_speaker_label"])
            check_type(argname="argument vocabulary_filter_method", value=vocabulary_filter_method, expected_type=type_hints["vocabulary_filter_method"])
            check_type(argname="argument vocabulary_filter_name", value=vocabulary_filter_name, expected_type=type_hints["vocabulary_filter_name"])
            check_type(argname="argument vocabulary_name", value=vocabulary_name, expected_type=type_hints["vocabulary_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
        }
        if content_identification_type is not None:
            self._values["content_identification_type"] = content_identification_type
        if content_redaction_type is not None:
            self._values["content_redaction_type"] = content_redaction_type
        if enable_partial_results_stabilization is not None:
            self._values["enable_partial_results_stabilization"] = enable_partial_results_stabilization
        if filter_partial_results is not None:
            self._values["filter_partial_results"] = filter_partial_results
        if language_model_name is not None:
            self._values["language_model_name"] = language_model_name
        if partial_results_stability is not None:
            self._values["partial_results_stability"] = partial_results_stability
        if pii_entity_types is not None:
            self._values["pii_entity_types"] = pii_entity_types
        if show_speaker_label is not None:
            self._values["show_speaker_label"] = show_speaker_label
        if vocabulary_filter_method is not None:
            self._values["vocabulary_filter_method"] = vocabulary_filter_method
        if vocabulary_filter_name is not None:
            self._values["vocabulary_filter_name"] = vocabulary_filter_name
        if vocabulary_name is not None:
            self._values["vocabulary_name"] = vocabulary_name

    @builtins.property
    def language_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.'''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_identification_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.'''
        result = self._values.get("content_identification_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_redaction_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.'''
        result = self._values.get("content_redaction_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_partial_results_stabilization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.'''
        result = self._values.get("enable_partial_results_stabilization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filter_partial_results(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.'''
        result = self._values.get("filter_partial_results")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def language_model_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.'''
        result = self._values.get("language_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partial_results_stability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.'''
        result = self._values.get("partial_results_stability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pii_entity_types(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.'''
        result = self._values.get("pii_entity_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def show_speaker_label(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#show_speaker_label ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#show_speaker_label}.'''
        result = self._values.get("show_speaker_label")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vocabulary_filter_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.'''
        result = self._values.get("vocabulary_filter_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_filter_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.'''
        result = self._values.get("vocabulary_filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.'''
        result = self._values.get("vocabulary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee042a4ec4997ec7f62bc110a76a84cac8af5fab40c1e8e0b70019f71e48b728)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContentIdentificationType")
    def reset_content_identification_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentIdentificationType", []))

    @jsii.member(jsii_name="resetContentRedactionType")
    def reset_content_redaction_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentRedactionType", []))

    @jsii.member(jsii_name="resetEnablePartialResultsStabilization")
    def reset_enable_partial_results_stabilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePartialResultsStabilization", []))

    @jsii.member(jsii_name="resetFilterPartialResults")
    def reset_filter_partial_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterPartialResults", []))

    @jsii.member(jsii_name="resetLanguageModelName")
    def reset_language_model_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageModelName", []))

    @jsii.member(jsii_name="resetPartialResultsStability")
    def reset_partial_results_stability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartialResultsStability", []))

    @jsii.member(jsii_name="resetPiiEntityTypes")
    def reset_pii_entity_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPiiEntityTypes", []))

    @jsii.member(jsii_name="resetShowSpeakerLabel")
    def reset_show_speaker_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShowSpeakerLabel", []))

    @jsii.member(jsii_name="resetVocabularyFilterMethod")
    def reset_vocabulary_filter_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyFilterMethod", []))

    @jsii.member(jsii_name="resetVocabularyFilterName")
    def reset_vocabulary_filter_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyFilterName", []))

    @jsii.member(jsii_name="resetVocabularyName")
    def reset_vocabulary_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyName", []))

    @builtins.property
    @jsii.member(jsii_name="contentIdentificationTypeInput")
    def content_identification_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentIdentificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentRedactionTypeInput")
    def content_redaction_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentRedactionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePartialResultsStabilizationInput")
    def enable_partial_results_stabilization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePartialResultsStabilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterPartialResultsInput")
    def filter_partial_results_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filterPartialResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="languageModelNameInput")
    def language_model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageModelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="partialResultsStabilityInput")
    def partial_results_stability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partialResultsStabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="piiEntityTypesInput")
    def pii_entity_types_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "piiEntityTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="showSpeakerLabelInput")
    def show_speaker_label_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showSpeakerLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterMethodInput")
    def vocabulary_filter_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterNameInput")
    def vocabulary_filter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyNameInput")
    def vocabulary_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="contentIdentificationType")
    def content_identification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentIdentificationType"))

    @content_identification_type.setter
    def content_identification_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4801e3cf1922dab3bdeb53f0a8f2518645050e3c1ab5af48bf914f3e26d27a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentIdentificationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentRedactionType")
    def content_redaction_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentRedactionType"))

    @content_redaction_type.setter
    def content_redaction_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee80f913efa032e8a8ff86532b50452f76da18ce456fa1988d7eb42f2a78a798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentRedactionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePartialResultsStabilization")
    def enable_partial_results_stabilization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePartialResultsStabilization"))

    @enable_partial_results_stabilization.setter
    def enable_partial_results_stabilization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ae63201d61ae5c632eeb4cfeea2c50f72f3c77db0c1f6f44a3241600777f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePartialResultsStabilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterPartialResults")
    def filter_partial_results(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filterPartialResults"))

    @filter_partial_results.setter
    def filter_partial_results(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cfd132cccdc50c0eda0f60a8ff7fc6d38d6e769084e43be557c853f987feec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPartialResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4520d09712484041cf0df500314821a6a8af6c8f2c51be33777eaab47dac8a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageModelName")
    def language_model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageModelName"))

    @language_model_name.setter
    def language_model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4dc67dfe861c38beb5bfdcfe571fd55c1a2480ec1654e0887894d0efbc3a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageModelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partialResultsStability")
    def partial_results_stability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partialResultsStability"))

    @partial_results_stability.setter
    def partial_results_stability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9faa401f6400c49b4eb6687a0b61ef61130c71e7d60db5c9630083b6a45bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partialResultsStability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="piiEntityTypes")
    def pii_entity_types(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "piiEntityTypes"))

    @pii_entity_types.setter
    def pii_entity_types(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0917b34d56f1e6c700d78dd7cef6bc4efd22e9124ef01fb3ea100aa3b63917a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "piiEntityTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="showSpeakerLabel")
    def show_speaker_label(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "showSpeakerLabel"))

    @show_speaker_label.setter
    def show_speaker_label(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4967bf53dd4d1681c790002bb4d95b00dd3348c648603babfbf5df232b4c1ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "showSpeakerLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterMethod")
    def vocabulary_filter_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterMethod"))

    @vocabulary_filter_method.setter
    def vocabulary_filter_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3999b13ccaba32b2348274ba5ec0695bb1522cb445d2249494ab483929a08575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterName")
    def vocabulary_filter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterName"))

    @vocabulary_filter_name.setter
    def vocabulary_filter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6f434604690e71d6aa7d010c4b299b86f0f2768c157954c4817033bc133caa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyName")
    def vocabulary_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyName"))

    @vocabulary_name.setter
    def vocabulary_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a8996a077ef53100149fb259d1a0cb1ec04cb37b310108dbead4689db26fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8862c3437bfaf6132431d7341432456d6cba751cf6606b57e5966ee217173651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87dcc72bb258f2ab9eae4055139745aa431d203226b01763de9d3924e71a6cc0)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.'''
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ff1f0a9422b8b69e9cf90b176f8a32b94d5ecfe11db64148721aa0405383fa2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="insightsTargetInput")
    def insights_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTarget")
    def insights_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsTarget"))

    @insights_target.setter
    def insights_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f91ff362c3dbc3aedaa13265a63bc77eff686fc70649573c6897b697f9d889f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79d0feba135e26d8a3f9d01cda1393bd9a24bf3279eadfe0b1390ee144ebfbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d365e0f6a9e963056a14ae95c0c9a0f5a28ffe23097091633877f17a2f9530a4)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.'''
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6be32a656d4e2fb387e6085beee8ff88470c21a00829d22ff45b41fd0a2f4996)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="insightsTargetInput")
    def insights_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTarget")
    def insights_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsTarget"))

    @insights_target.setter
    def insights_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67799aa5997fa2f2a4fded5811a4e55d0c651b3540284f588556d58f2e7baaa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411fbba9039008c539cbef4083cb80b2cd6a89798d7c77de600bd88ac5e15f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df1ccda45a44586a37cf023c5fb89df38d53a764ce2098605cf55c46dc209622)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7ff6f24a6c3334439cb02dbd308aeeccdad2108c547bddbe906db28182921b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980c6096607f9e58380d0d04d8900ad7220b6ea151d21a08df9efba313b4948d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b005ce02070d8feda7b055461f126cc777537976ecacab86f368a71d9b7329d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2078ad0b73fc8cadeb82b22bfeea8768dcb4a3af3535cee35aee64050d9bfcb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72212f8059de28940e32546dd6f8d46e88552502623fcf7fce2ccffe4bdae4f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__849c646b364351b9e28a5050992716edc30030c528e8aa0efc0e14cb25879268)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAmazonTranscribeCallAnalyticsProcessorConfiguration")
    def put_amazon_transcribe_call_analytics_processor_configuration(
        self,
        *,
        language_code: builtins.str,
        call_analytics_stream_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_identification_type: typing.Optional[builtins.str] = None,
        content_redaction_type: typing.Optional[builtins.str] = None,
        enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        post_call_analytics_settings: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        vocabulary_filter_method: typing.Optional[builtins.str] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.
        :param call_analytics_stream_categories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#call_analytics_stream_categories ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#call_analytics_stream_categories}.
        :param content_identification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.
        :param content_redaction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.
        :param enable_partial_results_stabilization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.
        :param filter_partial_results: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.
        :param language_model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.
        :param partial_results_stability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.
        :param pii_entity_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.
        :param post_call_analytics_settings: post_call_analytics_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#post_call_analytics_settings ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#post_call_analytics_settings}
        :param vocabulary_filter_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.
        :param vocabulary_filter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.
        :param vocabulary_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration(
            language_code=language_code,
            call_analytics_stream_categories=call_analytics_stream_categories,
            content_identification_type=content_identification_type,
            content_redaction_type=content_redaction_type,
            enable_partial_results_stabilization=enable_partial_results_stabilization,
            filter_partial_results=filter_partial_results,
            language_model_name=language_model_name,
            partial_results_stability=partial_results_stability,
            pii_entity_types=pii_entity_types,
            post_call_analytics_settings=post_call_analytics_settings,
            vocabulary_filter_method=vocabulary_filter_method,
            vocabulary_filter_name=vocabulary_filter_name,
            vocabulary_name=vocabulary_name,
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonTranscribeCallAnalyticsProcessorConfiguration", [value]))

    @jsii.member(jsii_name="putAmazonTranscribeProcessorConfiguration")
    def put_amazon_transcribe_processor_configuration(
        self,
        *,
        language_code: builtins.str,
        content_identification_type: typing.Optional[builtins.str] = None,
        content_redaction_type: typing.Optional[builtins.str] = None,
        enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        show_speaker_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vocabulary_filter_method: typing.Optional[builtins.str] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.
        :param content_identification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.
        :param content_redaction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.
        :param enable_partial_results_stabilization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.
        :param filter_partial_results: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.
        :param language_model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.
        :param partial_results_stability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.
        :param pii_entity_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.
        :param show_speaker_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#show_speaker_label ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#show_speaker_label}.
        :param vocabulary_filter_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.
        :param vocabulary_filter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.
        :param vocabulary_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration(
            language_code=language_code,
            content_identification_type=content_identification_type,
            content_redaction_type=content_redaction_type,
            enable_partial_results_stabilization=enable_partial_results_stabilization,
            filter_partial_results=filter_partial_results,
            language_model_name=language_model_name,
            partial_results_stability=partial_results_stability,
            pii_entity_types=pii_entity_types,
            show_speaker_label=show_speaker_label,
            vocabulary_filter_method=vocabulary_filter_method,
            vocabulary_filter_name=vocabulary_filter_name,
            vocabulary_name=vocabulary_name,
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonTranscribeProcessorConfiguration", [value]))

    @jsii.member(jsii_name="putKinesisDataStreamSinkConfiguration")
    def put_kinesis_data_stream_sink_configuration(
        self,
        *,
        insights_target: builtins.str,
    ) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration(
            insights_target=insights_target
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisDataStreamSinkConfiguration", [value]))

    @jsii.member(jsii_name="putLambdaFunctionSinkConfiguration")
    def put_lambda_function_sink_configuration(
        self,
        *,
        insights_target: builtins.str,
    ) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration(
            insights_target=insights_target
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaFunctionSinkConfiguration", [value]))

    @jsii.member(jsii_name="putS3RecordingSinkConfiguration")
    def put_s3_recording_sink_configuration(
        self,
        *,
        destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#destination ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#destination}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putS3RecordingSinkConfiguration", [value]))

    @jsii.member(jsii_name="putSnsTopicSinkConfiguration")
    def put_sns_topic_sink_configuration(
        self,
        *,
        insights_target: builtins.str,
    ) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration(
            insights_target=insights_target
        )

        return typing.cast(None, jsii.invoke(self, "putSnsTopicSinkConfiguration", [value]))

    @jsii.member(jsii_name="putSqsQueueSinkConfiguration")
    def put_sqs_queue_sink_configuration(
        self,
        *,
        insights_target: builtins.str,
    ) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration(
            insights_target=insights_target
        )

        return typing.cast(None, jsii.invoke(self, "putSqsQueueSinkConfiguration", [value]))

    @jsii.member(jsii_name="putVoiceAnalyticsProcessorConfiguration")
    def put_voice_analytics_processor_configuration(
        self,
        *,
        speaker_search_status: builtins.str,
        voice_tone_analysis_status: builtins.str,
    ) -> None:
        '''
        :param speaker_search_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#speaker_search_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#speaker_search_status}.
        :param voice_tone_analysis_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_tone_analysis_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_tone_analysis_status}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration(
            speaker_search_status=speaker_search_status,
            voice_tone_analysis_status=voice_tone_analysis_status,
        )

        return typing.cast(None, jsii.invoke(self, "putVoiceAnalyticsProcessorConfiguration", [value]))

    @jsii.member(jsii_name="resetAmazonTranscribeCallAnalyticsProcessorConfiguration")
    def reset_amazon_transcribe_call_analytics_processor_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonTranscribeCallAnalyticsProcessorConfiguration", []))

    @jsii.member(jsii_name="resetAmazonTranscribeProcessorConfiguration")
    def reset_amazon_transcribe_processor_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonTranscribeProcessorConfiguration", []))

    @jsii.member(jsii_name="resetKinesisDataStreamSinkConfiguration")
    def reset_kinesis_data_stream_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisDataStreamSinkConfiguration", []))

    @jsii.member(jsii_name="resetLambdaFunctionSinkConfiguration")
    def reset_lambda_function_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionSinkConfiguration", []))

    @jsii.member(jsii_name="resetS3RecordingSinkConfiguration")
    def reset_s3_recording_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3RecordingSinkConfiguration", []))

    @jsii.member(jsii_name="resetSnsTopicSinkConfiguration")
    def reset_sns_topic_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnsTopicSinkConfiguration", []))

    @jsii.member(jsii_name="resetSqsQueueSinkConfiguration")
    def reset_sqs_queue_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsQueueSinkConfiguration", []))

    @jsii.member(jsii_name="resetVoiceAnalyticsProcessorConfiguration")
    def reset_voice_analytics_processor_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVoiceAnalyticsProcessorConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="amazonTranscribeCallAnalyticsProcessorConfiguration")
    def amazon_transcribe_call_analytics_processor_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference, jsii.get(self, "amazonTranscribeCallAnalyticsProcessorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="amazonTranscribeProcessorConfiguration")
    def amazon_transcribe_processor_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference, jsii.get(self, "amazonTranscribeProcessorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="kinesisDataStreamSinkConfiguration")
    def kinesis_data_stream_sink_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference, jsii.get(self, "kinesisDataStreamSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionSinkConfiguration")
    def lambda_function_sink_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference, jsii.get(self, "lambdaFunctionSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3RecordingSinkConfiguration")
    def s3_recording_sink_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference", jsii.get(self, "s3RecordingSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="snsTopicSinkConfiguration")
    def sns_topic_sink_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference", jsii.get(self, "snsTopicSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueSinkConfiguration")
    def sqs_queue_sink_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference", jsii.get(self, "sqsQueueSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="voiceAnalyticsProcessorConfiguration")
    def voice_analytics_processor_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference", jsii.get(self, "voiceAnalyticsProcessorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="amazonTranscribeCallAnalyticsProcessorConfigurationInput")
    def amazon_transcribe_call_analytics_processor_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration], jsii.get(self, "amazonTranscribeCallAnalyticsProcessorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="amazonTranscribeProcessorConfigurationInput")
    def amazon_transcribe_processor_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration], jsii.get(self, "amazonTranscribeProcessorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisDataStreamSinkConfigurationInput")
    def kinesis_data_stream_sink_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration], jsii.get(self, "kinesisDataStreamSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionSinkConfigurationInput")
    def lambda_function_sink_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration], jsii.get(self, "lambdaFunctionSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3RecordingSinkConfigurationInput")
    def s3_recording_sink_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration"], jsii.get(self, "s3RecordingSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="snsTopicSinkConfigurationInput")
    def sns_topic_sink_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration"], jsii.get(self, "snsTopicSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueSinkConfigurationInput")
    def sqs_queue_sink_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration"], jsii.get(self, "sqsQueueSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="voiceAnalyticsProcessorConfigurationInput")
    def voice_analytics_processor_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration"], jsii.get(self, "voiceAnalyticsProcessorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c708fa1624896b7fb38d57a4d1d7c230a08a2d32ee9936f52db45dca8ff4398e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5840deb7e4e777dad853312676c10dbcd37668c11af4416197588b753f1fefab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration:
    def __init__(self, *, destination: typing.Optional[builtins.str] = None) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#destination ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7dd49e5a5209375bd631cf4bd0174041b42507a12b0ce1f9ba0bf71f183fb7)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#destination ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#destination}.'''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93f286bfa1c4e3973b4c93162cb7cdbfa4539707651ccba48fdb6f21ad3e1e60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80ce536f2cd0091712d2f05fd25368b3a83be8bb78cce53ebe0670899b0a269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee84f64f725005369cec07c926595f3e34ae32ad256ce7d6d5820ff8d8e6fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e63d463bfb724dbd9d20427581eeccc9ec36f5d465bfa75430a3122fe5621f)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.'''
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce9cc330ebfb9a2717057c73b1c5acf1154bd2e42871a1c37ddb8a9638a7d858)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="insightsTargetInput")
    def insights_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTarget")
    def insights_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsTarget"))

    @insights_target.setter
    def insights_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b812522b5ae6561b29d103290cfbd083383552603965345b8ce8a7c247f88997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc724f2fb276886aa8f802995384de10774ab8dca1c9061fc7580a91730dd128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67525cbbbc8ef9cbeba8e207b5c0b1742ca71875579345ac4a0dc6672b45551d)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.'''
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e7d8bc82119c60830a2c2dd2f7bc3c8c49b96c31942bf50c6f919717bd920ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="insightsTargetInput")
    def insights_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTarget")
    def insights_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsTarget"))

    @insights_target.setter
    def insights_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c045a8a9531827b1da377c0992a85e708d69aacd53a0a27f09243ee5d9f8035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0723a1f351923440a588914848c6792467dd725d02759743f0e139a942fac12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "speaker_search_status": "speakerSearchStatus",
        "voice_tone_analysis_status": "voiceToneAnalysisStatus",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration:
    def __init__(
        self,
        *,
        speaker_search_status: builtins.str,
        voice_tone_analysis_status: builtins.str,
    ) -> None:
        '''
        :param speaker_search_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#speaker_search_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#speaker_search_status}.
        :param voice_tone_analysis_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_tone_analysis_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_tone_analysis_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04993477632c61472176e59161e6167a90c83b09f7dd6a3e065ac011d8fdc8e1)
            check_type(argname="argument speaker_search_status", value=speaker_search_status, expected_type=type_hints["speaker_search_status"])
            check_type(argname="argument voice_tone_analysis_status", value=voice_tone_analysis_status, expected_type=type_hints["voice_tone_analysis_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "speaker_search_status": speaker_search_status,
            "voice_tone_analysis_status": voice_tone_analysis_status,
        }

    @builtins.property
    def speaker_search_status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#speaker_search_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#speaker_search_status}.'''
        result = self._values.get("speaker_search_status")
        assert result is not None, "Required property 'speaker_search_status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def voice_tone_analysis_status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_tone_analysis_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_tone_analysis_status}.'''
        result = self._values.get("voice_tone_analysis_status")
        assert result is not None, "Required property 'voice_tone_analysis_status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03cc5d0ce5e2972d2826f70899ead2cc60ff4de484d85a46a664c535aa7aafed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="speakerSearchStatusInput")
    def speaker_search_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "speakerSearchStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="voiceToneAnalysisStatusInput")
    def voice_tone_analysis_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "voiceToneAnalysisStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="speakerSearchStatus")
    def speaker_search_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "speakerSearchStatus"))

    @speaker_search_status.setter
    def speaker_search_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1528177a72a175512fe2a4aaa3b7404b08aa2de13a194726b9d66a505f5c19bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speakerSearchStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="voiceToneAnalysisStatus")
    def voice_tone_analysis_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "voiceToneAnalysisStatus"))

    @voice_tone_analysis_status.setter
    def voice_tone_analysis_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4408cb1b47a41c5a59af4a2833b4940343fa8cc96cb9dbd149ea3da17010435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "voiceToneAnalysisStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc78806f7d4dab6323e74559ded8de492f5182589e6d5ba1ef92f759b43e4688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules", "disabled": "disabled"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration:
    def __init__(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules", typing.Dict[builtins.str, typing.Any]]]],
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rules ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rules}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#disabled ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#disabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009bd4ffbeb6de67ce09a97f27a9a797d663ed377f2f8538a805cbe020a73c38)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rules": rules,
        }
        if disabled is not None:
            self._values["disabled"] = disabled

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rules ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules"]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#disabled ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0576274bf92a4d77ffe4e1ac2385252de4f9b91103fb5d39fe5cf16ff051a23c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0a5f8ed247e6e007be743a530695f50d4da2444215beb1a5fa1911bb4f7258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79be2aaaa7e81d6a8f50efe7bd1c9eb3d5886a369bc02968121592be4ce18df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234ff160c3460fd7876b4890ab548ee5b96c8adeda0b2d65f1634da9208ed6f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "issue_detection_configuration": "issueDetectionConfiguration",
        "keyword_match_configuration": "keywordMatchConfiguration",
        "sentiment_configuration": "sentimentConfiguration",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules:
    def __init__(
        self,
        *,
        type: builtins.str,
        issue_detection_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        keyword_match_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sentiment_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#type}.
        :param issue_detection_configuration: issue_detection_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#issue_detection_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#issue_detection_configuration}
        :param keyword_match_configuration: keyword_match_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keyword_match_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keyword_match_configuration}
        :param sentiment_configuration: sentiment_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_configuration}
        '''
        if isinstance(issue_detection_configuration, dict):
            issue_detection_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration(**issue_detection_configuration)
        if isinstance(keyword_match_configuration, dict):
            keyword_match_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration(**keyword_match_configuration)
        if isinstance(sentiment_configuration, dict):
            sentiment_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration(**sentiment_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e96325882c3c653f78224c0ddf75c9d161196bf7d8697c438a0d0c0d0987d62)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument issue_detection_configuration", value=issue_detection_configuration, expected_type=type_hints["issue_detection_configuration"])
            check_type(argname="argument keyword_match_configuration", value=keyword_match_configuration, expected_type=type_hints["keyword_match_configuration"])
            check_type(argname="argument sentiment_configuration", value=sentiment_configuration, expected_type=type_hints["sentiment_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if issue_detection_configuration is not None:
            self._values["issue_detection_configuration"] = issue_detection_configuration
        if keyword_match_configuration is not None:
            self._values["keyword_match_configuration"] = keyword_match_configuration
        if sentiment_configuration is not None:
            self._values["sentiment_configuration"] = sentiment_configuration

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issue_detection_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration"]:
        '''issue_detection_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#issue_detection_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#issue_detection_configuration}
        '''
        result = self._values.get("issue_detection_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration"], result)

    @builtins.property
    def keyword_match_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration"]:
        '''keyword_match_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keyword_match_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keyword_match_configuration}
        '''
        result = self._values.get("keyword_match_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration"], result)

    @builtins.property
    def sentiment_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration"]:
        '''sentiment_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_configuration}
        '''
        result = self._values.get("sentiment_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"rule_name": "ruleName"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration:
    def __init__(self, *, rule_name: builtins.str) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6103c44869eff057d7f42be471af0873a9d6cc9d806fcacdda8d6bc65ddff113)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
        }

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e919733acaa42b6581d674fa0850bc8420dcf5d56d46f40a5ed64181a37a0161)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3e39caa97a9a806cf10a586f67e327ff224ee501697a55c66eb2fe9cfe05fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9688a4badf1fb790e51f37d5f57dc4b901ec54dbec019e296e5ada8204a52c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration",
    jsii_struct_bases=[],
    name_mapping={"keywords": "keywords", "rule_name": "ruleName", "negate": "negate"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration:
    def __init__(
        self,
        *,
        keywords: typing.Sequence[builtins.str],
        rule_name: builtins.str,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param keywords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keywords ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keywords}.
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        :param negate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#negate ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#negate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b49e0868a093f1de4e7978178aa9bccb16babff41dde8b9cdb2a9a2eb3afaf)
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keywords": keywords,
            "rule_name": rule_name,
        }
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def keywords(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keywords ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keywords}.'''
        result = self._values.get("keywords")
        assert result is not None, "Required property 'keywords' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#negate ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#negate}.'''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b8002bfc696bb5842892e9441ac13dca1c7012302943df443fe925bb4a156dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @builtins.property
    @jsii.member(jsii_name="keywordsInput")
    def keywords_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keywordsInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keywords")
    def keywords(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keywords"))

    @keywords.setter
    def keywords(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8cd37ee21f5640702fa0cc723473bab88aef95f5ef6494d3ffbc541a83d9d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keywords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bf55c816a60f10ce35f85ade8d5522780e655c8afdc528f10d691089634d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93dccebc43af312f9ac39907cbd622ffe13ee5c3832f1b769ee96d1f4f837f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b3799b8c44de9bcd689caed221c28537f8a7abfe3e48b41f847bbece7770f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0efc3cf9d4b3618744c4f45bf57d7293c997e75c745550bf0f0182c8c5e98843)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15bec854fabceee03604d80662eeaccce7deb43470a851a53748912c5f05d2bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea7879277f17cb8112e633f5ba2a3305851b50525cb04e1c370f78f926f7e13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf01418984a899942caa521eaa7a04dff7c282bd0a7f3eb2181f066b2c7d06ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b4773ee9c58ae0eee13ccf7f28e6b94c89585932c04cf617f9a044ad56bad23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc38f0f5f55a07fbd768d91f5628a869c0167d7692bdf1ad673a3589459d0399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b8d977f444dbd325b806bbf20ab5a9be2ba86c344252bad06f65d98e7ae5cb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIssueDetectionConfiguration")
    def put_issue_detection_configuration(self, *, rule_name: builtins.str) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration(
            rule_name=rule_name
        )

        return typing.cast(None, jsii.invoke(self, "putIssueDetectionConfiguration", [value]))

    @jsii.member(jsii_name="putKeywordMatchConfiguration")
    def put_keyword_match_configuration(
        self,
        *,
        keywords: typing.Sequence[builtins.str],
        rule_name: builtins.str,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param keywords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keywords ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keywords}.
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        :param negate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#negate ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#negate}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration(
            keywords=keywords, rule_name=rule_name, negate=negate
        )

        return typing.cast(None, jsii.invoke(self, "putKeywordMatchConfiguration", [value]))

    @jsii.member(jsii_name="putSentimentConfiguration")
    def put_sentiment_configuration(
        self,
        *,
        rule_name: builtins.str,
        sentiment_type: builtins.str,
        time_period: jsii.Number,
    ) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        :param sentiment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_type}.
        :param time_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#time_period ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#time_period}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration(
            rule_name=rule_name, sentiment_type=sentiment_type, time_period=time_period
        )

        return typing.cast(None, jsii.invoke(self, "putSentimentConfiguration", [value]))

    @jsii.member(jsii_name="resetIssueDetectionConfiguration")
    def reset_issue_detection_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssueDetectionConfiguration", []))

    @jsii.member(jsii_name="resetKeywordMatchConfiguration")
    def reset_keyword_match_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeywordMatchConfiguration", []))

    @jsii.member(jsii_name="resetSentimentConfiguration")
    def reset_sentiment_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSentimentConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="issueDetectionConfiguration")
    def issue_detection_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference, jsii.get(self, "issueDetectionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="keywordMatchConfiguration")
    def keyword_match_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference, jsii.get(self, "keywordMatchConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="sentimentConfiguration")
    def sentiment_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference", jsii.get(self, "sentimentConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="issueDetectionConfigurationInput")
    def issue_detection_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration], jsii.get(self, "issueDetectionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="keywordMatchConfigurationInput")
    def keyword_match_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration], jsii.get(self, "keywordMatchConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="sentimentConfigurationInput")
    def sentiment_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration"], jsii.get(self, "sentimentConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd73d3e54261862aae8612fcdaff3806a7dc10bd69bfd19906dbd3053882c2a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10026442ee4fe6ceb5e371f5aa7b7abaa888cb9c2ce0390926d155563ce85d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "rule_name": "ruleName",
        "sentiment_type": "sentimentType",
        "time_period": "timePeriod",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration:
    def __init__(
        self,
        *,
        rule_name: builtins.str,
        sentiment_type: builtins.str,
        time_period: jsii.Number,
    ) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        :param sentiment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_type}.
        :param time_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#time_period ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#time_period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33a3d06fec3a248ce6a85d873a099e582b1a0437e28f72a5ae35b8e78f9ca83)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument sentiment_type", value=sentiment_type, expected_type=type_hints["sentiment_type"])
            check_type(argname="argument time_period", value=time_period, expected_type=type_hints["time_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
            "sentiment_type": sentiment_type,
            "time_period": time_period,
        }

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sentiment_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_type}.'''
        result = self._values.get("sentiment_type")
        assert result is not None, "Required property 'sentiment_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#time_period ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#time_period}.'''
        result = self._values.get("time_period")
        assert result is not None, "Required property 'time_period' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__371183424475efe9c2c9d0561c5dc7f0b31e47f532d6e25dad6fe62d797c0cdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sentimentTypeInput")
    def sentiment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sentimentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timePeriodInput")
    def time_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f812bf2b1055b51fb7e12ac96db3b5df5f2cd048aee2cd8289047cc7737cde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sentimentType")
    def sentiment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sentimentType"))

    @sentiment_type.setter
    def sentiment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94c3d8dae62edbce23b86a5ccb3ce578bb003b6888784bbbe5208417fd5dfba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sentimentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timePeriod")
    def time_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timePeriod"))

    @time_period.setter
    def time_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8739ba9c60f8e98b6ab3ecb8a2499c48482271d2705edce3dafa63bde0ed4fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timePeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a9f0357298ebfea4bcbcf1a4e220c2bf4f70f899907cc914dbd124537c13c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#create ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#delete ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#update ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766f44ba0dbf95552a9191dee7cef7fe819ca65e72e44cf847eff40ab5b7a7a0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#create ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#delete ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#update ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__433ca85c6071ecf4a5a6483ee852ba382a069e23d0689322525fecbde5a0bacf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73105ae722f9f91ef99fc9902f633740266622900c4b538f47e0b0976a78b5dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00beacc1181652db9a4c872185500050a3d0243408832794dbb448f823e9de10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30de8d701f14e4a2540601d88c93116ead756f19274222901f494bf19a1fc6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84fc46bb99eadaae19fdf0fdfadf3f3a7a80d8245978a6df8f49b34c294c8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ChimesdkmediapipelinesMediaInsightsPipelineConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__caa8b7c1b288db26f5f503b3326290886ed2ebc0657038bd3215bbd8048a4300(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    elements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    resource_access_role_arn: builtins.str,
    real_time_alert_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3c79ad8fd91299c571793385bd9597e992db17a8cae9173dda4cad3872938fc0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88251684cf501836da2199a21d345ca479a66d994bf0244805cda64b582dea3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c907cffed96dced25641d3490249f15f431b55fcd42125396be7af55a63753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad4497bf9c4b14405b7c8adf0f7c83dc4db834c6e4c69de20321338b44adfe4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c345da0278a9dcd5ed788cb047e9ac27c7b585d2a215f01d5099c549a49307(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b3b62f734eeada67de411869349f367e53a947c075ade6111fcc260f657ec9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a43c2a778ff47a0f92d5bc26d983d258e7916e7cb812483fe16d21e260145d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    resource_access_role_arn: builtins.str,
    real_time_alert_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1bdfe34057141e6e19d04c8c2be4978fb95a150480db73b8cd7b9228820b1c(
    *,
    type: builtins.str,
    amazon_transcribe_call_analytics_processor_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    amazon_transcribe_processor_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_data_stream_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_function_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_recording_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sns_topic_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_queue_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    voice_analytics_processor_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8596c248f2eb5452c156c07215618acdac32c475d27f91c7c6875e27ddfa69e7(
    *,
    language_code: builtins.str,
    call_analytics_stream_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_identification_type: typing.Optional[builtins.str] = None,
    content_redaction_type: typing.Optional[builtins.str] = None,
    enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language_model_name: typing.Optional[builtins.str] = None,
    partial_results_stability: typing.Optional[builtins.str] = None,
    pii_entity_types: typing.Optional[builtins.str] = None,
    post_call_analytics_settings: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    vocabulary_filter_method: typing.Optional[builtins.str] = None,
    vocabulary_filter_name: typing.Optional[builtins.str] = None,
    vocabulary_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f75941048901685858c0a2d6f04932044fa72485705afc8278c09627cfc3aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a529ddb0b3cc0ed142bea462b1080e2d3675cb3790c0430a002a11941a9dd124(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb5bffabd7e83f46ce4534501ed85c31fed02270f5d353ccbc66d07d21e5035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24461617814b9ac127b61d6f2bda43525a55f54d81c16711964c1bc356971dc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075b43fca4487ffbd8a601e4f560a70e79e5b0d2468ec14395d70189ad1144c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4078e374c823b68cc038121447d96cc41ca6f350074943c6cbf5cb295f2055e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0f05778f9aace52f20ce376e86eefea605f8c546becad0290ded3dcc0028f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35c1f1377977509bf023ee7a2066d111e0cdc9843da23debd77f91d0854e7c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd9092d05edbf76373467c80f5130e4c2d1514101aef2dc89d28577918decae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7da26b477067afc3fce9b665c40f6cbecc7ff5959349d1c6c430a6a47e86a45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7bf2cac204457d789fab8a62e34cb528f4a39dff20692a57b286f73ad6f7a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e302f0ad41801ec5959d8a70a57b6c2235e93ead2b99e40b4d4ced1945e50d5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1601973212d01aa06057c8e90636a3e5a04c0e5aff15494c7aebefdd74ad46b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a20fb3c788f81316cc1d0a06c0cd060428bfa01255335102ee4d5bd1d363e1(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a46200f09fb43794ef1d9fd2161ae09dfc1d0e6b3bab0016590b61e38d6b39(
    *,
    data_access_role_arn: builtins.str,
    output_location: builtins.str,
    content_redaction_output: typing.Optional[builtins.str] = None,
    output_encryption_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce17813a92d1897dfea56d6554f5bda72473b727ebc4056bf65f61882e87f3bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09690ca9003c31f63cb8c194e855aa9b0c2274e6864718e3262d01921f6730d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb39826421d92c1bc4ad102d875976ee6d6cd10cf8ba3b49466c8757cd16e999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb2cc97b19f3c9660b1088c18933ad61a8f142bc7160f70e48db7c29d99edff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc1bb024355e5d475f8c97837efefe72775fae9833e6c6eb4dca9917c28ba96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fffd27b2a0197783e58ae2f78af67a1897a8799660f3c061ec1cc72efc30fdf(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09fbf37f49c3812cc245192a4bde01575a26cec538ce168dc00b7b1d1544ea4(
    *,
    language_code: builtins.str,
    content_identification_type: typing.Optional[builtins.str] = None,
    content_redaction_type: typing.Optional[builtins.str] = None,
    enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language_model_name: typing.Optional[builtins.str] = None,
    partial_results_stability: typing.Optional[builtins.str] = None,
    pii_entity_types: typing.Optional[builtins.str] = None,
    show_speaker_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vocabulary_filter_method: typing.Optional[builtins.str] = None,
    vocabulary_filter_name: typing.Optional[builtins.str] = None,
    vocabulary_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee042a4ec4997ec7f62bc110a76a84cac8af5fab40c1e8e0b70019f71e48b728(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4801e3cf1922dab3bdeb53f0a8f2518645050e3c1ab5af48bf914f3e26d27a49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee80f913efa032e8a8ff86532b50452f76da18ce456fa1988d7eb42f2a78a798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ae63201d61ae5c632eeb4cfeea2c50f72f3c77db0c1f6f44a3241600777f5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cfd132cccdc50c0eda0f60a8ff7fc6d38d6e769084e43be557c853f987feec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4520d09712484041cf0df500314821a6a8af6c8f2c51be33777eaab47dac8a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4dc67dfe861c38beb5bfdcfe571fd55c1a2480ec1654e0887894d0efbc3a3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9faa401f6400c49b4eb6687a0b61ef61130c71e7d60db5c9630083b6a45bc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0917b34d56f1e6c700d78dd7cef6bc4efd22e9124ef01fb3ea100aa3b63917a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4967bf53dd4d1681c790002bb4d95b00dd3348c648603babfbf5df232b4c1ef2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3999b13ccaba32b2348274ba5ec0695bb1522cb445d2249494ab483929a08575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6f434604690e71d6aa7d010c4b299b86f0f2768c157954c4817033bc133caa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a8996a077ef53100149fb259d1a0cb1ec04cb37b310108dbead4689db26fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8862c3437bfaf6132431d7341432456d6cba751cf6606b57e5966ee217173651(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87dcc72bb258f2ab9eae4055139745aa431d203226b01763de9d3924e71a6cc0(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff1f0a9422b8b69e9cf90b176f8a32b94d5ecfe11db64148721aa0405383fa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f91ff362c3dbc3aedaa13265a63bc77eff686fc70649573c6897b697f9d889f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79d0feba135e26d8a3f9d01cda1393bd9a24bf3279eadfe0b1390ee144ebfbf(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d365e0f6a9e963056a14ae95c0c9a0f5a28ffe23097091633877f17a2f9530a4(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be32a656d4e2fb387e6085beee8ff88470c21a00829d22ff45b41fd0a2f4996(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67799aa5997fa2f2a4fded5811a4e55d0c651b3540284f588556d58f2e7baaa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411fbba9039008c539cbef4083cb80b2cd6a89798d7c77de600bd88ac5e15f82(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1ccda45a44586a37cf023c5fb89df38d53a764ce2098605cf55c46dc209622(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7ff6f24a6c3334439cb02dbd308aeeccdad2108c547bddbe906db28182921b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980c6096607f9e58380d0d04d8900ad7220b6ea151d21a08df9efba313b4948d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b005ce02070d8feda7b055461f126cc777537976ecacab86f368a71d9b7329d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2078ad0b73fc8cadeb82b22bfeea8768dcb4a3af3535cee35aee64050d9bfcb8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72212f8059de28940e32546dd6f8d46e88552502623fcf7fce2ccffe4bdae4f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849c646b364351b9e28a5050992716edc30030c528e8aa0efc0e14cb25879268(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c708fa1624896b7fb38d57a4d1d7c230a08a2d32ee9936f52db45dca8ff4398e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5840deb7e4e777dad853312676c10dbcd37668c11af4416197588b753f1fefab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7dd49e5a5209375bd631cf4bd0174041b42507a12b0ce1f9ba0bf71f183fb7(
    *,
    destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f286bfa1c4e3973b4c93162cb7cdbfa4539707651ccba48fdb6f21ad3e1e60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80ce536f2cd0091712d2f05fd25368b3a83be8bb78cce53ebe0670899b0a269(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee84f64f725005369cec07c926595f3e34ae32ad256ce7d6d5820ff8d8e6fb8(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e63d463bfb724dbd9d20427581eeccc9ec36f5d465bfa75430a3122fe5621f(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9cc330ebfb9a2717057c73b1c5acf1154bd2e42871a1c37ddb8a9638a7d858(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b812522b5ae6561b29d103290cfbd083383552603965345b8ce8a7c247f88997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc724f2fb276886aa8f802995384de10774ab8dca1c9061fc7580a91730dd128(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67525cbbbc8ef9cbeba8e207b5c0b1742ca71875579345ac4a0dc6672b45551d(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7d8bc82119c60830a2c2dd2f7bc3c8c49b96c31942bf50c6f919717bd920ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c045a8a9531827b1da377c0992a85e708d69aacd53a0a27f09243ee5d9f8035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0723a1f351923440a588914848c6792467dd725d02759743f0e139a942fac12(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04993477632c61472176e59161e6167a90c83b09f7dd6a3e065ac011d8fdc8e1(
    *,
    speaker_search_status: builtins.str,
    voice_tone_analysis_status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cc5d0ce5e2972d2826f70899ead2cc60ff4de484d85a46a664c535aa7aafed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1528177a72a175512fe2a4aaa3b7404b08aa2de13a194726b9d66a505f5c19bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4408cb1b47a41c5a59af4a2833b4940343fa8cc96cb9dbd149ea3da17010435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc78806f7d4dab6323e74559ded8de492f5182589e6d5ba1ef92f759b43e4688(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009bd4ffbeb6de67ce09a97f27a9a797d663ed377f2f8538a805cbe020a73c38(
    *,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules, typing.Dict[builtins.str, typing.Any]]]],
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0576274bf92a4d77ffe4e1ac2385252de4f9b91103fb5d39fe5cf16ff051a23c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0a5f8ed247e6e007be743a530695f50d4da2444215beb1a5fa1911bb4f7258(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79be2aaaa7e81d6a8f50efe7bd1c9eb3d5886a369bc02968121592be4ce18df5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234ff160c3460fd7876b4890ab548ee5b96c8adeda0b2d65f1634da9208ed6f7(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e96325882c3c653f78224c0ddf75c9d161196bf7d8697c438a0d0c0d0987d62(
    *,
    type: builtins.str,
    issue_detection_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    keyword_match_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sentiment_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6103c44869eff057d7f42be471af0873a9d6cc9d806fcacdda8d6bc65ddff113(
    *,
    rule_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e919733acaa42b6581d674fa0850bc8420dcf5d56d46f40a5ed64181a37a0161(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3e39caa97a9a806cf10a586f67e327ff224ee501697a55c66eb2fe9cfe05fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9688a4badf1fb790e51f37d5f57dc4b901ec54dbec019e296e5ada8204a52c(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b49e0868a093f1de4e7978178aa9bccb16babff41dde8b9cdb2a9a2eb3afaf(
    *,
    keywords: typing.Sequence[builtins.str],
    rule_name: builtins.str,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8002bfc696bb5842892e9441ac13dca1c7012302943df443fe925bb4a156dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cd37ee21f5640702fa0cc723473bab88aef95f5ef6494d3ffbc541a83d9d4e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bf55c816a60f10ce35f85ade8d5522780e655c8afdc528f10d691089634d06(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dccebc43af312f9ac39907cbd622ffe13ee5c3832f1b769ee96d1f4f837f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b3799b8c44de9bcd689caed221c28537f8a7abfe3e48b41f847bbece7770f1(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efc3cf9d4b3618744c4f45bf57d7293c997e75c745550bf0f0182c8c5e98843(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bec854fabceee03604d80662eeaccce7deb43470a851a53748912c5f05d2bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea7879277f17cb8112e633f5ba2a3305851b50525cb04e1c370f78f926f7e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf01418984a899942caa521eaa7a04dff7c282bd0a7f3eb2181f066b2c7d06ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4773ee9c58ae0eee13ccf7f28e6b94c89585932c04cf617f9a044ad56bad23(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc38f0f5f55a07fbd768d91f5628a869c0167d7692bdf1ad673a3589459d0399(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8d977f444dbd325b806bbf20ab5a9be2ba86c344252bad06f65d98e7ae5cb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd73d3e54261862aae8612fcdaff3806a7dc10bd69bfd19906dbd3053882c2a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10026442ee4fe6ceb5e371f5aa7b7abaa888cb9c2ce0390926d155563ce85d46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33a3d06fec3a248ce6a85d873a099e582b1a0437e28f72a5ae35b8e78f9ca83(
    *,
    rule_name: builtins.str,
    sentiment_type: builtins.str,
    time_period: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371183424475efe9c2c9d0561c5dc7f0b31e47f532d6e25dad6fe62d797c0cdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f812bf2b1055b51fb7e12ac96db3b5df5f2cd048aee2cd8289047cc7737cde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94c3d8dae62edbce23b86a5ccb3ce578bb003b6888784bbbe5208417fd5dfba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8739ba9c60f8e98b6ab3ecb8a2499c48482271d2705edce3dafa63bde0ed4fbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a9f0357298ebfea4bcbcf1a4e220c2bf4f70f899907cc914dbd124537c13c8(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766f44ba0dbf95552a9191dee7cef7fe819ca65e72e44cf847eff40ab5b7a7a0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433ca85c6071ecf4a5a6483ee852ba382a069e23d0689322525fecbde5a0bacf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73105ae722f9f91ef99fc9902f633740266622900c4b538f47e0b0976a78b5dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00beacc1181652db9a4c872185500050a3d0243408832794dbb448f823e9de10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30de8d701f14e4a2540601d88c93116ead756f19274222901f494bf19a1fc6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84fc46bb99eadaae19fdf0fdfadf3f3a7a80d8245978a6df8f49b34c294c8f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
