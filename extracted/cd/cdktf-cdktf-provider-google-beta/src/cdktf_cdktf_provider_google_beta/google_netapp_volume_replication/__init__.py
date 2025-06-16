r'''
# `google_netapp_volume_replication`

Refer to the Terraform Registry for docs: [`google_netapp_volume_replication`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication).
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


class GoogleNetappVolumeReplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication google_netapp_volume_replication}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        replication_schedule: builtins.str,
        volume_name: builtins.str,
        delete_destination_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        destination_volume_parameters: typing.Optional[typing.Union["GoogleNetappVolumeReplicationDestinationVolumeParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        force_stopping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetappVolumeReplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication google_netapp_volume_replication} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Name of region for this resource. The resource needs to be created in the region of the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#location GoogleNetappVolumeReplication#location}
        :param name: The name of the replication. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#name GoogleNetappVolumeReplication#name}
        :param replication_schedule: Specifies the replication interval. Possible values: ["EVERY_10_MINUTES", "HOURLY", "DAILY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#replication_schedule GoogleNetappVolumeReplication#replication_schedule}
        :param volume_name: The name of the existing source volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#volume_name GoogleNetappVolumeReplication#volume_name}
        :param delete_destination_volume: A destination volume is created as part of replication creation. The destination volume will not became under Terraform management unless you import it manually. If you delete the replication, this volume will remain. Setting this parameter to true will delete the *current* destination volume when destroying the replication. If you reversed the replication direction, this will be your former source volume! For production use, it is recommended to keep this parameter false to avoid accidental volume deletion. Handle with care. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#delete_destination_volume GoogleNetappVolumeReplication#delete_destination_volume}
        :param description: An description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#description GoogleNetappVolumeReplication#description}
        :param destination_volume_parameters: destination_volume_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#destination_volume_parameters GoogleNetappVolumeReplication#destination_volume_parameters}
        :param force_stopping: Only replications with mirror_state=MIRRORED can be stopped. A replication in mirror_state=TRANSFERRING currently receives an update and stopping the update might be undesirable. Set this parameter to true to stop anyway. All data transferred to the destination will be discarded and content of destination volume will remain at the state of the last successful update. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#force_stopping GoogleNetappVolumeReplication#force_stopping}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#id GoogleNetappVolumeReplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#labels GoogleNetappVolumeReplication#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#project GoogleNetappVolumeReplication#project}.
        :param replication_enabled: Set to false to stop/break the mirror. Stopping the mirror makes the destination volume read-write and act independently from the source volume. Set to true to enable/resume the mirror. WARNING: Resuming a mirror overwrites any changes done to the destination volume with the content of the source volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#replication_enabled GoogleNetappVolumeReplication#replication_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#timeouts GoogleNetappVolumeReplication#timeouts}
        :param wait_for_mirror: Replication resource state is independent of mirror_state. With enough data, it can take many hours for mirror_state to reach MIRRORED. If you want Terraform to wait for the mirror to finish on create/stop/resume operations, set this parameter to true. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#wait_for_mirror GoogleNetappVolumeReplication#wait_for_mirror}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6126fa22046d0ed8522e234de860bf819686da8cdc43d31cea885ee0595881)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetappVolumeReplicationConfig(
            location=location,
            name=name,
            replication_schedule=replication_schedule,
            volume_name=volume_name,
            delete_destination_volume=delete_destination_volume,
            description=description,
            destination_volume_parameters=destination_volume_parameters,
            force_stopping=force_stopping,
            id=id,
            labels=labels,
            project=project,
            replication_enabled=replication_enabled,
            timeouts=timeouts,
            wait_for_mirror=wait_for_mirror,
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
        '''Generates CDKTF code for importing a GoogleNetappVolumeReplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetappVolumeReplication to import.
        :param import_from_id: The id of the existing GoogleNetappVolumeReplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetappVolumeReplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27fdf5b650155ff4b574c4586217422a480d744c0d3f6f8c1072deee89e0336)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationVolumeParameters")
    def put_destination_volume_parameters(
        self,
        *,
        storage_pool: builtins.str,
        description: typing.Optional[builtins.str] = None,
        share_name: typing.Optional[builtins.str] = None,
        tiering_policy: typing.Optional[typing.Union["GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_pool: Name of an existing storage pool for the destination volume with format: 'projects/{{project}}/locations/{{location}}/storagePools/{{poolId}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#storage_pool GoogleNetappVolumeReplication#storage_pool}
        :param description: Description for the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#description GoogleNetappVolumeReplication#description}
        :param share_name: Share name for destination volume. If not specified, name of source volume's share name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#share_name GoogleNetappVolumeReplication#share_name}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#tiering_policy GoogleNetappVolumeReplication#tiering_policy}
        :param volume_id: Name for the destination volume to be created. If not specified, the name of the source volume will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#volume_id GoogleNetappVolumeReplication#volume_id}
        '''
        value = GoogleNetappVolumeReplicationDestinationVolumeParameters(
            storage_pool=storage_pool,
            description=description,
            share_name=share_name,
            tiering_policy=tiering_policy,
            volume_id=volume_id,
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationVolumeParameters", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#create GoogleNetappVolumeReplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#delete GoogleNetappVolumeReplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#update GoogleNetappVolumeReplication#update}.
        '''
        value = GoogleNetappVolumeReplicationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeleteDestinationVolume")
    def reset_delete_destination_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteDestinationVolume", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDestinationVolumeParameters")
    def reset_destination_volume_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationVolumeParameters", []))

    @jsii.member(jsii_name="resetForceStopping")
    def reset_force_stopping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceStopping", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReplicationEnabled")
    def reset_replication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationEnabled", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWaitForMirror")
    def reset_wait_for_mirror(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForMirror", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="destinationVolume")
    def destination_volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationVolume"))

    @builtins.property
    @jsii.member(jsii_name="destinationVolumeParameters")
    def destination_volume_parameters(
        self,
    ) -> "GoogleNetappVolumeReplicationDestinationVolumeParametersOutputReference":
        return typing.cast("GoogleNetappVolumeReplicationDestinationVolumeParametersOutputReference", jsii.get(self, "destinationVolumeParameters"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="healthy")
    def healthy(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "healthy"))

    @builtins.property
    @jsii.member(jsii_name="hybridPeeringDetails")
    def hybrid_peering_details(
        self,
    ) -> "GoogleNetappVolumeReplicationHybridPeeringDetailsList":
        return typing.cast("GoogleNetappVolumeReplicationHybridPeeringDetailsList", jsii.get(self, "hybridPeeringDetails"))

    @builtins.property
    @jsii.member(jsii_name="hybridReplicationType")
    def hybrid_replication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hybridReplicationType"))

    @builtins.property
    @jsii.member(jsii_name="mirrorState")
    def mirror_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mirrorState"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="sourceVolume")
    def source_volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceVolume"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateDetails")
    def state_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateDetails"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetappVolumeReplicationTimeoutsOutputReference":
        return typing.cast("GoogleNetappVolumeReplicationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="transferStats")
    def transfer_stats(self) -> "GoogleNetappVolumeReplicationTransferStatsList":
        return typing.cast("GoogleNetappVolumeReplicationTransferStatsList", jsii.get(self, "transferStats"))

    @builtins.property
    @jsii.member(jsii_name="deleteDestinationVolumeInput")
    def delete_destination_volume_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteDestinationVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationVolumeParametersInput")
    def destination_volume_parameters_input(
        self,
    ) -> typing.Optional["GoogleNetappVolumeReplicationDestinationVolumeParameters"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeReplicationDestinationVolumeParameters"], jsii.get(self, "destinationVolumeParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="forceStoppingInput")
    def force_stopping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceStoppingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationEnabledInput")
    def replication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replicationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationScheduleInput")
    def replication_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetappVolumeReplicationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetappVolumeReplicationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeNameInput")
    def volume_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForMirrorInput")
    def wait_for_mirror_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForMirrorInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteDestinationVolume")
    def delete_destination_volume(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteDestinationVolume"))

    @delete_destination_volume.setter
    def delete_destination_volume(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd6e1b8fa494052e52d3af847d38ed86896e7945a01a40f717cc22d72b55a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteDestinationVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf2f0086da6070717a78a2daa3217ddd6cceaef384f7d3af9cf485315d8ebf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceStopping")
    def force_stopping(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceStopping"))

    @force_stopping.setter
    def force_stopping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d11537c23d3287d054b6dc0e1ecab187e469bedf736a97e8880c7e35bc72cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceStopping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1bf3dd644a3e468677fb9b9e7a1981b269ae89a7e1510e5ce120fe32dab0b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d41f2756677485e63408f0ea6b43332222487a7e1ee11ed369a4fa9a1e9b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04670739c4763417e1a24657de152f06c779ccc50c5592c35c405f90bb970bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8803c507faab6f347ff118547a0e08f04f85e67b14552bf5b568dc60cb7e6425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d703f066ebdb1aca6a4b326996185a43e64389a4fdb491f71f6da6f1b689d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationEnabled")
    def replication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replicationEnabled"))

    @replication_enabled.setter
    def replication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fadc032fe3650f461d92ea197996ce12645d7ed4f39ad07ff4bd2577955bb57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationSchedule")
    def replication_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationSchedule"))

    @replication_schedule.setter
    def replication_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9047a62b9af59d951cada1cc9771d829190a83797f39e149e3fe6168ec2536dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b217bc2f7009cf7ac08bc01ba8eea60eea474b961782cda91c8906509febf80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForMirror")
    def wait_for_mirror(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForMirror"))

    @wait_for_mirror.setter
    def wait_for_mirror(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cbf0af59e5796f1fa2c79c57f84db776001762fbac29f2a95a615c5d7b803b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForMirror", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationConfig",
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
        "name": "name",
        "replication_schedule": "replicationSchedule",
        "volume_name": "volumeName",
        "delete_destination_volume": "deleteDestinationVolume",
        "description": "description",
        "destination_volume_parameters": "destinationVolumeParameters",
        "force_stopping": "forceStopping",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "replication_enabled": "replicationEnabled",
        "timeouts": "timeouts",
        "wait_for_mirror": "waitForMirror",
    },
)
class GoogleNetappVolumeReplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        replication_schedule: builtins.str,
        volume_name: builtins.str,
        delete_destination_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        destination_volume_parameters: typing.Optional[typing.Union["GoogleNetappVolumeReplicationDestinationVolumeParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        force_stopping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetappVolumeReplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Name of region for this resource. The resource needs to be created in the region of the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#location GoogleNetappVolumeReplication#location}
        :param name: The name of the replication. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#name GoogleNetappVolumeReplication#name}
        :param replication_schedule: Specifies the replication interval. Possible values: ["EVERY_10_MINUTES", "HOURLY", "DAILY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#replication_schedule GoogleNetappVolumeReplication#replication_schedule}
        :param volume_name: The name of the existing source volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#volume_name GoogleNetappVolumeReplication#volume_name}
        :param delete_destination_volume: A destination volume is created as part of replication creation. The destination volume will not became under Terraform management unless you import it manually. If you delete the replication, this volume will remain. Setting this parameter to true will delete the *current* destination volume when destroying the replication. If you reversed the replication direction, this will be your former source volume! For production use, it is recommended to keep this parameter false to avoid accidental volume deletion. Handle with care. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#delete_destination_volume GoogleNetappVolumeReplication#delete_destination_volume}
        :param description: An description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#description GoogleNetappVolumeReplication#description}
        :param destination_volume_parameters: destination_volume_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#destination_volume_parameters GoogleNetappVolumeReplication#destination_volume_parameters}
        :param force_stopping: Only replications with mirror_state=MIRRORED can be stopped. A replication in mirror_state=TRANSFERRING currently receives an update and stopping the update might be undesirable. Set this parameter to true to stop anyway. All data transferred to the destination will be discarded and content of destination volume will remain at the state of the last successful update. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#force_stopping GoogleNetappVolumeReplication#force_stopping}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#id GoogleNetappVolumeReplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#labels GoogleNetappVolumeReplication#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#project GoogleNetappVolumeReplication#project}.
        :param replication_enabled: Set to false to stop/break the mirror. Stopping the mirror makes the destination volume read-write and act independently from the source volume. Set to true to enable/resume the mirror. WARNING: Resuming a mirror overwrites any changes done to the destination volume with the content of the source volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#replication_enabled GoogleNetappVolumeReplication#replication_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#timeouts GoogleNetappVolumeReplication#timeouts}
        :param wait_for_mirror: Replication resource state is independent of mirror_state. With enough data, it can take many hours for mirror_state to reach MIRRORED. If you want Terraform to wait for the mirror to finish on create/stop/resume operations, set this parameter to true. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#wait_for_mirror GoogleNetappVolumeReplication#wait_for_mirror}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination_volume_parameters, dict):
            destination_volume_parameters = GoogleNetappVolumeReplicationDestinationVolumeParameters(**destination_volume_parameters)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetappVolumeReplicationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3732427564d730d8667176b6e9794557575ca84e70a682ef139e59e406b056f2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replication_schedule", value=replication_schedule, expected_type=type_hints["replication_schedule"])
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
            check_type(argname="argument delete_destination_volume", value=delete_destination_volume, expected_type=type_hints["delete_destination_volume"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_volume_parameters", value=destination_volume_parameters, expected_type=type_hints["destination_volume_parameters"])
            check_type(argname="argument force_stopping", value=force_stopping, expected_type=type_hints["force_stopping"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument replication_enabled", value=replication_enabled, expected_type=type_hints["replication_enabled"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument wait_for_mirror", value=wait_for_mirror, expected_type=type_hints["wait_for_mirror"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "replication_schedule": replication_schedule,
            "volume_name": volume_name,
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
        if delete_destination_volume is not None:
            self._values["delete_destination_volume"] = delete_destination_volume
        if description is not None:
            self._values["description"] = description
        if destination_volume_parameters is not None:
            self._values["destination_volume_parameters"] = destination_volume_parameters
        if force_stopping is not None:
            self._values["force_stopping"] = force_stopping
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if replication_enabled is not None:
            self._values["replication_enabled"] = replication_enabled
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if wait_for_mirror is not None:
            self._values["wait_for_mirror"] = wait_for_mirror

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
        '''Name of region for this resource. The resource needs to be created in the region of the destination volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#location GoogleNetappVolumeReplication#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the replication. Needs to be unique per location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#name GoogleNetappVolumeReplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_schedule(self) -> builtins.str:
        '''Specifies the replication interval. Possible values: ["EVERY_10_MINUTES", "HOURLY", "DAILY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#replication_schedule GoogleNetappVolumeReplication#replication_schedule}
        '''
        result = self._values.get("replication_schedule")
        assert result is not None, "Required property 'replication_schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_name(self) -> builtins.str:
        '''The name of the existing source volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#volume_name GoogleNetappVolumeReplication#volume_name}
        '''
        result = self._values.get("volume_name")
        assert result is not None, "Required property 'volume_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_destination_volume(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A destination volume is created as part of replication creation.

        The destination volume will not became
        under Terraform management unless you import it manually. If you delete the replication, this volume
        will remain.
        Setting this parameter to true will delete the *current* destination volume when destroying the
        replication. If you reversed the replication direction, this will be your former source volume!
        For production use, it is recommended to keep this parameter false to avoid accidental volume
        deletion. Handle with care. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#delete_destination_volume GoogleNetappVolumeReplication#delete_destination_volume}
        '''
        result = self._values.get("delete_destination_volume")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#description GoogleNetappVolumeReplication#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_volume_parameters(
        self,
    ) -> typing.Optional["GoogleNetappVolumeReplicationDestinationVolumeParameters"]:
        '''destination_volume_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#destination_volume_parameters GoogleNetappVolumeReplication#destination_volume_parameters}
        '''
        result = self._values.get("destination_volume_parameters")
        return typing.cast(typing.Optional["GoogleNetappVolumeReplicationDestinationVolumeParameters"], result)

    @builtins.property
    def force_stopping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only replications with mirror_state=MIRRORED can be stopped.

        A replication in mirror_state=TRANSFERRING
        currently receives an update and stopping the update might be undesirable. Set this parameter to true
        to stop anyway. All data transferred to the destination will be discarded and content of destination
        volume will remain at the state of the last successful update. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#force_stopping GoogleNetappVolumeReplication#force_stopping}
        '''
        result = self._values.get("force_stopping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#id GoogleNetappVolumeReplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#labels GoogleNetappVolumeReplication#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#project GoogleNetappVolumeReplication#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to false to stop/break the mirror.

        Stopping the mirror makes the destination volume read-write
        and act independently from the source volume.
        Set to true to enable/resume the mirror. WARNING: Resuming a mirror overwrites any changes
        done to the destination volume with the content of the source volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#replication_enabled GoogleNetappVolumeReplication#replication_enabled}
        '''
        result = self._values.get("replication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleNetappVolumeReplicationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#timeouts GoogleNetappVolumeReplication#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetappVolumeReplicationTimeouts"], result)

    @builtins.property
    def wait_for_mirror(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Replication resource state is independent of mirror_state.

        With enough data, it can take many hours
        for mirror_state to reach MIRRORED. If you want Terraform to wait for the mirror to finish on
        create/stop/resume operations, set this parameter to true. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#wait_for_mirror GoogleNetappVolumeReplication#wait_for_mirror}
        '''
        result = self._values.get("wait_for_mirror")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeReplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationDestinationVolumeParameters",
    jsii_struct_bases=[],
    name_mapping={
        "storage_pool": "storagePool",
        "description": "description",
        "share_name": "shareName",
        "tiering_policy": "tieringPolicy",
        "volume_id": "volumeId",
    },
)
class GoogleNetappVolumeReplicationDestinationVolumeParameters:
    def __init__(
        self,
        *,
        storage_pool: builtins.str,
        description: typing.Optional[builtins.str] = None,
        share_name: typing.Optional[builtins.str] = None,
        tiering_policy: typing.Optional[typing.Union["GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_pool: Name of an existing storage pool for the destination volume with format: 'projects/{{project}}/locations/{{location}}/storagePools/{{poolId}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#storage_pool GoogleNetappVolumeReplication#storage_pool}
        :param description: Description for the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#description GoogleNetappVolumeReplication#description}
        :param share_name: Share name for destination volume. If not specified, name of source volume's share name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#share_name GoogleNetappVolumeReplication#share_name}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#tiering_policy GoogleNetappVolumeReplication#tiering_policy}
        :param volume_id: Name for the destination volume to be created. If not specified, the name of the source volume will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#volume_id GoogleNetappVolumeReplication#volume_id}
        '''
        if isinstance(tiering_policy, dict):
            tiering_policy = GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy(**tiering_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd9d3d19b613945b0864a51246dd0e03683ad95a84f2942db838dcc5f92bb37)
            check_type(argname="argument storage_pool", value=storage_pool, expected_type=type_hints["storage_pool"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument share_name", value=share_name, expected_type=type_hints["share_name"])
            check_type(argname="argument tiering_policy", value=tiering_policy, expected_type=type_hints["tiering_policy"])
            check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "storage_pool": storage_pool,
        }
        if description is not None:
            self._values["description"] = description
        if share_name is not None:
            self._values["share_name"] = share_name
        if tiering_policy is not None:
            self._values["tiering_policy"] = tiering_policy
        if volume_id is not None:
            self._values["volume_id"] = volume_id

    @builtins.property
    def storage_pool(self) -> builtins.str:
        '''Name of an existing storage pool for the destination volume with format: 'projects/{{project}}/locations/{{location}}/storagePools/{{poolId}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#storage_pool GoogleNetappVolumeReplication#storage_pool}
        '''
        result = self._values.get("storage_pool")
        assert result is not None, "Required property 'storage_pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description for the destination volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#description GoogleNetappVolumeReplication#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_name(self) -> typing.Optional[builtins.str]:
        '''Share name for destination volume. If not specified, name of source volume's share name will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#share_name GoogleNetappVolumeReplication#share_name}
        '''
        result = self._values.get("share_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tiering_policy(
        self,
    ) -> typing.Optional["GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy"]:
        '''tiering_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#tiering_policy GoogleNetappVolumeReplication#tiering_policy}
        '''
        result = self._values.get("tiering_policy")
        return typing.cast(typing.Optional["GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy"], result)

    @builtins.property
    def volume_id(self) -> typing.Optional[builtins.str]:
        '''Name for the destination volume to be created.

        If not specified, the name of the source volume will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#volume_id GoogleNetappVolumeReplication#volume_id}
        '''
        result = self._values.get("volume_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeReplicationDestinationVolumeParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeReplicationDestinationVolumeParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationDestinationVolumeParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c837df4602549992badbc53cce99825b1f6ed5a6221254aa95c53e05a2fd642d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTieringPolicy")
    def put_tiering_policy(
        self,
        *,
        cooling_threshold_days: typing.Optional[jsii.Number] = None,
        tier_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_threshold_days: Optional. Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183. Default is 31. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#cooling_threshold_days GoogleNetappVolumeReplication#cooling_threshold_days}
        :param tier_action: Optional. Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#tier_action GoogleNetappVolumeReplication#tier_action}
        '''
        value = GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy(
            cooling_threshold_days=cooling_threshold_days, tier_action=tier_action
        )

        return typing.cast(None, jsii.invoke(self, "putTieringPolicy", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetShareName")
    def reset_share_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareName", []))

    @jsii.member(jsii_name="resetTieringPolicy")
    def reset_tiering_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTieringPolicy", []))

    @jsii.member(jsii_name="resetVolumeId")
    def reset_volume_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeId", []))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicy")
    def tiering_policy(
        self,
    ) -> "GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference":
        return typing.cast("GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference", jsii.get(self, "tieringPolicy"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="shareNameInput")
    def share_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePoolInput")
    def storage_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storagePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicyInput")
    def tiering_policy_input(
        self,
    ) -> typing.Optional["GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy"], jsii.get(self, "tieringPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeIdInput")
    def volume_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22459ea1ba0f043f9f8d023da1bbf578ae749e847b4b3c883abdbde65bf71b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareName")
    def share_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareName"))

    @share_name.setter
    def share_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109b1e886df5a95d41699c03a55871ace36cfa93dcb064d1c4e06d62d6eed543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePool")
    def storage_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePool"))

    @storage_pool.setter
    def storage_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236a5062e1b85d00a307838f2d5e065eca197e13cba5a3bd847d6c3c9bde0afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeId"))

    @volume_id.setter
    def volume_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c1edee9511fbc0acd66464cd11a36a5a39d34e1745abceb2ae7a1b1497c524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeReplicationDestinationVolumeParameters]:
        return typing.cast(typing.Optional[GoogleNetappVolumeReplicationDestinationVolumeParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeReplicationDestinationVolumeParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb21ef313c7ac7c3620bd20acd2ca9699c22cdf63f4498cbc2d14c5a9c339113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cooling_threshold_days": "coolingThresholdDays",
        "tier_action": "tierAction",
    },
)
class GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy:
    def __init__(
        self,
        *,
        cooling_threshold_days: typing.Optional[jsii.Number] = None,
        tier_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_threshold_days: Optional. Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183. Default is 31. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#cooling_threshold_days GoogleNetappVolumeReplication#cooling_threshold_days}
        :param tier_action: Optional. Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#tier_action GoogleNetappVolumeReplication#tier_action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6cc3b16696837b9080da3ea4072f5142ed08e13382b8d2a834d2519c04756c)
            check_type(argname="argument cooling_threshold_days", value=cooling_threshold_days, expected_type=type_hints["cooling_threshold_days"])
            check_type(argname="argument tier_action", value=tier_action, expected_type=type_hints["tier_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cooling_threshold_days is not None:
            self._values["cooling_threshold_days"] = cooling_threshold_days
        if tier_action is not None:
            self._values["tier_action"] = tier_action

    @builtins.property
    def cooling_threshold_days(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183.
        Default is 31.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#cooling_threshold_days GoogleNetappVolumeReplication#cooling_threshold_days}
        '''
        result = self._values.get("cooling_threshold_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_action(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#tier_action GoogleNetappVolumeReplication#tier_action}
        '''
        result = self._values.get("tier_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da658307a6be09baa690db0c4943dcc2ca40c3a77af918f0df16af2ecb26eab6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCoolingThresholdDays")
    def reset_cooling_threshold_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolingThresholdDays", []))

    @jsii.member(jsii_name="resetTierAction")
    def reset_tier_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierAction", []))

    @builtins.property
    @jsii.member(jsii_name="coolingThresholdDaysInput")
    def cooling_threshold_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coolingThresholdDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="tierActionInput")
    def tier_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierActionInput"))

    @builtins.property
    @jsii.member(jsii_name="coolingThresholdDays")
    def cooling_threshold_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coolingThresholdDays"))

    @cooling_threshold_days.setter
    def cooling_threshold_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d17dd55854263283dc0d4eb2942b307c694eda71da77241c0735d4e7184baa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolingThresholdDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierAction")
    def tier_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tierAction"))

    @tier_action.setter
    def tier_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0130403d7f16c64b4dd80ac9fd39d88aebbe0bef72dedc1762fec4e4b7603e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy]:
        return typing.cast(typing.Optional[GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d067a80e3d7b2be38bc3af979e6e718b76590b1e7d776519f46498a40d8af13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationHybridPeeringDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleNetappVolumeReplicationHybridPeeringDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeReplicationHybridPeeringDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeReplicationHybridPeeringDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationHybridPeeringDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29f8c1ac0c809eaf9b0bed754245ce064f7022aac905d98e5a1b67a6927190ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetappVolumeReplicationHybridPeeringDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b04245af250e65dbf462ff4062745dd2a222fab07d8048ec512d084a6e2b5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetappVolumeReplicationHybridPeeringDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76393678275be93e6e338cf2739748b7c292b554723ae95a066a0ff05db2040)
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
            type_hints = typing.get_type_hints(_typecheckingstub__345e7239330ae1a22d1b8c13579137bf412cfd5c4e89d77849f9105280384455)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33798dd711b0542512b9d4144de4a9dcf292f8930f7142d78ecb17aaebba0377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleNetappVolumeReplicationHybridPeeringDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationHybridPeeringDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9321e3b55b4a88d1a03abace9fa3384017558187d767aedad6aa96107a4c6bef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="commandExpiryTime")
    def command_expiry_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commandExpiryTime"))

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passphrase"))

    @builtins.property
    @jsii.member(jsii_name="peerClusterName")
    def peer_cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerClusterName"))

    @builtins.property
    @jsii.member(jsii_name="peerSvmName")
    def peer_svm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerSvmName"))

    @builtins.property
    @jsii.member(jsii_name="peerVolumeName")
    def peer_volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerVolumeName"))

    @builtins.property
    @jsii.member(jsii_name="subnetIp")
    def subnet_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetIp"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeReplicationHybridPeeringDetails]:
        return typing.cast(typing.Optional[GoogleNetappVolumeReplicationHybridPeeringDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeReplicationHybridPeeringDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74687e54d2e31b0f0e961cb7daa8499ef179910379606215ecdb2fdc7a3a15ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetappVolumeReplicationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#create GoogleNetappVolumeReplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#delete GoogleNetappVolumeReplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#update GoogleNetappVolumeReplication#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3cf9ecdfae3026670a83e090192ac9c8f6e507b55ddb0ad8cf281e6d25d0314)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#create GoogleNetappVolumeReplication#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#delete GoogleNetappVolumeReplication#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume_replication#update GoogleNetappVolumeReplication#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeReplicationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeReplicationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6826a152909a66ec5f44287e633d7b0375f82aa6728ff610e9ac11a46f5fe772)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b527e0ba9c3989ee9f2524889c9a38dc1eba9aa32af0f63c28f2036aeef2ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5c8678b220163857c40a802b3f47b5a949b6f97d13a166681f7e932545748d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354b46fec908fd6637124b2e5b3ac7eeec5068f313e901873ca7ee1978fde3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeReplicationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeReplicationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeReplicationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df31a63a08bd7bc1b9a452411486ddefc8119a399eb21b7996047b1bc8cbcc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationTransferStats",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleNetappVolumeReplicationTransferStats:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeReplicationTransferStats(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeReplicationTransferStatsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationTransferStatsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eddeae7f37a401d6e80bb12102a4ac4aee5d3e8e7d1b87a323b9d48e322d683)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetappVolumeReplicationTransferStatsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187531f3539f2ecb3375927f2c1e844b58255efae451cbe17cf0f85bff623c83)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetappVolumeReplicationTransferStatsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e61357a1606d4ee743ba18a0c2bed2e33d8c23007adb40a7a5ba6ce194ac82d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__626614756cc53f26c0efeb13a573dfef071be9de877f8dcdc2dfbc3ec0f734d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab499fc305189c8d24c95353e29331571eb753d0c17492274809b340500287aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleNetappVolumeReplicationTransferStatsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolumeReplication.GoogleNetappVolumeReplicationTransferStatsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf8c38cdb1da7191bdec08d29be0b40ff14dfc11b91dc327254c5c4abb1d7554)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="lagDuration")
    def lag_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lagDuration"))

    @builtins.property
    @jsii.member(jsii_name="lastTransferBytes")
    def last_transfer_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransferBytes"))

    @builtins.property
    @jsii.member(jsii_name="lastTransferDuration")
    def last_transfer_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransferDuration"))

    @builtins.property
    @jsii.member(jsii_name="lastTransferEndTime")
    def last_transfer_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransferEndTime"))

    @builtins.property
    @jsii.member(jsii_name="lastTransferError")
    def last_transfer_error(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransferError"))

    @builtins.property
    @jsii.member(jsii_name="totalTransferDuration")
    def total_transfer_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalTransferDuration"))

    @builtins.property
    @jsii.member(jsii_name="transferBytes")
    def transfer_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transferBytes"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeReplicationTransferStats]:
        return typing.cast(typing.Optional[GoogleNetappVolumeReplicationTransferStats], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeReplicationTransferStats],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a9b8db655a48594b334af8adfae6a03d3ae8a3085d43174adc1a916b46bcc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetappVolumeReplication",
    "GoogleNetappVolumeReplicationConfig",
    "GoogleNetappVolumeReplicationDestinationVolumeParameters",
    "GoogleNetappVolumeReplicationDestinationVolumeParametersOutputReference",
    "GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy",
    "GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference",
    "GoogleNetappVolumeReplicationHybridPeeringDetails",
    "GoogleNetappVolumeReplicationHybridPeeringDetailsList",
    "GoogleNetappVolumeReplicationHybridPeeringDetailsOutputReference",
    "GoogleNetappVolumeReplicationTimeouts",
    "GoogleNetappVolumeReplicationTimeoutsOutputReference",
    "GoogleNetappVolumeReplicationTransferStats",
    "GoogleNetappVolumeReplicationTransferStatsList",
    "GoogleNetappVolumeReplicationTransferStatsOutputReference",
]

publication.publish()

def _typecheckingstub__6d6126fa22046d0ed8522e234de860bf819686da8cdc43d31cea885ee0595881(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    replication_schedule: builtins.str,
    volume_name: builtins.str,
    delete_destination_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    destination_volume_parameters: typing.Optional[typing.Union[GoogleNetappVolumeReplicationDestinationVolumeParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    force_stopping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetappVolumeReplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__f27fdf5b650155ff4b574c4586217422a480d744c0d3f6f8c1072deee89e0336(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd6e1b8fa494052e52d3af847d38ed86896e7945a01a40f717cc22d72b55a05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf2f0086da6070717a78a2daa3217ddd6cceaef384f7d3af9cf485315d8ebf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d11537c23d3287d054b6dc0e1ecab187e469bedf736a97e8880c7e35bc72cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1bf3dd644a3e468677fb9b9e7a1981b269ae89a7e1510e5ce120fe32dab0b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d41f2756677485e63408f0ea6b43332222487a7e1ee11ed369a4fa9a1e9b50(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04670739c4763417e1a24657de152f06c779ccc50c5592c35c405f90bb970bfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8803c507faab6f347ff118547a0e08f04f85e67b14552bf5b568dc60cb7e6425(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d703f066ebdb1aca6a4b326996185a43e64389a4fdb491f71f6da6f1b689d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fadc032fe3650f461d92ea197996ce12645d7ed4f39ad07ff4bd2577955bb57(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9047a62b9af59d951cada1cc9771d829190a83797f39e149e3fe6168ec2536dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b217bc2f7009cf7ac08bc01ba8eea60eea474b961782cda91c8906509febf80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cbf0af59e5796f1fa2c79c57f84db776001762fbac29f2a95a615c5d7b803b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3732427564d730d8667176b6e9794557575ca84e70a682ef139e59e406b056f2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    replication_schedule: builtins.str,
    volume_name: builtins.str,
    delete_destination_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    destination_volume_parameters: typing.Optional[typing.Union[GoogleNetappVolumeReplicationDestinationVolumeParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    force_stopping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetappVolumeReplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd9d3d19b613945b0864a51246dd0e03683ad95a84f2942db838dcc5f92bb37(
    *,
    storage_pool: builtins.str,
    description: typing.Optional[builtins.str] = None,
    share_name: typing.Optional[builtins.str] = None,
    tiering_policy: typing.Optional[typing.Union[GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c837df4602549992badbc53cce99825b1f6ed5a6221254aa95c53e05a2fd642d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22459ea1ba0f043f9f8d023da1bbf578ae749e847b4b3c883abdbde65bf71b25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109b1e886df5a95d41699c03a55871ace36cfa93dcb064d1c4e06d62d6eed543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236a5062e1b85d00a307838f2d5e065eca197e13cba5a3bd847d6c3c9bde0afa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c1edee9511fbc0acd66464cd11a36a5a39d34e1745abceb2ae7a1b1497c524(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb21ef313c7ac7c3620bd20acd2ca9699c22cdf63f4498cbc2d14c5a9c339113(
    value: typing.Optional[GoogleNetappVolumeReplicationDestinationVolumeParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6cc3b16696837b9080da3ea4072f5142ed08e13382b8d2a834d2519c04756c(
    *,
    cooling_threshold_days: typing.Optional[jsii.Number] = None,
    tier_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da658307a6be09baa690db0c4943dcc2ca40c3a77af918f0df16af2ecb26eab6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d17dd55854263283dc0d4eb2942b307c694eda71da77241c0735d4e7184baa5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0130403d7f16c64b4dd80ac9fd39d88aebbe0bef72dedc1762fec4e4b7603e6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d067a80e3d7b2be38bc3af979e6e718b76590b1e7d776519f46498a40d8af13(
    value: typing.Optional[GoogleNetappVolumeReplicationDestinationVolumeParametersTieringPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f8c1ac0c809eaf9b0bed754245ce064f7022aac905d98e5a1b67a6927190ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b04245af250e65dbf462ff4062745dd2a222fab07d8048ec512d084a6e2b5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76393678275be93e6e338cf2739748b7c292b554723ae95a066a0ff05db2040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345e7239330ae1a22d1b8c13579137bf412cfd5c4e89d77849f9105280384455(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33798dd711b0542512b9d4144de4a9dcf292f8930f7142d78ecb17aaebba0377(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9321e3b55b4a88d1a03abace9fa3384017558187d767aedad6aa96107a4c6bef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74687e54d2e31b0f0e961cb7daa8499ef179910379606215ecdb2fdc7a3a15ee(
    value: typing.Optional[GoogleNetappVolumeReplicationHybridPeeringDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3cf9ecdfae3026670a83e090192ac9c8f6e507b55ddb0ad8cf281e6d25d0314(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6826a152909a66ec5f44287e633d7b0375f82aa6728ff610e9ac11a46f5fe772(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b527e0ba9c3989ee9f2524889c9a38dc1eba9aa32af0f63c28f2036aeef2ba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5c8678b220163857c40a802b3f47b5a949b6f97d13a166681f7e932545748d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354b46fec908fd6637124b2e5b3ac7eeec5068f313e901873ca7ee1978fde3e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df31a63a08bd7bc1b9a452411486ddefc8119a399eb21b7996047b1bc8cbcc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeReplicationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eddeae7f37a401d6e80bb12102a4ac4aee5d3e8e7d1b87a323b9d48e322d683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187531f3539f2ecb3375927f2c1e844b58255efae451cbe17cf0f85bff623c83(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e61357a1606d4ee743ba18a0c2bed2e33d8c23007adb40a7a5ba6ce194ac82d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626614756cc53f26c0efeb13a573dfef071be9de877f8dcdc2dfbc3ec0f734d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab499fc305189c8d24c95353e29331571eb753d0c17492274809b340500287aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8c38cdb1da7191bdec08d29be0b40ff14dfc11b91dc327254c5c4abb1d7554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a9b8db655a48594b334af8adfae6a03d3ae8a3085d43174adc1a916b46bcc6(
    value: typing.Optional[GoogleNetappVolumeReplicationTransferStats],
) -> None:
    """Type checking stubs"""
    pass
