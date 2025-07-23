r'''
# `google_compute_reservation`

Refer to the Terraform Registry for docs: [`google_compute_reservation`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation).
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


class ComputeReservation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation google_compute_reservation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        specific_reservation: typing.Union["ComputeReservationSpecificReservation", typing.Dict[builtins.str, typing.Any]],
        zone: builtins.str,
        delete_after_duration: typing.Optional[typing.Union["ComputeReservationDeleteAfterDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_at_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_sharing_policy: typing.Optional[typing.Union["ComputeReservationReservationSharingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        share_settings: typing.Optional[typing.Union["ComputeReservationShareSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        specific_reservation_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputeReservationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation google_compute_reservation} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#name ComputeReservation#name}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#specific_reservation ComputeReservation#specific_reservation}
        :param zone: The zone where the reservation is made. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#zone ComputeReservation#zone}
        :param delete_after_duration: delete_after_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete_after_duration ComputeReservation#delete_after_duration}
        :param delete_at_time: Absolute time in future when the reservation will be auto-deleted by Compute Engine. Timestamp is represented in RFC3339 text format. Cannot be used with delete_after_duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete_at_time ComputeReservation#delete_at_time}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#description ComputeReservation#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#id ComputeReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#project ComputeReservation#project}.
        :param reservation_sharing_policy: reservation_sharing_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#reservation_sharing_policy ComputeReservation#reservation_sharing_policy}
        :param share_settings: share_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#share_settings ComputeReservation#share_settings}
        :param specific_reservation_required: When set to true, only VMs that target this reservation by name can consume this reservation. Otherwise, it can be consumed by VMs with affinity for any reservation. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#specific_reservation_required ComputeReservation#specific_reservation_required}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#timeouts ComputeReservation#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117c37c2fd3798ee840d6dad324ab4849cd08b066cb3b3f3a58fd3f8400b0c34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeReservationConfig(
            name=name,
            specific_reservation=specific_reservation,
            zone=zone,
            delete_after_duration=delete_after_duration,
            delete_at_time=delete_at_time,
            description=description,
            id=id,
            project=project,
            reservation_sharing_policy=reservation_sharing_policy,
            share_settings=share_settings,
            specific_reservation_required=specific_reservation_required,
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
        '''Generates CDKTF code for importing a ComputeReservation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeReservation to import.
        :param import_from_id: The id of the existing ComputeReservation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeReservation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2987696f2a236e608708b05acf027a24b04e2981ef4b2359428dbc82502dfa2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeleteAfterDuration")
    def put_delete_after_duration(
        self,
        *,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nanos: Number of nanoseconds for the auto-delete duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#nanos ComputeReservation#nanos}
        :param seconds: Number of seconds for the auto-delete duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#seconds ComputeReservation#seconds}
        '''
        value = ComputeReservationDeleteAfterDuration(nanos=nanos, seconds=seconds)

        return typing.cast(None, jsii.invoke(self, "putDeleteAfterDuration", [value]))

    @jsii.member(jsii_name="putReservationSharingPolicy")
    def put_reservation_sharing_policy(
        self,
        *,
        service_share_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_share_type: Sharing config for all Google Cloud services. Possible values: ["ALLOW_ALL", "DISALLOW_ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#service_share_type ComputeReservation#service_share_type}
        '''
        value = ComputeReservationReservationSharingPolicy(
            service_share_type=service_share_type
        )

        return typing.cast(None, jsii.invoke(self, "putReservationSharingPolicy", [value]))

    @jsii.member(jsii_name="putShareSettings")
    def put_share_settings(
        self,
        *,
        project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeReservationShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        share_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project_map: project_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#project_map ComputeReservation#project_map}
        :param share_type: Type of sharing for this shared-reservation Possible values: ["LOCAL", "SPECIFIC_PROJECTS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#share_type ComputeReservation#share_type}
        '''
        value = ComputeReservationShareSettings(
            project_map=project_map, share_type=share_type
        )

        return typing.cast(None, jsii.invoke(self, "putShareSettings", [value]))

    @jsii.member(jsii_name="putSpecificReservation")
    def put_specific_reservation(
        self,
        *,
        count: jsii.Number,
        instance_properties: typing.Optional[typing.Union["ComputeReservationSpecificReservationInstanceProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        source_instance_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: The number of resources that are allocated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#count ComputeReservation#count}
        :param instance_properties: instance_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#instance_properties ComputeReservation#instance_properties}
        :param source_instance_template: Specifies the instance template to create the reservation. If you use this field, you must exclude the instanceProperties field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#source_instance_template ComputeReservation#source_instance_template}
        '''
        value = ComputeReservationSpecificReservation(
            count=count,
            instance_properties=instance_properties,
            source_instance_template=source_instance_template,
        )

        return typing.cast(None, jsii.invoke(self, "putSpecificReservation", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#create ComputeReservation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete ComputeReservation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#update ComputeReservation#update}.
        '''
        value = ComputeReservationTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeleteAfterDuration")
    def reset_delete_after_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAfterDuration", []))

    @jsii.member(jsii_name="resetDeleteAtTime")
    def reset_delete_at_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAtTime", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReservationSharingPolicy")
    def reset_reservation_sharing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationSharingPolicy", []))

    @jsii.member(jsii_name="resetShareSettings")
    def reset_share_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareSettings", []))

    @jsii.member(jsii_name="resetSpecificReservationRequired")
    def reset_specific_reservation_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecificReservationRequired", []))

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
    @jsii.member(jsii_name="commitment")
    def commitment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitment"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDuration")
    def delete_after_duration(
        self,
    ) -> "ComputeReservationDeleteAfterDurationOutputReference":
        return typing.cast("ComputeReservationDeleteAfterDurationOutputReference", jsii.get(self, "deleteAfterDuration"))

    @builtins.property
    @jsii.member(jsii_name="reservationSharingPolicy")
    def reservation_sharing_policy(
        self,
    ) -> "ComputeReservationReservationSharingPolicyOutputReference":
        return typing.cast("ComputeReservationReservationSharingPolicyOutputReference", jsii.get(self, "reservationSharingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="shareSettings")
    def share_settings(self) -> "ComputeReservationShareSettingsOutputReference":
        return typing.cast("ComputeReservationShareSettingsOutputReference", jsii.get(self, "shareSettings"))

    @builtins.property
    @jsii.member(jsii_name="specificReservation")
    def specific_reservation(
        self,
    ) -> "ComputeReservationSpecificReservationOutputReference":
        return typing.cast("ComputeReservationSpecificReservationOutputReference", jsii.get(self, "specificReservation"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeReservationTimeoutsOutputReference":
        return typing.cast("ComputeReservationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="deleteAfterDurationInput")
    def delete_after_duration_input(
        self,
    ) -> typing.Optional["ComputeReservationDeleteAfterDuration"]:
        return typing.cast(typing.Optional["ComputeReservationDeleteAfterDuration"], jsii.get(self, "deleteAfterDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAtTimeInput")
    def delete_at_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteAtTimeInput"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationSharingPolicyInput")
    def reservation_sharing_policy_input(
        self,
    ) -> typing.Optional["ComputeReservationReservationSharingPolicy"]:
        return typing.cast(typing.Optional["ComputeReservationReservationSharingPolicy"], jsii.get(self, "reservationSharingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="shareSettingsInput")
    def share_settings_input(
        self,
    ) -> typing.Optional["ComputeReservationShareSettings"]:
        return typing.cast(typing.Optional["ComputeReservationShareSettings"], jsii.get(self, "shareSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="specificReservationInput")
    def specific_reservation_input(
        self,
    ) -> typing.Optional["ComputeReservationSpecificReservation"]:
        return typing.cast(typing.Optional["ComputeReservationSpecificReservation"], jsii.get(self, "specificReservationInput"))

    @builtins.property
    @jsii.member(jsii_name="specificReservationRequiredInput")
    def specific_reservation_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "specificReservationRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeReservationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeReservationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteAtTime")
    def delete_at_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteAtTime"))

    @delete_at_time.setter
    def delete_at_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025ffc9d6b18286a6f44fe3b7b2dc0183898d8faa0d6bc2f2853c9a7d9294eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAtTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e1432771a7121f4d1ac030eea817741e8a1812cb324260ae475092fbeeee38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f4041d5c35285bcec2a22a3f7159b1fad2cb893b2765c61c083437128ca2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42dea277bd6db52e70ed2dc91e4f499fd7e324fc521feb3f0ed2258e397ab7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0156de92fc92b32a34b503a50a921849491ecdbf92561186de06a4efd21e11ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__c9ea4340096813202d1a94d59dd87bfea652c258631c9e360733d42e614eee5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specificReservationRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0bff7606afd01408ac63b8dd9458eac3ec604055134ee9a106a1f667801094a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationConfig",
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
        "specific_reservation": "specificReservation",
        "zone": "zone",
        "delete_after_duration": "deleteAfterDuration",
        "delete_at_time": "deleteAtTime",
        "description": "description",
        "id": "id",
        "project": "project",
        "reservation_sharing_policy": "reservationSharingPolicy",
        "share_settings": "shareSettings",
        "specific_reservation_required": "specificReservationRequired",
        "timeouts": "timeouts",
    },
)
class ComputeReservationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        specific_reservation: typing.Union["ComputeReservationSpecificReservation", typing.Dict[builtins.str, typing.Any]],
        zone: builtins.str,
        delete_after_duration: typing.Optional[typing.Union["ComputeReservationDeleteAfterDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        delete_at_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_sharing_policy: typing.Optional[typing.Union["ComputeReservationReservationSharingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        share_settings: typing.Optional[typing.Union["ComputeReservationShareSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        specific_reservation_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputeReservationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#name ComputeReservation#name}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#specific_reservation ComputeReservation#specific_reservation}
        :param zone: The zone where the reservation is made. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#zone ComputeReservation#zone}
        :param delete_after_duration: delete_after_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete_after_duration ComputeReservation#delete_after_duration}
        :param delete_at_time: Absolute time in future when the reservation will be auto-deleted by Compute Engine. Timestamp is represented in RFC3339 text format. Cannot be used with delete_after_duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete_at_time ComputeReservation#delete_at_time}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#description ComputeReservation#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#id ComputeReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#project ComputeReservation#project}.
        :param reservation_sharing_policy: reservation_sharing_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#reservation_sharing_policy ComputeReservation#reservation_sharing_policy}
        :param share_settings: share_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#share_settings ComputeReservation#share_settings}
        :param specific_reservation_required: When set to true, only VMs that target this reservation by name can consume this reservation. Otherwise, it can be consumed by VMs with affinity for any reservation. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#specific_reservation_required ComputeReservation#specific_reservation_required}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#timeouts ComputeReservation#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(specific_reservation, dict):
            specific_reservation = ComputeReservationSpecificReservation(**specific_reservation)
        if isinstance(delete_after_duration, dict):
            delete_after_duration = ComputeReservationDeleteAfterDuration(**delete_after_duration)
        if isinstance(reservation_sharing_policy, dict):
            reservation_sharing_policy = ComputeReservationReservationSharingPolicy(**reservation_sharing_policy)
        if isinstance(share_settings, dict):
            share_settings = ComputeReservationShareSettings(**share_settings)
        if isinstance(timeouts, dict):
            timeouts = ComputeReservationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5d1fc913bec6937d9a2ff070bb75002ee2d726e476692944f5de3747d8f5c6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument specific_reservation", value=specific_reservation, expected_type=type_hints["specific_reservation"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
            check_type(argname="argument delete_after_duration", value=delete_after_duration, expected_type=type_hints["delete_after_duration"])
            check_type(argname="argument delete_at_time", value=delete_at_time, expected_type=type_hints["delete_at_time"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument reservation_sharing_policy", value=reservation_sharing_policy, expected_type=type_hints["reservation_sharing_policy"])
            check_type(argname="argument share_settings", value=share_settings, expected_type=type_hints["share_settings"])
            check_type(argname="argument specific_reservation_required", value=specific_reservation_required, expected_type=type_hints["specific_reservation_required"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "specific_reservation": specific_reservation,
            "zone": zone,
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
        if delete_after_duration is not None:
            self._values["delete_after_duration"] = delete_after_duration
        if delete_at_time is not None:
            self._values["delete_at_time"] = delete_at_time
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if reservation_sharing_policy is not None:
            self._values["reservation_sharing_policy"] = reservation_sharing_policy
        if share_settings is not None:
            self._values["share_settings"] = share_settings
        if specific_reservation_required is not None:
            self._values["specific_reservation_required"] = specific_reservation_required
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
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#name ComputeReservation#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def specific_reservation(self) -> "ComputeReservationSpecificReservation":
        '''specific_reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#specific_reservation ComputeReservation#specific_reservation}
        '''
        result = self._values.get("specific_reservation")
        assert result is not None, "Required property 'specific_reservation' is missing"
        return typing.cast("ComputeReservationSpecificReservation", result)

    @builtins.property
    def zone(self) -> builtins.str:
        '''The zone where the reservation is made.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#zone ComputeReservation#zone}
        '''
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_after_duration(
        self,
    ) -> typing.Optional["ComputeReservationDeleteAfterDuration"]:
        '''delete_after_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete_after_duration ComputeReservation#delete_after_duration}
        '''
        result = self._values.get("delete_after_duration")
        return typing.cast(typing.Optional["ComputeReservationDeleteAfterDuration"], result)

    @builtins.property
    def delete_at_time(self) -> typing.Optional[builtins.str]:
        '''Absolute time in future when the reservation will be auto-deleted by Compute Engine.

        Timestamp is represented in RFC3339 text format.
        Cannot be used with delete_after_duration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete_at_time ComputeReservation#delete_at_time}
        '''
        result = self._values.get("delete_at_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#description ComputeReservation#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#id ComputeReservation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#project ComputeReservation#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_sharing_policy(
        self,
    ) -> typing.Optional["ComputeReservationReservationSharingPolicy"]:
        '''reservation_sharing_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#reservation_sharing_policy ComputeReservation#reservation_sharing_policy}
        '''
        result = self._values.get("reservation_sharing_policy")
        return typing.cast(typing.Optional["ComputeReservationReservationSharingPolicy"], result)

    @builtins.property
    def share_settings(self) -> typing.Optional["ComputeReservationShareSettings"]:
        '''share_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#share_settings ComputeReservation#share_settings}
        '''
        result = self._values.get("share_settings")
        return typing.cast(typing.Optional["ComputeReservationShareSettings"], result)

    @builtins.property
    def specific_reservation_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, only VMs that target this reservation by name can consume this reservation.

        Otherwise, it can be consumed by VMs with
        affinity for any reservation. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#specific_reservation_required ComputeReservation#specific_reservation_required}
        '''
        result = self._values.get("specific_reservation_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeReservationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#timeouts ComputeReservation#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeReservationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationDeleteAfterDuration",
    jsii_struct_bases=[],
    name_mapping={"nanos": "nanos", "seconds": "seconds"},
)
class ComputeReservationDeleteAfterDuration:
    def __init__(
        self,
        *,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nanos: Number of nanoseconds for the auto-delete duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#nanos ComputeReservation#nanos}
        :param seconds: Number of seconds for the auto-delete duration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#seconds ComputeReservation#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea9e7cfeba9afb640273c190a131f4b1b75191d26b2588b928901b0fd21280d)
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Number of nanoseconds for the auto-delete duration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#nanos ComputeReservation#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[builtins.str]:
        '''Number of seconds for the auto-delete duration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#seconds ComputeReservation#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationDeleteAfterDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeReservationDeleteAfterDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationDeleteAfterDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c4c2411202adc7427d5b7e05ece125849d29f63a0e4a897ed84cab92343a95c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__074d6b50820fda8b9306a80a064c8322ef2ce3572c60c9c10a63bbbbd08aaef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c11333c1bf33f1bd8bed8ae2ae631ab8831f035dc7391313e4e50c72630fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeReservationDeleteAfterDuration]:
        return typing.cast(typing.Optional[ComputeReservationDeleteAfterDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeReservationDeleteAfterDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85515ec4911f8e5fd4f6e7289c97113ee4482eddb6f1d3de9b6e67d7fc3d8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationReservationSharingPolicy",
    jsii_struct_bases=[],
    name_mapping={"service_share_type": "serviceShareType"},
)
class ComputeReservationReservationSharingPolicy:
    def __init__(
        self,
        *,
        service_share_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_share_type: Sharing config for all Google Cloud services. Possible values: ["ALLOW_ALL", "DISALLOW_ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#service_share_type ComputeReservation#service_share_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e3109d66f646bb5d5e517d0b058c215e5504cbc5360e2e1ef7622eb85b1889)
            check_type(argname="argument service_share_type", value=service_share_type, expected_type=type_hints["service_share_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_share_type is not None:
            self._values["service_share_type"] = service_share_type

    @builtins.property
    def service_share_type(self) -> typing.Optional[builtins.str]:
        '''Sharing config for all Google Cloud services. Possible values: ["ALLOW_ALL", "DISALLOW_ALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#service_share_type ComputeReservation#service_share_type}
        '''
        result = self._values.get("service_share_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationReservationSharingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeReservationReservationSharingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationReservationSharingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceef9fc2e7d0856b288bb51b76360652ba4928d3c0d6015feb7d22b0f6cf52bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetServiceShareType")
    def reset_service_share_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceShareType", []))

    @builtins.property
    @jsii.member(jsii_name="serviceShareTypeInput")
    def service_share_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceShareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceShareType")
    def service_share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceShareType"))

    @service_share_type.setter
    def service_share_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1732e65d7904d2c5e12e9886e80a0ffc8f2e608f656f81cef71e07416d814679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceShareType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeReservationReservationSharingPolicy]:
        return typing.cast(typing.Optional[ComputeReservationReservationSharingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeReservationReservationSharingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55f20d758a2daac9eb95707f60530ea47e819b4a99e34d6aa25ed4318ee9498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationShareSettings",
    jsii_struct_bases=[],
    name_mapping={"project_map": "projectMap", "share_type": "shareType"},
)
class ComputeReservationShareSettings:
    def __init__(
        self,
        *,
        project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeReservationShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        share_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project_map: project_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#project_map ComputeReservation#project_map}
        :param share_type: Type of sharing for this shared-reservation Possible values: ["LOCAL", "SPECIFIC_PROJECTS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#share_type ComputeReservation#share_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63e90b06ab02c460197e5a93a371b0ac8d393686e1be1ec98495fce3389b518)
            check_type(argname="argument project_map", value=project_map, expected_type=type_hints["project_map"])
            check_type(argname="argument share_type", value=share_type, expected_type=type_hints["share_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project_map is not None:
            self._values["project_map"] = project_map
        if share_type is not None:
            self._values["share_type"] = share_type

    @builtins.property
    def project_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeReservationShareSettingsProjectMap"]]]:
        '''project_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#project_map ComputeReservation#project_map}
        '''
        result = self._values.get("project_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeReservationShareSettingsProjectMap"]]], result)

    @builtins.property
    def share_type(self) -> typing.Optional[builtins.str]:
        '''Type of sharing for this shared-reservation Possible values: ["LOCAL", "SPECIFIC_PROJECTS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#share_type ComputeReservation#share_type}
        '''
        result = self._values.get("share_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationShareSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeReservationShareSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationShareSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae2d9258caffb848ddaf91b96630f728974f25cac9d73bbb3b504fc1f3209079)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProjectMap")
    def put_project_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeReservationShareSettingsProjectMap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd0be3ec2956ce8a843adb7a789d751a3c32092fb6f567a0e8ec1e0ebd152d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProjectMap", [value]))

    @jsii.member(jsii_name="resetProjectMap")
    def reset_project_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectMap", []))

    @jsii.member(jsii_name="resetShareType")
    def reset_share_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareType", []))

    @builtins.property
    @jsii.member(jsii_name="projectMap")
    def project_map(self) -> "ComputeReservationShareSettingsProjectMapList":
        return typing.cast("ComputeReservationShareSettingsProjectMapList", jsii.get(self, "projectMap"))

    @builtins.property
    @jsii.member(jsii_name="projectMapInput")
    def project_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeReservationShareSettingsProjectMap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeReservationShareSettingsProjectMap"]]], jsii.get(self, "projectMapInput"))

    @builtins.property
    @jsii.member(jsii_name="shareTypeInput")
    def share_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="shareType")
    def share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareType"))

    @share_type.setter
    def share_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbff7cea0704bec287744f4c100ccbbf7703cba0ea065d9e75b5237d5d408b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeReservationShareSettings]:
        return typing.cast(typing.Optional[ComputeReservationShareSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeReservationShareSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6aa7dc20979c48fb0349a7d8eb55e5abbe553ef41e9e4c8713276912feb0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationShareSettingsProjectMap",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "project_id": "projectId"},
)
class ComputeReservationShareSettingsProjectMap:
    def __init__(
        self,
        *,
        id: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#id ComputeReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_id: The project id/number, should be same as the key of this project config in the project map. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#project_id ComputeReservation#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a6c0e18897d26aab67509db6141ebd4982e2f4de4d9fda34a6237e3a0d0a69)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#id ComputeReservation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The project id/number, should be same as the key of this project config in the project map.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#project_id ComputeReservation#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationShareSettingsProjectMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeReservationShareSettingsProjectMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationShareSettingsProjectMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__698c9c1fc80234863d57fe3485a74c6eebcd52353099995c138896e0e75fdd70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeReservationShareSettingsProjectMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a359cb0ed30a9b4f0d2f071ce63473d5940e40d448a0666697d8b22d59269a8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeReservationShareSettingsProjectMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47131b9e4b8ce2da36d35f0f6e38a15e116a637e91704bc29b03e33afd571e4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c189be74f9721492fd7ffa1159170c9d255ba03459527a2abe97983324f43e19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__110eed1cd12b841b1b4bb5b00ffb83f2f5d5ba417a80b30650d01a18c4926e0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationShareSettingsProjectMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationShareSettingsProjectMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationShareSettingsProjectMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fdd07a105b8dd804481cf127a943ec7a4c49eb9ef61c4f3c0654517463e734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeReservationShareSettingsProjectMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationShareSettingsProjectMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6451c6a195bbab409b7c901c9f40efa7d8447f6cbe364ea3c974997fdda84f5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1700c60a293e589349b2a993bd532cc1a6ddf7341a842d2da1eb9975d13815e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e266e27d97f02321a411c12523f22b0b0ea6b18adfd045edafc5f27594a8359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationShareSettingsProjectMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationShareSettingsProjectMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationShareSettingsProjectMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e543f781bbbeac4d85a0024648854463dc39589db94885f72fe11838872fbe0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservation",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "instance_properties": "instanceProperties",
        "source_instance_template": "sourceInstanceTemplate",
    },
)
class ComputeReservationSpecificReservation:
    def __init__(
        self,
        *,
        count: jsii.Number,
        instance_properties: typing.Optional[typing.Union["ComputeReservationSpecificReservationInstanceProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        source_instance_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: The number of resources that are allocated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#count ComputeReservation#count}
        :param instance_properties: instance_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#instance_properties ComputeReservation#instance_properties}
        :param source_instance_template: Specifies the instance template to create the reservation. If you use this field, you must exclude the instanceProperties field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#source_instance_template ComputeReservation#source_instance_template}
        '''
        if isinstance(instance_properties, dict):
            instance_properties = ComputeReservationSpecificReservationInstanceProperties(**instance_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a94ddc57ac3a70ead41d97ce0952935c3ff73b217a502a7ff3ff568158c4f4f)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument instance_properties", value=instance_properties, expected_type=type_hints["instance_properties"])
            check_type(argname="argument source_instance_template", value=source_instance_template, expected_type=type_hints["source_instance_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
        }
        if instance_properties is not None:
            self._values["instance_properties"] = instance_properties
        if source_instance_template is not None:
            self._values["source_instance_template"] = source_instance_template

    @builtins.property
    def count(self) -> jsii.Number:
        '''The number of resources that are allocated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#count ComputeReservation#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def instance_properties(
        self,
    ) -> typing.Optional["ComputeReservationSpecificReservationInstanceProperties"]:
        '''instance_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#instance_properties ComputeReservation#instance_properties}
        '''
        result = self._values.get("instance_properties")
        return typing.cast(typing.Optional["ComputeReservationSpecificReservationInstanceProperties"], result)

    @builtins.property
    def source_instance_template(self) -> typing.Optional[builtins.str]:
        '''Specifies the instance template to create the reservation. If you use this field, you must exclude the instanceProperties field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#source_instance_template ComputeReservation#source_instance_template}
        '''
        result = self._values.get("source_instance_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationSpecificReservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationInstanceProperties",
    jsii_struct_bases=[],
    name_mapping={
        "machine_type": "machineType",
        "guest_accelerators": "guestAccelerators",
        "local_ssds": "localSsds",
        "min_cpu_platform": "minCpuPlatform",
    },
)
class ComputeReservationSpecificReservationInstanceProperties:
    def __init__(
        self,
        *,
        machine_type: builtins.str,
        guest_accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        local_ssds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeReservationSpecificReservationInstancePropertiesLocalSsds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_type: The name of the machine type to reserve. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#machine_type ComputeReservation#machine_type}
        :param guest_accelerators: guest_accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#guest_accelerators ComputeReservation#guest_accelerators}
        :param local_ssds: local_ssds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#local_ssds ComputeReservation#local_ssds}
        :param min_cpu_platform: The minimum CPU platform for the reservation. For example, '"Intel Skylake"'. See the CPU platform availability reference](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform#availablezones) for information on available CPU platforms. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#min_cpu_platform ComputeReservation#min_cpu_platform}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81195774c48df98d71dc67e653d5394ac9f5aefba64c315e43e2ccbff35917c)
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument guest_accelerators", value=guest_accelerators, expected_type=type_hints["guest_accelerators"])
            check_type(argname="argument local_ssds", value=local_ssds, expected_type=type_hints["local_ssds"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "machine_type": machine_type,
        }
        if guest_accelerators is not None:
            self._values["guest_accelerators"] = guest_accelerators
        if local_ssds is not None:
            self._values["local_ssds"] = local_ssds
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''The name of the machine type to reserve.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#machine_type ComputeReservation#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def guest_accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators"]]]:
        '''guest_accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#guest_accelerators ComputeReservation#guest_accelerators}
        '''
        result = self._values.get("guest_accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators"]]], result)

    @builtins.property
    def local_ssds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeReservationSpecificReservationInstancePropertiesLocalSsds"]]]:
        '''local_ssds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#local_ssds ComputeReservation#local_ssds}
        '''
        result = self._values.get("local_ssds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeReservationSpecificReservationInstancePropertiesLocalSsds"]]], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''The minimum CPU platform for the reservation.

        For example,
        '"Intel Skylake"'. See
        the CPU platform availability reference](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform#availablezones)
        for information on available CPU platforms.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#min_cpu_platform ComputeReservation#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationSpecificReservationInstanceProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: jsii.Number,
        accelerator_type: builtins.str,
    ) -> None:
        '''
        :param accelerator_count: The number of the guest accelerator cards exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#accelerator_count ComputeReservation#accelerator_count}
        :param accelerator_type: The full or partial URL of the accelerator type to attach to this instance. For example: 'projects/my-project/zones/us-central1-c/acceleratorTypes/nvidia-tesla-p100'. If you are creating an instance template, specify only the accelerator name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#accelerator_type ComputeReservation#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192a479a30fba2733ce31bbe8dcbd6804a20aa88d322cce20cd1ee41b645b139)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator_count": accelerator_count,
            "accelerator_type": accelerator_type,
        }

    @builtins.property
    def accelerator_count(self) -> jsii.Number:
        '''The number of the guest accelerator cards exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#accelerator_count ComputeReservation#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        assert result is not None, "Required property 'accelerator_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def accelerator_type(self) -> builtins.str:
        '''The full or partial URL of the accelerator type to attach to this instance. For example: 'projects/my-project/zones/us-central1-c/acceleratorTypes/nvidia-tesla-p100'.

        If you are creating an instance template, specify only the accelerator name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#accelerator_type ComputeReservation#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        assert result is not None, "Required property 'accelerator_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ffcf5c7ab2e0a9b0728f6a767542851cddf315768254f862f8d860d288db1ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246d0b76e9ce8bba99c457bc72426d02b69305e52bd103e46ae0cf40cfb6ccc9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0446c3754b850991cd5a0e850b10e2b17d30e612165afdad5f30a8d5e05212ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ba09294e2aa6012cfcb0027806a924851cd49a083ce3a0a4363cb68a1bc3505)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcd46de0c1ff58bfdc0f78977e69666fb6b96ab38e7474c5224b22b5ea5571d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9cd82da39b783c21c84512af7f60defc09c87fa2df9bcde73235a7c6c4c163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f587b73956f41d28f9a604e191a2aa0776634fbbe2ed60e2efa8697f48974dcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__69e9d9f25810e40e8af435fa56594ea6312b852c18c085e0b7c8415359d0327c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5719a031cad4c538157faf30d7b5e2f39a51b40bae59584b0100a97be42de38c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f82366d0a5522984f5623e29fffb46f02a1fd0526335b8012d332c39b98e5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationInstancePropertiesLocalSsds",
    jsii_struct_bases=[],
    name_mapping={"disk_size_gb": "diskSizeGb", "interface": "interface"},
)
class ComputeReservationSpecificReservationInstancePropertiesLocalSsds:
    def __init__(
        self,
        *,
        disk_size_gb: jsii.Number,
        interface: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gb: The size of the disk in base-2 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#disk_size_gb ComputeReservation#disk_size_gb}
        :param interface: The disk interface to use for attaching this disk. Default value: "SCSI" Possible values: ["SCSI", "NVME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#interface ComputeReservation#interface}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbab0e3e6b24bb0c4aa4aaedd79698425ab71c825b8a994b3ee5f445a94cd595)
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_size_gb": disk_size_gb,
        }
        if interface is not None:
            self._values["interface"] = interface

    @builtins.property
    def disk_size_gb(self) -> jsii.Number:
        '''The size of the disk in base-2 GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#disk_size_gb ComputeReservation#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        assert result is not None, "Required property 'disk_size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interface(self) -> typing.Optional[builtins.str]:
        '''The disk interface to use for attaching this disk. Default value: "SCSI" Possible values: ["SCSI", "NVME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#interface ComputeReservation#interface}
        '''
        result = self._values.get("interface")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationSpecificReservationInstancePropertiesLocalSsds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeReservationSpecificReservationInstancePropertiesLocalSsdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationInstancePropertiesLocalSsdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__108aa8f7fadf2d4171a18d2707cb17585cf67cb7f7f053e634ecf7f58e6e29c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeReservationSpecificReservationInstancePropertiesLocalSsdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a088abf07faf5477a93c2a893c79079bd9b3317c24a5180bb4dd2f4e033a76f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeReservationSpecificReservationInstancePropertiesLocalSsdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4881ad2262b56dd683b483cb63ff2413ebddb1b87ff40454fad1352aa8a75f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9818ac4c236082927743bd81c1535e2c876b8431c114b07890c0c9658c17c42e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ea5f1a658afc687258ad943bb480ea956d8d20fce211fcc0825f77cf3665eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesLocalSsds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesLocalSsds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesLocalSsds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e105b5a96cea4cbc90c17e8bbcab7bcd311206f6c85c80e7887cff6f5737a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeReservationSpecificReservationInstancePropertiesLocalSsdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationInstancePropertiesLocalSsdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5043dcedd955127f0d3a68c432991bc6611f4c2bbfbb0dbb9d24d79b253f88d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInterface")
    def reset_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterface", []))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceInput")
    def interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08400e7db70c1ab884bdd5f1cff0cf241f79334325a8b790239154ed5753998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2377ac6cf48774e257cdef50c2b8db3dc18fa28b8b7d2af4eae47058c5fcb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationSpecificReservationInstancePropertiesLocalSsds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationSpecificReservationInstancePropertiesLocalSsds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationSpecificReservationInstancePropertiesLocalSsds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760a17e40aa4f940d6e12dfe81f6d4f1dfc9a6d9e814688ac374865e0f9be01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeReservationSpecificReservationInstancePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationInstancePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6377f69b265b9b399f44682c49828bf4512af6e1252e8a11533b6f4337438528)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGuestAccelerators")
    def put_guest_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb3fb18671eaeaa5c8bbbbd669bccf0f4425b2ccf61563335eb4a3344ab2035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestAccelerators", [value]))

    @jsii.member(jsii_name="putLocalSsds")
    def put_local_ssds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationSpecificReservationInstancePropertiesLocalSsds, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ceba1dded3362526ddb7f2d038d31c5b79c0eee5d24c3e1746039e6dd23461d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocalSsds", [value]))

    @jsii.member(jsii_name="resetGuestAccelerators")
    def reset_guest_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestAccelerators", []))

    @jsii.member(jsii_name="resetLocalSsds")
    def reset_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsds", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @builtins.property
    @jsii.member(jsii_name="guestAccelerators")
    def guest_accelerators(
        self,
    ) -> ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsList:
        return typing.cast(ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsList, jsii.get(self, "guestAccelerators"))

    @builtins.property
    @jsii.member(jsii_name="localSsds")
    def local_ssds(
        self,
    ) -> ComputeReservationSpecificReservationInstancePropertiesLocalSsdsList:
        return typing.cast(ComputeReservationSpecificReservationInstancePropertiesLocalSsdsList, jsii.get(self, "localSsds"))

    @builtins.property
    @jsii.member(jsii_name="guestAcceleratorsInput")
    def guest_accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]]], jsii.get(self, "guestAcceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdsInput")
    def local_ssds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesLocalSsds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesLocalSsds]]], jsii.get(self, "localSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed1502bd6e89795b142458dc7cd045cedf5ebdb13569de68892f41eb137b96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b851c4b53a3d9b00b297a79627057e492d67801ef5f104fd3fae534b4598cf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeReservationSpecificReservationInstanceProperties]:
        return typing.cast(typing.Optional[ComputeReservationSpecificReservationInstanceProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeReservationSpecificReservationInstanceProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c533ff0ba345e0c2f482d55807fb70818a0f080d333674cd4ab62d361083c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeReservationSpecificReservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationSpecificReservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5239df2aa3d5c9dd6848ee073c53e02a5f558c589c2598a70d980abc82289cf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceProperties")
    def put_instance_properties(
        self,
        *,
        machine_type: builtins.str,
        guest_accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        local_ssds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationSpecificReservationInstancePropertiesLocalSsds, typing.Dict[builtins.str, typing.Any]]]]] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_type: The name of the machine type to reserve. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#machine_type ComputeReservation#machine_type}
        :param guest_accelerators: guest_accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#guest_accelerators ComputeReservation#guest_accelerators}
        :param local_ssds: local_ssds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#local_ssds ComputeReservation#local_ssds}
        :param min_cpu_platform: The minimum CPU platform for the reservation. For example, '"Intel Skylake"'. See the CPU platform availability reference](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform#availablezones) for information on available CPU platforms. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#min_cpu_platform ComputeReservation#min_cpu_platform}
        '''
        value = ComputeReservationSpecificReservationInstanceProperties(
            machine_type=machine_type,
            guest_accelerators=guest_accelerators,
            local_ssds=local_ssds,
            min_cpu_platform=min_cpu_platform,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceProperties", [value]))

    @jsii.member(jsii_name="resetInstanceProperties")
    def reset_instance_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceProperties", []))

    @jsii.member(jsii_name="resetSourceInstanceTemplate")
    def reset_source_instance_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceInstanceTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="instanceProperties")
    def instance_properties(
        self,
    ) -> ComputeReservationSpecificReservationInstancePropertiesOutputReference:
        return typing.cast(ComputeReservationSpecificReservationInstancePropertiesOutputReference, jsii.get(self, "instanceProperties"))

    @builtins.property
    @jsii.member(jsii_name="inUseCount")
    def in_use_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "inUseCount"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="instancePropertiesInput")
    def instance_properties_input(
        self,
    ) -> typing.Optional[ComputeReservationSpecificReservationInstanceProperties]:
        return typing.cast(typing.Optional[ComputeReservationSpecificReservationInstanceProperties], jsii.get(self, "instancePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceTemplateInput")
    def source_instance_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInstanceTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8b7f926066c8492fa34d07afdb741c193e8a2d3e1f56ee0c27c4e58610c91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceTemplate")
    def source_instance_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstanceTemplate"))

    @source_instance_template.setter
    def source_instance_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272699509a3cbf82c0daee7816f1f37fd1fe34783e553191efeea9883328ea44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceInstanceTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeReservationSpecificReservation]:
        return typing.cast(typing.Optional[ComputeReservationSpecificReservation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeReservationSpecificReservation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba47933dbc244ff3c3a3cff0a3808a71a65c0deeb11f85a08b1b2712c0396149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeReservationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#create ComputeReservation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete ComputeReservation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#update ComputeReservation#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9b21e931f3c54190d550bf2b8dc957065889978743a530ec14b35b7773d5fc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#create ComputeReservation#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#delete ComputeReservation#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_reservation#update ComputeReservation#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeReservationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeReservationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeReservation.ComputeReservationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1a8c23dfa32867c1967cfa454ba2f4b7fdaad31fe58fa0173d27ca845486f65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec780037599f85d2e3fcca18c348914a1a744552b5bc52fcbc80da5bb1144195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cda3fb2482873c51f31b3010c4403547fa57078e80e6586bda669b59c84f1ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0900c609d842b949dbb4f6cc52e062d5ba547f01110215235b0dbc63c2d566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5840b2d5df8a43b1e45b205ae3da797cda63acd8a254740e9349c3d38bf0b017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeReservation",
    "ComputeReservationConfig",
    "ComputeReservationDeleteAfterDuration",
    "ComputeReservationDeleteAfterDurationOutputReference",
    "ComputeReservationReservationSharingPolicy",
    "ComputeReservationReservationSharingPolicyOutputReference",
    "ComputeReservationShareSettings",
    "ComputeReservationShareSettingsOutputReference",
    "ComputeReservationShareSettingsProjectMap",
    "ComputeReservationShareSettingsProjectMapList",
    "ComputeReservationShareSettingsProjectMapOutputReference",
    "ComputeReservationSpecificReservation",
    "ComputeReservationSpecificReservationInstanceProperties",
    "ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators",
    "ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsList",
    "ComputeReservationSpecificReservationInstancePropertiesGuestAcceleratorsOutputReference",
    "ComputeReservationSpecificReservationInstancePropertiesLocalSsds",
    "ComputeReservationSpecificReservationInstancePropertiesLocalSsdsList",
    "ComputeReservationSpecificReservationInstancePropertiesLocalSsdsOutputReference",
    "ComputeReservationSpecificReservationInstancePropertiesOutputReference",
    "ComputeReservationSpecificReservationOutputReference",
    "ComputeReservationTimeouts",
    "ComputeReservationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__117c37c2fd3798ee840d6dad324ab4849cd08b066cb3b3f3a58fd3f8400b0c34(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    specific_reservation: typing.Union[ComputeReservationSpecificReservation, typing.Dict[builtins.str, typing.Any]],
    zone: builtins.str,
    delete_after_duration: typing.Optional[typing.Union[ComputeReservationDeleteAfterDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_at_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_sharing_policy: typing.Optional[typing.Union[ComputeReservationReservationSharingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    share_settings: typing.Optional[typing.Union[ComputeReservationShareSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    specific_reservation_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputeReservationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e2987696f2a236e608708b05acf027a24b04e2981ef4b2359428dbc82502dfa2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025ffc9d6b18286a6f44fe3b7b2dc0183898d8faa0d6bc2f2853c9a7d9294eda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e1432771a7121f4d1ac030eea817741e8a1812cb324260ae475092fbeeee38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f4041d5c35285bcec2a22a3f7159b1fad2cb893b2765c61c083437128ca2e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42dea277bd6db52e70ed2dc91e4f499fd7e324fc521feb3f0ed2258e397ab7c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0156de92fc92b32a34b503a50a921849491ecdbf92561186de06a4efd21e11ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ea4340096813202d1a94d59dd87bfea652c258631c9e360733d42e614eee5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bff7606afd01408ac63b8dd9458eac3ec604055134ee9a106a1f667801094a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5d1fc913bec6937d9a2ff070bb75002ee2d726e476692944f5de3747d8f5c6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    specific_reservation: typing.Union[ComputeReservationSpecificReservation, typing.Dict[builtins.str, typing.Any]],
    zone: builtins.str,
    delete_after_duration: typing.Optional[typing.Union[ComputeReservationDeleteAfterDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_at_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_sharing_policy: typing.Optional[typing.Union[ComputeReservationReservationSharingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    share_settings: typing.Optional[typing.Union[ComputeReservationShareSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    specific_reservation_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputeReservationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea9e7cfeba9afb640273c190a131f4b1b75191d26b2588b928901b0fd21280d(
    *,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4c2411202adc7427d5b7e05ece125849d29f63a0e4a897ed84cab92343a95c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074d6b50820fda8b9306a80a064c8322ef2ce3572c60c9c10a63bbbbd08aaef8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c11333c1bf33f1bd8bed8ae2ae631ab8831f035dc7391313e4e50c72630fc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85515ec4911f8e5fd4f6e7289c97113ee4482eddb6f1d3de9b6e67d7fc3d8f0(
    value: typing.Optional[ComputeReservationDeleteAfterDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e3109d66f646bb5d5e517d0b058c215e5504cbc5360e2e1ef7622eb85b1889(
    *,
    service_share_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceef9fc2e7d0856b288bb51b76360652ba4928d3c0d6015feb7d22b0f6cf52bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1732e65d7904d2c5e12e9886e80a0ffc8f2e608f656f81cef71e07416d814679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55f20d758a2daac9eb95707f60530ea47e819b4a99e34d6aa25ed4318ee9498(
    value: typing.Optional[ComputeReservationReservationSharingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63e90b06ab02c460197e5a93a371b0ac8d393686e1be1ec98495fce3389b518(
    *,
    project_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationShareSettingsProjectMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    share_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2d9258caffb848ddaf91b96630f728974f25cac9d73bbb3b504fc1f3209079(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd0be3ec2956ce8a843adb7a789d751a3c32092fb6f567a0e8ec1e0ebd152d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationShareSettingsProjectMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbff7cea0704bec287744f4c100ccbbf7703cba0ea065d9e75b5237d5d408b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6aa7dc20979c48fb0349a7d8eb55e5abbe553ef41e9e4c8713276912feb0aa(
    value: typing.Optional[ComputeReservationShareSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a6c0e18897d26aab67509db6141ebd4982e2f4de4d9fda34a6237e3a0d0a69(
    *,
    id: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698c9c1fc80234863d57fe3485a74c6eebcd52353099995c138896e0e75fdd70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a359cb0ed30a9b4f0d2f071ce63473d5940e40d448a0666697d8b22d59269a8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47131b9e4b8ce2da36d35f0f6e38a15e116a637e91704bc29b03e33afd571e4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c189be74f9721492fd7ffa1159170c9d255ba03459527a2abe97983324f43e19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110eed1cd12b841b1b4bb5b00ffb83f2f5d5ba417a80b30650d01a18c4926e0f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fdd07a105b8dd804481cf127a943ec7a4c49eb9ef61c4f3c0654517463e734(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationShareSettingsProjectMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6451c6a195bbab409b7c901c9f40efa7d8447f6cbe364ea3c974997fdda84f5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1700c60a293e589349b2a993bd532cc1a6ddf7341a842d2da1eb9975d13815e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e266e27d97f02321a411c12523f22b0b0ea6b18adfd045edafc5f27594a8359(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e543f781bbbeac4d85a0024648854463dc39589db94885f72fe11838872fbe0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationShareSettingsProjectMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a94ddc57ac3a70ead41d97ce0952935c3ff73b217a502a7ff3ff568158c4f4f(
    *,
    count: jsii.Number,
    instance_properties: typing.Optional[typing.Union[ComputeReservationSpecificReservationInstanceProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    source_instance_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81195774c48df98d71dc67e653d5394ac9f5aefba64c315e43e2ccbff35917c(
    *,
    machine_type: builtins.str,
    guest_accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    local_ssds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationSpecificReservationInstancePropertiesLocalSsds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192a479a30fba2733ce31bbe8dcbd6804a20aa88d322cce20cd1ee41b645b139(
    *,
    accelerator_count: jsii.Number,
    accelerator_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffcf5c7ab2e0a9b0728f6a767542851cddf315768254f862f8d860d288db1ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246d0b76e9ce8bba99c457bc72426d02b69305e52bd103e46ae0cf40cfb6ccc9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0446c3754b850991cd5a0e850b10e2b17d30e612165afdad5f30a8d5e05212ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba09294e2aa6012cfcb0027806a924851cd49a083ce3a0a4363cb68a1bc3505(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd46de0c1ff58bfdc0f78977e69666fb6b96ab38e7474c5224b22b5ea5571d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9cd82da39b783c21c84512af7f60defc09c87fa2df9bcde73235a7c6c4c163(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f587b73956f41d28f9a604e191a2aa0776634fbbe2ed60e2efa8697f48974dcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e9d9f25810e40e8af435fa56594ea6312b852c18c085e0b7c8415359d0327c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5719a031cad4c538157faf30d7b5e2f39a51b40bae59584b0100a97be42de38c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f82366d0a5522984f5623e29fffb46f02a1fd0526335b8012d332c39b98e5b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbab0e3e6b24bb0c4aa4aaedd79698425ab71c825b8a994b3ee5f445a94cd595(
    *,
    disk_size_gb: jsii.Number,
    interface: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108aa8f7fadf2d4171a18d2707cb17585cf67cb7f7f053e634ecf7f58e6e29c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a088abf07faf5477a93c2a893c79079bd9b3317c24a5180bb4dd2f4e033a76f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4881ad2262b56dd683b483cb63ff2413ebddb1b87ff40454fad1352aa8a75f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9818ac4c236082927743bd81c1535e2c876b8431c114b07890c0c9658c17c42e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ea5f1a658afc687258ad943bb480ea956d8d20fce211fcc0825f77cf3665eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e105b5a96cea4cbc90c17e8bbcab7bcd311206f6c85c80e7887cff6f5737a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeReservationSpecificReservationInstancePropertiesLocalSsds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5043dcedd955127f0d3a68c432991bc6611f4c2bbfbb0dbb9d24d79b253f88d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08400e7db70c1ab884bdd5f1cff0cf241f79334325a8b790239154ed5753998(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2377ac6cf48774e257cdef50c2b8db3dc18fa28b8b7d2af4eae47058c5fcb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760a17e40aa4f940d6e12dfe81f6d4f1dfc9a6d9e814688ac374865e0f9be01a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationSpecificReservationInstancePropertiesLocalSsds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6377f69b265b9b399f44682c49828bf4512af6e1252e8a11533b6f4337438528(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb3fb18671eaeaa5c8bbbbd669bccf0f4425b2ccf61563335eb4a3344ab2035(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationSpecificReservationInstancePropertiesGuestAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ceba1dded3362526ddb7f2d038d31c5b79c0eee5d24c3e1746039e6dd23461d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeReservationSpecificReservationInstancePropertiesLocalSsds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed1502bd6e89795b142458dc7cd045cedf5ebdb13569de68892f41eb137b96f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b851c4b53a3d9b00b297a79627057e492d67801ef5f104fd3fae534b4598cf92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c533ff0ba345e0c2f482d55807fb70818a0f080d333674cd4ab62d361083c1(
    value: typing.Optional[ComputeReservationSpecificReservationInstanceProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5239df2aa3d5c9dd6848ee073c53e02a5f558c589c2598a70d980abc82289cf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8b7f926066c8492fa34d07afdb741c193e8a2d3e1f56ee0c27c4e58610c91e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272699509a3cbf82c0daee7816f1f37fd1fe34783e553191efeea9883328ea44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba47933dbc244ff3c3a3cff0a3808a71a65c0deeb11f85a08b1b2712c0396149(
    value: typing.Optional[ComputeReservationSpecificReservation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9b21e931f3c54190d550bf2b8dc957065889978743a530ec14b35b7773d5fc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a8c23dfa32867c1967cfa454ba2f4b7fdaad31fe58fa0173d27ca845486f65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec780037599f85d2e3fcca18c348914a1a744552b5bc52fcbc80da5bb1144195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cda3fb2482873c51f31b3010c4403547fa57078e80e6586bda669b59c84f1ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0900c609d842b949dbb4f6cc52e062d5ba547f01110215235b0dbc63c2d566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5840b2d5df8a43b1e45b205ae3da797cda63acd8a254740e9349c3d38bf0b017(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeReservationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
