r'''
# `google_pubsub_lite_topic`

Refer to the Terraform Registry for docs: [`google_pubsub_lite_topic`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic).
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


class GooglePubsubLiteTopic(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopic",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic google_pubsub_lite_topic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        partition_config: typing.Optional[typing.Union["GooglePubsubLiteTopicPartitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reservation_config: typing.Optional[typing.Union["GooglePubsubLiteTopicReservationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_config: typing.Optional[typing.Union["GooglePubsubLiteTopicRetentionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GooglePubsubLiteTopicTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic google_pubsub_lite_topic} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#name GooglePubsubLiteTopic#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#id GooglePubsubLiteTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param partition_config: partition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#partition_config GooglePubsubLiteTopic#partition_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#project GooglePubsubLiteTopic#project}.
        :param region: The region of the pubsub lite topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#region GooglePubsubLiteTopic#region}
        :param reservation_config: reservation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#reservation_config GooglePubsubLiteTopic#reservation_config}
        :param retention_config: retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#retention_config GooglePubsubLiteTopic#retention_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#timeouts GooglePubsubLiteTopic#timeouts}
        :param zone: The zone of the pubsub lite topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#zone GooglePubsubLiteTopic#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80da6b290525f3e02cdbce693981c844fb5b539b014c9ce1b59f4124bdff6b96)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GooglePubsubLiteTopicConfig(
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
        '''Generates CDKTF code for importing a GooglePubsubLiteTopic resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GooglePubsubLiteTopic to import.
        :param import_from_id: The id of the existing GooglePubsubLiteTopic that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GooglePubsubLiteTopic to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b50a1b336664a877f962ed6563a40d70e59d625f6cc41bc59b02d00086213e)
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
        capacity: typing.Optional[typing.Union["GooglePubsubLiteTopicPartitionConfigCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: The number of partitions in the topic. Must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#count GooglePubsubLiteTopic#count}
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#capacity GooglePubsubLiteTopic#capacity}
        '''
        value = GooglePubsubLiteTopicPartitionConfig(count=count, capacity=capacity)

        return typing.cast(None, jsii.invoke(self, "putPartitionConfig", [value]))

    @jsii.member(jsii_name="putReservationConfig")
    def put_reservation_config(
        self,
        *,
        throughput_reservation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param throughput_reservation: The Reservation to use for this topic's throughput capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#throughput_reservation GooglePubsubLiteTopic#throughput_reservation}
        '''
        value = GooglePubsubLiteTopicReservationConfig(
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
        :param per_partition_bytes: The provisioned storage, in bytes, per partition. If the number of bytes stored in any of the topic's partitions grows beyond this value, older messages will be dropped to make room for newer ones, regardless of the value of period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#per_partition_bytes GooglePubsubLiteTopic#per_partition_bytes}
        :param period: How long a published message is retained. If unset, messages will be retained as long as the bytes retained for each partition is below perPartitionBytes. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#period GooglePubsubLiteTopic#period}
        '''
        value = GooglePubsubLiteTopicRetentionConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#create GooglePubsubLiteTopic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#delete GooglePubsubLiteTopic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#update GooglePubsubLiteTopic#update}.
        '''
        value = GooglePubsubLiteTopicTimeouts(
            create=create, delete=delete, update=update
        )

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
    def partition_config(self) -> "GooglePubsubLiteTopicPartitionConfigOutputReference":
        return typing.cast("GooglePubsubLiteTopicPartitionConfigOutputReference", jsii.get(self, "partitionConfig"))

    @builtins.property
    @jsii.member(jsii_name="reservationConfig")
    def reservation_config(
        self,
    ) -> "GooglePubsubLiteTopicReservationConfigOutputReference":
        return typing.cast("GooglePubsubLiteTopicReservationConfigOutputReference", jsii.get(self, "reservationConfig"))

    @builtins.property
    @jsii.member(jsii_name="retentionConfig")
    def retention_config(self) -> "GooglePubsubLiteTopicRetentionConfigOutputReference":
        return typing.cast("GooglePubsubLiteTopicRetentionConfigOutputReference", jsii.get(self, "retentionConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GooglePubsubLiteTopicTimeoutsOutputReference":
        return typing.cast("GooglePubsubLiteTopicTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GooglePubsubLiteTopicPartitionConfig"]:
        return typing.cast(typing.Optional["GooglePubsubLiteTopicPartitionConfig"], jsii.get(self, "partitionConfigInput"))

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
    ) -> typing.Optional["GooglePubsubLiteTopicReservationConfig"]:
        return typing.cast(typing.Optional["GooglePubsubLiteTopicReservationConfig"], jsii.get(self, "reservationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionConfigInput")
    def retention_config_input(
        self,
    ) -> typing.Optional["GooglePubsubLiteTopicRetentionConfig"]:
        return typing.cast(typing.Optional["GooglePubsubLiteTopicRetentionConfig"], jsii.get(self, "retentionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePubsubLiteTopicTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GooglePubsubLiteTopicTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a941d2bc331d1281e36fb69973f1ac3aa16de990a0104239870d26d11a084e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d4b11d299176f102dd3fbe37e24b519537ce34a5229b8fcee69541bad2812c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bea1b6688dae9515aa8b2124e026eec30480677d520151e7f1eaf030fa055dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4847746a61c50d70096b79484dfea5237a225515b2fe6777d41369b94e321d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9377a943bf8d5ee234abdd145291a9eace96da412ec4b51c334202a737c9209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicConfig",
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
class GooglePubsubLiteTopicConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        partition_config: typing.Optional[typing.Union["GooglePubsubLiteTopicPartitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reservation_config: typing.Optional[typing.Union["GooglePubsubLiteTopicReservationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        retention_config: typing.Optional[typing.Union["GooglePubsubLiteTopicRetentionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GooglePubsubLiteTopicTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Name of the topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#name GooglePubsubLiteTopic#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#id GooglePubsubLiteTopic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param partition_config: partition_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#partition_config GooglePubsubLiteTopic#partition_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#project GooglePubsubLiteTopic#project}.
        :param region: The region of the pubsub lite topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#region GooglePubsubLiteTopic#region}
        :param reservation_config: reservation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#reservation_config GooglePubsubLiteTopic#reservation_config}
        :param retention_config: retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#retention_config GooglePubsubLiteTopic#retention_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#timeouts GooglePubsubLiteTopic#timeouts}
        :param zone: The zone of the pubsub lite topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#zone GooglePubsubLiteTopic#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(partition_config, dict):
            partition_config = GooglePubsubLiteTopicPartitionConfig(**partition_config)
        if isinstance(reservation_config, dict):
            reservation_config = GooglePubsubLiteTopicReservationConfig(**reservation_config)
        if isinstance(retention_config, dict):
            retention_config = GooglePubsubLiteTopicRetentionConfig(**retention_config)
        if isinstance(timeouts, dict):
            timeouts = GooglePubsubLiteTopicTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6b4ac1f865566c3de8a2b6513ed1406c564eec94142e4a8547580b5f20f527)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#name GooglePubsubLiteTopic#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#id GooglePubsubLiteTopic#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_config(
        self,
    ) -> typing.Optional["GooglePubsubLiteTopicPartitionConfig"]:
        '''partition_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#partition_config GooglePubsubLiteTopic#partition_config}
        '''
        result = self._values.get("partition_config")
        return typing.cast(typing.Optional["GooglePubsubLiteTopicPartitionConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#project GooglePubsubLiteTopic#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the pubsub lite topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#region GooglePubsubLiteTopic#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_config(
        self,
    ) -> typing.Optional["GooglePubsubLiteTopicReservationConfig"]:
        '''reservation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#reservation_config GooglePubsubLiteTopic#reservation_config}
        '''
        result = self._values.get("reservation_config")
        return typing.cast(typing.Optional["GooglePubsubLiteTopicReservationConfig"], result)

    @builtins.property
    def retention_config(
        self,
    ) -> typing.Optional["GooglePubsubLiteTopicRetentionConfig"]:
        '''retention_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#retention_config GooglePubsubLiteTopic#retention_config}
        '''
        result = self._values.get("retention_config")
        return typing.cast(typing.Optional["GooglePubsubLiteTopicRetentionConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GooglePubsubLiteTopicTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#timeouts GooglePubsubLiteTopic#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GooglePubsubLiteTopicTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The zone of the pubsub lite topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#zone GooglePubsubLiteTopic#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubLiteTopicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicPartitionConfig",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "capacity": "capacity"},
)
class GooglePubsubLiteTopicPartitionConfig:
    def __init__(
        self,
        *,
        count: jsii.Number,
        capacity: typing.Optional[typing.Union["GooglePubsubLiteTopicPartitionConfigCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: The number of partitions in the topic. Must be at least 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#count GooglePubsubLiteTopic#count}
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#capacity GooglePubsubLiteTopic#capacity}
        '''
        if isinstance(capacity, dict):
            capacity = GooglePubsubLiteTopicPartitionConfigCapacity(**capacity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266870b6fa9a22ecd740d0ff68b0aa5a0727551775b6d6cc9927955189f3e426)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#count GooglePubsubLiteTopic#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def capacity(
        self,
    ) -> typing.Optional["GooglePubsubLiteTopicPartitionConfigCapacity"]:
        '''capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#capacity GooglePubsubLiteTopic#capacity}
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional["GooglePubsubLiteTopicPartitionConfigCapacity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubLiteTopicPartitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicPartitionConfigCapacity",
    jsii_struct_bases=[],
    name_mapping={
        "publish_mib_per_sec": "publishMibPerSec",
        "subscribe_mib_per_sec": "subscribeMibPerSec",
    },
)
class GooglePubsubLiteTopicPartitionConfigCapacity:
    def __init__(
        self,
        *,
        publish_mib_per_sec: jsii.Number,
        subscribe_mib_per_sec: jsii.Number,
    ) -> None:
        '''
        :param publish_mib_per_sec: Subscribe throughput capacity per partition in MiB/s. Must be >= 4 and <= 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#publish_mib_per_sec GooglePubsubLiteTopic#publish_mib_per_sec}
        :param subscribe_mib_per_sec: Publish throughput capacity per partition in MiB/s. Must be >= 4 and <= 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#subscribe_mib_per_sec GooglePubsubLiteTopic#subscribe_mib_per_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18638096eb2d202cb831ea1b0144e8941e38c73347783386843c068489da4bf2)
            check_type(argname="argument publish_mib_per_sec", value=publish_mib_per_sec, expected_type=type_hints["publish_mib_per_sec"])
            check_type(argname="argument subscribe_mib_per_sec", value=subscribe_mib_per_sec, expected_type=type_hints["subscribe_mib_per_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "publish_mib_per_sec": publish_mib_per_sec,
            "subscribe_mib_per_sec": subscribe_mib_per_sec,
        }

    @builtins.property
    def publish_mib_per_sec(self) -> jsii.Number:
        '''Subscribe throughput capacity per partition in MiB/s. Must be >= 4 and <= 16.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#publish_mib_per_sec GooglePubsubLiteTopic#publish_mib_per_sec}
        '''
        result = self._values.get("publish_mib_per_sec")
        assert result is not None, "Required property 'publish_mib_per_sec' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subscribe_mib_per_sec(self) -> jsii.Number:
        '''Publish throughput capacity per partition in MiB/s. Must be >= 4 and <= 16.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#subscribe_mib_per_sec GooglePubsubLiteTopic#subscribe_mib_per_sec}
        '''
        result = self._values.get("subscribe_mib_per_sec")
        assert result is not None, "Required property 'subscribe_mib_per_sec' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubLiteTopicPartitionConfigCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubLiteTopicPartitionConfigCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicPartitionConfigCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4da56110425252d24e534ac15864e2c9f73c2a902457e608dbd6ec44e0fe38bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0df8b33e6002a4564e6e0803ab89ba00706582605537215559e973be38a7ef3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishMibPerSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscribeMibPerSec")
    def subscribe_mib_per_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subscribeMibPerSec"))

    @subscribe_mib_per_sec.setter
    def subscribe_mib_per_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1c0ea92862f42deb3887d7aec8fcc0ea42af72224a0d7867d95e86fcab2928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribeMibPerSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GooglePubsubLiteTopicPartitionConfigCapacity]:
        return typing.cast(typing.Optional[GooglePubsubLiteTopicPartitionConfigCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubLiteTopicPartitionConfigCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef27ae5f5467dcb8aed9fe6e8a6a4864af60c0efc51c7cd47ec1c1bdeedb1285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GooglePubsubLiteTopicPartitionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicPartitionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a75f188b2528fd93124b5ceb28a3224f24470e7303c808a4f9905fb129215fe7)
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
        :param publish_mib_per_sec: Subscribe throughput capacity per partition in MiB/s. Must be >= 4 and <= 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#publish_mib_per_sec GooglePubsubLiteTopic#publish_mib_per_sec}
        :param subscribe_mib_per_sec: Publish throughput capacity per partition in MiB/s. Must be >= 4 and <= 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#subscribe_mib_per_sec GooglePubsubLiteTopic#subscribe_mib_per_sec}
        '''
        value = GooglePubsubLiteTopicPartitionConfigCapacity(
            publish_mib_per_sec=publish_mib_per_sec,
            subscribe_mib_per_sec=subscribe_mib_per_sec,
        )

        return typing.cast(None, jsii.invoke(self, "putCapacity", [value]))

    @jsii.member(jsii_name="resetCapacity")
    def reset_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacity", []))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> GooglePubsubLiteTopicPartitionConfigCapacityOutputReference:
        return typing.cast(GooglePubsubLiteTopicPartitionConfigCapacityOutputReference, jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(
        self,
    ) -> typing.Optional[GooglePubsubLiteTopicPartitionConfigCapacity]:
        return typing.cast(typing.Optional[GooglePubsubLiteTopicPartitionConfigCapacity], jsii.get(self, "capacityInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b8a636a841aaff68b9ad0f65efdeb830950587e037cefe3dda7f34aac28cd53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePubsubLiteTopicPartitionConfig]:
        return typing.cast(typing.Optional[GooglePubsubLiteTopicPartitionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubLiteTopicPartitionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0cbb19b7a9e065103b79af582e91ecdf0d707006f0ec9f7032111b74271155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicReservationConfig",
    jsii_struct_bases=[],
    name_mapping={"throughput_reservation": "throughputReservation"},
)
class GooglePubsubLiteTopicReservationConfig:
    def __init__(
        self,
        *,
        throughput_reservation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param throughput_reservation: The Reservation to use for this topic's throughput capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#throughput_reservation GooglePubsubLiteTopic#throughput_reservation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04311c1f4d2959ba60659f9e3cdbeb44e4d8bdad85a7604d248381276aa8bd6)
            check_type(argname="argument throughput_reservation", value=throughput_reservation, expected_type=type_hints["throughput_reservation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if throughput_reservation is not None:
            self._values["throughput_reservation"] = throughput_reservation

    @builtins.property
    def throughput_reservation(self) -> typing.Optional[builtins.str]:
        '''The Reservation to use for this topic's throughput capacity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#throughput_reservation GooglePubsubLiteTopic#throughput_reservation}
        '''
        result = self._values.get("throughput_reservation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubLiteTopicReservationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubLiteTopicReservationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicReservationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b0dae3c13e9911c64e6d3202a7cbdc98bcaa919930a1524ad58382ec7a78184)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bac2feb341897da9cb05f128ab59a3f44452ce7c1e359b37b32ac21773ae24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputReservation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePubsubLiteTopicReservationConfig]:
        return typing.cast(typing.Optional[GooglePubsubLiteTopicReservationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubLiteTopicReservationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5037860d5ea59597335977e096a615d23bc34782119bc80c8cdd1e2b057f8992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicRetentionConfig",
    jsii_struct_bases=[],
    name_mapping={"per_partition_bytes": "perPartitionBytes", "period": "period"},
)
class GooglePubsubLiteTopicRetentionConfig:
    def __init__(
        self,
        *,
        per_partition_bytes: builtins.str,
        period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param per_partition_bytes: The provisioned storage, in bytes, per partition. If the number of bytes stored in any of the topic's partitions grows beyond this value, older messages will be dropped to make room for newer ones, regardless of the value of period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#per_partition_bytes GooglePubsubLiteTopic#per_partition_bytes}
        :param period: How long a published message is retained. If unset, messages will be retained as long as the bytes retained for each partition is below perPartitionBytes. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#period GooglePubsubLiteTopic#period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f025e712e2fd510bb59b0db04cf669084646321aed9930e812712ab68780003a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#per_partition_bytes GooglePubsubLiteTopic#per_partition_bytes}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#period GooglePubsubLiteTopic#period}
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubLiteTopicRetentionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubLiteTopicRetentionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicRetentionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0e6eeee7237ffc5ba6945dbb4179e7a0eada59858b1cdd19722b9f713455643)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4f3452cf5168cc70c0f798d538797235cf33ca150b432a7304758c5abc36a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perPartitionBytes")
    def per_partition_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perPartitionBytes"))

    @per_partition_bytes.setter
    def per_partition_bytes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9567cb93dc913b2dacecafd384941431f1449fa50180a8ac7244f984e7fc9be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perPartitionBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GooglePubsubLiteTopicRetentionConfig]:
        return typing.cast(typing.Optional[GooglePubsubLiteTopicRetentionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GooglePubsubLiteTopicRetentionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9973def241463639139533af4f39ff0f2c8b80608b048c78cab33991361faa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GooglePubsubLiteTopicTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#create GooglePubsubLiteTopic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#delete GooglePubsubLiteTopic#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#update GooglePubsubLiteTopic#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d88ef640d97b1110efc89c48bb3a3baa473903afa21f31698beb98b2686b86)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#create GooglePubsubLiteTopic#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#delete GooglePubsubLiteTopic#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_pubsub_lite_topic#update GooglePubsubLiteTopic#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GooglePubsubLiteTopicTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GooglePubsubLiteTopicTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googlePubsubLiteTopic.GooglePubsubLiteTopicTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9981ac4d0cf3b2f1111706a3a846341bb9552cc862144ff93a10f2d4f317441)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d7948093c2daea6cf650afe2287f867ec77397c1d343b67a2b81b9bcbe7249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2abd667f83012374bf876c034635d3861b791c02411ff6742f4aa0dd4c716116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0312377f1b69a101019b04ffd484c876b823268e6f15c021dd8d9a0633045248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubLiteTopicTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubLiteTopicTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubLiteTopicTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca5a936b80c473a34008db34468fa13373fb7b9f24a8044a46c4e6eb0d8cfd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GooglePubsubLiteTopic",
    "GooglePubsubLiteTopicConfig",
    "GooglePubsubLiteTopicPartitionConfig",
    "GooglePubsubLiteTopicPartitionConfigCapacity",
    "GooglePubsubLiteTopicPartitionConfigCapacityOutputReference",
    "GooglePubsubLiteTopicPartitionConfigOutputReference",
    "GooglePubsubLiteTopicReservationConfig",
    "GooglePubsubLiteTopicReservationConfigOutputReference",
    "GooglePubsubLiteTopicRetentionConfig",
    "GooglePubsubLiteTopicRetentionConfigOutputReference",
    "GooglePubsubLiteTopicTimeouts",
    "GooglePubsubLiteTopicTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__80da6b290525f3e02cdbce693981c844fb5b539b014c9ce1b59f4124bdff6b96(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    partition_config: typing.Optional[typing.Union[GooglePubsubLiteTopicPartitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reservation_config: typing.Optional[typing.Union[GooglePubsubLiteTopicReservationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_config: typing.Optional[typing.Union[GooglePubsubLiteTopicRetentionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GooglePubsubLiteTopicTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f9b50a1b336664a877f962ed6563a40d70e59d625f6cc41bc59b02d00086213e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a941d2bc331d1281e36fb69973f1ac3aa16de990a0104239870d26d11a084e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d4b11d299176f102dd3fbe37e24b519537ce34a5229b8fcee69541bad2812c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bea1b6688dae9515aa8b2124e026eec30480677d520151e7f1eaf030fa055dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4847746a61c50d70096b79484dfea5237a225515b2fe6777d41369b94e321d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9377a943bf8d5ee234abdd145291a9eace96da412ec4b51c334202a737c9209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6b4ac1f865566c3de8a2b6513ed1406c564eec94142e4a8547580b5f20f527(
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
    partition_config: typing.Optional[typing.Union[GooglePubsubLiteTopicPartitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reservation_config: typing.Optional[typing.Union[GooglePubsubLiteTopicReservationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_config: typing.Optional[typing.Union[GooglePubsubLiteTopicRetentionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GooglePubsubLiteTopicTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266870b6fa9a22ecd740d0ff68b0aa5a0727551775b6d6cc9927955189f3e426(
    *,
    count: jsii.Number,
    capacity: typing.Optional[typing.Union[GooglePubsubLiteTopicPartitionConfigCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18638096eb2d202cb831ea1b0144e8941e38c73347783386843c068489da4bf2(
    *,
    publish_mib_per_sec: jsii.Number,
    subscribe_mib_per_sec: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da56110425252d24e534ac15864e2c9f73c2a902457e608dbd6ec44e0fe38bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df8b33e6002a4564e6e0803ab89ba00706582605537215559e973be38a7ef3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1c0ea92862f42deb3887d7aec8fcc0ea42af72224a0d7867d95e86fcab2928(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef27ae5f5467dcb8aed9fe6e8a6a4864af60c0efc51c7cd47ec1c1bdeedb1285(
    value: typing.Optional[GooglePubsubLiteTopicPartitionConfigCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75f188b2528fd93124b5ceb28a3224f24470e7303c808a4f9905fb129215fe7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a636a841aaff68b9ad0f65efdeb830950587e037cefe3dda7f34aac28cd53e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0cbb19b7a9e065103b79af582e91ecdf0d707006f0ec9f7032111b74271155(
    value: typing.Optional[GooglePubsubLiteTopicPartitionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04311c1f4d2959ba60659f9e3cdbeb44e4d8bdad85a7604d248381276aa8bd6(
    *,
    throughput_reservation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0dae3c13e9911c64e6d3202a7cbdc98bcaa919930a1524ad58382ec7a78184(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bac2feb341897da9cb05f128ab59a3f44452ce7c1e359b37b32ac21773ae24f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5037860d5ea59597335977e096a615d23bc34782119bc80c8cdd1e2b057f8992(
    value: typing.Optional[GooglePubsubLiteTopicReservationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f025e712e2fd510bb59b0db04cf669084646321aed9930e812712ab68780003a(
    *,
    per_partition_bytes: builtins.str,
    period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e6eeee7237ffc5ba6945dbb4179e7a0eada59858b1cdd19722b9f713455643(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4f3452cf5168cc70c0f798d538797235cf33ca150b432a7304758c5abc36a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9567cb93dc913b2dacecafd384941431f1449fa50180a8ac7244f984e7fc9be0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9973def241463639139533af4f39ff0f2c8b80608b048c78cab33991361faa8(
    value: typing.Optional[GooglePubsubLiteTopicRetentionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d88ef640d97b1110efc89c48bb3a3baa473903afa21f31698beb98b2686b86(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9981ac4d0cf3b2f1111706a3a846341bb9552cc862144ff93a10f2d4f317441(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d7948093c2daea6cf650afe2287f867ec77397c1d343b67a2b81b9bcbe7249(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abd667f83012374bf876c034635d3861b791c02411ff6742f4aa0dd4c716116(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0312377f1b69a101019b04ffd484c876b823268e6f15c021dd8d9a0633045248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca5a936b80c473a34008db34468fa13373fb7b9f24a8044a46c4e6eb0d8cfd2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GooglePubsubLiteTopicTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
