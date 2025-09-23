r'''
# `aws_dlm_lifecycle_policy`

Refer to the Terraform Registry for docs: [`aws_dlm_lifecycle_policy`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy).
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


class DlmLifecyclePolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy aws_dlm_lifecycle_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: builtins.str,
        execution_role_arn: builtins.str,
        policy_details: typing.Union["DlmLifecyclePolicyPolicyDetails", typing.Dict[builtins.str, typing.Any]],
        default_policy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy aws_dlm_lifecycle_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#description DlmLifecyclePolicy#description}.
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_role_arn DlmLifecyclePolicy#execution_role_arn}.
        :param policy_details: policy_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_details DlmLifecyclePolicy#policy_details}
        :param default_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#default_policy DlmLifecyclePolicy#default_policy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#id DlmLifecyclePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#region DlmLifecyclePolicy#region}
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#state DlmLifecyclePolicy#state}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#tags DlmLifecyclePolicy#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#tags_all DlmLifecyclePolicy#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbe156837bcecb09c52e230c31e44e5177ca8a14e81e40acf163c4c73e6a268)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DlmLifecyclePolicyConfig(
            description=description,
            execution_role_arn=execution_role_arn,
            policy_details=policy_details,
            default_policy=default_policy,
            id=id,
            region=region,
            state=state,
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
        '''Generates CDKTF code for importing a DlmLifecyclePolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DlmLifecyclePolicy to import.
        :param import_from_id: The id of the existing DlmLifecyclePolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DlmLifecyclePolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ddbfcdc4c93323295b5cbc301f0a29527d1c58cece393f95c8c1d3f661fbfe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPolicyDetails")
    def put_policy_details(
        self,
        *,
        action: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsAction", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_interval: typing.Optional[jsii.Number] = None,
        event_source: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsExclusions", typing.Dict[builtins.str, typing.Any]]] = None,
        extend_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parameters: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_language: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
        resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        retain_interval: typing.Optional[jsii.Number] = None,
        schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#action DlmLifecyclePolicy#action}
        :param copy_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.
        :param create_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#create_interval DlmLifecyclePolicy#create_interval}.
        :param event_source: event_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#event_source DlmLifecyclePolicy#event_source}
        :param exclusions: exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclusions DlmLifecyclePolicy#exclusions}
        :param extend_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#extend_deletion DlmLifecyclePolicy#extend_deletion}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        :param policy_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_language DlmLifecyclePolicy#policy_language}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_type DlmLifecyclePolicy#policy_type}.
        :param resource_locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_locations DlmLifecyclePolicy#resource_locations}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_type DlmLifecyclePolicy#resource_type}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_types DlmLifecyclePolicy#resource_types}.
        :param retain_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_interval DlmLifecyclePolicy#retain_interval}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#schedule DlmLifecyclePolicy#schedule}
        :param target_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target_tags DlmLifecyclePolicy#target_tags}.
        '''
        value = DlmLifecyclePolicyPolicyDetails(
            action=action,
            copy_tags=copy_tags,
            create_interval=create_interval,
            event_source=event_source,
            exclusions=exclusions,
            extend_deletion=extend_deletion,
            parameters=parameters,
            policy_language=policy_language,
            policy_type=policy_type,
            resource_locations=resource_locations,
            resource_type=resource_type,
            resource_types=resource_types,
            retain_interval=retain_interval,
            schedule=schedule,
            target_tags=target_tags,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyDetails", [value]))

    @jsii.member(jsii_name="resetDefaultPolicy")
    def reset_default_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="policyDetails")
    def policy_details(self) -> "DlmLifecyclePolicyPolicyDetailsOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsOutputReference", jsii.get(self, "policyDetails"))

    @builtins.property
    @jsii.member(jsii_name="defaultPolicyInput")
    def default_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDetailsInput")
    def policy_details_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetails"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetails"], jsii.get(self, "policyDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

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
    @jsii.member(jsii_name="defaultPolicy")
    def default_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPolicy"))

    @default_policy.setter
    def default_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de24a90124610e3e0c2a0aaa3aa601f62c715198ebac8f45498c39dc2d3f112a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3849a4beaf2de11f89d2b1a74f1ff5ff8895ef4fba8aa202a90f25385e3bd8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d99eca60ef7e61c225e5c8d28bd54588e7ec40abeb2c684c227edb383a7ac6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e4f88d1c7a361267c8834cf0fe69d359f0fb66f0b8fb32840e6043a2bbfcb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ef15727cd06fad1072c0e392d17ae9840f2b67509c2c5c7832a7e5f0c0bf8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244ba13b61b431b4cba1c05acbfae9b37925bc4c7cd2e44b5b736e6779479a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6785abdb647e2b69033b1bebe89234a2b0f1f2f31315bb5dc705edc848cbc2e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b0c2eff3520097ae97b9488a5fdfdc93f372cd1977316841ba9cfc6a1c8b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "execution_role_arn": "executionRoleArn",
        "policy_details": "policyDetails",
        "default_policy": "defaultPolicy",
        "id": "id",
        "region": "region",
        "state": "state",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class DlmLifecyclePolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        execution_role_arn: builtins.str,
        policy_details: typing.Union["DlmLifecyclePolicyPolicyDetails", typing.Dict[builtins.str, typing.Any]],
        default_policy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
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
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#description DlmLifecyclePolicy#description}.
        :param execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_role_arn DlmLifecyclePolicy#execution_role_arn}.
        :param policy_details: policy_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_details DlmLifecyclePolicy#policy_details}
        :param default_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#default_policy DlmLifecyclePolicy#default_policy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#id DlmLifecyclePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#region DlmLifecyclePolicy#region}
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#state DlmLifecyclePolicy#state}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#tags DlmLifecyclePolicy#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#tags_all DlmLifecyclePolicy#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(policy_details, dict):
            policy_details = DlmLifecyclePolicyPolicyDetails(**policy_details)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dda0c7b3666c9c69624b0c7130cc0fa2ababc41631b0cbf85be40de766ea8a6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument policy_details", value=policy_details, expected_type=type_hints["policy_details"])
            check_type(argname="argument default_policy", value=default_policy, expected_type=type_hints["default_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "execution_role_arn": execution_role_arn,
            "policy_details": policy_details,
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
        if default_policy is not None:
            self._values["default_policy"] = default_policy
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if state is not None:
            self._values["state"] = state
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
    def description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#description DlmLifecyclePolicy#description}.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_role_arn DlmLifecyclePolicy#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_details(self) -> "DlmLifecyclePolicyPolicyDetails":
        '''policy_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_details DlmLifecyclePolicy#policy_details}
        '''
        result = self._values.get("policy_details")
        assert result is not None, "Required property 'policy_details' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetails", result)

    @builtins.property
    def default_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#default_policy DlmLifecyclePolicy#default_policy}.'''
        result = self._values.get("default_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#id DlmLifecyclePolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#region DlmLifecyclePolicy#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#state DlmLifecyclePolicy#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#tags DlmLifecyclePolicy#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#tags_all DlmLifecyclePolicy#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetails",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "copy_tags": "copyTags",
        "create_interval": "createInterval",
        "event_source": "eventSource",
        "exclusions": "exclusions",
        "extend_deletion": "extendDeletion",
        "parameters": "parameters",
        "policy_language": "policyLanguage",
        "policy_type": "policyType",
        "resource_locations": "resourceLocations",
        "resource_type": "resourceType",
        "resource_types": "resourceTypes",
        "retain_interval": "retainInterval",
        "schedule": "schedule",
        "target_tags": "targetTags",
    },
)
class DlmLifecyclePolicyPolicyDetails:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsAction", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_interval: typing.Optional[jsii.Number] = None,
        event_source: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsEventSource", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusions: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsExclusions", typing.Dict[builtins.str, typing.Any]]] = None,
        extend_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parameters: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_language: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
        resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        retain_interval: typing.Optional[jsii.Number] = None,
        schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#action DlmLifecyclePolicy#action}
        :param copy_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.
        :param create_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#create_interval DlmLifecyclePolicy#create_interval}.
        :param event_source: event_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#event_source DlmLifecyclePolicy#event_source}
        :param exclusions: exclusions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclusions DlmLifecyclePolicy#exclusions}
        :param extend_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#extend_deletion DlmLifecyclePolicy#extend_deletion}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        :param policy_language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_language DlmLifecyclePolicy#policy_language}.
        :param policy_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_type DlmLifecyclePolicy#policy_type}.
        :param resource_locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_locations DlmLifecyclePolicy#resource_locations}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_type DlmLifecyclePolicy#resource_type}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_types DlmLifecyclePolicy#resource_types}.
        :param retain_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_interval DlmLifecyclePolicy#retain_interval}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#schedule DlmLifecyclePolicy#schedule}
        :param target_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target_tags DlmLifecyclePolicy#target_tags}.
        '''
        if isinstance(action, dict):
            action = DlmLifecyclePolicyPolicyDetailsAction(**action)
        if isinstance(event_source, dict):
            event_source = DlmLifecyclePolicyPolicyDetailsEventSource(**event_source)
        if isinstance(exclusions, dict):
            exclusions = DlmLifecyclePolicyPolicyDetailsExclusions(**exclusions)
        if isinstance(parameters, dict):
            parameters = DlmLifecyclePolicyPolicyDetailsParameters(**parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98f504d834e3e13eac910a982cc05b656c2435ccbc1970b89affef5bce57932)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
            check_type(argname="argument create_interval", value=create_interval, expected_type=type_hints["create_interval"])
            check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument extend_deletion", value=extend_deletion, expected_type=type_hints["extend_deletion"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument policy_language", value=policy_language, expected_type=type_hints["policy_language"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument resource_locations", value=resource_locations, expected_type=type_hints["resource_locations"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument retain_interval", value=retain_interval, expected_type=type_hints["retain_interval"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument target_tags", value=target_tags, expected_type=type_hints["target_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if copy_tags is not None:
            self._values["copy_tags"] = copy_tags
        if create_interval is not None:
            self._values["create_interval"] = create_interval
        if event_source is not None:
            self._values["event_source"] = event_source
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if extend_deletion is not None:
            self._values["extend_deletion"] = extend_deletion
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy_language is not None:
            self._values["policy_language"] = policy_language
        if policy_type is not None:
            self._values["policy_type"] = policy_type
        if resource_locations is not None:
            self._values["resource_locations"] = resource_locations
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if resource_types is not None:
            self._values["resource_types"] = resource_types
        if retain_interval is not None:
            self._values["retain_interval"] = retain_interval
        if schedule is not None:
            self._values["schedule"] = schedule
        if target_tags is not None:
            self._values["target_tags"] = target_tags

    @builtins.property
    def action(self) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#action DlmLifecyclePolicy#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsAction"], result)

    @builtins.property
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.'''
        result = self._values.get("copy_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#create_interval DlmLifecyclePolicy#create_interval}.'''
        result = self._values.get("create_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event_source(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsEventSource"]:
        '''event_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#event_source DlmLifecyclePolicy#event_source}
        '''
        result = self._values.get("event_source")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsEventSource"], result)

    @builtins.property
    def exclusions(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsExclusions"]:
        '''exclusions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclusions DlmLifecyclePolicy#exclusions}
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsExclusions"], result)

    @builtins.property
    def extend_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#extend_deletion DlmLifecyclePolicy#extend_deletion}.'''
        result = self._values.get("extend_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsParameters"]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsParameters"], result)

    @builtins.property
    def policy_language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_language DlmLifecyclePolicy#policy_language}.'''
        result = self._values.get("policy_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#policy_type DlmLifecyclePolicy#policy_type}.'''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_locations DlmLifecyclePolicy#resource_locations}.'''
        result = self._values.get("resource_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_type DlmLifecyclePolicy#resource_type}.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#resource_types DlmLifecyclePolicy#resource_types}.'''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retain_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_interval DlmLifecyclePolicy#retain_interval}.'''
        result = self._values.get("retain_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsSchedule"]]]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#schedule DlmLifecyclePolicy#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsSchedule"]]], result)

    @builtins.property
    def target_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target_tags DlmLifecyclePolicy#target_tags}.'''
        result = self._values.get("target_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsAction",
    jsii_struct_bases=[],
    name_mapping={"cross_region_copy": "crossRegionCopy", "name": "name"},
)
class DlmLifecyclePolicyPolicyDetailsAction:
    def __init__(
        self,
        *,
        cross_region_copy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
    ) -> None:
        '''
        :param cross_region_copy: cross_region_copy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cross_region_copy DlmLifecyclePolicy#cross_region_copy}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26890b6671d92d7545572f5b301e0d1969c65150415651162857a73ae3e275d0)
            check_type(argname="argument cross_region_copy", value=cross_region_copy, expected_type=type_hints["cross_region_copy"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cross_region_copy": cross_region_copy,
            "name": name,
        }

    @builtins.property
    def cross_region_copy(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy"]]:
        '''cross_region_copy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cross_region_copy DlmLifecyclePolicy#cross_region_copy}
        '''
        result = self._values.get("cross_region_copy")
        assert result is not None, "Required property 'cross_region_copy' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "target": "target",
        "retain_rule": "retainRule",
    },
)
class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Union["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]],
        target: builtins.str,
        retain_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#encryption_configuration DlmLifecyclePolicy#encryption_configuration}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target DlmLifecyclePolicy#target}.
        :param retain_rule: retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        '''
        if isinstance(encryption_configuration, dict):
            encryption_configuration = DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration(**encryption_configuration)
        if isinstance(retain_rule, dict):
            retain_rule = DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule(**retain_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b963efc6b9ad0f27f2794f5e99c7ae8336f0113f44ba1f6d40587aa76e21d17d)
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encryption_configuration": encryption_configuration,
            "target": target,
        }
        if retain_rule is not None:
            self._values["retain_rule"] = retain_rule

    @builtins.property
    def encryption_configuration(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration":
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#encryption_configuration DlmLifecyclePolicy#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        assert result is not None, "Required property 'encryption_configuration' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration", result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target DlmLifecyclePolicy#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retain_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule"]:
        '''retain_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        '''
        result = self._values.get("retain_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"cmk_arn": "cmkArn", "encrypted": "encrypted"},
)
class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration:
    def __init__(
        self,
        *,
        cmk_arn: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cmk_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7bf1f3bd21089904639984d3d181b0b20299ddb51dbd2da3599ff99768d49f)
            check_type(argname="argument cmk_arn", value=cmk_arn, expected_type=type_hints["cmk_arn"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cmk_arn is not None:
            self._values["cmk_arn"] = cmk_arn
        if encrypted is not None:
            self._values["encrypted"] = encrypted

    @builtins.property
    def cmk_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.'''
        result = self._values.get("cmk_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.'''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc23dca30a5f9cb16b076d9d8667c5c97a3b3865c2918b1247f91b0bc016dc3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCmkArn")
    def reset_cmk_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmkArn", []))

    @jsii.member(jsii_name="resetEncrypted")
    def reset_encrypted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncrypted", []))

    @builtins.property
    @jsii.member(jsii_name="cmkArnInput")
    def cmk_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cmkArnInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedInput")
    def encrypted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="cmkArn")
    def cmk_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cmkArn"))

    @cmk_arn.setter
    def cmk_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b45bb6db4981f82a2c2927d10166807789fae53861df11b49275e019bfe1b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmkArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00b0e66d58af39dca8534f56ab7a1c415df72a783f902a18b477c177224ed40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d4f72a7d4d1dd6e5eed31e105635cf774b0432a45ff880a7b2f59d12f8ddd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7de461397832524009602bdfae48d680a239694c5bf3fe32d1f3db6494b7347)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2209cad54d74cdeb10c20ea140a56fea1a227714fab88ddf8ecd7b0417fd12d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b04287af0acb8f80e95ed13ffba6729e8cd586fc2475278448af6cfd0bb680)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b53e5052284ed1f5c5d5a1529edb23310b47ffabdacca4c0bc6655a55fb5096)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4c95a8218e04cb252fa51021bd06ca196a161b370bef0bf9b68565497e69534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c7e327786014f7e45625eb3070dc83bb48d7bf2fa7c59cf1213ab8c2b26073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d76ceb7053e7c5c7c7f04b77a529945db768407271ebfe403ad63d8556e9142f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(
        self,
        *,
        cmk_arn: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cmk_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration(
            cmk_arn=cmk_arn, encrypted=encrypted
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putRetainRule")
    def put_retain_rule(
        self,
        *,
        interval: jsii.Number,
        interval_unit: builtins.str,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule(
            interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putRetainRule", [value]))

    @jsii.member(jsii_name="resetRetainRule")
    def reset_retain_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainRule", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference, jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="retainRule")
    def retain_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference", jsii.get(self, "retainRule"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retainRuleInput")
    def retain_rule_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule"], jsii.get(self, "retainRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78782477551083e8842f4a33b568120cb933f078abf88eafe7439ec8bf79e49d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcafa8a4edcf0a4a2341a668c10db21364c20ce833b9cfc8f3fc781c36c171b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
)
class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule:
    def __init__(self, *, interval: jsii.Number, interval_unit: builtins.str) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d60ced79f5e22dc19d5e35e55067572fcecb6397075f459098ab8d4a727c720)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "interval_unit": interval_unit,
        }

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        assert result is not None, "Required property 'interval_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39b3367f5d01890fcad8436622732197536b5db9bf3791b336d6d52862822f2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed072c4052f99af68d437890a92156f20d9d3677ba3cf1043687e7f0b0cd645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cbfc36a90ffd254744e300809680e9205ab876496d16182eecaeee8d7c1a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06bad5c023c5b5edc0ca3ac47470992869b03148f73acc867133a007078e74fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67cdcbe83b908fb433b26a1d68d3ab52ec0bdc45e083a73d66464de309c32de8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCrossRegionCopy")
    def put_cross_region_copy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30719f4cf780a3539bc4da6a998348a82b4e78becdbc0efa495132991a9456bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCrossRegionCopy", [value]))

    @builtins.property
    @jsii.member(jsii_name="crossRegionCopy")
    def cross_region_copy(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList, jsii.get(self, "crossRegionCopy"))

    @builtins.property
    @jsii.member(jsii_name="crossRegionCopyInput")
    def cross_region_copy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]], jsii.get(self, "crossRegionCopyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812a373ee7ea3d510f80985457194da0df12d1316ae862195f3281ceb5fd3361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsAction]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef992c8203835d101962752c452ad7a92a3c2cfb1dc9490b803de1c93a0432cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsEventSource",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters", "type": "type"},
)
class DlmLifecyclePolicyPolicyDetailsEventSource:
    def __init__(
        self,
        *,
        parameters: typing.Union["DlmLifecyclePolicyPolicyDetailsEventSourceParameters", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
    ) -> None:
        '''
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#type DlmLifecyclePolicy#type}.
        '''
        if isinstance(parameters, dict):
            parameters = DlmLifecyclePolicyPolicyDetailsEventSourceParameters(**parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83847bf8d87df1a522c3fcf21644a5fe08508ff075379c2f90696e5f55b84fa)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameters": parameters,
            "type": type,
        }

    @builtins.property
    def parameters(self) -> "DlmLifecyclePolicyPolicyDetailsEventSourceParameters":
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsEventSourceParameters", result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#type DlmLifecyclePolicy#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsEventSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e62b0d7c4312057b60331de0691ec6cac1ea0e09b0d37f5b95ca012b546727c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        description_regex: builtins.str,
        event_type: builtins.str,
        snapshot_owner: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param description_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#description_regex DlmLifecyclePolicy#description_regex}.
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#event_type DlmLifecyclePolicy#event_type}.
        :param snapshot_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#snapshot_owner DlmLifecyclePolicy#snapshot_owner}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsEventSourceParameters(
            description_regex=description_regex,
            event_type=event_type,
            snapshot_owner=snapshot_owner,
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsEventSourceParameters"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsEventSourceParameters"], jsii.get(self, "parametersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5d85a1cfbba3e5e4654f34035e175ef8994ebb173b1d3f146935d21e948b98b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e33fb95c56cb587ebbde33599a19475319f73c107da4d57a823128855eec833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsEventSourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "description_regex": "descriptionRegex",
        "event_type": "eventType",
        "snapshot_owner": "snapshotOwner",
    },
)
class DlmLifecyclePolicyPolicyDetailsEventSourceParameters:
    def __init__(
        self,
        *,
        description_regex: builtins.str,
        event_type: builtins.str,
        snapshot_owner: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param description_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#description_regex DlmLifecyclePolicy#description_regex}.
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#event_type DlmLifecyclePolicy#event_type}.
        :param snapshot_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#snapshot_owner DlmLifecyclePolicy#snapshot_owner}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b34c057aec859d97ae058fcf0b43befaf4b2d85f43298be44c69aeb6a67788e)
            check_type(argname="argument description_regex", value=description_regex, expected_type=type_hints["description_regex"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument snapshot_owner", value=snapshot_owner, expected_type=type_hints["snapshot_owner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description_regex": description_regex,
            "event_type": event_type,
            "snapshot_owner": snapshot_owner,
        }

    @builtins.property
    def description_regex(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#description_regex DlmLifecyclePolicy#description_regex}.'''
        result = self._values.get("description_regex")
        assert result is not None, "Required property 'description_regex' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#event_type DlmLifecyclePolicy#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snapshot_owner(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#snapshot_owner DlmLifecyclePolicy#snapshot_owner}.'''
        result = self._values.get("snapshot_owner")
        assert result is not None, "Required property 'snapshot_owner' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsEventSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd62e334f723a921d5d55001f8221f1fa7683812d3ec6b2e389f7d2d091e83cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="descriptionRegexInput")
    def description_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotOwnerInput")
    def snapshot_owner_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "snapshotOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionRegex")
    def description_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "descriptionRegex"))

    @description_regex.setter
    def description_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e804d50f198597b96b16d3f3cbcb2dca9428a18d92bdec4aae9e0f054938147a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "descriptionRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4440ff741fc67981bb771f49323a8172237398cbc718df39ed43197c151974d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotOwner")
    def snapshot_owner(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "snapshotOwner"))

    @snapshot_owner.setter
    def snapshot_owner(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3bc941413402d7a7eaff616be908314eb85d63c8e9ef2da1b1cdc3f0bb89b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSourceParameters]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSourceParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSourceParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e3467b8e0ea7f7d6cbd3442c309f3fea7838854a23ca5b718ef52c0f4ef592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsExclusions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_boot_volumes": "excludeBootVolumes",
        "exclude_tags": "excludeTags",
        "exclude_volume_types": "excludeVolumeTypes",
    },
)
class DlmLifecyclePolicyPolicyDetailsExclusions:
    def __init__(
        self,
        *,
        exclude_boot_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        exclude_volume_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude_boot_volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_boot_volumes DlmLifecyclePolicy#exclude_boot_volumes}.
        :param exclude_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_tags DlmLifecyclePolicy#exclude_tags}.
        :param exclude_volume_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_volume_types DlmLifecyclePolicy#exclude_volume_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6188c4d66ecb1310b7be3567ace24f9a3d4f15e0f1e0cd7745fac4d2c9a2b74f)
            check_type(argname="argument exclude_boot_volumes", value=exclude_boot_volumes, expected_type=type_hints["exclude_boot_volumes"])
            check_type(argname="argument exclude_tags", value=exclude_tags, expected_type=type_hints["exclude_tags"])
            check_type(argname="argument exclude_volume_types", value=exclude_volume_types, expected_type=type_hints["exclude_volume_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_boot_volumes is not None:
            self._values["exclude_boot_volumes"] = exclude_boot_volumes
        if exclude_tags is not None:
            self._values["exclude_tags"] = exclude_tags
        if exclude_volume_types is not None:
            self._values["exclude_volume_types"] = exclude_volume_types

    @builtins.property
    def exclude_boot_volumes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_boot_volumes DlmLifecyclePolicy#exclude_boot_volumes}.'''
        result = self._values.get("exclude_boot_volumes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_tags DlmLifecyclePolicy#exclude_tags}.'''
        result = self._values.get("exclude_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def exclude_volume_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_volume_types DlmLifecyclePolicy#exclude_volume_types}.'''
        result = self._values.get("exclude_volume_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsExclusions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__230bcade77a41b989f5c9dfd19ef730d6b3c6623fb87bc5164f3da9bb13d54d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeBootVolumes")
    def reset_exclude_boot_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeBootVolumes", []))

    @jsii.member(jsii_name="resetExcludeTags")
    def reset_exclude_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeTags", []))

    @jsii.member(jsii_name="resetExcludeVolumeTypes")
    def reset_exclude_volume_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeVolumeTypes", []))

    @builtins.property
    @jsii.member(jsii_name="excludeBootVolumesInput")
    def exclude_boot_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeBootVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeTagsInput")
    def exclude_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "excludeTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeVolumeTypesInput")
    def exclude_volume_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeVolumeTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeBootVolumes")
    def exclude_boot_volumes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeBootVolumes"))

    @exclude_boot_volumes.setter
    def exclude_boot_volumes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f5b471eb848b6d23628a7587ac03d96621747fa951f918b5d1fb043b0436f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeBootVolumes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeTags")
    def exclude_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "excludeTags"))

    @exclude_tags.setter
    def exclude_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad12df39b8795cdee3b5cd250cfe848a5307c8107019577f9c6aaa9867026647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeVolumeTypes")
    def exclude_volume_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeVolumeTypes"))

    @exclude_volume_types.setter
    def exclude_volume_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f659c9c90f6b29823582b0150b3028a2fe141f172899a48d0f39ef1ae773287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeVolumeTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e5e7895019dd941c0ece77497b57945d552620f3db64776d279cb2fcc75067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c847fc5dd9ba2a22a44e7efcb3dcd18b34992c503746b199957f505608d2140d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        cross_region_copy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy, typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
    ) -> None:
        '''
        :param cross_region_copy: cross_region_copy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cross_region_copy DlmLifecyclePolicy#cross_region_copy}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsAction(
            cross_region_copy=cross_region_copy, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putEventSource")
    def put_event_source(
        self,
        *,
        parameters: typing.Union[DlmLifecyclePolicyPolicyDetailsEventSourceParameters, typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
    ) -> None:
        '''
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#parameters DlmLifecyclePolicy#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#type DlmLifecyclePolicy#type}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsEventSource(
            parameters=parameters, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEventSource", [value]))

    @jsii.member(jsii_name="putExclusions")
    def put_exclusions(
        self,
        *,
        exclude_boot_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        exclude_volume_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude_boot_volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_boot_volumes DlmLifecyclePolicy#exclude_boot_volumes}.
        :param exclude_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_tags DlmLifecyclePolicy#exclude_tags}.
        :param exclude_volume_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_volume_types DlmLifecyclePolicy#exclude_volume_types}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsExclusions(
            exclude_boot_volumes=exclude_boot_volumes,
            exclude_tags=exclude_tags,
            exclude_volume_types=exclude_volume_types,
        )

        return typing.cast(None, jsii.invoke(self, "putExclusions", [value]))

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param exclude_boot_volume: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_boot_volume DlmLifecyclePolicy#exclude_boot_volume}.
        :param no_reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#no_reboot DlmLifecyclePolicy#no_reboot}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsParameters(
            exclude_boot_volume=exclude_boot_volume, no_reboot=no_reboot
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsSchedule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af32f46a0a0640385c6a433dd75fdca1bb9c4fce9f3da41b6845036bcf639bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetCopyTags")
    def reset_copy_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTags", []))

    @jsii.member(jsii_name="resetCreateInterval")
    def reset_create_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateInterval", []))

    @jsii.member(jsii_name="resetEventSource")
    def reset_event_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventSource", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @jsii.member(jsii_name="resetExtendDeletion")
    def reset_extend_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendDeletion", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPolicyLanguage")
    def reset_policy_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyLanguage", []))

    @jsii.member(jsii_name="resetPolicyType")
    def reset_policy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyType", []))

    @jsii.member(jsii_name="resetResourceLocations")
    def reset_resource_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceLocations", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetResourceTypes")
    def reset_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypes", []))

    @jsii.member(jsii_name="resetRetainInterval")
    def reset_retain_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainInterval", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTargetTags")
    def reset_target_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetTags", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> DlmLifecyclePolicyPolicyDetailsActionOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="eventSource")
    def event_source(self) -> DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference, jsii.get(self, "eventSource"))

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference, jsii.get(self, "exclusions"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "DlmLifecyclePolicyPolicyDetailsParametersOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "DlmLifecyclePolicyPolicyDetailsScheduleList":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleList", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsAction]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTagsInput")
    def copy_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="createIntervalInput")
    def create_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "createIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceInput")
    def event_source_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource], jsii.get(self, "eventSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="extendDeletionInput")
    def extend_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "extendDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsParameters"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsParameters"], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="policyLanguageInput")
    def policy_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="policyTypeInput")
    def policy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceLocationsInput")
    def resource_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="retainIntervalInput")
    def retain_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retainIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsSchedule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsSchedule"]]], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTagsInput")
    def target_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "targetTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTags")
    def copy_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTags"))

    @copy_tags.setter
    def copy_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7522efbdd96f1e589045221191d0f4555aec26c723c961541cead6d3fdb06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createInterval")
    def create_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createInterval"))

    @create_interval.setter
    def create_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a05d6c5885e15a3c7a09df7edefb363eb00e24b12e0274d0975570653d4c031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendDeletion")
    def extend_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "extendDeletion"))

    @extend_deletion.setter
    def extend_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f6a0e869d858f2d87b9a54a004276bdd1cf6acfbe1f37cdadb8186d5b2dd50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyLanguage")
    def policy_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyLanguage"))

    @policy_language.setter
    def policy_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57a37b003fe4cf9da0705b5dae2eee6630bd38d081adc89f0545e72d341da0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyLanguage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyType"))

    @policy_type.setter
    def policy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c073121b9a06cde840aea522af4b6c8ba947c51a35e5271da4e6209b014991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceLocations")
    def resource_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceLocations"))

    @resource_locations.setter
    def resource_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a371da97eec332d4846ff5eb0b3aa412bb41c5ead25980d285fe7f6268d236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa511b7b46db524f48795bccd1cd6e7e5f68cab79eca1559c95a17c9d2de331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeca2438878be6f2620d641f54e1fb82d4ac8e168e42adc3a194da951ae2d5a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retainInterval")
    def retain_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retainInterval"))

    @retain_interval.setter
    def retain_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edba55eb00cf93373dcafa3d77cc963192a909fcb981f4db5c6726dccad93689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetTags")
    def target_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "targetTags"))

    @target_tags.setter
    def target_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3c3e4c06ac550f34035f5fd0b30322a2c424441212747327893e7322055b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DlmLifecyclePolicyPolicyDetails]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfbf2a47e2aeb2533733f1b5a53e3dc41b2dc5c8e5d3ce495ff063d158031e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsParameters",
    jsii_struct_bases=[],
    name_mapping={"exclude_boot_volume": "excludeBootVolume", "no_reboot": "noReboot"},
)
class DlmLifecyclePolicyPolicyDetailsParameters:
    def __init__(
        self,
        *,
        exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param exclude_boot_volume: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_boot_volume DlmLifecyclePolicy#exclude_boot_volume}.
        :param no_reboot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#no_reboot DlmLifecyclePolicy#no_reboot}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b38768870d44ac053c7f97df700cbfd05081b7c1077f1b9b8dbd7bf4bb5e6ea)
            check_type(argname="argument exclude_boot_volume", value=exclude_boot_volume, expected_type=type_hints["exclude_boot_volume"])
            check_type(argname="argument no_reboot", value=no_reboot, expected_type=type_hints["no_reboot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_boot_volume is not None:
            self._values["exclude_boot_volume"] = exclude_boot_volume
        if no_reboot is not None:
            self._values["no_reboot"] = no_reboot

    @builtins.property
    def exclude_boot_volume(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#exclude_boot_volume DlmLifecyclePolicy#exclude_boot_volume}.'''
        result = self._values.get("exclude_boot_volume")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def no_reboot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#no_reboot DlmLifecyclePolicy#no_reboot}.'''
        result = self._values.get("no_reboot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67ebd01bf0d5519fc4cec1a5f14eb08e1bef1217cb58df9b2911475accafc18e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeBootVolume")
    def reset_exclude_boot_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeBootVolume", []))

    @jsii.member(jsii_name="resetNoReboot")
    def reset_no_reboot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoReboot", []))

    @builtins.property
    @jsii.member(jsii_name="excludeBootVolumeInput")
    def exclude_boot_volume_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeBootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="noRebootInput")
    def no_reboot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noRebootInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeBootVolume")
    def exclude_boot_volume(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeBootVolume"))

    @exclude_boot_volume.setter
    def exclude_boot_volume(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adff67b011888fecbdf8ecb7755dd830083a2fee840ad3f562efcff9cc010355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeBootVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noReboot")
    def no_reboot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noReboot"))

    @no_reboot.setter
    def no_reboot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9afed822890caea61b017d38c1793cbd0a61f9923adf82693f88dc9208c3bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noReboot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsParameters]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6efa990e98c2e546db129083dfcaf6bd97d33d572cd4a0b89aa42b65054d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "create_rule": "createRule",
        "name": "name",
        "retain_rule": "retainRule",
        "archive_rule": "archiveRule",
        "copy_tags": "copyTags",
        "cross_region_copy_rule": "crossRegionCopyRule",
        "deprecate_rule": "deprecateRule",
        "fast_restore_rule": "fastRestoreRule",
        "share_rule": "shareRule",
        "tags_to_add": "tagsToAdd",
        "variable_tags": "variableTags",
    },
)
class DlmLifecyclePolicyPolicyDetailsSchedule:
    def __init__(
        self,
        *,
        create_rule: typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCreateRule", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        retain_rule: typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleRetainRule", typing.Dict[builtins.str, typing.Any]],
        archive_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cross_region_copy_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        deprecate_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_restore_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule", typing.Dict[builtins.str, typing.Any]]] = None,
        share_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleShareRule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags_to_add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variable_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param create_rule: create_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#create_rule DlmLifecyclePolicy#create_rule}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.
        :param retain_rule: retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        :param archive_rule: archive_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#archive_rule DlmLifecyclePolicy#archive_rule}
        :param copy_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.
        :param cross_region_copy_rule: cross_region_copy_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cross_region_copy_rule DlmLifecyclePolicy#cross_region_copy_rule}
        :param deprecate_rule: deprecate_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#deprecate_rule DlmLifecyclePolicy#deprecate_rule}
        :param fast_restore_rule: fast_restore_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#fast_restore_rule DlmLifecyclePolicy#fast_restore_rule}
        :param share_rule: share_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#share_rule DlmLifecyclePolicy#share_rule}
        :param tags_to_add: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#tags_to_add DlmLifecyclePolicy#tags_to_add}.
        :param variable_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#variable_tags DlmLifecyclePolicy#variable_tags}.
        '''
        if isinstance(create_rule, dict):
            create_rule = DlmLifecyclePolicyPolicyDetailsScheduleCreateRule(**create_rule)
        if isinstance(retain_rule, dict):
            retain_rule = DlmLifecyclePolicyPolicyDetailsScheduleRetainRule(**retain_rule)
        if isinstance(archive_rule, dict):
            archive_rule = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule(**archive_rule)
        if isinstance(deprecate_rule, dict):
            deprecate_rule = DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule(**deprecate_rule)
        if isinstance(fast_restore_rule, dict):
            fast_restore_rule = DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule(**fast_restore_rule)
        if isinstance(share_rule, dict):
            share_rule = DlmLifecyclePolicyPolicyDetailsScheduleShareRule(**share_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2a8090c5d82e4e0885339a185710eaa19cdcecd03b0f8bba8af6c969fce5c4)
            check_type(argname="argument create_rule", value=create_rule, expected_type=type_hints["create_rule"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
            check_type(argname="argument archive_rule", value=archive_rule, expected_type=type_hints["archive_rule"])
            check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
            check_type(argname="argument cross_region_copy_rule", value=cross_region_copy_rule, expected_type=type_hints["cross_region_copy_rule"])
            check_type(argname="argument deprecate_rule", value=deprecate_rule, expected_type=type_hints["deprecate_rule"])
            check_type(argname="argument fast_restore_rule", value=fast_restore_rule, expected_type=type_hints["fast_restore_rule"])
            check_type(argname="argument share_rule", value=share_rule, expected_type=type_hints["share_rule"])
            check_type(argname="argument tags_to_add", value=tags_to_add, expected_type=type_hints["tags_to_add"])
            check_type(argname="argument variable_tags", value=variable_tags, expected_type=type_hints["variable_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "create_rule": create_rule,
            "name": name,
            "retain_rule": retain_rule,
        }
        if archive_rule is not None:
            self._values["archive_rule"] = archive_rule
        if copy_tags is not None:
            self._values["copy_tags"] = copy_tags
        if cross_region_copy_rule is not None:
            self._values["cross_region_copy_rule"] = cross_region_copy_rule
        if deprecate_rule is not None:
            self._values["deprecate_rule"] = deprecate_rule
        if fast_restore_rule is not None:
            self._values["fast_restore_rule"] = fast_restore_rule
        if share_rule is not None:
            self._values["share_rule"] = share_rule
        if tags_to_add is not None:
            self._values["tags_to_add"] = tags_to_add
        if variable_tags is not None:
            self._values["variable_tags"] = variable_tags

    @builtins.property
    def create_rule(self) -> "DlmLifecyclePolicyPolicyDetailsScheduleCreateRule":
        '''create_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#create_rule DlmLifecyclePolicy#create_rule}
        '''
        result = self._values.get("create_rule")
        assert result is not None, "Required property 'create_rule' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleCreateRule", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#name DlmLifecyclePolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retain_rule(self) -> "DlmLifecyclePolicyPolicyDetailsScheduleRetainRule":
        '''retain_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        '''
        result = self._values.get("retain_rule")
        assert result is not None, "Required property 'retain_rule' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleRetainRule", result)

    @builtins.property
    def archive_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule"]:
        '''archive_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#archive_rule DlmLifecyclePolicy#archive_rule}
        '''
        result = self._values.get("archive_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule"], result)

    @builtins.property
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.'''
        result = self._values.get("copy_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cross_region_copy_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule"]]]:
        '''cross_region_copy_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cross_region_copy_rule DlmLifecyclePolicy#cross_region_copy_rule}
        '''
        result = self._values.get("cross_region_copy_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule"]]], result)

    @builtins.property
    def deprecate_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule"]:
        '''deprecate_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#deprecate_rule DlmLifecyclePolicy#deprecate_rule}
        '''
        result = self._values.get("deprecate_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule"], result)

    @builtins.property
    def fast_restore_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule"]:
        '''fast_restore_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#fast_restore_rule DlmLifecyclePolicy#fast_restore_rule}
        '''
        result = self._values.get("fast_restore_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule"], result)

    @builtins.property
    def share_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleShareRule"]:
        '''share_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#share_rule DlmLifecyclePolicy#share_rule}
        '''
        result = self._values.get("share_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleShareRule"], result)

    @builtins.property
    def tags_to_add(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#tags_to_add DlmLifecyclePolicy#tags_to_add}.'''
        result = self._values.get("tags_to_add")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def variable_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#variable_tags DlmLifecyclePolicy#variable_tags}.'''
        result = self._values.get("variable_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule",
    jsii_struct_bases=[],
    name_mapping={"archive_retain_rule": "archiveRetainRule"},
)
class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule:
    def __init__(
        self,
        *,
        archive_retain_rule: typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param archive_retain_rule: archive_retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#archive_retain_rule DlmLifecyclePolicy#archive_retain_rule}
        '''
        if isinstance(archive_retain_rule, dict):
            archive_retain_rule = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule(**archive_retain_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f24cbff243e7d7b082a095c14f7a02d27465ed4871d7068ab32f86520bdc75)
            check_type(argname="argument archive_retain_rule", value=archive_retain_rule, expected_type=type_hints["archive_retain_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "archive_retain_rule": archive_retain_rule,
        }

    @builtins.property
    def archive_retain_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule":
        '''archive_retain_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#archive_retain_rule DlmLifecyclePolicy#archive_retain_rule}
        '''
        result = self._values.get("archive_retain_rule")
        assert result is not None, "Required property 'archive_retain_rule' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule",
    jsii_struct_bases=[],
    name_mapping={"retention_archive_tier": "retentionArchiveTier"},
)
class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule:
    def __init__(
        self,
        *,
        retention_archive_tier: typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param retention_archive_tier: retention_archive_tier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retention_archive_tier DlmLifecyclePolicy#retention_archive_tier}
        '''
        if isinstance(retention_archive_tier, dict):
            retention_archive_tier = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier(**retention_archive_tier)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b837c9324b04e029e4cfda0be85001922816a6d1d7d5c613fa531f22d37343a9)
            check_type(argname="argument retention_archive_tier", value=retention_archive_tier, expected_type=type_hints["retention_archive_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retention_archive_tier": retention_archive_tier,
        }

    @builtins.property
    def retention_archive_tier(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier":
        '''retention_archive_tier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retention_archive_tier DlmLifecyclePolicy#retention_archive_tier}
        '''
        result = self._values.get("retention_archive_tier")
        assert result is not None, "Required property 'retention_archive_tier' is missing"
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32cbf2bfedcb40e9af12f900b69eef7c5c763b3830e7315d382c1f1b65a4eba9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRetentionArchiveTier")
    def put_retention_archive_tier(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier(
            count=count, interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionArchiveTier", [value]))

    @builtins.property
    @jsii.member(jsii_name="retentionArchiveTier")
    def retention_archive_tier(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference", jsii.get(self, "retentionArchiveTier"))

    @builtins.property
    @jsii.member(jsii_name="retentionArchiveTierInput")
    def retention_archive_tier_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier"], jsii.get(self, "retentionArchiveTierInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ab78402ba8b41c3231debc9252faa2819b2cb724b36f9494acef48ed36dae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "interval": "interval",
        "interval_unit": "intervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920f250c863be29c548545898b0014ad4aead27a33c72585866bf6e33c31b69f)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33545afb6262d5b464b73579371e981d085ca27f84dd744d16955de130fd9cce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa54e20516757dee23a5cfa25b18667c0382e92c299720cc5be71894849d6c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64274b9cca7b9696d1e10afa9b82d632558fe7d97b12736f03836d250b94e7f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4858ef838e55aea3f8c9c20ae192cbd141beea5a02f11d473db6af9bd77c0ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00774205dfb61276a3525af657ec752f950a594aed16ec97f0ba86fff199016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed8e46da36a9c64fe6dfdfa3ed9833982177da33a31dbd9ab3cc4ed441e8f75a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putArchiveRetainRule")
    def put_archive_retain_rule(
        self,
        *,
        retention_archive_tier: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param retention_archive_tier: retention_archive_tier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retention_archive_tier DlmLifecyclePolicy#retention_archive_tier}
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule(
            retention_archive_tier=retention_archive_tier
        )

        return typing.cast(None, jsii.invoke(self, "putArchiveRetainRule", [value]))

    @builtins.property
    @jsii.member(jsii_name="archiveRetainRule")
    def archive_retain_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference, jsii.get(self, "archiveRetainRule"))

    @builtins.property
    @jsii.member(jsii_name="archiveRetainRuleInput")
    def archive_retain_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule], jsii.get(self, "archiveRetainRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e6119de975dfe0e1555a2f7b315b8a651c6dc6ee7e535be40b47d38bf8691d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCreateRule",
    jsii_struct_bases=[],
    name_mapping={
        "cron_expression": "cronExpression",
        "interval": "interval",
        "interval_unit": "intervalUnit",
        "location": "location",
        "scripts": "scripts",
        "times": "times",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleCreateRule:
    def __init__(
        self,
        *,
        cron_expression: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        scripts: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts", typing.Dict[builtins.str, typing.Any]]] = None,
        times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cron_expression DlmLifecyclePolicy#cron_expression}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#location DlmLifecyclePolicy#location}.
        :param scripts: scripts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#scripts DlmLifecyclePolicy#scripts}
        :param times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#times DlmLifecyclePolicy#times}.
        '''
        if isinstance(scripts, dict):
            scripts = DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts(**scripts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c77d5cb3d264940bf656d1f240c79411aad70a46c630bcd8a94dbbb68c5d13)
            check_type(argname="argument cron_expression", value=cron_expression, expected_type=type_hints["cron_expression"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
            check_type(argname="argument times", value=times, expected_type=type_hints["times"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron_expression is not None:
            self._values["cron_expression"] = cron_expression
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit
        if location is not None:
            self._values["location"] = location
        if scripts is not None:
            self._values["scripts"] = scripts
        if times is not None:
            self._values["times"] = times

    @builtins.property
    def cron_expression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cron_expression DlmLifecyclePolicy#cron_expression}.'''
        result = self._values.get("cron_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#location DlmLifecyclePolicy#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scripts(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts"]:
        '''scripts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#scripts DlmLifecyclePolicy#scripts}
        '''
        result = self._values.get("scripts")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts"], result)

    @builtins.property
    def times(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#times DlmLifecyclePolicy#times}.'''
        result = self._values.get("times")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCreateRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c3b2a63d8e8fc153571a39c7348449ccdf9d372ce34ff31cdc24fbdea3cd927)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScripts")
    def put_scripts(
        self,
        *,
        execution_handler: builtins.str,
        execute_operation_on_script_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        execution_handler_service: typing.Optional[builtins.str] = None,
        execution_timeout: typing.Optional[jsii.Number] = None,
        maximum_retry_count: typing.Optional[jsii.Number] = None,
        stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param execution_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_handler DlmLifecyclePolicy#execution_handler}.
        :param execute_operation_on_script_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execute_operation_on_script_failure DlmLifecyclePolicy#execute_operation_on_script_failure}.
        :param execution_handler_service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_handler_service DlmLifecyclePolicy#execution_handler_service}.
        :param execution_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_timeout DlmLifecyclePolicy#execution_timeout}.
        :param maximum_retry_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#maximum_retry_count DlmLifecyclePolicy#maximum_retry_count}.
        :param stages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#stages DlmLifecyclePolicy#stages}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts(
            execution_handler=execution_handler,
            execute_operation_on_script_failure=execute_operation_on_script_failure,
            execution_handler_service=execution_handler_service,
            execution_timeout=execution_timeout,
            maximum_retry_count=maximum_retry_count,
            stages=stages,
        )

        return typing.cast(None, jsii.invoke(self, "putScripts", [value]))

    @jsii.member(jsii_name="resetCronExpression")
    def reset_cron_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronExpression", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetScripts")
    def reset_scripts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScripts", []))

    @jsii.member(jsii_name="resetTimes")
    def reset_times(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimes", []))

    @builtins.property
    @jsii.member(jsii_name="scripts")
    def scripts(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference", jsii.get(self, "scripts"))

    @builtins.property
    @jsii.member(jsii_name="cronExpressionInput")
    def cron_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptsInput")
    def scripts_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts"], jsii.get(self, "scriptsInput"))

    @builtins.property
    @jsii.member(jsii_name="timesInput")
    def times_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "timesInput"))

    @builtins.property
    @jsii.member(jsii_name="cronExpression")
    def cron_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronExpression"))

    @cron_expression.setter
    def cron_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb3677ea81fe6b1fc93b721cc23f9c09a1af172dd05c00b9822b9d507577a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e62dda270ae41c51b0bfb85284616f39debb1f91b2c2a488f943d4b64f4bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7825b54efff488f9b47ab6066724696ad81965f512a809effdbd0f2e800d1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc3cb09f5a8bb422b45c938a8d168071505cb067a4104769ed182e878a72377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="times")
    def times(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "times"))

    @times.setter
    def times(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0757a47f22113dda5a5525b901c353b4d1caf03fa9988f07168aa94fc4447dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "times", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70a019a87b668f6b73b9547fd6fbed5c5176e2d00f3ddab8fa1640e743c2081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts",
    jsii_struct_bases=[],
    name_mapping={
        "execution_handler": "executionHandler",
        "execute_operation_on_script_failure": "executeOperationOnScriptFailure",
        "execution_handler_service": "executionHandlerService",
        "execution_timeout": "executionTimeout",
        "maximum_retry_count": "maximumRetryCount",
        "stages": "stages",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts:
    def __init__(
        self,
        *,
        execution_handler: builtins.str,
        execute_operation_on_script_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        execution_handler_service: typing.Optional[builtins.str] = None,
        execution_timeout: typing.Optional[jsii.Number] = None,
        maximum_retry_count: typing.Optional[jsii.Number] = None,
        stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param execution_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_handler DlmLifecyclePolicy#execution_handler}.
        :param execute_operation_on_script_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execute_operation_on_script_failure DlmLifecyclePolicy#execute_operation_on_script_failure}.
        :param execution_handler_service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_handler_service DlmLifecyclePolicy#execution_handler_service}.
        :param execution_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_timeout DlmLifecyclePolicy#execution_timeout}.
        :param maximum_retry_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#maximum_retry_count DlmLifecyclePolicy#maximum_retry_count}.
        :param stages: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#stages DlmLifecyclePolicy#stages}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be160b3b90a1b9818c261381285218586b218aa0fd48271161defa2dd04a62ac)
            check_type(argname="argument execution_handler", value=execution_handler, expected_type=type_hints["execution_handler"])
            check_type(argname="argument execute_operation_on_script_failure", value=execute_operation_on_script_failure, expected_type=type_hints["execute_operation_on_script_failure"])
            check_type(argname="argument execution_handler_service", value=execution_handler_service, expected_type=type_hints["execution_handler_service"])
            check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
            check_type(argname="argument maximum_retry_count", value=maximum_retry_count, expected_type=type_hints["maximum_retry_count"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_handler": execution_handler,
        }
        if execute_operation_on_script_failure is not None:
            self._values["execute_operation_on_script_failure"] = execute_operation_on_script_failure
        if execution_handler_service is not None:
            self._values["execution_handler_service"] = execution_handler_service
        if execution_timeout is not None:
            self._values["execution_timeout"] = execution_timeout
        if maximum_retry_count is not None:
            self._values["maximum_retry_count"] = maximum_retry_count
        if stages is not None:
            self._values["stages"] = stages

    @builtins.property
    def execution_handler(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_handler DlmLifecyclePolicy#execution_handler}.'''
        result = self._values.get("execution_handler")
        assert result is not None, "Required property 'execution_handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execute_operation_on_script_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execute_operation_on_script_failure DlmLifecyclePolicy#execute_operation_on_script_failure}.'''
        result = self._values.get("execute_operation_on_script_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def execution_handler_service(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_handler_service DlmLifecyclePolicy#execution_handler_service}.'''
        result = self._values.get("execution_handler_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#execution_timeout DlmLifecyclePolicy#execution_timeout}.'''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_retry_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#maximum_retry_count DlmLifecyclePolicy#maximum_retry_count}.'''
        result = self._values.get("maximum_retry_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#stages DlmLifecyclePolicy#stages}.'''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60f513ba34bf1ce0d9a5390e660df293a249bf1efa44af499ed12b74546c78bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecuteOperationOnScriptFailure")
    def reset_execute_operation_on_script_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecuteOperationOnScriptFailure", []))

    @jsii.member(jsii_name="resetExecutionHandlerService")
    def reset_execution_handler_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionHandlerService", []))

    @jsii.member(jsii_name="resetExecutionTimeout")
    def reset_execution_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionTimeout", []))

    @jsii.member(jsii_name="resetMaximumRetryCount")
    def reset_maximum_retry_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetryCount", []))

    @jsii.member(jsii_name="resetStages")
    def reset_stages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStages", []))

    @builtins.property
    @jsii.member(jsii_name="executeOperationOnScriptFailureInput")
    def execute_operation_on_script_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "executeOperationOnScriptFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="executionHandlerInput")
    def execution_handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionHandlerInput"))

    @builtins.property
    @jsii.member(jsii_name="executionHandlerServiceInput")
    def execution_handler_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionHandlerServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="executionTimeoutInput")
    def execution_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetryCountInput")
    def maximum_retry_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumRetryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="stagesInput")
    def stages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stagesInput"))

    @builtins.property
    @jsii.member(jsii_name="executeOperationOnScriptFailure")
    def execute_operation_on_script_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "executeOperationOnScriptFailure"))

    @execute_operation_on_script_failure.setter
    def execute_operation_on_script_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae528c62bb4306839eacc3ecfdbb7c89fd71e8c88358e907372341551f6becf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeOperationOnScriptFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionHandler")
    def execution_handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionHandler"))

    @execution_handler.setter
    def execution_handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad36fc50a8acd42e1f78b0006796e0e9b55624a281b681a3e90fba8191e18ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionHandler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionHandlerService")
    def execution_handler_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionHandlerService"))

    @execution_handler_service.setter
    def execution_handler_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef9a785904a86de44ded125359c204ba078545878fd5d9959d67512f96fbb20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionHandlerService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab3cf9dc33cc38d6d71ee6356bb018ba331b41eb565720b269820057be809ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumRetryCount")
    def maximum_retry_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumRetryCount"))

    @maximum_retry_count.setter
    def maximum_retry_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2f40e31db58e9d9ed5cb5689be063033f1a746f80625e63dd34fdfd810b9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumRetryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stages"))

    @stages.setter
    def stages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8b3de6999b06624c87820e4ca9a9c1194a682d85562d6f9885fbbef01eba50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1411213ae5ac0f54dcd3abb9df0b8fbc879aea7d675c10747a49dfd9c73f2f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule",
    jsii_struct_bases=[],
    name_mapping={
        "encrypted": "encrypted",
        "cmk_arn": "cmkArn",
        "copy_tags": "copyTags",
        "deprecate_rule": "deprecateRule",
        "retain_rule": "retainRule",
        "target": "target",
        "target_region": "targetRegion",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule:
    def __init__(
        self,
        *,
        encrypted: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cmk_arn: typing.Optional[builtins.str] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deprecate_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule", typing.Dict[builtins.str, typing.Any]]] = None,
        retain_rule: typing.Optional[typing.Union["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[builtins.str] = None,
        target_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.
        :param cmk_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.
        :param copy_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.
        :param deprecate_rule: deprecate_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#deprecate_rule DlmLifecyclePolicy#deprecate_rule}
        :param retain_rule: retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target DlmLifecyclePolicy#target}.
        :param target_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target_region DlmLifecyclePolicy#target_region}.
        '''
        if isinstance(deprecate_rule, dict):
            deprecate_rule = DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule(**deprecate_rule)
        if isinstance(retain_rule, dict):
            retain_rule = DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule(**retain_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2862e2fe9889b8004d4ac4a41843c4082162ab35a06ed075943b670747ed12)
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument cmk_arn", value=cmk_arn, expected_type=type_hints["cmk_arn"])
            check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
            check_type(argname="argument deprecate_rule", value=deprecate_rule, expected_type=type_hints["deprecate_rule"])
            check_type(argname="argument retain_rule", value=retain_rule, expected_type=type_hints["retain_rule"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument target_region", value=target_region, expected_type=type_hints["target_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encrypted": encrypted,
        }
        if cmk_arn is not None:
            self._values["cmk_arn"] = cmk_arn
        if copy_tags is not None:
            self._values["copy_tags"] = copy_tags
        if deprecate_rule is not None:
            self._values["deprecate_rule"] = deprecate_rule
        if retain_rule is not None:
            self._values["retain_rule"] = retain_rule
        if target is not None:
            self._values["target"] = target
        if target_region is not None:
            self._values["target_region"] = target_region

    @builtins.property
    def encrypted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#encrypted DlmLifecyclePolicy#encrypted}.'''
        result = self._values.get("encrypted")
        assert result is not None, "Required property 'encrypted' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def cmk_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cmk_arn DlmLifecyclePolicy#cmk_arn}.'''
        result = self._values.get("cmk_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#copy_tags DlmLifecyclePolicy#copy_tags}.'''
        result = self._values.get("copy_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deprecate_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule"]:
        '''deprecate_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#deprecate_rule DlmLifecyclePolicy#deprecate_rule}
        '''
        result = self._values.get("deprecate_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule"], result)

    @builtins.property
    def retain_rule(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule"]:
        '''retain_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#retain_rule DlmLifecyclePolicy#retain_rule}
        '''
        result = self._values.get("retain_rule")
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule"], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target DlmLifecyclePolicy#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target_region DlmLifecyclePolicy#target_region}.'''
        result = self._values.get("target_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
)
class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule:
    def __init__(self, *, interval: jsii.Number, interval_unit: builtins.str) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045732adf3e07d8ff890172ebe09a0501d6890984ca8087227c0d598dfb9bfc9)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "interval_unit": interval_unit,
        }

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        assert result is not None, "Required property 'interval_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bb1bcf005c6f60eb1f77d70a4497d39b04280b92bc15abc5c42121ce3e27e7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6505577fc0ebf04bcdbf021c66cd2d91468175866c50e90c2fffc6a3c125796b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f160771898724a50382b352409920df1ca8a5451cab638dc5158f36bc0d297c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cba936299741674e2ccc97bf000674222466b7a8c9644db318a1e044492d75d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9e561fb47925aa0ff6132d436b2e64b464dbc8c6682d11c17ef85e998b282d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8018b297c7718073c3e0753e4f50c4449a9247a082594ab377694db834de4e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9870ff33a67d028aae6730cbb9a74d753385b156eb31312559e14fc15c66566a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a671f4ec8cf20e741c3f11e06de9fadfeb973a20e7643a51842a11ea41fb62cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda6c5458891e77735f9d7dbde6bbfef12fa50cbf54e2630f39d811727c76a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca6560e1cdba675794de008046e01816dbffe706adae03c828b2a698cb33f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__977027d87620a12d7ca655da01a23b8144ee43e1cf9baca6ccd48cd1d7724565)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDeprecateRule")
    def put_deprecate_rule(
        self,
        *,
        interval: jsii.Number,
        interval_unit: builtins.str,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule(
            interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putDeprecateRule", [value]))

    @jsii.member(jsii_name="putRetainRule")
    def put_retain_rule(
        self,
        *,
        interval: jsii.Number,
        interval_unit: builtins.str,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule(
            interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putRetainRule", [value]))

    @jsii.member(jsii_name="resetCmkArn")
    def reset_cmk_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmkArn", []))

    @jsii.member(jsii_name="resetCopyTags")
    def reset_copy_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTags", []))

    @jsii.member(jsii_name="resetDeprecateRule")
    def reset_deprecate_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprecateRule", []))

    @jsii.member(jsii_name="resetRetainRule")
    def reset_retain_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainRule", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetTargetRegion")
    def reset_target_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="deprecateRule")
    def deprecate_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference, jsii.get(self, "deprecateRule"))

    @builtins.property
    @jsii.member(jsii_name="retainRule")
    def retain_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference", jsii.get(self, "retainRule"))

    @builtins.property
    @jsii.member(jsii_name="cmkArnInput")
    def cmk_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cmkArnInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTagsInput")
    def copy_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="deprecateRuleInput")
    def deprecate_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule], jsii.get(self, "deprecateRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedInput")
    def encrypted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="retainRuleInput")
    def retain_rule_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule"], jsii.get(self, "retainRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRegionInput")
    def target_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="cmkArn")
    def cmk_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cmkArn"))

    @cmk_arn.setter
    def cmk_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49bbb4ea58ade975a027e6f9159e6577775c2f88d10a2af8f15e7a06384a2e64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmkArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyTags")
    def copy_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTags"))

    @copy_tags.setter
    def copy_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfc8a75b2fd7414a3b9ca611a73ea39e4e714b7bd0c69b66860603b98a63c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ee1550815b5b0a997cc7ba6c81ebb72643391c293bef3fcbe5edc28860d19c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faae971fced1d095e8ce70e119507a4b5d32ed6f21d988607a1ff40533c79e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRegion")
    def target_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRegion"))

    @target_region.setter
    def target_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16a2e012c26c692a388091898995399bbaafd0c6bc71dd7d16bb93284360fbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f483f19c68acaa74bb3b8fe37606be140a71818fcb9e7110634a0edcd295de49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
)
class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule:
    def __init__(self, *, interval: jsii.Number, interval_unit: builtins.str) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b147090f2f5eca7d6cf20b1a8effaf05174d2d40008a04242a277707d2a5c3bd)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "interval_unit": interval_unit,
        }

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        assert result is not None, "Required property 'interval_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82b49c31bab633a8ac16bda6aad1923bc3f98b6d9f1147b08c901b836d633d4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d634beb3335264efd3eb0f6381bdb50701f920bf116a2eac329855057bf20479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f898032e22d1528e225b91518acdf0ea0ab67c0ec5de61325bec697238660d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f09d8f7b6c168277797f4e609b000475e54564aa8a97fd81ffb5fd713b15891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "interval": "interval",
        "interval_unit": "intervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85aabba8090b710237f91635ce85109ade2ada20b796663cafe29e8f6244e60)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea6a160af879c12af9d1088f95278885af6577f8834c07bc2cc25a6c0a0925fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30483f4a4c2fd6e6f690209ccdcec2ec1e98ce74ce4ca526c31d6929aaee8009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d26f8652243dc7a980078d0c3acc3f8bc0f5e453875ac6cf599c7e63a3a3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31f7f77ab272b7a45a134f424fbf9edc45f898fbb490eff693b78bf6fc309f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3258278ffad7d3d1a8f906998c7832f80e0880a0cbd9931513111e6ca5a19af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "count": "count",
        "interval": "interval",
        "interval_unit": "intervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule:
    def __init__(
        self,
        *,
        availability_zones: typing.Sequence[builtins.str],
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#availability_zones DlmLifecyclePolicy#availability_zones}.
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8987489509f9b881bc6e17c03af53022403d7d318fd1eb21e721bc37435ca3)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zones": availability_zones,
        }
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit

    @builtins.property
    def availability_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#availability_zones DlmLifecyclePolicy#availability_zones}.'''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ef418e4a5248f216bb40f5553b07e362ca3883a63f3b156b8c240a7504fdbf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityZonesInput")
    def availability_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b7f8f95ce86692ce2248381b618854f3f30833ebdeabad39c820400fb1d42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc0f73d55b81c7fd9528b1ab31e1f14462959e60d1b589ceb969728d57c70c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee641b432770b69faf3ead223ad95b0afb148ff38e93797cae3cff8a6532793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfb562254f1f451773ab79a3331e0f1a81aa4d8baa1541cedbb6d204a2e3b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470a6059d7a8f692259b3489e1a93aecf62f36b5a2ff3b9ad033c4d70b375253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8363f5a2f861c83ad2955fd7d31e348b907bb7c95dbb50c651880da5642ac1cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3ed0084d76f99548130b9a23e235c7aabf7cd14197962cb9eec35b43be60cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56dd18dffc78c9f4fe44b847e58fd7fcb6a45665e816be0fa89ed4472890a6d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f355c292a25711a28a496861735ddd347f138cf5969403e84cfdee34be3654e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5815e0fb1d5f4fd3fdb4db03b7405fb1dfbbc42cb6d0a2aba2be0c7a26e031f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f27c79acea7e383fa1270b3eed8db5239481ea8fcaf520db74b20cdd830f733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DlmLifecyclePolicyPolicyDetailsScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cd2ed3a21d19559fb0725c830674cfea111052a964919a1fba31984513ccec6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putArchiveRule")
    def put_archive_rule(
        self,
        *,
        archive_retain_rule: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param archive_retain_rule: archive_retain_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#archive_retain_rule DlmLifecyclePolicy#archive_retain_rule}
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule(
            archive_retain_rule=archive_retain_rule
        )

        return typing.cast(None, jsii.invoke(self, "putArchiveRule", [value]))

    @jsii.member(jsii_name="putCreateRule")
    def put_create_rule(
        self,
        *,
        cron_expression: typing.Optional[builtins.str] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        scripts: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts, typing.Dict[builtins.str, typing.Any]]] = None,
        times: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#cron_expression DlmLifecyclePolicy#cron_expression}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#location DlmLifecyclePolicy#location}.
        :param scripts: scripts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#scripts DlmLifecyclePolicy#scripts}
        :param times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#times DlmLifecyclePolicy#times}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleCreateRule(
            cron_expression=cron_expression,
            interval=interval,
            interval_unit=interval_unit,
            location=location,
            scripts=scripts,
            times=times,
        )

        return typing.cast(None, jsii.invoke(self, "putCreateRule", [value]))

    @jsii.member(jsii_name="putCrossRegionCopyRule")
    def put_cross_region_copy_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a797d1b5625123ab00c72be84eec66947692d8f967917605c170d36139d07f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCrossRegionCopyRule", [value]))

    @jsii.member(jsii_name="putDeprecateRule")
    def put_deprecate_rule(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule(
            count=count, interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putDeprecateRule", [value]))

    @jsii.member(jsii_name="putFastRestoreRule")
    def put_fast_restore_rule(
        self,
        *,
        availability_zones: typing.Sequence[builtins.str],
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#availability_zones DlmLifecyclePolicy#availability_zones}.
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule(
            availability_zones=availability_zones,
            count=count,
            interval=interval,
            interval_unit=interval_unit,
        )

        return typing.cast(None, jsii.invoke(self, "putFastRestoreRule", [value]))

    @jsii.member(jsii_name="putRetainRule")
    def put_retain_rule(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleRetainRule(
            count=count, interval=interval, interval_unit=interval_unit
        )

        return typing.cast(None, jsii.invoke(self, "putRetainRule", [value]))

    @jsii.member(jsii_name="putShareRule")
    def put_share_rule(
        self,
        *,
        target_accounts: typing.Sequence[builtins.str],
        unshare_interval: typing.Optional[jsii.Number] = None,
        unshare_interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_accounts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target_accounts DlmLifecyclePolicy#target_accounts}.
        :param unshare_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#unshare_interval DlmLifecyclePolicy#unshare_interval}.
        :param unshare_interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#unshare_interval_unit DlmLifecyclePolicy#unshare_interval_unit}.
        '''
        value = DlmLifecyclePolicyPolicyDetailsScheduleShareRule(
            target_accounts=target_accounts,
            unshare_interval=unshare_interval,
            unshare_interval_unit=unshare_interval_unit,
        )

        return typing.cast(None, jsii.invoke(self, "putShareRule", [value]))

    @jsii.member(jsii_name="resetArchiveRule")
    def reset_archive_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveRule", []))

    @jsii.member(jsii_name="resetCopyTags")
    def reset_copy_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTags", []))

    @jsii.member(jsii_name="resetCrossRegionCopyRule")
    def reset_cross_region_copy_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRegionCopyRule", []))

    @jsii.member(jsii_name="resetDeprecateRule")
    def reset_deprecate_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprecateRule", []))

    @jsii.member(jsii_name="resetFastRestoreRule")
    def reset_fast_restore_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFastRestoreRule", []))

    @jsii.member(jsii_name="resetShareRule")
    def reset_share_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareRule", []))

    @jsii.member(jsii_name="resetTagsToAdd")
    def reset_tags_to_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsToAdd", []))

    @jsii.member(jsii_name="resetVariableTags")
    def reset_variable_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariableTags", []))

    @builtins.property
    @jsii.member(jsii_name="archiveRule")
    def archive_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference, jsii.get(self, "archiveRule"))

    @builtins.property
    @jsii.member(jsii_name="createRule")
    def create_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference, jsii.get(self, "createRule"))

    @builtins.property
    @jsii.member(jsii_name="crossRegionCopyRule")
    def cross_region_copy_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList, jsii.get(self, "crossRegionCopyRule"))

    @builtins.property
    @jsii.member(jsii_name="deprecateRule")
    def deprecate_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference, jsii.get(self, "deprecateRule"))

    @builtins.property
    @jsii.member(jsii_name="fastRestoreRule")
    def fast_restore_rule(
        self,
    ) -> DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference:
        return typing.cast(DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference, jsii.get(self, "fastRestoreRule"))

    @builtins.property
    @jsii.member(jsii_name="retainRule")
    def retain_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference", jsii.get(self, "retainRule"))

    @builtins.property
    @jsii.member(jsii_name="shareRule")
    def share_rule(
        self,
    ) -> "DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference":
        return typing.cast("DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference", jsii.get(self, "shareRule"))

    @builtins.property
    @jsii.member(jsii_name="archiveRuleInput")
    def archive_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule], jsii.get(self, "archiveRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTagsInput")
    def copy_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="createRuleInput")
    def create_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule], jsii.get(self, "createRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRegionCopyRuleInput")
    def cross_region_copy_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]], jsii.get(self, "crossRegionCopyRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="deprecateRuleInput")
    def deprecate_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule], jsii.get(self, "deprecateRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="fastRestoreRuleInput")
    def fast_restore_rule_input(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule], jsii.get(self, "fastRestoreRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="retainRuleInput")
    def retain_rule_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleRetainRule"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleRetainRule"], jsii.get(self, "retainRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="shareRuleInput")
    def share_rule_input(
        self,
    ) -> typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleShareRule"]:
        return typing.cast(typing.Optional["DlmLifecyclePolicyPolicyDetailsScheduleShareRule"], jsii.get(self, "shareRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsToAddInput")
    def tags_to_add_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsToAddInput"))

    @builtins.property
    @jsii.member(jsii_name="variableTagsInput")
    def variable_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variableTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTags")
    def copy_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTags"))

    @copy_tags.setter
    def copy_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa4ba56138b269ff257540c007f6a8b5a77df6f65c3737d95b6940a142721d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__418a8e8be83c846edadc1273f79bccc860dfcdafe35e6e40308f153d84c35ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsToAdd")
    def tags_to_add(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsToAdd"))

    @tags_to_add.setter
    def tags_to_add(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce1ba84d32cb8db28913ed49314d61f44716de9de275446588fd0abf418834f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsToAdd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variableTags")
    def variable_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "variableTags"))

    @variable_tags.setter
    def variable_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b8b174e66ed13f9282a87e9fe503afc74ac552676b33b78c2d21fecd9181d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variableTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19d402814f496dde9abaef58fbaf199cd162de6c1ddac2298ae339d404f3f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleRetainRule",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "interval": "interval",
        "interval_unit": "intervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleRetainRule:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[jsii.Number] = None,
        interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.
        :param interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23bb58b1099de4d20b36167b8518b6312a5dd3d905413b00b6f0afd581501cf6)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument interval_unit", value=interval_unit, expected_type=type_hints["interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval is not None:
            self._values["interval"] = interval
        if interval_unit is not None:
            self._values["interval_unit"] = interval_unit

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#count DlmLifecyclePolicy#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval DlmLifecyclePolicy#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#interval_unit DlmLifecyclePolicy#interval_unit}.'''
        result = self._values.get("interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleRetainRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5079c52f739659d238bd48e235f880c5d63174827989a772f666f6303b6afc4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetIntervalUnit")
    def reset_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalUnitInput")
    def interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa53ed3b68ffd26a820c89e81ead36e2555f80cf74af0a814b9fc55c005aeba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec19db5dc5b640b75e4476f65dfb6a4cfe5925fc54019e6e4f12e5f20b86cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalUnit")
    def interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intervalUnit"))

    @interval_unit.setter
    def interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f228fa5c3119b42574a89dd807bb82062406297735259f9bfafb76646f417ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ed3394ff55b905b89c3863bffa176107a592bb9a9eb81b26a8ae973a7bdc3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleShareRule",
    jsii_struct_bases=[],
    name_mapping={
        "target_accounts": "targetAccounts",
        "unshare_interval": "unshareInterval",
        "unshare_interval_unit": "unshareIntervalUnit",
    },
)
class DlmLifecyclePolicyPolicyDetailsScheduleShareRule:
    def __init__(
        self,
        *,
        target_accounts: typing.Sequence[builtins.str],
        unshare_interval: typing.Optional[jsii.Number] = None,
        unshare_interval_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_accounts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target_accounts DlmLifecyclePolicy#target_accounts}.
        :param unshare_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#unshare_interval DlmLifecyclePolicy#unshare_interval}.
        :param unshare_interval_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#unshare_interval_unit DlmLifecyclePolicy#unshare_interval_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5e97ddaa87974f7e53c47f77e9bdad0f392ce052257539b013b6dc77a8d146)
            check_type(argname="argument target_accounts", value=target_accounts, expected_type=type_hints["target_accounts"])
            check_type(argname="argument unshare_interval", value=unshare_interval, expected_type=type_hints["unshare_interval"])
            check_type(argname="argument unshare_interval_unit", value=unshare_interval_unit, expected_type=type_hints["unshare_interval_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_accounts": target_accounts,
        }
        if unshare_interval is not None:
            self._values["unshare_interval"] = unshare_interval
        if unshare_interval_unit is not None:
            self._values["unshare_interval_unit"] = unshare_interval_unit

    @builtins.property
    def target_accounts(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#target_accounts DlmLifecyclePolicy#target_accounts}.'''
        result = self._values.get("target_accounts")
        assert result is not None, "Required property 'target_accounts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def unshare_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#unshare_interval DlmLifecyclePolicy#unshare_interval}.'''
        result = self._values.get("unshare_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unshare_interval_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/dlm_lifecycle_policy#unshare_interval_unit DlmLifecyclePolicy#unshare_interval_unit}.'''
        result = self._values.get("unshare_interval_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DlmLifecyclePolicyPolicyDetailsScheduleShareRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dlmLifecyclePolicy.DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa610fcf4adb65e6683a922e50ab955fcec644355b27129dd71c2f49e33a3421)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUnshareInterval")
    def reset_unshare_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnshareInterval", []))

    @jsii.member(jsii_name="resetUnshareIntervalUnit")
    def reset_unshare_interval_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnshareIntervalUnit", []))

    @builtins.property
    @jsii.member(jsii_name="targetAccountsInput")
    def target_accounts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetAccountsInput"))

    @builtins.property
    @jsii.member(jsii_name="unshareIntervalInput")
    def unshare_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unshareIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="unshareIntervalUnitInput")
    def unshare_interval_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unshareIntervalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="targetAccounts")
    def target_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetAccounts"))

    @target_accounts.setter
    def target_accounts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006fbd16cfc4938ea1e69df4f269ca2c48c9115c5eb9e06d2e30c93c3c1c9718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetAccounts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unshareInterval")
    def unshare_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unshareInterval"))

    @unshare_interval.setter
    def unshare_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4263234ce4789b44f6a7663e8ac799a286dac9cdf72bafa851062f6d640b9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unshareInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unshareIntervalUnit")
    def unshare_interval_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unshareIntervalUnit"))

    @unshare_interval_unit.setter
    def unshare_interval_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8c24ac53beea358545cdfe6680988203ec5fc2a1ea81096a966c71f0355be8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unshareIntervalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleShareRule]:
        return typing.cast(typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleShareRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleShareRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2685cab8127bc3318c619ef43d87ae3c7982512ec9cd818d1dceb581ddf4fbb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DlmLifecyclePolicy",
    "DlmLifecyclePolicyConfig",
    "DlmLifecyclePolicyPolicyDetails",
    "DlmLifecyclePolicyPolicyDetailsAction",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfigurationOutputReference",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyList",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyOutputReference",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule",
    "DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsActionOutputReference",
    "DlmLifecyclePolicyPolicyDetailsEventSource",
    "DlmLifecyclePolicyPolicyDetailsEventSourceOutputReference",
    "DlmLifecyclePolicyPolicyDetailsEventSourceParameters",
    "DlmLifecyclePolicyPolicyDetailsEventSourceParametersOutputReference",
    "DlmLifecyclePolicyPolicyDetailsExclusions",
    "DlmLifecyclePolicyPolicyDetailsExclusionsOutputReference",
    "DlmLifecyclePolicyPolicyDetailsOutputReference",
    "DlmLifecyclePolicyPolicyDetailsParameters",
    "DlmLifecyclePolicyPolicyDetailsParametersOutputReference",
    "DlmLifecyclePolicyPolicyDetailsSchedule",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTierOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCreateRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts",
    "DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScriptsOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleList",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleList",
    "DlmLifecyclePolicyPolicyDetailsScheduleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleRetainRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleRetainRuleOutputReference",
    "DlmLifecyclePolicyPolicyDetailsScheduleShareRule",
    "DlmLifecyclePolicyPolicyDetailsScheduleShareRuleOutputReference",
]

publication.publish()

def _typecheckingstub__7fbe156837bcecb09c52e230c31e44e5177ca8a14e81e40acf163c4c73e6a268(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: builtins.str,
    execution_role_arn: builtins.str,
    policy_details: typing.Union[DlmLifecyclePolicyPolicyDetails, typing.Dict[builtins.str, typing.Any]],
    default_policy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b3ddbfcdc4c93323295b5cbc301f0a29527d1c58cece393f95c8c1d3f661fbfe(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de24a90124610e3e0c2a0aaa3aa601f62c715198ebac8f45498c39dc2d3f112a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3849a4beaf2de11f89d2b1a74f1ff5ff8895ef4fba8aa202a90f25385e3bd8f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d99eca60ef7e61c225e5c8d28bd54588e7ec40abeb2c684c227edb383a7ac6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e4f88d1c7a361267c8834cf0fe69d359f0fb66f0b8fb32840e6043a2bbfcb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ef15727cd06fad1072c0e392d17ae9840f2b67509c2c5c7832a7e5f0c0bf8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244ba13b61b431b4cba1c05acbfae9b37925bc4c7cd2e44b5b736e6779479a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6785abdb647e2b69033b1bebe89234a2b0f1f2f31315bb5dc705edc848cbc2e0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b0c2eff3520097ae97b9488a5fdfdc93f372cd1977316841ba9cfc6a1c8b6c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dda0c7b3666c9c69624b0c7130cc0fa2ababc41631b0cbf85be40de766ea8a6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    execution_role_arn: builtins.str,
    policy_details: typing.Union[DlmLifecyclePolicyPolicyDetails, typing.Dict[builtins.str, typing.Any]],
    default_policy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98f504d834e3e13eac910a982cc05b656c2435ccbc1970b89affef5bce57932(
    *,
    action: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsAction, typing.Dict[builtins.str, typing.Any]]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_interval: typing.Optional[jsii.Number] = None,
    event_source: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsEventSource, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusions: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsExclusions, typing.Dict[builtins.str, typing.Any]]] = None,
    extend_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    parameters: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_language: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
    resource_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    retain_interval: typing.Optional[jsii.Number] = None,
    schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsSchedule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26890b6671d92d7545572f5b301e0d1969c65150415651162857a73ae3e275d0(
    *,
    cross_region_copy: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b963efc6b9ad0f27f2794f5e99c7ae8336f0113f44ba1f6d40587aa76e21d17d(
    *,
    encryption_configuration: typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]],
    target: builtins.str,
    retain_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7bf1f3bd21089904639984d3d181b0b20299ddb51dbd2da3599ff99768d49f(
    *,
    cmk_arn: typing.Optional[builtins.str] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc23dca30a5f9cb16b076d9d8667c5c97a3b3865c2918b1247f91b0bc016dc3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b45bb6db4981f82a2c2927d10166807789fae53861df11b49275e019bfe1b95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00b0e66d58af39dca8534f56ab7a1c415df72a783f902a18b477c177224ed40(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d4f72a7d4d1dd6e5eed31e105635cf774b0432a45ff880a7b2f59d12f8ddd4(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7de461397832524009602bdfae48d680a239694c5bf3fe32d1f3db6494b7347(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2209cad54d74cdeb10c20ea140a56fea1a227714fab88ddf8ecd7b0417fd12d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b04287af0acb8f80e95ed13ffba6729e8cd586fc2475278448af6cfd0bb680(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b53e5052284ed1f5c5d5a1529edb23310b47ffabdacca4c0bc6655a55fb5096(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c95a8218e04cb252fa51021bd06ca196a161b370bef0bf9b68565497e69534(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c7e327786014f7e45625eb3070dc83bb48d7bf2fa7c59cf1213ab8c2b26073(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76ceb7053e7c5c7c7f04b77a529945db768407271ebfe403ad63d8556e9142f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78782477551083e8842f4a33b568120cb933f078abf88eafe7439ec8bf79e49d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcafa8a4edcf0a4a2341a668c10db21364c20ce833b9cfc8f3fc781c36c171b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d60ced79f5e22dc19d5e35e55067572fcecb6397075f459098ab8d4a727c720(
    *,
    interval: jsii.Number,
    interval_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b3367f5d01890fcad8436622732197536b5db9bf3791b336d6d52862822f2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed072c4052f99af68d437890a92156f20d9d3677ba3cf1043687e7f0b0cd645(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cbfc36a90ffd254744e300809680e9205ab876496d16182eecaeee8d7c1a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bad5c023c5b5edc0ca3ac47470992869b03148f73acc867133a007078e74fb(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopyRetainRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67cdcbe83b908fb433b26a1d68d3ab52ec0bdc45e083a73d66464de309c32de8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30719f4cf780a3539bc4da6a998348a82b4e78becdbc0efa495132991a9456bf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsActionCrossRegionCopy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812a373ee7ea3d510f80985457194da0df12d1316ae862195f3281ceb5fd3361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef992c8203835d101962752c452ad7a92a3c2cfb1dc9490b803de1c93a0432cc(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83847bf8d87df1a522c3fcf21644a5fe08508ff075379c2f90696e5f55b84fa(
    *,
    parameters: typing.Union[DlmLifecyclePolicyPolicyDetailsEventSourceParameters, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e62b0d7c4312057b60331de0691ec6cac1ea0e09b0d37f5b95ca012b546727c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d85a1cfbba3e5e4654f34035e175ef8994ebb173b1d3f146935d21e948b98b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e33fb95c56cb587ebbde33599a19475319f73c107da4d57a823128855eec833(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b34c057aec859d97ae058fcf0b43befaf4b2d85f43298be44c69aeb6a67788e(
    *,
    description_regex: builtins.str,
    event_type: builtins.str,
    snapshot_owner: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd62e334f723a921d5d55001f8221f1fa7683812d3ec6b2e389f7d2d091e83cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e804d50f198597b96b16d3f3cbcb2dca9428a18d92bdec4aae9e0f054938147a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4440ff741fc67981bb771f49323a8172237398cbc718df39ed43197c151974d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3bc941413402d7a7eaff616be908314eb85d63c8e9ef2da1b1cdc3f0bb89b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e3467b8e0ea7f7d6cbd3442c309f3fea7838854a23ca5b718ef52c0f4ef592(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsEventSourceParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6188c4d66ecb1310b7be3567ace24f9a3d4f15e0f1e0cd7745fac4d2c9a2b74f(
    *,
    exclude_boot_volumes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    exclude_volume_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230bcade77a41b989f5c9dfd19ef730d6b3c6623fb87bc5164f3da9bb13d54d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f5b471eb848b6d23628a7587ac03d96621747fa951f918b5d1fb043b0436f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad12df39b8795cdee3b5cd250cfe848a5307c8107019577f9c6aaa9867026647(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f659c9c90f6b29823582b0150b3028a2fe141f172899a48d0f39ef1ae773287(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e5e7895019dd941c0ece77497b57945d552620f3db64776d279cb2fcc75067(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsExclusions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c847fc5dd9ba2a22a44e7efcb3dcd18b34992c503746b199957f505608d2140d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af32f46a0a0640385c6a433dd75fdca1bb9c4fce9f3da41b6845036bcf639bc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7522efbdd96f1e589045221191d0f4555aec26c723c961541cead6d3fdb06f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a05d6c5885e15a3c7a09df7edefb363eb00e24b12e0274d0975570653d4c031(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f6a0e869d858f2d87b9a54a004276bdd1cf6acfbe1f37cdadb8186d5b2dd50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57a37b003fe4cf9da0705b5dae2eee6630bd38d081adc89f0545e72d341da0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c073121b9a06cde840aea522af4b6c8ba947c51a35e5271da4e6209b014991(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a371da97eec332d4846ff5eb0b3aa412bb41c5ead25980d285fe7f6268d236(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa511b7b46db524f48795bccd1cd6e7e5f68cab79eca1559c95a17c9d2de331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeca2438878be6f2620d641f54e1fb82d4ac8e168e42adc3a194da951ae2d5a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edba55eb00cf93373dcafa3d77cc963192a909fcb981f4db5c6726dccad93689(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3c3e4c06ac550f34035f5fd0b30322a2c424441212747327893e7322055b43(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbf2a47e2aeb2533733f1b5a53e3dc41b2dc5c8e5d3ce495ff063d158031e07(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b38768870d44ac053c7f97df700cbfd05081b7c1077f1b9b8dbd7bf4bb5e6ea(
    *,
    exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_reboot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ebd01bf0d5519fc4cec1a5f14eb08e1bef1217cb58df9b2911475accafc18e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adff67b011888fecbdf8ecb7755dd830083a2fee840ad3f562efcff9cc010355(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9afed822890caea61b017d38c1793cbd0a61f9923adf82693f88dc9208c3bd8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6efa990e98c2e546db129083dfcaf6bd97d33d572cd4a0b89aa42b65054d83(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2a8090c5d82e4e0885339a185710eaa19cdcecd03b0f8bba8af6c969fce5c4(
    *,
    create_rule: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    retain_rule: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule, typing.Dict[builtins.str, typing.Any]],
    archive_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule, typing.Dict[builtins.str, typing.Any]]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cross_region_copy_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deprecate_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule, typing.Dict[builtins.str, typing.Any]]] = None,
    fast_restore_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule, typing.Dict[builtins.str, typing.Any]]] = None,
    share_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleShareRule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags_to_add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variable_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f24cbff243e7d7b082a095c14f7a02d27465ed4871d7068ab32f86520bdc75(
    *,
    archive_retain_rule: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b837c9324b04e029e4cfda0be85001922816a6d1d7d5c613fa531f22d37343a9(
    *,
    retention_archive_tier: typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cbf2bfedcb40e9af12f900b69eef7c5c763b3830e7315d382c1f1b65a4eba9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ab78402ba8b41c3231debc9252faa2819b2cb724b36f9494acef48ed36dae4(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920f250c863be29c548545898b0014ad4aead27a33c72585866bf6e33c31b69f(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33545afb6262d5b464b73579371e981d085ca27f84dd744d16955de130fd9cce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa54e20516757dee23a5cfa25b18667c0382e92c299720cc5be71894849d6c99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64274b9cca7b9696d1e10afa9b82d632558fe7d97b12736f03836d250b94e7f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4858ef838e55aea3f8c9c20ae192cbd141beea5a02f11d473db6af9bd77c0ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00774205dfb61276a3525af657ec752f950a594aed16ec97f0ba86fff199016(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRuleArchiveRetainRuleRetentionArchiveTier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8e46da36a9c64fe6dfdfa3ed9833982177da33a31dbd9ab3cc4ed441e8f75a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e6119de975dfe0e1555a2f7b315b8a651c6dc6ee7e535be40b47d38bf8691d(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleArchiveRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c77d5cb3d264940bf656d1f240c79411aad70a46c630bcd8a94dbbb68c5d13(
    *,
    cron_expression: typing.Optional[builtins.str] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    scripts: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts, typing.Dict[builtins.str, typing.Any]]] = None,
    times: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3b2a63d8e8fc153571a39c7348449ccdf9d372ce34ff31cdc24fbdea3cd927(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb3677ea81fe6b1fc93b721cc23f9c09a1af172dd05c00b9822b9d507577a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e62dda270ae41c51b0bfb85284616f39debb1f91b2c2a488f943d4b64f4bd0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7825b54efff488f9b47ab6066724696ad81965f512a809effdbd0f2e800d1b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc3cb09f5a8bb422b45c938a8d168071505cb067a4104769ed182e878a72377(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0757a47f22113dda5a5525b901c353b4d1caf03fa9988f07168aa94fc4447dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70a019a87b668f6b73b9547fd6fbed5c5176e2d00f3ddab8fa1640e743c2081(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be160b3b90a1b9818c261381285218586b218aa0fd48271161defa2dd04a62ac(
    *,
    execution_handler: builtins.str,
    execute_operation_on_script_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    execution_handler_service: typing.Optional[builtins.str] = None,
    execution_timeout: typing.Optional[jsii.Number] = None,
    maximum_retry_count: typing.Optional[jsii.Number] = None,
    stages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f513ba34bf1ce0d9a5390e660df293a249bf1efa44af499ed12b74546c78bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae528c62bb4306839eacc3ecfdbb7c89fd71e8c88358e907372341551f6becf8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad36fc50a8acd42e1f78b0006796e0e9b55624a281b681a3e90fba8191e18ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef9a785904a86de44ded125359c204ba078545878fd5d9959d67512f96fbb20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab3cf9dc33cc38d6d71ee6356bb018ba331b41eb565720b269820057be809ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2f40e31db58e9d9ed5cb5689be063033f1a746f80625e63dd34fdfd810b9af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8b3de6999b06624c87820e4ca9a9c1194a682d85562d6f9885fbbef01eba50(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1411213ae5ac0f54dcd3abb9df0b8fbc879aea7d675c10747a49dfd9c73f2f4(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCreateRuleScripts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2862e2fe9889b8004d4ac4a41843c4082162ab35a06ed075943b670747ed12(
    *,
    encrypted: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    cmk_arn: typing.Optional[builtins.str] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deprecate_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule, typing.Dict[builtins.str, typing.Any]]] = None,
    retain_rule: typing.Optional[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[builtins.str] = None,
    target_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045732adf3e07d8ff890172ebe09a0501d6890984ca8087227c0d598dfb9bfc9(
    *,
    interval: jsii.Number,
    interval_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb1bcf005c6f60eb1f77d70a4497d39b04280b92bc15abc5c42121ce3e27e7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6505577fc0ebf04bcdbf021c66cd2d91468175866c50e90c2fffc6a3c125796b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f160771898724a50382b352409920df1ca8a5451cab638dc5158f36bc0d297c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cba936299741674e2ccc97bf000674222466b7a8c9644db318a1e044492d75d(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleDeprecateRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e561fb47925aa0ff6132d436b2e64b464dbc8c6682d11c17ef85e998b282d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8018b297c7718073c3e0753e4f50c4449a9247a082594ab377694db834de4e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9870ff33a67d028aae6730cbb9a74d753385b156eb31312559e14fc15c66566a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a671f4ec8cf20e741c3f11e06de9fadfeb973a20e7643a51842a11ea41fb62cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda6c5458891e77735f9d7dbde6bbfef12fa50cbf54e2630f39d811727c76a71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca6560e1cdba675794de008046e01816dbffe706adae03c828b2a698cb33f2e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977027d87620a12d7ca655da01a23b8144ee43e1cf9baca6ccd48cd1d7724565(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bbb4ea58ade975a027e6f9159e6577775c2f88d10a2af8f15e7a06384a2e64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfc8a75b2fd7414a3b9ca611a73ea39e4e714b7bd0c69b66860603b98a63c78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ee1550815b5b0a997cc7ba6c81ebb72643391c293bef3fcbe5edc28860d19c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faae971fced1d095e8ce70e119507a4b5d32ed6f21d988607a1ff40533c79e90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16a2e012c26c692a388091898995399bbaafd0c6bc71dd7d16bb93284360fbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f483f19c68acaa74bb3b8fe37606be140a71818fcb9e7110634a0edcd295de49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b147090f2f5eca7d6cf20b1a8effaf05174d2d40008a04242a277707d2a5c3bd(
    *,
    interval: jsii.Number,
    interval_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b49c31bab633a8ac16bda6aad1923bc3f98b6d9f1147b08c901b836d633d4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d634beb3335264efd3eb0f6381bdb50701f920bf116a2eac329855057bf20479(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f898032e22d1528e225b91518acdf0ea0ab67c0ec5de61325bec697238660d28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f09d8f7b6c168277797f4e609b000475e54564aa8a97fd81ffb5fd713b15891(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRuleRetainRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85aabba8090b710237f91635ce85109ade2ada20b796663cafe29e8f6244e60(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6a160af879c12af9d1088f95278885af6577f8834c07bc2cc25a6c0a0925fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30483f4a4c2fd6e6f690209ccdcec2ec1e98ce74ce4ca526c31d6929aaee8009(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d26f8652243dc7a980078d0c3acc3f8bc0f5e453875ac6cf599c7e63a3a3be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31f7f77ab272b7a45a134f424fbf9edc45f898fbb490eff693b78bf6fc309f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3258278ffad7d3d1a8f906998c7832f80e0880a0cbd9931513111e6ca5a19af7(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleDeprecateRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8987489509f9b881bc6e17c03af53022403d7d318fd1eb21e721bc37435ca3(
    *,
    availability_zones: typing.Sequence[builtins.str],
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef418e4a5248f216bb40f5553b07e362ca3883a63f3b156b8c240a7504fdbf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b7f8f95ce86692ce2248381b618854f3f30833ebdeabad39c820400fb1d42a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc0f73d55b81c7fd9528b1ab31e1f14462959e60d1b589ceb969728d57c70c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee641b432770b69faf3ead223ad95b0afb148ff38e93797cae3cff8a6532793(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfb562254f1f451773ab79a3331e0f1a81aa4d8baa1541cedbb6d204a2e3b42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470a6059d7a8f692259b3489e1a93aecf62f36b5a2ff3b9ad033c4d70b375253(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleFastRestoreRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8363f5a2f861c83ad2955fd7d31e348b907bb7c95dbb50c651880da5642ac1cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3ed0084d76f99548130b9a23e235c7aabf7cd14197962cb9eec35b43be60cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dd18dffc78c9f4fe44b847e58fd7fcb6a45665e816be0fa89ed4472890a6d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f355c292a25711a28a496861735ddd347f138cf5969403e84cfdee34be3654e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5815e0fb1d5f4fd3fdb4db03b7405fb1dfbbc42cb6d0a2aba2be0c7a26e031f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f27c79acea7e383fa1270b3eed8db5239481ea8fcaf520db74b20cdd830f733(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DlmLifecyclePolicyPolicyDetailsSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd2ed3a21d19559fb0725c830674cfea111052a964919a1fba31984513ccec6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a797d1b5625123ab00c72be84eec66947692d8f967917605c170d36139d07f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DlmLifecyclePolicyPolicyDetailsScheduleCrossRegionCopyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa4ba56138b269ff257540c007f6a8b5a77df6f65c3737d95b6940a142721d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418a8e8be83c846edadc1273f79bccc860dfcdafe35e6e40308f153d84c35ebe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce1ba84d32cb8db28913ed49314d61f44716de9de275446588fd0abf418834f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b8b174e66ed13f9282a87e9fe503afc74ac552676b33b78c2d21fecd9181d6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19d402814f496dde9abaef58fbaf199cd162de6c1ddac2298ae339d404f3f94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DlmLifecyclePolicyPolicyDetailsSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23bb58b1099de4d20b36167b8518b6312a5dd3d905413b00b6f0afd581501cf6(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[jsii.Number] = None,
    interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5079c52f739659d238bd48e235f880c5d63174827989a772f666f6303b6afc4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa53ed3b68ffd26a820c89e81ead36e2555f80cf74af0a814b9fc55c005aeba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec19db5dc5b640b75e4476f65dfb6a4cfe5925fc54019e6e4f12e5f20b86cb2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f228fa5c3119b42574a89dd807bb82062406297735259f9bfafb76646f417ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ed3394ff55b905b89c3863bffa176107a592bb9a9eb81b26a8ae973a7bdc3f(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleRetainRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5e97ddaa87974f7e53c47f77e9bdad0f392ce052257539b013b6dc77a8d146(
    *,
    target_accounts: typing.Sequence[builtins.str],
    unshare_interval: typing.Optional[jsii.Number] = None,
    unshare_interval_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa610fcf4adb65e6683a922e50ab955fcec644355b27129dd71c2f49e33a3421(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006fbd16cfc4938ea1e69df4f269ca2c48c9115c5eb9e06d2e30c93c3c1c9718(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4263234ce4789b44f6a7663e8ac799a286dac9cdf72bafa851062f6d640b9af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8c24ac53beea358545cdfe6680988203ec5fc2a1ea81096a966c71f0355be8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2685cab8127bc3318c619ef43d87ae3c7982512ec9cd818d1dceb581ddf4fbb8(
    value: typing.Optional[DlmLifecyclePolicyPolicyDetailsScheduleShareRule],
) -> None:
    """Type checking stubs"""
    pass
