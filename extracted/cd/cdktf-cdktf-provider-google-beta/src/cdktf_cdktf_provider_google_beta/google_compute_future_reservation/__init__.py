r'''
# `google_compute_future_reservation`

Refer to the Terraform Registry for docs: [`google_compute_future_reservation`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation).
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


class GoogleComputeFutureReservation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation google_compute_future_reservation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        time_window: typing.Union["GoogleComputeFutureReservationTimeWindow", typing.Dict[builtins.str, typing.Any]],
        auto_created_reservations_delete_time: typing.Optional[builtins.str] = None,
        auto_created_reservations_duration: typing.Optional[typing.Union["GoogleComputeFutureReservationAutoCreatedReservationsDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_delete_auto_created_reservations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commitment_info: typing.Optional[typing.Union["GoogleComputeFutureReservationCommitmentInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        planning_status: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_mode: typing.Optional[builtins.str] = None,
        reservation_name: typing.Optional[builtins.str] = None,
        scheduling_type: typing.Optional[builtins.str] = None,
        share_settings: typing.Optional[typing.Union["GoogleComputeFutureReservationShareSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        specific_reservation_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        specific_sku_properties: typing.Optional[typing.Union["GoogleComputeFutureReservationSpecificSkuProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeFutureReservationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation google_compute_future_reservation} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the las character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#name GoogleComputeFutureReservation#name}
        :param time_window: time_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#time_window GoogleComputeFutureReservation#time_window}
        :param auto_created_reservations_delete_time: Future timestamp when the FR auto-created reservations will be deleted by Compute Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_created_reservations_delete_time GoogleComputeFutureReservation#auto_created_reservations_delete_time}
        :param auto_created_reservations_duration: auto_created_reservations_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_created_reservations_duration GoogleComputeFutureReservation#auto_created_reservations_duration}
        :param auto_delete_auto_created_reservations: Setting for enabling or disabling automatic deletion for auto-created reservation. If set to true, auto-created reservations will be deleted at Future Reservation's end time (default) or at user's defined timestamp if any of the [autoCreatedReservationsDeleteTime, autoCreatedReservationsDuration] values is specified. For keeping auto-created reservation indefinitely, this value should be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_delete_auto_created_reservations GoogleComputeFutureReservation#auto_delete_auto_created_reservations}
        :param commitment_info: commitment_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_info GoogleComputeFutureReservation#commitment_info}
        :param deployment_type: Type of the deployment requested as part of future reservation. Possible values: ["DENSE", "FLEXIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#deployment_type GoogleComputeFutureReservation#deployment_type}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#description GoogleComputeFutureReservation#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#id GoogleComputeFutureReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name_prefix: Name prefix for the reservations to be created at the time of delivery. The name prefix must comply with RFC1035. Maximum allowed length for name prefix is 20. Automatically created reservations name format will be -date-####. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#name_prefix GoogleComputeFutureReservation#name_prefix}
        :param planning_status: Planning state before being submitted for evaluation Possible values: ["DRAFT", "SUBMITTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#planning_status GoogleComputeFutureReservation#planning_status}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#project GoogleComputeFutureReservation#project}.
        :param reservation_mode: The reservation mode which determines reservation-termination behavior and expected pricing. Possible values: ["CALENDAR", "DEFAULT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#reservation_mode GoogleComputeFutureReservation#reservation_mode}
        :param reservation_name: Name of reservations where the capacity is provisioned at the time of delivery of future reservations. If the reservation with the given name does not exist already, it is created automatically at the time of Approval with INACTIVE state till specified start-time. Either provide the reservationName or a namePrefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#reservation_name GoogleComputeFutureReservation#reservation_name}
        :param scheduling_type: Maintenance information for this reservation Possible values: ["GROUPED", "INDEPENDENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#scheduling_type GoogleComputeFutureReservation#scheduling_type}
        :param share_settings: share_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#share_settings GoogleComputeFutureReservation#share_settings}
        :param specific_reservation_required: Indicates whether the auto-created reservation can be consumed by VMs with affinity for "any" reservation. If the field is set, then only VMs that target the reservation by name can consume from the delivered reservation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#specific_reservation_required GoogleComputeFutureReservation#specific_reservation_required}
        :param specific_sku_properties: specific_sku_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#specific_sku_properties GoogleComputeFutureReservation#specific_sku_properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#timeouts GoogleComputeFutureReservation#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb039468e8a09425b894bb418f5aa093f552e5ee56a65a46597b18015baf26e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeFutureReservationConfig(
            name=name,
            time_window=time_window,
            auto_created_reservations_delete_time=auto_created_reservations_delete_time,
            auto_created_reservations_duration=auto_created_reservations_duration,
            auto_delete_auto_created_reservations=auto_delete_auto_created_reservations,
            commitment_info=commitment_info,
            deployment_type=deployment_type,
            description=description,
            id=id,
            name_prefix=name_prefix,
            planning_status=planning_status,
            project=project,
            reservation_mode=reservation_mode,
            reservation_name=reservation_name,
            scheduling_type=scheduling_type,
            share_settings=share_settings,
            specific_reservation_required=specific_reservation_required,
            specific_sku_properties=specific_sku_properties,
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
        '''Generates CDKTF code for importing a GoogleComputeFutureReservation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeFutureReservation to import.
        :param import_from_id: The id of the existing GoogleComputeFutureReservation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeFutureReservation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15cc4960866eb9b6d457db60884a63a683eb09314da56e15744c7c92d772284d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoCreatedReservationsDuration")
    def put_auto_created_reservations_duration(
        self,
        *,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#nanos GoogleComputeFutureReservation#nanos}
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#seconds GoogleComputeFutureReservation#seconds}
        '''
        value = GoogleComputeFutureReservationAutoCreatedReservationsDuration(
            nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putAutoCreatedReservationsDuration", [value]))

    @jsii.member(jsii_name="putCommitmentInfo")
    def put_commitment_info(
        self,
        *,
        commitment_name: typing.Optional[builtins.str] = None,
        commitment_plan: typing.Optional[builtins.str] = None,
        previous_commitment_terms: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param commitment_name: name of the commitment where capacity is being delivered to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_name GoogleComputeFutureReservation#commitment_name}
        :param commitment_plan: Indicates if a Commitment needs to be created as part of FR delivery. If this field is not present, then no commitment needs to be created. Possible values: ["INVALID", "THIRTY_SIX_MONTH", "TWELVE_MONTH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_plan GoogleComputeFutureReservation#commitment_plan}
        :param previous_commitment_terms: Only applicable if FR is delivering to the same reservation. If set, all parent commitments will be extended to match the end date of the plan for this commitment. Possible values: ["EXTEND"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#previous_commitment_terms GoogleComputeFutureReservation#previous_commitment_terms}
        '''
        value = GoogleComputeFutureReservationCommitmentInfo(
            commitment_name=commitment_name,
            commitment_plan=commitment_plan,
            previous_commitment_terms=previous_commitment_terms,
        )

        return typing.cast(None, jsii.invoke(self, "putCommitmentInfo", [value]))

    @jsii.member(jsii_name="putShareSettings")
    def put_share_settings(
        self,
        *,
        project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeFutureReservationShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        share_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project_map: project_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#project_map GoogleComputeFutureReservation#project_map}
        :param projects: list of Project names to specify consumer projects for this shared-reservation. This is only valid when shareType's value is SPECIFIC_PROJECTS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#projects GoogleComputeFutureReservation#projects}
        :param share_type: Type of sharing for this future reservation. Possible values: ["LOCAL", "SPECIFIC_PROJECTS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#share_type GoogleComputeFutureReservation#share_type}
        '''
        value = GoogleComputeFutureReservationShareSettings(
            project_map=project_map, projects=projects, share_type=share_type
        )

        return typing.cast(None, jsii.invoke(self, "putShareSettings", [value]))

    @jsii.member(jsii_name="putSpecificSkuProperties")
    def put_specific_sku_properties(
        self,
        *,
        instance_properties: typing.Optional[typing.Union["GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        source_instance_template: typing.Optional[builtins.str] = None,
        total_count: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_properties: instance_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#instance_properties GoogleComputeFutureReservation#instance_properties}
        :param source_instance_template: The instance template that will be used to populate the ReservedInstanceProperties of the future reservation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#source_instance_template GoogleComputeFutureReservation#source_instance_template}
        :param total_count: Total number of instances for which capacity assurance is requested at a future time period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#total_count GoogleComputeFutureReservation#total_count}
        '''
        value = GoogleComputeFutureReservationSpecificSkuProperties(
            instance_properties=instance_properties,
            source_instance_template=source_instance_template,
            total_count=total_count,
        )

        return typing.cast(None, jsii.invoke(self, "putSpecificSkuProperties", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#create GoogleComputeFutureReservation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#delete GoogleComputeFutureReservation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#update GoogleComputeFutureReservation#update}.
        '''
        value = GoogleComputeFutureReservationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTimeWindow")
    def put_time_window(
        self,
        *,
        start_time: builtins.str,
        duration: typing.Optional[typing.Union["GoogleComputeFutureReservationTimeWindowDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        end_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_time: Start time of the future reservation in RFC3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#start_time GoogleComputeFutureReservation#start_time}
        :param duration: duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#duration GoogleComputeFutureReservation#duration}
        :param end_time: End time of the future reservation in RFC3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#end_time GoogleComputeFutureReservation#end_time}
        '''
        value = GoogleComputeFutureReservationTimeWindow(
            start_time=start_time, duration=duration, end_time=end_time
        )

        return typing.cast(None, jsii.invoke(self, "putTimeWindow", [value]))

    @jsii.member(jsii_name="resetAutoCreatedReservationsDeleteTime")
    def reset_auto_created_reservations_delete_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoCreatedReservationsDeleteTime", []))

    @jsii.member(jsii_name="resetAutoCreatedReservationsDuration")
    def reset_auto_created_reservations_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoCreatedReservationsDuration", []))

    @jsii.member(jsii_name="resetAutoDeleteAutoCreatedReservations")
    def reset_auto_delete_auto_created_reservations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeleteAutoCreatedReservations", []))

    @jsii.member(jsii_name="resetCommitmentInfo")
    def reset_commitment_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitmentInfo", []))

    @jsii.member(jsii_name="resetDeploymentType")
    def reset_deployment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetPlanningStatus")
    def reset_planning_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlanningStatus", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReservationMode")
    def reset_reservation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationMode", []))

    @jsii.member(jsii_name="resetReservationName")
    def reset_reservation_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationName", []))

    @jsii.member(jsii_name="resetSchedulingType")
    def reset_scheduling_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulingType", []))

    @jsii.member(jsii_name="resetShareSettings")
    def reset_share_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareSettings", []))

    @jsii.member(jsii_name="resetSpecificReservationRequired")
    def reset_specific_reservation_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecificReservationRequired", []))

    @jsii.member(jsii_name="resetSpecificSkuProperties")
    def reset_specific_sku_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecificSkuProperties", []))

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
    @jsii.member(jsii_name="autoCreatedReservationsDuration")
    def auto_created_reservations_duration(
        self,
    ) -> "GoogleComputeFutureReservationAutoCreatedReservationsDurationOutputReference":
        return typing.cast("GoogleComputeFutureReservationAutoCreatedReservationsDurationOutputReference", jsii.get(self, "autoCreatedReservationsDuration"))

    @builtins.property
    @jsii.member(jsii_name="commitmentInfo")
    def commitment_info(
        self,
    ) -> "GoogleComputeFutureReservationCommitmentInfoOutputReference":
        return typing.cast("GoogleComputeFutureReservationCommitmentInfoOutputReference", jsii.get(self, "commitmentInfo"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="selfLinkWithId")
    def self_link_with_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLinkWithId"))

    @builtins.property
    @jsii.member(jsii_name="shareSettings")
    def share_settings(
        self,
    ) -> "GoogleComputeFutureReservationShareSettingsOutputReference":
        return typing.cast("GoogleComputeFutureReservationShareSettingsOutputReference", jsii.get(self, "shareSettings"))

    @builtins.property
    @jsii.member(jsii_name="specificSkuProperties")
    def specific_sku_properties(
        self,
    ) -> "GoogleComputeFutureReservationSpecificSkuPropertiesOutputReference":
        return typing.cast("GoogleComputeFutureReservationSpecificSkuPropertiesOutputReference", jsii.get(self, "specificSkuProperties"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleComputeFutureReservationStatusList":
        return typing.cast("GoogleComputeFutureReservationStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeFutureReservationTimeoutsOutputReference":
        return typing.cast("GoogleComputeFutureReservationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="timeWindow")
    def time_window(self) -> "GoogleComputeFutureReservationTimeWindowOutputReference":
        return typing.cast("GoogleComputeFutureReservationTimeWindowOutputReference", jsii.get(self, "timeWindow"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @builtins.property
    @jsii.member(jsii_name="autoCreatedReservationsDeleteTimeInput")
    def auto_created_reservations_delete_time_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoCreatedReservationsDeleteTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoCreatedReservationsDurationInput")
    def auto_created_reservations_duration_input(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationAutoCreatedReservationsDuration"]:
        return typing.cast(typing.Optional["GoogleComputeFutureReservationAutoCreatedReservationsDuration"], jsii.get(self, "autoCreatedReservationsDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteAutoCreatedReservationsInput")
    def auto_delete_auto_created_reservations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoDeleteAutoCreatedReservationsInput"))

    @builtins.property
    @jsii.member(jsii_name="commitmentInfoInput")
    def commitment_info_input(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationCommitmentInfo"]:
        return typing.cast(typing.Optional["GoogleComputeFutureReservationCommitmentInfo"], jsii.get(self, "commitmentInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentTypeInput")
    def deployment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="planningStatusInput")
    def planning_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "planningStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationModeInput")
    def reservation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationNameInput")
    def reservation_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulingTypeInput")
    def scheduling_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schedulingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="shareSettingsInput")
    def share_settings_input(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationShareSettings"]:
        return typing.cast(typing.Optional["GoogleComputeFutureReservationShareSettings"], jsii.get(self, "shareSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="specificReservationRequiredInput")
    def specific_reservation_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "specificReservationRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="specificSkuPropertiesInput")
    def specific_sku_properties_input(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationSpecificSkuProperties"]:
        return typing.cast(typing.Optional["GoogleComputeFutureReservationSpecificSkuProperties"], jsii.get(self, "specificSkuPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeFutureReservationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeFutureReservationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowInput")
    def time_window_input(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationTimeWindow"]:
        return typing.cast(typing.Optional["GoogleComputeFutureReservationTimeWindow"], jsii.get(self, "timeWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="autoCreatedReservationsDeleteTime")
    def auto_created_reservations_delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoCreatedReservationsDeleteTime"))

    @auto_created_reservations_delete_time.setter
    def auto_created_reservations_delete_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed84cc5f16293b3eb2e294fc309a37ba6f70dd2ce3abf3ec5577ed74e23c7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoCreatedReservationsDeleteTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDeleteAutoCreatedReservations")
    def auto_delete_auto_created_reservations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoDeleteAutoCreatedReservations"))

    @auto_delete_auto_created_reservations.setter
    def auto_delete_auto_created_reservations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664e21b6b7f8e0f381f6ccdc3a7af7809ee75b17fdac6afa23db965736d6b103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeleteAutoCreatedReservations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentType")
    def deployment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentType"))

    @deployment_type.setter
    def deployment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c964772d5abeef6de4e93e06ef8f3b1d7e5bfdbbdf5ea39b3521a18bd62814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9f5469126ad7d8634446edfea473cfa758f1854f366a8be10d0b40b9d83bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a340980375f4b66a7706972da57b799a2ca77ff95d7257d3c7954b69db977d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3bbb4eb3617902c930cc910470e38fbbf4bf892e461aa28ce8951be3e2d44b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a21a18aef95022b39a1c6d74ddac3ae07fe4c292f83dffe50e9495398d35e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="planningStatus")
    def planning_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "planningStatus"))

    @planning_status.setter
    def planning_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65379aea5c56b77afc4d000d3453b2b6118bcee67e904bab06588bb9f6d23f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "planningStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272dd0f74e9b2652ffbcefe68d595af2f2b80e09fa9ffb3b52616bded9e4bdca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservationMode")
    def reservation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationMode"))

    @reservation_mode.setter
    def reservation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239896ae05554b9588071876f642fc765f98a8062e7539320259633187c3adbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservationName")
    def reservation_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationName"))

    @reservation_name.setter
    def reservation_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b21f480538719cb0c6e384e8f590b4e5ed1ee2839822fd8b845b9bad52d1e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedulingType")
    def scheduling_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedulingType"))

    @scheduling_type.setter
    def scheduling_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f26ea4dae4b95430a8c2419ca62474dd3bd04a03f922bb5e2179fea2daff8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="specificReservationRequired")
    def specific_reservation_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "specificReservationRequired"))

    @specific_reservation_required.setter
    def specific_reservation_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fdb096818f2a480e3d7d94d4174dbe4a83d0e6b60cdba212bd85e3050e9971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specificReservationRequired", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationAutoCreatedReservationsDuration",
    jsii_struct_bases=[],
    name_mapping={"nanos": "nanos", "seconds": "seconds"},
)
class GoogleComputeFutureReservationAutoCreatedReservationsDuration:
    def __init__(
        self,
        *,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#nanos GoogleComputeFutureReservation#nanos}
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#seconds GoogleComputeFutureReservation#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5941a957c783d71d9130fbb103f8b927824afebd1632f2fec3ea4beb3eda8091)
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#nanos GoogleComputeFutureReservation#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[builtins.str]:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#seconds GoogleComputeFutureReservation#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationAutoCreatedReservationsDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationAutoCreatedReservationsDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationAutoCreatedReservationsDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eef0dc7981d06959c180c54904e128820dc3c54410990178a07c9085e81caf9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a35156df722a36017faf895ed07f8a3af5ee27258a999ec64750f224974a19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134cd778041f7fa81301e1e9e90aff74dd7f10f2d42a0f159dcc55d3fa28a5ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationAutoCreatedReservationsDuration]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationAutoCreatedReservationsDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationAutoCreatedReservationsDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7efb019f4e3052b79acd05b4b63cb34aefcfb101d59994ce52e847dd0b1a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationCommitmentInfo",
    jsii_struct_bases=[],
    name_mapping={
        "commitment_name": "commitmentName",
        "commitment_plan": "commitmentPlan",
        "previous_commitment_terms": "previousCommitmentTerms",
    },
)
class GoogleComputeFutureReservationCommitmentInfo:
    def __init__(
        self,
        *,
        commitment_name: typing.Optional[builtins.str] = None,
        commitment_plan: typing.Optional[builtins.str] = None,
        previous_commitment_terms: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param commitment_name: name of the commitment where capacity is being delivered to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_name GoogleComputeFutureReservation#commitment_name}
        :param commitment_plan: Indicates if a Commitment needs to be created as part of FR delivery. If this field is not present, then no commitment needs to be created. Possible values: ["INVALID", "THIRTY_SIX_MONTH", "TWELVE_MONTH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_plan GoogleComputeFutureReservation#commitment_plan}
        :param previous_commitment_terms: Only applicable if FR is delivering to the same reservation. If set, all parent commitments will be extended to match the end date of the plan for this commitment. Possible values: ["EXTEND"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#previous_commitment_terms GoogleComputeFutureReservation#previous_commitment_terms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3efc9a8b21ac6b3f167a1c18c34667cc1eb25c1e0be178be3eb8fb855f6d00)
            check_type(argname="argument commitment_name", value=commitment_name, expected_type=type_hints["commitment_name"])
            check_type(argname="argument commitment_plan", value=commitment_plan, expected_type=type_hints["commitment_plan"])
            check_type(argname="argument previous_commitment_terms", value=previous_commitment_terms, expected_type=type_hints["previous_commitment_terms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if commitment_name is not None:
            self._values["commitment_name"] = commitment_name
        if commitment_plan is not None:
            self._values["commitment_plan"] = commitment_plan
        if previous_commitment_terms is not None:
            self._values["previous_commitment_terms"] = previous_commitment_terms

    @builtins.property
    def commitment_name(self) -> typing.Optional[builtins.str]:
        '''name of the commitment where capacity is being delivered to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_name GoogleComputeFutureReservation#commitment_name}
        '''
        result = self._values.get("commitment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commitment_plan(self) -> typing.Optional[builtins.str]:
        '''Indicates if a Commitment needs to be created as part of FR delivery.

        If this field is not present, then no commitment needs to be created. Possible values: ["INVALID", "THIRTY_SIX_MONTH", "TWELVE_MONTH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_plan GoogleComputeFutureReservation#commitment_plan}
        '''
        result = self._values.get("commitment_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def previous_commitment_terms(self) -> typing.Optional[builtins.str]:
        '''Only applicable if FR is delivering to the same reservation.

        If set, all parent commitments will be extended to match the end date of the plan for this commitment. Possible values: ["EXTEND"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#previous_commitment_terms GoogleComputeFutureReservation#previous_commitment_terms}
        '''
        result = self._values.get("previous_commitment_terms")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationCommitmentInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationCommitmentInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationCommitmentInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__815e4ea23943c8aab9973a4c8d2983dc8313bca6865f39579ce49dc3797440b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommitmentName")
    def reset_commitment_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitmentName", []))

    @jsii.member(jsii_name="resetCommitmentPlan")
    def reset_commitment_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitmentPlan", []))

    @jsii.member(jsii_name="resetPreviousCommitmentTerms")
    def reset_previous_commitment_terms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreviousCommitmentTerms", []))

    @builtins.property
    @jsii.member(jsii_name="commitmentNameInput")
    def commitment_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitmentNameInput"))

    @builtins.property
    @jsii.member(jsii_name="commitmentPlanInput")
    def commitment_plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitmentPlanInput"))

    @builtins.property
    @jsii.member(jsii_name="previousCommitmentTermsInput")
    def previous_commitment_terms_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "previousCommitmentTermsInput"))

    @builtins.property
    @jsii.member(jsii_name="commitmentName")
    def commitment_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitmentName"))

    @commitment_name.setter
    def commitment_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d098d24003a300b2a9fc4b14513e63eb2452e3aa9de111c7072c9ac7c00741f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitmentName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitmentPlan")
    def commitment_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitmentPlan"))

    @commitment_plan.setter
    def commitment_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bdeee8d2ef1144c05c68474c9c5a7a24fd82308a49836d756a701a22748d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitmentPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="previousCommitmentTerms")
    def previous_commitment_terms(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "previousCommitmentTerms"))

    @previous_commitment_terms.setter
    def previous_commitment_terms(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ea30a96883fefa6d440966a3a4434d96a618b81b900890df04452b94505e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previousCommitmentTerms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationCommitmentInfo]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationCommitmentInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationCommitmentInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea074f8ca72391591e3de79ebeb17f35c59fe94309725992f8739bfceb4d46b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationConfig",
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
        "time_window": "timeWindow",
        "auto_created_reservations_delete_time": "autoCreatedReservationsDeleteTime",
        "auto_created_reservations_duration": "autoCreatedReservationsDuration",
        "auto_delete_auto_created_reservations": "autoDeleteAutoCreatedReservations",
        "commitment_info": "commitmentInfo",
        "deployment_type": "deploymentType",
        "description": "description",
        "id": "id",
        "name_prefix": "namePrefix",
        "planning_status": "planningStatus",
        "project": "project",
        "reservation_mode": "reservationMode",
        "reservation_name": "reservationName",
        "scheduling_type": "schedulingType",
        "share_settings": "shareSettings",
        "specific_reservation_required": "specificReservationRequired",
        "specific_sku_properties": "specificSkuProperties",
        "timeouts": "timeouts",
    },
)
class GoogleComputeFutureReservationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        time_window: typing.Union["GoogleComputeFutureReservationTimeWindow", typing.Dict[builtins.str, typing.Any]],
        auto_created_reservations_delete_time: typing.Optional[builtins.str] = None,
        auto_created_reservations_duration: typing.Optional[typing.Union[GoogleComputeFutureReservationAutoCreatedReservationsDuration, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_delete_auto_created_reservations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commitment_info: typing.Optional[typing.Union[GoogleComputeFutureReservationCommitmentInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        planning_status: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_mode: typing.Optional[builtins.str] = None,
        reservation_name: typing.Optional[builtins.str] = None,
        scheduling_type: typing.Optional[builtins.str] = None,
        share_settings: typing.Optional[typing.Union["GoogleComputeFutureReservationShareSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        specific_reservation_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        specific_sku_properties: typing.Optional[typing.Union["GoogleComputeFutureReservationSpecificSkuProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeFutureReservationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the las character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#name GoogleComputeFutureReservation#name}
        :param time_window: time_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#time_window GoogleComputeFutureReservation#time_window}
        :param auto_created_reservations_delete_time: Future timestamp when the FR auto-created reservations will be deleted by Compute Engine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_created_reservations_delete_time GoogleComputeFutureReservation#auto_created_reservations_delete_time}
        :param auto_created_reservations_duration: auto_created_reservations_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_created_reservations_duration GoogleComputeFutureReservation#auto_created_reservations_duration}
        :param auto_delete_auto_created_reservations: Setting for enabling or disabling automatic deletion for auto-created reservation. If set to true, auto-created reservations will be deleted at Future Reservation's end time (default) or at user's defined timestamp if any of the [autoCreatedReservationsDeleteTime, autoCreatedReservationsDuration] values is specified. For keeping auto-created reservation indefinitely, this value should be set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_delete_auto_created_reservations GoogleComputeFutureReservation#auto_delete_auto_created_reservations}
        :param commitment_info: commitment_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_info GoogleComputeFutureReservation#commitment_info}
        :param deployment_type: Type of the deployment requested as part of future reservation. Possible values: ["DENSE", "FLEXIBLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#deployment_type GoogleComputeFutureReservation#deployment_type}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#description GoogleComputeFutureReservation#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#id GoogleComputeFutureReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name_prefix: Name prefix for the reservations to be created at the time of delivery. The name prefix must comply with RFC1035. Maximum allowed length for name prefix is 20. Automatically created reservations name format will be -date-####. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#name_prefix GoogleComputeFutureReservation#name_prefix}
        :param planning_status: Planning state before being submitted for evaluation Possible values: ["DRAFT", "SUBMITTED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#planning_status GoogleComputeFutureReservation#planning_status}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#project GoogleComputeFutureReservation#project}.
        :param reservation_mode: The reservation mode which determines reservation-termination behavior and expected pricing. Possible values: ["CALENDAR", "DEFAULT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#reservation_mode GoogleComputeFutureReservation#reservation_mode}
        :param reservation_name: Name of reservations where the capacity is provisioned at the time of delivery of future reservations. If the reservation with the given name does not exist already, it is created automatically at the time of Approval with INACTIVE state till specified start-time. Either provide the reservationName or a namePrefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#reservation_name GoogleComputeFutureReservation#reservation_name}
        :param scheduling_type: Maintenance information for this reservation Possible values: ["GROUPED", "INDEPENDENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#scheduling_type GoogleComputeFutureReservation#scheduling_type}
        :param share_settings: share_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#share_settings GoogleComputeFutureReservation#share_settings}
        :param specific_reservation_required: Indicates whether the auto-created reservation can be consumed by VMs with affinity for "any" reservation. If the field is set, then only VMs that target the reservation by name can consume from the delivered reservation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#specific_reservation_required GoogleComputeFutureReservation#specific_reservation_required}
        :param specific_sku_properties: specific_sku_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#specific_sku_properties GoogleComputeFutureReservation#specific_sku_properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#timeouts GoogleComputeFutureReservation#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(time_window, dict):
            time_window = GoogleComputeFutureReservationTimeWindow(**time_window)
        if isinstance(auto_created_reservations_duration, dict):
            auto_created_reservations_duration = GoogleComputeFutureReservationAutoCreatedReservationsDuration(**auto_created_reservations_duration)
        if isinstance(commitment_info, dict):
            commitment_info = GoogleComputeFutureReservationCommitmentInfo(**commitment_info)
        if isinstance(share_settings, dict):
            share_settings = GoogleComputeFutureReservationShareSettings(**share_settings)
        if isinstance(specific_sku_properties, dict):
            specific_sku_properties = GoogleComputeFutureReservationSpecificSkuProperties(**specific_sku_properties)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeFutureReservationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6e102566375c5d4d294a152f1ca65c0ba40fa4721d9283d1c532959486235c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument time_window", value=time_window, expected_type=type_hints["time_window"])
            check_type(argname="argument auto_created_reservations_delete_time", value=auto_created_reservations_delete_time, expected_type=type_hints["auto_created_reservations_delete_time"])
            check_type(argname="argument auto_created_reservations_duration", value=auto_created_reservations_duration, expected_type=type_hints["auto_created_reservations_duration"])
            check_type(argname="argument auto_delete_auto_created_reservations", value=auto_delete_auto_created_reservations, expected_type=type_hints["auto_delete_auto_created_reservations"])
            check_type(argname="argument commitment_info", value=commitment_info, expected_type=type_hints["commitment_info"])
            check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument planning_status", value=planning_status, expected_type=type_hints["planning_status"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument reservation_mode", value=reservation_mode, expected_type=type_hints["reservation_mode"])
            check_type(argname="argument reservation_name", value=reservation_name, expected_type=type_hints["reservation_name"])
            check_type(argname="argument scheduling_type", value=scheduling_type, expected_type=type_hints["scheduling_type"])
            check_type(argname="argument share_settings", value=share_settings, expected_type=type_hints["share_settings"])
            check_type(argname="argument specific_reservation_required", value=specific_reservation_required, expected_type=type_hints["specific_reservation_required"])
            check_type(argname="argument specific_sku_properties", value=specific_sku_properties, expected_type=type_hints["specific_sku_properties"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "time_window": time_window,
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
        if auto_created_reservations_delete_time is not None:
            self._values["auto_created_reservations_delete_time"] = auto_created_reservations_delete_time
        if auto_created_reservations_duration is not None:
            self._values["auto_created_reservations_duration"] = auto_created_reservations_duration
        if auto_delete_auto_created_reservations is not None:
            self._values["auto_delete_auto_created_reservations"] = auto_delete_auto_created_reservations
        if commitment_info is not None:
            self._values["commitment_info"] = commitment_info
        if deployment_type is not None:
            self._values["deployment_type"] = deployment_type
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if planning_status is not None:
            self._values["planning_status"] = planning_status
        if project is not None:
            self._values["project"] = project
        if reservation_mode is not None:
            self._values["reservation_mode"] = reservation_mode
        if reservation_name is not None:
            self._values["reservation_name"] = reservation_name
        if scheduling_type is not None:
            self._values["scheduling_type"] = scheduling_type
        if share_settings is not None:
            self._values["share_settings"] = share_settings
        if specific_reservation_required is not None:
            self._values["specific_reservation_required"] = specific_reservation_required
        if specific_sku_properties is not None:
            self._values["specific_sku_properties"] = specific_sku_properties
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
    def name(self) -> builtins.str:
        '''Name of the resource.

        Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the las
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#name GoogleComputeFutureReservation#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_window(self) -> "GoogleComputeFutureReservationTimeWindow":
        '''time_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#time_window GoogleComputeFutureReservation#time_window}
        '''
        result = self._values.get("time_window")
        assert result is not None, "Required property 'time_window' is missing"
        return typing.cast("GoogleComputeFutureReservationTimeWindow", result)

    @builtins.property
    def auto_created_reservations_delete_time(self) -> typing.Optional[builtins.str]:
        '''Future timestamp when the FR auto-created reservations will be deleted by Compute Engine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_created_reservations_delete_time GoogleComputeFutureReservation#auto_created_reservations_delete_time}
        '''
        result = self._values.get("auto_created_reservations_delete_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_created_reservations_duration(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationAutoCreatedReservationsDuration]:
        '''auto_created_reservations_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_created_reservations_duration GoogleComputeFutureReservation#auto_created_reservations_duration}
        '''
        result = self._values.get("auto_created_reservations_duration")
        return typing.cast(typing.Optional[GoogleComputeFutureReservationAutoCreatedReservationsDuration], result)

    @builtins.property
    def auto_delete_auto_created_reservations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting for enabling or disabling automatic deletion for auto-created reservation.

        If set to true, auto-created reservations will be deleted at Future Reservation's end time (default) or at user's defined timestamp if any of the [autoCreatedReservationsDeleteTime, autoCreatedReservationsDuration] values is specified. For keeping auto-created reservation indefinitely, this value should be set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#auto_delete_auto_created_reservations GoogleComputeFutureReservation#auto_delete_auto_created_reservations}
        '''
        result = self._values.get("auto_delete_auto_created_reservations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commitment_info(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationCommitmentInfo]:
        '''commitment_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#commitment_info GoogleComputeFutureReservation#commitment_info}
        '''
        result = self._values.get("commitment_info")
        return typing.cast(typing.Optional[GoogleComputeFutureReservationCommitmentInfo], result)

    @builtins.property
    def deployment_type(self) -> typing.Optional[builtins.str]:
        '''Type of the deployment requested as part of future reservation. Possible values: ["DENSE", "FLEXIBLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#deployment_type GoogleComputeFutureReservation#deployment_type}
        '''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#description GoogleComputeFutureReservation#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#id GoogleComputeFutureReservation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Name prefix for the reservations to be created at the time of delivery.

        The name prefix must comply with RFC1035. Maximum allowed length for name prefix is 20. Automatically created reservations name format will be -date-####.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#name_prefix GoogleComputeFutureReservation#name_prefix}
        '''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def planning_status(self) -> typing.Optional[builtins.str]:
        '''Planning state before being submitted for evaluation Possible values: ["DRAFT", "SUBMITTED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#planning_status GoogleComputeFutureReservation#planning_status}
        '''
        result = self._values.get("planning_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#project GoogleComputeFutureReservation#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_mode(self) -> typing.Optional[builtins.str]:
        '''The reservation mode which determines reservation-termination behavior and expected pricing. Possible values: ["CALENDAR", "DEFAULT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#reservation_mode GoogleComputeFutureReservation#reservation_mode}
        '''
        result = self._values.get("reservation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_name(self) -> typing.Optional[builtins.str]:
        '''Name of reservations where the capacity is provisioned at the time of delivery of future reservations.

        If the reservation with the given name does not exist already, it is created automatically at the time of Approval with INACTIVE state till specified start-time. Either provide the reservationName or a namePrefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#reservation_name GoogleComputeFutureReservation#reservation_name}
        '''
        result = self._values.get("reservation_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduling_type(self) -> typing.Optional[builtins.str]:
        '''Maintenance information for this reservation Possible values: ["GROUPED", "INDEPENDENT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#scheduling_type GoogleComputeFutureReservation#scheduling_type}
        '''
        result = self._values.get("scheduling_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_settings(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationShareSettings"]:
        '''share_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#share_settings GoogleComputeFutureReservation#share_settings}
        '''
        result = self._values.get("share_settings")
        return typing.cast(typing.Optional["GoogleComputeFutureReservationShareSettings"], result)

    @builtins.property
    def specific_reservation_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the auto-created reservation can be consumed by VMs with affinity for "any" reservation.

        If the field is set, then only VMs that target the reservation by name can consume from the delivered reservation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#specific_reservation_required GoogleComputeFutureReservation#specific_reservation_required}
        '''
        result = self._values.get("specific_reservation_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def specific_sku_properties(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationSpecificSkuProperties"]:
        '''specific_sku_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#specific_sku_properties GoogleComputeFutureReservation#specific_sku_properties}
        '''
        result = self._values.get("specific_sku_properties")
        return typing.cast(typing.Optional["GoogleComputeFutureReservationSpecificSkuProperties"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeFutureReservationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#timeouts GoogleComputeFutureReservation#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeFutureReservationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationShareSettings",
    jsii_struct_bases=[],
    name_mapping={
        "project_map": "projectMap",
        "projects": "projects",
        "share_type": "shareType",
    },
)
class GoogleComputeFutureReservationShareSettings:
    def __init__(
        self,
        *,
        project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeFutureReservationShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        share_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project_map: project_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#project_map GoogleComputeFutureReservation#project_map}
        :param projects: list of Project names to specify consumer projects for this shared-reservation. This is only valid when shareType's value is SPECIFIC_PROJECTS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#projects GoogleComputeFutureReservation#projects}
        :param share_type: Type of sharing for this future reservation. Possible values: ["LOCAL", "SPECIFIC_PROJECTS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#share_type GoogleComputeFutureReservation#share_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbefe66851cc40796cce17897c184afbce2cee6a71582314549a69766b2b2dc3)
            check_type(argname="argument project_map", value=project_map, expected_type=type_hints["project_map"])
            check_type(argname="argument projects", value=projects, expected_type=type_hints["projects"])
            check_type(argname="argument share_type", value=share_type, expected_type=type_hints["share_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project_map is not None:
            self._values["project_map"] = project_map
        if projects is not None:
            self._values["projects"] = projects
        if share_type is not None:
            self._values["share_type"] = share_type

    @builtins.property
    def project_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeFutureReservationShareSettingsProjectMap"]]]:
        '''project_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#project_map GoogleComputeFutureReservation#project_map}
        '''
        result = self._values.get("project_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeFutureReservationShareSettingsProjectMap"]]], result)

    @builtins.property
    def projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''list of Project names to specify consumer projects for this shared-reservation.

        This is only valid when shareType's value is SPECIFIC_PROJECTS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#projects GoogleComputeFutureReservation#projects}
        '''
        result = self._values.get("projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def share_type(self) -> typing.Optional[builtins.str]:
        '''Type of sharing for this future reservation. Possible values: ["LOCAL", "SPECIFIC_PROJECTS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#share_type GoogleComputeFutureReservation#share_type}
        '''
        result = self._values.get("share_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationShareSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationShareSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationShareSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1311a2184c1ec3f12f170c4b19e727724610a42d85a16087a1b1e760a1e54e80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProjectMap")
    def put_project_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeFutureReservationShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9ed9f0757c22de3948a6bf26636f603d13ec9b21e720be6d1ec3e95bd748b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProjectMap", [value]))

    @jsii.member(jsii_name="resetProjectMap")
    def reset_project_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectMap", []))

    @jsii.member(jsii_name="resetProjects")
    def reset_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjects", []))

    @jsii.member(jsii_name="resetShareType")
    def reset_share_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareType", []))

    @builtins.property
    @jsii.member(jsii_name="projectMap")
    def project_map(
        self,
    ) -> "GoogleComputeFutureReservationShareSettingsProjectMapList":
        return typing.cast("GoogleComputeFutureReservationShareSettingsProjectMapList", jsii.get(self, "projectMap"))

    @builtins.property
    @jsii.member(jsii_name="projectMapInput")
    def project_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeFutureReservationShareSettingsProjectMap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeFutureReservationShareSettingsProjectMap"]]], jsii.get(self, "projectMapInput"))

    @builtins.property
    @jsii.member(jsii_name="projectsInput")
    def projects_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectsInput"))

    @builtins.property
    @jsii.member(jsii_name="shareTypeInput")
    def share_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="projects")
    def projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projects"))

    @projects.setter
    def projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ff58b494cee9a6e57da2024ed6fa4f2bc4a6a02f38eae7a94755656cb8e0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareType")
    def share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareType"))

    @share_type.setter
    def share_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a429b5fd36023984dcd44e1a8c87a9e72db5de42678075cfb7813a431bd7d438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationShareSettings]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationShareSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationShareSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8994caf5f4eff8b700336d74de816c2fa36d8d260713c95e944a3f3a3c18be15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationShareSettingsProjectMap",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "project_id": "projectId"},
)
class GoogleComputeFutureReservationShareSettingsProjectMap:
    def __init__(
        self,
        *,
        id: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#id GoogleComputeFutureReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_id: The project ID, should be same as the key of this project config in the parent map. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#project_id GoogleComputeFutureReservation#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbfce69fa5a24900ea3f22f830d8cc80d3050e0979b2607dacfa68364f83e57)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#id GoogleComputeFutureReservation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The project ID, should be same as the key of this project config in the parent map.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#project_id GoogleComputeFutureReservation#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationShareSettingsProjectMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationShareSettingsProjectMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationShareSettingsProjectMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__becc19e5539187f580d76a322c7dda8c5dafab9804bd657ef5fd3c0cf48d4423)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationShareSettingsProjectMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c562e088d7b996ec7618313e35ce734b43dc3d76e874e4dcf6d490999f2ff502)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationShareSettingsProjectMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8576ab388e0aa62b986793687e98fe6d99e9cb1a2419559b015e4720bd4eb5ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b2d4e21d0554353651992c96fbe0750213f2f71530eb615953a01192896adca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9e6062f117461a12cb7f03e3273fa65fbfce77b4ed5674aecb88f45ed83eed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationShareSettingsProjectMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationShareSettingsProjectMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationShareSettingsProjectMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00c3ef996ed0e32678e65bd35ab3dcc88bb944bf2bdbb70d9fea9e3248ec1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationShareSettingsProjectMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationShareSettingsProjectMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db065e8989704a18ce0a951880b22db25ec970eea066b0498ba058bc612c0b84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6d0858ad48214e0b05b8d946cbbc59a898321ef710822cfd9b5449ff7e811a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553761455bd1fbe47c017859f34796a49ad9464353b4f4fb73ee6cabe1b45507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationShareSettingsProjectMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationShareSettingsProjectMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationShareSettingsProjectMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29b015007370183a221ea3ce2ac38f949022d8dea2c7c504b783acc40b51e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuProperties",
    jsii_struct_bases=[],
    name_mapping={
        "instance_properties": "instanceProperties",
        "source_instance_template": "sourceInstanceTemplate",
        "total_count": "totalCount",
    },
)
class GoogleComputeFutureReservationSpecificSkuProperties:
    def __init__(
        self,
        *,
        instance_properties: typing.Optional[typing.Union["GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        source_instance_template: typing.Optional[builtins.str] = None,
        total_count: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_properties: instance_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#instance_properties GoogleComputeFutureReservation#instance_properties}
        :param source_instance_template: The instance template that will be used to populate the ReservedInstanceProperties of the future reservation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#source_instance_template GoogleComputeFutureReservation#source_instance_template}
        :param total_count: Total number of instances for which capacity assurance is requested at a future time period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#total_count GoogleComputeFutureReservation#total_count}
        '''
        if isinstance(instance_properties, dict):
            instance_properties = GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties(**instance_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c548aa79433bfd8237defbab0b46efa786fdbda7f4ab5bd954eb0b360faa22c5)
            check_type(argname="argument instance_properties", value=instance_properties, expected_type=type_hints["instance_properties"])
            check_type(argname="argument source_instance_template", value=source_instance_template, expected_type=type_hints["source_instance_template"])
            check_type(argname="argument total_count", value=total_count, expected_type=type_hints["total_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_properties is not None:
            self._values["instance_properties"] = instance_properties
        if source_instance_template is not None:
            self._values["source_instance_template"] = source_instance_template
        if total_count is not None:
            self._values["total_count"] = total_count

    @builtins.property
    def instance_properties(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties"]:
        '''instance_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#instance_properties GoogleComputeFutureReservation#instance_properties}
        '''
        result = self._values.get("instance_properties")
        return typing.cast(typing.Optional["GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties"], result)

    @builtins.property
    def source_instance_template(self) -> typing.Optional[builtins.str]:
        '''The instance template that will be used to populate the ReservedInstanceProperties of the future reservation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#source_instance_template GoogleComputeFutureReservation#source_instance_template}
        '''
        result = self._values.get("source_instance_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def total_count(self) -> typing.Optional[builtins.str]:
        '''Total number of instances for which capacity assurance is requested at a future time period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#total_count GoogleComputeFutureReservation#total_count}
        '''
        result = self._values.get("total_count")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationSpecificSkuProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties",
    jsii_struct_bases=[],
    name_mapping={
        "guest_accelerators": "guestAccelerators",
        "local_ssds": "localSsds",
        "location_hint": "locationHint",
        "machine_type": "machineType",
        "maintenance_freeze_duration_hours": "maintenanceFreezeDurationHours",
        "maintenance_interval": "maintenanceInterval",
        "min_cpu_platform": "minCpuPlatform",
    },
)
class GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties:
    def __init__(
        self,
        *,
        guest_accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        local_ssds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        location_hint: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        maintenance_freeze_duration_hours: typing.Optional[jsii.Number] = None,
        maintenance_interval: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param guest_accelerators: guest_accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#guest_accelerators GoogleComputeFutureReservation#guest_accelerators}
        :param local_ssds: local_ssds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#local_ssds GoogleComputeFutureReservation#local_ssds}
        :param location_hint: An opaque location hint used to place the allocation close to other resources. This field is for use by internal tools that use the public API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#location_hint GoogleComputeFutureReservation#location_hint}
        :param machine_type: Specifies type of machine (name only) which has fixed number of vCPUs and fixed amount of memory. This also includes specifying custom machine type following custom-NUMBER_OF_CPUS-AMOUNT_OF_MEMORY pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#machine_type GoogleComputeFutureReservation#machine_type}
        :param maintenance_freeze_duration_hours: Specifies the number of hours after reservation creation where instances using the reservation won't be scheduled for maintenance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#maintenance_freeze_duration_hours GoogleComputeFutureReservation#maintenance_freeze_duration_hours}
        :param maintenance_interval: Specifies the frequency of planned maintenance events. The accepted values are: PERIODIC Possible values: ["PERIODIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#maintenance_interval GoogleComputeFutureReservation#maintenance_interval}
        :param min_cpu_platform: Minimum cpu platform the reservation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#min_cpu_platform GoogleComputeFutureReservation#min_cpu_platform}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e57d23fab88c8fdea736df8760db33c8443c73843f8e99188354d4dc8394f00)
            check_type(argname="argument guest_accelerators", value=guest_accelerators, expected_type=type_hints["guest_accelerators"])
            check_type(argname="argument local_ssds", value=local_ssds, expected_type=type_hints["local_ssds"])
            check_type(argname="argument location_hint", value=location_hint, expected_type=type_hints["location_hint"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument maintenance_freeze_duration_hours", value=maintenance_freeze_duration_hours, expected_type=type_hints["maintenance_freeze_duration_hours"])
            check_type(argname="argument maintenance_interval", value=maintenance_interval, expected_type=type_hints["maintenance_interval"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if guest_accelerators is not None:
            self._values["guest_accelerators"] = guest_accelerators
        if local_ssds is not None:
            self._values["local_ssds"] = local_ssds
        if location_hint is not None:
            self._values["location_hint"] = location_hint
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if maintenance_freeze_duration_hours is not None:
            self._values["maintenance_freeze_duration_hours"] = maintenance_freeze_duration_hours
        if maintenance_interval is not None:
            self._values["maintenance_interval"] = maintenance_interval
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform

    @builtins.property
    def guest_accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators"]]]:
        '''guest_accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#guest_accelerators GoogleComputeFutureReservation#guest_accelerators}
        '''
        result = self._values.get("guest_accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators"]]], result)

    @builtins.property
    def local_ssds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds"]]]:
        '''local_ssds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#local_ssds GoogleComputeFutureReservation#local_ssds}
        '''
        result = self._values.get("local_ssds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds"]]], result)

    @builtins.property
    def location_hint(self) -> typing.Optional[builtins.str]:
        '''An opaque location hint used to place the allocation close to other resources.

        This field is for use by internal tools that use the public API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#location_hint GoogleComputeFutureReservation#location_hint}
        '''
        result = self._values.get("location_hint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Specifies type of machine (name only) which has fixed number of vCPUs and fixed amount of memory.

        This also includes specifying custom machine type following custom-NUMBER_OF_CPUS-AMOUNT_OF_MEMORY pattern.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#machine_type GoogleComputeFutureReservation#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_freeze_duration_hours(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of hours after reservation creation where instances using the reservation won't be scheduled for maintenance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#maintenance_freeze_duration_hours GoogleComputeFutureReservation#maintenance_freeze_duration_hours}
        '''
        result = self._values.get("maintenance_freeze_duration_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maintenance_interval(self) -> typing.Optional[builtins.str]:
        '''Specifies the frequency of planned maintenance events. The accepted values are: PERIODIC Possible values: ["PERIODIC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#maintenance_interval GoogleComputeFutureReservation#maintenance_interval}
        '''
        result = self._values.get("maintenance_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Minimum cpu platform the reservation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#min_cpu_platform GoogleComputeFutureReservation#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of the guest accelerator cards exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#accelerator_count GoogleComputeFutureReservation#accelerator_count}
        :param accelerator_type: Full or partial URL of the accelerator type resource to attach to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#accelerator_type GoogleComputeFutureReservation#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe819a2ab84c429624672c4575f9beb582e7d4a9815ecfed205eaefa470a0e0f)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type

    @builtins.property
    def accelerator_count(self) -> typing.Optional[jsii.Number]:
        '''The number of the guest accelerator cards exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#accelerator_count GoogleComputeFutureReservation#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Full or partial URL of the accelerator type resource to attach to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#accelerator_type GoogleComputeFutureReservation#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1f5fa0646934fb5411459d02837e9b76b2750415f46cfbf031415c87ec86ddd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42cfdc29f450f3d912096ecd513ffa86db5e893dc2a455ffd4c69bee85c0dc1b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01569b5ae552bce7885af3e86990b44fcfd6f724488ca98e33eba053bf4518b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__653f60c997c92d286c553d118400cfd6e3b6bdd24378ad005f0a5a53b467b867)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f9d27f62e7a293ecee5e3528672bc5ee5e56c7295ac05e6c68ab52018d75d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da64b8df49e86c6cfc673228f4b232369ce51abc315c4a81720e4e89026823df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd92d4ca6663bde116fe0016012ba02ddd010e3a82bd46ebc9fb90e8b3e61b55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdea0ebe02623b2a27fab08f68db951bff1915a5b60ceed453503e444d8d9fe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58582fda51ea8877359fa2ac426f41b150edfa1c7e2a32dc44af01d42b7eb1f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e457b83466953c23bd3f72631321e6eb0306626f629eaddc0924e64ca6129859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds",
    jsii_struct_bases=[],
    name_mapping={"disk_size_gb": "diskSizeGb", "interface": "interface"},
)
class GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds:
    def __init__(
        self,
        *,
        disk_size_gb: typing.Optional[builtins.str] = None,
        interface: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: Specifies the size of the disk in base-2 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#disk_size_gb GoogleComputeFutureReservation#disk_size_gb}
        :param interface: Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. The default is SCSI. Possible values: ["SCSI", "NVME"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#interface GoogleComputeFutureReservation#interface}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ee80d7ba1a0563dae3039934d31503ca87bfef1a085b20ab1cb72bb8847508)
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if interface is not None:
            self._values["interface"] = interface

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[builtins.str]:
        '''Specifies the size of the disk in base-2 GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#disk_size_gb GoogleComputeFutureReservation#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface(self) -> typing.Optional[builtins.str]:
        '''Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME.

        The default is SCSI. Possible values: ["SCSI", "NVME"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#interface GoogleComputeFutureReservation#interface}
        '''
        result = self._values.get("interface")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__069c5f9fffbdbd9ab4435ca1d347c9025ef1d3dc0dcef48e2cf842a4c0b1b7a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a258c974112d285435a209c97d14cb84ce33747dae19ae712eca4fee807b4cdf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c097fa49080d998d19685f0df567c7efd18de27422a13e40ef9fc13cf35cbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__115b155e4177291a79d5ca6b0db7ecac19a5ba064a15dce74c55fa2aaae789b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ec2cd572a58dc9c27621ef3822bd524d9ed02febc1fb8c87d37a6152be1470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c194cca5dd8f836b689ab58c1fb0fcdd5cce0002d1434b213cce3536ac16274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e14f57acafd881c26ce282903abba51c3da846e9b2d2995f01345836a12d1e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetInterface")
    def reset_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterface", []))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceInput")
    def interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c440fd6c099e0ffb5f367e6e2565366610554b86865015d8dba4a88bc636b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de83ed76d4742675161bb80bc69fbd792171b47aeae12d2cfe3f9b424cd70d82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e92e03d5e53f29bc6f794194dca25275dce44b8b1046e2a4e17a4e86716b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38034ec4013ccaab007698372f9679064fb114a46f86101985a307ae6ebb5fc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGuestAccelerators")
    def put_guest_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045c9052e97131c2d9c19565a019d4ad433c92374f383324b4dc071b98d6ad4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestAccelerators", [value]))

    @jsii.member(jsii_name="putLocalSsds")
    def put_local_ssds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a12da8657a2999e81735c90d5c8f7ee23eea85dc47bb91d562ae0ac87e52eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocalSsds", [value]))

    @jsii.member(jsii_name="resetGuestAccelerators")
    def reset_guest_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestAccelerators", []))

    @jsii.member(jsii_name="resetLocalSsds")
    def reset_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsds", []))

    @jsii.member(jsii_name="resetLocationHint")
    def reset_location_hint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationHint", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMaintenanceFreezeDurationHours")
    def reset_maintenance_freeze_duration_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceFreezeDurationHours", []))

    @jsii.member(jsii_name="resetMaintenanceInterval")
    def reset_maintenance_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceInterval", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @builtins.property
    @jsii.member(jsii_name="guestAccelerators")
    def guest_accelerators(
        self,
    ) -> GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList:
        return typing.cast(GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList, jsii.get(self, "guestAccelerators"))

    @builtins.property
    @jsii.member(jsii_name="localSsds")
    def local_ssds(
        self,
    ) -> GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsList:
        return typing.cast(GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsList, jsii.get(self, "localSsds"))

    @builtins.property
    @jsii.member(jsii_name="guestAcceleratorsInput")
    def guest_accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]]], jsii.get(self, "guestAcceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdsInput")
    def local_ssds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]]], jsii.get(self, "localSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationHintInput")
    def location_hint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationHintInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceFreezeDurationHoursInput")
    def maintenance_freeze_duration_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maintenanceFreezeDurationHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceIntervalInput")
    def maintenance_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="locationHint")
    def location_hint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locationHint"))

    @location_hint.setter
    def location_hint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cc3550094881dec89a644b9c0962b0954fbaad0e83438ee07f2fa1cbd0b816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationHint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fb7cee12380caa575eeace0b6c7f6a4b9df43583f6dabdfa15ce83486ad9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceFreezeDurationHours")
    def maintenance_freeze_duration_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maintenanceFreezeDurationHours"))

    @maintenance_freeze_duration_hours.setter
    def maintenance_freeze_duration_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c735125a3a166cc49804725cb67a275d16489709dac1383e03d70d6978c5bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceFreezeDurationHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceInterval")
    def maintenance_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceInterval"))

    @maintenance_interval.setter
    def maintenance_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6005b71af19b3a1a045bf3f03dd52a562035d1c1d47019ecd8123871c8f1b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263978a17325c1c8be743d79b9fc39a75647c556e97f1fc13cbb822279afe3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70498a6381d92a3c9c3c5269a122bff0ecc112cdfd8c5e723a4df66c30c478d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationSpecificSkuPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationSpecificSkuPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33e549d7337ff09cbfad8a1272a2e59a2b619d2b0c43f7e7c820f1e5ee344bf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceProperties")
    def put_instance_properties(
        self,
        *,
        guest_accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        local_ssds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds, typing.Dict[builtins.str, typing.Any]]]]] = None,
        location_hint: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        maintenance_freeze_duration_hours: typing.Optional[jsii.Number] = None,
        maintenance_interval: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param guest_accelerators: guest_accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#guest_accelerators GoogleComputeFutureReservation#guest_accelerators}
        :param local_ssds: local_ssds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#local_ssds GoogleComputeFutureReservation#local_ssds}
        :param location_hint: An opaque location hint used to place the allocation close to other resources. This field is for use by internal tools that use the public API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#location_hint GoogleComputeFutureReservation#location_hint}
        :param machine_type: Specifies type of machine (name only) which has fixed number of vCPUs and fixed amount of memory. This also includes specifying custom machine type following custom-NUMBER_OF_CPUS-AMOUNT_OF_MEMORY pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#machine_type GoogleComputeFutureReservation#machine_type}
        :param maintenance_freeze_duration_hours: Specifies the number of hours after reservation creation where instances using the reservation won't be scheduled for maintenance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#maintenance_freeze_duration_hours GoogleComputeFutureReservation#maintenance_freeze_duration_hours}
        :param maintenance_interval: Specifies the frequency of planned maintenance events. The accepted values are: PERIODIC Possible values: ["PERIODIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#maintenance_interval GoogleComputeFutureReservation#maintenance_interval}
        :param min_cpu_platform: Minimum cpu platform the reservation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#min_cpu_platform GoogleComputeFutureReservation#min_cpu_platform}
        '''
        value = GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties(
            guest_accelerators=guest_accelerators,
            local_ssds=local_ssds,
            location_hint=location_hint,
            machine_type=machine_type,
            maintenance_freeze_duration_hours=maintenance_freeze_duration_hours,
            maintenance_interval=maintenance_interval,
            min_cpu_platform=min_cpu_platform,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceProperties", [value]))

    @jsii.member(jsii_name="resetInstanceProperties")
    def reset_instance_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceProperties", []))

    @jsii.member(jsii_name="resetSourceInstanceTemplate")
    def reset_source_instance_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceInstanceTemplate", []))

    @jsii.member(jsii_name="resetTotalCount")
    def reset_total_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalCount", []))

    @builtins.property
    @jsii.member(jsii_name="instanceProperties")
    def instance_properties(
        self,
    ) -> GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesOutputReference:
        return typing.cast(GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesOutputReference, jsii.get(self, "instanceProperties"))

    @builtins.property
    @jsii.member(jsii_name="instancePropertiesInput")
    def instance_properties_input(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties], jsii.get(self, "instancePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceTemplateInput")
    def source_instance_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInstanceTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="totalCountInput")
    def total_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "totalCountInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceTemplate")
    def source_instance_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstanceTemplate"))

    @source_instance_template.setter
    def source_instance_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d429fd480f53c937b130acfe08101b5fd25fe95168d9c8d09b9416f2b53c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceInstanceTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalCount")
    def total_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalCount"))

    @total_count.setter
    def total_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cea6a463eea819df5ba8fcaca4ff7238770f4e84eb6019583eb2b8a81b3c152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationSpecificSkuProperties]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationSpecificSkuProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationSpecificSkuProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b75a3edc40a0c056e997143a548662eecb4fdf2afbcf99cadc44bdecc4f2017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cccb04f1eafbe5610a30274207e31a44ee148fa54e7bc58e3252c4881c6d80c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d5435031920eee4549121292851681f54d77523bd296a4f0644eb31950b6c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66b79178194b456d7e8da0cf2a2de4ccbf91ec42be4b0753e9ba3c80ab20cd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__951ee0584c1a114d7a345315edcc0d7b8bdd2710777cb25e00234e7de795ff26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e827112cad89af45520c424f70281cc4a736cc6fa06d704559384ff6bebc14b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe31d37d46c09a52934520939ca5b99f7312c3bd8dfda8f2c193352f9cf3fa2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "count"))

    @builtins.property
    @jsii.member(jsii_name="timeStamp")
    def time_stamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeStamp"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfo]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c353c064d8d6c791b63fe34d5e7298976d3d70b0c3edfd7dadedd5e350189c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecs",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7ea45f259552a6378b3d2796b0b04ef109683b21fdf615718a9473a734270ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780ac12b8db880c45a87e90138b59f49bc160ea1521c6f4bb5787e86ca242130)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd7df8144630bda4dc42f35331bb81348692ce080a4aab98bea10e7cbc024ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51de3c77e757ce4816aa3cebbe673682bae17237483e6e4594639a6b516e3dec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32729b37470813e4c2d21a44a60a0f693b55259307b7ba302fa48484c36421bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceb3834253a4ea8992ced9d5f93cc6a4cae9158af98e5e01e24928105f3e7e75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="shareSettings")
    def share_settings(
        self,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsList":
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsList", jsii.get(self, "shareSettings"))

    @builtins.property
    @jsii.member(jsii_name="specificSkuProperties")
    def specific_sku_properties(
        self,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesList":
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesList", jsii.get(self, "specificSkuProperties"))

    @builtins.property
    @jsii.member(jsii_name="timeWindow")
    def time_window(
        self,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowList":
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowList", jsii.get(self, "timeWindow"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecs]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44cd3665cb5af27cb857cabb63c66110cf9e319784dee5672dcbde8e75aa1fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettings",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9c469ce17b08d22485bb25ec6d6175b75d9b9943881b636b797ed24b1844d3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf839e14cca61cfa7275c6e05376c60ca7f0c1fc2075ce4e02d7cddda5c1519a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f99365257208c855584bd562ec1b2ef7a94adf74ad0d6230542f46269d433a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2be164cb292b1a8c834c3563af62eaca0470abcded641481dcc132ab3ee5c980)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ed970e28a18fb50024c0a1af893e6b4661af6fede33fd17dcbc10664e20663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0c9e7b597ca5aa03352a6277c646d08986e3073f7dfcd09a3c78bf0beae18a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="projectMap")
    def project_map(
        self,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapList":
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapList", jsii.get(self, "projectMap"))

    @builtins.property
    @jsii.member(jsii_name="projects")
    def projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projects"))

    @builtins.property
    @jsii.member(jsii_name="shareType")
    def share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettings]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f07580748ac957a3325845167c885b7e95dfacb6d6f2bbf4e17a4f73b531f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMap",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMap:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__750c8788a23383d7ec95c290e872a9c510eee6d6fa7fcb5c3e475e65979f205c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a66fd334eff8ef1561c34fa8c405ef381a727acf97697d46b670d2cfaa4cdfa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72be4180320c2fb7a292712bfb964fc02937cd38516dc6bef5165ffa23631a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e42636b230d65a33f8ac6344a7a0b8c379b9a034509753ad4acee8676cc3e997)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c7716de7b4114646df5a0f4817088d8797715cbd53c7931e6f7e754a95b0287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8c7595c06bf81281e7b78cbda3f1c55a732ea63d4ae351bbd32e122a0658439)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMap]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21aee030a8a2e73e7820f98f2a6cea7ca007192e7d4eeb08b5a24b221520f915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuProperties",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuProperties:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstanceProperties",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstanceProperties:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstanceProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAccelerators",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAccelerators:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21f2bc58b27128aebe946fe88936aac0976328b955574073e612c2ae6cb503c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d6f7bb734aea0c3c98786cc0169f04390ac6470cea17d0208e85dccd21aeaf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad19f910cd061cee37251fcdea0b738b18ab11dfb198a6b5ba528608aa367e05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8f70b1372e5c683c1b7022262249cc8a16e98c0c9f7a8ed0ed77bd93de0aa44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6ffa6158629f2cf9412c889da4f66db226814409d88dc3c78469009368a39be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3da5f7f686123bea8ae868ba5fea3f38192a1989a383fc40a76bd471877bfb65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAccelerators]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAccelerators], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAccelerators],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34f8b5d5928f8d925337293eccbdaff1adaf1b7f3af17485b9ad1e7a66e5c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abd1c84e507cbe949ad582c1f825cf86789921429a20c43cf44c65f20e381d4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cdcfb78c3c42b650093c7f2132891ff4f39006a268d48f071e5c260e2026547)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c94ddb5fc3bc8ad82fa1f174571d994bfe027864ebf5b6af68afcf67bc4c00e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67f1680e8258399207e2a4681a31e944cad12e94cb4a195142700c8db924b696)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d780906ca92379702367cecc9b0984cd94539e5d9244b4702a2cee5b71d387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsds",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__479bb4e13e4b15c9c023747637f651e595dfef0a50256a55f37d239d71dd077c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86723df458881e80275c7f9a256f68be951db5cf223cf9ed474dafd1c7d50d7c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5effe8f8fcdd7dd24be5d3f274be79ed3ef5deefbb0440ece967456f4589017)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72525a9dbf1deefca746147c57e1d6f167a32f062e65c4c80fb53bf49d2b8b97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f228aefa2d31000fe52b2fffc6bc7453baf74b1d306e6727a6cc5d9193a7e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8639ca52cc8b23b30bda8058e54c495153b52cc9301167352026df45f00a91e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsds]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3c941e61d24a5030b8695957c076bf0b77ca4172ba0c97a568073ab3d39454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b10ccdf3bdafec05c6cfcef58c98127b4931b0f45c504bfcdf1e2c426b85b9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="guestAccelerators")
    def guest_accelerators(
        self,
    ) -> GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList:
        return typing.cast(GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList, jsii.get(self, "guestAccelerators"))

    @builtins.property
    @jsii.member(jsii_name="localSsds")
    def local_ssds(
        self,
    ) -> GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsList:
        return typing.cast(GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsList, jsii.get(self, "localSsds"))

    @builtins.property
    @jsii.member(jsii_name="locationHint")
    def location_hint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locationHint"))

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceFreezeDurationHours")
    def maintenance_freeze_duration_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maintenanceFreezeDurationHours"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceInterval")
    def maintenance_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceInterval"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstanceProperties]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstanceProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstanceProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37551b0e04001e35f8f262619fc8616c407da8cd519d6950dfec51991dcdb6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03911efad67b6d16f511833562a9dd95f3dbccdae3fc3b7b21538260379b667e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8742082cbd42f9049e12b2c3d3f16cf34e0cc29b62dd23839b2c5fcbf7ecf482)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633ca5ee3179684a2ff8d4240ba1e5db85b47e441b27e1069b6f98288f3f5c6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eacb20a5e66bcb44ef0296eccb7ed01169365882695893d2709706fda48f8f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b120c77d0ea8687bdb93f7482b237db3dfad4215d5f2ad4f4db8ae3f9178345f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0547cd3e8ead09354dee39393f944e8640d7a951a906ab285632d5518410cdd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="instanceProperties")
    def instance_properties(
        self,
    ) -> GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesList:
        return typing.cast(GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesList, jsii.get(self, "instanceProperties"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceTemplate")
    def source_instance_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstanceTemplate"))

    @builtins.property
    @jsii.member(jsii_name="totalCount")
    def total_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuProperties]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f928f9815c57bc4aa202a0d45fbeac670e322d2d4c30f81d7d5ebea5c6997ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindow",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindow:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDuration",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDuration:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f87307b4fc742fc92c35cec5402c271f67ff98973cd59348dedf7ecc4d166ba8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010118a4dcab36afedb3fba000bc7f6e60207ec952c30794cb678cc0dafc30cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9febc53986aad95f283988e0982be3b210e0835fdd247db1e07d28156a9f10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd80809f29db1316ddf522fbef0b6f7dbf3091b66fb389f11925cacefca70e4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b916fadc2bd531b36b6d575699edc74d65767e5fee77a3dbd54de91b24eb1681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e1dca202d341a12fa8444dfd06725d88e485e847e2e549ad824c178bdc7d366)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "seconds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDuration]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a771795bdb517ab9fe82eb58f1641b8d8fc21d87800b577480c4d794b645d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bf3c6d568132eab8ce9cf9cf5b5bf0b195a4ee7afdd8b31954af56f951b9a85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d750fb633256b27a6075b53bd5df97f74d2dacc9602dc5f5cea1fc254db036e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a542cbd924c051206a5e49aee2633c3fe611b80f25b5a9d27a6b4ce625be6d21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d457eac8b316e8ac3a36e24bc70a17011fb20ab1ff51ee6b48651237b7e9bcbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46c4fee0dd62b6c4f6356f60588fc1f811bfdf6700e4430aa180156689671887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abf9874413714f13deb3144399231b2d1500b464d8ddd1b5bf1227a58bc61dfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(
        self,
    ) -> GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationList:
        return typing.cast(GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationList, jsii.get(self, "duration"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindow]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4942dd5808dc601749920ccdd78f0ca656424f02694e0eb3f42c9073d9d1392e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__510ae0d6880daaeb40d1876b533d23c4510188cfc6b7fa2f586eb71d0a6c0e7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusLastKnownGoodStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280cf1e07e870c3ac475f9b821b0b0f93a41d66d571582521f769e5eadfc0c5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusLastKnownGoodStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edeca47e0b28e0c2be3d4bfe2d772004341999227d60b97003c13ad3b08eade0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c4dda0dfd3634adf5bbd9dd3a810ebb8f1ee508c8150315b755379fde9e21f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a32bb2c172f43eb96d7c5c7488bda103f0ac98be5387740c48c9e1564414dda5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusLastKnownGoodStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusLastKnownGoodStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f104ac053f03a54f5915f0cc6daa9013e870879252629ed42f8437f2f94d749a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="existingMatchingUsageInfo")
    def existing_matching_usage_info(
        self,
    ) -> GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoList:
        return typing.cast(GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoList, jsii.get(self, "existingMatchingUsageInfo"))

    @builtins.property
    @jsii.member(jsii_name="futureReservationSpecs")
    def future_reservation_specs(
        self,
    ) -> GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsList:
        return typing.cast(GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsList, jsii.get(self, "futureReservationSpecs"))

    @builtins.property
    @jsii.member(jsii_name="lockTime")
    def lock_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockTime"))

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @builtins.property
    @jsii.member(jsii_name="procurementStatus")
    def procurement_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "procurementStatus"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodState]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1efb2385814bba8f272613e3f5b38546765c8a6fd58db770e8bf97b6b3f1840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65d4ee27f751def1301ecf4331a7aded4fb87cd753274a4d01add6d68995aef1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea3a640e9619ce203ac9fa57952c1ec556730bbfbabf483c2f2cb4cb26f06a7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fc4b0d2a4d43bd2f3b3e6b6dbe36c0bc4e4f3cbab6f716233a7b7fba0094df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9c84e2c7fd60bc500b8e2c0533255ad4cabf85bbdc70aba16c153d8601e00ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5df1e36c45e0a565eb49fe2f8e5c808973637e2482ff2b9ee7ed2d1df15a35c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a72125e57938b10e1595899af05ce9e46f772b4ad0dcdf366d2bc06600124c0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="amendmentStatus")
    def amendment_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "amendmentStatus"))

    @builtins.property
    @jsii.member(jsii_name="autoCreatedReservations")
    def auto_created_reservations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "autoCreatedReservations"))

    @builtins.property
    @jsii.member(jsii_name="fulfilledCount")
    def fulfilled_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fulfilledCount"))

    @builtins.property
    @jsii.member(jsii_name="lastKnownGoodState")
    def last_known_good_state(
        self,
    ) -> GoogleComputeFutureReservationStatusLastKnownGoodStateList:
        return typing.cast(GoogleComputeFutureReservationStatusLastKnownGoodStateList, jsii.get(self, "lastKnownGoodState"))

    @builtins.property
    @jsii.member(jsii_name="lockTime")
    def lock_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockTime"))

    @builtins.property
    @jsii.member(jsii_name="procurementStatus")
    def procurement_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "procurementStatus"))

    @builtins.property
    @jsii.member(jsii_name="specificSkuProperties")
    def specific_sku_properties(
        self,
    ) -> "GoogleComputeFutureReservationStatusSpecificSkuPropertiesList":
        return typing.cast("GoogleComputeFutureReservationStatusSpecificSkuPropertiesList", jsii.get(self, "specificSkuProperties"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeFutureReservationStatus]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fb745de9f0f27d26feb25775e27f5d0d8dd7c979714e634d017727f044cada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusSpecificSkuProperties",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleComputeFutureReservationStatusSpecificSkuProperties:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationStatusSpecificSkuProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationStatusSpecificSkuPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusSpecificSkuPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29cdb17b3d962616e0f1992a1fad02e86f4d7241d5a4c0d050b1f6667db4dee8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeFutureReservationStatusSpecificSkuPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939849e5e25b14abaa2d9b2d6695f746c876d193382f6f86c746e2d4e991ad5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeFutureReservationStatusSpecificSkuPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64beac041d9a2659344c43d5d8b4006943a86bd62735d220b29acae13d5f6e7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26b5402d9245a63cc8c4522426f376f8ec9b152cf60332d974d1bd40fb10fad7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae6e07a5c7d51083911f25d821bc49ed05e084dd357f8fccccfc7b4764f78a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationStatusSpecificSkuPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationStatusSpecificSkuPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59a625345fc0b7ffa7bae2596839833418b5c9aa1d5793ee320372114ce0004d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceTemplateId")
    def source_instance_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstanceTemplateId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationStatusSpecificSkuProperties]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationStatusSpecificSkuProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationStatusSpecificSkuProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac85a492d8502f033dd66312aeb191c7fd6b86e51bdf3e28b9c0286e33bb8d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationTimeWindow",
    jsii_struct_bases=[],
    name_mapping={
        "start_time": "startTime",
        "duration": "duration",
        "end_time": "endTime",
    },
)
class GoogleComputeFutureReservationTimeWindow:
    def __init__(
        self,
        *,
        start_time: builtins.str,
        duration: typing.Optional[typing.Union["GoogleComputeFutureReservationTimeWindowDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        end_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_time: Start time of the future reservation in RFC3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#start_time GoogleComputeFutureReservation#start_time}
        :param duration: duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#duration GoogleComputeFutureReservation#duration}
        :param end_time: End time of the future reservation in RFC3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#end_time GoogleComputeFutureReservation#end_time}
        '''
        if isinstance(duration, dict):
            duration = GoogleComputeFutureReservationTimeWindowDuration(**duration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2875f7031083d7865be0e77a35f79b47fcb20d02c3e1123cd5baa786902337f)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_time": start_time,
        }
        if duration is not None:
            self._values["duration"] = duration
        if end_time is not None:
            self._values["end_time"] = end_time

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Start time of the future reservation in RFC3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#start_time GoogleComputeFutureReservation#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(
        self,
    ) -> typing.Optional["GoogleComputeFutureReservationTimeWindowDuration"]:
        '''duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#duration GoogleComputeFutureReservation#duration}
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional["GoogleComputeFutureReservationTimeWindowDuration"], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''End time of the future reservation in RFC3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#end_time GoogleComputeFutureReservation#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationTimeWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationTimeWindowDuration",
    jsii_struct_bases=[],
    name_mapping={"nanos": "nanos", "seconds": "seconds"},
)
class GoogleComputeFutureReservationTimeWindowDuration:
    def __init__(
        self,
        *,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#nanos GoogleComputeFutureReservation#nanos}
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#seconds GoogleComputeFutureReservation#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b01026143f0e5f0fc694e693b9fa4f0c384498764a6c31cf268179608a5a08e)
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#nanos GoogleComputeFutureReservation#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[builtins.str]:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#seconds GoogleComputeFutureReservation#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationTimeWindowDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationTimeWindowDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationTimeWindowDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20f7f2a345174d532e47be4e1fbe9e32196ca5138b72f65e2583e8fb313fec46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a335e345d843eacf8ab5a2016b73f0427b0c8651637d86fc1eec9a1b4bd98364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a76ff8edecce09ed92b8e9412e55274fa2169ec3b2d1f6465d6bc7a54f2d7c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationTimeWindowDuration]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationTimeWindowDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationTimeWindowDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077b7059907a20d862932e98c6d99c2cf408d59c4a2fd6ac7bb930dd70ace549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeFutureReservationTimeWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationTimeWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__624de61be04c3cd28167e4a47622cd87f100ac27277a0c16ec0d92539feadc03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDuration")
    def put_duration(
        self,
        *,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#nanos GoogleComputeFutureReservation#nanos}
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#seconds GoogleComputeFutureReservation#seconds}
        '''
        value = GoogleComputeFutureReservationTimeWindowDuration(
            nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putDuration", [value]))

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(
        self,
    ) -> GoogleComputeFutureReservationTimeWindowDurationOutputReference:
        return typing.cast(GoogleComputeFutureReservationTimeWindowDurationOutputReference, jsii.get(self, "duration"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationTimeWindowDuration]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationTimeWindowDuration], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a46029e56890bfb27532e2d01299714ef9ef2acff2bfc3d60b27237ca9066a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45cead6b2f762afe0f22b180f34495f50995f6995ab0e2a7237b3e93b03a7635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeFutureReservationTimeWindow]:
        return typing.cast(typing.Optional[GoogleComputeFutureReservationTimeWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeFutureReservationTimeWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd8067643af1875a7bc07f9f3546853e621c528acf18b67318a798097d60866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeFutureReservationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#create GoogleComputeFutureReservation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#delete GoogleComputeFutureReservation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#update GoogleComputeFutureReservation#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1388e739f27e4a3a52236a23149d7ceaeaebf4c1b6e5ea915b2db6d3a22578)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#create GoogleComputeFutureReservation#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#delete GoogleComputeFutureReservation#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_future_reservation#update GoogleComputeFutureReservation#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeFutureReservationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeFutureReservationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeFutureReservation.GoogleComputeFutureReservationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01d729eeee424b3a71e6f08630aa5ba63d5d3265b84833af7ef5933b9b582711)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d2057a03624b58b22233b0c9695e13bf2afc85e345156fc6454fc689174000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f887ed3ed923e7029b7a48a3d9db5f0f7e1ee0293d4ebf203ab77281935d6f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5220ee1482f24f3fe87ff85d8d9bb325d13e712bb3f38db7133b5b4356db7e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7dd5800e8d017edd4726e7af692efaeb6b77a12f74dd8ccc7a3e146408ada0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeFutureReservation",
    "GoogleComputeFutureReservationAutoCreatedReservationsDuration",
    "GoogleComputeFutureReservationAutoCreatedReservationsDurationOutputReference",
    "GoogleComputeFutureReservationCommitmentInfo",
    "GoogleComputeFutureReservationCommitmentInfoOutputReference",
    "GoogleComputeFutureReservationConfig",
    "GoogleComputeFutureReservationShareSettings",
    "GoogleComputeFutureReservationShareSettingsOutputReference",
    "GoogleComputeFutureReservationShareSettingsProjectMap",
    "GoogleComputeFutureReservationShareSettingsProjectMapList",
    "GoogleComputeFutureReservationShareSettingsProjectMapOutputReference",
    "GoogleComputeFutureReservationSpecificSkuProperties",
    "GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties",
    "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators",
    "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList",
    "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference",
    "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds",
    "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsList",
    "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference",
    "GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesOutputReference",
    "GoogleComputeFutureReservationSpecificSkuPropertiesOutputReference",
    "GoogleComputeFutureReservationStatus",
    "GoogleComputeFutureReservationStatusLastKnownGoodState",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfo",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfoOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecs",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettings",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMap",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMapOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuProperties",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstanceProperties",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAccelerators",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAcceleratorsOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsds",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsdsOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindow",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDuration",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDurationOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowOutputReference",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateList",
    "GoogleComputeFutureReservationStatusLastKnownGoodStateOutputReference",
    "GoogleComputeFutureReservationStatusList",
    "GoogleComputeFutureReservationStatusOutputReference",
    "GoogleComputeFutureReservationStatusSpecificSkuProperties",
    "GoogleComputeFutureReservationStatusSpecificSkuPropertiesList",
    "GoogleComputeFutureReservationStatusSpecificSkuPropertiesOutputReference",
    "GoogleComputeFutureReservationTimeWindow",
    "GoogleComputeFutureReservationTimeWindowDuration",
    "GoogleComputeFutureReservationTimeWindowDurationOutputReference",
    "GoogleComputeFutureReservationTimeWindowOutputReference",
    "GoogleComputeFutureReservationTimeouts",
    "GoogleComputeFutureReservationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4bb039468e8a09425b894bb418f5aa093f552e5ee56a65a46597b18015baf26e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    time_window: typing.Union[GoogleComputeFutureReservationTimeWindow, typing.Dict[builtins.str, typing.Any]],
    auto_created_reservations_delete_time: typing.Optional[builtins.str] = None,
    auto_created_reservations_duration: typing.Optional[typing.Union[GoogleComputeFutureReservationAutoCreatedReservationsDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_delete_auto_created_reservations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commitment_info: typing.Optional[typing.Union[GoogleComputeFutureReservationCommitmentInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    planning_status: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_mode: typing.Optional[builtins.str] = None,
    reservation_name: typing.Optional[builtins.str] = None,
    scheduling_type: typing.Optional[builtins.str] = None,
    share_settings: typing.Optional[typing.Union[GoogleComputeFutureReservationShareSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    specific_reservation_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    specific_sku_properties: typing.Optional[typing.Union[GoogleComputeFutureReservationSpecificSkuProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeFutureReservationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__15cc4960866eb9b6d457db60884a63a683eb09314da56e15744c7c92d772284d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed84cc5f16293b3eb2e294fc309a37ba6f70dd2ce3abf3ec5577ed74e23c7ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664e21b6b7f8e0f381f6ccdc3a7af7809ee75b17fdac6afa23db965736d6b103(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c964772d5abeef6de4e93e06ef8f3b1d7e5bfdbbdf5ea39b3521a18bd62814(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9f5469126ad7d8634446edfea473cfa758f1854f366a8be10d0b40b9d83bee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a340980375f4b66a7706972da57b799a2ca77ff95d7257d3c7954b69db977d0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bbb4eb3617902c930cc910470e38fbbf4bf892e461aa28ce8951be3e2d44b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a21a18aef95022b39a1c6d74ddac3ae07fe4c292f83dffe50e9495398d35e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65379aea5c56b77afc4d000d3453b2b6118bcee67e904bab06588bb9f6d23f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272dd0f74e9b2652ffbcefe68d595af2f2b80e09fa9ffb3b52616bded9e4bdca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239896ae05554b9588071876f642fc765f98a8062e7539320259633187c3adbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b21f480538719cb0c6e384e8f590b4e5ed1ee2839822fd8b845b9bad52d1e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f26ea4dae4b95430a8c2419ca62474dd3bd04a03f922bb5e2179fea2daff8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fdb096818f2a480e3d7d94d4174dbe4a83d0e6b60cdba212bd85e3050e9971(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5941a957c783d71d9130fbb103f8b927824afebd1632f2fec3ea4beb3eda8091(
    *,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef0dc7981d06959c180c54904e128820dc3c54410990178a07c9085e81caf9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a35156df722a36017faf895ed07f8a3af5ee27258a999ec64750f224974a19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134cd778041f7fa81301e1e9e90aff74dd7f10f2d42a0f159dcc55d3fa28a5ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7efb019f4e3052b79acd05b4b63cb34aefcfb101d59994ce52e847dd0b1a49(
    value: typing.Optional[GoogleComputeFutureReservationAutoCreatedReservationsDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3efc9a8b21ac6b3f167a1c18c34667cc1eb25c1e0be178be3eb8fb855f6d00(
    *,
    commitment_name: typing.Optional[builtins.str] = None,
    commitment_plan: typing.Optional[builtins.str] = None,
    previous_commitment_terms: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815e4ea23943c8aab9973a4c8d2983dc8313bca6865f39579ce49dc3797440b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d098d24003a300b2a9fc4b14513e63eb2452e3aa9de111c7072c9ac7c00741f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bdeee8d2ef1144c05c68474c9c5a7a24fd82308a49836d756a701a22748d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ea30a96883fefa6d440966a3a4434d96a618b81b900890df04452b94505e3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea074f8ca72391591e3de79ebeb17f35c59fe94309725992f8739bfceb4d46b(
    value: typing.Optional[GoogleComputeFutureReservationCommitmentInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6e102566375c5d4d294a152f1ca65c0ba40fa4721d9283d1c532959486235c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    time_window: typing.Union[GoogleComputeFutureReservationTimeWindow, typing.Dict[builtins.str, typing.Any]],
    auto_created_reservations_delete_time: typing.Optional[builtins.str] = None,
    auto_created_reservations_duration: typing.Optional[typing.Union[GoogleComputeFutureReservationAutoCreatedReservationsDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_delete_auto_created_reservations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commitment_info: typing.Optional[typing.Union[GoogleComputeFutureReservationCommitmentInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    planning_status: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_mode: typing.Optional[builtins.str] = None,
    reservation_name: typing.Optional[builtins.str] = None,
    scheduling_type: typing.Optional[builtins.str] = None,
    share_settings: typing.Optional[typing.Union[GoogleComputeFutureReservationShareSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    specific_reservation_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    specific_sku_properties: typing.Optional[typing.Union[GoogleComputeFutureReservationSpecificSkuProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeFutureReservationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbefe66851cc40796cce17897c184afbce2cee6a71582314549a69766b2b2dc3(
    *,
    project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationShareSettingsProjectMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    share_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1311a2184c1ec3f12f170c4b19e727724610a42d85a16087a1b1e760a1e54e80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9ed9f0757c22de3948a6bf26636f603d13ec9b21e720be6d1ec3e95bd748b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationShareSettingsProjectMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ff58b494cee9a6e57da2024ed6fa4f2bc4a6a02f38eae7a94755656cb8e0f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a429b5fd36023984dcd44e1a8c87a9e72db5de42678075cfb7813a431bd7d438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8994caf5f4eff8b700336d74de816c2fa36d8d260713c95e944a3f3a3c18be15(
    value: typing.Optional[GoogleComputeFutureReservationShareSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbfce69fa5a24900ea3f22f830d8cc80d3050e0979b2607dacfa68364f83e57(
    *,
    id: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__becc19e5539187f580d76a322c7dda8c5dafab9804bd657ef5fd3c0cf48d4423(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c562e088d7b996ec7618313e35ce734b43dc3d76e874e4dcf6d490999f2ff502(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8576ab388e0aa62b986793687e98fe6d99e9cb1a2419559b015e4720bd4eb5ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2d4e21d0554353651992c96fbe0750213f2f71530eb615953a01192896adca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e6062f117461a12cb7f03e3273fa65fbfce77b4ed5674aecb88f45ed83eed7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00c3ef996ed0e32678e65bd35ab3dcc88bb944bf2bdbb70d9fea9e3248ec1a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationShareSettingsProjectMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db065e8989704a18ce0a951880b22db25ec970eea066b0498ba058bc612c0b84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6d0858ad48214e0b05b8d946cbbc59a898321ef710822cfd9b5449ff7e811a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553761455bd1fbe47c017859f34796a49ad9464353b4f4fb73ee6cabe1b45507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29b015007370183a221ea3ce2ac38f949022d8dea2c7c504b783acc40b51e87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationShareSettingsProjectMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c548aa79433bfd8237defbab0b46efa786fdbda7f4ab5bd954eb0b360faa22c5(
    *,
    instance_properties: typing.Optional[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    source_instance_template: typing.Optional[builtins.str] = None,
    total_count: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e57d23fab88c8fdea736df8760db33c8443c73843f8e99188354d4dc8394f00(
    *,
    guest_accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    local_ssds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location_hint: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    maintenance_freeze_duration_hours: typing.Optional[jsii.Number] = None,
    maintenance_interval: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe819a2ab84c429624672c4575f9beb582e7d4a9815ecfed205eaefa470a0e0f(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f5fa0646934fb5411459d02837e9b76b2750415f46cfbf031415c87ec86ddd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cfdc29f450f3d912096ecd513ffa86db5e893dc2a455ffd4c69bee85c0dc1b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01569b5ae552bce7885af3e86990b44fcfd6f724488ca98e33eba053bf4518b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653f60c997c92d286c553d118400cfd6e3b6bdd24378ad005f0a5a53b467b867(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f9d27f62e7a293ecee5e3528672bc5ee5e56c7295ac05e6c68ab52018d75d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da64b8df49e86c6cfc673228f4b232369ce51abc315c4a81720e4e89026823df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd92d4ca6663bde116fe0016012ba02ddd010e3a82bd46ebc9fb90e8b3e61b55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdea0ebe02623b2a27fab08f68db951bff1915a5b60ceed453503e444d8d9fe4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58582fda51ea8877359fa2ac426f41b150edfa1c7e2a32dc44af01d42b7eb1f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e457b83466953c23bd3f72631321e6eb0306626f629eaddc0924e64ca6129859(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ee80d7ba1a0563dae3039934d31503ca87bfef1a085b20ab1cb72bb8847508(
    *,
    disk_size_gb: typing.Optional[builtins.str] = None,
    interface: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069c5f9fffbdbd9ab4435ca1d347c9025ef1d3dc0dcef48e2cf842a4c0b1b7a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a258c974112d285435a209c97d14cb84ce33747dae19ae712eca4fee807b4cdf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c097fa49080d998d19685f0df567c7efd18de27422a13e40ef9fc13cf35cbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115b155e4177291a79d5ca6b0db7ecac19a5ba064a15dce74c55fa2aaae789b8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ec2cd572a58dc9c27621ef3822bd524d9ed02febc1fb8c87d37a6152be1470(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c194cca5dd8f836b689ab58c1fb0fcdd5cce0002d1434b213cce3536ac16274(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e14f57acafd881c26ce282903abba51c3da846e9b2d2995f01345836a12d1e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c440fd6c099e0ffb5f367e6e2565366610554b86865015d8dba4a88bc636b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de83ed76d4742675161bb80bc69fbd792171b47aeae12d2cfe3f9b424cd70d82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e92e03d5e53f29bc6f794194dca25275dce44b8b1046e2a4e17a4e86716b1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38034ec4013ccaab007698372f9679064fb114a46f86101985a307ae6ebb5fc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045c9052e97131c2d9c19565a019d4ad433c92374f383324b4dc071b98d6ad4b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesGuestAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a12da8657a2999e81735c90d5c8f7ee23eea85dc47bb91d562ae0ac87e52eb6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeFutureReservationSpecificSkuPropertiesInstancePropertiesLocalSsds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cc3550094881dec89a644b9c0962b0954fbaad0e83438ee07f2fa1cbd0b816(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fb7cee12380caa575eeace0b6c7f6a4b9df43583f6dabdfa15ce83486ad9c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c735125a3a166cc49804725cb67a275d16489709dac1383e03d70d6978c5bb5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6005b71af19b3a1a045bf3f03dd52a562035d1c1d47019ecd8123871c8f1b19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263978a17325c1c8be743d79b9fc39a75647c556e97f1fc13cbb822279afe3f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70498a6381d92a3c9c3c5269a122bff0ecc112cdfd8c5e723a4df66c30c478d(
    value: typing.Optional[GoogleComputeFutureReservationSpecificSkuPropertiesInstanceProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e549d7337ff09cbfad8a1272a2e59a2b619d2b0c43f7e7c820f1e5ee344bf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d429fd480f53c937b130acfe08101b5fd25fe95168d9c8d09b9416f2b53c05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cea6a463eea819df5ba8fcaca4ff7238770f4e84eb6019583eb2b8a81b3c152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b75a3edc40a0c056e997143a548662eecb4fdf2afbcf99cadc44bdecc4f2017(
    value: typing.Optional[GoogleComputeFutureReservationSpecificSkuProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cccb04f1eafbe5610a30274207e31a44ee148fa54e7bc58e3252c4881c6d80c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d5435031920eee4549121292851681f54d77523bd296a4f0644eb31950b6c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66b79178194b456d7e8da0cf2a2de4ccbf91ec42be4b0753e9ba3c80ab20cd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951ee0584c1a114d7a345315edcc0d7b8bdd2710777cb25e00234e7de795ff26(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e827112cad89af45520c424f70281cc4a736cc6fa06d704559384ff6bebc14b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe31d37d46c09a52934520939ca5b99f7312c3bd8dfda8f2c193352f9cf3fa2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c353c064d8d6c791b63fe34d5e7298976d3d70b0c3edfd7dadedd5e350189c(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateExistingMatchingUsageInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ea45f259552a6378b3d2796b0b04ef109683b21fdf615718a9473a734270ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780ac12b8db880c45a87e90138b59f49bc160ea1521c6f4bb5787e86ca242130(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd7df8144630bda4dc42f35331bb81348692ce080a4aab98bea10e7cbc024ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51de3c77e757ce4816aa3cebbe673682bae17237483e6e4594639a6b516e3dec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32729b37470813e4c2d21a44a60a0f693b55259307b7ba302fa48484c36421bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb3834253a4ea8992ced9d5f93cc6a4cae9158af98e5e01e24928105f3e7e75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cd3665cb5af27cb857cabb63c66110cf9e319784dee5672dcbde8e75aa1fd0(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c469ce17b08d22485bb25ec6d6175b75d9b9943881b636b797ed24b1844d3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf839e14cca61cfa7275c6e05376c60ca7f0c1fc2075ce4e02d7cddda5c1519a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f99365257208c855584bd562ec1b2ef7a94adf74ad0d6230542f46269d433a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be164cb292b1a8c834c3563af62eaca0470abcded641481dcc132ab3ee5c980(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ed970e28a18fb50024c0a1af893e6b4661af6fede33fd17dcbc10664e20663(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c9e7b597ca5aa03352a6277c646d08986e3073f7dfcd09a3c78bf0beae18a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f07580748ac957a3325845167c885b7e95dfacb6d6f2bbf4e17a4f73b531f2b(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750c8788a23383d7ec95c290e872a9c510eee6d6fa7fcb5c3e475e65979f205c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a66fd334eff8ef1561c34fa8c405ef381a727acf97697d46b670d2cfaa4cdfa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72be4180320c2fb7a292712bfb964fc02937cd38516dc6bef5165ffa23631a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42636b230d65a33f8ac6344a7a0b8c379b9a034509753ad4acee8676cc3e997(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7716de7b4114646df5a0f4817088d8797715cbd53c7931e6f7e754a95b0287(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c7595c06bf81281e7b78cbda3f1c55a732ea63d4ae351bbd32e122a0658439(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21aee030a8a2e73e7820f98f2a6cea7ca007192e7d4eeb08b5a24b221520f915(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsShareSettingsProjectMap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f2bc58b27128aebe946fe88936aac0976328b955574073e612c2ae6cb503c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d6f7bb734aea0c3c98786cc0169f04390ac6470cea17d0208e85dccd21aeaf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad19f910cd061cee37251fcdea0b738b18ab11dfb198a6b5ba528608aa367e05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f70b1372e5c683c1b7022262249cc8a16e98c0c9f7a8ed0ed77bd93de0aa44(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ffa6158629f2cf9412c889da4f66db226814409d88dc3c78469009368a39be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da5f7f686123bea8ae868ba5fea3f38192a1989a383fc40a76bd471877bfb65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34f8b5d5928f8d925337293eccbdaff1adaf1b7f3af17485b9ad1e7a66e5c3d(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesGuestAccelerators],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd1c84e507cbe949ad582c1f825cf86789921429a20c43cf44c65f20e381d4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdcfb78c3c42b650093c7f2132891ff4f39006a268d48f071e5c260e2026547(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94ddb5fc3bc8ad82fa1f174571d994bfe027864ebf5b6af68afcf67bc4c00e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f1680e8258399207e2a4681a31e944cad12e94cb4a195142700c8db924b696(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d780906ca92379702367cecc9b0984cd94539e5d9244b4702a2cee5b71d387(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479bb4e13e4b15c9c023747637f651e595dfef0a50256a55f37d239d71dd077c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86723df458881e80275c7f9a256f68be951db5cf223cf9ed474dafd1c7d50d7c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5effe8f8fcdd7dd24be5d3f274be79ed3ef5deefbb0440ece967456f4589017(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72525a9dbf1deefca746147c57e1d6f167a32f062e65c4c80fb53bf49d2b8b97(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f228aefa2d31000fe52b2fffc6bc7453baf74b1d306e6727a6cc5d9193a7e8b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8639ca52cc8b23b30bda8058e54c495153b52cc9301167352026df45f00a91e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3c941e61d24a5030b8695957c076bf0b77ca4172ba0c97a568073ab3d39454(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstancePropertiesLocalSsds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b10ccdf3bdafec05c6cfcef58c98127b4931b0f45c504bfcdf1e2c426b85b9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37551b0e04001e35f8f262619fc8616c407da8cd519d6950dfec51991dcdb6ae(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuPropertiesInstanceProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03911efad67b6d16f511833562a9dd95f3dbccdae3fc3b7b21538260379b667e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8742082cbd42f9049e12b2c3d3f16cf34e0cc29b62dd23839b2c5fcbf7ecf482(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633ca5ee3179684a2ff8d4240ba1e5db85b47e441b27e1069b6f98288f3f5c6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eacb20a5e66bcb44ef0296eccb7ed01169365882695893d2709706fda48f8f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b120c77d0ea8687bdb93f7482b237db3dfad4215d5f2ad4f4db8ae3f9178345f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0547cd3e8ead09354dee39393f944e8640d7a951a906ab285632d5518410cdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f928f9815c57bc4aa202a0d45fbeac670e322d2d4c30f81d7d5ebea5c6997ccd(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsSpecificSkuProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87307b4fc742fc92c35cec5402c271f67ff98973cd59348dedf7ecc4d166ba8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010118a4dcab36afedb3fba000bc7f6e60207ec952c30794cb678cc0dafc30cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9febc53986aad95f283988e0982be3b210e0835fdd247db1e07d28156a9f10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd80809f29db1316ddf522fbef0b6f7dbf3091b66fb389f11925cacefca70e4b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b916fadc2bd531b36b6d575699edc74d65767e5fee77a3dbd54de91b24eb1681(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1dca202d341a12fa8444dfd06725d88e485e847e2e549ad824c178bdc7d366(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a771795bdb517ab9fe82eb58f1641b8d8fc21d87800b577480c4d794b645d8(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindowDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf3c6d568132eab8ce9cf9cf5b5bf0b195a4ee7afdd8b31954af56f951b9a85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d750fb633256b27a6075b53bd5df97f74d2dacc9602dc5f5cea1fc254db036e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a542cbd924c051206a5e49aee2633c3fe611b80f25b5a9d27a6b4ce625be6d21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d457eac8b316e8ac3a36e24bc70a17011fb20ab1ff51ee6b48651237b7e9bcbe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c4fee0dd62b6c4f6356f60588fc1f811bfdf6700e4430aa180156689671887(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf9874413714f13deb3144399231b2d1500b464d8ddd1b5bf1227a58bc61dfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4942dd5808dc601749920ccdd78f0ca656424f02694e0eb3f42c9073d9d1392e(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodStateFutureReservationSpecsTimeWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510ae0d6880daaeb40d1876b533d23c4510188cfc6b7fa2f586eb71d0a6c0e7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280cf1e07e870c3ac475f9b821b0b0f93a41d66d571582521f769e5eadfc0c5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edeca47e0b28e0c2be3d4bfe2d772004341999227d60b97003c13ad3b08eade0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c4dda0dfd3634adf5bbd9dd3a810ebb8f1ee508c8150315b755379fde9e21f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32bb2c172f43eb96d7c5c7488bda103f0ac98be5387740c48c9e1564414dda5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f104ac053f03a54f5915f0cc6daa9013e870879252629ed42f8437f2f94d749a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1efb2385814bba8f272613e3f5b38546765c8a6fd58db770e8bf97b6b3f1840(
    value: typing.Optional[GoogleComputeFutureReservationStatusLastKnownGoodState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d4ee27f751def1301ecf4331a7aded4fb87cd753274a4d01add6d68995aef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea3a640e9619ce203ac9fa57952c1ec556730bbfbabf483c2f2cb4cb26f06a7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fc4b0d2a4d43bd2f3b3e6b6dbe36c0bc4e4f3cbab6f716233a7b7fba0094df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c84e2c7fd60bc500b8e2c0533255ad4cabf85bbdc70aba16c153d8601e00ea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df1e36c45e0a565eb49fe2f8e5c808973637e2482ff2b9ee7ed2d1df15a35c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72125e57938b10e1595899af05ce9e46f772b4ad0dcdf366d2bc06600124c0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fb745de9f0f27d26feb25775e27f5d0d8dd7c979714e634d017727f044cada(
    value: typing.Optional[GoogleComputeFutureReservationStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cdb17b3d962616e0f1992a1fad02e86f4d7241d5a4c0d050b1f6667db4dee8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939849e5e25b14abaa2d9b2d6695f746c876d193382f6f86c746e2d4e991ad5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64beac041d9a2659344c43d5d8b4006943a86bd62735d220b29acae13d5f6e7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b5402d9245a63cc8c4522426f376f8ec9b152cf60332d974d1bd40fb10fad7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6e07a5c7d51083911f25d821bc49ed05e084dd357f8fccccfc7b4764f78a08(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a625345fc0b7ffa7bae2596839833418b5c9aa1d5793ee320372114ce0004d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac85a492d8502f033dd66312aeb191c7fd6b86e51bdf3e28b9c0286e33bb8d1d(
    value: typing.Optional[GoogleComputeFutureReservationStatusSpecificSkuProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2875f7031083d7865be0e77a35f79b47fcb20d02c3e1123cd5baa786902337f(
    *,
    start_time: builtins.str,
    duration: typing.Optional[typing.Union[GoogleComputeFutureReservationTimeWindowDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    end_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b01026143f0e5f0fc694e693b9fa4f0c384498764a6c31cf268179608a5a08e(
    *,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f7f2a345174d532e47be4e1fbe9e32196ca5138b72f65e2583e8fb313fec46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a335e345d843eacf8ab5a2016b73f0427b0c8651637d86fc1eec9a1b4bd98364(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a76ff8edecce09ed92b8e9412e55274fa2169ec3b2d1f6465d6bc7a54f2d7c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077b7059907a20d862932e98c6d99c2cf408d59c4a2fd6ac7bb930dd70ace549(
    value: typing.Optional[GoogleComputeFutureReservationTimeWindowDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624de61be04c3cd28167e4a47622cd87f100ac27277a0c16ec0d92539feadc03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a46029e56890bfb27532e2d01299714ef9ef2acff2bfc3d60b27237ca9066a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45cead6b2f762afe0f22b180f34495f50995f6995ab0e2a7237b3e93b03a7635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd8067643af1875a7bc07f9f3546853e621c528acf18b67318a798097d60866(
    value: typing.Optional[GoogleComputeFutureReservationTimeWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1388e739f27e4a3a52236a23149d7ceaeaebf4c1b6e5ea915b2db6d3a22578(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d729eeee424b3a71e6f08630aa5ba63d5d3265b84833af7ef5933b9b582711(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d2057a03624b58b22233b0c9695e13bf2afc85e345156fc6454fc689174000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f887ed3ed923e7029b7a48a3d9db5f0f7e1ee0293d4ebf203ab77281935d6f89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5220ee1482f24f3fe87ff85d8d9bb325d13e712bb3f38db7133b5b4356db7e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7dd5800e8d017edd4726e7af692efaeb6b77a12f74dd8ccc7a3e146408ada0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeFutureReservationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
