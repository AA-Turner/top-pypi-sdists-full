r'''
# `google_pubsub_lite_topic`

Refer to the Terraform Registry for docs: [`google_pubsub_lite_topic`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic).
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


class PubsubLiteTopic(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopic",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic google_pubsub_lite_topic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        partition_config: typing.Optional[typing.Union["PubsubLiteTopicPartitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reservation_config: typing.Optional[typing.Union["PubsubLiteTopicReservationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_config: typing.Optional[typing.Union["PubsubLiteTopicRetentionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PubsubLiteTopicTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic google_pubsub_lite_topic} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#name PubsubLiteTopic#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#id PubsubLiteTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param partition_config: partition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#partition_config PubsubLiteTopic#partition_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#project PubsubLiteTopic#project}.
        :param region: The region of the pubsub lite topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#region PubsubLiteTopic#region}
        :param reservation_config: reservation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#reservation_config PubsubLiteTopic#reservation_config}
        :param retention_config: retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#retention_config PubsubLiteTopic#retention_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#timeouts PubsubLiteTopic#timeouts}
        :param zone: The zone of the pubsub lite topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#zone PubsubLiteTopic#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf67273eef62c203aa17d30a476bd41d91389291dafcc1ecf657ef0f30e4c912)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PubsubLiteTopicConfig(
            name=name,
            id=id,
            partition_config=partition_config,
            project=project,
            region=region,
            reservation_config=reservation_config,
            retention_config=retention_config,
            timeouts=timeouts,
            zone=zone,
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
        '''Generates CDKTF code for importing a PubsubLiteTopic resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PubsubLiteTopic to import.
        :param import_from_id: The id of the existing PubsubLiteTopic that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PubsubLiteTopic to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c90fa8eed90e734db115856f3dd604c640a31959995e7be4ddd6386e41e4363)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPartitionConfig")
    def put_partition_config(
        self,
        *,
        count: jsii.Number,
        capacity: typing.Optional[typing.Union["PubsubLiteTopicPartitionConfigCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: The number of partitions in the topic. Must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#count PubsubLiteTopic#count}
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#capacity PubsubLiteTopic#capacity}
        '''
        value = PubsubLiteTopicPartitionConfig(count=count, capacity=capacity)

        return typing.cast(None, jsii.invoke(self, "putPartitionConfig", [value]))

    @jsii.member(jsii_name="putReservationConfig")
    def put_reservation_config(
        self,
        *,
        throughput_reservation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param throughput_reservation: The Reservation to use for this topic's throughput capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#throughput_reservation PubsubLiteTopic#throughput_reservation}
        '''
        value = PubsubLiteTopicReservationConfig(
            throughput_reservation=throughput_reservation
        )

        return typing.cast(None, jsii.invoke(self, "putReservationConfig", [value]))

    @jsii.member(jsii_name="putRetentionConfig")
    def put_retention_config(
        self,
        *,
        per_partition_bytes: builtins.str,
        period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param per_partition_bytes: The provisioned storage, in bytes, per partition. If the number of bytes stored in any of the topic's partitions grows beyond this value, older messages will be dropped to make room for newer ones, regardless of the value of period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#per_partition_bytes PubsubLiteTopic#per_partition_bytes}
        :param period: How long a published message is retained. If unset, messages will be retained as long as the bytes retained for each partition is below perPartitionBytes. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#period PubsubLiteTopic#period}
        '''
        value = PubsubLiteTopicRetentionConfig(
            per_partition_bytes=per_partition_bytes, period=period
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#create PubsubLiteTopic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#delete PubsubLiteTopic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#update PubsubLiteTopic#update}.
        '''
        value = PubsubLiteTopicTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPartitionConfig")
    def reset_partition_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReservationConfig")
    def reset_reservation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationConfig", []))

    @jsii.member(jsii_name="resetRetentionConfig")
    def reset_retention_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    @jsii.member(jsii_name="partitionConfig")
    def partition_config(self) -> "PubsubLiteTopicPartitionConfigOutputReference":
        return typing.cast("PubsubLiteTopicPartitionConfigOutputReference", jsii.get(self, "partitionConfig"))

    @builtins.property
    @jsii.member(jsii_name="reservationConfig")
    def reservation_config(self) -> "PubsubLiteTopicReservationConfigOutputReference":
        return typing.cast("PubsubLiteTopicReservationConfigOutputReference", jsii.get(self, "reservationConfig"))

    @builtins.property
    @jsii.member(jsii_name="retentionConfig")
    def retention_config(self) -> "PubsubLiteTopicRetentionConfigOutputReference":
        return typing.cast("PubsubLiteTopicRetentionConfigOutputReference", jsii.get(self, "retentionConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PubsubLiteTopicTimeoutsOutputReference":
        return typing.cast("PubsubLiteTopicTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionConfigInput")
    def partition_config_input(
        self,
    ) -> typing.Optional["PubsubLiteTopicPartitionConfig"]:
        return typing.cast(typing.Optional["PubsubLiteTopicPartitionConfig"], jsii.get(self, "partitionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationConfigInput")
    def reservation_config_input(
        self,
    ) -> typing.Optional["PubsubLiteTopicReservationConfig"]:
        return typing.cast(typing.Optional["PubsubLiteTopicReservationConfig"], jsii.get(self, "reservationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionConfigInput")
    def retention_config_input(
        self,
    ) -> typing.Optional["PubsubLiteTopicRetentionConfig"]:
        return typing.cast(typing.Optional["PubsubLiteTopicRetentionConfig"], jsii.get(self, "retentionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PubsubLiteTopicTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PubsubLiteTopicTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8929e4c9ed025ac62404a5ef1ff8a6a9311d0017c68c51a338f7c51a9e853e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f2f3207030a2dc8c8c9df46d844ac6a4704e90e619538a22dcbeb41774fde6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664d2ef4f9f71cfd4140a3afe9ee9b8f849f3b62259cc847feca4a28a631f474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc82138bb45e3d2688a58aa43a5dc8ee05dad589c9d38ab4eceb92de2fb37f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3d353851d9490075232ffd831125781dd0c105b357b14e32625a2c1c99b341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicConfig",
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
        "id": "id",
        "partition_config": "partitionConfig",
        "project": "project",
        "region": "region",
        "reservation_config": "reservationConfig",
        "retention_config": "retentionConfig",
        "timeouts": "timeouts",
        "zone": "zone",
    },
)
class PubsubLiteTopicConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        partition_config: typing.Optional[typing.Union["PubsubLiteTopicPartitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reservation_config: typing.Optional[typing.Union["PubsubLiteTopicReservationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_config: typing.Optional[typing.Union["PubsubLiteTopicRetentionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PubsubLiteTopicTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#name PubsubLiteTopic#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#id PubsubLiteTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param partition_config: partition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#partition_config PubsubLiteTopic#partition_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#project PubsubLiteTopic#project}.
        :param region: The region of the pubsub lite topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#region PubsubLiteTopic#region}
        :param reservation_config: reservation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#reservation_config PubsubLiteTopic#reservation_config}
        :param retention_config: retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#retention_config PubsubLiteTopic#retention_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#timeouts PubsubLiteTopic#timeouts}
        :param zone: The zone of the pubsub lite topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#zone PubsubLiteTopic#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(partition_config, dict):
            partition_config = PubsubLiteTopicPartitionConfig(**partition_config)
        if isinstance(reservation_config, dict):
            reservation_config = PubsubLiteTopicReservationConfig(**reservation_config)
        if isinstance(retention_config, dict):
            retention_config = PubsubLiteTopicRetentionConfig(**retention_config)
        if isinstance(timeouts, dict):
            timeouts = PubsubLiteTopicTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b1b02a5e3da01e2b98a8ba1365d952b90c09cf342b25ed0f01dc4d81fbbffb5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument partition_config", value=partition_config, expected_type=type_hints["partition_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument reservation_config", value=reservation_config, expected_type=type_hints["reservation_config"])
            check_type(argname="argument retention_config", value=retention_config, expected_type=type_hints["retention_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if partition_config is not None:
            self._values["partition_config"] = partition_config
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if reservation_config is not None:
            self._values["reservation_config"] = reservation_config
        if retention_config is not None:
            self._values["retention_config"] = retention_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zone is not None:
            self._values["zone"] = zone

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
        '''Name of the topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#name PubsubLiteTopic#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#id PubsubLiteTopic#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_config(self) -> typing.Optional["PubsubLiteTopicPartitionConfig"]:
        '''partition_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#partition_config PubsubLiteTopic#partition_config}
        '''
        result = self._values.get("partition_config")
        return typing.cast(typing.Optional["PubsubLiteTopicPartitionConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#project PubsubLiteTopic#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the pubsub lite topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#region PubsubLiteTopic#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_config(self) -> typing.Optional["PubsubLiteTopicReservationConfig"]:
        '''reservation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#reservation_config PubsubLiteTopic#reservation_config}
        '''
        result = self._values.get("reservation_config")
        return typing.cast(typing.Optional["PubsubLiteTopicReservationConfig"], result)

    @builtins.property
    def retention_config(self) -> typing.Optional["PubsubLiteTopicRetentionConfig"]:
        '''retention_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#retention_config PubsubLiteTopic#retention_config}
        '''
        result = self._values.get("retention_config")
        return typing.cast(typing.Optional["PubsubLiteTopicRetentionConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PubsubLiteTopicTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#timeouts PubsubLiteTopic#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PubsubLiteTopicTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The zone of the pubsub lite topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#zone PubsubLiteTopic#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubLiteTopicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicPartitionConfig",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "capacity": "capacity"},
)
class PubsubLiteTopicPartitionConfig:
    def __init__(
        self,
        *,
        count: jsii.Number,
        capacity: typing.Optional[typing.Union["PubsubLiteTopicPartitionConfigCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: The number of partitions in the topic. Must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#count PubsubLiteTopic#count}
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#capacity PubsubLiteTopic#capacity}
        '''
        if isinstance(capacity, dict):
            capacity = PubsubLiteTopicPartitionConfigCapacity(**capacity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072a6d9da1433314fe64f67879850976c9d12e5ff564b929050bb4b839116269)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
        }
        if capacity is not None:
            self._values["capacity"] = capacity

    @builtins.property
    def count(self) -> jsii.Number:
        '''The number of partitions in the topic. Must be at least 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#count PubsubLiteTopic#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def capacity(self) -> typing.Optional["PubsubLiteTopicPartitionConfigCapacity"]:
        '''capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#capacity PubsubLiteTopic#capacity}
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional["PubsubLiteTopicPartitionConfigCapacity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubLiteTopicPartitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicPartitionConfigCapacity",
    jsii_struct_bases=[],
    name_mapping={
        "publish_mib_per_sec": "publishMibPerSec",
        "subscribe_mib_per_sec": "subscribeMibPerSec",
    },
)
class PubsubLiteTopicPartitionConfigCapacity:
    def __init__(
        self,
        *,
        publish_mib_per_sec: jsii.Number,
        subscribe_mib_per_sec: jsii.Number,
    ) -> None:
        '''
        :param publish_mib_per_sec: Subscribe throughput capacity per partition in MiB/s. Must be >= 4 and <= 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#publish_mib_per_sec PubsubLiteTopic#publish_mib_per_sec}
        :param subscribe_mib_per_sec: Publish throughput capacity per partition in MiB/s. Must be >= 4 and <= 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#subscribe_mib_per_sec PubsubLiteTopic#subscribe_mib_per_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42942f9fd993d5297e631b4af728f72d1ef860d435e847cc740aaede8e2ae202)
            check_type(argname="argument publish_mib_per_sec", value=publish_mib_per_sec, expected_type=type_hints["publish_mib_per_sec"])
            check_type(argname="argument subscribe_mib_per_sec", value=subscribe_mib_per_sec, expected_type=type_hints["subscribe_mib_per_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "publish_mib_per_sec": publish_mib_per_sec,
            "subscribe_mib_per_sec": subscribe_mib_per_sec,
        }

    @builtins.property
    def publish_mib_per_sec(self) -> jsii.Number:
        '''Subscribe throughput capacity per partition in MiB/s. Must be >= 4 and <= 16.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#publish_mib_per_sec PubsubLiteTopic#publish_mib_per_sec}
        '''
        result = self._values.get("publish_mib_per_sec")
        assert result is not None, "Required property 'publish_mib_per_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subscribe_mib_per_sec(self) -> jsii.Number:
        '''Publish throughput capacity per partition in MiB/s. Must be >= 4 and <= 16.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#subscribe_mib_per_sec PubsubLiteTopic#subscribe_mib_per_sec}
        '''
        result = self._values.get("subscribe_mib_per_sec")
        assert result is not None, "Required property 'subscribe_mib_per_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubLiteTopicPartitionConfigCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubLiteTopicPartitionConfigCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicPartitionConfigCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d7d764505168784e77224312266ed45fc73475ea90a5f94b2841cc96619e625)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="publishMibPerSecInput")
    def publish_mib_per_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "publishMibPerSecInput"))

    @builtins.property
    @jsii.member(jsii_name="subscribeMibPerSecInput")
    def subscribe_mib_per_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "subscribeMibPerSecInput"))

    @builtins.property
    @jsii.member(jsii_name="publishMibPerSec")
    def publish_mib_per_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "publishMibPerSec"))

    @publish_mib_per_sec.setter
    def publish_mib_per_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dcc252325c769d4843907ef014a6e2278cd46c76e22adc6ada4428cf4f81b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishMibPerSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscribeMibPerSec")
    def subscribe_mib_per_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subscribeMibPerSec"))

    @subscribe_mib_per_sec.setter
    def subscribe_mib_per_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38db9b6f06bf6747cf5d4d4e3a4dd526457b611f56b9b37770d484105c52cd73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribeMibPerSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubLiteTopicPartitionConfigCapacity]:
        return typing.cast(typing.Optional[PubsubLiteTopicPartitionConfigCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubLiteTopicPartitionConfigCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d94d94895d160cf947fea6a196b26b086bff6836c4328323f07030073c88a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PubsubLiteTopicPartitionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicPartitionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51716d644a2ee897bc1a71f4e8ca2f0aeb4d6a95fac25da4a82a32af992d5a31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCapacity")
    def put_capacity(
        self,
        *,
        publish_mib_per_sec: jsii.Number,
        subscribe_mib_per_sec: jsii.Number,
    ) -> None:
        '''
        :param publish_mib_per_sec: Subscribe throughput capacity per partition in MiB/s. Must be >= 4 and <= 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#publish_mib_per_sec PubsubLiteTopic#publish_mib_per_sec}
        :param subscribe_mib_per_sec: Publish throughput capacity per partition in MiB/s. Must be >= 4 and <= 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#subscribe_mib_per_sec PubsubLiteTopic#subscribe_mib_per_sec}
        '''
        value = PubsubLiteTopicPartitionConfigCapacity(
            publish_mib_per_sec=publish_mib_per_sec,
            subscribe_mib_per_sec=subscribe_mib_per_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putCapacity", [value]))

    @jsii.member(jsii_name="resetCapacity")
    def reset_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> PubsubLiteTopicPartitionConfigCapacityOutputReference:
        return typing.cast(PubsubLiteTopicPartitionConfigCapacityOutputReference, jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[PubsubLiteTopicPartitionConfigCapacity]:
        return typing.cast(typing.Optional[PubsubLiteTopicPartitionConfigCapacity], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148ad73f6be71114333ff97e86a6417a39341b7c5b62e4bfd0d7d85cc36d321a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubLiteTopicPartitionConfig]:
        return typing.cast(typing.Optional[PubsubLiteTopicPartitionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubLiteTopicPartitionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4465540ef68fef260f4f870ca7ae69be3b2b6ebea03ef273be7916e40ed42d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicReservationConfig",
    jsii_struct_bases=[],
    name_mapping={"throughput_reservation": "throughputReservation"},
)
class PubsubLiteTopicReservationConfig:
    def __init__(
        self,
        *,
        throughput_reservation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param throughput_reservation: The Reservation to use for this topic's throughput capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#throughput_reservation PubsubLiteTopic#throughput_reservation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e2269733830031d2a2a9ba4dfaf0d34e7ba534f42917483479c8348dc47f38)
            check_type(argname="argument throughput_reservation", value=throughput_reservation, expected_type=type_hints["throughput_reservation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if throughput_reservation is not None:
            self._values["throughput_reservation"] = throughput_reservation

    @builtins.property
    def throughput_reservation(self) -> typing.Optional[builtins.str]:
        '''The Reservation to use for this topic's throughput capacity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#throughput_reservation PubsubLiteTopic#throughput_reservation}
        '''
        result = self._values.get("throughput_reservation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubLiteTopicReservationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubLiteTopicReservationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicReservationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__544e862448f60d4ca2aefe7d1d3248246f299742a9b7088a8f808b039c52c429)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetThroughputReservation")
    def reset_throughput_reservation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughputReservation", []))

    @builtins.property
    @jsii.member(jsii_name="throughputReservationInput")
    def throughput_reservation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "throughputReservationInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputReservation")
    def throughput_reservation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "throughputReservation"))

    @throughput_reservation.setter
    def throughput_reservation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22805097fbd5bd3ea002fba7928d6be9c46a17a717b74b5dd7b6c99f8d9e9cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputReservation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubLiteTopicReservationConfig]:
        return typing.cast(typing.Optional[PubsubLiteTopicReservationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubLiteTopicReservationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4ff787c7fb9c37363d690171024e8969394bfe2d160ad88edbfea40cfc6c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicRetentionConfig",
    jsii_struct_bases=[],
    name_mapping={"per_partition_bytes": "perPartitionBytes", "period": "period"},
)
class PubsubLiteTopicRetentionConfig:
    def __init__(
        self,
        *,
        per_partition_bytes: builtins.str,
        period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param per_partition_bytes: The provisioned storage, in bytes, per partition. If the number of bytes stored in any of the topic's partitions grows beyond this value, older messages will be dropped to make room for newer ones, regardless of the value of period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#per_partition_bytes PubsubLiteTopic#per_partition_bytes}
        :param period: How long a published message is retained. If unset, messages will be retained as long as the bytes retained for each partition is below perPartitionBytes. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#period PubsubLiteTopic#period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b674e9a86605abe331373510569e4df6eb41d1420610ed151296f8290f6df8cc)
            check_type(argname="argument per_partition_bytes", value=per_partition_bytes, expected_type=type_hints["per_partition_bytes"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "per_partition_bytes": per_partition_bytes,
        }
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def per_partition_bytes(self) -> builtins.str:
        '''The provisioned storage, in bytes, per partition.

        If the number of bytes stored
        in any of the topic's partitions grows beyond this value, older messages will be
        dropped to make room for newer ones, regardless of the value of period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#per_partition_bytes PubsubLiteTopic#per_partition_bytes}
        '''
        result = self._values.get("per_partition_bytes")
        assert result is not None, "Required property 'per_partition_bytes' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> typing.Optional[builtins.str]:
        '''How long a published message is retained.

        If unset, messages will be retained as
        long as the bytes retained for each partition is below perPartitionBytes. A
        duration in seconds with up to nine fractional digits, terminated by 's'.
        Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#period PubsubLiteTopic#period}
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubLiteTopicRetentionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubLiteTopicRetentionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicRetentionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3467982ebe15d6b870ed26e3f8891d38a36a27cff1d0ce3319db2a871a8f3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPeriod")
    def reset_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="perPartitionBytesInput")
    def per_partition_bytes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perPartitionBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f86f3c22ff148c19578b18139562e268ae1702e4d954f751fb9b6bb11d78337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perPartitionBytes")
    def per_partition_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perPartitionBytes"))

    @per_partition_bytes.setter
    def per_partition_bytes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2218be806b2441e26781e82d905693f665c04870bc79b26507696a70b5137752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perPartitionBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PubsubLiteTopicRetentionConfig]:
        return typing.cast(typing.Optional[PubsubLiteTopicRetentionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PubsubLiteTopicRetentionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a6ca0e396c994f3b6f6d7a1273b4478cabbc72f9460e487a7a0e13793e371f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PubsubLiteTopicTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#create PubsubLiteTopic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#delete PubsubLiteTopic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#update PubsubLiteTopic#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be600a6125c8ee5af3cf2f1cc8e03a23b37ae99862ce83f10c3e9e9c81a97cdd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#create PubsubLiteTopic#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#delete PubsubLiteTopic#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/pubsub_lite_topic#update PubsubLiteTopic#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PubsubLiteTopicTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PubsubLiteTopicTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.pubsubLiteTopic.PubsubLiteTopicTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__964c3f3d324077531a559fcecf9dc7dad3a5bc06b56d7dc9ccc5fa24d0736151)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4f8fea1747198ac75c1f53fcc41f464db4107a7df2f2e3e3ecdbfa15ce33618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e5c54e832982ec8e632bc93db3551fba8c74e33ce88b97801ca54cdcfc30d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692e5871d5f64797c519527b0f5a71d6644e7cd407ea619e57d79a35d57be883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubLiteTopicTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubLiteTopicTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubLiteTopicTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e512f36ff8bd8040a22bff5a7b8448a4572ab6fa81b2a87c83cc31322581529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PubsubLiteTopic",
    "PubsubLiteTopicConfig",
    "PubsubLiteTopicPartitionConfig",
    "PubsubLiteTopicPartitionConfigCapacity",
    "PubsubLiteTopicPartitionConfigCapacityOutputReference",
    "PubsubLiteTopicPartitionConfigOutputReference",
    "PubsubLiteTopicReservationConfig",
    "PubsubLiteTopicReservationConfigOutputReference",
    "PubsubLiteTopicRetentionConfig",
    "PubsubLiteTopicRetentionConfigOutputReference",
    "PubsubLiteTopicTimeouts",
    "PubsubLiteTopicTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bf67273eef62c203aa17d30a476bd41d91389291dafcc1ecf657ef0f30e4c912(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    partition_config: typing.Optional[typing.Union[PubsubLiteTopicPartitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reservation_config: typing.Optional[typing.Union[PubsubLiteTopicReservationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_config: typing.Optional[typing.Union[PubsubLiteTopicRetentionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PubsubLiteTopicTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__2c90fa8eed90e734db115856f3dd604c640a31959995e7be4ddd6386e41e4363(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8929e4c9ed025ac62404a5ef1ff8a6a9311d0017c68c51a338f7c51a9e853e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f2f3207030a2dc8c8c9df46d844ac6a4704e90e619538a22dcbeb41774fde6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664d2ef4f9f71cfd4140a3afe9ee9b8f849f3b62259cc847feca4a28a631f474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc82138bb45e3d2688a58aa43a5dc8ee05dad589c9d38ab4eceb92de2fb37f8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3d353851d9490075232ffd831125781dd0c105b357b14e32625a2c1c99b341(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1b02a5e3da01e2b98a8ba1365d952b90c09cf342b25ed0f01dc4d81fbbffb5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    partition_config: typing.Optional[typing.Union[PubsubLiteTopicPartitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reservation_config: typing.Optional[typing.Union[PubsubLiteTopicReservationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_config: typing.Optional[typing.Union[PubsubLiteTopicRetentionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PubsubLiteTopicTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072a6d9da1433314fe64f67879850976c9d12e5ff564b929050bb4b839116269(
    *,
    count: jsii.Number,
    capacity: typing.Optional[typing.Union[PubsubLiteTopicPartitionConfigCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42942f9fd993d5297e631b4af728f72d1ef860d435e847cc740aaede8e2ae202(
    *,
    publish_mib_per_sec: jsii.Number,
    subscribe_mib_per_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7d764505168784e77224312266ed45fc73475ea90a5f94b2841cc96619e625(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcc252325c769d4843907ef014a6e2278cd46c76e22adc6ada4428cf4f81b5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38db9b6f06bf6747cf5d4d4e3a4dd526457b611f56b9b37770d484105c52cd73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d94d94895d160cf947fea6a196b26b086bff6836c4328323f07030073c88a1a(
    value: typing.Optional[PubsubLiteTopicPartitionConfigCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51716d644a2ee897bc1a71f4e8ca2f0aeb4d6a95fac25da4a82a32af992d5a31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148ad73f6be71114333ff97e86a6417a39341b7c5b62e4bfd0d7d85cc36d321a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4465540ef68fef260f4f870ca7ae69be3b2b6ebea03ef273be7916e40ed42d4a(
    value: typing.Optional[PubsubLiteTopicPartitionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e2269733830031d2a2a9ba4dfaf0d34e7ba534f42917483479c8348dc47f38(
    *,
    throughput_reservation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544e862448f60d4ca2aefe7d1d3248246f299742a9b7088a8f808b039c52c429(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22805097fbd5bd3ea002fba7928d6be9c46a17a717b74b5dd7b6c99f8d9e9cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4ff787c7fb9c37363d690171024e8969394bfe2d160ad88edbfea40cfc6c7b(
    value: typing.Optional[PubsubLiteTopicReservationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b674e9a86605abe331373510569e4df6eb41d1420610ed151296f8290f6df8cc(
    *,
    per_partition_bytes: builtins.str,
    period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3467982ebe15d6b870ed26e3f8891d38a36a27cff1d0ce3319db2a871a8f3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f86f3c22ff148c19578b18139562e268ae1702e4d954f751fb9b6bb11d78337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2218be806b2441e26781e82d905693f665c04870bc79b26507696a70b5137752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a6ca0e396c994f3b6f6d7a1273b4478cabbc72f9460e487a7a0e13793e371f(
    value: typing.Optional[PubsubLiteTopicRetentionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be600a6125c8ee5af3cf2f1cc8e03a23b37ae99862ce83f10c3e9e9c81a97cdd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964c3f3d324077531a559fcecf9dc7dad3a5bc06b56d7dc9ccc5fa24d0736151(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f8fea1747198ac75c1f53fcc41f464db4107a7df2f2e3e3ecdbfa15ce33618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e5c54e832982ec8e632bc93db3551fba8c74e33ce88b97801ca54cdcfc30d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692e5871d5f64797c519527b0f5a71d6644e7cd407ea619e57d79a35d57be883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e512f36ff8bd8040a22bff5a7b8448a4572ab6fa81b2a87c83cc31322581529(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PubsubLiteTopicTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
