r'''
# `azurerm_pim_eligible_role_assignment`

Refer to the Terraform Registry for docs: [`azurerm_pim_eligible_role_assignment`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment).
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


class PimEligibleRoleAssignment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment azurerm_pim_eligible_role_assignment}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        principal_id: builtins.str,
        role_definition_id: builtins.str,
        scope: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        condition_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["PimEligibleRoleAssignmentSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        ticket: typing.Optional[typing.Union["PimEligibleRoleAssignmentTicket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PimEligibleRoleAssignmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment azurerm_pim_eligible_role_assignment} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param principal_id: Object ID of the principal for this eligible role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#principal_id PimEligibleRoleAssignment#principal_id}
        :param role_definition_id: Role definition ID for this eligible role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#role_definition_id PimEligibleRoleAssignment#role_definition_id}
        :param scope: Scope for this eligible role assignment, should be a valid resource ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#scope PimEligibleRoleAssignment#scope}
        :param condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#condition PimEligibleRoleAssignment#condition}.
        :param condition_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#condition_version PimEligibleRoleAssignment#condition_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#id PimEligibleRoleAssignment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param justification: The justification for this eligible role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#justification PimEligibleRoleAssignment#justification}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#schedule PimEligibleRoleAssignment#schedule}
        :param ticket: ticket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#ticket PimEligibleRoleAssignment#ticket}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#timeouts PimEligibleRoleAssignment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edeb1e3334474a50832e4b0d27d9ab9e8f759557c6badd444edf13ad7f009144)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PimEligibleRoleAssignmentConfig(
            principal_id=principal_id,
            role_definition_id=role_definition_id,
            scope=scope,
            condition=condition,
            condition_version=condition_version,
            id=id,
            justification=justification,
            schedule=schedule,
            ticket=ticket,
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
        '''Generates CDKTF code for importing a PimEligibleRoleAssignment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PimEligibleRoleAssignment to import.
        :param import_from_id: The id of the existing PimEligibleRoleAssignment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PimEligibleRoleAssignment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c78a6b3bed3c1deedcef14fd41a4445f10abb1d56e94822f65684938ad65fc1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        expiration: typing.Optional[typing.Union["PimEligibleRoleAssignmentScheduleExpiration", typing.Dict[builtins.str, typing.Any]]] = None,
        start_date_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration: expiration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#expiration PimEligibleRoleAssignment#expiration}
        :param start_date_time: The start date/time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#start_date_time PimEligibleRoleAssignment#start_date_time}
        '''
        value = PimEligibleRoleAssignmentSchedule(
            expiration=expiration, start_date_time=start_date_time
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="putTicket")
    def put_ticket(
        self,
        *,
        number: typing.Optional[builtins.str] = None,
        system_attribute: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param number: User-supplied ticket number to be included with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#number PimEligibleRoleAssignment#number}
        :param system_attribute: User-supplied ticket system name to be included with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#system PimEligibleRoleAssignment#system}
        '''
        value = PimEligibleRoleAssignmentTicket(
            number=number, system_attribute=system_attribute
        )

        return typing.cast(None, jsii.invoke(self, "putTicket", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#create PimEligibleRoleAssignment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#delete PimEligibleRoleAssignment#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#read PimEligibleRoleAssignment#read}.
        '''
        value = PimEligibleRoleAssignmentTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetConditionVersion")
    def reset_condition_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJustification")
    def reset_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJustification", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTicket")
    def reset_ticket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTicket", []))

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
    @jsii.member(jsii_name="principalType")
    def principal_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalType"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "PimEligibleRoleAssignmentScheduleOutputReference":
        return typing.cast("PimEligibleRoleAssignmentScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="ticket")
    def ticket(self) -> "PimEligibleRoleAssignmentTicketOutputReference":
        return typing.cast("PimEligibleRoleAssignmentTicketOutputReference", jsii.get(self, "ticket"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PimEligibleRoleAssignmentTimeoutsOutputReference":
        return typing.cast("PimEligibleRoleAssignmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionVersionInput")
    def condition_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="justificationInput")
    def justification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "justificationInput"))

    @builtins.property
    @jsii.member(jsii_name="principalIdInput")
    def principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionIdInput")
    def role_definition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleDefinitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional["PimEligibleRoleAssignmentSchedule"]:
        return typing.cast(typing.Optional["PimEligibleRoleAssignmentSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="ticketInput")
    def ticket_input(self) -> typing.Optional["PimEligibleRoleAssignmentTicket"]:
        return typing.cast(typing.Optional["PimEligibleRoleAssignmentTicket"], jsii.get(self, "ticketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PimEligibleRoleAssignmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PimEligibleRoleAssignmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979570a09dcbae4c8488e89620e3afe790aec884ab1337ce3e95595eb42d5d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conditionVersion")
    def condition_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionVersion"))

    @condition_version.setter
    def condition_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe37c03f1f735c732f8f35d1cdb8c93fd2e164ea61baf8b9e75c40d3e1dc2c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cba340955c2a92945d53a96711b6459f3120ca4aaebac361fce03b25b339e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="justification")
    def justification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "justification"))

    @justification.setter
    def justification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea6f5917d82c71e4ab8990ad0b39c733062374322dc18f3f7e397c630af304c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "justification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @principal_id.setter
    def principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0825401e623c07bbd5ae354bdc559de621e2e793def804088161f047dbaec539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionId")
    def role_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleDefinitionId"))

    @role_definition_id.setter
    def role_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25dc3b81ef0cde73ccd36221e1b169419a126c69309ddd6ef92ce276a7632c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleDefinitionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42505351176d7c40f6df20ca7456f348285778f29333aeb3a6434b9e9ab5e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "principal_id": "principalId",
        "role_definition_id": "roleDefinitionId",
        "scope": "scope",
        "condition": "condition",
        "condition_version": "conditionVersion",
        "id": "id",
        "justification": "justification",
        "schedule": "schedule",
        "ticket": "ticket",
        "timeouts": "timeouts",
    },
)
class PimEligibleRoleAssignmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        principal_id: builtins.str,
        role_definition_id: builtins.str,
        scope: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        condition_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["PimEligibleRoleAssignmentSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        ticket: typing.Optional[typing.Union["PimEligibleRoleAssignmentTicket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PimEligibleRoleAssignmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param principal_id: Object ID of the principal for this eligible role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#principal_id PimEligibleRoleAssignment#principal_id}
        :param role_definition_id: Role definition ID for this eligible role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#role_definition_id PimEligibleRoleAssignment#role_definition_id}
        :param scope: Scope for this eligible role assignment, should be a valid resource ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#scope PimEligibleRoleAssignment#scope}
        :param condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#condition PimEligibleRoleAssignment#condition}.
        :param condition_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#condition_version PimEligibleRoleAssignment#condition_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#id PimEligibleRoleAssignment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param justification: The justification for this eligible role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#justification PimEligibleRoleAssignment#justification}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#schedule PimEligibleRoleAssignment#schedule}
        :param ticket: ticket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#ticket PimEligibleRoleAssignment#ticket}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#timeouts PimEligibleRoleAssignment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(schedule, dict):
            schedule = PimEligibleRoleAssignmentSchedule(**schedule)
        if isinstance(ticket, dict):
            ticket = PimEligibleRoleAssignmentTicket(**ticket)
        if isinstance(timeouts, dict):
            timeouts = PimEligibleRoleAssignmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f91790e92db561847759929ea0461edf553b31ea378acb21a4c034ba213e6c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument role_definition_id", value=role_definition_id, expected_type=type_hints["role_definition_id"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument condition_version", value=condition_version, expected_type=type_hints["condition_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument justification", value=justification, expected_type=type_hints["justification"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument ticket", value=ticket, expected_type=type_hints["ticket"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principal_id": principal_id,
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
        if condition is not None:
            self._values["condition"] = condition
        if condition_version is not None:
            self._values["condition_version"] = condition_version
        if id is not None:
            self._values["id"] = id
        if justification is not None:
            self._values["justification"] = justification
        if schedule is not None:
            self._values["schedule"] = schedule
        if ticket is not None:
            self._values["ticket"] = ticket
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
    def principal_id(self) -> builtins.str:
        '''Object ID of the principal for this eligible role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#principal_id PimEligibleRoleAssignment#principal_id}
        '''
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_definition_id(self) -> builtins.str:
        '''Role definition ID for this eligible role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#role_definition_id PimEligibleRoleAssignment#role_definition_id}
        '''
        result = self._values.get("role_definition_id")
        assert result is not None, "Required property 'role_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''Scope for this eligible role assignment, should be a valid resource ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#scope PimEligibleRoleAssignment#scope}
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#condition PimEligibleRoleAssignment#condition}.'''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#condition_version PimEligibleRoleAssignment#condition_version}.'''
        result = self._values.get("condition_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#id PimEligibleRoleAssignment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def justification(self) -> typing.Optional[builtins.str]:
        '''The justification for this eligible role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#justification PimEligibleRoleAssignment#justification}
        '''
        result = self._values.get("justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional["PimEligibleRoleAssignmentSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#schedule PimEligibleRoleAssignment#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["PimEligibleRoleAssignmentSchedule"], result)

    @builtins.property
    def ticket(self) -> typing.Optional["PimEligibleRoleAssignmentTicket"]:
        '''ticket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#ticket PimEligibleRoleAssignment#ticket}
        '''
        result = self._values.get("ticket")
        return typing.cast(typing.Optional["PimEligibleRoleAssignmentTicket"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PimEligibleRoleAssignmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#timeouts PimEligibleRoleAssignment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PimEligibleRoleAssignmentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimEligibleRoleAssignmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentSchedule",
    jsii_struct_bases=[],
    name_mapping={"expiration": "expiration", "start_date_time": "startDateTime"},
)
class PimEligibleRoleAssignmentSchedule:
    def __init__(
        self,
        *,
        expiration: typing.Optional[typing.Union["PimEligibleRoleAssignmentScheduleExpiration", typing.Dict[builtins.str, typing.Any]]] = None,
        start_date_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration: expiration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#expiration PimEligibleRoleAssignment#expiration}
        :param start_date_time: The start date/time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#start_date_time PimEligibleRoleAssignment#start_date_time}
        '''
        if isinstance(expiration, dict):
            expiration = PimEligibleRoleAssignmentScheduleExpiration(**expiration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6472c2139d7a524d81b1c29af378ec7f64be08c1bdfc6512f5812f54c6673e30)
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument start_date_time", value=start_date_time, expected_type=type_hints["start_date_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expiration is not None:
            self._values["expiration"] = expiration
        if start_date_time is not None:
            self._values["start_date_time"] = start_date_time

    @builtins.property
    def expiration(
        self,
    ) -> typing.Optional["PimEligibleRoleAssignmentScheduleExpiration"]:
        '''expiration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#expiration PimEligibleRoleAssignment#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional["PimEligibleRoleAssignmentScheduleExpiration"], result)

    @builtins.property
    def start_date_time(self) -> typing.Optional[builtins.str]:
        '''The start date/time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#start_date_time PimEligibleRoleAssignment#start_date_time}
        '''
        result = self._values.get("start_date_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimEligibleRoleAssignmentSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentScheduleExpiration",
    jsii_struct_bases=[],
    name_mapping={
        "duration_days": "durationDays",
        "duration_hours": "durationHours",
        "end_date_time": "endDateTime",
    },
)
class PimEligibleRoleAssignmentScheduleExpiration:
    def __init__(
        self,
        *,
        duration_days: typing.Optional[jsii.Number] = None,
        duration_hours: typing.Optional[jsii.Number] = None,
        end_date_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param duration_days: The duration of the eligible role assignment in days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#duration_days PimEligibleRoleAssignment#duration_days}
        :param duration_hours: The duration of the eligible role assignment in hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#duration_hours PimEligibleRoleAssignment#duration_hours}
        :param end_date_time: The end date/time of the eligible role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#end_date_time PimEligibleRoleAssignment#end_date_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fe66166dc7292a6ae7ae28a18f1018827ae8e904b8e422c14815d3acd1b7ba)
            check_type(argname="argument duration_days", value=duration_days, expected_type=type_hints["duration_days"])
            check_type(argname="argument duration_hours", value=duration_hours, expected_type=type_hints["duration_hours"])
            check_type(argname="argument end_date_time", value=end_date_time, expected_type=type_hints["end_date_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if duration_days is not None:
            self._values["duration_days"] = duration_days
        if duration_hours is not None:
            self._values["duration_hours"] = duration_hours
        if end_date_time is not None:
            self._values["end_date_time"] = end_date_time

    @builtins.property
    def duration_days(self) -> typing.Optional[jsii.Number]:
        '''The duration of the eligible role assignment in days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#duration_days PimEligibleRoleAssignment#duration_days}
        '''
        result = self._values.get("duration_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def duration_hours(self) -> typing.Optional[jsii.Number]:
        '''The duration of the eligible role assignment in hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#duration_hours PimEligibleRoleAssignment#duration_hours}
        '''
        result = self._values.get("duration_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_date_time(self) -> typing.Optional[builtins.str]:
        '''The end date/time of the eligible role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#end_date_time PimEligibleRoleAssignment#end_date_time}
        '''
        result = self._values.get("end_date_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimEligibleRoleAssignmentScheduleExpiration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PimEligibleRoleAssignmentScheduleExpirationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentScheduleExpirationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c53abdb18051f86069e176b7fc43594b4c890f1f48c5a09944e5979a13cabd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDurationDays")
    def reset_duration_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurationDays", []))

    @jsii.member(jsii_name="resetDurationHours")
    def reset_duration_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDurationHours", []))

    @jsii.member(jsii_name="resetEndDateTime")
    def reset_end_date_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDateTime", []))

    @builtins.property
    @jsii.member(jsii_name="durationDaysInput")
    def duration_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="durationHoursInput")
    def duration_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="endDateTimeInput")
    def end_date_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="durationDays")
    def duration_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationDays"))

    @duration_days.setter
    def duration_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0050951d709cb0909ab7594a07a41baa043950b5f0e5d83de0e07527b196a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationHours")
    def duration_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationHours"))

    @duration_hours.setter
    def duration_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811bb3ba493af396b0f6417ed9ba169d2a23c84a3b3c1641db2a23516b13a834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endDateTime")
    def end_date_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDateTime"))

    @end_date_time.setter
    def end_date_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75bf16d764efc4b048bc3870b3f77573702004ec837e3a5f30e8239428353d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PimEligibleRoleAssignmentScheduleExpiration]:
        return typing.cast(typing.Optional[PimEligibleRoleAssignmentScheduleExpiration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PimEligibleRoleAssignmentScheduleExpiration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2d00ecdb0eafcc93347d7663d88f03bed55da8c6c9c092b411f6ac93bf80b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PimEligibleRoleAssignmentScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5426bc48e3221e2462ec789b776224eb260b20459e5bd07c2f1304338584889b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExpiration")
    def put_expiration(
        self,
        *,
        duration_days: typing.Optional[jsii.Number] = None,
        duration_hours: typing.Optional[jsii.Number] = None,
        end_date_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param duration_days: The duration of the eligible role assignment in days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#duration_days PimEligibleRoleAssignment#duration_days}
        :param duration_hours: The duration of the eligible role assignment in hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#duration_hours PimEligibleRoleAssignment#duration_hours}
        :param end_date_time: The end date/time of the eligible role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#end_date_time PimEligibleRoleAssignment#end_date_time}
        '''
        value = PimEligibleRoleAssignmentScheduleExpiration(
            duration_days=duration_days,
            duration_hours=duration_hours,
            end_date_time=end_date_time,
        )

        return typing.cast(None, jsii.invoke(self, "putExpiration", [value]))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetStartDateTime")
    def reset_start_date_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartDateTime", []))

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> PimEligibleRoleAssignmentScheduleExpirationOutputReference:
        return typing.cast(PimEligibleRoleAssignmentScheduleExpirationOutputReference, jsii.get(self, "expiration"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(
        self,
    ) -> typing.Optional[PimEligibleRoleAssignmentScheduleExpiration]:
        return typing.cast(typing.Optional[PimEligibleRoleAssignmentScheduleExpiration], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateTimeInput")
    def start_date_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateTime")
    def start_date_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDateTime"))

    @start_date_time.setter
    def start_date_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7bb5a1510487180be51584a55c456aa2a58d770333ba4d9fcb7e5c56e9f2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PimEligibleRoleAssignmentSchedule]:
        return typing.cast(typing.Optional[PimEligibleRoleAssignmentSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PimEligibleRoleAssignmentSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565e48c8848beb2719395aa0bd26a536c450057cca211800c169c1fcc1544233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentTicket",
    jsii_struct_bases=[],
    name_mapping={"number": "number", "system_attribute": "systemAttribute"},
)
class PimEligibleRoleAssignmentTicket:
    def __init__(
        self,
        *,
        number: typing.Optional[builtins.str] = None,
        system_attribute: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param number: User-supplied ticket number to be included with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#number PimEligibleRoleAssignment#number}
        :param system_attribute: User-supplied ticket system name to be included with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#system PimEligibleRoleAssignment#system}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f665f09d31259d662c2b8b97e8b43e1d50323efa86cb4a5cb897ad1abbec882e)
            check_type(argname="argument number", value=number, expected_type=type_hints["number"])
            check_type(argname="argument system_attribute", value=system_attribute, expected_type=type_hints["system_attribute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if number is not None:
            self._values["number"] = number
        if system_attribute is not None:
            self._values["system_attribute"] = system_attribute

    @builtins.property
    def number(self) -> typing.Optional[builtins.str]:
        '''User-supplied ticket number to be included with the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#number PimEligibleRoleAssignment#number}
        '''
        result = self._values.get("number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_attribute(self) -> typing.Optional[builtins.str]:
        '''User-supplied ticket system name to be included with the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#system PimEligibleRoleAssignment#system}
        '''
        result = self._values.get("system_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimEligibleRoleAssignmentTicket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PimEligibleRoleAssignmentTicketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentTicketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef67f96fb699cdd2276793449a478d6d7ab61dec2f22f8d40966ca407ddecd4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNumber")
    def reset_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumber", []))

    @jsii.member(jsii_name="resetSystemAttribute")
    def reset_system_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemAttribute", []))

    @builtins.property
    @jsii.member(jsii_name="numberInput")
    def number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "numberInput"))

    @builtins.property
    @jsii.member(jsii_name="systemAttributeInput")
    def system_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="number")
    def number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "number"))

    @number.setter
    def number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19aac94173ef986328067c3d606da29dd76adc6fb9ca558fc4b6758442ee338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "number", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemAttribute")
    def system_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemAttribute"))

    @system_attribute.setter
    def system_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d12bc6b9c3c6647bff7861b58f2abc399091a3a12cddcb5c4500fdfe12f107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PimEligibleRoleAssignmentTicket]:
        return typing.cast(typing.Optional[PimEligibleRoleAssignmentTicket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PimEligibleRoleAssignmentTicket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f55ed623bcf5c4fe26e1c5c8bf1356ebc31e71d56c93508532aca95133867a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class PimEligibleRoleAssignmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#create PimEligibleRoleAssignment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#delete PimEligibleRoleAssignment#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#read PimEligibleRoleAssignment#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649fe937ec80799e4f88dfdfd6415da3dc18f9b17546ceb3736a414b9163b82d)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#create PimEligibleRoleAssignment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#delete PimEligibleRoleAssignment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_eligible_role_assignment#read PimEligibleRoleAssignment#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimEligibleRoleAssignmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PimEligibleRoleAssignmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimEligibleRoleAssignment.PimEligibleRoleAssignmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6488f48e50c726ee2d8fe743d62a4dd53da1fdfed0e32a958e5514606acb8f47)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce8178689b3aaa3bf7c31166045fed8fc57b220dee94c4613c0a47f99ab1f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c1537854e39d05929b24595ba58b804be4669b96f0a894a6ace36a8b6a5b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135f614faeaa64b5e6acff9370293568232d111e31302e78841ede90f22d0263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PimEligibleRoleAssignmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PimEligibleRoleAssignmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PimEligibleRoleAssignmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5195615b1e1f7d3e1aec7b6b2a11dd34275794567fff713b0452f8a5e4bde328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PimEligibleRoleAssignment",
    "PimEligibleRoleAssignmentConfig",
    "PimEligibleRoleAssignmentSchedule",
    "PimEligibleRoleAssignmentScheduleExpiration",
    "PimEligibleRoleAssignmentScheduleExpirationOutputReference",
    "PimEligibleRoleAssignmentScheduleOutputReference",
    "PimEligibleRoleAssignmentTicket",
    "PimEligibleRoleAssignmentTicketOutputReference",
    "PimEligibleRoleAssignmentTimeouts",
    "PimEligibleRoleAssignmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__edeb1e3334474a50832e4b0d27d9ab9e8f759557c6badd444edf13ad7f009144(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    principal_id: builtins.str,
    role_definition_id: builtins.str,
    scope: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    condition_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[PimEligibleRoleAssignmentSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    ticket: typing.Optional[typing.Union[PimEligibleRoleAssignmentTicket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PimEligibleRoleAssignmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8c78a6b3bed3c1deedcef14fd41a4445f10abb1d56e94822f65684938ad65fc1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979570a09dcbae4c8488e89620e3afe790aec884ab1337ce3e95595eb42d5d26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe37c03f1f735c732f8f35d1cdb8c93fd2e164ea61baf8b9e75c40d3e1dc2c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cba340955c2a92945d53a96711b6459f3120ca4aaebac361fce03b25b339e1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea6f5917d82c71e4ab8990ad0b39c733062374322dc18f3f7e397c630af304c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0825401e623c07bbd5ae354bdc559de621e2e793def804088161f047dbaec539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dc3b81ef0cde73ccd36221e1b169419a126c69309ddd6ef92ce276a7632c28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42505351176d7c40f6df20ca7456f348285778f29333aeb3a6434b9e9ab5e55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f91790e92db561847759929ea0461edf553b31ea378acb21a4c034ba213e6c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    principal_id: builtins.str,
    role_definition_id: builtins.str,
    scope: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    condition_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[PimEligibleRoleAssignmentSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    ticket: typing.Optional[typing.Union[PimEligibleRoleAssignmentTicket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PimEligibleRoleAssignmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6472c2139d7a524d81b1c29af378ec7f64be08c1bdfc6512f5812f54c6673e30(
    *,
    expiration: typing.Optional[typing.Union[PimEligibleRoleAssignmentScheduleExpiration, typing.Dict[builtins.str, typing.Any]]] = None,
    start_date_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fe66166dc7292a6ae7ae28a18f1018827ae8e904b8e422c14815d3acd1b7ba(
    *,
    duration_days: typing.Optional[jsii.Number] = None,
    duration_hours: typing.Optional[jsii.Number] = None,
    end_date_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c53abdb18051f86069e176b7fc43594b4c890f1f48c5a09944e5979a13cabd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0050951d709cb0909ab7594a07a41baa043950b5f0e5d83de0e07527b196a71(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811bb3ba493af396b0f6417ed9ba169d2a23c84a3b3c1641db2a23516b13a834(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bf16d764efc4b048bc3870b3f77573702004ec837e3a5f30e8239428353d0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2d00ecdb0eafcc93347d7663d88f03bed55da8c6c9c092b411f6ac93bf80b8(
    value: typing.Optional[PimEligibleRoleAssignmentScheduleExpiration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5426bc48e3221e2462ec789b776224eb260b20459e5bd07c2f1304338584889b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7bb5a1510487180be51584a55c456aa2a58d770333ba4d9fcb7e5c56e9f2ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565e48c8848beb2719395aa0bd26a536c450057cca211800c169c1fcc1544233(
    value: typing.Optional[PimEligibleRoleAssignmentSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f665f09d31259d662c2b8b97e8b43e1d50323efa86cb4a5cb897ad1abbec882e(
    *,
    number: typing.Optional[builtins.str] = None,
    system_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef67f96fb699cdd2276793449a478d6d7ab61dec2f22f8d40966ca407ddecd4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19aac94173ef986328067c3d606da29dd76adc6fb9ca558fc4b6758442ee338(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d12bc6b9c3c6647bff7861b58f2abc399091a3a12cddcb5c4500fdfe12f107(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f55ed623bcf5c4fe26e1c5c8bf1356ebc31e71d56c93508532aca95133867a(
    value: typing.Optional[PimEligibleRoleAssignmentTicket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649fe937ec80799e4f88dfdfd6415da3dc18f9b17546ceb3736a414b9163b82d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6488f48e50c726ee2d8fe743d62a4dd53da1fdfed0e32a958e5514606acb8f47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce8178689b3aaa3bf7c31166045fed8fc57b220dee94c4613c0a47f99ab1f2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c1537854e39d05929b24595ba58b804be4669b96f0a894a6ace36a8b6a5b82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135f614faeaa64b5e6acff9370293568232d111e31302e78841ede90f22d0263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5195615b1e1f7d3e1aec7b6b2a11dd34275794567fff713b0452f8a5e4bde328(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PimEligibleRoleAssignmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
