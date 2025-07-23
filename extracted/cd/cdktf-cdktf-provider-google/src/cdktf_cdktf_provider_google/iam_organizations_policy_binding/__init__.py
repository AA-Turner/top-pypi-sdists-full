r'''
# `google_iam_organizations_policy_binding`

Refer to the Terraform Registry for docs: [`google_iam_organizations_policy_binding`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding).
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


class IamOrganizationsPolicyBinding(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamOrganizationsPolicyBinding.IamOrganizationsPolicyBinding",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding google_iam_organizations_policy_binding}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        organization: builtins.str,
        policy: builtins.str,
        policy_binding_id: builtins.str,
        target: typing.Union["IamOrganizationsPolicyBindingTarget", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        condition: typing.Optional[typing.Union["IamOrganizationsPolicyBindingCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        policy_kind: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IamOrganizationsPolicyBindingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding google_iam_organizations_policy_binding} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the Policy Binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#location IamOrganizationsPolicyBinding#location}
        :param organization: The parent organization of the Policy Binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#organization IamOrganizationsPolicyBinding#organization}
        :param policy: Required. Immutable. The resource name of the policy to be bound. The binding parent and policy must belong to the same Organization (or Project). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy IamOrganizationsPolicyBinding#policy}
        :param policy_binding_id: The Policy Binding ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy_binding_id IamOrganizationsPolicyBinding#policy_binding_id}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#target IamOrganizationsPolicyBinding#target}
        :param annotations: Optional. User defined annotations. See https://google.aip.dev/148#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#annotations IamOrganizationsPolicyBinding#annotations}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#condition IamOrganizationsPolicyBinding#condition}
        :param display_name: Optional. The description of the policy binding. Must be less than or equal to 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#display_name IamOrganizationsPolicyBinding#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#id IamOrganizationsPolicyBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_kind: Immutable. The kind of the policy to attach in this binding. This field must be one of the following: - Left empty (will be automatically set to the policy kind) - The input policy kind Possible values: POLICY_KIND_UNSPECIFIED PRINCIPAL_ACCESS_BOUNDARY ACCESS Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy_kind IamOrganizationsPolicyBinding#policy_kind}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#timeouts IamOrganizationsPolicyBinding#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e572344225ae7ec01add3be54180a57feededcc23f6a2595091ddb7a8ab54745)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IamOrganizationsPolicyBindingConfig(
            location=location,
            organization=organization,
            policy=policy,
            policy_binding_id=policy_binding_id,
            target=target,
            annotations=annotations,
            condition=condition,
            display_name=display_name,
            id=id,
            policy_kind=policy_kind,
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
        '''Generates CDKTF code for importing a IamOrganizationsPolicyBinding resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IamOrganizationsPolicyBinding to import.
        :param import_from_id: The id of the existing IamOrganizationsPolicyBinding that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IamOrganizationsPolicyBinding to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceaa9a82d0f0c9245db50080130172c352ff2d83e8de501a9a9110c1363dd4fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#description IamOrganizationsPolicyBinding#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#expression IamOrganizationsPolicyBinding#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#location IamOrganizationsPolicyBinding#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#title IamOrganizationsPolicyBinding#title}
        '''
        value = IamOrganizationsPolicyBindingCondition(
            description=description,
            expression=expression,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        principal_set: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param principal_set: Required. Immutable. Full Resource Name of the principal set used for principal access boundary policy bindings. Examples for each one of the following supported principal set types: - Organization '//cloudresourcemanager.googleapis.com/organizations/ORGANIZATION_ID' - Workforce Identity: '//iam.googleapis.com/locations/global/workforcePools/WORKFORCE_POOL_ID' - Workspace Identity: '//iam.googleapis.com/locations/global/workspace/WORKSPACE_ID' It must be parent by the policy binding's parent (the organization). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#principal_set IamOrganizationsPolicyBinding#principal_set}
        '''
        value = IamOrganizationsPolicyBindingTarget(principal_set=principal_set)

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#create IamOrganizationsPolicyBinding#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#delete IamOrganizationsPolicyBinding#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#update IamOrganizationsPolicyBinding#update}.
        '''
        value = IamOrganizationsPolicyBindingTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPolicyKind")
    def reset_policy_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyKind", []))

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
    @jsii.member(jsii_name="condition")
    def condition(self) -> "IamOrganizationsPolicyBindingConditionOutputReference":
        return typing.cast("IamOrganizationsPolicyBindingConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="policyUid")
    def policy_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyUid"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "IamOrganizationsPolicyBindingTargetOutputReference":
        return typing.cast("IamOrganizationsPolicyBindingTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IamOrganizationsPolicyBindingTimeoutsOutputReference":
        return typing.cast("IamOrganizationsPolicyBindingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional["IamOrganizationsPolicyBindingCondition"]:
        return typing.cast(typing.Optional["IamOrganizationsPolicyBindingCondition"], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="policyBindingIdInput")
    def policy_binding_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyBindingIdInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyKindInput")
    def policy_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyKindInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional["IamOrganizationsPolicyBindingTarget"]:
        return typing.cast(typing.Optional["IamOrganizationsPolicyBindingTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamOrganizationsPolicyBindingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IamOrganizationsPolicyBindingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9086c1204301141c7156b29c54060f4aa562a58d8d3e7fc1233cc895df5325c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb2aa08033ea89f41762dcb5bc3193c1cf756fa38057805b94511490c5c2d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fd793a68ed146061ac413ba73e6adbf35cec95a219c52c7d363d4a274ccfd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ae21cfeb3e0f2208a620d2d03c9d221e13c6bf3752d093f757c1cc65a914f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057fd82b8be5515ba87081837557318d3f882737a2a75adef1f404e3448c3d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7ac5e78f1ba8586d22d8aa868221aabb8a287204ea688d82997f802d5bf9cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyBindingId")
    def policy_binding_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyBindingId"))

    @policy_binding_id.setter
    def policy_binding_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03887c5596eb4c8d5ef204248a0198d4850a485a99c289a6ff15ed9d6e24b188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyBindingId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyKind")
    def policy_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyKind"))

    @policy_kind.setter
    def policy_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18621d52fb9af11f2dcb43fb833cebd70173c4139a6a2499271d913eb02b8990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyKind", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamOrganizationsPolicyBinding.IamOrganizationsPolicyBindingCondition",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "expression": "expression",
        "location": "location",
        "title": "title",
    },
)
class IamOrganizationsPolicyBindingCondition:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#description IamOrganizationsPolicyBinding#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#expression IamOrganizationsPolicyBinding#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#location IamOrganizationsPolicyBinding#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#title IamOrganizationsPolicyBinding#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c8b65a6306f73e93754baae83fc57da2cbffd248f1fdf0c3d2a013c7ab7721)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if expression is not None:
            self._values["expression"] = expression
        if location is not None:
            self._values["location"] = location
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#description IamOrganizationsPolicyBinding#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#expression IamOrganizationsPolicyBinding#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Optional.

        String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#location IamOrganizationsPolicyBinding#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#title IamOrganizationsPolicyBinding#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamOrganizationsPolicyBindingCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamOrganizationsPolicyBindingConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamOrganizationsPolicyBinding.IamOrganizationsPolicyBindingConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a20776774444c4eebbfc6f42acdbad605e534f91dbe9ddcaa9950b82a9d0d4c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpression")
    def reset_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpression", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53dae6a825b34d9d9074a75dda9fb6260c95afc04ff25c85254a56fad631f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0d5da0145496dbf32290f4f396d3b23a37d75eb737122164fc853c3dd04770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6cf0b3688010fe521bf88f71b42aaf782ad723fbf20c2b3fd2cdf578845f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a83b2db1b33092e29f5fd82e40d81f1e9c8733bfcdcded1b9cd0bc560eeadb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamOrganizationsPolicyBindingCondition]:
        return typing.cast(typing.Optional[IamOrganizationsPolicyBindingCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamOrganizationsPolicyBindingCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb660ab9ff3b57026da3692a906601f49ba78124d1c7e77e41eb0068c5756e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamOrganizationsPolicyBinding.IamOrganizationsPolicyBindingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "organization": "organization",
        "policy": "policy",
        "policy_binding_id": "policyBindingId",
        "target": "target",
        "annotations": "annotations",
        "condition": "condition",
        "display_name": "displayName",
        "id": "id",
        "policy_kind": "policyKind",
        "timeouts": "timeouts",
    },
)
class IamOrganizationsPolicyBindingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        organization: builtins.str,
        policy: builtins.str,
        policy_binding_id: builtins.str,
        target: typing.Union["IamOrganizationsPolicyBindingTarget", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        condition: typing.Optional[typing.Union[IamOrganizationsPolicyBindingCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        policy_kind: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["IamOrganizationsPolicyBindingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the Policy Binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#location IamOrganizationsPolicyBinding#location}
        :param organization: The parent organization of the Policy Binding. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#organization IamOrganizationsPolicyBinding#organization}
        :param policy: Required. Immutable. The resource name of the policy to be bound. The binding parent and policy must belong to the same Organization (or Project). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy IamOrganizationsPolicyBinding#policy}
        :param policy_binding_id: The Policy Binding ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy_binding_id IamOrganizationsPolicyBinding#policy_binding_id}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#target IamOrganizationsPolicyBinding#target}
        :param annotations: Optional. User defined annotations. See https://google.aip.dev/148#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#annotations IamOrganizationsPolicyBinding#annotations}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#condition IamOrganizationsPolicyBinding#condition}
        :param display_name: Optional. The description of the policy binding. Must be less than or equal to 63 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#display_name IamOrganizationsPolicyBinding#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#id IamOrganizationsPolicyBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_kind: Immutable. The kind of the policy to attach in this binding. This field must be one of the following: - Left empty (will be automatically set to the policy kind) - The input policy kind Possible values: POLICY_KIND_UNSPECIFIED PRINCIPAL_ACCESS_BOUNDARY ACCESS Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy_kind IamOrganizationsPolicyBinding#policy_kind}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#timeouts IamOrganizationsPolicyBinding#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(target, dict):
            target = IamOrganizationsPolicyBindingTarget(**target)
        if isinstance(condition, dict):
            condition = IamOrganizationsPolicyBindingCondition(**condition)
        if isinstance(timeouts, dict):
            timeouts = IamOrganizationsPolicyBindingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9707d4ac4f6bdb92180c98efba02443049ebc17b2969432006abd0dc2f2cc445)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument policy_binding_id", value=policy_binding_id, expected_type=type_hints["policy_binding_id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy_kind", value=policy_kind, expected_type=type_hints["policy_kind"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "organization": organization,
            "policy": policy,
            "policy_binding_id": policy_binding_id,
            "target": target,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if condition is not None:
            self._values["condition"] = condition
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if policy_kind is not None:
            self._values["policy_kind"] = policy_kind
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
    def location(self) -> builtins.str:
        '''The location of the Policy Binding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#location IamOrganizationsPolicyBinding#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''The parent organization of the Policy Binding.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#organization IamOrganizationsPolicyBinding#organization}
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy(self) -> builtins.str:
        '''Required.

        Immutable. The resource name of the policy to be bound. The binding parent and policy must belong to the same Organization (or Project).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy IamOrganizationsPolicyBinding#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_binding_id(self) -> builtins.str:
        '''The Policy Binding ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy_binding_id IamOrganizationsPolicyBinding#policy_binding_id}
        '''
        result = self._values.get("policy_binding_id")
        assert result is not None, "Required property 'policy_binding_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> "IamOrganizationsPolicyBindingTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#target IamOrganizationsPolicyBinding#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("IamOrganizationsPolicyBindingTarget", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. User defined annotations. See https://google.aip.dev/148#annotations for more details such as format and size limitations.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#annotations IamOrganizationsPolicyBinding#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def condition(self) -> typing.Optional[IamOrganizationsPolicyBindingCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#condition IamOrganizationsPolicyBinding#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[IamOrganizationsPolicyBindingCondition], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. The description of the policy binding. Must be less than or equal to 63 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#display_name IamOrganizationsPolicyBinding#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#id IamOrganizationsPolicyBinding#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_kind(self) -> typing.Optional[builtins.str]:
        '''Immutable.

        The kind of the policy to attach in this binding. This
        field must be one of the following:  - Left empty (will be automatically set
        to the policy kind) - The input policy kind   Possible values:  POLICY_KIND_UNSPECIFIED PRINCIPAL_ACCESS_BOUNDARY ACCESS

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#policy_kind IamOrganizationsPolicyBinding#policy_kind}
        '''
        result = self._values.get("policy_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IamOrganizationsPolicyBindingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#timeouts IamOrganizationsPolicyBinding#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IamOrganizationsPolicyBindingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamOrganizationsPolicyBindingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamOrganizationsPolicyBinding.IamOrganizationsPolicyBindingTarget",
    jsii_struct_bases=[],
    name_mapping={"principal_set": "principalSet"},
)
class IamOrganizationsPolicyBindingTarget:
    def __init__(self, *, principal_set: typing.Optional[builtins.str] = None) -> None:
        '''
        :param principal_set: Required. Immutable. Full Resource Name of the principal set used for principal access boundary policy bindings. Examples for each one of the following supported principal set types: - Organization '//cloudresourcemanager.googleapis.com/organizations/ORGANIZATION_ID' - Workforce Identity: '//iam.googleapis.com/locations/global/workforcePools/WORKFORCE_POOL_ID' - Workspace Identity: '//iam.googleapis.com/locations/global/workspace/WORKSPACE_ID' It must be parent by the policy binding's parent (the organization). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#principal_set IamOrganizationsPolicyBinding#principal_set}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daab58bbaf7e965b54ce4f5bab8d4938ce9eedaf8850eb6394de18d136240b44)
            check_type(argname="argument principal_set", value=principal_set, expected_type=type_hints["principal_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if principal_set is not None:
            self._values["principal_set"] = principal_set

    @builtins.property
    def principal_set(self) -> typing.Optional[builtins.str]:
        '''Required.

        Immutable. Full Resource Name of the principal set used for principal access boundary policy bindings.
        Examples for each one of the following supported principal set types:

        - Organization '//cloudresourcemanager.googleapis.com/organizations/ORGANIZATION_ID'
        - Workforce Identity: '//iam.googleapis.com/locations/global/workforcePools/WORKFORCE_POOL_ID'
        - Workspace Identity: '//iam.googleapis.com/locations/global/workspace/WORKSPACE_ID'
          It must be parent by the policy binding's parent (the organization).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#principal_set IamOrganizationsPolicyBinding#principal_set}
        '''
        result = self._values.get("principal_set")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamOrganizationsPolicyBindingTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamOrganizationsPolicyBindingTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamOrganizationsPolicyBinding.IamOrganizationsPolicyBindingTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c6888c3adfd12a06781fbd8b10252090a0625f20a67754d8dee318312091775)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrincipalSet")
    def reset_principal_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipalSet", []))

    @builtins.property
    @jsii.member(jsii_name="principalSetInput")
    def principal_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalSetInput"))

    @builtins.property
    @jsii.member(jsii_name="principalSet")
    def principal_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalSet"))

    @principal_set.setter
    def principal_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661927365e0f6405c4dab15394b527ab0deed2675bd56512ee9e9ec76a1ade0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IamOrganizationsPolicyBindingTarget]:
        return typing.cast(typing.Optional[IamOrganizationsPolicyBindingTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IamOrganizationsPolicyBindingTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f226d4923d704bebd9e57904193c2f82e097b00ea0c6b3d3b43e6a5fbbf2f0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.iamOrganizationsPolicyBinding.IamOrganizationsPolicyBindingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IamOrganizationsPolicyBindingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#create IamOrganizationsPolicyBinding#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#delete IamOrganizationsPolicyBinding#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#update IamOrganizationsPolicyBinding#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c580a6446ca5f31af4df36c33d8e865f09171cb50a8b0df0319c7b54310ce45)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#create IamOrganizationsPolicyBinding#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#delete IamOrganizationsPolicyBinding#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/iam_organizations_policy_binding#update IamOrganizationsPolicyBinding#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamOrganizationsPolicyBindingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamOrganizationsPolicyBindingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.iamOrganizationsPolicyBinding.IamOrganizationsPolicyBindingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fdb3ae7d07c828aa7e47f5606e5f25ccb4d9506cdb66b331c16ff94506636b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c62b3307ee62c19210fa8f8796ab47672749f07d769492cc0778d3767d4db128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc7b640153bbfe5ee4ebb240362a3107c064a7232e614b2f6cb772939c2a0bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e1ef3e61c67fbe9468963b50065241c0e30c02249646e8b45e563ffc3fdf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamOrganizationsPolicyBindingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamOrganizationsPolicyBindingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamOrganizationsPolicyBindingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e842787ee82d336f2b8fdb960f3ed445d863f7b01695fc1209362b72f450e28c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IamOrganizationsPolicyBinding",
    "IamOrganizationsPolicyBindingCondition",
    "IamOrganizationsPolicyBindingConditionOutputReference",
    "IamOrganizationsPolicyBindingConfig",
    "IamOrganizationsPolicyBindingTarget",
    "IamOrganizationsPolicyBindingTargetOutputReference",
    "IamOrganizationsPolicyBindingTimeouts",
    "IamOrganizationsPolicyBindingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e572344225ae7ec01add3be54180a57feededcc23f6a2595091ddb7a8ab54745(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    organization: builtins.str,
    policy: builtins.str,
    policy_binding_id: builtins.str,
    target: typing.Union[IamOrganizationsPolicyBindingTarget, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    condition: typing.Optional[typing.Union[IamOrganizationsPolicyBindingCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    policy_kind: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IamOrganizationsPolicyBindingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ceaa9a82d0f0c9245db50080130172c352ff2d83e8de501a9a9110c1363dd4fa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9086c1204301141c7156b29c54060f4aa562a58d8d3e7fc1233cc895df5325c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb2aa08033ea89f41762dcb5bc3193c1cf756fa38057805b94511490c5c2d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fd793a68ed146061ac413ba73e6adbf35cec95a219c52c7d363d4a274ccfd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ae21cfeb3e0f2208a620d2d03c9d221e13c6bf3752d093f757c1cc65a914f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057fd82b8be5515ba87081837557318d3f882737a2a75adef1f404e3448c3d05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7ac5e78f1ba8586d22d8aa868221aabb8a287204ea688d82997f802d5bf9cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03887c5596eb4c8d5ef204248a0198d4850a485a99c289a6ff15ed9d6e24b188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18621d52fb9af11f2dcb43fb833cebd70173c4139a6a2499271d913eb02b8990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c8b65a6306f73e93754baae83fc57da2cbffd248f1fdf0c3d2a013c7ab7721(
    *,
    description: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20776774444c4eebbfc6f42acdbad605e534f91dbe9ddcaa9950b82a9d0d4c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53dae6a825b34d9d9074a75dda9fb6260c95afc04ff25c85254a56fad631f7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0d5da0145496dbf32290f4f396d3b23a37d75eb737122164fc853c3dd04770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6cf0b3688010fe521bf88f71b42aaf782ad723fbf20c2b3fd2cdf578845f91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a83b2db1b33092e29f5fd82e40d81f1e9c8733bfcdcded1b9cd0bc560eeadb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb660ab9ff3b57026da3692a906601f49ba78124d1c7e77e41eb0068c5756e70(
    value: typing.Optional[IamOrganizationsPolicyBindingCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9707d4ac4f6bdb92180c98efba02443049ebc17b2969432006abd0dc2f2cc445(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    organization: builtins.str,
    policy: builtins.str,
    policy_binding_id: builtins.str,
    target: typing.Union[IamOrganizationsPolicyBindingTarget, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    condition: typing.Optional[typing.Union[IamOrganizationsPolicyBindingCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    policy_kind: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[IamOrganizationsPolicyBindingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daab58bbaf7e965b54ce4f5bab8d4938ce9eedaf8850eb6394de18d136240b44(
    *,
    principal_set: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6888c3adfd12a06781fbd8b10252090a0625f20a67754d8dee318312091775(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661927365e0f6405c4dab15394b527ab0deed2675bd56512ee9e9ec76a1ade0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f226d4923d704bebd9e57904193c2f82e097b00ea0c6b3d3b43e6a5fbbf2f0af(
    value: typing.Optional[IamOrganizationsPolicyBindingTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c580a6446ca5f31af4df36c33d8e865f09171cb50a8b0df0319c7b54310ce45(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fdb3ae7d07c828aa7e47f5606e5f25ccb4d9506cdb66b331c16ff94506636b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62b3307ee62c19210fa8f8796ab47672749f07d769492cc0778d3767d4db128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc7b640153bbfe5ee4ebb240362a3107c064a7232e614b2f6cb772939c2a0bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e1ef3e61c67fbe9468963b50065241c0e30c02249646e8b45e563ffc3fdf94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e842787ee82d336f2b8fdb960f3ed445d863f7b01695fc1209362b72f450e28c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IamOrganizationsPolicyBindingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
