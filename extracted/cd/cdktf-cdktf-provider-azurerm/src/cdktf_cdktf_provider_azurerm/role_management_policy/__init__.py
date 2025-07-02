r'''
# `azurerm_role_management_policy`

Refer to the Terraform Registry for docs: [`azurerm_role_management_policy`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy).
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


class RoleManagementPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy azurerm_role_management_policy}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        role_definition_id: builtins.str,
        scope: builtins.str,
        activation_rules: typing.Optional[typing.Union["RoleManagementPolicyActivationRules", typing.Dict[builtins.str, typing.Any]]] = None,
        active_assignment_rules: typing.Optional[typing.Union["RoleManagementPolicyActiveAssignmentRules", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_assignment_rules: typing.Optional[typing.Union["RoleManagementPolicyEligibleAssignmentRules", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notification_rules: typing.Optional[typing.Union["RoleManagementPolicyNotificationRules", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["RoleManagementPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy azurerm_role_management_policy} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param role_definition_id: ID of the Azure Role to which this policy is assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#role_definition_id RoleManagementPolicy#role_definition_id}
        :param scope: The scope of the role to which this policy will apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#scope RoleManagementPolicy#scope}
        :param activation_rules: activation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#activation_rules RoleManagementPolicy#activation_rules}
        :param active_assignment_rules: active_assignment_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#active_assignment_rules RoleManagementPolicy#active_assignment_rules}
        :param eligible_assignment_rules: eligible_assignment_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_assignment_rules RoleManagementPolicy#eligible_assignment_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#id RoleManagementPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_rules: notification_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_rules RoleManagementPolicy#notification_rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#timeouts RoleManagementPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7958f98ab342a04a32627778d30c149ca16a9bb6af2e428d72838d7dd038d76)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RoleManagementPolicyConfig(
            role_definition_id=role_definition_id,
            scope=scope,
            activation_rules=activation_rules,
            active_assignment_rules=active_assignment_rules,
            eligible_assignment_rules=eligible_assignment_rules,
            id=id,
            notification_rules=notification_rules,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a RoleManagementPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RoleManagementPolicy to import.
        :param import_from_id: The id of the existing RoleManagementPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RoleManagementPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d96bd8a92943f2764024d6c593eeee05ac62f47986fda2bed89e2e9db96cda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActivationRules")
    def put_activation_rules(
        self,
        *,
        approval_stage: typing.Optional[typing.Union["RoleManagementPolicyActivationRulesApprovalStage", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_duration: typing.Optional[builtins.str] = None,
        require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_conditional_access_authentication_context: typing.Optional[builtins.str] = None,
        require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_stage: approval_stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approval_stage RoleManagementPolicy#approval_stage}
        :param maximum_duration: The time after which the an activation can be valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#maximum_duration RoleManagementPolicy#maximum_duration}
        :param require_approval: Whether an approval is required for activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_approval RoleManagementPolicy#require_approval}
        :param required_conditional_access_authentication_context: Whether a conditional access context is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#required_conditional_access_authentication_context RoleManagementPolicy#required_conditional_access_authentication_context}
        :param require_justification: Whether a justification is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_justification RoleManagementPolicy#require_justification}
        :param require_multifactor_authentication: Whether multi-factor authentication is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_multifactor_authentication RoleManagementPolicy#require_multifactor_authentication}
        :param require_ticket_info: Whether ticket information is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_ticket_info RoleManagementPolicy#require_ticket_info}
        '''
        value = RoleManagementPolicyActivationRules(
            approval_stage=approval_stage,
            maximum_duration=maximum_duration,
            require_approval=require_approval,
            required_conditional_access_authentication_context=required_conditional_access_authentication_context,
            require_justification=require_justification,
            require_multifactor_authentication=require_multifactor_authentication,
            require_ticket_info=require_ticket_info,
        )

        return typing.cast(None, jsii.invoke(self, "putActivationRules", [value]))

    @jsii.member(jsii_name="putActiveAssignmentRules")
    def put_active_assignment_rules(
        self,
        *,
        expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expire_after: typing.Optional[builtins.str] = None,
        require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param expiration_required: Must the assignment have an expiry date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expiration_required RoleManagementPolicy#expiration_required}
        :param expire_after: The duration after which assignments expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expire_after RoleManagementPolicy#expire_after}
        :param require_justification: Whether a justification is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_justification RoleManagementPolicy#require_justification}
        :param require_multifactor_authentication: Whether multi-factor authentication is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_multifactor_authentication RoleManagementPolicy#require_multifactor_authentication}
        :param require_ticket_info: Whether ticket information is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_ticket_info RoleManagementPolicy#require_ticket_info}
        '''
        value = RoleManagementPolicyActiveAssignmentRules(
            expiration_required=expiration_required,
            expire_after=expire_after,
            require_justification=require_justification,
            require_multifactor_authentication=require_multifactor_authentication,
            require_ticket_info=require_ticket_info,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveAssignmentRules", [value]))

    @jsii.member(jsii_name="putEligibleAssignmentRules")
    def put_eligible_assignment_rules(
        self,
        *,
        expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expire_after: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration_required: Must the assignment have an expiry date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expiration_required RoleManagementPolicy#expiration_required}
        :param expire_after: The duration after which assignments expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expire_after RoleManagementPolicy#expire_after}
        '''
        value = RoleManagementPolicyEligibleAssignmentRules(
            expiration_required=expiration_required, expire_after=expire_after
        )

        return typing.cast(None, jsii.invoke(self, "putEligibleAssignmentRules", [value]))

    @jsii.member(jsii_name="putNotificationRules")
    def put_notification_rules(
        self,
        *,
        active_assignments: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesActiveAssignments", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_activations: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleActivations", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_assignments: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleAssignments", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param active_assignments: active_assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#active_assignments RoleManagementPolicy#active_assignments}
        :param eligible_activations: eligible_activations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_activations RoleManagementPolicy#eligible_activations}
        :param eligible_assignments: eligible_assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_assignments RoleManagementPolicy#eligible_assignments}
        '''
        value = RoleManagementPolicyNotificationRules(
            active_assignments=active_assignments,
            eligible_activations=eligible_activations,
            eligible_assignments=eligible_assignments,
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationRules", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#create RoleManagementPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#delete RoleManagementPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#read RoleManagementPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#update RoleManagementPolicy#update}.
        '''
        value = RoleManagementPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActivationRules")
    def reset_activation_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivationRules", []))

    @jsii.member(jsii_name="resetActiveAssignmentRules")
    def reset_active_assignment_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveAssignmentRules", []))

    @jsii.member(jsii_name="resetEligibleAssignmentRules")
    def reset_eligible_assignment_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEligibleAssignmentRules", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotificationRules")
    def reset_notification_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationRules", []))

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
    @jsii.member(jsii_name="activationRules")
    def activation_rules(self) -> "RoleManagementPolicyActivationRulesOutputReference":
        return typing.cast("RoleManagementPolicyActivationRulesOutputReference", jsii.get(self, "activationRules"))

    @builtins.property
    @jsii.member(jsii_name="activeAssignmentRules")
    def active_assignment_rules(
        self,
    ) -> "RoleManagementPolicyActiveAssignmentRulesOutputReference":
        return typing.cast("RoleManagementPolicyActiveAssignmentRulesOutputReference", jsii.get(self, "activeAssignmentRules"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAssignmentRules")
    def eligible_assignment_rules(
        self,
    ) -> "RoleManagementPolicyEligibleAssignmentRulesOutputReference":
        return typing.cast("RoleManagementPolicyEligibleAssignmentRulesOutputReference", jsii.get(self, "eligibleAssignmentRules"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="notificationRules")
    def notification_rules(
        self,
    ) -> "RoleManagementPolicyNotificationRulesOutputReference":
        return typing.cast("RoleManagementPolicyNotificationRulesOutputReference", jsii.get(self, "notificationRules"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RoleManagementPolicyTimeoutsOutputReference":
        return typing.cast("RoleManagementPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="activationRulesInput")
    def activation_rules_input(
        self,
    ) -> typing.Optional["RoleManagementPolicyActivationRules"]:
        return typing.cast(typing.Optional["RoleManagementPolicyActivationRules"], jsii.get(self, "activationRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="activeAssignmentRulesInput")
    def active_assignment_rules_input(
        self,
    ) -> typing.Optional["RoleManagementPolicyActiveAssignmentRules"]:
        return typing.cast(typing.Optional["RoleManagementPolicyActiveAssignmentRules"], jsii.get(self, "activeAssignmentRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAssignmentRulesInput")
    def eligible_assignment_rules_input(
        self,
    ) -> typing.Optional["RoleManagementPolicyEligibleAssignmentRules"]:
        return typing.cast(typing.Optional["RoleManagementPolicyEligibleAssignmentRules"], jsii.get(self, "eligibleAssignmentRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationRulesInput")
    def notification_rules_input(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRules"]:
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRules"], jsii.get(self, "notificationRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionIdInput")
    def role_definition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleDefinitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RoleManagementPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RoleManagementPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__addb81e8089959c530a0e2ec779d5e531eeec9e61fc6b2a8f88233230684cc2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionId")
    def role_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleDefinitionId"))

    @role_definition_id.setter
    def role_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57b355c6265e872a58d8419e5d490e490baf05a39e76b9c39364cba5fae531f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleDefinitionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378254f98eb3ecc635250a387025dd4a9cc3979dfbfd41477903be3222d7b2ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActivationRules",
    jsii_struct_bases=[],
    name_mapping={
        "approval_stage": "approvalStage",
        "maximum_duration": "maximumDuration",
        "require_approval": "requireApproval",
        "required_conditional_access_authentication_context": "requiredConditionalAccessAuthenticationContext",
        "require_justification": "requireJustification",
        "require_multifactor_authentication": "requireMultifactorAuthentication",
        "require_ticket_info": "requireTicketInfo",
    },
)
class RoleManagementPolicyActivationRules:
    def __init__(
        self,
        *,
        approval_stage: typing.Optional[typing.Union["RoleManagementPolicyActivationRulesApprovalStage", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_duration: typing.Optional[builtins.str] = None,
        require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_conditional_access_authentication_context: typing.Optional[builtins.str] = None,
        require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_stage: approval_stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approval_stage RoleManagementPolicy#approval_stage}
        :param maximum_duration: The time after which the an activation can be valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#maximum_duration RoleManagementPolicy#maximum_duration}
        :param require_approval: Whether an approval is required for activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_approval RoleManagementPolicy#require_approval}
        :param required_conditional_access_authentication_context: Whether a conditional access context is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#required_conditional_access_authentication_context RoleManagementPolicy#required_conditional_access_authentication_context}
        :param require_justification: Whether a justification is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_justification RoleManagementPolicy#require_justification}
        :param require_multifactor_authentication: Whether multi-factor authentication is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_multifactor_authentication RoleManagementPolicy#require_multifactor_authentication}
        :param require_ticket_info: Whether ticket information is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_ticket_info RoleManagementPolicy#require_ticket_info}
        '''
        if isinstance(approval_stage, dict):
            approval_stage = RoleManagementPolicyActivationRulesApprovalStage(**approval_stage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8817b4b0333f740f41876d8ea9b7f8449b018723f48c662fdf6e50b5531245b)
            check_type(argname="argument approval_stage", value=approval_stage, expected_type=type_hints["approval_stage"])
            check_type(argname="argument maximum_duration", value=maximum_duration, expected_type=type_hints["maximum_duration"])
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
            check_type(argname="argument required_conditional_access_authentication_context", value=required_conditional_access_authentication_context, expected_type=type_hints["required_conditional_access_authentication_context"])
            check_type(argname="argument require_justification", value=require_justification, expected_type=type_hints["require_justification"])
            check_type(argname="argument require_multifactor_authentication", value=require_multifactor_authentication, expected_type=type_hints["require_multifactor_authentication"])
            check_type(argname="argument require_ticket_info", value=require_ticket_info, expected_type=type_hints["require_ticket_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if approval_stage is not None:
            self._values["approval_stage"] = approval_stage
        if maximum_duration is not None:
            self._values["maximum_duration"] = maximum_duration
        if require_approval is not None:
            self._values["require_approval"] = require_approval
        if required_conditional_access_authentication_context is not None:
            self._values["required_conditional_access_authentication_context"] = required_conditional_access_authentication_context
        if require_justification is not None:
            self._values["require_justification"] = require_justification
        if require_multifactor_authentication is not None:
            self._values["require_multifactor_authentication"] = require_multifactor_authentication
        if require_ticket_info is not None:
            self._values["require_ticket_info"] = require_ticket_info

    @builtins.property
    def approval_stage(
        self,
    ) -> typing.Optional["RoleManagementPolicyActivationRulesApprovalStage"]:
        '''approval_stage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approval_stage RoleManagementPolicy#approval_stage}
        '''
        result = self._values.get("approval_stage")
        return typing.cast(typing.Optional["RoleManagementPolicyActivationRulesApprovalStage"], result)

    @builtins.property
    def maximum_duration(self) -> typing.Optional[builtins.str]:
        '''The time after which the an activation can be valid for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#maximum_duration RoleManagementPolicy#maximum_duration}
        '''
        result = self._values.get("maximum_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an approval is required for activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_approval RoleManagementPolicy#require_approval}
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_conditional_access_authentication_context(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Whether a conditional access context is required during activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#required_conditional_access_authentication_context RoleManagementPolicy#required_conditional_access_authentication_context}
        '''
        result = self._values.get("required_conditional_access_authentication_context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_justification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a justification is required during activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_justification RoleManagementPolicy#require_justification}
        '''
        result = self._values.get("require_justification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_multifactor_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether multi-factor authentication is required during activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_multifactor_authentication RoleManagementPolicy#require_multifactor_authentication}
        '''
        result = self._values.get("require_multifactor_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_ticket_info(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether ticket information is required during activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_ticket_info RoleManagementPolicy#require_ticket_info}
        '''
        result = self._values.get("require_ticket_info")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyActivationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActivationRulesApprovalStage",
    jsii_struct_bases=[],
    name_mapping={"primary_approver": "primaryApprover"},
)
class RoleManagementPolicyActivationRulesApprovalStage:
    def __init__(
        self,
        *,
        primary_approver: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param primary_approver: primary_approver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#primary_approver RoleManagementPolicy#primary_approver}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a80dbe513481e62ed165c87c501216da9a99b9909fad485cf9f7888479ecdc)
            check_type(argname="argument primary_approver", value=primary_approver, expected_type=type_hints["primary_approver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primary_approver": primary_approver,
        }

    @builtins.property
    def primary_approver(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover"]]:
        '''primary_approver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#primary_approver RoleManagementPolicy#primary_approver}
        '''
        result = self._values.get("primary_approver")
        assert result is not None, "Required property 'primary_approver' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyActivationRulesApprovalStage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyActivationRulesApprovalStageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActivationRulesApprovalStageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bcbac330ad097bb2ba7c0002311a5134c2e863f7042a3d174e2d6eb60ecc328)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrimaryApprover")
    def put_primary_approver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380b2fbfb9c09914fced4e66604eb073524b599d2ffee67749320f9c5f4ea801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrimaryApprover", [value]))

    @builtins.property
    @jsii.member(jsii_name="primaryApprover")
    def primary_approver(
        self,
    ) -> "RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList":
        return typing.cast("RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList", jsii.get(self, "primaryApprover"))

    @builtins.property
    @jsii.member(jsii_name="primaryApproverInput")
    def primary_approver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover"]]], jsii.get(self, "primaryApproverInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyActivationRulesApprovalStage]:
        return typing.cast(typing.Optional[RoleManagementPolicyActivationRulesApprovalStage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyActivationRulesApprovalStage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f8b20a4d5ffdb9483fe95ba76a076ad326423c7ba08379c1eaa6ea07f4d5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover",
    jsii_struct_bases=[],
    name_mapping={"object_id": "objectId", "type": "type"},
)
class RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover:
    def __init__(self, *, object_id: builtins.str, type: builtins.str) -> None:
        '''
        :param object_id: The ID of the object to act as an approver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#object_id RoleManagementPolicy#object_id}
        :param type: The type of object acting as an approver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#type RoleManagementPolicy#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5c80c0330bfe3536c3a7c99f779bd00fecd12f96e3728e8243bc82ea157a94)
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id": object_id,
            "type": type,
        }

    @builtins.property
    def object_id(self) -> builtins.str:
        '''The ID of the object to act as an approver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#object_id RoleManagementPolicy#object_id}
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of object acting as an approver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#type RoleManagementPolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7743638bcb25dd33ffd63f941c013cc382245507aa6abc77d3ce0fc73c878446)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287f3b4f9007e23d4bf3f909a2851f1337af687d61693f6fc488d52483ce7f1c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ca0a7e783d804cb3daa5d3c66d6a2e759408580a9ca066a863a7461087ce7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f4e937602296abe4a010bdaee611a492551619f9c737a42efc0836dce54f38c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c32dbb3278072cabcb9aed170c37d84766c52e663cc85fa5c422f69e9830228a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c75f607de633e7db92657d1c32b0b64bb2c91c609351b5c8a1c5c84a427aa29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5920876e232a63cc5e13f450f03fdb5d1708d77c050600084f3ba2a34984c61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec13f25b8e7c57a1fece1e2c98badc9cd9a760c637c38a7495feb11bd11cc6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ba51e0961027fc053c7d5ca121bfb22a129c346f6ec150462fd72f655e8e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663a7eecb7866a96248388f16c6bf84f2209fbee9d51558bb50f9508c7fddc08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RoleManagementPolicyActivationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActivationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d38b43ce1ca9002e627a904d9f4f6ff42192264a31257e2408462abb4e14df8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApprovalStage")
    def put_approval_stage(
        self,
        *,
        primary_approver: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param primary_approver: primary_approver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#primary_approver RoleManagementPolicy#primary_approver}
        '''
        value = RoleManagementPolicyActivationRulesApprovalStage(
            primary_approver=primary_approver
        )

        return typing.cast(None, jsii.invoke(self, "putApprovalStage", [value]))

    @jsii.member(jsii_name="resetApprovalStage")
    def reset_approval_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalStage", []))

    @jsii.member(jsii_name="resetMaximumDuration")
    def reset_maximum_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumDuration", []))

    @jsii.member(jsii_name="resetRequireApproval")
    def reset_require_approval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireApproval", []))

    @jsii.member(jsii_name="resetRequiredConditionalAccessAuthenticationContext")
    def reset_required_conditional_access_authentication_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredConditionalAccessAuthenticationContext", []))

    @jsii.member(jsii_name="resetRequireJustification")
    def reset_require_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireJustification", []))

    @jsii.member(jsii_name="resetRequireMultifactorAuthentication")
    def reset_require_multifactor_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireMultifactorAuthentication", []))

    @jsii.member(jsii_name="resetRequireTicketInfo")
    def reset_require_ticket_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireTicketInfo", []))

    @builtins.property
    @jsii.member(jsii_name="approvalStage")
    def approval_stage(
        self,
    ) -> RoleManagementPolicyActivationRulesApprovalStageOutputReference:
        return typing.cast(RoleManagementPolicyActivationRulesApprovalStageOutputReference, jsii.get(self, "approvalStage"))

    @builtins.property
    @jsii.member(jsii_name="approvalStageInput")
    def approval_stage_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyActivationRulesApprovalStage]:
        return typing.cast(typing.Optional[RoleManagementPolicyActivationRulesApprovalStage], jsii.get(self, "approvalStageInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumDurationInput")
    def maximum_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maximumDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="requireApprovalInput")
    def require_approval_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireApprovalInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredConditionalAccessAuthenticationContextInput")
    def required_conditional_access_authentication_context_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requiredConditionalAccessAuthenticationContextInput"))

    @builtins.property
    @jsii.member(jsii_name="requireJustificationInput")
    def require_justification_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireJustificationInput"))

    @builtins.property
    @jsii.member(jsii_name="requireMultifactorAuthenticationInput")
    def require_multifactor_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireMultifactorAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="requireTicketInfoInput")
    def require_ticket_info_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireTicketInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumDuration")
    def maximum_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maximumDuration"))

    @maximum_duration.setter
    def maximum_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391c844f959befc52853ac3e5c0bb35a601f833cd20984b3dfc14b0d57887bb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireApproval")
    def require_approval(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireApproval"))

    @require_approval.setter
    def require_approval(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e4f19fa96facb9839f5a65962b6c469b4a7cd41f3e80ee5e205d27a09df428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireApproval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredConditionalAccessAuthenticationContext")
    def required_conditional_access_authentication_context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requiredConditionalAccessAuthenticationContext"))

    @required_conditional_access_authentication_context.setter
    def required_conditional_access_authentication_context(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724b3430a03b43054f3a1c627272529a5682bb9f9dcb273eb7481c321920790e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredConditionalAccessAuthenticationContext", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireJustification")
    def require_justification(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireJustification"))

    @require_justification.setter
    def require_justification(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db17090e0894215893b19e401e41bc8741ce8e164b94d46a5779d378d3590e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireJustification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireMultifactorAuthentication")
    def require_multifactor_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireMultifactorAuthentication"))

    @require_multifactor_authentication.setter
    def require_multifactor_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc52fd7416447e25f360e1e5242f5d8c136059d63f89d2eadbb1e506f063cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireMultifactorAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireTicketInfo")
    def require_ticket_info(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireTicketInfo"))

    @require_ticket_info.setter
    def require_ticket_info(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9ee6ca674608fa93a0bbcfc364319d747e5d1a00cb6abed539f00ec2ce7a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireTicketInfo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RoleManagementPolicyActivationRules]:
        return typing.cast(typing.Optional[RoleManagementPolicyActivationRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyActivationRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db394a3467401a9bece1f62693ef1eefac279a29873dd3923f4abe87a36b4211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActiveAssignmentRules",
    jsii_struct_bases=[],
    name_mapping={
        "expiration_required": "expirationRequired",
        "expire_after": "expireAfter",
        "require_justification": "requireJustification",
        "require_multifactor_authentication": "requireMultifactorAuthentication",
        "require_ticket_info": "requireTicketInfo",
    },
)
class RoleManagementPolicyActiveAssignmentRules:
    def __init__(
        self,
        *,
        expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expire_after: typing.Optional[builtins.str] = None,
        require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param expiration_required: Must the assignment have an expiry date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expiration_required RoleManagementPolicy#expiration_required}
        :param expire_after: The duration after which assignments expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expire_after RoleManagementPolicy#expire_after}
        :param require_justification: Whether a justification is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_justification RoleManagementPolicy#require_justification}
        :param require_multifactor_authentication: Whether multi-factor authentication is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_multifactor_authentication RoleManagementPolicy#require_multifactor_authentication}
        :param require_ticket_info: Whether ticket information is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_ticket_info RoleManagementPolicy#require_ticket_info}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26adbf08a862ea1a8886a9b21f58486bc8c7233db381c49cf512b02e47938aa1)
            check_type(argname="argument expiration_required", value=expiration_required, expected_type=type_hints["expiration_required"])
            check_type(argname="argument expire_after", value=expire_after, expected_type=type_hints["expire_after"])
            check_type(argname="argument require_justification", value=require_justification, expected_type=type_hints["require_justification"])
            check_type(argname="argument require_multifactor_authentication", value=require_multifactor_authentication, expected_type=type_hints["require_multifactor_authentication"])
            check_type(argname="argument require_ticket_info", value=require_ticket_info, expected_type=type_hints["require_ticket_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expiration_required is not None:
            self._values["expiration_required"] = expiration_required
        if expire_after is not None:
            self._values["expire_after"] = expire_after
        if require_justification is not None:
            self._values["require_justification"] = require_justification
        if require_multifactor_authentication is not None:
            self._values["require_multifactor_authentication"] = require_multifactor_authentication
        if require_ticket_info is not None:
            self._values["require_ticket_info"] = require_ticket_info

    @builtins.property
    def expiration_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Must the assignment have an expiry date.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expiration_required RoleManagementPolicy#expiration_required}
        '''
        result = self._values.get("expiration_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expire_after(self) -> typing.Optional[builtins.str]:
        '''The duration after which assignments expire.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expire_after RoleManagementPolicy#expire_after}
        '''
        result = self._values.get("expire_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_justification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a justification is required to make an assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_justification RoleManagementPolicy#require_justification}
        '''
        result = self._values.get("require_justification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_multifactor_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether multi-factor authentication is required to make an assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_multifactor_authentication RoleManagementPolicy#require_multifactor_authentication}
        '''
        result = self._values.get("require_multifactor_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_ticket_info(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether ticket information is required to make an assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#require_ticket_info RoleManagementPolicy#require_ticket_info}
        '''
        result = self._values.get("require_ticket_info")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyActiveAssignmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyActiveAssignmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyActiveAssignmentRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e32c13a92ad42ece0686e392384305e66ed8eb09567d7e2b1aa0f2952e4fefc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExpirationRequired")
    def reset_expiration_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationRequired", []))

    @jsii.member(jsii_name="resetExpireAfter")
    def reset_expire_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpireAfter", []))

    @jsii.member(jsii_name="resetRequireJustification")
    def reset_require_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireJustification", []))

    @jsii.member(jsii_name="resetRequireMultifactorAuthentication")
    def reset_require_multifactor_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireMultifactorAuthentication", []))

    @jsii.member(jsii_name="resetRequireTicketInfo")
    def reset_require_ticket_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireTicketInfo", []))

    @builtins.property
    @jsii.member(jsii_name="expirationRequiredInput")
    def expiration_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "expirationRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="expireAfterInput")
    def expire_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="requireJustificationInput")
    def require_justification_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireJustificationInput"))

    @builtins.property
    @jsii.member(jsii_name="requireMultifactorAuthenticationInput")
    def require_multifactor_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireMultifactorAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="requireTicketInfoInput")
    def require_ticket_info_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireTicketInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationRequired")
    def expiration_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "expirationRequired"))

    @expiration_required.setter
    def expiration_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2528dd29c4c80818787af36d29f79bbeec06e87dc7894852e4a6270d3f44ec6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expireAfter")
    def expire_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireAfter"))

    @expire_after.setter
    def expire_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f97e18a4b67471cce1df581bef9ac2970aa689ee91c2ae4f3033ec33789b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireJustification")
    def require_justification(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireJustification"))

    @require_justification.setter
    def require_justification(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554f670eb73ad224548b78eca138e02ce0fd6d18bd07d209d50445d02a2a88f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireJustification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireMultifactorAuthentication")
    def require_multifactor_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireMultifactorAuthentication"))

    @require_multifactor_authentication.setter
    def require_multifactor_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30ba4aa381e923d71cbb521d41fe1d1df333fd94444fffcb59e4474ec9a0b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireMultifactorAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireTicketInfo")
    def require_ticket_info(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireTicketInfo"))

    @require_ticket_info.setter
    def require_ticket_info(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fe6a0762689c82e33125158ae5d0604daa694427d6f13c20a0e69bfcaaa0ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireTicketInfo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyActiveAssignmentRules]:
        return typing.cast(typing.Optional[RoleManagementPolicyActiveAssignmentRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyActiveAssignmentRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c1011ab2c0a3cf196a3b58b296c57f34381fe37f81c70905f181e0f7f5c187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "role_definition_id": "roleDefinitionId",
        "scope": "scope",
        "activation_rules": "activationRules",
        "active_assignment_rules": "activeAssignmentRules",
        "eligible_assignment_rules": "eligibleAssignmentRules",
        "id": "id",
        "notification_rules": "notificationRules",
        "timeouts": "timeouts",
    },
)
class RoleManagementPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        role_definition_id: builtins.str,
        scope: builtins.str,
        activation_rules: typing.Optional[typing.Union[RoleManagementPolicyActivationRules, typing.Dict[builtins.str, typing.Any]]] = None,
        active_assignment_rules: typing.Optional[typing.Union[RoleManagementPolicyActiveAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_assignment_rules: typing.Optional[typing.Union["RoleManagementPolicyEligibleAssignmentRules", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notification_rules: typing.Optional[typing.Union["RoleManagementPolicyNotificationRules", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["RoleManagementPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param role_definition_id: ID of the Azure Role to which this policy is assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#role_definition_id RoleManagementPolicy#role_definition_id}
        :param scope: The scope of the role to which this policy will apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#scope RoleManagementPolicy#scope}
        :param activation_rules: activation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#activation_rules RoleManagementPolicy#activation_rules}
        :param active_assignment_rules: active_assignment_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#active_assignment_rules RoleManagementPolicy#active_assignment_rules}
        :param eligible_assignment_rules: eligible_assignment_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_assignment_rules RoleManagementPolicy#eligible_assignment_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#id RoleManagementPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_rules: notification_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_rules RoleManagementPolicy#notification_rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#timeouts RoleManagementPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(activation_rules, dict):
            activation_rules = RoleManagementPolicyActivationRules(**activation_rules)
        if isinstance(active_assignment_rules, dict):
            active_assignment_rules = RoleManagementPolicyActiveAssignmentRules(**active_assignment_rules)
        if isinstance(eligible_assignment_rules, dict):
            eligible_assignment_rules = RoleManagementPolicyEligibleAssignmentRules(**eligible_assignment_rules)
        if isinstance(notification_rules, dict):
            notification_rules = RoleManagementPolicyNotificationRules(**notification_rules)
        if isinstance(timeouts, dict):
            timeouts = RoleManagementPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3901d2192e8b18794b49ab4b77569df94ff84e4bfd15db54679d8a675987e73)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument role_definition_id", value=role_definition_id, expected_type=type_hints["role_definition_id"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument activation_rules", value=activation_rules, expected_type=type_hints["activation_rules"])
            check_type(argname="argument active_assignment_rules", value=active_assignment_rules, expected_type=type_hints["active_assignment_rules"])
            check_type(argname="argument eligible_assignment_rules", value=eligible_assignment_rules, expected_type=type_hints["eligible_assignment_rules"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_rules", value=notification_rules, expected_type=type_hints["notification_rules"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_definition_id": role_definition_id,
            "scope": scope,
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
        if activation_rules is not None:
            self._values["activation_rules"] = activation_rules
        if active_assignment_rules is not None:
            self._values["active_assignment_rules"] = active_assignment_rules
        if eligible_assignment_rules is not None:
            self._values["eligible_assignment_rules"] = eligible_assignment_rules
        if id is not None:
            self._values["id"] = id
        if notification_rules is not None:
            self._values["notification_rules"] = notification_rules
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
    def role_definition_id(self) -> builtins.str:
        '''ID of the Azure Role to which this policy is assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#role_definition_id RoleManagementPolicy#role_definition_id}
        '''
        result = self._values.get("role_definition_id")
        assert result is not None, "Required property 'role_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''The scope of the role to which this policy will apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#scope RoleManagementPolicy#scope}
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activation_rules(self) -> typing.Optional[RoleManagementPolicyActivationRules]:
        '''activation_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#activation_rules RoleManagementPolicy#activation_rules}
        '''
        result = self._values.get("activation_rules")
        return typing.cast(typing.Optional[RoleManagementPolicyActivationRules], result)

    @builtins.property
    def active_assignment_rules(
        self,
    ) -> typing.Optional[RoleManagementPolicyActiveAssignmentRules]:
        '''active_assignment_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#active_assignment_rules RoleManagementPolicy#active_assignment_rules}
        '''
        result = self._values.get("active_assignment_rules")
        return typing.cast(typing.Optional[RoleManagementPolicyActiveAssignmentRules], result)

    @builtins.property
    def eligible_assignment_rules(
        self,
    ) -> typing.Optional["RoleManagementPolicyEligibleAssignmentRules"]:
        '''eligible_assignment_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_assignment_rules RoleManagementPolicy#eligible_assignment_rules}
        '''
        result = self._values.get("eligible_assignment_rules")
        return typing.cast(typing.Optional["RoleManagementPolicyEligibleAssignmentRules"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#id RoleManagementPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_rules(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRules"]:
        '''notification_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_rules RoleManagementPolicy#notification_rules}
        '''
        result = self._values.get("notification_rules")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRules"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RoleManagementPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#timeouts RoleManagementPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RoleManagementPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyEligibleAssignmentRules",
    jsii_struct_bases=[],
    name_mapping={
        "expiration_required": "expirationRequired",
        "expire_after": "expireAfter",
    },
)
class RoleManagementPolicyEligibleAssignmentRules:
    def __init__(
        self,
        *,
        expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expire_after: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration_required: Must the assignment have an expiry date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expiration_required RoleManagementPolicy#expiration_required}
        :param expire_after: The duration after which assignments expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expire_after RoleManagementPolicy#expire_after}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7863f00e4a694cb52633f6391b689ff5aef42c2fb201587ef9938be9279c80)
            check_type(argname="argument expiration_required", value=expiration_required, expected_type=type_hints["expiration_required"])
            check_type(argname="argument expire_after", value=expire_after, expected_type=type_hints["expire_after"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expiration_required is not None:
            self._values["expiration_required"] = expiration_required
        if expire_after is not None:
            self._values["expire_after"] = expire_after

    @builtins.property
    def expiration_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Must the assignment have an expiry date.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expiration_required RoleManagementPolicy#expiration_required}
        '''
        result = self._values.get("expiration_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expire_after(self) -> typing.Optional[builtins.str]:
        '''The duration after which assignments expire.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#expire_after RoleManagementPolicy#expire_after}
        '''
        result = self._values.get("expire_after")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyEligibleAssignmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyEligibleAssignmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyEligibleAssignmentRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d77ad5e64ce313459c7581c24a741e4e81fa08c44441fb869f5a1adcb5407b4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExpirationRequired")
    def reset_expiration_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationRequired", []))

    @jsii.member(jsii_name="resetExpireAfter")
    def reset_expire_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpireAfter", []))

    @builtins.property
    @jsii.member(jsii_name="expirationRequiredInput")
    def expiration_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "expirationRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="expireAfterInput")
    def expire_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationRequired")
    def expiration_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "expirationRequired"))

    @expiration_required.setter
    def expiration_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692f8912f03ff5a2ba1dc0de97e95284c3ea839579917d5ccf6f1c6695f02a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expireAfter")
    def expire_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireAfter"))

    @expire_after.setter
    def expire_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5670af07a216c9bad022c312aa26f6c8caf79de8b5ae093ad4357921f7e52fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyEligibleAssignmentRules]:
        return typing.cast(typing.Optional[RoleManagementPolicyEligibleAssignmentRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyEligibleAssignmentRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab6ee61ea11eb7812c019f5dc593182117a7f1efb8a6522d84224df2565f763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRules",
    jsii_struct_bases=[],
    name_mapping={
        "active_assignments": "activeAssignments",
        "eligible_activations": "eligibleActivations",
        "eligible_assignments": "eligibleAssignments",
    },
)
class RoleManagementPolicyNotificationRules:
    def __init__(
        self,
        *,
        active_assignments: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesActiveAssignments", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_activations: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleActivations", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_assignments: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleAssignments", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param active_assignments: active_assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#active_assignments RoleManagementPolicy#active_assignments}
        :param eligible_activations: eligible_activations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_activations RoleManagementPolicy#eligible_activations}
        :param eligible_assignments: eligible_assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_assignments RoleManagementPolicy#eligible_assignments}
        '''
        if isinstance(active_assignments, dict):
            active_assignments = RoleManagementPolicyNotificationRulesActiveAssignments(**active_assignments)
        if isinstance(eligible_activations, dict):
            eligible_activations = RoleManagementPolicyNotificationRulesEligibleActivations(**eligible_activations)
        if isinstance(eligible_assignments, dict):
            eligible_assignments = RoleManagementPolicyNotificationRulesEligibleAssignments(**eligible_assignments)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77f9606393ac2667e9a8d93ce096c5439602b85c38f79707c9167ced893696c)
            check_type(argname="argument active_assignments", value=active_assignments, expected_type=type_hints["active_assignments"])
            check_type(argname="argument eligible_activations", value=eligible_activations, expected_type=type_hints["eligible_activations"])
            check_type(argname="argument eligible_assignments", value=eligible_assignments, expected_type=type_hints["eligible_assignments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_assignments is not None:
            self._values["active_assignments"] = active_assignments
        if eligible_activations is not None:
            self._values["eligible_activations"] = eligible_activations
        if eligible_assignments is not None:
            self._values["eligible_assignments"] = eligible_assignments

    @builtins.property
    def active_assignments(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesActiveAssignments"]:
        '''active_assignments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#active_assignments RoleManagementPolicy#active_assignments}
        '''
        result = self._values.get("active_assignments")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesActiveAssignments"], result)

    @builtins.property
    def eligible_activations(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesEligibleActivations"]:
        '''eligible_activations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_activations RoleManagementPolicy#eligible_activations}
        '''
        result = self._values.get("eligible_activations")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesEligibleActivations"], result)

    @builtins.property
    def eligible_assignments(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesEligibleAssignments"]:
        '''eligible_assignments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#eligible_assignments RoleManagementPolicy#eligible_assignments}
        '''
        result = self._values.get("eligible_assignments")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesEligibleAssignments"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesActiveAssignments",
    jsii_struct_bases=[],
    name_mapping={
        "admin_notifications": "adminNotifications",
        "approver_notifications": "approverNotifications",
        "assignee_notifications": "assigneeNotifications",
    },
)
class RoleManagementPolicyNotificationRulesActiveAssignments:
    def __init__(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        if isinstance(admin_notifications, dict):
            admin_notifications = RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications(**admin_notifications)
        if isinstance(approver_notifications, dict):
            approver_notifications = RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications(**approver_notifications)
        if isinstance(assignee_notifications, dict):
            assignee_notifications = RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications(**assignee_notifications)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a6b00f92060b6b8f31b592a0b7204ce8c41a7ec3a4b151d6e764e24fc4d4d5)
            check_type(argname="argument admin_notifications", value=admin_notifications, expected_type=type_hints["admin_notifications"])
            check_type(argname="argument approver_notifications", value=approver_notifications, expected_type=type_hints["approver_notifications"])
            check_type(argname="argument assignee_notifications", value=assignee_notifications, expected_type=type_hints["assignee_notifications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_notifications is not None:
            self._values["admin_notifications"] = admin_notifications
        if approver_notifications is not None:
            self._values["approver_notifications"] = approver_notifications
        if assignee_notifications is not None:
            self._values["assignee_notifications"] = assignee_notifications

    @builtins.property
    def admin_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications"]:
        '''admin_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        '''
        result = self._values.get("admin_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications"], result)

    @builtins.property
    def approver_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications"]:
        '''approver_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        '''
        result = self._values.get("approver_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications"], result)

    @builtins.property
    def assignee_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications"]:
        '''assignee_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        result = self._values.get("assignee_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesActiveAssignments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36ba6b8aacdc5125670ad81aea16edefb83153d07a9ad236f067159116dc0c6)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69fa0be3ab335862296c443ca281120170e9642328d2d371a80ca8d944ea7c7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5bf32dcda731c78d89c5f6c25aca8e99641a20d79342a8077bae78b293ee3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ddfb631b05d4774381c655ada78174439b84c84cdf20a0d5b6267f720e60db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0195657bf7040cc0d59da92ed458a291e6bd05e70135614a2d5208854ec871ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac8be4ce28819305975ad7b7b6cd97e73513a661f248cc1eb451e2117beedb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f9abbfff2712ff78d4d8d1de52243a20909159b1992876db13e34fcf411d5a)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a5406c254b8b045f6632c7f7fa030e6b77cb644fe787b9e4328b9fc718ffd33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf92a6a97c4b9791c3645c1fabc60f903ae083649bfdd12ddb4b1e3561276303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a307f10d2d45750214da1e5bc87010e3c7c8f5a0474123cb0d4a18524be9c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06820c753880777d4ef7e51aa394cbc1953ad271e79c8b09235426ef62eb9f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb713aab94cf1bacb051b8f5eb47a868d51bb8a8c1947c51a5d2a0a83eb9fd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077a3f85d93203115317a88c27f78650f960619f974d2df410ec41f19b62176b)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b240453fc1291830479dd6ddc8abb7cb114e47e4eff98d7acb8bd7f99507e52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477b46ba57b4cad5dd34e81fc19416c80b8af05a3112754247768bff90247876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03afa4068544dbc9c34b56849f3bdec00834df5397d634d044395eaef7f4957a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41d45f4a7f259fa37d122d3fe162b2db1931fb1315f170a830f570d4d94ebe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9451fdc2ddf347497a52967de8e8f3cdcf0d27243601e1f3162a6e1237254f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2cc8ed3621a07b386878b25818c0b5ddb2cbe0dff141c954eb2fc09e6bbcf4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminNotifications")
    def put_admin_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putAdminNotifications", [value]))

    @jsii.member(jsii_name="putApproverNotifications")
    def put_approver_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putApproverNotifications", [value]))

    @jsii.member(jsii_name="putAssigneeNotifications")
    def put_assignee_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putAssigneeNotifications", [value]))

    @jsii.member(jsii_name="resetAdminNotifications")
    def reset_admin_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminNotifications", []))

    @jsii.member(jsii_name="resetApproverNotifications")
    def reset_approver_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApproverNotifications", []))

    @jsii.member(jsii_name="resetAssigneeNotifications")
    def reset_assignee_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssigneeNotifications", []))

    @builtins.property
    @jsii.member(jsii_name="adminNotifications")
    def admin_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference, jsii.get(self, "adminNotifications"))

    @builtins.property
    @jsii.member(jsii_name="approverNotifications")
    def approver_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference, jsii.get(self, "approverNotifications"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotifications")
    def assignee_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference, jsii.get(self, "assigneeNotifications"))

    @builtins.property
    @jsii.member(jsii_name="adminNotificationsInput")
    def admin_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications], jsii.get(self, "adminNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="approverNotificationsInput")
    def approver_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications], jsii.get(self, "approverNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotificationsInput")
    def assignee_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications], jsii.get(self, "assigneeNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignments]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb54d3ef71fa78cbfd9c3e126854b45cc353b7b55cb169d0d4cd0aaa4816e7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleActivations",
    jsii_struct_bases=[],
    name_mapping={
        "admin_notifications": "adminNotifications",
        "approver_notifications": "approverNotifications",
        "assignee_notifications": "assigneeNotifications",
    },
)
class RoleManagementPolicyNotificationRulesEligibleActivations:
    def __init__(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        if isinstance(admin_notifications, dict):
            admin_notifications = RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications(**admin_notifications)
        if isinstance(approver_notifications, dict):
            approver_notifications = RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications(**approver_notifications)
        if isinstance(assignee_notifications, dict):
            assignee_notifications = RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications(**assignee_notifications)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c508e24250072d0414d26933018f785871f0ad99d8d7c308ca297eaff04a85)
            check_type(argname="argument admin_notifications", value=admin_notifications, expected_type=type_hints["admin_notifications"])
            check_type(argname="argument approver_notifications", value=approver_notifications, expected_type=type_hints["approver_notifications"])
            check_type(argname="argument assignee_notifications", value=assignee_notifications, expected_type=type_hints["assignee_notifications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_notifications is not None:
            self._values["admin_notifications"] = admin_notifications
        if approver_notifications is not None:
            self._values["approver_notifications"] = approver_notifications
        if assignee_notifications is not None:
            self._values["assignee_notifications"] = assignee_notifications

    @builtins.property
    def admin_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications"]:
        '''admin_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        '''
        result = self._values.get("admin_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications"], result)

    @builtins.property
    def approver_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications"]:
        '''approver_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        '''
        result = self._values.get("approver_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications"], result)

    @builtins.property
    def assignee_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications"]:
        '''assignee_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        result = self._values.get("assignee_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesEligibleActivations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c8f0622f109f47e2ad782a46f92b83ec3c581680a4392108b891d614f8a7e0)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2badc3b782f82c0152e3011b47f579794286b1c5bf5adc5260bd50e58f05d5be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3e6a26efe40ba97d59b1dadd2ebb8fcca783b2e0b6f5f1aaa9d85ae2f83ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e458529de294a08ae6ca7a299ffe0b7d6782d695421435e19f74d2a76813ba3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35a76774dbfe29e33cf230d95449403b3994ad335a9a911f81023eafab62098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7735e10f1c6f5358e43361ada8cc8a6cf3130f14ddaae8e0fb40e04ef37fb44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90dd071e7ca289636bf96818c5b9ee5fd7ec46a36d45749fd293b2e8977bbbd3)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88df8e85460daa6c8cbd3b2d46fea435d4dcadf153fc960e2364fd8891e7deac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2170420d0c7b245383bd047e1e9c25ae15a5f0a1fe6a7eb920153d564b6247c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e20b560b5d069a9736bf8aea2d9ccc686819619a7e2fd267a4d0948975b3ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e5ff12ae8109ec0288563ceb132cbeae3976563c6d8ba8168113d237709f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c45b65b7b08bb7cb16b30a3f27da2d211c024c1ed5799c5aa8874a593e6d068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae26b7e08a17b6e5e89e657b6b07cf88895e9ac2b8384e83fe8dbc2c33d633f)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__721d8ee2087ad10bf2d85fe76b093985d41dcd819a185c2f8b4b4289677f5be9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c9af9121b9a450ff9993bc42fd6068915155f47685ce93e4f8e8b44f5d843f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e39d6088e80c86d7e98740fa76a174bee90450ca8ff5ec233d1571bab59be72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36ed28e41f6ea308bab7741de8cf0ac50f42b4c05e8003f1d5228fafb4f72e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92930c7d3de072a6c5e39766d935d4d857e4d963a7505b8cf6c1ebd31e960a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RoleManagementPolicyNotificationRulesEligibleActivationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleActivationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f12cf01d75a0227e1bef80c82bc3757da2ad3f66198eaa9537e386e21d74beb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminNotifications")
    def put_admin_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putAdminNotifications", [value]))

    @jsii.member(jsii_name="putApproverNotifications")
    def put_approver_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putApproverNotifications", [value]))

    @jsii.member(jsii_name="putAssigneeNotifications")
    def put_assignee_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putAssigneeNotifications", [value]))

    @jsii.member(jsii_name="resetAdminNotifications")
    def reset_admin_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminNotifications", []))

    @jsii.member(jsii_name="resetApproverNotifications")
    def reset_approver_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApproverNotifications", []))

    @jsii.member(jsii_name="resetAssigneeNotifications")
    def reset_assignee_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssigneeNotifications", []))

    @builtins.property
    @jsii.member(jsii_name="adminNotifications")
    def admin_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference, jsii.get(self, "adminNotifications"))

    @builtins.property
    @jsii.member(jsii_name="approverNotifications")
    def approver_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference, jsii.get(self, "approverNotifications"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotifications")
    def assignee_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference, jsii.get(self, "assigneeNotifications"))

    @builtins.property
    @jsii.member(jsii_name="adminNotificationsInput")
    def admin_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications], jsii.get(self, "adminNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="approverNotificationsInput")
    def approver_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications], jsii.get(self, "approverNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotificationsInput")
    def assignee_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications], jsii.get(self, "assigneeNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivations]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d957eeee9b7a6c9002e935921d2958ccbb1fa2ea3a8e0024918c79a92ece02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleAssignments",
    jsii_struct_bases=[],
    name_mapping={
        "admin_notifications": "adminNotifications",
        "approver_notifications": "approverNotifications",
        "assignee_notifications": "assigneeNotifications",
    },
)
class RoleManagementPolicyNotificationRulesEligibleAssignments:
    def __init__(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union["RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        if isinstance(admin_notifications, dict):
            admin_notifications = RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications(**admin_notifications)
        if isinstance(approver_notifications, dict):
            approver_notifications = RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications(**approver_notifications)
        if isinstance(assignee_notifications, dict):
            assignee_notifications = RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications(**assignee_notifications)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e910b43a32824ba097d8914610075edc3982704540a55fbe9fbe629bf55e201)
            check_type(argname="argument admin_notifications", value=admin_notifications, expected_type=type_hints["admin_notifications"])
            check_type(argname="argument approver_notifications", value=approver_notifications, expected_type=type_hints["approver_notifications"])
            check_type(argname="argument assignee_notifications", value=assignee_notifications, expected_type=type_hints["assignee_notifications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_notifications is not None:
            self._values["admin_notifications"] = admin_notifications
        if approver_notifications is not None:
            self._values["approver_notifications"] = approver_notifications
        if assignee_notifications is not None:
            self._values["assignee_notifications"] = assignee_notifications

    @builtins.property
    def admin_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications"]:
        '''admin_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        '''
        result = self._values.get("admin_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications"], result)

    @builtins.property
    def approver_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications"]:
        '''approver_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        '''
        result = self._values.get("approver_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications"], result)

    @builtins.property
    def assignee_notifications(
        self,
    ) -> typing.Optional["RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications"]:
        '''assignee_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        result = self._values.get("assignee_notifications")
        return typing.cast(typing.Optional["RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesEligibleAssignments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b774d51e05fd6f3e0ec1d3d9b3ddf7dfe77860a1186f5363d0a4c0bad42c31b)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01c6d819b04299eac8cdf2d686f4f90dd4697de48e8f07db97264c9742e1be30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce20ce683e70bee428c345c592e06baee7d9360b8cac7af6c9e92030b668376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3a659ed5d2ac12a8233476c6a70bdb87492f4ba7fa4ddf9aec95297cf0c449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0ccf0083c9788155c9fced2764ad70c1e03174cc35d860d5cbd329e7d5522c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087779bbd6f5e47e734168918f4a689a68c02f1609cfba6d822c85266570e25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab917d4781f7b23131af7123ffbec83d6a570d49a9b5845bb01f9d36a31be28)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77376f08e0aa6d0d576b15c6eadc51c9fea1363ef769ee6c5f529aae63d26aef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6285e0f6fe85d757cf3d978a65dfa4bb6b29fcd3ccc8f1891f7a370f849e01ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41eea8eab13f7020f5759ee999f369f66663e3213b6515d0292858645756a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffad0d57bc2bbbbc0131a72d5d2046ab65efddfe121dcd9a6531c1e86227ad1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08cd72ea3978346f01e5f77c27a8d7d6c0127f41a2d95ef8d1450d0df962df49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042a0d8c13e27d8ccac65d28880b3fbeb217ea462b44d6017328766bd450e28d)
            check_type(argname="argument default_recipients", value=default_recipients, expected_type=type_hints["default_recipients"])
            check_type(argname="argument notification_level", value=notification_level, expected_type=type_hints["notification_level"])
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_recipients": default_recipients,
            "notification_level": notification_level,
        }
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients

    @builtins.property
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the default recipients are notified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8d43de7f1f780bc23dd6f74d8a6443c21813f7e51ee540489a95f08b18cec57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRecipientsInput")
    def default_recipients_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationLevelInput")
    def notification_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195b735ef7b0b7e226b980040b443760c4ed3dc1d5fd2be821d5899ea0094a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRecipients")
    def default_recipients(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultRecipients"))

    @default_recipients.setter
    def default_recipients(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010e5be67714d5256b33562e7a2059cd3027ff0d53a0ee80879327612a51890a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2885e9d15265fe3ae63001ad33b58d6675db68c0a66ad7d59e7102070929e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8f3e7f4b19b1be9631e02bbdc27aa7fd1096ddf12dc6fb67c24fe383433c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17dc5bfca50270548a1ed680b2054c0b998a26fa25aacd15b345c65526047df7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminNotifications")
    def put_admin_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putAdminNotifications", [value]))

    @jsii.member(jsii_name="putApproverNotifications")
    def put_approver_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putApproverNotifications", [value]))

    @jsii.member(jsii_name="putAssigneeNotifications")
    def put_assignee_notifications(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#default_recipients RoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#notification_level RoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#additional_recipients RoleManagementPolicy#additional_recipients}
        '''
        value = RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications(
            default_recipients=default_recipients,
            notification_level=notification_level,
            additional_recipients=additional_recipients,
        )

        return typing.cast(None, jsii.invoke(self, "putAssigneeNotifications", [value]))

    @jsii.member(jsii_name="resetAdminNotifications")
    def reset_admin_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminNotifications", []))

    @jsii.member(jsii_name="resetApproverNotifications")
    def reset_approver_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApproverNotifications", []))

    @jsii.member(jsii_name="resetAssigneeNotifications")
    def reset_assignee_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssigneeNotifications", []))

    @builtins.property
    @jsii.member(jsii_name="adminNotifications")
    def admin_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference, jsii.get(self, "adminNotifications"))

    @builtins.property
    @jsii.member(jsii_name="approverNotifications")
    def approver_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference, jsii.get(self, "approverNotifications"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotifications")
    def assignee_notifications(
        self,
    ) -> RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference, jsii.get(self, "assigneeNotifications"))

    @builtins.property
    @jsii.member(jsii_name="adminNotificationsInput")
    def admin_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications], jsii.get(self, "adminNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="approverNotificationsInput")
    def approver_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications], jsii.get(self, "approverNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotificationsInput")
    def assignee_notifications_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications], jsii.get(self, "assigneeNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignments]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1667dcfa3774ffa860d1f67f0c009df9f22b87a5e205b35a58921e31319bc88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RoleManagementPolicyNotificationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyNotificationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a34943a9078c11a0602ca9dbedeb5e0fd601c3e2d86df00956a47a34843a2c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveAssignments")
    def put_active_assignments(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        value = RoleManagementPolicyNotificationRulesActiveAssignments(
            admin_notifications=admin_notifications,
            approver_notifications=approver_notifications,
            assignee_notifications=assignee_notifications,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveAssignments", [value]))

    @jsii.member(jsii_name="putEligibleActivations")
    def put_eligible_activations(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        value = RoleManagementPolicyNotificationRulesEligibleActivations(
            admin_notifications=admin_notifications,
            approver_notifications=approver_notifications,
            assignee_notifications=assignee_notifications,
        )

        return typing.cast(None, jsii.invoke(self, "putEligibleActivations", [value]))

    @jsii.member(jsii_name="putEligibleAssignments")
    def put_eligible_assignments(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#admin_notifications RoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#approver_notifications RoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#assignee_notifications RoleManagementPolicy#assignee_notifications}
        '''
        value = RoleManagementPolicyNotificationRulesEligibleAssignments(
            admin_notifications=admin_notifications,
            approver_notifications=approver_notifications,
            assignee_notifications=assignee_notifications,
        )

        return typing.cast(None, jsii.invoke(self, "putEligibleAssignments", [value]))

    @jsii.member(jsii_name="resetActiveAssignments")
    def reset_active_assignments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveAssignments", []))

    @jsii.member(jsii_name="resetEligibleActivations")
    def reset_eligible_activations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEligibleActivations", []))

    @jsii.member(jsii_name="resetEligibleAssignments")
    def reset_eligible_assignments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEligibleAssignments", []))

    @builtins.property
    @jsii.member(jsii_name="activeAssignments")
    def active_assignments(
        self,
    ) -> RoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference, jsii.get(self, "activeAssignments"))

    @builtins.property
    @jsii.member(jsii_name="eligibleActivations")
    def eligible_activations(
        self,
    ) -> RoleManagementPolicyNotificationRulesEligibleActivationsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesEligibleActivationsOutputReference, jsii.get(self, "eligibleActivations"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAssignments")
    def eligible_assignments(
        self,
    ) -> RoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference:
        return typing.cast(RoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference, jsii.get(self, "eligibleAssignments"))

    @builtins.property
    @jsii.member(jsii_name="activeAssignmentsInput")
    def active_assignments_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignments]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignments], jsii.get(self, "activeAssignmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleActivationsInput")
    def eligible_activations_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivations]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivations], jsii.get(self, "eligibleActivationsInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAssignmentsInput")
    def eligible_assignments_input(
        self,
    ) -> typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignments]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignments], jsii.get(self, "eligibleAssignmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RoleManagementPolicyNotificationRules]:
        return typing.cast(typing.Optional[RoleManagementPolicyNotificationRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RoleManagementPolicyNotificationRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c008734465556b2e7b05e3cc82f2bfb605a18b29cd81ef7da59932fdd28f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class RoleManagementPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#create RoleManagementPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#delete RoleManagementPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#read RoleManagementPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#update RoleManagementPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c15fd84a7104e05e29b5c7b5ac13c2e2213b475dc59332038b6d5d3a5b0ceb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#create RoleManagementPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#delete RoleManagementPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#read RoleManagementPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/role_management_policy#update RoleManagementPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleManagementPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RoleManagementPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.roleManagementPolicy.RoleManagementPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__325912e7bc65a08bfbc1f43ea8e24177e1a3618ed68b27317295e9c3b1201d49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__618f611eeaf92b0d3ee54704b60d587c5b16f481c7a9bc0b7782a4a7a5712f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca89866bccb12811450fe1a1824a32131e506c734d2770628e68e96c48c65bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bea80d7fb343afd0a17cbf4eb0790c5a49bc3d26b15a744d71075b42aeb8fe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0f63bc5a144e35143d69657af74cf9dc8eeca72f307ca104c4a0da1b56077c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RoleManagementPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RoleManagementPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RoleManagementPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9246d83515060da189896eac0e363a0670e92f7cbaffdebfc6e5535f7c870e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RoleManagementPolicy",
    "RoleManagementPolicyActivationRules",
    "RoleManagementPolicyActivationRulesApprovalStage",
    "RoleManagementPolicyActivationRulesApprovalStageOutputReference",
    "RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover",
    "RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList",
    "RoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference",
    "RoleManagementPolicyActivationRulesOutputReference",
    "RoleManagementPolicyActiveAssignmentRules",
    "RoleManagementPolicyActiveAssignmentRulesOutputReference",
    "RoleManagementPolicyConfig",
    "RoleManagementPolicyEligibleAssignmentRules",
    "RoleManagementPolicyEligibleAssignmentRulesOutputReference",
    "RoleManagementPolicyNotificationRules",
    "RoleManagementPolicyNotificationRulesActiveAssignments",
    "RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications",
    "RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications",
    "RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications",
    "RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference",
    "RoleManagementPolicyNotificationRulesEligibleActivations",
    "RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications",
    "RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications",
    "RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications",
    "RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesEligibleActivationsOutputReference",
    "RoleManagementPolicyNotificationRulesEligibleAssignments",
    "RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications",
    "RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications",
    "RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications",
    "RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference",
    "RoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference",
    "RoleManagementPolicyNotificationRulesOutputReference",
    "RoleManagementPolicyTimeouts",
    "RoleManagementPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e7958f98ab342a04a32627778d30c149ca16a9bb6af2e428d72838d7dd038d76(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    role_definition_id: builtins.str,
    scope: builtins.str,
    activation_rules: typing.Optional[typing.Union[RoleManagementPolicyActivationRules, typing.Dict[builtins.str, typing.Any]]] = None,
    active_assignment_rules: typing.Optional[typing.Union[RoleManagementPolicyActiveAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
    eligible_assignment_rules: typing.Optional[typing.Union[RoleManagementPolicyEligibleAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notification_rules: typing.Optional[typing.Union[RoleManagementPolicyNotificationRules, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[RoleManagementPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a3d96bd8a92943f2764024d6c593eeee05ac62f47986fda2bed89e2e9db96cda(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addb81e8089959c530a0e2ec779d5e531eeec9e61fc6b2a8f88233230684cc2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57b355c6265e872a58d8419e5d490e490baf05a39e76b9c39364cba5fae531f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378254f98eb3ecc635250a387025dd4a9cc3979dfbfd41477903be3222d7b2ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8817b4b0333f740f41876d8ea9b7f8449b018723f48c662fdf6e50b5531245b(
    *,
    approval_stage: typing.Optional[typing.Union[RoleManagementPolicyActivationRulesApprovalStage, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_duration: typing.Optional[builtins.str] = None,
    require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_conditional_access_authentication_context: typing.Optional[builtins.str] = None,
    require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a80dbe513481e62ed165c87c501216da9a99b9909fad485cf9f7888479ecdc(
    *,
    primary_approver: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcbac330ad097bb2ba7c0002311a5134c2e863f7042a3d174e2d6eb60ecc328(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380b2fbfb9c09914fced4e66604eb073524b599d2ffee67749320f9c5f4ea801(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f8b20a4d5ffdb9483fe95ba76a076ad326423c7ba08379c1eaa6ea07f4d5fc(
    value: typing.Optional[RoleManagementPolicyActivationRulesApprovalStage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5c80c0330bfe3536c3a7c99f779bd00fecd12f96e3728e8243bc82ea157a94(
    *,
    object_id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7743638bcb25dd33ffd63f941c013cc382245507aa6abc77d3ce0fc73c878446(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287f3b4f9007e23d4bf3f909a2851f1337af687d61693f6fc488d52483ce7f1c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ca0a7e783d804cb3daa5d3c66d6a2e759408580a9ca066a863a7461087ce7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4e937602296abe4a010bdaee611a492551619f9c737a42efc0836dce54f38c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32dbb3278072cabcb9aed170c37d84766c52e663cc85fa5c422f69e9830228a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c75f607de633e7db92657d1c32b0b64bb2c91c609351b5c8a1c5c84a427aa29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5920876e232a63cc5e13f450f03fdb5d1708d77c050600084f3ba2a34984c61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec13f25b8e7c57a1fece1e2c98badc9cd9a760c637c38a7495feb11bd11cc6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ba51e0961027fc053c7d5ca121bfb22a129c346f6ec150462fd72f655e8e8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663a7eecb7866a96248388f16c6bf84f2209fbee9d51558bb50f9508c7fddc08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d38b43ce1ca9002e627a904d9f4f6ff42192264a31257e2408462abb4e14df8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391c844f959befc52853ac3e5c0bb35a601f833cd20984b3dfc14b0d57887bb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e4f19fa96facb9839f5a65962b6c469b4a7cd41f3e80ee5e205d27a09df428(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724b3430a03b43054f3a1c627272529a5682bb9f9dcb273eb7481c321920790e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db17090e0894215893b19e401e41bc8741ce8e164b94d46a5779d378d3590e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc52fd7416447e25f360e1e5242f5d8c136059d63f89d2eadbb1e506f063cca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9ee6ca674608fa93a0bbcfc364319d747e5d1a00cb6abed539f00ec2ce7a9d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db394a3467401a9bece1f62693ef1eefac279a29873dd3923f4abe87a36b4211(
    value: typing.Optional[RoleManagementPolicyActivationRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26adbf08a862ea1a8886a9b21f58486bc8c7233db381c49cf512b02e47938aa1(
    *,
    expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expire_after: typing.Optional[builtins.str] = None,
    require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e32c13a92ad42ece0686e392384305e66ed8eb09567d7e2b1aa0f2952e4fefc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2528dd29c4c80818787af36d29f79bbeec06e87dc7894852e4a6270d3f44ec6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f97e18a4b67471cce1df581bef9ac2970aa689ee91c2ae4f3033ec33789b86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554f670eb73ad224548b78eca138e02ce0fd6d18bd07d209d50445d02a2a88f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30ba4aa381e923d71cbb521d41fe1d1df333fd94444fffcb59e4474ec9a0b3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fe6a0762689c82e33125158ae5d0604daa694427d6f13c20a0e69bfcaaa0ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c1011ab2c0a3cf196a3b58b296c57f34381fe37f81c70905f181e0f7f5c187(
    value: typing.Optional[RoleManagementPolicyActiveAssignmentRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3901d2192e8b18794b49ab4b77569df94ff84e4bfd15db54679d8a675987e73(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role_definition_id: builtins.str,
    scope: builtins.str,
    activation_rules: typing.Optional[typing.Union[RoleManagementPolicyActivationRules, typing.Dict[builtins.str, typing.Any]]] = None,
    active_assignment_rules: typing.Optional[typing.Union[RoleManagementPolicyActiveAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
    eligible_assignment_rules: typing.Optional[typing.Union[RoleManagementPolicyEligibleAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notification_rules: typing.Optional[typing.Union[RoleManagementPolicyNotificationRules, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[RoleManagementPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7863f00e4a694cb52633f6391b689ff5aef42c2fb201587ef9938be9279c80(
    *,
    expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expire_after: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77ad5e64ce313459c7581c24a741e4e81fa08c44441fb869f5a1adcb5407b4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692f8912f03ff5a2ba1dc0de97e95284c3ea839579917d5ccf6f1c6695f02a74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5670af07a216c9bad022c312aa26f6c8caf79de8b5ae093ad4357921f7e52fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab6ee61ea11eb7812c019f5dc593182117a7f1efb8a6522d84224df2565f763(
    value: typing.Optional[RoleManagementPolicyEligibleAssignmentRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77f9606393ac2667e9a8d93ce096c5439602b85c38f79707c9167ced893696c(
    *,
    active_assignments: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesActiveAssignments, typing.Dict[builtins.str, typing.Any]]] = None,
    eligible_activations: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleActivations, typing.Dict[builtins.str, typing.Any]]] = None,
    eligible_assignments: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleAssignments, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a6b00f92060b6b8f31b592a0b7204ce8c41a7ec3a4b151d6e764e24fc4d4d5(
    *,
    admin_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    approver_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    assignee_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36ba6b8aacdc5125670ad81aea16edefb83153d07a9ad236f067159116dc0c6(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fa0be3ab335862296c443ca281120170e9642328d2d371a80ca8d944ea7c7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bf32dcda731c78d89c5f6c25aca8e99641a20d79342a8077bae78b293ee3b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddfb631b05d4774381c655ada78174439b84c84cdf20a0d5b6267f720e60db4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0195657bf7040cc0d59da92ed458a291e6bd05e70135614a2d5208854ec871ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac8be4ce28819305975ad7b7b6cd97e73513a661f248cc1eb451e2117beedb6(
    value: typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f9abbfff2712ff78d4d8d1de52243a20909159b1992876db13e34fcf411d5a(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5406c254b8b045f6632c7f7fa030e6b77cb644fe787b9e4328b9fc718ffd33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf92a6a97c4b9791c3645c1fabc60f903ae083649bfdd12ddb4b1e3561276303(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a307f10d2d45750214da1e5bc87010e3c7c8f5a0474123cb0d4a18524be9c27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06820c753880777d4ef7e51aa394cbc1953ad271e79c8b09235426ef62eb9f0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb713aab94cf1bacb051b8f5eb47a868d51bb8a8c1947c51a5d2a0a83eb9fd5(
    value: typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077a3f85d93203115317a88c27f78650f960619f974d2df410ec41f19b62176b(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b240453fc1291830479dd6ddc8abb7cb114e47e4eff98d7acb8bd7f99507e52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477b46ba57b4cad5dd34e81fc19416c80b8af05a3112754247768bff90247876(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03afa4068544dbc9c34b56849f3bdec00834df5397d634d044395eaef7f4957a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41d45f4a7f259fa37d122d3fe162b2db1931fb1315f170a830f570d4d94ebe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9451fdc2ddf347497a52967de8e8f3cdcf0d27243601e1f3162a6e1237254f2(
    value: typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2cc8ed3621a07b386878b25818c0b5ddb2cbe0dff141c954eb2fc09e6bbcf4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb54d3ef71fa78cbfd9c3e126854b45cc353b7b55cb169d0d4cd0aaa4816e7bf(
    value: typing.Optional[RoleManagementPolicyNotificationRulesActiveAssignments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c508e24250072d0414d26933018f785871f0ad99d8d7c308ca297eaff04a85(
    *,
    admin_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    approver_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    assignee_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c8f0622f109f47e2ad782a46f92b83ec3c581680a4392108b891d614f8a7e0(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2badc3b782f82c0152e3011b47f579794286b1c5bf5adc5260bd50e58f05d5be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3e6a26efe40ba97d59b1dadd2ebb8fcca783b2e0b6f5f1aaa9d85ae2f83ede(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e458529de294a08ae6ca7a299ffe0b7d6782d695421435e19f74d2a76813ba3b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35a76774dbfe29e33cf230d95449403b3994ad335a9a911f81023eafab62098(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7735e10f1c6f5358e43361ada8cc8a6cf3130f14ddaae8e0fb40e04ef37fb44d(
    value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dd071e7ca289636bf96818c5b9ee5fd7ec46a36d45749fd293b2e8977bbbd3(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88df8e85460daa6c8cbd3b2d46fea435d4dcadf153fc960e2364fd8891e7deac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2170420d0c7b245383bd047e1e9c25ae15a5f0a1fe6a7eb920153d564b6247c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e20b560b5d069a9736bf8aea2d9ccc686819619a7e2fd267a4d0948975b3ff8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e5ff12ae8109ec0288563ceb132cbeae3976563c6d8ba8168113d237709f74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c45b65b7b08bb7cb16b30a3f27da2d211c024c1ed5799c5aa8874a593e6d068(
    value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae26b7e08a17b6e5e89e657b6b07cf88895e9ac2b8384e83fe8dbc2c33d633f(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721d8ee2087ad10bf2d85fe76b093985d41dcd819a185c2f8b4b4289677f5be9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c9af9121b9a450ff9993bc42fd6068915155f47685ce93e4f8e8b44f5d843f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e39d6088e80c86d7e98740fa76a174bee90450ca8ff5ec233d1571bab59be72(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36ed28e41f6ea308bab7741de8cf0ac50f42b4c05e8003f1d5228fafb4f72e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92930c7d3de072a6c5e39766d935d4d857e4d963a7505b8cf6c1ebd31e960a1f(
    value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12cf01d75a0227e1bef80c82bc3757da2ad3f66198eaa9537e386e21d74beb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d957eeee9b7a6c9002e935921d2958ccbb1fa2ea3a8e0024918c79a92ece02(
    value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleActivations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e910b43a32824ba097d8914610075edc3982704540a55fbe9fbe629bf55e201(
    *,
    admin_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    approver_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    assignee_notifications: typing.Optional[typing.Union[RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b774d51e05fd6f3e0ec1d3d9b3ddf7dfe77860a1186f5363d0a4c0bad42c31b(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c6d819b04299eac8cdf2d686f4f90dd4697de48e8f07db97264c9742e1be30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce20ce683e70bee428c345c592e06baee7d9360b8cac7af6c9e92030b668376(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3a659ed5d2ac12a8233476c6a70bdb87492f4ba7fa4ddf9aec95297cf0c449(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0ccf0083c9788155c9fced2764ad70c1e03174cc35d860d5cbd329e7d5522c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087779bbd6f5e47e734168918f4a689a68c02f1609cfba6d822c85266570e25d(
    value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab917d4781f7b23131af7123ffbec83d6a570d49a9b5845bb01f9d36a31be28(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77376f08e0aa6d0d576b15c6eadc51c9fea1363ef769ee6c5f529aae63d26aef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6285e0f6fe85d757cf3d978a65dfa4bb6b29fcd3ccc8f1891f7a370f849e01ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41eea8eab13f7020f5759ee999f369f66663e3213b6515d0292858645756a8c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffad0d57bc2bbbbc0131a72d5d2046ab65efddfe121dcd9a6531c1e86227ad1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08cd72ea3978346f01e5f77c27a8d7d6c0127f41a2d95ef8d1450d0df962df49(
    value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042a0d8c13e27d8ccac65d28880b3fbeb217ea462b44d6017328766bd450e28d(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d43de7f1f780bc23dd6f74d8a6443c21813f7e51ee540489a95f08b18cec57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195b735ef7b0b7e226b980040b443760c4ed3dc1d5fd2be821d5899ea0094a05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010e5be67714d5256b33562e7a2059cd3027ff0d53a0ee80879327612a51890a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2885e9d15265fe3ae63001ad33b58d6675db68c0a66ad7d59e7102070929e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8f3e7f4b19b1be9631e02bbdc27aa7fd1096ddf12dc6fb67c24fe383433c85(
    value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17dc5bfca50270548a1ed680b2054c0b998a26fa25aacd15b345c65526047df7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1667dcfa3774ffa860d1f67f0c009df9f22b87a5e205b35a58921e31319bc88(
    value: typing.Optional[RoleManagementPolicyNotificationRulesEligibleAssignments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a34943a9078c11a0602ca9dbedeb5e0fd601c3e2d86df00956a47a34843a2c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c008734465556b2e7b05e3cc82f2bfb605a18b29cd81ef7da59932fdd28f4a(
    value: typing.Optional[RoleManagementPolicyNotificationRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c15fd84a7104e05e29b5c7b5ac13c2e2213b475dc59332038b6d5d3a5b0ceb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325912e7bc65a08bfbc1f43ea8e24177e1a3618ed68b27317295e9c3b1201d49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618f611eeaf92b0d3ee54704b60d587c5b16f481c7a9bc0b7782a4a7a5712f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca89866bccb12811450fe1a1824a32131e506c734d2770628e68e96c48c65bd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bea80d7fb343afd0a17cbf4eb0790c5a49bc3d26b15a744d71075b42aeb8fe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0f63bc5a144e35143d69657af74cf9dc8eeca72f307ca104c4a0da1b56077c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9246d83515060da189896eac0e363a0670e92f7cbaffdebfc6e5535f7c870e4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RoleManagementPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
