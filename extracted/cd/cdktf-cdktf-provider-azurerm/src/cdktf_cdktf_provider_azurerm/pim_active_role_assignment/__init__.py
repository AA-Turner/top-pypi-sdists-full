r'''
# `azurerm_pim_active_role_assignment`

Refer to the Terraform Registry for docs: [`azurerm_pim_active_role_assignment`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment).
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


class PimActiveRoleAssignment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment azurerm_pim_active_role_assignment}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        principal_id: builtins.str,
        role_definition_id: builtins.str,
        scope: builtins.str,
        id: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["PimActiveRoleAssignmentSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        ticket: typing.Optional[typing.Union["PimActiveRoleAssignmentTicket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PimActiveRoleAssignmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment azurerm_pim_active_role_assignment} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param principal_id: Object ID of the principal for this role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#principal_id PimActiveRoleAssignment#principal_id}
        :param role_definition_id: Role definition ID for this role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#role_definition_id PimActiveRoleAssignment#role_definition_id}
        :param scope: Scope for this role assignment, should be a valid resource ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#scope PimActiveRoleAssignment#scope}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#id PimActiveRoleAssignment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param justification: The justification for this role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#justification PimActiveRoleAssignment#justification}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#schedule PimActiveRoleAssignment#schedule}
        :param ticket: ticket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#ticket PimActiveRoleAssignment#ticket}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#timeouts PimActiveRoleAssignment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4ae8a02b7caa20af056c80c757dcee36910b18be221ff9256dfb81fd29b2f4)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PimActiveRoleAssignmentConfig(
            principal_id=principal_id,
            role_definition_id=role_definition_id,
            scope=scope,
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
        '''Generates CDKTF code for importing a PimActiveRoleAssignment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PimActiveRoleAssignment to import.
        :param import_from_id: The id of the existing PimActiveRoleAssignment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PimActiveRoleAssignment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69f33389a600c9627faddbdc4ce13c75b6f38ea368d49e217df662de65db32a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        expiration: typing.Optional[typing.Union["PimActiveRoleAssignmentScheduleExpiration", typing.Dict[builtins.str, typing.Any]]] = None,
        start_date_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration: expiration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#expiration PimActiveRoleAssignment#expiration}
        :param start_date_time: The start date/time of the role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#start_date_time PimActiveRoleAssignment#start_date_time}
        '''
        value = PimActiveRoleAssignmentSchedule(
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
        :param number: User-supplied ticket number to be included with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#number PimActiveRoleAssignment#number}
        :param system_attribute: User-supplied ticket system name to be included with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#system PimActiveRoleAssignment#system}
        '''
        value = PimActiveRoleAssignmentTicket(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#create PimActiveRoleAssignment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#delete PimActiveRoleAssignment#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#read PimActiveRoleAssignment#read}.
        '''
        value = PimActiveRoleAssignmentTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

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
    def schedule(self) -> "PimActiveRoleAssignmentScheduleOutputReference":
        return typing.cast("PimActiveRoleAssignmentScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="ticket")
    def ticket(self) -> "PimActiveRoleAssignmentTicketOutputReference":
        return typing.cast("PimActiveRoleAssignmentTicketOutputReference", jsii.get(self, "ticket"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PimActiveRoleAssignmentTimeoutsOutputReference":
        return typing.cast("PimActiveRoleAssignmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def schedule_input(self) -> typing.Optional["PimActiveRoleAssignmentSchedule"]:
        return typing.cast(typing.Optional["PimActiveRoleAssignmentSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="ticketInput")
    def ticket_input(self) -> typing.Optional["PimActiveRoleAssignmentTicket"]:
        return typing.cast(typing.Optional["PimActiveRoleAssignmentTicket"], jsii.get(self, "ticketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PimActiveRoleAssignmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PimActiveRoleAssignmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04ecb4231534dfe52b5955693208a395c768a23cf8548d6840530b8a914ed16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="justification")
    def justification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "justification"))

    @justification.setter
    def justification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5b902114ef68691ea0534661b4331395a8808aeab16877ced26524eef1f132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "justification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @principal_id.setter
    def principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b035f6473f66970330cde2af6b74dce952b9c207f52e79469124265e80ce8b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleDefinitionId")
    def role_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleDefinitionId"))

    @role_definition_id.setter
    def role_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b1e1ddd73bff2187b81a5bcf4312a94a9a5db5bea0e67068d9b4ffecf1288d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleDefinitionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288733c4b86b05adde67bfd7b245b80e0d38ab8fef6af55fa106118988ea7723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentConfig",
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
        "id": "id",
        "justification": "justification",
        "schedule": "schedule",
        "ticket": "ticket",
        "timeouts": "timeouts",
    },
)
class PimActiveRoleAssignmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["PimActiveRoleAssignmentSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        ticket: typing.Optional[typing.Union["PimActiveRoleAssignmentTicket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PimActiveRoleAssignmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param principal_id: Object ID of the principal for this role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#principal_id PimActiveRoleAssignment#principal_id}
        :param role_definition_id: Role definition ID for this role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#role_definition_id PimActiveRoleAssignment#role_definition_id}
        :param scope: Scope for this role assignment, should be a valid resource ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#scope PimActiveRoleAssignment#scope}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#id PimActiveRoleAssignment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param justification: The justification for this role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#justification PimActiveRoleAssignment#justification}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#schedule PimActiveRoleAssignment#schedule}
        :param ticket: ticket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#ticket PimActiveRoleAssignment#ticket}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#timeouts PimActiveRoleAssignment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(schedule, dict):
            schedule = PimActiveRoleAssignmentSchedule(**schedule)
        if isinstance(ticket, dict):
            ticket = PimActiveRoleAssignmentTicket(**ticket)
        if isinstance(timeouts, dict):
            timeouts = PimActiveRoleAssignmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cdc6b6dc1e5eb7cf321d7e45eb2d5e3e7cced05ac56ba69d27d3d0122ce84bd)
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
        '''Object ID of the principal for this role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#principal_id PimActiveRoleAssignment#principal_id}
        '''
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_definition_id(self) -> builtins.str:
        '''Role definition ID for this role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#role_definition_id PimActiveRoleAssignment#role_definition_id}
        '''
        result = self._values.get("role_definition_id")
        assert result is not None, "Required property 'role_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''Scope for this role assignment, should be a valid resource ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#scope PimActiveRoleAssignment#scope}
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#id PimActiveRoleAssignment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def justification(self) -> typing.Optional[builtins.str]:
        '''The justification for this role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#justification PimActiveRoleAssignment#justification}
        '''
        result = self._values.get("justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional["PimActiveRoleAssignmentSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#schedule PimActiveRoleAssignment#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["PimActiveRoleAssignmentSchedule"], result)

    @builtins.property
    def ticket(self) -> typing.Optional["PimActiveRoleAssignmentTicket"]:
        '''ticket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#ticket PimActiveRoleAssignment#ticket}
        '''
        result = self._values.get("ticket")
        return typing.cast(typing.Optional["PimActiveRoleAssignmentTicket"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PimActiveRoleAssignmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#timeouts PimActiveRoleAssignment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PimActiveRoleAssignmentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimActiveRoleAssignmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentSchedule",
    jsii_struct_bases=[],
    name_mapping={"expiration": "expiration", "start_date_time": "startDateTime"},
)
class PimActiveRoleAssignmentSchedule:
    def __init__(
        self,
        *,
        expiration: typing.Optional[typing.Union["PimActiveRoleAssignmentScheduleExpiration", typing.Dict[builtins.str, typing.Any]]] = None,
        start_date_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration: expiration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#expiration PimActiveRoleAssignment#expiration}
        :param start_date_time: The start date/time of the role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#start_date_time PimActiveRoleAssignment#start_date_time}
        '''
        if isinstance(expiration, dict):
            expiration = PimActiveRoleAssignmentScheduleExpiration(**expiration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374850b4eae43fdceab7774867e734a0730792a0a6d03459e92e33015815fa1b)
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
    ) -> typing.Optional["PimActiveRoleAssignmentScheduleExpiration"]:
        '''expiration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#expiration PimActiveRoleAssignment#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional["PimActiveRoleAssignmentScheduleExpiration"], result)

    @builtins.property
    def start_date_time(self) -> typing.Optional[builtins.str]:
        '''The start date/time of the role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#start_date_time PimActiveRoleAssignment#start_date_time}
        '''
        result = self._values.get("start_date_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimActiveRoleAssignmentSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentScheduleExpiration",
    jsii_struct_bases=[],
    name_mapping={
        "duration_days": "durationDays",
        "duration_hours": "durationHours",
        "end_date_time": "endDateTime",
    },
)
class PimActiveRoleAssignmentScheduleExpiration:
    def __init__(
        self,
        *,
        duration_days: typing.Optional[jsii.Number] = None,
        duration_hours: typing.Optional[jsii.Number] = None,
        end_date_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param duration_days: The duration of the role assignment in days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#duration_days PimActiveRoleAssignment#duration_days}
        :param duration_hours: The duration of the role assignment in hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#duration_hours PimActiveRoleAssignment#duration_hours}
        :param end_date_time: The end date/time of the role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#end_date_time PimActiveRoleAssignment#end_date_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22824bd015373aafdec5c4463a4e22befa5c01df2442d77709c081ddf8331df2)
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
        '''The duration of the role assignment in days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#duration_days PimActiveRoleAssignment#duration_days}
        '''
        result = self._values.get("duration_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def duration_hours(self) -> typing.Optional[jsii.Number]:
        '''The duration of the role assignment in hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#duration_hours PimActiveRoleAssignment#duration_hours}
        '''
        result = self._values.get("duration_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_date_time(self) -> typing.Optional[builtins.str]:
        '''The end date/time of the role assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#end_date_time PimActiveRoleAssignment#end_date_time}
        '''
        result = self._values.get("end_date_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimActiveRoleAssignmentScheduleExpiration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PimActiveRoleAssignmentScheduleExpirationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentScheduleExpirationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca953e9f186fa02095f9c2e26c14d44f8e71992d5786d2f2c29d00c9905fca07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__954eb7c44fb7e2d9150f0c8034d6971fa2238598194436ea32334b984db0e9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="durationHours")
    def duration_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "durationHours"))

    @duration_hours.setter
    def duration_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ed3c20194309bbdd4de31315dd30cd65ec25bf76a43089d88ca26328afec61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endDateTime")
    def end_date_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDateTime"))

    @end_date_time.setter
    def end_date_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48954ea4be243da7e7b366fa87084725f6d006a570a3c5b215c693863d4f894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PimActiveRoleAssignmentScheduleExpiration]:
        return typing.cast(typing.Optional[PimActiveRoleAssignmentScheduleExpiration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PimActiveRoleAssignmentScheduleExpiration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5601801a5a93a492fc338ad7171e61f39577dd28d8f9c9a6e4d36aaa9d3d85ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PimActiveRoleAssignmentScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4e2a00ac7a87aa586d25a877aad17905514232bea869d90cf2b4f3385724b57)
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
        :param duration_days: The duration of the role assignment in days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#duration_days PimActiveRoleAssignment#duration_days}
        :param duration_hours: The duration of the role assignment in hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#duration_hours PimActiveRoleAssignment#duration_hours}
        :param end_date_time: The end date/time of the role assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#end_date_time PimActiveRoleAssignment#end_date_time}
        '''
        value = PimActiveRoleAssignmentScheduleExpiration(
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
    def expiration(self) -> PimActiveRoleAssignmentScheduleExpirationOutputReference:
        return typing.cast(PimActiveRoleAssignmentScheduleExpirationOutputReference, jsii.get(self, "expiration"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(
        self,
    ) -> typing.Optional[PimActiveRoleAssignmentScheduleExpiration]:
        return typing.cast(typing.Optional[PimActiveRoleAssignmentScheduleExpiration], jsii.get(self, "expirationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ad5be60b8e86bb98496dfbd88ef60ad67c86b55f1a677d981b1039f4fef28326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDateTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PimActiveRoleAssignmentSchedule]:
        return typing.cast(typing.Optional[PimActiveRoleAssignmentSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PimActiveRoleAssignmentSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d0462559685ff81d64102ddf74e2e8d445674020917100ebe8a63adf50ea14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentTicket",
    jsii_struct_bases=[],
    name_mapping={"number": "number", "system_attribute": "systemAttribute"},
)
class PimActiveRoleAssignmentTicket:
    def __init__(
        self,
        *,
        number: typing.Optional[builtins.str] = None,
        system_attribute: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param number: User-supplied ticket number to be included with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#number PimActiveRoleAssignment#number}
        :param system_attribute: User-supplied ticket system name to be included with the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#system PimActiveRoleAssignment#system}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f07d8733312a2047f2686ba1b7bc470fdc70cb988accf174bd93baa5885cb9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#number PimActiveRoleAssignment#number}
        '''
        result = self._values.get("number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_attribute(self) -> typing.Optional[builtins.str]:
        '''User-supplied ticket system name to be included with the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#system PimActiveRoleAssignment#system}
        '''
        result = self._values.get("system_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimActiveRoleAssignmentTicket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PimActiveRoleAssignmentTicketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentTicketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6658d670bdbbdbfe0bb29fe463605f08ed4b15ca64f07921a53734aa1da40acb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c468955c3c3caeefa7a82ee15e6e1623b47983431dc23b83f385f4f8e321ca3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "number", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemAttribute")
    def system_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemAttribute"))

    @system_attribute.setter
    def system_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bae0b14b3a5f1fd259c811b19b377495d104af875a054cffa9736c466a68125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PimActiveRoleAssignmentTicket]:
        return typing.cast(typing.Optional[PimActiveRoleAssignmentTicket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PimActiveRoleAssignmentTicket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b225c44cbed32c0edee97d0778d8cdc033092795696c5247181e02e41987dbae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class PimActiveRoleAssignmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#create PimActiveRoleAssignment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#delete PimActiveRoleAssignment#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#read PimActiveRoleAssignment#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578f3987152c788019f8a440a9847eeaba742593c5852e38b0d9d3931ec88e23)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#create PimActiveRoleAssignment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#delete PimActiveRoleAssignment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/pim_active_role_assignment#read PimActiveRoleAssignment#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PimActiveRoleAssignmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PimActiveRoleAssignmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pimActiveRoleAssignment.PimActiveRoleAssignmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20341bd9ddc7fb9fed7fbb49e41bab7f35f11429e81999a63264acbb9d7db2de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b00f3f669de38ddc38920841f059a477b37e1926f8d0b4ba29d4c4057f41b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a150eb1dcebd285554d255338590c4eefc8842dfa8888480e247aef014ffdcf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f3192813f0dddc6984e5e9b707b5f1c1765ae0231245d34fb3235eb4cf3ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PimActiveRoleAssignmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PimActiveRoleAssignmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PimActiveRoleAssignmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1b9610ab12f99d2decfbda2bac1f9454a341f9aafaf58379dc4d8ac49e993b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PimActiveRoleAssignment",
    "PimActiveRoleAssignmentConfig",
    "PimActiveRoleAssignmentSchedule",
    "PimActiveRoleAssignmentScheduleExpiration",
    "PimActiveRoleAssignmentScheduleExpirationOutputReference",
    "PimActiveRoleAssignmentScheduleOutputReference",
    "PimActiveRoleAssignmentTicket",
    "PimActiveRoleAssignmentTicketOutputReference",
    "PimActiveRoleAssignmentTimeouts",
    "PimActiveRoleAssignmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cd4ae8a02b7caa20af056c80c757dcee36910b18be221ff9256dfb81fd29b2f4(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    principal_id: builtins.str,
    role_definition_id: builtins.str,
    scope: builtins.str,
    id: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[PimActiveRoleAssignmentSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    ticket: typing.Optional[typing.Union[PimActiveRoleAssignmentTicket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PimActiveRoleAssignmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a69f33389a600c9627faddbdc4ce13c75b6f38ea368d49e217df662de65db32a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04ecb4231534dfe52b5955693208a395c768a23cf8548d6840530b8a914ed16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5b902114ef68691ea0534661b4331395a8808aeab16877ced26524eef1f132(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b035f6473f66970330cde2af6b74dce952b9c207f52e79469124265e80ce8b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b1e1ddd73bff2187b81a5bcf4312a94a9a5db5bea0e67068d9b4ffecf1288d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288733c4b86b05adde67bfd7b245b80e0d38ab8fef6af55fa106118988ea7723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdc6b6dc1e5eb7cf321d7e45eb2d5e3e7cced05ac56ba69d27d3d0122ce84bd(
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
    id: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[PimActiveRoleAssignmentSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    ticket: typing.Optional[typing.Union[PimActiveRoleAssignmentTicket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PimActiveRoleAssignmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374850b4eae43fdceab7774867e734a0730792a0a6d03459e92e33015815fa1b(
    *,
    expiration: typing.Optional[typing.Union[PimActiveRoleAssignmentScheduleExpiration, typing.Dict[builtins.str, typing.Any]]] = None,
    start_date_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22824bd015373aafdec5c4463a4e22befa5c01df2442d77709c081ddf8331df2(
    *,
    duration_days: typing.Optional[jsii.Number] = None,
    duration_hours: typing.Optional[jsii.Number] = None,
    end_date_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca953e9f186fa02095f9c2e26c14d44f8e71992d5786d2f2c29d00c9905fca07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954eb7c44fb7e2d9150f0c8034d6971fa2238598194436ea32334b984db0e9ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ed3c20194309bbdd4de31315dd30cd65ec25bf76a43089d88ca26328afec61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48954ea4be243da7e7b366fa87084725f6d006a570a3c5b215c693863d4f894(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5601801a5a93a492fc338ad7171e61f39577dd28d8f9c9a6e4d36aaa9d3d85ab(
    value: typing.Optional[PimActiveRoleAssignmentScheduleExpiration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e2a00ac7a87aa586d25a877aad17905514232bea869d90cf2b4f3385724b57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5be60b8e86bb98496dfbd88ef60ad67c86b55f1a677d981b1039f4fef28326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d0462559685ff81d64102ddf74e2e8d445674020917100ebe8a63adf50ea14(
    value: typing.Optional[PimActiveRoleAssignmentSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f07d8733312a2047f2686ba1b7bc470fdc70cb988accf174bd93baa5885cb9(
    *,
    number: typing.Optional[builtins.str] = None,
    system_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6658d670bdbbdbfe0bb29fe463605f08ed4b15ca64f07921a53734aa1da40acb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c468955c3c3caeefa7a82ee15e6e1623b47983431dc23b83f385f4f8e321ca3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bae0b14b3a5f1fd259c811b19b377495d104af875a054cffa9736c466a68125(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b225c44cbed32c0edee97d0778d8cdc033092795696c5247181e02e41987dbae(
    value: typing.Optional[PimActiveRoleAssignmentTicket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578f3987152c788019f8a440a9847eeaba742593c5852e38b0d9d3931ec88e23(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20341bd9ddc7fb9fed7fbb49e41bab7f35f11429e81999a63264acbb9d7db2de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b00f3f669de38ddc38920841f059a477b37e1926f8d0b4ba29d4c4057f41b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a150eb1dcebd285554d255338590c4eefc8842dfa8888480e247aef014ffdcf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f3192813f0dddc6984e5e9b707b5f1c1765ae0231245d34fb3235eb4cf3ebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1b9610ab12f99d2decfbda2bac1f9454a341f9aafaf58379dc4d8ac49e993b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PimActiveRoleAssignmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
