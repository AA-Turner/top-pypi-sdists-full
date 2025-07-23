r'''
# `google_netapp_volume_replication`

Refer to the Terraform Registry for docs: [`google_netapp_volume_replication`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication).
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


class NetappVolumeReplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication google_netapp_volume_replication}.'''

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
        destination_volume_parameters: typing.Optional[typing.Union["NetappVolumeReplicationDestinationVolumeParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        force_stopping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeReplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication google_netapp_volume_replication} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Name of region for this resource. The resource needs to be created in the region of the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#location NetappVolumeReplication#location}
        :param name: The name of the replication. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#name NetappVolumeReplication#name}
        :param replication_schedule: Specifies the replication interval. Possible values: ["EVERY_10_MINUTES", "HOURLY", "DAILY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#replication_schedule NetappVolumeReplication#replication_schedule}
        :param volume_name: The name of the existing source volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#volume_name NetappVolumeReplication#volume_name}
        :param delete_destination_volume: A destination volume is created as part of replication creation. The destination volume will not became under Terraform management unless you import it manually. If you delete the replication, this volume will remain. Setting this parameter to true will delete the *current* destination volume when destroying the replication. If you reversed the replication direction, this will be your former source volume! For production use, it is recommended to keep this parameter false to avoid accidental volume deletion. Handle with care. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#delete_destination_volume NetappVolumeReplication#delete_destination_volume}
        :param description: An description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#description NetappVolumeReplication#description}
        :param destination_volume_parameters: destination_volume_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#destination_volume_parameters NetappVolumeReplication#destination_volume_parameters}
        :param force_stopping: Only replications with mirror_state=MIRRORED can be stopped. A replication in mirror_state=TRANSFERRING currently receives an update and stopping the update might be undesirable. Set this parameter to true to stop anyway. All data transferred to the destination will be discarded and content of destination volume will remain at the state of the last successful update. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#force_stopping NetappVolumeReplication#force_stopping}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#id NetappVolumeReplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#labels NetappVolumeReplication#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#project NetappVolumeReplication#project}.
        :param replication_enabled: Set to false to stop/break the mirror. Stopping the mirror makes the destination volume read-write and act independently from the source volume. Set to true to enable/resume the mirror. WARNING: Resuming a mirror overwrites any changes done to the destination volume with the content of the source volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#replication_enabled NetappVolumeReplication#replication_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#timeouts NetappVolumeReplication#timeouts}
        :param wait_for_mirror: Replication resource state is independent of mirror_state. With enough data, it can take many hours for mirror_state to reach MIRRORED. If you want Terraform to wait for the mirror to finish on create/stop/resume operations, set this parameter to true. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#wait_for_mirror NetappVolumeReplication#wait_for_mirror}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef6ed6cd3ce1743cc310d6ab6b04e0258cdc6843232fe338fa793434c5d0d6a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetappVolumeReplicationConfig(
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
        '''Generates CDKTF code for importing a NetappVolumeReplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetappVolumeReplication to import.
        :param import_from_id: The id of the existing NetappVolumeReplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetappVolumeReplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb611deabe0c85bdbf541eabaf1ae2c0a77322bc41623644a3f86de7d4bae10)
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
        tiering_policy: typing.Optional[typing.Union["NetappVolumeReplicationDestinationVolumeParametersTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_pool: Name of an existing storage pool for the destination volume with format: 'projects/{{project}}/locations/{{location}}/storagePools/{{poolId}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#storage_pool NetappVolumeReplication#storage_pool}
        :param description: Description for the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#description NetappVolumeReplication#description}
        :param share_name: Share name for destination volume. If not specified, name of source volume's share name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#share_name NetappVolumeReplication#share_name}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#tiering_policy NetappVolumeReplication#tiering_policy}
        :param volume_id: Name for the destination volume to be created. If not specified, the name of the source volume will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#volume_id NetappVolumeReplication#volume_id}
        '''
        value = NetappVolumeReplicationDestinationVolumeParameters(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#create NetappVolumeReplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#delete NetappVolumeReplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#update NetappVolumeReplication#update}.
        '''
        value = NetappVolumeReplicationTimeouts(
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
    ) -> "NetappVolumeReplicationDestinationVolumeParametersOutputReference":
        return typing.cast("NetappVolumeReplicationDestinationVolumeParametersOutputReference", jsii.get(self, "destinationVolumeParameters"))

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
    ) -> "NetappVolumeReplicationHybridPeeringDetailsList":
        return typing.cast("NetappVolumeReplicationHybridPeeringDetailsList", jsii.get(self, "hybridPeeringDetails"))

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
    def timeouts(self) -> "NetappVolumeReplicationTimeoutsOutputReference":
        return typing.cast("NetappVolumeReplicationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="transferStats")
    def transfer_stats(self) -> "NetappVolumeReplicationTransferStatsList":
        return typing.cast("NetappVolumeReplicationTransferStatsList", jsii.get(self, "transferStats"))

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
    ) -> typing.Optional["NetappVolumeReplicationDestinationVolumeParameters"]:
        return typing.cast(typing.Optional["NetappVolumeReplicationDestinationVolumeParameters"], jsii.get(self, "destinationVolumeParametersInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappVolumeReplicationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappVolumeReplicationTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5f55246bbf3baef6c35dc722bcfcab589ebd649dc6e541241089c4e08d534636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteDestinationVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31211c694570bdcf177bdb18ce0b68fee337efc91fd13bf45641a0ce6a068478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efc293a963dc734685b4266b5cd997f14c439c507e8372db5bad1467eb7804da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceStopping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f790f6e82b105c9ce463ef255c90a3c8348fbbea6503a7e5766c9add674d99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed13c3ed45ab8bd7ff2bc14fc4fb0c83aa890fe06d729e89bd514b3016e5438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c0f0a32f8728ee97d067de98f795586f4a394e34367d6ad6270aef7fad4cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28a258a3d4add45d6f431c940c00eacb6b58ef3f93acda4daf6819271d7f7ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309962afcda8069b7930b6b12e3f1a07c8308dcb08137d6661e76cdb31f2b907)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89157d3e0460314ff423e2834d7f1726a26d817f3353487410ecc08d0e704f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationSchedule")
    def replication_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationSchedule"))

    @replication_schedule.setter
    def replication_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36daf0e8af397784c8bc6c13a6c58d25c650220845e10d4382144fb84e7de875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeName")
    def volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeName"))

    @volume_name.setter
    def volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e35b488f5be59ec37048a4db1407f3ab92ed12be32da5655e1d4d280ff2dc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c66c420ba22e46a74a067c98fc98caf4c3a71f03b6ed8ef5210683aad3780c13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForMirror", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationConfig",
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
class NetappVolumeReplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination_volume_parameters: typing.Optional[typing.Union["NetappVolumeReplicationDestinationVolumeParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        force_stopping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeReplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param location: Name of region for this resource. The resource needs to be created in the region of the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#location NetappVolumeReplication#location}
        :param name: The name of the replication. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#name NetappVolumeReplication#name}
        :param replication_schedule: Specifies the replication interval. Possible values: ["EVERY_10_MINUTES", "HOURLY", "DAILY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#replication_schedule NetappVolumeReplication#replication_schedule}
        :param volume_name: The name of the existing source volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#volume_name NetappVolumeReplication#volume_name}
        :param delete_destination_volume: A destination volume is created as part of replication creation. The destination volume will not became under Terraform management unless you import it manually. If you delete the replication, this volume will remain. Setting this parameter to true will delete the *current* destination volume when destroying the replication. If you reversed the replication direction, this will be your former source volume! For production use, it is recommended to keep this parameter false to avoid accidental volume deletion. Handle with care. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#delete_destination_volume NetappVolumeReplication#delete_destination_volume}
        :param description: An description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#description NetappVolumeReplication#description}
        :param destination_volume_parameters: destination_volume_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#destination_volume_parameters NetappVolumeReplication#destination_volume_parameters}
        :param force_stopping: Only replications with mirror_state=MIRRORED can be stopped. A replication in mirror_state=TRANSFERRING currently receives an update and stopping the update might be undesirable. Set this parameter to true to stop anyway. All data transferred to the destination will be discarded and content of destination volume will remain at the state of the last successful update. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#force_stopping NetappVolumeReplication#force_stopping}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#id NetappVolumeReplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#labels NetappVolumeReplication#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#project NetappVolumeReplication#project}.
        :param replication_enabled: Set to false to stop/break the mirror. Stopping the mirror makes the destination volume read-write and act independently from the source volume. Set to true to enable/resume the mirror. WARNING: Resuming a mirror overwrites any changes done to the destination volume with the content of the source volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#replication_enabled NetappVolumeReplication#replication_enabled}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#timeouts NetappVolumeReplication#timeouts}
        :param wait_for_mirror: Replication resource state is independent of mirror_state. With enough data, it can take many hours for mirror_state to reach MIRRORED. If you want Terraform to wait for the mirror to finish on create/stop/resume operations, set this parameter to true. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#wait_for_mirror NetappVolumeReplication#wait_for_mirror}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination_volume_parameters, dict):
            destination_volume_parameters = NetappVolumeReplicationDestinationVolumeParameters(**destination_volume_parameters)
        if isinstance(timeouts, dict):
            timeouts = NetappVolumeReplicationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba8920d569fac96235b47f22d7e68677c0f633c128e19be11d32e0fa766f5e9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#location NetappVolumeReplication#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the replication. Needs to be unique per location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#name NetappVolumeReplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_schedule(self) -> builtins.str:
        '''Specifies the replication interval. Possible values: ["EVERY_10_MINUTES", "HOURLY", "DAILY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#replication_schedule NetappVolumeReplication#replication_schedule}
        '''
        result = self._values.get("replication_schedule")
        assert result is not None, "Required property 'replication_schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_name(self) -> builtins.str:
        '''The name of the existing source volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#volume_name NetappVolumeReplication#volume_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#delete_destination_volume NetappVolumeReplication#delete_destination_volume}
        '''
        result = self._values.get("delete_destination_volume")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#description NetappVolumeReplication#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_volume_parameters(
        self,
    ) -> typing.Optional["NetappVolumeReplicationDestinationVolumeParameters"]:
        '''destination_volume_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#destination_volume_parameters NetappVolumeReplication#destination_volume_parameters}
        '''
        result = self._values.get("destination_volume_parameters")
        return typing.cast(typing.Optional["NetappVolumeReplicationDestinationVolumeParameters"], result)

    @builtins.property
    def force_stopping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only replications with mirror_state=MIRRORED can be stopped.

        A replication in mirror_state=TRANSFERRING
        currently receives an update and stopping the update might be undesirable. Set this parameter to true
        to stop anyway. All data transferred to the destination will be discarded and content of destination
        volume will remain at the state of the last successful update. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#force_stopping NetappVolumeReplication#force_stopping}
        '''
        result = self._values.get("force_stopping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#id NetappVolumeReplication#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#labels NetappVolumeReplication#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#project NetappVolumeReplication#project}.'''
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#replication_enabled NetappVolumeReplication#replication_enabled}
        '''
        result = self._values.get("replication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetappVolumeReplicationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#timeouts NetappVolumeReplication#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetappVolumeReplicationTimeouts"], result)

    @builtins.property
    def wait_for_mirror(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Replication resource state is independent of mirror_state.

        With enough data, it can take many hours
        for mirror_state to reach MIRRORED. If you want Terraform to wait for the mirror to finish on
        create/stop/resume operations, set this parameter to true. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#wait_for_mirror NetappVolumeReplication#wait_for_mirror}
        '''
        result = self._values.get("wait_for_mirror")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeReplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationDestinationVolumeParameters",
    jsii_struct_bases=[],
    name_mapping={
        "storage_pool": "storagePool",
        "description": "description",
        "share_name": "shareName",
        "tiering_policy": "tieringPolicy",
        "volume_id": "volumeId",
    },
)
class NetappVolumeReplicationDestinationVolumeParameters:
    def __init__(
        self,
        *,
        storage_pool: builtins.str,
        description: typing.Optional[builtins.str] = None,
        share_name: typing.Optional[builtins.str] = None,
        tiering_policy: typing.Optional[typing.Union["NetappVolumeReplicationDestinationVolumeParametersTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param storage_pool: Name of an existing storage pool for the destination volume with format: 'projects/{{project}}/locations/{{location}}/storagePools/{{poolId}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#storage_pool NetappVolumeReplication#storage_pool}
        :param description: Description for the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#description NetappVolumeReplication#description}
        :param share_name: Share name for destination volume. If not specified, name of source volume's share name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#share_name NetappVolumeReplication#share_name}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#tiering_policy NetappVolumeReplication#tiering_policy}
        :param volume_id: Name for the destination volume to be created. If not specified, the name of the source volume will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#volume_id NetappVolumeReplication#volume_id}
        '''
        if isinstance(tiering_policy, dict):
            tiering_policy = NetappVolumeReplicationDestinationVolumeParametersTieringPolicy(**tiering_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbb5b3c469eabeb6aa830ef2e1667e2ffdd036c2f7a69d795c7c7c36c544dd3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#storage_pool NetappVolumeReplication#storage_pool}
        '''
        result = self._values.get("storage_pool")
        assert result is not None, "Required property 'storage_pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description for the destination volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#description NetappVolumeReplication#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_name(self) -> typing.Optional[builtins.str]:
        '''Share name for destination volume. If not specified, name of source volume's share name will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#share_name NetappVolumeReplication#share_name}
        '''
        result = self._values.get("share_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tiering_policy(
        self,
    ) -> typing.Optional["NetappVolumeReplicationDestinationVolumeParametersTieringPolicy"]:
        '''tiering_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#tiering_policy NetappVolumeReplication#tiering_policy}
        '''
        result = self._values.get("tiering_policy")
        return typing.cast(typing.Optional["NetappVolumeReplicationDestinationVolumeParametersTieringPolicy"], result)

    @builtins.property
    def volume_id(self) -> typing.Optional[builtins.str]:
        '''Name for the destination volume to be created.

        If not specified, the name of the source volume will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#volume_id NetappVolumeReplication#volume_id}
        '''
        result = self._values.get("volume_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeReplicationDestinationVolumeParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeReplicationDestinationVolumeParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationDestinationVolumeParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67dd776c5ca5a77ba201102f9102282df6b9a7feb9cab242cdac8973c2f7a0a1)
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
        :param cooling_threshold_days: Optional. Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183. Default is 31. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#cooling_threshold_days NetappVolumeReplication#cooling_threshold_days}
        :param tier_action: Optional. Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#tier_action NetappVolumeReplication#tier_action}
        '''
        value = NetappVolumeReplicationDestinationVolumeParametersTieringPolicy(
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
    ) -> "NetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference":
        return typing.cast("NetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference", jsii.get(self, "tieringPolicy"))

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
    ) -> typing.Optional["NetappVolumeReplicationDestinationVolumeParametersTieringPolicy"]:
        return typing.cast(typing.Optional["NetappVolumeReplicationDestinationVolumeParametersTieringPolicy"], jsii.get(self, "tieringPolicyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2f4950340d40d6e09b680ce685509115b84a52f0ea6d4d38599bafa3920f35af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareName")
    def share_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareName"))

    @share_name.setter
    def share_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3930bb785bc1780a342bb35dbbb744723cde7e085384366dd50bd49879597cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePool")
    def storage_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePool"))

    @storage_pool.setter
    def storage_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac5a6e8953c1c921fa824db12b1c5b46a2bc6047f968c75d43f52e6e40cc738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeId"))

    @volume_id.setter
    def volume_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331b650d386597137c45ba92455882fb93c8107efd781f306d8a2f55b05b0bc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeReplicationDestinationVolumeParameters]:
        return typing.cast(typing.Optional[NetappVolumeReplicationDestinationVolumeParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeReplicationDestinationVolumeParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697f8e4c8e8cfcb1c5589a81ac6b0648bfaddc55410b338ca9b641fe6bb0cff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationDestinationVolumeParametersTieringPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cooling_threshold_days": "coolingThresholdDays",
        "tier_action": "tierAction",
    },
)
class NetappVolumeReplicationDestinationVolumeParametersTieringPolicy:
    def __init__(
        self,
        *,
        cooling_threshold_days: typing.Optional[jsii.Number] = None,
        tier_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_threshold_days: Optional. Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183. Default is 31. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#cooling_threshold_days NetappVolumeReplication#cooling_threshold_days}
        :param tier_action: Optional. Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#tier_action NetappVolumeReplication#tier_action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082b6bd103df72c66a36597d53d3d2fa9340b8533b01bf1c15b130da38c0090a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#cooling_threshold_days NetappVolumeReplication#cooling_threshold_days}
        '''
        result = self._values.get("cooling_threshold_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_action(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#tier_action NetappVolumeReplication#tier_action}
        '''
        result = self._values.get("tier_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeReplicationDestinationVolumeParametersTieringPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef7aa031281f0335213e82631f8f7b33b1d9a7ec323287722669c77d08638d3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ace9e52d0b01ebef7acb111206870849f1d078318dd2be7a94e5184c2efe86cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolingThresholdDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierAction")
    def tier_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tierAction"))

    @tier_action.setter
    def tier_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bbedec467cd4767673c4f209bb2eabe3c501e0c3dd61bbaa2eb8a207926809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeReplicationDestinationVolumeParametersTieringPolicy]:
        return typing.cast(typing.Optional[NetappVolumeReplicationDestinationVolumeParametersTieringPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeReplicationDestinationVolumeParametersTieringPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2143308ac2b4654350650d5415cc3526bf727ef9d05cd5d3ce1eb4a6ad3291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationHybridPeeringDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetappVolumeReplicationHybridPeeringDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeReplicationHybridPeeringDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeReplicationHybridPeeringDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationHybridPeeringDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7eb38973242caec5d6527e010f3639f97518bce700804d5cafc143f7b09e3a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetappVolumeReplicationHybridPeeringDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac549ce5214be8011887d299124e219f1e9428c0e8f00c04e9e1abd1e0ce5cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeReplicationHybridPeeringDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124cbac93f952bb986de08245da49b1d7b4758abc446f34522a3ff507c82cf5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59a3a28513bc62e90e43d37183700f07f33db666c0e7a4c7247cfc9c3e4a6f2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7159f54a4bcd97625fd2c90e9bcfd0aaf4f98627f688997fa23a1dd435a524d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NetappVolumeReplicationHybridPeeringDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationHybridPeeringDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03c78201d73a0daf770de50f4f909e65c3fdcc8f194adfff164b8d4969dd50d9)
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
    ) -> typing.Optional[NetappVolumeReplicationHybridPeeringDetails]:
        return typing.cast(typing.Optional[NetappVolumeReplicationHybridPeeringDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeReplicationHybridPeeringDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b67e2436757b5c14cd443ae9851247ec087e99a27a538671ab14d707790591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetappVolumeReplicationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#create NetappVolumeReplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#delete NetappVolumeReplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#update NetappVolumeReplication#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f4c3142711d87440d3c3a6afad4ca83dfd08a028894019055114523822f816)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#create NetappVolumeReplication#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#delete NetappVolumeReplication#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume_replication#update NetappVolumeReplication#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeReplicationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeReplicationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9071ffb5a133d53e4ea6da5a80e35391dcd446259e9d8e2ea9b153b069d31737)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d39fc0b9e6431c5d379e9109f7db310944e7cb5ea48d7985acb41b172c20e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4899d89355acd2b5aaa9f92e4da1935cce552885a12c390ae4457d8036671d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844eee34cbf3572a5e1237152a6fa799844f24d2aae9dd8380ddb283a334a278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeReplicationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeReplicationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeReplicationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e749addb099a8af68fc90cd13fe2feda57a16a9938d31f47f49a37df15286b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationTransferStats",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetappVolumeReplicationTransferStats:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeReplicationTransferStats(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeReplicationTransferStatsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationTransferStatsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05f9d96cca8bb84a93fbe01461ae3315bf34239932a53368a9a38ce5dd692fb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetappVolumeReplicationTransferStatsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef58f2451584c0f277790b609966b5633ff3900f97c8bae0aa485518071c2e98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeReplicationTransferStatsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e143fd135573885b9bd8ecdbaa7ea59aed93d3f5fa4c5c575e853228c226ae29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__818b2e3f4f27b75cf47b4999624706ca1df51b0be97ddf5e1192bd7909442e28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__088052174400176178024ee3c13b030db7580bcee6e420146de5a7502a3776cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NetappVolumeReplicationTransferStatsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolumeReplication.NetappVolumeReplicationTransferStatsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1673a917d6a144046744bcad1530cc7ba381a7932b603f78203585b2eb966966)
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
    def internal_value(self) -> typing.Optional[NetappVolumeReplicationTransferStats]:
        return typing.cast(typing.Optional[NetappVolumeReplicationTransferStats], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeReplicationTransferStats],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba290ccf0e2172d3c38ee1dc962bc218bf01fdc9524a35ea674aac0f2dda3ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetappVolumeReplication",
    "NetappVolumeReplicationConfig",
    "NetappVolumeReplicationDestinationVolumeParameters",
    "NetappVolumeReplicationDestinationVolumeParametersOutputReference",
    "NetappVolumeReplicationDestinationVolumeParametersTieringPolicy",
    "NetappVolumeReplicationDestinationVolumeParametersTieringPolicyOutputReference",
    "NetappVolumeReplicationHybridPeeringDetails",
    "NetappVolumeReplicationHybridPeeringDetailsList",
    "NetappVolumeReplicationHybridPeeringDetailsOutputReference",
    "NetappVolumeReplicationTimeouts",
    "NetappVolumeReplicationTimeoutsOutputReference",
    "NetappVolumeReplicationTransferStats",
    "NetappVolumeReplicationTransferStatsList",
    "NetappVolumeReplicationTransferStatsOutputReference",
]

publication.publish()

def _typecheckingstub__fef6ed6cd3ce1743cc310d6ab6b04e0258cdc6843232fe338fa793434c5d0d6a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    replication_schedule: builtins.str,
    volume_name: builtins.str,
    delete_destination_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    destination_volume_parameters: typing.Optional[typing.Union[NetappVolumeReplicationDestinationVolumeParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    force_stopping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeReplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2cb611deabe0c85bdbf541eabaf1ae2c0a77322bc41623644a3f86de7d4bae10(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f55246bbf3baef6c35dc722bcfcab589ebd649dc6e541241089c4e08d534636(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31211c694570bdcf177bdb18ce0b68fee337efc91fd13bf45641a0ce6a068478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc293a963dc734685b4266b5cd997f14c439c507e8372db5bad1467eb7804da(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f790f6e82b105c9ce463ef255c90a3c8348fbbea6503a7e5766c9add674d99b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed13c3ed45ab8bd7ff2bc14fc4fb0c83aa890fe06d729e89bd514b3016e5438(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c0f0a32f8728ee97d067de98f795586f4a394e34367d6ad6270aef7fad4cec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28a258a3d4add45d6f431c940c00eacb6b58ef3f93acda4daf6819271d7f7ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309962afcda8069b7930b6b12e3f1a07c8308dcb08137d6661e76cdb31f2b907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89157d3e0460314ff423e2834d7f1726a26d817f3353487410ecc08d0e704f45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36daf0e8af397784c8bc6c13a6c58d25c650220845e10d4382144fb84e7de875(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e35b488f5be59ec37048a4db1407f3ab92ed12be32da5655e1d4d280ff2dc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66c420ba22e46a74a067c98fc98caf4c3a71f03b6ed8ef5210683aad3780c13(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba8920d569fac96235b47f22d7e68677c0f633c128e19be11d32e0fa766f5e9(
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
    destination_volume_parameters: typing.Optional[typing.Union[NetappVolumeReplicationDestinationVolumeParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    force_stopping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeReplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_mirror: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbb5b3c469eabeb6aa830ef2e1667e2ffdd036c2f7a69d795c7c7c36c544dd3(
    *,
    storage_pool: builtins.str,
    description: typing.Optional[builtins.str] = None,
    share_name: typing.Optional[builtins.str] = None,
    tiering_policy: typing.Optional[typing.Union[NetappVolumeReplicationDestinationVolumeParametersTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67dd776c5ca5a77ba201102f9102282df6b9a7feb9cab242cdac8973c2f7a0a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4950340d40d6e09b680ce685509115b84a52f0ea6d4d38599bafa3920f35af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3930bb785bc1780a342bb35dbbb744723cde7e085384366dd50bd49879597cfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac5a6e8953c1c921fa824db12b1c5b46a2bc6047f968c75d43f52e6e40cc738(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331b650d386597137c45ba92455882fb93c8107efd781f306d8a2f55b05b0bc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697f8e4c8e8cfcb1c5589a81ac6b0648bfaddc55410b338ca9b641fe6bb0cff1(
    value: typing.Optional[NetappVolumeReplicationDestinationVolumeParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082b6bd103df72c66a36597d53d3d2fa9340b8533b01bf1c15b130da38c0090a(
    *,
    cooling_threshold_days: typing.Optional[jsii.Number] = None,
    tier_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7aa031281f0335213e82631f8f7b33b1d9a7ec323287722669c77d08638d3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace9e52d0b01ebef7acb111206870849f1d078318dd2be7a94e5184c2efe86cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bbedec467cd4767673c4f209bb2eabe3c501e0c3dd61bbaa2eb8a207926809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2143308ac2b4654350650d5415cc3526bf727ef9d05cd5d3ce1eb4a6ad3291(
    value: typing.Optional[NetappVolumeReplicationDestinationVolumeParametersTieringPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7eb38973242caec5d6527e010f3639f97518bce700804d5cafc143f7b09e3a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac549ce5214be8011887d299124e219f1e9428c0e8f00c04e9e1abd1e0ce5cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124cbac93f952bb986de08245da49b1d7b4758abc446f34522a3ff507c82cf5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a3a28513bc62e90e43d37183700f07f33db666c0e7a4c7247cfc9c3e4a6f2d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7159f54a4bcd97625fd2c90e9bcfd0aaf4f98627f688997fa23a1dd435a524d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c78201d73a0daf770de50f4f909e65c3fdcc8f194adfff164b8d4969dd50d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b67e2436757b5c14cd443ae9851247ec087e99a27a538671ab14d707790591(
    value: typing.Optional[NetappVolumeReplicationHybridPeeringDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f4c3142711d87440d3c3a6afad4ca83dfd08a028894019055114523822f816(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9071ffb5a133d53e4ea6da5a80e35391dcd446259e9d8e2ea9b153b069d31737(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d39fc0b9e6431c5d379e9109f7db310944e7cb5ea48d7985acb41b172c20e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4899d89355acd2b5aaa9f92e4da1935cce552885a12c390ae4457d8036671d11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844eee34cbf3572a5e1237152a6fa799844f24d2aae9dd8380ddb283a334a278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e749addb099a8af68fc90cd13fe2feda57a16a9938d31f47f49a37df15286b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeReplicationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f9d96cca8bb84a93fbe01461ae3315bf34239932a53368a9a38ce5dd692fb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef58f2451584c0f277790b609966b5633ff3900f97c8bae0aa485518071c2e98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e143fd135573885b9bd8ecdbaa7ea59aed93d3f5fa4c5c575e853228c226ae29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818b2e3f4f27b75cf47b4999624706ca1df51b0be97ddf5e1192bd7909442e28(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088052174400176178024ee3c13b030db7580bcee6e420146de5a7502a3776cf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1673a917d6a144046744bcad1530cc7ba381a7932b603f78203585b2eb966966(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba290ccf0e2172d3c38ee1dc962bc218bf01fdc9524a35ea674aac0f2dda3ea3(
    value: typing.Optional[NetappVolumeReplicationTransferStats],
) -> None:
    """Type checking stubs"""
    pass
