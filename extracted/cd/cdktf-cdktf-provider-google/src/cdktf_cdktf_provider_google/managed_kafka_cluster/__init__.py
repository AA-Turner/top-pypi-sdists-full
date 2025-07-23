r'''
# `google_managed_kafka_cluster`

Refer to the Terraform Registry for docs: [`google_managed_kafka_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster).
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


class ManagedKafkaCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster google_managed_kafka_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        capacity_config: typing.Union["ManagedKafkaClusterCapacityConfig", typing.Dict[builtins.str, typing.Any]],
        cluster_id: builtins.str,
        gcp_config: typing.Union["ManagedKafkaClusterGcpConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        rebalance_config: typing.Optional[typing.Union["ManagedKafkaClusterRebalanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ManagedKafkaClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster google_managed_kafka_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity_config: capacity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#capacity_config ManagedKafkaCluster#capacity_config}
        :param cluster_id: The ID to use for the cluster, which will become the final component of the cluster's name. The ID must be 1-63 characters long, and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' to comply with RFC 1035. This value is structured like: 'my-cluster-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#cluster_id ManagedKafkaCluster#cluster_id}
        :param gcp_config: gcp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#gcp_config ManagedKafkaCluster#gcp_config}
        :param location: ID of the location of the Kafka resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#location ManagedKafkaCluster#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#id ManagedKafkaCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: List of label KEY=VALUE pairs to add. Keys must start with a lowercase character and contain only hyphens (-), underscores ( ), lowercase characters, and numbers. Values must contain only hyphens (-), underscores ( ), lowercase characters, and numbers. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#labels ManagedKafkaCluster#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#project ManagedKafkaCluster#project}.
        :param rebalance_config: rebalance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#rebalance_config ManagedKafkaCluster#rebalance_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#timeouts ManagedKafkaCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b287f92d9d9d037f892b656b79c6aeb590277e050d79e1a21ef0e09e9f86c69)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ManagedKafkaClusterConfig(
            capacity_config=capacity_config,
            cluster_id=cluster_id,
            gcp_config=gcp_config,
            location=location,
            id=id,
            labels=labels,
            project=project,
            rebalance_config=rebalance_config,
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
        '''Generates CDKTF code for importing a ManagedKafkaCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ManagedKafkaCluster to import.
        :param import_from_id: The id of the existing ManagedKafkaCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ManagedKafkaCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62179bee48f279b4e0712f5db4ff3098e64e5d0f62333453abfeb38c002a8575)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCapacityConfig")
    def put_capacity_config(
        self,
        *,
        memory_bytes: builtins.str,
        vcpu_count: builtins.str,
    ) -> None:
        '''
        :param memory_bytes: The memory to provision for the cluster in bytes. The value must be between 1 GiB and 8 GiB per vCPU. Ex. 1024Mi, 4Gi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#memory_bytes ManagedKafkaCluster#memory_bytes}
        :param vcpu_count: The number of vCPUs to provision for the cluster. The minimum is 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#vcpu_count ManagedKafkaCluster#vcpu_count}
        '''
        value = ManagedKafkaClusterCapacityConfig(
            memory_bytes=memory_bytes, vcpu_count=vcpu_count
        )

        return typing.cast(None, jsii.invoke(self, "putCapacityConfig", [value]))

    @jsii.member(jsii_name="putGcpConfig")
    def put_gcp_config(
        self,
        *,
        access_config: typing.Union["ManagedKafkaClusterGcpConfigAccessConfig", typing.Dict[builtins.str, typing.Any]],
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#access_config ManagedKafkaCluster#access_config}
        :param kms_key: The Cloud KMS Key name to use for encryption. The key must be located in the same region as the cluster and cannot be changed. Must be in the format 'projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#kms_key ManagedKafkaCluster#kms_key}
        '''
        value = ManagedKafkaClusterGcpConfig(
            access_config=access_config, kms_key=kms_key
        )

        return typing.cast(None, jsii.invoke(self, "putGcpConfig", [value]))

    @jsii.member(jsii_name="putRebalanceConfig")
    def put_rebalance_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: The rebalance behavior for the cluster. When not specified, defaults to 'NO_REBALANCE'. Possible values: 'MODE_UNSPECIFIED', 'NO_REBALANCE', 'AUTO_REBALANCE_ON_SCALE_UP'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#mode ManagedKafkaCluster#mode}
        '''
        value = ManagedKafkaClusterRebalanceConfig(mode=mode)

        return typing.cast(None, jsii.invoke(self, "putRebalanceConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#create ManagedKafkaCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#delete ManagedKafkaCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#update ManagedKafkaCluster#update}.
        '''
        value = ManagedKafkaClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRebalanceConfig")
    def reset_rebalance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRebalanceConfig", []))

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
    @jsii.member(jsii_name="capacityConfig")
    def capacity_config(self) -> "ManagedKafkaClusterCapacityConfigOutputReference":
        return typing.cast("ManagedKafkaClusterCapacityConfigOutputReference", jsii.get(self, "capacityConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="gcpConfig")
    def gcp_config(self) -> "ManagedKafkaClusterGcpConfigOutputReference":
        return typing.cast("ManagedKafkaClusterGcpConfigOutputReference", jsii.get(self, "gcpConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="rebalanceConfig")
    def rebalance_config(self) -> "ManagedKafkaClusterRebalanceConfigOutputReference":
        return typing.cast("ManagedKafkaClusterRebalanceConfigOutputReference", jsii.get(self, "rebalanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ManagedKafkaClusterTimeoutsOutputReference":
        return typing.cast("ManagedKafkaClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="capacityConfigInput")
    def capacity_config_input(
        self,
    ) -> typing.Optional["ManagedKafkaClusterCapacityConfig"]:
        return typing.cast(typing.Optional["ManagedKafkaClusterCapacityConfig"], jsii.get(self, "capacityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpConfigInput")
    def gcp_config_input(self) -> typing.Optional["ManagedKafkaClusterGcpConfig"]:
        return typing.cast(typing.Optional["ManagedKafkaClusterGcpConfig"], jsii.get(self, "gcpConfigInput"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rebalanceConfigInput")
    def rebalance_config_input(
        self,
    ) -> typing.Optional["ManagedKafkaClusterRebalanceConfig"]:
        return typing.cast(typing.Optional["ManagedKafkaClusterRebalanceConfig"], jsii.get(self, "rebalanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ManagedKafkaClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ManagedKafkaClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2538d5f6a220346722c42a696de833ef74732b72c6137ca368ab9ab90f97c716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc7e095a098190007198a1a1e0c1ca0a8e4958aceaad9af2bc118d597e022cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4403dae38a124e32dc82c569383f883b89e6ebc7224fb184599230a5c09a418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb80bd0b808fb1cb45e03aaf45cd7e33cbd0b365b4568dd15e6abe74e75e0f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f922721591c4013ecad1b59b60a919e4bd4f4d4a7177b7f233da94673ad133db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterCapacityConfig",
    jsii_struct_bases=[],
    name_mapping={"memory_bytes": "memoryBytes", "vcpu_count": "vcpuCount"},
)
class ManagedKafkaClusterCapacityConfig:
    def __init__(self, *, memory_bytes: builtins.str, vcpu_count: builtins.str) -> None:
        '''
        :param memory_bytes: The memory to provision for the cluster in bytes. The value must be between 1 GiB and 8 GiB per vCPU. Ex. 1024Mi, 4Gi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#memory_bytes ManagedKafkaCluster#memory_bytes}
        :param vcpu_count: The number of vCPUs to provision for the cluster. The minimum is 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#vcpu_count ManagedKafkaCluster#vcpu_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86133390f27f41c1bc02323db97b2c1d56a6052201758a7b6198a67ef03faad3)
            check_type(argname="argument memory_bytes", value=memory_bytes, expected_type=type_hints["memory_bytes"])
            check_type(argname="argument vcpu_count", value=vcpu_count, expected_type=type_hints["vcpu_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "memory_bytes": memory_bytes,
            "vcpu_count": vcpu_count,
        }

    @builtins.property
    def memory_bytes(self) -> builtins.str:
        '''The memory to provision for the cluster in bytes.

        The value must be between 1 GiB and 8 GiB per vCPU. Ex. 1024Mi, 4Gi.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#memory_bytes ManagedKafkaCluster#memory_bytes}
        '''
        result = self._values.get("memory_bytes")
        assert result is not None, "Required property 'memory_bytes' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vcpu_count(self) -> builtins.str:
        '''The number of vCPUs to provision for the cluster. The minimum is 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#vcpu_count ManagedKafkaCluster#vcpu_count}
        '''
        result = self._values.get("vcpu_count")
        assert result is not None, "Required property 'vcpu_count' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaClusterCapacityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedKafkaClusterCapacityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterCapacityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17a9b54889fea79166abb1048e21639df2a0a8c54d485f92800b6a406284577b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="memoryBytesInput")
    def memory_bytes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="vcpuCountInput")
    def vcpu_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vcpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryBytes")
    def memory_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memoryBytes"))

    @memory_bytes.setter
    def memory_bytes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787977a9fb2dd1bfb2a99b48027aae97d8a469526a3502a3c86e63eb00c47b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcpuCount")
    def vcpu_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcpuCount"))

    @vcpu_count.setter
    def vcpu_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af45ad58c0d6db33ad268713102f9f37b687310d5f1c3a46097ce36bfcda402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ManagedKafkaClusterCapacityConfig]:
        return typing.cast(typing.Optional[ManagedKafkaClusterCapacityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedKafkaClusterCapacityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a615a75667fd7002dfbbf27b37581a2cb40025aba34c4f2fd3bf23feef65de4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "capacity_config": "capacityConfig",
        "cluster_id": "clusterId",
        "gcp_config": "gcpConfig",
        "location": "location",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "rebalance_config": "rebalanceConfig",
        "timeouts": "timeouts",
    },
)
class ManagedKafkaClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity_config: typing.Union[ManagedKafkaClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
        cluster_id: builtins.str,
        gcp_config: typing.Union["ManagedKafkaClusterGcpConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        rebalance_config: typing.Optional[typing.Union["ManagedKafkaClusterRebalanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ManagedKafkaClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capacity_config: capacity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#capacity_config ManagedKafkaCluster#capacity_config}
        :param cluster_id: The ID to use for the cluster, which will become the final component of the cluster's name. The ID must be 1-63 characters long, and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' to comply with RFC 1035. This value is structured like: 'my-cluster-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#cluster_id ManagedKafkaCluster#cluster_id}
        :param gcp_config: gcp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#gcp_config ManagedKafkaCluster#gcp_config}
        :param location: ID of the location of the Kafka resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#location ManagedKafkaCluster#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#id ManagedKafkaCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: List of label KEY=VALUE pairs to add. Keys must start with a lowercase character and contain only hyphens (-), underscores ( ), lowercase characters, and numbers. Values must contain only hyphens (-), underscores ( ), lowercase characters, and numbers. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#labels ManagedKafkaCluster#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#project ManagedKafkaCluster#project}.
        :param rebalance_config: rebalance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#rebalance_config ManagedKafkaCluster#rebalance_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#timeouts ManagedKafkaCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capacity_config, dict):
            capacity_config = ManagedKafkaClusterCapacityConfig(**capacity_config)
        if isinstance(gcp_config, dict):
            gcp_config = ManagedKafkaClusterGcpConfig(**gcp_config)
        if isinstance(rebalance_config, dict):
            rebalance_config = ManagedKafkaClusterRebalanceConfig(**rebalance_config)
        if isinstance(timeouts, dict):
            timeouts = ManagedKafkaClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766b988579c8db52e1fec541ecfa5913c57c5bb7d5708090d54662abd39715a3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capacity_config", value=capacity_config, expected_type=type_hints["capacity_config"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument gcp_config", value=gcp_config, expected_type=type_hints["gcp_config"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rebalance_config", value=rebalance_config, expected_type=type_hints["rebalance_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_config": capacity_config,
            "cluster_id": cluster_id,
            "gcp_config": gcp_config,
            "location": location,
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
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if rebalance_config is not None:
            self._values["rebalance_config"] = rebalance_config
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
    def capacity_config(self) -> ManagedKafkaClusterCapacityConfig:
        '''capacity_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#capacity_config ManagedKafkaCluster#capacity_config}
        '''
        result = self._values.get("capacity_config")
        assert result is not None, "Required property 'capacity_config' is missing"
        return typing.cast(ManagedKafkaClusterCapacityConfig, result)

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''The ID to use for the cluster, which will become the final component of the cluster's name.

        The ID must be 1-63 characters long, and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' to comply with RFC 1035. This value is structured like: 'my-cluster-id'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#cluster_id ManagedKafkaCluster#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_config(self) -> "ManagedKafkaClusterGcpConfig":
        '''gcp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#gcp_config ManagedKafkaCluster#gcp_config}
        '''
        result = self._values.get("gcp_config")
        assert result is not None, "Required property 'gcp_config' is missing"
        return typing.cast("ManagedKafkaClusterGcpConfig", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''ID of the location of the Kafka resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#location ManagedKafkaCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#id ManagedKafkaCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''List of label KEY=VALUE pairs to add.

        Keys must start with a lowercase character and contain only hyphens (-), underscores ( ), lowercase characters, and numbers. Values must contain only hyphens (-), underscores ( ), lowercase characters, and numbers.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#labels ManagedKafkaCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#project ManagedKafkaCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rebalance_config(self) -> typing.Optional["ManagedKafkaClusterRebalanceConfig"]:
        '''rebalance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#rebalance_config ManagedKafkaCluster#rebalance_config}
        '''
        result = self._values.get("rebalance_config")
        return typing.cast(typing.Optional["ManagedKafkaClusterRebalanceConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ManagedKafkaClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#timeouts ManagedKafkaCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ManagedKafkaClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterGcpConfig",
    jsii_struct_bases=[],
    name_mapping={"access_config": "accessConfig", "kms_key": "kmsKey"},
)
class ManagedKafkaClusterGcpConfig:
    def __init__(
        self,
        *,
        access_config: typing.Union["ManagedKafkaClusterGcpConfigAccessConfig", typing.Dict[builtins.str, typing.Any]],
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#access_config ManagedKafkaCluster#access_config}
        :param kms_key: The Cloud KMS Key name to use for encryption. The key must be located in the same region as the cluster and cannot be changed. Must be in the format 'projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#kms_key ManagedKafkaCluster#kms_key}
        '''
        if isinstance(access_config, dict):
            access_config = ManagedKafkaClusterGcpConfigAccessConfig(**access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bef5e0929473ae9786b0fc473b3fc29b6811f3efe238e36251c9d0f9c0d413b)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_config": access_config,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def access_config(self) -> "ManagedKafkaClusterGcpConfigAccessConfig":
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#access_config ManagedKafkaCluster#access_config}
        '''
        result = self._values.get("access_config")
        assert result is not None, "Required property 'access_config' is missing"
        return typing.cast("ManagedKafkaClusterGcpConfigAccessConfig", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS Key name to use for encryption.

        The key must be located in the same region as the cluster and cannot be changed. Must be in the format 'projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#kms_key ManagedKafkaCluster#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaClusterGcpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterGcpConfigAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"network_configs": "networkConfigs"},
)
class ManagedKafkaClusterGcpConfigAccessConfig:
    def __init__(
        self,
        *,
        network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param network_configs: network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#network_configs ManagedKafkaCluster#network_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9111cf8e82a2d05ed732106173d0b2d27bb6602f16feb7ac3f96dac5a484df5)
            check_type(argname="argument network_configs", value=network_configs, expected_type=type_hints["network_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_configs": network_configs,
        }

    @builtins.property
    def network_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs"]]:
        '''network_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#network_configs ManagedKafkaCluster#network_configs}
        '''
        result = self._values.get("network_configs")
        assert result is not None, "Required property 'network_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaClusterGcpConfigAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs",
    jsii_struct_bases=[],
    name_mapping={"subnet": "subnet"},
)
class ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs:
    def __init__(self, *, subnet: builtins.str) -> None:
        '''
        :param subnet: Name of the VPC subnet from which the cluster is accessible. Both broker and bootstrap server IP addresses and DNS entries are automatically created in the subnet. There can only be one subnet per network, and the subnet must be located in the same region as the cluster. The project may differ. The name of the subnet must be in the format 'projects/PROJECT_ID/regions/REGION/subnetworks/SUBNET'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#subnet ManagedKafkaCluster#subnet}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d69a1317283cb612b1d05b06d8713b9a1150a7822e8ae5249efd84f2cc1aab4)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet": subnet,
        }

    @builtins.property
    def subnet(self) -> builtins.str:
        '''Name of the VPC subnet from which the cluster is accessible.

        Both broker and bootstrap server IP addresses and DNS entries are automatically created in the subnet. There can only be one subnet per network, and the subnet must be located in the same region as the cluster. The project may differ. The name of the subnet must be in the format 'projects/PROJECT_ID/regions/REGION/subnetworks/SUBNET'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#subnet ManagedKafkaCluster#subnet}
        '''
        result = self._values.get("subnet")
        assert result is not None, "Required property 'subnet' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e115dea2cd3564583db397df441769599b557813a8bf98f86418c2fe6c4de35c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4587a6f5704178e9a94d7463d1c68cb7b71ce5c09e42b93f8ef44c27c0a42e69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef63e1472eac71b4e9f8ea2c8636157843624c1ee17d896a324d8c2bea05036)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6fc917700ee6ebef9dc58ebe5c9d2457bd28010222721586d0e070ba99aaad0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40d4866a9d35f8447ef9a79b5a434b0b3b39f188dd0ac8e32c67d02174412c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59ddff7785de03471df1ea36f4a110e6a37a12a9b88454ed1f6ae92a4d17ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10b3b209e2a7e4c719dcddae52450b11d5107c25e532601c82bfdf71bf1bbaea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="subnetInput")
    def subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetInput"))

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet"))

    @subnet.setter
    def subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d70f2618f670936aab6ef97e61882fef48fac57782b713450be22f34c4ab44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcfc16d8666ee453c89d8c103a3a19f529a5ec3376d3af6eb4f87dbfa788e2df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ManagedKafkaClusterGcpConfigAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterGcpConfigAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd7ff3578cb5f447f34cd98d1bb2f9db0cfc6f0659b74ed34d5c28387fbb6eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkConfigs")
    def put_network_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31723c0f8f0717855be1f06f0f08a461dfc83446a0147e4ef2521bc7c73d4268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkConfigs", [value]))

    @builtins.property
    @jsii.member(jsii_name="networkConfigs")
    def network_configs(
        self,
    ) -> ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList:
        return typing.cast(ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList, jsii.get(self, "networkConfigs"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigsInput")
    def network_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]], jsii.get(self, "networkConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ManagedKafkaClusterGcpConfigAccessConfig]:
        return typing.cast(typing.Optional[ManagedKafkaClusterGcpConfigAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedKafkaClusterGcpConfigAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a13e0ffa170d4a8f870e8c8aa6707ebade429b39e959ab7d6b6cb643591d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ManagedKafkaClusterGcpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterGcpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__091874e452642ffb8d6e52bbd639aa3ae5bb0c9e7ebcd06cd5e1e45460034b7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        *,
        network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param network_configs: network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#network_configs ManagedKafkaCluster#network_configs}
        '''
        value = ManagedKafkaClusterGcpConfigAccessConfig(
            network_configs=network_configs
        )

        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @builtins.property
    @jsii.member(jsii_name="accessConfig")
    def access_config(self) -> ManagedKafkaClusterGcpConfigAccessConfigOutputReference:
        return typing.cast(ManagedKafkaClusterGcpConfigAccessConfigOutputReference, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional[ManagedKafkaClusterGcpConfigAccessConfig]:
        return typing.cast(typing.Optional[ManagedKafkaClusterGcpConfigAccessConfig], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1241507c6562860c0869962c13b02be4be146fd000a6e155b35d0d5f8e7d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ManagedKafkaClusterGcpConfig]:
        return typing.cast(typing.Optional[ManagedKafkaClusterGcpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedKafkaClusterGcpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f871df62f559447304f1709fe3a9daf72959b0a7ba5f307d58a120db92d6a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterRebalanceConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class ManagedKafkaClusterRebalanceConfig:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: The rebalance behavior for the cluster. When not specified, defaults to 'NO_REBALANCE'. Possible values: 'MODE_UNSPECIFIED', 'NO_REBALANCE', 'AUTO_REBALANCE_ON_SCALE_UP'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#mode ManagedKafkaCluster#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b250199e7e42e99035beb596f0c6a2780adc3686da4d443b46e2de82113292)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The rebalance behavior for the cluster. When not specified, defaults to 'NO_REBALANCE'. Possible values: 'MODE_UNSPECIFIED', 'NO_REBALANCE', 'AUTO_REBALANCE_ON_SCALE_UP'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#mode ManagedKafkaCluster#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaClusterRebalanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedKafkaClusterRebalanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterRebalanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b02dbee798591bb4a81d52d39f2b3a8f6df7b24b48646e21cdfd3522fed2999)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22471f03e39ca6bc2899ab3cb7ffa92ed1da5b8223f537618ce87e83f671bff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ManagedKafkaClusterRebalanceConfig]:
        return typing.cast(typing.Optional[ManagedKafkaClusterRebalanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedKafkaClusterRebalanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a00062e9a09ea4b37d366da0367f39a0965e2fec9de182c4acfda41cd8cef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ManagedKafkaClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#create ManagedKafkaCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#delete ManagedKafkaCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#update ManagedKafkaCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a08c41710b680901c9ba4c017ab221290759c8b25bce30fa92f28740356bb93)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#create ManagedKafkaCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#delete ManagedKafkaCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/managed_kafka_cluster#update ManagedKafkaCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedKafkaClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.managedKafkaCluster.ManagedKafkaClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa20ac56b73f45ac6fc5d26a78762cb648c05625a267412035705283cdbc388e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27cc5528b8e9a3498041b32896c11b282fab042fe7a551eab56d2c1f1927af04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9e1dcde9790087d82e617d4d6404a3edb0dd74ef0533183100a6fce344856c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33509c4556789b9e29d132319e98603c77647028630eb66b908d0999c3793fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedKafkaClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedKafkaClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedKafkaClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073297ee2b9eee5bff85075962784d036d77fd4a262520c3711ed4d5a2eb6be3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ManagedKafkaCluster",
    "ManagedKafkaClusterCapacityConfig",
    "ManagedKafkaClusterCapacityConfigOutputReference",
    "ManagedKafkaClusterConfig",
    "ManagedKafkaClusterGcpConfig",
    "ManagedKafkaClusterGcpConfigAccessConfig",
    "ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs",
    "ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList",
    "ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference",
    "ManagedKafkaClusterGcpConfigAccessConfigOutputReference",
    "ManagedKafkaClusterGcpConfigOutputReference",
    "ManagedKafkaClusterRebalanceConfig",
    "ManagedKafkaClusterRebalanceConfigOutputReference",
    "ManagedKafkaClusterTimeouts",
    "ManagedKafkaClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1b287f92d9d9d037f892b656b79c6aeb590277e050d79e1a21ef0e09e9f86c69(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity_config: typing.Union[ManagedKafkaClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
    cluster_id: builtins.str,
    gcp_config: typing.Union[ManagedKafkaClusterGcpConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    rebalance_config: typing.Optional[typing.Union[ManagedKafkaClusterRebalanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ManagedKafkaClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__62179bee48f279b4e0712f5db4ff3098e64e5d0f62333453abfeb38c002a8575(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2538d5f6a220346722c42a696de833ef74732b72c6137ca368ab9ab90f97c716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc7e095a098190007198a1a1e0c1ca0a8e4958aceaad9af2bc118d597e022cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4403dae38a124e32dc82c569383f883b89e6ebc7224fb184599230a5c09a418(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb80bd0b808fb1cb45e03aaf45cd7e33cbd0b365b4568dd15e6abe74e75e0f17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f922721591c4013ecad1b59b60a919e4bd4f4d4a7177b7f233da94673ad133db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86133390f27f41c1bc02323db97b2c1d56a6052201758a7b6198a67ef03faad3(
    *,
    memory_bytes: builtins.str,
    vcpu_count: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a9b54889fea79166abb1048e21639df2a0a8c54d485f92800b6a406284577b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787977a9fb2dd1bfb2a99b48027aae97d8a469526a3502a3c86e63eb00c47b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af45ad58c0d6db33ad268713102f9f37b687310d5f1c3a46097ce36bfcda402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a615a75667fd7002dfbbf27b37581a2cb40025aba34c4f2fd3bf23feef65de4e(
    value: typing.Optional[ManagedKafkaClusterCapacityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766b988579c8db52e1fec541ecfa5913c57c5bb7d5708090d54662abd39715a3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity_config: typing.Union[ManagedKafkaClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
    cluster_id: builtins.str,
    gcp_config: typing.Union[ManagedKafkaClusterGcpConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    rebalance_config: typing.Optional[typing.Union[ManagedKafkaClusterRebalanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ManagedKafkaClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bef5e0929473ae9786b0fc473b3fc29b6811f3efe238e36251c9d0f9c0d413b(
    *,
    access_config: typing.Union[ManagedKafkaClusterGcpConfigAccessConfig, typing.Dict[builtins.str, typing.Any]],
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9111cf8e82a2d05ed732106173d0b2d27bb6602f16feb7ac3f96dac5a484df5(
    *,
    network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d69a1317283cb612b1d05b06d8713b9a1150a7822e8ae5249efd84f2cc1aab4(
    *,
    subnet: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e115dea2cd3564583db397df441769599b557813a8bf98f86418c2fe6c4de35c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4587a6f5704178e9a94d7463d1c68cb7b71ce5c09e42b93f8ef44c27c0a42e69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef63e1472eac71b4e9f8ea2c8636157843624c1ee17d896a324d8c2bea05036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fc917700ee6ebef9dc58ebe5c9d2457bd28010222721586d0e070ba99aaad0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d4866a9d35f8447ef9a79b5a434b0b3b39f188dd0ac8e32c67d02174412c06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59ddff7785de03471df1ea36f4a110e6a37a12a9b88454ed1f6ae92a4d17ffe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b3b209e2a7e4c719dcddae52450b11d5107c25e532601c82bfdf71bf1bbaea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d70f2618f670936aab6ef97e61882fef48fac57782b713450be22f34c4ab44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfc16d8666ee453c89d8c103a3a19f529a5ec3376d3af6eb4f87dbfa788e2df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7ff3578cb5f447f34cd98d1bb2f9db0cfc6f0659b74ed34d5c28387fbb6eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31723c0f8f0717855be1f06f0f08a461dfc83446a0147e4ef2521bc7c73d4268(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a13e0ffa170d4a8f870e8c8aa6707ebade429b39e959ab7d6b6cb643591d4d(
    value: typing.Optional[ManagedKafkaClusterGcpConfigAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091874e452642ffb8d6e52bbd639aa3ae5bb0c9e7ebcd06cd5e1e45460034b7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1241507c6562860c0869962c13b02be4be146fd000a6e155b35d0d5f8e7d02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f871df62f559447304f1709fe3a9daf72959b0a7ba5f307d58a120db92d6a2(
    value: typing.Optional[ManagedKafkaClusterGcpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b250199e7e42e99035beb596f0c6a2780adc3686da4d443b46e2de82113292(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b02dbee798591bb4a81d52d39f2b3a8f6df7b24b48646e21cdfd3522fed2999(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22471f03e39ca6bc2899ab3cb7ffa92ed1da5b8223f537618ce87e83f671bff1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a00062e9a09ea4b37d366da0367f39a0965e2fec9de182c4acfda41cd8cef6(
    value: typing.Optional[ManagedKafkaClusterRebalanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a08c41710b680901c9ba4c017ab221290759c8b25bce30fa92f28740356bb93(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa20ac56b73f45ac6fc5d26a78762cb648c05625a267412035705283cdbc388e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cc5528b8e9a3498041b32896c11b282fab042fe7a551eab56d2c1f1927af04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9e1dcde9790087d82e617d4d6404a3edb0dd74ef0533183100a6fce344856c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33509c4556789b9e29d132319e98603c77647028630eb66b908d0999c3793fe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073297ee2b9eee5bff85075962784d036d77fd4a262520c3711ed4d5a2eb6be3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ManagedKafkaClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
