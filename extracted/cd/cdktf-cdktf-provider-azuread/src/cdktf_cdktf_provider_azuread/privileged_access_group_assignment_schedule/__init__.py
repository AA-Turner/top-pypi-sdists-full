r'''
# `azuread_privileged_access_group_assignment_schedule`

Refer to the Terraform Registry for docs: [`azuread_privileged_access_group_assignment_schedule`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule).
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


class PrivilegedAccessGroupAssignmentSchedule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.privilegedAccessGroupAssignmentSchedule.PrivilegedAccessGroupAssignmentSchedule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule azuread_privileged_access_group_assignment_schedule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        assignment_type: builtins.str,
        group_id: builtins.str,
        principal_id: builtins.str,
        duration: typing.Optional[builtins.str] = None,
        expiration_date: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        permanent_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_date: typing.Optional[builtins.str] = None,
        ticket_number: typing.Optional[builtins.str] = None,
        ticket_system: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["PrivilegedAccessGroupAssignmentScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule azuread_privileged_access_group_assignment_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param assignment_type: The ID of the assignment to the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#assignment_type PrivilegedAccessGroupAssignmentSchedule#assignment_type}
        :param group_id: The ID of the Group representing the scope of the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#group_id PrivilegedAccessGroupAssignmentSchedule#group_id}
        :param principal_id: The ID of the Principal assigned to the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#principal_id PrivilegedAccessGroupAssignmentSchedule#principal_id}
        :param duration: The duration of the assignment, formatted as an ISO8601 duration string (e.g. P3D for 3 days). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#duration PrivilegedAccessGroupAssignmentSchedule#duration}
        :param expiration_date: The date that this assignment expires, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#expiration_date PrivilegedAccessGroupAssignmentSchedule#expiration_date}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#id PrivilegedAccessGroupAssignmentSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param justification: The justification for the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#justification PrivilegedAccessGroupAssignmentSchedule#justification}
        :param permanent_assignment: Is the assignment permanent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#permanent_assignment PrivilegedAccessGroupAssignmentSchedule#permanent_assignment}
        :param start_date: The date that this assignment starts, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#start_date PrivilegedAccessGroupAssignmentSchedule#start_date}
        :param ticket_number: The ticket number authorising the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#ticket_number PrivilegedAccessGroupAssignmentSchedule#ticket_number}
        :param ticket_system: The ticket system authorising the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#ticket_system PrivilegedAccessGroupAssignmentSchedule#ticket_system}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#timeouts PrivilegedAccessGroupAssignmentSchedule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163199bc427f51fc486b7109a5037c04320f01daa053cd888b755fafc704a2d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PrivilegedAccessGroupAssignmentScheduleConfig(
            assignment_type=assignment_type,
            group_id=group_id,
            principal_id=principal_id,
            duration=duration,
            expiration_date=expiration_date,
            id=id,
            justification=justification,
            permanent_assignment=permanent_assignment,
            start_date=start_date,
            ticket_number=ticket_number,
            ticket_system=ticket_system,
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
        '''Generates CDKTF code for importing a PrivilegedAccessGroupAssignmentSchedule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PrivilegedAccessGroupAssignmentSchedule to import.
        :param import_from_id: The id of the existing PrivilegedAccessGroupAssignmentSchedule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PrivilegedAccessGroupAssignmentSchedule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d6f25a428afebb2605807402257baa7aebbabff314c4c01ad9e779f914c4a8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#create PrivilegedAccessGroupAssignmentSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#delete PrivilegedAccessGroupAssignmentSchedule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#read PrivilegedAccessGroupAssignmentSchedule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#update PrivilegedAccessGroupAssignmentSchedule#update}.
        '''
        value = PrivilegedAccessGroupAssignmentScheduleTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetExpirationDate")
    def reset_expiration_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationDate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJustification")
    def reset_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJustification", []))

    @jsii.member(jsii_name="resetPermanentAssignment")
    def reset_permanent_assignment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermanentAssignment", []))

    @jsii.member(jsii_name="resetStartDate")
    def reset_start_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartDate", []))

    @jsii.member(jsii_name="resetTicketNumber")
    def reset_ticket_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTicketNumber", []))

    @jsii.member(jsii_name="resetTicketSystem")
    def reset_ticket_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTicketSystem", []))

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
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "PrivilegedAccessGroupAssignmentScheduleTimeoutsOutputReference":
        return typing.cast("PrivilegedAccessGroupAssignmentScheduleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="assignmentTypeInput")
    def assignment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assignmentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationDateInput")
    def expiration_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationDateInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="justificationInput")
    def justification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "justificationInput"))

    @builtins.property
    @jsii.member(jsii_name="permanentAssignmentInput")
    def permanent_assignment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permanentAssignmentInput"))

    @builtins.property
    @jsii.member(jsii_name="principalIdInput")
    def principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="ticketNumberInput")
    def ticket_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ticketNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="ticketSystemInput")
    def ticket_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ticketSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivilegedAccessGroupAssignmentScheduleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivilegedAccessGroupAssignmentScheduleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="assignmentType")
    def assignment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assignmentType"))

    @assignment_type.setter
    def assignment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd5ec011c9c59d0cb13e41c4be228cc5a6e5c5c025848ce86c038d4ce997cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignmentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840c42df1b41c767cc37805e3ec97c3efc0e211f0dc26c69940ea5b97bd3d231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationDate")
    def expiration_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationDate"))

    @expiration_date.setter
    def expiration_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fdbdfdf3be80d9f07403677fc5ddad86887ba940d58ddcd1cbacba9f9250542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a9b731cd69c43417cb9207d0d3f19e932df6822718cec9db7a417e487ef6c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073c97158897cd59fbf6dbca51319c08c2853bcc70ba737d2f153d49637ce0b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="justification")
    def justification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "justification"))

    @justification.setter
    def justification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523a82534a19bad9fdf48dafe49294afb48782f695922fb827032ef19e1351d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "justification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permanentAssignment")
    def permanent_assignment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permanentAssignment"))

    @permanent_assignment.setter
    def permanent_assignment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165f937708b5eaeda27c7172a48916ff000a7d7cf3722cf889fbbffb315c546e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanentAssignment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @principal_id.setter
    def principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d644d22450cfc626c98c3922ff4df6111ad016d7324d5249655d49e4365496a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDate"))

    @start_date.setter
    def start_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b24174fc86ab1787512d1cc8f579458ff6a70f17b740b0ca98d0760ce7e9f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ticketNumber")
    def ticket_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ticketNumber"))

    @ticket_number.setter
    def ticket_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714907c0e6648e71029726d811a032cfe7756731e728aeca73e00e5e3857fa42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ticketNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ticketSystem")
    def ticket_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ticketSystem"))

    @ticket_system.setter
    def ticket_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7549a3015c7483461b23b0906e258d32fc8f4f3deb16115ef5ea587850064443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ticketSystem", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.privilegedAccessGroupAssignmentSchedule.PrivilegedAccessGroupAssignmentScheduleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "assignment_type": "assignmentType",
        "group_id": "groupId",
        "principal_id": "principalId",
        "duration": "duration",
        "expiration_date": "expirationDate",
        "id": "id",
        "justification": "justification",
        "permanent_assignment": "permanentAssignment",
        "start_date": "startDate",
        "ticket_number": "ticketNumber",
        "ticket_system": "ticketSystem",
        "timeouts": "timeouts",
    },
)
class PrivilegedAccessGroupAssignmentScheduleConfig(
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
        assignment_type: builtins.str,
        group_id: builtins.str,
        principal_id: builtins.str,
        duration: typing.Optional[builtins.str] = None,
        expiration_date: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        justification: typing.Optional[builtins.str] = None,
        permanent_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_date: typing.Optional[builtins.str] = None,
        ticket_number: typing.Optional[builtins.str] = None,
        ticket_system: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["PrivilegedAccessGroupAssignmentScheduleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param assignment_type: The ID of the assignment to the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#assignment_type PrivilegedAccessGroupAssignmentSchedule#assignment_type}
        :param group_id: The ID of the Group representing the scope of the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#group_id PrivilegedAccessGroupAssignmentSchedule#group_id}
        :param principal_id: The ID of the Principal assigned to the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#principal_id PrivilegedAccessGroupAssignmentSchedule#principal_id}
        :param duration: The duration of the assignment, formatted as an ISO8601 duration string (e.g. P3D for 3 days). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#duration PrivilegedAccessGroupAssignmentSchedule#duration}
        :param expiration_date: The date that this assignment expires, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#expiration_date PrivilegedAccessGroupAssignmentSchedule#expiration_date}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#id PrivilegedAccessGroupAssignmentSchedule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param justification: The justification for the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#justification PrivilegedAccessGroupAssignmentSchedule#justification}
        :param permanent_assignment: Is the assignment permanent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#permanent_assignment PrivilegedAccessGroupAssignmentSchedule#permanent_assignment}
        :param start_date: The date that this assignment starts, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#start_date PrivilegedAccessGroupAssignmentSchedule#start_date}
        :param ticket_number: The ticket number authorising the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#ticket_number PrivilegedAccessGroupAssignmentSchedule#ticket_number}
        :param ticket_system: The ticket system authorising the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#ticket_system PrivilegedAccessGroupAssignmentSchedule#ticket_system}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#timeouts PrivilegedAccessGroupAssignmentSchedule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = PrivilegedAccessGroupAssignmentScheduleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bac2d8e4d322d8cb0747e47c90f66695540ead9f76ce338b1af8fdf98d5c49f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument assignment_type", value=assignment_type, expected_type=type_hints["assignment_type"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument justification", value=justification, expected_type=type_hints["justification"])
            check_type(argname="argument permanent_assignment", value=permanent_assignment, expected_type=type_hints["permanent_assignment"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument ticket_number", value=ticket_number, expected_type=type_hints["ticket_number"])
            check_type(argname="argument ticket_system", value=ticket_system, expected_type=type_hints["ticket_system"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assignment_type": assignment_type,
            "group_id": group_id,
            "principal_id": principal_id,
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
        if duration is not None:
            self._values["duration"] = duration
        if expiration_date is not None:
            self._values["expiration_date"] = expiration_date
        if id is not None:
            self._values["id"] = id
        if justification is not None:
            self._values["justification"] = justification
        if permanent_assignment is not None:
            self._values["permanent_assignment"] = permanent_assignment
        if start_date is not None:
            self._values["start_date"] = start_date
        if ticket_number is not None:
            self._values["ticket_number"] = ticket_number
        if ticket_system is not None:
            self._values["ticket_system"] = ticket_system
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
    def assignment_type(self) -> builtins.str:
        '''The ID of the assignment to the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#assignment_type PrivilegedAccessGroupAssignmentSchedule#assignment_type}
        '''
        result = self._values.get("assignment_type")
        assert result is not None, "Required property 'assignment_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_id(self) -> builtins.str:
        '''The ID of the Group representing the scope of the assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#group_id PrivilegedAccessGroupAssignmentSchedule#group_id}
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal_id(self) -> builtins.str:
        '''The ID of the Principal assigned to the schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#principal_id PrivilegedAccessGroupAssignmentSchedule#principal_id}
        '''
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''The duration of the assignment, formatted as an ISO8601 duration string (e.g. P3D for 3 days).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#duration PrivilegedAccessGroupAssignmentSchedule#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration_date(self) -> typing.Optional[builtins.str]:
        '''The date that this assignment expires, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#expiration_date PrivilegedAccessGroupAssignmentSchedule#expiration_date}
        '''
        result = self._values.get("expiration_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#id PrivilegedAccessGroupAssignmentSchedule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def justification(self) -> typing.Optional[builtins.str]:
        '''The justification for the assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#justification PrivilegedAccessGroupAssignmentSchedule#justification}
        '''
        result = self._values.get("justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permanent_assignment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is the assignment permanent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#permanent_assignment PrivilegedAccessGroupAssignmentSchedule#permanent_assignment}
        '''
        result = self._values.get("permanent_assignment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def start_date(self) -> typing.Optional[builtins.str]:
        '''The date that this assignment starts, formatted as an RFC3339 date string in UTC (e.g. 2018-01-01T01:02:03Z).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#start_date PrivilegedAccessGroupAssignmentSchedule#start_date}
        '''
        result = self._values.get("start_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ticket_number(self) -> typing.Optional[builtins.str]:
        '''The ticket number authorising the assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#ticket_number PrivilegedAccessGroupAssignmentSchedule#ticket_number}
        '''
        result = self._values.get("ticket_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ticket_system(self) -> typing.Optional[builtins.str]:
        '''The ticket system authorising the assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#ticket_system PrivilegedAccessGroupAssignmentSchedule#ticket_system}
        '''
        result = self._values.get("ticket_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["PrivilegedAccessGroupAssignmentScheduleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#timeouts PrivilegedAccessGroupAssignmentSchedule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PrivilegedAccessGroupAssignmentScheduleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessGroupAssignmentScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.privilegedAccessGroupAssignmentSchedule.PrivilegedAccessGroupAssignmentScheduleTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class PrivilegedAccessGroupAssignmentScheduleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#create PrivilegedAccessGroupAssignmentSchedule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#delete PrivilegedAccessGroupAssignmentSchedule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#read PrivilegedAccessGroupAssignmentSchedule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#update PrivilegedAccessGroupAssignmentSchedule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570f5a6a17fb00c24ef386bedc9739761191b3b5d4e1dab7643d56fdd8ab6a0d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#create PrivilegedAccessGroupAssignmentSchedule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#delete PrivilegedAccessGroupAssignmentSchedule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#read PrivilegedAccessGroupAssignmentSchedule#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs/resources/privileged_access_group_assignment_schedule#update PrivilegedAccessGroupAssignmentSchedule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivilegedAccessGroupAssignmentScheduleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivilegedAccessGroupAssignmentScheduleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.privilegedAccessGroupAssignmentSchedule.PrivilegedAccessGroupAssignmentScheduleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76f28ff28a410b4822d4d0b2f332a2e6619e9ea6ded52df2ba097e2efa343bc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53b9bba0fea8bf2a9fac2b876a9daddb13ab68b872c3887b9661882a14186438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42758929663e7e600fc5ca700bd383eaf802dcf6aa558de1a8bf13a4fbf983e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb2768585399e9634e42d7d9de9c5b1d0e40c2bf907ba97c768efa869fe7dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6a93dcd59996d062de4b8a8805d9b5596c19556be1fe479eed3a34a3af4da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessGroupAssignmentScheduleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessGroupAssignmentScheduleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessGroupAssignmentScheduleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9b3d10698e0aaa03f7325b5d9349fa323c067e0803dd9ec8adca898d6ab3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PrivilegedAccessGroupAssignmentSchedule",
    "PrivilegedAccessGroupAssignmentScheduleConfig",
    "PrivilegedAccessGroupAssignmentScheduleTimeouts",
    "PrivilegedAccessGroupAssignmentScheduleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__163199bc427f51fc486b7109a5037c04320f01daa053cd888b755fafc704a2d9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    assignment_type: builtins.str,
    group_id: builtins.str,
    principal_id: builtins.str,
    duration: typing.Optional[builtins.str] = None,
    expiration_date: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    permanent_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_date: typing.Optional[builtins.str] = None,
    ticket_number: typing.Optional[builtins.str] = None,
    ticket_system: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[PrivilegedAccessGroupAssignmentScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3d6f25a428afebb2605807402257baa7aebbabff314c4c01ad9e779f914c4a8c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd5ec011c9c59d0cb13e41c4be228cc5a6e5c5c025848ce86c038d4ce997cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840c42df1b41c767cc37805e3ec97c3efc0e211f0dc26c69940ea5b97bd3d231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fdbdfdf3be80d9f07403677fc5ddad86887ba940d58ddcd1cbacba9f9250542(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a9b731cd69c43417cb9207d0d3f19e932df6822718cec9db7a417e487ef6c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073c97158897cd59fbf6dbca51319c08c2853bcc70ba737d2f153d49637ce0b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523a82534a19bad9fdf48dafe49294afb48782f695922fb827032ef19e1351d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165f937708b5eaeda27c7172a48916ff000a7d7cf3722cf889fbbffb315c546e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d644d22450cfc626c98c3922ff4df6111ad016d7324d5249655d49e4365496a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b24174fc86ab1787512d1cc8f579458ff6a70f17b740b0ca98d0760ce7e9f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714907c0e6648e71029726d811a032cfe7756731e728aeca73e00e5e3857fa42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7549a3015c7483461b23b0906e258d32fc8f4f3deb16115ef5ea587850064443(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bac2d8e4d322d8cb0747e47c90f66695540ead9f76ce338b1af8fdf98d5c49f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    assignment_type: builtins.str,
    group_id: builtins.str,
    principal_id: builtins.str,
    duration: typing.Optional[builtins.str] = None,
    expiration_date: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    justification: typing.Optional[builtins.str] = None,
    permanent_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_date: typing.Optional[builtins.str] = None,
    ticket_number: typing.Optional[builtins.str] = None,
    ticket_system: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[PrivilegedAccessGroupAssignmentScheduleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570f5a6a17fb00c24ef386bedc9739761191b3b5d4e1dab7643d56fdd8ab6a0d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f28ff28a410b4822d4d0b2f332a2e6619e9ea6ded52df2ba097e2efa343bc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b9bba0fea8bf2a9fac2b876a9daddb13ab68b872c3887b9661882a14186438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42758929663e7e600fc5ca700bd383eaf802dcf6aa558de1a8bf13a4fbf983e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb2768585399e9634e42d7d9de9c5b1d0e40c2bf907ba97c768efa869fe7dbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6a93dcd59996d062de4b8a8805d9b5596c19556be1fe479eed3a34a3af4da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9b3d10698e0aaa03f7325b5d9349fa323c067e0803dd9ec8adca898d6ab3ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivilegedAccessGroupAssignmentScheduleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
