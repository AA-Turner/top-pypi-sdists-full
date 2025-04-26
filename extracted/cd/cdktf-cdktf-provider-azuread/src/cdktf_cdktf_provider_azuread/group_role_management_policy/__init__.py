r'''
# `azuread_group_role_management_policy`

Refer to the Terraform Registry for docs: [`azuread_group_role_management_policy`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy).
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


class GroupRoleManagementPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy azuread_group_role_management_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group_id: builtins.str,
        role_id: builtins.str,
        activation_rules: typing.Optional[typing.Union["GroupRoleManagementPolicyActivationRules", typing.Dict[builtins.str, typing.Any]]] = None,
        active_assignment_rules: typing.Optional[typing.Union["GroupRoleManagementPolicyActiveAssignmentRules", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_assignment_rules: typing.Optional[typing.Union["GroupRoleManagementPolicyEligibleAssignmentRules", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notification_rules: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRules", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GroupRoleManagementPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy azuread_group_role_management_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group_id: ID of the group to which this policy is assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#group_id GroupRoleManagementPolicy#group_id}
        :param role_id: The ID of the role of this policy to the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#role_id GroupRoleManagementPolicy#role_id}
        :param activation_rules: activation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#activation_rules GroupRoleManagementPolicy#activation_rules}
        :param active_assignment_rules: active_assignment_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#active_assignment_rules GroupRoleManagementPolicy#active_assignment_rules}
        :param eligible_assignment_rules: eligible_assignment_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_assignment_rules GroupRoleManagementPolicy#eligible_assignment_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#id GroupRoleManagementPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_rules: notification_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_rules GroupRoleManagementPolicy#notification_rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#timeouts GroupRoleManagementPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62993a43335f5e90474e0591df569d21ff40596c6a85f9936e1bfeb5fe0da312)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GroupRoleManagementPolicyConfig(
            group_id=group_id,
            role_id=role_id,
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
        '''Generates CDKTF code for importing a GroupRoleManagementPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GroupRoleManagementPolicy to import.
        :param import_from_id: The id of the existing GroupRoleManagementPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GroupRoleManagementPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e826cc6d365e7397e9b385c2bd9a803f7f93d6fdd585205da026755f20867a49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActivationRules")
    def put_activation_rules(
        self,
        *,
        approval_stage: typing.Optional[typing.Union["GroupRoleManagementPolicyActivationRulesApprovalStage", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_duration: typing.Optional[builtins.str] = None,
        require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_conditional_access_authentication_context: typing.Optional[builtins.str] = None,
        require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_stage: approval_stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approval_stage GroupRoleManagementPolicy#approval_stage}
        :param maximum_duration: The time after which the an activation can be valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#maximum_duration GroupRoleManagementPolicy#maximum_duration}
        :param require_approval: Whether an approval is required for activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_approval GroupRoleManagementPolicy#require_approval}
        :param required_conditional_access_authentication_context: Whether a conditional access context is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#required_conditional_access_authentication_context GroupRoleManagementPolicy#required_conditional_access_authentication_context}
        :param require_justification: Whether a justification is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_justification GroupRoleManagementPolicy#require_justification}
        :param require_multifactor_authentication: Whether multi-factor authentication is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_multifactor_authentication GroupRoleManagementPolicy#require_multifactor_authentication}
        :param require_ticket_info: Whether ticket information is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_ticket_info GroupRoleManagementPolicy#require_ticket_info}
        '''
        value = GroupRoleManagementPolicyActivationRules(
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
        :param expiration_required: Must the assignment have an expiry date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expiration_required GroupRoleManagementPolicy#expiration_required}
        :param expire_after: The duration after which assignments expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expire_after GroupRoleManagementPolicy#expire_after}
        :param require_justification: Whether a justification is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_justification GroupRoleManagementPolicy#require_justification}
        :param require_multifactor_authentication: Whether multi-factor authentication is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_multifactor_authentication GroupRoleManagementPolicy#require_multifactor_authentication}
        :param require_ticket_info: Whether ticket information is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_ticket_info GroupRoleManagementPolicy#require_ticket_info}
        '''
        value = GroupRoleManagementPolicyActiveAssignmentRules(
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
        :param expiration_required: Must the assignment have an expiry date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expiration_required GroupRoleManagementPolicy#expiration_required}
        :param expire_after: The duration after which assignments expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expire_after GroupRoleManagementPolicy#expire_after}
        '''
        value = GroupRoleManagementPolicyEligibleAssignmentRules(
            expiration_required=expiration_required, expire_after=expire_after
        )

        return typing.cast(None, jsii.invoke(self, "putEligibleAssignmentRules", [value]))

    @jsii.member(jsii_name="putNotificationRules")
    def put_notification_rules(
        self,
        *,
        active_assignments: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesActiveAssignments", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_activations: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleActivations", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_assignments: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleAssignments", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param active_assignments: active_assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#active_assignments GroupRoleManagementPolicy#active_assignments}
        :param eligible_activations: eligible_activations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_activations GroupRoleManagementPolicy#eligible_activations}
        :param eligible_assignments: eligible_assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_assignments GroupRoleManagementPolicy#eligible_assignments}
        '''
        value = GroupRoleManagementPolicyNotificationRules(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#create GroupRoleManagementPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#delete GroupRoleManagementPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#read GroupRoleManagementPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#update GroupRoleManagementPolicy#update}.
        '''
        value = GroupRoleManagementPolicyTimeouts(
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
    def activation_rules(
        self,
    ) -> "GroupRoleManagementPolicyActivationRulesOutputReference":
        return typing.cast("GroupRoleManagementPolicyActivationRulesOutputReference", jsii.get(self, "activationRules"))

    @builtins.property
    @jsii.member(jsii_name="activeAssignmentRules")
    def active_assignment_rules(
        self,
    ) -> "GroupRoleManagementPolicyActiveAssignmentRulesOutputReference":
        return typing.cast("GroupRoleManagementPolicyActiveAssignmentRulesOutputReference", jsii.get(self, "activeAssignmentRules"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAssignmentRules")
    def eligible_assignment_rules(
        self,
    ) -> "GroupRoleManagementPolicyEligibleAssignmentRulesOutputReference":
        return typing.cast("GroupRoleManagementPolicyEligibleAssignmentRulesOutputReference", jsii.get(self, "eligibleAssignmentRules"))

    @builtins.property
    @jsii.member(jsii_name="notificationRules")
    def notification_rules(
        self,
    ) -> "GroupRoleManagementPolicyNotificationRulesOutputReference":
        return typing.cast("GroupRoleManagementPolicyNotificationRulesOutputReference", jsii.get(self, "notificationRules"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GroupRoleManagementPolicyTimeoutsOutputReference":
        return typing.cast("GroupRoleManagementPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="activationRulesInput")
    def activation_rules_input(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyActivationRules"]:
        return typing.cast(typing.Optional["GroupRoleManagementPolicyActivationRules"], jsii.get(self, "activationRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="activeAssignmentRulesInput")
    def active_assignment_rules_input(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyActiveAssignmentRules"]:
        return typing.cast(typing.Optional["GroupRoleManagementPolicyActiveAssignmentRules"], jsii.get(self, "activeAssignmentRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAssignmentRulesInput")
    def eligible_assignment_rules_input(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyEligibleAssignmentRules"]:
        return typing.cast(typing.Optional["GroupRoleManagementPolicyEligibleAssignmentRules"], jsii.get(self, "eligibleAssignmentRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationRulesInput")
    def notification_rules_input(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRules"]:
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRules"], jsii.get(self, "notificationRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="roleIdInput")
    def role_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GroupRoleManagementPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GroupRoleManagementPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0c569331ecfb04e8d47a0a977200e9191d6f9cd1fe2a40c7aba4c0c5fb7fedc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa64bb5cc7d06f9fecb92c131ed8edb0ebe5e664bca71bd6caa488356b4861d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @role_id.setter
    def role_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984f0c82a78013462aa9be99b616bb14cfa7bb9c50da088c85520a302bce4257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActivationRules",
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
class GroupRoleManagementPolicyActivationRules:
    def __init__(
        self,
        *,
        approval_stage: typing.Optional[typing.Union["GroupRoleManagementPolicyActivationRulesApprovalStage", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_duration: typing.Optional[builtins.str] = None,
        require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_conditional_access_authentication_context: typing.Optional[builtins.str] = None,
        require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param approval_stage: approval_stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approval_stage GroupRoleManagementPolicy#approval_stage}
        :param maximum_duration: The time after which the an activation can be valid for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#maximum_duration GroupRoleManagementPolicy#maximum_duration}
        :param require_approval: Whether an approval is required for activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_approval GroupRoleManagementPolicy#require_approval}
        :param required_conditional_access_authentication_context: Whether a conditional access context is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#required_conditional_access_authentication_context GroupRoleManagementPolicy#required_conditional_access_authentication_context}
        :param require_justification: Whether a justification is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_justification GroupRoleManagementPolicy#require_justification}
        :param require_multifactor_authentication: Whether multi-factor authentication is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_multifactor_authentication GroupRoleManagementPolicy#require_multifactor_authentication}
        :param require_ticket_info: Whether ticket information is required during activation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_ticket_info GroupRoleManagementPolicy#require_ticket_info}
        '''
        if isinstance(approval_stage, dict):
            approval_stage = GroupRoleManagementPolicyActivationRulesApprovalStage(**approval_stage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3ff73bda83bfa19d32a7bbb2d1f1efca7da71f7a36453bad6f6a496cdc68be)
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
    ) -> typing.Optional["GroupRoleManagementPolicyActivationRulesApprovalStage"]:
        '''approval_stage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approval_stage GroupRoleManagementPolicy#approval_stage}
        '''
        result = self._values.get("approval_stage")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyActivationRulesApprovalStage"], result)

    @builtins.property
    def maximum_duration(self) -> typing.Optional[builtins.str]:
        '''The time after which the an activation can be valid for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#maximum_duration GroupRoleManagementPolicy#maximum_duration}
        '''
        result = self._values.get("maximum_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether an approval is required for activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_approval GroupRoleManagementPolicy#require_approval}
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_conditional_access_authentication_context(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Whether a conditional access context is required during activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#required_conditional_access_authentication_context GroupRoleManagementPolicy#required_conditional_access_authentication_context}
        '''
        result = self._values.get("required_conditional_access_authentication_context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_justification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a justification is required during activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_justification GroupRoleManagementPolicy#require_justification}
        '''
        result = self._values.get("require_justification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_multifactor_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether multi-factor authentication is required during activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_multifactor_authentication GroupRoleManagementPolicy#require_multifactor_authentication}
        '''
        result = self._values.get("require_multifactor_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_ticket_info(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether ticket information is required during activation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_ticket_info GroupRoleManagementPolicy#require_ticket_info}
        '''
        result = self._values.get("require_ticket_info")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyActivationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActivationRulesApprovalStage",
    jsii_struct_bases=[],
    name_mapping={"primary_approver": "primaryApprover"},
)
class GroupRoleManagementPolicyActivationRulesApprovalStage:
    def __init__(
        self,
        *,
        primary_approver: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param primary_approver: primary_approver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#primary_approver GroupRoleManagementPolicy#primary_approver}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ccbb44c8f89ecb62d1b29c024bdc5ec6804d60cd8f4b972e290ed864e50d42)
            check_type(argname="argument primary_approver", value=primary_approver, expected_type=type_hints["primary_approver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primary_approver": primary_approver,
        }

    @builtins.property
    def primary_approver(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover"]]:
        '''primary_approver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#primary_approver GroupRoleManagementPolicy#primary_approver}
        '''
        result = self._values.get("primary_approver")
        assert result is not None, "Required property 'primary_approver' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyActivationRulesApprovalStage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyActivationRulesApprovalStageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActivationRulesApprovalStageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fcad0b554abeb21b427af4a8e135ef91509db51b30ffc42e1ef7da931307a35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrimaryApprover")
    def put_primary_approver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c3d96aff171ae2753d2bb110eb90b2f0d58b59c07df86143f491c0246df892b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrimaryApprover", [value]))

    @builtins.property
    @jsii.member(jsii_name="primaryApprover")
    def primary_approver(
        self,
    ) -> "GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList":
        return typing.cast("GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList", jsii.get(self, "primaryApprover"))

    @builtins.property
    @jsii.member(jsii_name="primaryApproverInput")
    def primary_approver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover"]]], jsii.get(self, "primaryApproverInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyActivationRulesApprovalStage]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyActivationRulesApprovalStage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyActivationRulesApprovalStage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdda16417c838ea338de703ea2cefde93d9e8bd7c956a5c8965be84c5b1c51b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover",
    jsii_struct_bases=[],
    name_mapping={"object_id": "objectId", "type": "type"},
)
class GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover:
    def __init__(
        self,
        *,
        object_id: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_id: The ID of the object to act as an approver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#object_id GroupRoleManagementPolicy#object_id}
        :param type: The type of object acting as an approver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#type GroupRoleManagementPolicy#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc459bba6d47b9d0c3cb989f54413f6b8cd7c02660d5b4b23977341d6c4e5829)
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id": object_id,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def object_id(self) -> builtins.str:
        '''The ID of the object to act as an approver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#object_id GroupRoleManagementPolicy#object_id}
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of object acting as an approver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#type GroupRoleManagementPolicy#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99827ef8959a0295df3d499c213ab120f938dd8f0cfa054b012ced868a2a5064)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574cd9086b32bd6edfe239da59ce60d2f88ca0b9b6772a477a9e331f29f0229e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036d66901485f67f225a43863871f50d1189dbd1a038a0a7b538ddc9b4ec80ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6e8c604dd50b18cbe870fe07031417503b969a0f06ad27e1621b93a021e8e72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1eda8707f8955d373be18e8c8a9b37fd8c022181cf962007d327d2c6a4f4e4cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f837bd95067d0b41f89a14c73a40ca77d9573b0b7aa64f51cb45b31277e638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b97dccc2d3f499cd33a9c58e2118e09fdf3051aaa7ac33aa5f532bfdf7f5613)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__378e65a14d50f6c01bbcc209bca8b995aa127123c90f4e77aec0574db0550b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010af9e6e3a691ad19e51a8f972fef5eaa4460e3274a1e69e673788a8bfdb1dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283575384538afa42ef312b7ccecb2e7f187c829ccab72811c36184987ef11d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GroupRoleManagementPolicyActivationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActivationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8641c86ea353d6ce74bc1ba671b9194d0b5eb1ba8da1f12666de209349679048)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApprovalStage")
    def put_approval_stage(
        self,
        *,
        primary_approver: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param primary_approver: primary_approver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#primary_approver GroupRoleManagementPolicy#primary_approver}
        '''
        value = GroupRoleManagementPolicyActivationRulesApprovalStage(
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
    ) -> GroupRoleManagementPolicyActivationRulesApprovalStageOutputReference:
        return typing.cast(GroupRoleManagementPolicyActivationRulesApprovalStageOutputReference, jsii.get(self, "approvalStage"))

    @builtins.property
    @jsii.member(jsii_name="approvalStageInput")
    def approval_stage_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyActivationRulesApprovalStage]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyActivationRulesApprovalStage], jsii.get(self, "approvalStageInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__64f75c0c1d875ec2c010031993aa07f1c188061239fc87b0684960b7e3cccaef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68db22a2d2270a5de5dbc8702eafb1c100681e2791ca351da8a927faeb38a337)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cddfc18c82c4080d60cab91986c98efbba86a074990b5b2830ab78b82900cf17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a79654b20ec44f2fe08edae6fb1ab0b2e2b6f67792c8c56ad964463761f7b171)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7510207ee380224855735d849fcd164401cda11806bc10302cfab0007f0e4e63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b96f6607806e5595f7c77776759a44438bc3f40d301f97cae05553a113cd730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireTicketInfo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyActivationRules]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyActivationRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyActivationRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85582e0a948f1b720624c70e9eabc7cd9e02b403c8b4d824b42d1fafbb223d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActiveAssignmentRules",
    jsii_struct_bases=[],
    name_mapping={
        "expiration_required": "expirationRequired",
        "expire_after": "expireAfter",
        "require_justification": "requireJustification",
        "require_multifactor_authentication": "requireMultifactorAuthentication",
        "require_ticket_info": "requireTicketInfo",
    },
)
class GroupRoleManagementPolicyActiveAssignmentRules:
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
        :param expiration_required: Must the assignment have an expiry date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expiration_required GroupRoleManagementPolicy#expiration_required}
        :param expire_after: The duration after which assignments expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expire_after GroupRoleManagementPolicy#expire_after}
        :param require_justification: Whether a justification is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_justification GroupRoleManagementPolicy#require_justification}
        :param require_multifactor_authentication: Whether multi-factor authentication is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_multifactor_authentication GroupRoleManagementPolicy#require_multifactor_authentication}
        :param require_ticket_info: Whether ticket information is required to make an assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_ticket_info GroupRoleManagementPolicy#require_ticket_info}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee7099acc0135e943382e2abff07ce6a5ee0113101f8d0035cc4c79751b2c02)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expiration_required GroupRoleManagementPolicy#expiration_required}
        '''
        result = self._values.get("expiration_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expire_after(self) -> typing.Optional[builtins.str]:
        '''The duration after which assignments expire.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expire_after GroupRoleManagementPolicy#expire_after}
        '''
        result = self._values.get("expire_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_justification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a justification is required to make an assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_justification GroupRoleManagementPolicy#require_justification}
        '''
        result = self._values.get("require_justification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_multifactor_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether multi-factor authentication is required to make an assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_multifactor_authentication GroupRoleManagementPolicy#require_multifactor_authentication}
        '''
        result = self._values.get("require_multifactor_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_ticket_info(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether ticket information is required to make an assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#require_ticket_info GroupRoleManagementPolicy#require_ticket_info}
        '''
        result = self._values.get("require_ticket_info")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyActiveAssignmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyActiveAssignmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyActiveAssignmentRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcd44b39fd5abca3cf6a560f7ddc550b2f782fcbf3d25d9676d7a552981bd743)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d17f6460ae0ad57aec9f142d93e9a28e5e47a6457835ddef2b211f250a2bb846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expireAfter")
    def expire_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireAfter"))

    @expire_after.setter
    def expire_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2102955168a9676ab38b84d1a30dfba1f24df4973ff987eb8732b80db14f593f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7fa2dd32db76074039480fb72ab39708a7e8826ea3cb798b4192040756a6892)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a2efdae3c842572c8a614ca113f117d97c9ed252f44304240b7b722ef56906a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__947ffea549ab952de81be7a6d5360c5fa0955605f5e94bce27cc9f165992628f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireTicketInfo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyActiveAssignmentRules]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyActiveAssignmentRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyActiveAssignmentRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a082f04cab491b9c3c54ba05855ecc34750ffb2d8c28ceea905d7638a7ec021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "group_id": "groupId",
        "role_id": "roleId",
        "activation_rules": "activationRules",
        "active_assignment_rules": "activeAssignmentRules",
        "eligible_assignment_rules": "eligibleAssignmentRules",
        "id": "id",
        "notification_rules": "notificationRules",
        "timeouts": "timeouts",
    },
)
class GroupRoleManagementPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        group_id: builtins.str,
        role_id: builtins.str,
        activation_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyActivationRules, typing.Dict[builtins.str, typing.Any]]] = None,
        active_assignment_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyActiveAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_assignment_rules: typing.Optional[typing.Union["GroupRoleManagementPolicyEligibleAssignmentRules", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        notification_rules: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRules", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GroupRoleManagementPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group_id: ID of the group to which this policy is assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#group_id GroupRoleManagementPolicy#group_id}
        :param role_id: The ID of the role of this policy to the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#role_id GroupRoleManagementPolicy#role_id}
        :param activation_rules: activation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#activation_rules GroupRoleManagementPolicy#activation_rules}
        :param active_assignment_rules: active_assignment_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#active_assignment_rules GroupRoleManagementPolicy#active_assignment_rules}
        :param eligible_assignment_rules: eligible_assignment_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_assignment_rules GroupRoleManagementPolicy#eligible_assignment_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#id GroupRoleManagementPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_rules: notification_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_rules GroupRoleManagementPolicy#notification_rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#timeouts GroupRoleManagementPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(activation_rules, dict):
            activation_rules = GroupRoleManagementPolicyActivationRules(**activation_rules)
        if isinstance(active_assignment_rules, dict):
            active_assignment_rules = GroupRoleManagementPolicyActiveAssignmentRules(**active_assignment_rules)
        if isinstance(eligible_assignment_rules, dict):
            eligible_assignment_rules = GroupRoleManagementPolicyEligibleAssignmentRules(**eligible_assignment_rules)
        if isinstance(notification_rules, dict):
            notification_rules = GroupRoleManagementPolicyNotificationRules(**notification_rules)
        if isinstance(timeouts, dict):
            timeouts = GroupRoleManagementPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19658290548778368e430d18ee77f220195b5300f6920db2d879bdfba8f374b4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument role_id", value=role_id, expected_type=type_hints["role_id"])
            check_type(argname="argument activation_rules", value=activation_rules, expected_type=type_hints["activation_rules"])
            check_type(argname="argument active_assignment_rules", value=active_assignment_rules, expected_type=type_hints["active_assignment_rules"])
            check_type(argname="argument eligible_assignment_rules", value=eligible_assignment_rules, expected_type=type_hints["eligible_assignment_rules"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_rules", value=notification_rules, expected_type=type_hints["notification_rules"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
            "role_id": role_id,
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
    def group_id(self) -> builtins.str:
        '''ID of the group to which this policy is assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#group_id GroupRoleManagementPolicy#group_id}
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_id(self) -> builtins.str:
        '''The ID of the role of this policy to the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#role_id GroupRoleManagementPolicy#role_id}
        '''
        result = self._values.get("role_id")
        assert result is not None, "Required property 'role_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activation_rules(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyActivationRules]:
        '''activation_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#activation_rules GroupRoleManagementPolicy#activation_rules}
        '''
        result = self._values.get("activation_rules")
        return typing.cast(typing.Optional[GroupRoleManagementPolicyActivationRules], result)

    @builtins.property
    def active_assignment_rules(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyActiveAssignmentRules]:
        '''active_assignment_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#active_assignment_rules GroupRoleManagementPolicy#active_assignment_rules}
        '''
        result = self._values.get("active_assignment_rules")
        return typing.cast(typing.Optional[GroupRoleManagementPolicyActiveAssignmentRules], result)

    @builtins.property
    def eligible_assignment_rules(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyEligibleAssignmentRules"]:
        '''eligible_assignment_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_assignment_rules GroupRoleManagementPolicy#eligible_assignment_rules}
        '''
        result = self._values.get("eligible_assignment_rules")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyEligibleAssignmentRules"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#id GroupRoleManagementPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_rules(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRules"]:
        '''notification_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_rules GroupRoleManagementPolicy#notification_rules}
        '''
        result = self._values.get("notification_rules")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRules"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GroupRoleManagementPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#timeouts GroupRoleManagementPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyEligibleAssignmentRules",
    jsii_struct_bases=[],
    name_mapping={
        "expiration_required": "expirationRequired",
        "expire_after": "expireAfter",
    },
)
class GroupRoleManagementPolicyEligibleAssignmentRules:
    def __init__(
        self,
        *,
        expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expire_after: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration_required: Must the assignment have an expiry date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expiration_required GroupRoleManagementPolicy#expiration_required}
        :param expire_after: The duration after which assignments expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expire_after GroupRoleManagementPolicy#expire_after}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea28738ab1e5159dc84aac60b7d218808846b93e77140c0daaaa257d4dbf49c3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expiration_required GroupRoleManagementPolicy#expiration_required}
        '''
        result = self._values.get("expiration_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expire_after(self) -> typing.Optional[builtins.str]:
        '''The duration after which assignments expire.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#expire_after GroupRoleManagementPolicy#expire_after}
        '''
        result = self._values.get("expire_after")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyEligibleAssignmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyEligibleAssignmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyEligibleAssignmentRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cde40e73b380fc718bf2fb57f4eae5fb6bd629ca87fa055b475c24052248539d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf68799661d9c9e034f84522848a3a9cebae4a3c6e3fa82610bbfc575ee8ac6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expireAfter")
    def expire_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireAfter"))

    @expire_after.setter
    def expire_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b129e4d11f95863d698828570428c3dde8a93e9284eddd7e50bc869378ebcf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyEligibleAssignmentRules]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyEligibleAssignmentRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyEligibleAssignmentRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300ce38f9b75430d00fc27655779ff3e871707a09fe3f05de71abcd7addfdaee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRules",
    jsii_struct_bases=[],
    name_mapping={
        "active_assignments": "activeAssignments",
        "eligible_activations": "eligibleActivations",
        "eligible_assignments": "eligibleAssignments",
    },
)
class GroupRoleManagementPolicyNotificationRules:
    def __init__(
        self,
        *,
        active_assignments: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesActiveAssignments", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_activations: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleActivations", typing.Dict[builtins.str, typing.Any]]] = None,
        eligible_assignments: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleAssignments", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param active_assignments: active_assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#active_assignments GroupRoleManagementPolicy#active_assignments}
        :param eligible_activations: eligible_activations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_activations GroupRoleManagementPolicy#eligible_activations}
        :param eligible_assignments: eligible_assignments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_assignments GroupRoleManagementPolicy#eligible_assignments}
        '''
        if isinstance(active_assignments, dict):
            active_assignments = GroupRoleManagementPolicyNotificationRulesActiveAssignments(**active_assignments)
        if isinstance(eligible_activations, dict):
            eligible_activations = GroupRoleManagementPolicyNotificationRulesEligibleActivations(**eligible_activations)
        if isinstance(eligible_assignments, dict):
            eligible_assignments = GroupRoleManagementPolicyNotificationRulesEligibleAssignments(**eligible_assignments)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4cb253e9ecd940ef9a8a22b1c7ec074b5e7a6686bfa018c95c10da73ba8285)
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
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesActiveAssignments"]:
        '''active_assignments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#active_assignments GroupRoleManagementPolicy#active_assignments}
        '''
        result = self._values.get("active_assignments")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesActiveAssignments"], result)

    @builtins.property
    def eligible_activations(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleActivations"]:
        '''eligible_activations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_activations GroupRoleManagementPolicy#eligible_activations}
        '''
        result = self._values.get("eligible_activations")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleActivations"], result)

    @builtins.property
    def eligible_assignments(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleAssignments"]:
        '''eligible_assignments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#eligible_assignments GroupRoleManagementPolicy#eligible_assignments}
        '''
        result = self._values.get("eligible_assignments")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleAssignments"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesActiveAssignments",
    jsii_struct_bases=[],
    name_mapping={
        "admin_notifications": "adminNotifications",
        "approver_notifications": "approverNotifications",
        "assignee_notifications": "assigneeNotifications",
    },
)
class GroupRoleManagementPolicyNotificationRulesActiveAssignments:
    def __init__(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        if isinstance(admin_notifications, dict):
            admin_notifications = GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications(**admin_notifications)
        if isinstance(approver_notifications, dict):
            approver_notifications = GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications(**approver_notifications)
        if isinstance(assignee_notifications, dict):
            assignee_notifications = GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications(**assignee_notifications)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c22a2f196372c8eae848af7da8b5fd76e97f4314c872a4f6d7001727f97d904)
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
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications"]:
        '''admin_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        '''
        result = self._values.get("admin_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications"], result)

    @builtins.property
    def approver_notifications(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications"]:
        '''approver_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        '''
        result = self._values.get("approver_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications"], result)

    @builtins.property
    def assignee_notifications(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications"]:
        '''assignee_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        result = self._values.get("assignee_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesActiveAssignments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bf39c453ab967151963e4113e2c779c5a425c1733874e716bf226adc1f337b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5533279f4ed7af62858a4b22e7b2504357e53f5bdd109e68feb92bf7bded54c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72474602bf3d4f89d6f5ef8fa3a9c26dff8e984e5ccdc1476ef744232061b507)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a6188024b118b72ebcfcce85e2f9ab63d28bdf6de4ef01c9a4099aa09602e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35738d9d2c92a980b40f896e0a7027e7fe52cc218f915581e24c282550641be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1130d8dd8bf3daa1001b074f01c454b71a80aa31bb89915e8246cda9d233df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42071a8d54e2120acffdf560848ccb616c66ba90c4dbcc749d35107c90156846)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc434ca1f53a58ef53ffec403370c465ec934ee2b7a9869f5c672a0698785b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2845011ee2e501dd00717835350d5dce06b4cc43e11c5e106f7d4eff0578330c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a07aa9901608b1e1cc744ac270af7b272ab9e102bfe7cbf695480441d6fd5f1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e04f31237bfe8717855c93f85e076505904fc3d332fdcef7712756ef144436b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe1446ebfe9c515ac4338fb96cd9d24ed041fa58016b5ffcc4a65401f3bd401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a16e7122ae60aac5f71391b4ebfe9b5ad03061a23f1323ebc0f22cd8d3f7c4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ee71ec1d031ca0a112b4c19bd9befd96ff8cf2134258ab4ff363f25c941598)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c123855b5e05f1ae4dea162d56e8f55bc9ce4e9ec575e3b309d33f9543e70fdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8467c6ac706781ce3a0755eb29c992148a78f897f3531906af55a7ce49d62dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c7bb1ef3a9a446e90ca3e3b203ad8faad736f36a2e389bfa0a7b2cb60d64a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b2d6656807d7fa2bda212952a00a8584fda2298c01707f0b9373eca6e5717e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GroupRoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b81431d7c88088d83e3906a1ba60420d18485432ec619edbee5e9b0a4c674e37)
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications(
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications(
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications(
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
    ) -> GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference, jsii.get(self, "adminNotifications"))

    @builtins.property
    @jsii.member(jsii_name="approverNotifications")
    def approver_notifications(
        self,
    ) -> GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference, jsii.get(self, "approverNotifications"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotifications")
    def assignee_notifications(
        self,
    ) -> GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference, jsii.get(self, "assigneeNotifications"))

    @builtins.property
    @jsii.member(jsii_name="adminNotificationsInput")
    def admin_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications], jsii.get(self, "adminNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="approverNotificationsInput")
    def approver_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications], jsii.get(self, "approverNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotificationsInput")
    def assignee_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications], jsii.get(self, "assigneeNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignments]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f571f9ba5dbcbc86578927013ee4d8aa01546f802bfe69ccbfa22f3d9edf314b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleActivations",
    jsii_struct_bases=[],
    name_mapping={
        "admin_notifications": "adminNotifications",
        "approver_notifications": "approverNotifications",
        "assignee_notifications": "assigneeNotifications",
    },
)
class GroupRoleManagementPolicyNotificationRulesEligibleActivations:
    def __init__(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        if isinstance(admin_notifications, dict):
            admin_notifications = GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications(**admin_notifications)
        if isinstance(approver_notifications, dict):
            approver_notifications = GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications(**approver_notifications)
        if isinstance(assignee_notifications, dict):
            assignee_notifications = GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications(**assignee_notifications)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49b50fe84c5a20fe4c101007fe132487f076966a642a59c19621bd1818b8178)
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
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications"]:
        '''admin_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        '''
        result = self._values.get("admin_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications"], result)

    @builtins.property
    def approver_notifications(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications"]:
        '''approver_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        '''
        result = self._values.get("approver_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications"], result)

    @builtins.property
    def assignee_notifications(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications"]:
        '''assignee_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        result = self._values.get("assignee_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesEligibleActivations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d5b1ee5f526a0e009636c49ad15ca4ecb1f11968c1bdd16461c15ed2b86fbd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec70bddf850a51b4ebc1f44e0b2d667fd3623f44297f0a3e38662208a039354c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29669ca39d0eba6cc5ce11f76750e9fea16db21c3ab882322f5394a8e89bcee7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a403ff9f8bddaa25e0c4571049c552983eae589ee4e7c6223e83c73e1596b48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743a47704e1dd3cb8b2aa89d3ca520b7b77b4fbfa5535560ab11e793830413fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1c7a12fd1dbf102d8e4ffd26e642af93430c89bee032941fd76258aa1840e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74592b3068962e784d9e17de750626c075d9cec22262ecdc214ea01e33a2aa2b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33ec941f795cdf1cea78563f112762e89d7df1c90dcc8132678182e6479cbd3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__caacdf3edbfa325a0299ac81ab68c7650aa5af3807133503aca322a9815f7607)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3251e6d312e398d44863dc27519534a0c30d8e46d9a4bdd22451c26c301d6e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b1bf863f91fd08817e74531110b5fd03dafb593b9175a0534b93fe35b67153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e433e05c962e23ceb021f31abfad412473eed5a091c7db4f188fa9d00333a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35c8d2ce45ca0ee320031edb1a8f3d39a7433c1ca1ba476a39bd026f47d96ad)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f977e98761f7f46cc2df189ef449d7a0d0538a0f2bb444da902db6a003e37835)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7102f5818687a45fcf23e74c93f1a98e5c18d55cf2e8d5421154064b041091f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8fc7e860ae70be688c458737f674cb9bc6bba84ad60f255ca92f5df3124d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826bb02908efbeab325f3a4b141260d4a48e3765599969860912f34b3713ae76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f57d7467b404904522aca697a33b81a56d635ad7652b8934f73930e4e15eb15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GroupRoleManagementPolicyNotificationRulesEligibleActivationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleActivationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f88fc2b49a4432cac9afed194e1fa68b59f38a7a5ee96c3a2cc1abc339c7e66d)
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications(
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications(
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications(
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
    ) -> GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference, jsii.get(self, "adminNotifications"))

    @builtins.property
    @jsii.member(jsii_name="approverNotifications")
    def approver_notifications(
        self,
    ) -> GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference, jsii.get(self, "approverNotifications"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotifications")
    def assignee_notifications(
        self,
    ) -> GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference, jsii.get(self, "assigneeNotifications"))

    @builtins.property
    @jsii.member(jsii_name="adminNotificationsInput")
    def admin_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications], jsii.get(self, "adminNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="approverNotificationsInput")
    def approver_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications], jsii.get(self, "approverNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotificationsInput")
    def assignee_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications], jsii.get(self, "assigneeNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivations]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae00b9b4c0ab44b942db8026e9ea99152ba082c6f1d3b5b5ccc0fd72cc828b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleAssignments",
    jsii_struct_bases=[],
    name_mapping={
        "admin_notifications": "adminNotifications",
        "approver_notifications": "approverNotifications",
        "assignee_notifications": "assigneeNotifications",
    },
)
class GroupRoleManagementPolicyNotificationRulesEligibleAssignments:
    def __init__(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        if isinstance(admin_notifications, dict):
            admin_notifications = GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications(**admin_notifications)
        if isinstance(approver_notifications, dict):
            approver_notifications = GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications(**approver_notifications)
        if isinstance(assignee_notifications, dict):
            assignee_notifications = GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications(**assignee_notifications)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e236caa9ca97c28601e68bc01673f36959de4ef753aa0cb2078a35b75b3b0d)
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
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications"]:
        '''admin_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        '''
        result = self._values.get("admin_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications"], result)

    @builtins.property
    def approver_notifications(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications"]:
        '''approver_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        '''
        result = self._values.get("approver_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications"], result)

    @builtins.property
    def assignee_notifications(
        self,
    ) -> typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications"]:
        '''assignee_notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        result = self._values.get("assignee_notifications")
        return typing.cast(typing.Optional["GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesEligibleAssignments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab067141e4a6306af12bf2631ff76c66334c0ae416d1dfea273b8f354db480dd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02b06103db55dbea632b5dddb6d523e19c4a77ed04e87c4f9186cf8eb090012a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9ad89b07ec073a3720981fd62f1d8df18ddf81bceedfb04104b2c42b4e00655)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85267c7277f835d585125f1c43ac95c869f30acba27a4f9bb75a003d7392816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e90d4685ec9f1778dfb4d902ef97430438fac6ce09a245addce5b931ea9771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b9f03076db0dc6bda6d47871b605f0d33b9ef8a1c05286734da8ec6f97e81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d6946969aa8f9180b9536a3e5521c019c1d2c41b6152a99b8e8c73e6d4dc17)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4665383a2758accfda22e324a2e123e386b97f863f939aec165f60b479dc41a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47999c6cdfef755292a1ad4938cf4e17e14f7642bed6e66983cadff1255054d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14442a72f47e0ba0e71a4c6412933117a4d0d68db884453973a8f44312c656fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb1bdef652b7c1c4ee5fa6af00b9202a1bf0ee671a43ce2456540f0ae818e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36f7eaf1b0303b53670c262f86f07b7959c7d0da175356f4807a4c0e609aafa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "default_recipients": "defaultRecipients",
        "notification_level": "notificationLevel",
        "additional_recipients": "additionalRecipients",
    },
)
class GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications:
    def __init__(
        self,
        *,
        default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_level: builtins.str,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbab6e0dcf141f0e081878b8c330e0c5402695e83313785ee1441380c62031f6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        '''
        result = self._values.get("default_recipients")
        assert result is not None, "Required property 'default_recipients' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_level(self) -> builtins.str:
        '''What level of notifications are sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        '''
        result = self._values.get("notification_level")
        assert result is not None, "Required property 'notification_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The additional recipients to notify.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bd1cbfdbe9b509305f71ed8fad3eccf10666826594e81a9fda867a4278fe5ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb7f2052fa22a5b633ebffb29e48d6b14c5b1193881ca63e7aeca1875757c336)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5c38fddd54cffb15c5aa4cfd3c8b54774814f4cdd32ba15d93a9d214e177498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationLevel")
    def notification_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationLevel"))

    @notification_level.setter
    def notification_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bd4efe880a0a17959347c554c03896ceca62e64f5d7a4d4a5aafcf227aba00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e4a79babb4dd293327d2ce9cb8439d379b46f2e761894fc1693d60e3098255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2349dee9a9305a08455becb3fe4d4643d88449141cc98031c8890c7f5c2ff886)
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications(
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications(
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
        :param default_recipients: Whether the default recipients are notified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#default_recipients GroupRoleManagementPolicy#default_recipients}
        :param notification_level: What level of notifications are sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#notification_level GroupRoleManagementPolicy#notification_level}
        :param additional_recipients: The additional recipients to notify. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#additional_recipients GroupRoleManagementPolicy#additional_recipients}
        '''
        value = GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications(
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
    ) -> GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference, jsii.get(self, "adminNotifications"))

    @builtins.property
    @jsii.member(jsii_name="approverNotifications")
    def approver_notifications(
        self,
    ) -> GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference, jsii.get(self, "approverNotifications"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotifications")
    def assignee_notifications(
        self,
    ) -> GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference, jsii.get(self, "assigneeNotifications"))

    @builtins.property
    @jsii.member(jsii_name="adminNotificationsInput")
    def admin_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications], jsii.get(self, "adminNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="approverNotificationsInput")
    def approver_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications], jsii.get(self, "approverNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="assigneeNotificationsInput")
    def assignee_notifications_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications], jsii.get(self, "assigneeNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignments]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1faa0a740e895eb1873a83be4d93e24b1b0a516a235957688174cfe6ce5cf4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GroupRoleManagementPolicyNotificationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyNotificationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ead77107cc84a90cc4142fa8dfb30ed93f4511f09843f2b57d67005226b8afa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveAssignments")
    def put_active_assignments(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        value = GroupRoleManagementPolicyNotificationRulesActiveAssignments(
            admin_notifications=admin_notifications,
            approver_notifications=approver_notifications,
            assignee_notifications=assignee_notifications,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveAssignments", [value]))

    @jsii.member(jsii_name="putEligibleActivations")
    def put_eligible_activations(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        value = GroupRoleManagementPolicyNotificationRulesEligibleActivations(
            admin_notifications=admin_notifications,
            approver_notifications=approver_notifications,
            assignee_notifications=assignee_notifications,
        )

        return typing.cast(None, jsii.invoke(self, "putEligibleActivations", [value]))

    @jsii.member(jsii_name="putEligibleAssignments")
    def put_eligible_assignments(
        self,
        *,
        admin_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        approver_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        assignee_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param admin_notifications: admin_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#admin_notifications GroupRoleManagementPolicy#admin_notifications}
        :param approver_notifications: approver_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#approver_notifications GroupRoleManagementPolicy#approver_notifications}
        :param assignee_notifications: assignee_notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#assignee_notifications GroupRoleManagementPolicy#assignee_notifications}
        '''
        value = GroupRoleManagementPolicyNotificationRulesEligibleAssignments(
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
    ) -> GroupRoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference, jsii.get(self, "activeAssignments"))

    @builtins.property
    @jsii.member(jsii_name="eligibleActivations")
    def eligible_activations(
        self,
    ) -> GroupRoleManagementPolicyNotificationRulesEligibleActivationsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesEligibleActivationsOutputReference, jsii.get(self, "eligibleActivations"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAssignments")
    def eligible_assignments(
        self,
    ) -> GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference:
        return typing.cast(GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference, jsii.get(self, "eligibleAssignments"))

    @builtins.property
    @jsii.member(jsii_name="activeAssignmentsInput")
    def active_assignments_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignments]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignments], jsii.get(self, "activeAssignmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleActivationsInput")
    def eligible_activations_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivations]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivations], jsii.get(self, "eligibleActivationsInput"))

    @builtins.property
    @jsii.member(jsii_name="eligibleAssignmentsInput")
    def eligible_assignments_input(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignments]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignments], jsii.get(self, "eligibleAssignmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GroupRoleManagementPolicyNotificationRules]:
        return typing.cast(typing.Optional[GroupRoleManagementPolicyNotificationRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GroupRoleManagementPolicyNotificationRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0647a920f0782f8274425afd59a1dd48dd9cd2d4bcfa4f0fc9f6572140194a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class GroupRoleManagementPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#create GroupRoleManagementPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#delete GroupRoleManagementPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#read GroupRoleManagementPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#update GroupRoleManagementPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42fb93b9d910d8f346d63d58772896d81bd3cfd6e9181d6fba0d2835271bcdc3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#create GroupRoleManagementPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#delete GroupRoleManagementPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#read GroupRoleManagementPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/group_role_management_policy#update GroupRoleManagementPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleManagementPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupRoleManagementPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.groupRoleManagementPolicy.GroupRoleManagementPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83787a3e4d9697277ed1f8fc3c055664f7f3fa11e6a8287b4b4634f463f60267)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c83def158f4f68bac779bd444f74d3c1b50878ac39922cdfe4100597c7e4cba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18254036e0edb97c61c173a6845313bfb9ff988062a63d779016645a546ae9a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08f2e55dc76438ac198ee38c0e9bbe0dd33de957bc8a7d97d9f3212a9ae0bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0689937e935044fdfab816d8e6347bef9fdcb21d3d031e7b883032cdae451c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupRoleManagementPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupRoleManagementPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupRoleManagementPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbcd4d6cd8dc85d5b64dd371a8bd4b99833c72b8948cae653228eed4799666af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GroupRoleManagementPolicy",
    "GroupRoleManagementPolicyActivationRules",
    "GroupRoleManagementPolicyActivationRulesApprovalStage",
    "GroupRoleManagementPolicyActivationRulesApprovalStageOutputReference",
    "GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover",
    "GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverList",
    "GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApproverOutputReference",
    "GroupRoleManagementPolicyActivationRulesOutputReference",
    "GroupRoleManagementPolicyActiveAssignmentRules",
    "GroupRoleManagementPolicyActiveAssignmentRulesOutputReference",
    "GroupRoleManagementPolicyConfig",
    "GroupRoleManagementPolicyEligibleAssignmentRules",
    "GroupRoleManagementPolicyEligibleAssignmentRulesOutputReference",
    "GroupRoleManagementPolicyNotificationRules",
    "GroupRoleManagementPolicyNotificationRulesActiveAssignments",
    "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications",
    "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications",
    "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications",
    "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesActiveAssignmentsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesEligibleActivations",
    "GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications",
    "GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications",
    "GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications",
    "GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesEligibleActivationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesEligibleAssignments",
    "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications",
    "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications",
    "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications",
    "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotificationsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsOutputReference",
    "GroupRoleManagementPolicyNotificationRulesOutputReference",
    "GroupRoleManagementPolicyTimeouts",
    "GroupRoleManagementPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__62993a43335f5e90474e0591df569d21ff40596c6a85f9936e1bfeb5fe0da312(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group_id: builtins.str,
    role_id: builtins.str,
    activation_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyActivationRules, typing.Dict[builtins.str, typing.Any]]] = None,
    active_assignment_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyActiveAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
    eligible_assignment_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyEligibleAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notification_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRules, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GroupRoleManagementPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e826cc6d365e7397e9b385c2bd9a803f7f93d6fdd585205da026755f20867a49(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c569331ecfb04e8d47a0a977200e9191d6f9cd1fe2a40c7aba4c0c5fb7fedc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa64bb5cc7d06f9fecb92c131ed8edb0ebe5e664bca71bd6caa488356b4861d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984f0c82a78013462aa9be99b616bb14cfa7bb9c50da088c85520a302bce4257(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3ff73bda83bfa19d32a7bbb2d1f1efca7da71f7a36453bad6f6a496cdc68be(
    *,
    approval_stage: typing.Optional[typing.Union[GroupRoleManagementPolicyActivationRulesApprovalStage, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_duration: typing.Optional[builtins.str] = None,
    require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_conditional_access_authentication_context: typing.Optional[builtins.str] = None,
    require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ccbb44c8f89ecb62d1b29c024bdc5ec6804d60cd8f4b972e290ed864e50d42(
    *,
    primary_approver: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fcad0b554abeb21b427af4a8e135ef91509db51b30ffc42e1ef7da931307a35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3d96aff171ae2753d2bb110eb90b2f0d58b59c07df86143f491c0246df892b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdda16417c838ea338de703ea2cefde93d9e8bd7c956a5c8965be84c5b1c51b(
    value: typing.Optional[GroupRoleManagementPolicyActivationRulesApprovalStage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc459bba6d47b9d0c3cb989f54413f6b8cd7c02660d5b4b23977341d6c4e5829(
    *,
    object_id: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99827ef8959a0295df3d499c213ab120f938dd8f0cfa054b012ced868a2a5064(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574cd9086b32bd6edfe239da59ce60d2f88ca0b9b6772a477a9e331f29f0229e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036d66901485f67f225a43863871f50d1189dbd1a038a0a7b538ddc9b4ec80ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e8c604dd50b18cbe870fe07031417503b969a0f06ad27e1621b93a021e8e72(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eda8707f8955d373be18e8c8a9b37fd8c022181cf962007d327d2c6a4f4e4cb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f837bd95067d0b41f89a14c73a40ca77d9573b0b7aa64f51cb45b31277e638(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b97dccc2d3f499cd33a9c58e2118e09fdf3051aaa7ac33aa5f532bfdf7f5613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378e65a14d50f6c01bbcc209bca8b995aa127123c90f4e77aec0574db0550b00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010af9e6e3a691ad19e51a8f972fef5eaa4460e3274a1e69e673788a8bfdb1dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283575384538afa42ef312b7ccecb2e7f187c829ccab72811c36184987ef11d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupRoleManagementPolicyActivationRulesApprovalStagePrimaryApprover]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8641c86ea353d6ce74bc1ba671b9194d0b5eb1ba8da1f12666de209349679048(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f75c0c1d875ec2c010031993aa07f1c188061239fc87b0684960b7e3cccaef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68db22a2d2270a5de5dbc8702eafb1c100681e2791ca351da8a927faeb38a337(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddfc18c82c4080d60cab91986c98efbba86a074990b5b2830ab78b82900cf17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79654b20ec44f2fe08edae6fb1ab0b2e2b6f67792c8c56ad964463761f7b171(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7510207ee380224855735d849fcd164401cda11806bc10302cfab0007f0e4e63(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b96f6607806e5595f7c77776759a44438bc3f40d301f97cae05553a113cd730(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85582e0a948f1b720624c70e9eabc7cd9e02b403c8b4d824b42d1fafbb223d97(
    value: typing.Optional[GroupRoleManagementPolicyActivationRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee7099acc0135e943382e2abff07ce6a5ee0113101f8d0035cc4c79751b2c02(
    *,
    expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expire_after: typing.Optional[builtins.str] = None,
    require_justification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_multifactor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_ticket_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd44b39fd5abca3cf6a560f7ddc550b2f782fcbf3d25d9676d7a552981bd743(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17f6460ae0ad57aec9f142d93e9a28e5e47a6457835ddef2b211f250a2bb846(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2102955168a9676ab38b84d1a30dfba1f24df4973ff987eb8732b80db14f593f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fa2dd32db76074039480fb72ab39708a7e8826ea3cb798b4192040756a6892(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2efdae3c842572c8a614ca113f117d97c9ed252f44304240b7b722ef56906a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947ffea549ab952de81be7a6d5360c5fa0955605f5e94bce27cc9f165992628f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a082f04cab491b9c3c54ba05855ecc34750ffb2d8c28ceea905d7638a7ec021(
    value: typing.Optional[GroupRoleManagementPolicyActiveAssignmentRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19658290548778368e430d18ee77f220195b5300f6920db2d879bdfba8f374b4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group_id: builtins.str,
    role_id: builtins.str,
    activation_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyActivationRules, typing.Dict[builtins.str, typing.Any]]] = None,
    active_assignment_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyActiveAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
    eligible_assignment_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyEligibleAssignmentRules, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    notification_rules: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRules, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GroupRoleManagementPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea28738ab1e5159dc84aac60b7d218808846b93e77140c0daaaa257d4dbf49c3(
    *,
    expiration_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expire_after: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde40e73b380fc718bf2fb57f4eae5fb6bd629ca87fa055b475c24052248539d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf68799661d9c9e034f84522848a3a9cebae4a3c6e3fa82610bbfc575ee8ac6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b129e4d11f95863d698828570428c3dde8a93e9284eddd7e50bc869378ebcf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300ce38f9b75430d00fc27655779ff3e871707a09fe3f05de71abcd7addfdaee(
    value: typing.Optional[GroupRoleManagementPolicyEligibleAssignmentRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4cb253e9ecd940ef9a8a22b1c7ec074b5e7a6686bfa018c95c10da73ba8285(
    *,
    active_assignments: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesActiveAssignments, typing.Dict[builtins.str, typing.Any]]] = None,
    eligible_activations: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleActivations, typing.Dict[builtins.str, typing.Any]]] = None,
    eligible_assignments: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleAssignments, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c22a2f196372c8eae848af7da8b5fd76e97f4314c872a4f6d7001727f97d904(
    *,
    admin_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    approver_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    assignee_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bf39c453ab967151963e4113e2c779c5a425c1733874e716bf226adc1f337b(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5533279f4ed7af62858a4b22e7b2504357e53f5bdd109e68feb92bf7bded54c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72474602bf3d4f89d6f5ef8fa3a9c26dff8e984e5ccdc1476ef744232061b507(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6188024b118b72ebcfcce85e2f9ab63d28bdf6de4ef01c9a4099aa09602e1b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35738d9d2c92a980b40f896e0a7027e7fe52cc218f915581e24c282550641be9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1130d8dd8bf3daa1001b074f01c454b71a80aa31bb89915e8246cda9d233df(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAdminNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42071a8d54e2120acffdf560848ccb616c66ba90c4dbcc749d35107c90156846(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc434ca1f53a58ef53ffec403370c465ec934ee2b7a9869f5c672a0698785b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2845011ee2e501dd00717835350d5dce06b4cc43e11c5e106f7d4eff0578330c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07aa9901608b1e1cc744ac270af7b272ab9e102bfe7cbf695480441d6fd5f1d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e04f31237bfe8717855c93f85e076505904fc3d332fdcef7712756ef144436b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe1446ebfe9c515ac4338fb96cd9d24ed041fa58016b5ffcc4a65401f3bd401(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsApproverNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a16e7122ae60aac5f71391b4ebfe9b5ad03061a23f1323ebc0f22cd8d3f7c4c(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ee71ec1d031ca0a112b4c19bd9befd96ff8cf2134258ab4ff363f25c941598(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c123855b5e05f1ae4dea162d56e8f55bc9ce4e9ec575e3b309d33f9543e70fdc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8467c6ac706781ce3a0755eb29c992148a78f897f3531906af55a7ce49d62dfb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c7bb1ef3a9a446e90ca3e3b203ad8faad736f36a2e389bfa0a7b2cb60d64a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b2d6656807d7fa2bda212952a00a8584fda2298c01707f0b9373eca6e5717e(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignmentsAssigneeNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81431d7c88088d83e3906a1ba60420d18485432ec619edbee5e9b0a4c674e37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f571f9ba5dbcbc86578927013ee4d8aa01546f802bfe69ccbfa22f3d9edf314b(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesActiveAssignments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49b50fe84c5a20fe4c101007fe132487f076966a642a59c19621bd1818b8178(
    *,
    admin_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    approver_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    assignee_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d5b1ee5f526a0e009636c49ad15ca4ecb1f11968c1bdd16461c15ed2b86fbd(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec70bddf850a51b4ebc1f44e0b2d667fd3623f44297f0a3e38662208a039354c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29669ca39d0eba6cc5ce11f76750e9fea16db21c3ab882322f5394a8e89bcee7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a403ff9f8bddaa25e0c4571049c552983eae589ee4e7c6223e83c73e1596b48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743a47704e1dd3cb8b2aa89d3ca520b7b77b4fbfa5535560ab11e793830413fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1c7a12fd1dbf102d8e4ffd26e642af93430c89bee032941fd76258aa1840e2(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAdminNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74592b3068962e784d9e17de750626c075d9cec22262ecdc214ea01e33a2aa2b(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ec941f795cdf1cea78563f112762e89d7df1c90dcc8132678182e6479cbd3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caacdf3edbfa325a0299ac81ab68c7650aa5af3807133503aca322a9815f7607(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3251e6d312e398d44863dc27519534a0c30d8e46d9a4bdd22451c26c301d6e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b1bf863f91fd08817e74531110b5fd03dafb593b9175a0534b93fe35b67153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e433e05c962e23ceb021f31abfad412473eed5a091c7db4f188fa9d00333a8(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsApproverNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35c8d2ce45ca0ee320031edb1a8f3d39a7433c1ca1ba476a39bd026f47d96ad(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f977e98761f7f46cc2df189ef449d7a0d0538a0f2bb444da902db6a003e37835(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7102f5818687a45fcf23e74c93f1a98e5c18d55cf2e8d5421154064b041091f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8fc7e860ae70be688c458737f674cb9bc6bba84ad60f255ca92f5df3124d6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826bb02908efbeab325f3a4b141260d4a48e3765599969860912f34b3713ae76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f57d7467b404904522aca697a33b81a56d635ad7652b8934f73930e4e15eb15(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivationsAssigneeNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88fc2b49a4432cac9afed194e1fa68b59f38a7a5ee96c3a2cc1abc339c7e66d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae00b9b4c0ab44b942db8026e9ea99152ba082c6f1d3b5b5ccc0fd72cc828b2(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleActivations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e236caa9ca97c28601e68bc01673f36959de4ef753aa0cb2078a35b75b3b0d(
    *,
    admin_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    approver_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    assignee_notifications: typing.Optional[typing.Union[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab067141e4a6306af12bf2631ff76c66334c0ae416d1dfea273b8f354db480dd(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b06103db55dbea632b5dddb6d523e19c4a77ed04e87c4f9186cf8eb090012a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ad89b07ec073a3720981fd62f1d8df18ddf81bceedfb04104b2c42b4e00655(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85267c7277f835d585125f1c43ac95c869f30acba27a4f9bb75a003d7392816(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e90d4685ec9f1778dfb4d902ef97430438fac6ce09a245addce5b931ea9771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b9f03076db0dc6bda6d47871b605f0d33b9ef8a1c05286734da8ec6f97e81c(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAdminNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d6946969aa8f9180b9536a3e5521c019c1d2c41b6152a99b8e8c73e6d4dc17(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4665383a2758accfda22e324a2e123e386b97f863f939aec165f60b479dc41a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47999c6cdfef755292a1ad4938cf4e17e14f7642bed6e66983cadff1255054d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14442a72f47e0ba0e71a4c6412933117a4d0d68db884453973a8f44312c656fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb1bdef652b7c1c4ee5fa6af00b9202a1bf0ee671a43ce2456540f0ae818e94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36f7eaf1b0303b53670c262f86f07b7959c7d0da175356f4807a4c0e609aafa(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsApproverNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbab6e0dcf141f0e081878b8c330e0c5402695e83313785ee1441380c62031f6(
    *,
    default_recipients: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_level: builtins.str,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd1cbfdbe9b509305f71ed8fad3eccf10666826594e81a9fda867a4278fe5ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7f2052fa22a5b633ebffb29e48d6b14c5b1193881ca63e7aeca1875757c336(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c38fddd54cffb15c5aa4cfd3c8b54774814f4cdd32ba15d93a9d214e177498(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bd4efe880a0a17959347c554c03896ceca62e64f5d7a4d4a5aafcf227aba00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e4a79babb4dd293327d2ce9cb8439d379b46f2e761894fc1693d60e3098255(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignmentsAssigneeNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2349dee9a9305a08455becb3fe4d4643d88449141cc98031c8890c7f5c2ff886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1faa0a740e895eb1873a83be4d93e24b1b0a516a235957688174cfe6ce5cf4c(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRulesEligibleAssignments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ead77107cc84a90cc4142fa8dfb30ed93f4511f09843f2b57d67005226b8afa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0647a920f0782f8274425afd59a1dd48dd9cd2d4bcfa4f0fc9f6572140194a23(
    value: typing.Optional[GroupRoleManagementPolicyNotificationRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fb93b9d910d8f346d63d58772896d81bd3cfd6e9181d6fba0d2835271bcdc3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83787a3e4d9697277ed1f8fc3c055664f7f3fa11e6a8287b4b4634f463f60267(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83def158f4f68bac779bd444f74d3c1b50878ac39922cdfe4100597c7e4cba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18254036e0edb97c61c173a6845313bfb9ff988062a63d779016645a546ae9a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08f2e55dc76438ac198ee38c0e9bbe0dd33de957bc8a7d97d9f3212a9ae0bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0689937e935044fdfab816d8e6347bef9fdcb21d3d031e7b883032cdae451c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbcd4d6cd8dc85d5b64dd371a8bd4b99833c72b8948cae653228eed4799666af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GroupRoleManagementPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
