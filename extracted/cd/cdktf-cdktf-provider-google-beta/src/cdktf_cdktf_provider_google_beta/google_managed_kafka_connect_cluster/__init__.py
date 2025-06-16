r'''
# `google_managed_kafka_connect_cluster`

Refer to the Terraform Registry for docs: [`google_managed_kafka_connect_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster).
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


class GoogleManagedKafkaConnectCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster google_managed_kafka_connect_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        capacity_config: typing.Union["GoogleManagedKafkaConnectClusterCapacityConfig", typing.Dict[builtins.str, typing.Any]],
        connect_cluster_id: builtins.str,
        gcp_config: typing.Union["GoogleManagedKafkaConnectClusterGcpConfig", typing.Dict[builtins.str, typing.Any]],
        kafka_cluster: builtins.str,
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleManagedKafkaConnectClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster google_managed_kafka_connect_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity_config: capacity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#capacity_config GoogleManagedKafkaConnectCluster#capacity_config}
        :param connect_cluster_id: The ID to use for the Connect Cluster, which will become the final component of the connect cluster's name. This value is structured like: 'my-connect-cluster-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#connect_cluster_id GoogleManagedKafkaConnectCluster#connect_cluster_id}
        :param gcp_config: gcp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#gcp_config GoogleManagedKafkaConnectCluster#gcp_config}
        :param kafka_cluster: The name of the Kafka cluster this Kafka Connect cluster is attached to. Structured like: 'projects/PROJECT_ID/locations/LOCATION/clusters/CLUSTER_ID'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#kafka_cluster GoogleManagedKafkaConnectCluster#kafka_cluster}
        :param location: ID of the location of the Kafka Connect resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#location GoogleManagedKafkaConnectCluster#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#id GoogleManagedKafkaConnectCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: List of label KEY=VALUE pairs to add. Keys must start with a lowercase character and contain only hyphens (-), underscores ( ), lowercase characters, and numbers. Values must contain only hyphens (-), underscores ( ), lowercase characters, and numbers. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#labels GoogleManagedKafkaConnectCluster#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#project GoogleManagedKafkaConnectCluster#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#timeouts GoogleManagedKafkaConnectCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e623b52ec3940956057ef2df769c31a726e623d57090fdb06f84b08f56e4deff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleManagedKafkaConnectClusterConfig(
            capacity_config=capacity_config,
            connect_cluster_id=connect_cluster_id,
            gcp_config=gcp_config,
            kafka_cluster=kafka_cluster,
            location=location,
            id=id,
            labels=labels,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleManagedKafkaConnectCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleManagedKafkaConnectCluster to import.
        :param import_from_id: The id of the existing GoogleManagedKafkaConnectCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleManagedKafkaConnectCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5aced72a87b3b8a1eafa4b245bf1561af8fc47ba61edbf8433ccbda0cbd9b27)
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
        :param memory_bytes: The memory to provision for the cluster in bytes. The CPU:memory ratio (vCPU:GiB) must be between 1:1 and 1:8. Minimum: 3221225472 (3 GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#memory_bytes GoogleManagedKafkaConnectCluster#memory_bytes}
        :param vcpu_count: The number of vCPUs to provision for the cluster. The minimum is 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#vcpu_count GoogleManagedKafkaConnectCluster#vcpu_count}
        '''
        value = GoogleManagedKafkaConnectClusterCapacityConfig(
            memory_bytes=memory_bytes, vcpu_count=vcpu_count
        )

        return typing.cast(None, jsii.invoke(self, "putCapacityConfig", [value]))

    @jsii.member(jsii_name="putGcpConfig")
    def put_gcp_config(
        self,
        *,
        access_config: typing.Union["GoogleManagedKafkaConnectClusterGcpConfigAccessConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#access_config GoogleManagedKafkaConnectCluster#access_config}
        '''
        value = GoogleManagedKafkaConnectClusterGcpConfig(access_config=access_config)

        return typing.cast(None, jsii.invoke(self, "putGcpConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#create GoogleManagedKafkaConnectCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#delete GoogleManagedKafkaConnectCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#update GoogleManagedKafkaConnectCluster#update}.
        '''
        value = GoogleManagedKafkaConnectClusterTimeouts(
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
    def capacity_config(
        self,
    ) -> "GoogleManagedKafkaConnectClusterCapacityConfigOutputReference":
        return typing.cast("GoogleManagedKafkaConnectClusterCapacityConfigOutputReference", jsii.get(self, "capacityConfig"))

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
    def gcp_config(self) -> "GoogleManagedKafkaConnectClusterGcpConfigOutputReference":
        return typing.cast("GoogleManagedKafkaConnectClusterGcpConfigOutputReference", jsii.get(self, "gcpConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

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
    def timeouts(self) -> "GoogleManagedKafkaConnectClusterTimeoutsOutputReference":
        return typing.cast("GoogleManagedKafkaConnectClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="capacityConfigInput")
    def capacity_config_input(
        self,
    ) -> typing.Optional["GoogleManagedKafkaConnectClusterCapacityConfig"]:
        return typing.cast(typing.Optional["GoogleManagedKafkaConnectClusterCapacityConfig"], jsii.get(self, "capacityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectClusterIdInput")
    def connect_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpConfigInput")
    def gcp_config_input(
        self,
    ) -> typing.Optional["GoogleManagedKafkaConnectClusterGcpConfig"]:
        return typing.cast(typing.Optional["GoogleManagedKafkaConnectClusterGcpConfig"], jsii.get(self, "gcpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterInput")
    def kafka_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kafkaClusterInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleManagedKafkaConnectClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleManagedKafkaConnectClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectClusterId")
    def connect_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectClusterId"))

    @connect_cluster_id.setter
    def connect_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4a6b1ed369d106da2c68a043354a1d12d405955ee1c874426b2000b2581a98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__677eadf1de21694bb9835a6ef3da2364344b2180a926a78cd789aa9e4102800d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kafkaCluster")
    def kafka_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kafkaCluster"))

    @kafka_cluster.setter
    def kafka_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6087a0320e751774085f545500ab0f12c11f1a62aaf9d11f88ecd77676521eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kafkaCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd08e310bdb86b1d152309f059c21cbfe3d5faa4f589f8c8d128d8149fb1c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ffa8115163b2b5dfa30c551cf0530c79c21ca29a95e59553dff6bb6adbecb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c50add51c5e11563b1bbe699987fdcf605471ba71545bce4f2c55c6b4d3080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterCapacityConfig",
    jsii_struct_bases=[],
    name_mapping={"memory_bytes": "memoryBytes", "vcpu_count": "vcpuCount"},
)
class GoogleManagedKafkaConnectClusterCapacityConfig:
    def __init__(self, *, memory_bytes: builtins.str, vcpu_count: builtins.str) -> None:
        '''
        :param memory_bytes: The memory to provision for the cluster in bytes. The CPU:memory ratio (vCPU:GiB) must be between 1:1 and 1:8. Minimum: 3221225472 (3 GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#memory_bytes GoogleManagedKafkaConnectCluster#memory_bytes}
        :param vcpu_count: The number of vCPUs to provision for the cluster. The minimum is 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#vcpu_count GoogleManagedKafkaConnectCluster#vcpu_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d1e5b213ccd43976dd1ea70fa357fc6e0c5d6c354c3b6bd9cf65e5b5905545)
            check_type(argname="argument memory_bytes", value=memory_bytes, expected_type=type_hints["memory_bytes"])
            check_type(argname="argument vcpu_count", value=vcpu_count, expected_type=type_hints["vcpu_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "memory_bytes": memory_bytes,
            "vcpu_count": vcpu_count,
        }

    @builtins.property
    def memory_bytes(self) -> builtins.str:
        '''The memory to provision for the cluster in bytes.

        The CPU:memory ratio (vCPU:GiB) must be between 1:1 and 1:8. Minimum: 3221225472 (3 GiB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#memory_bytes GoogleManagedKafkaConnectCluster#memory_bytes}
        '''
        result = self._values.get("memory_bytes")
        assert result is not None, "Required property 'memory_bytes' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vcpu_count(self) -> builtins.str:
        '''The number of vCPUs to provision for the cluster. The minimum is 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#vcpu_count GoogleManagedKafkaConnectCluster#vcpu_count}
        '''
        result = self._values.get("vcpu_count")
        assert result is not None, "Required property 'vcpu_count' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaConnectClusterCapacityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleManagedKafkaConnectClusterCapacityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterCapacityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2576466a81b098d487b33242973de776b38d8e981b1dbfec5445be8b1f6f3aa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f815dbae1d720ed5bdec0a5082fbcb082d69a8ce38d8af02aac4b75fe10467e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcpuCount")
    def vcpu_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcpuCount"))

    @vcpu_count.setter
    def vcpu_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0716d3bca6989f152445a6fd40e4253cd622c87b2af6f3dd1b9793545d7bb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleManagedKafkaConnectClusterCapacityConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaConnectClusterCapacityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleManagedKafkaConnectClusterCapacityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66999556043d981f1be42ccffaefe336eaa07177af61ecdca5adbc4fe02d65a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterConfig",
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
        "connect_cluster_id": "connectClusterId",
        "gcp_config": "gcpConfig",
        "kafka_cluster": "kafkaCluster",
        "location": "location",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleManagedKafkaConnectClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity_config: typing.Union[GoogleManagedKafkaConnectClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
        connect_cluster_id: builtins.str,
        gcp_config: typing.Union["GoogleManagedKafkaConnectClusterGcpConfig", typing.Dict[builtins.str, typing.Any]],
        kafka_cluster: builtins.str,
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleManagedKafkaConnectClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capacity_config: capacity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#capacity_config GoogleManagedKafkaConnectCluster#capacity_config}
        :param connect_cluster_id: The ID to use for the Connect Cluster, which will become the final component of the connect cluster's name. This value is structured like: 'my-connect-cluster-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#connect_cluster_id GoogleManagedKafkaConnectCluster#connect_cluster_id}
        :param gcp_config: gcp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#gcp_config GoogleManagedKafkaConnectCluster#gcp_config}
        :param kafka_cluster: The name of the Kafka cluster this Kafka Connect cluster is attached to. Structured like: 'projects/PROJECT_ID/locations/LOCATION/clusters/CLUSTER_ID'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#kafka_cluster GoogleManagedKafkaConnectCluster#kafka_cluster}
        :param location: ID of the location of the Kafka Connect resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#location GoogleManagedKafkaConnectCluster#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#id GoogleManagedKafkaConnectCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: List of label KEY=VALUE pairs to add. Keys must start with a lowercase character and contain only hyphens (-), underscores ( ), lowercase characters, and numbers. Values must contain only hyphens (-), underscores ( ), lowercase characters, and numbers. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#labels GoogleManagedKafkaConnectCluster#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#project GoogleManagedKafkaConnectCluster#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#timeouts GoogleManagedKafkaConnectCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capacity_config, dict):
            capacity_config = GoogleManagedKafkaConnectClusterCapacityConfig(**capacity_config)
        if isinstance(gcp_config, dict):
            gcp_config = GoogleManagedKafkaConnectClusterGcpConfig(**gcp_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleManagedKafkaConnectClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e605cadaf54675253051d0a8bfb3480b8ede9ca3268748e5b8476b010ff736d0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capacity_config", value=capacity_config, expected_type=type_hints["capacity_config"])
            check_type(argname="argument connect_cluster_id", value=connect_cluster_id, expected_type=type_hints["connect_cluster_id"])
            check_type(argname="argument gcp_config", value=gcp_config, expected_type=type_hints["gcp_config"])
            check_type(argname="argument kafka_cluster", value=kafka_cluster, expected_type=type_hints["kafka_cluster"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_config": capacity_config,
            "connect_cluster_id": connect_cluster_id,
            "gcp_config": gcp_config,
            "kafka_cluster": kafka_cluster,
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
    def capacity_config(self) -> GoogleManagedKafkaConnectClusterCapacityConfig:
        '''capacity_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#capacity_config GoogleManagedKafkaConnectCluster#capacity_config}
        '''
        result = self._values.get("capacity_config")
        assert result is not None, "Required property 'capacity_config' is missing"
        return typing.cast(GoogleManagedKafkaConnectClusterCapacityConfig, result)

    @builtins.property
    def connect_cluster_id(self) -> builtins.str:
        '''The ID to use for the Connect Cluster, which will become the final component of the connect cluster's name.

        This value is structured like: 'my-connect-cluster-id'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#connect_cluster_id GoogleManagedKafkaConnectCluster#connect_cluster_id}
        '''
        result = self._values.get("connect_cluster_id")
        assert result is not None, "Required property 'connect_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_config(self) -> "GoogleManagedKafkaConnectClusterGcpConfig":
        '''gcp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#gcp_config GoogleManagedKafkaConnectCluster#gcp_config}
        '''
        result = self._values.get("gcp_config")
        assert result is not None, "Required property 'gcp_config' is missing"
        return typing.cast("GoogleManagedKafkaConnectClusterGcpConfig", result)

    @builtins.property
    def kafka_cluster(self) -> builtins.str:
        '''The name of the Kafka cluster this Kafka Connect cluster is attached to. Structured like: 'projects/PROJECT_ID/locations/LOCATION/clusters/CLUSTER_ID'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#kafka_cluster GoogleManagedKafkaConnectCluster#kafka_cluster}
        '''
        result = self._values.get("kafka_cluster")
        assert result is not None, "Required property 'kafka_cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''ID of the location of the Kafka Connect resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#location GoogleManagedKafkaConnectCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#id GoogleManagedKafkaConnectCluster#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#labels GoogleManagedKafkaConnectCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#project GoogleManagedKafkaConnectCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleManagedKafkaConnectClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#timeouts GoogleManagedKafkaConnectCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleManagedKafkaConnectClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaConnectClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterGcpConfig",
    jsii_struct_bases=[],
    name_mapping={"access_config": "accessConfig"},
)
class GoogleManagedKafkaConnectClusterGcpConfig:
    def __init__(
        self,
        *,
        access_config: typing.Union["GoogleManagedKafkaConnectClusterGcpConfigAccessConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#access_config GoogleManagedKafkaConnectCluster#access_config}
        '''
        if isinstance(access_config, dict):
            access_config = GoogleManagedKafkaConnectClusterGcpConfigAccessConfig(**access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d4fee94beeefa18c21563199183e7a4d8a85fc8944eb3dd04c1c976ffe31a1)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_config": access_config,
        }

    @builtins.property
    def access_config(self) -> "GoogleManagedKafkaConnectClusterGcpConfigAccessConfig":
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#access_config GoogleManagedKafkaConnectCluster#access_config}
        '''
        result = self._values.get("access_config")
        assert result is not None, "Required property 'access_config' is missing"
        return typing.cast("GoogleManagedKafkaConnectClusterGcpConfigAccessConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaConnectClusterGcpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterGcpConfigAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"network_configs": "networkConfigs"},
)
class GoogleManagedKafkaConnectClusterGcpConfigAccessConfig:
    def __init__(
        self,
        *,
        network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param network_configs: network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#network_configs GoogleManagedKafkaConnectCluster#network_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba36ad0380794adb8cc535ff86e9ce34a8f23251712c9a8f7923b510e95d5034)
            check_type(argname="argument network_configs", value=network_configs, expected_type=type_hints["network_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_configs": network_configs,
        }

    @builtins.property
    def network_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs"]]:
        '''network_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#network_configs GoogleManagedKafkaConnectCluster#network_configs}
        '''
        result = self._values.get("network_configs")
        assert result is not None, "Required property 'network_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaConnectClusterGcpConfigAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "primary_subnet": "primarySubnet",
        "additional_subnets": "additionalSubnets",
        "dns_domain_names": "dnsDomainNames",
    },
)
class GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs:
    def __init__(
        self,
        *,
        primary_subnet: builtins.str,
        additional_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        dns_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param primary_subnet: VPC subnet to make available to the Kafka Connect cluster. Structured like: projects/{project}/regions/{region}/subnetworks/{subnet_id}. It is used to create a Private Service Connect (PSC) interface for the Kafka Connect workers. It must be located in the same region as the Kafka Connect cluster. The CIDR range of the subnet must be within the IPv4 address ranges for private networks, as specified in RFC 1918. The primary subnet CIDR range must have a minimum size of /22 (1024 addresses). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#primary_subnet GoogleManagedKafkaConnectCluster#primary_subnet}
        :param additional_subnets: Additional subnets may be specified. They may be in another region, but must be in the same VPC network. The Connect workers can communicate with network endpoints in either the primary or additional subnets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#additional_subnets GoogleManagedKafkaConnectCluster#additional_subnets}
        :param dns_domain_names: Additional DNS domain names from the subnet's network to be made visible to the Connect Cluster. When using MirrorMaker2, it's necessary to add the bootstrap address's dns domain name of the target cluster to make it visible to the connector. For example: my-kafka-cluster.us-central1.managedkafka.my-project.cloud.goog Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#dns_domain_names GoogleManagedKafkaConnectCluster#dns_domain_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265a120d240ffe67f43c5b0b8fbb6b9d243a1a5449d847a3894e6bdb1ccf782e)
            check_type(argname="argument primary_subnet", value=primary_subnet, expected_type=type_hints["primary_subnet"])
            check_type(argname="argument additional_subnets", value=additional_subnets, expected_type=type_hints["additional_subnets"])
            check_type(argname="argument dns_domain_names", value=dns_domain_names, expected_type=type_hints["dns_domain_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primary_subnet": primary_subnet,
        }
        if additional_subnets is not None:
            self._values["additional_subnets"] = additional_subnets
        if dns_domain_names is not None:
            self._values["dns_domain_names"] = dns_domain_names

    @builtins.property
    def primary_subnet(self) -> builtins.str:
        '''VPC subnet to make available to the Kafka Connect cluster.

        Structured like: projects/{project}/regions/{region}/subnetworks/{subnet_id}. It is used to create a Private Service Connect (PSC) interface for the Kafka Connect workers. It must be located in the same region as the Kafka Connect cluster. The CIDR range of the subnet must be within the IPv4 address ranges for private networks, as specified in RFC 1918. The primary subnet CIDR range must have a minimum size of /22 (1024 addresses).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#primary_subnet GoogleManagedKafkaConnectCluster#primary_subnet}
        '''
        result = self._values.get("primary_subnet")
        assert result is not None, "Required property 'primary_subnet' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional subnets may be specified.

        They may be in another region, but must be in the same VPC network. The Connect workers can communicate with network endpoints in either the primary or additional subnets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#additional_subnets GoogleManagedKafkaConnectCluster#additional_subnets}
        '''
        result = self._values.get("additional_subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dns_domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional DNS domain names from the subnet's network to be made visible to the Connect Cluster.

        When using MirrorMaker2, it's necessary to add the bootstrap address's dns domain name of the target cluster to make it visible to the connector. For example: my-kafka-cluster.us-central1.managedkafka.my-project.cloud.goog

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#dns_domain_names GoogleManagedKafkaConnectCluster#dns_domain_names}
        '''
        result = self._values.get("dns_domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98a410ea6198126c8794f5db0e62333d65bcb6814e86691e28591c4a50d81ed1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8bbadfd34492bcdc16b724b0d9cf5f7ee2eb9a1172bf9b215885af0a0a6e03)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad081ddd474e6da7d5da91e09a27f896b9e4490e05a2648c2f6d646abae95d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__340a3c638b944ef6cb9bd8b2231ee4c74db911c2e200cb293008933ae69e49fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7748b0a84be0df5270b6dae260d1fd383e1cfd810e47fd9942fa7b7bcf3d0ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50af8fa03d838f3b5dfbcd8f60b28fcdca7acc9b0ccbd5782a7ffd899cb7311c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a83cbef411417238c0a5011aa0a6a440f08e08585245fdc854d524cbee0651)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdditionalSubnets")
    def reset_additional_subnets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalSubnets", []))

    @jsii.member(jsii_name="resetDnsDomainNames")
    def reset_dns_domain_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsDomainNames", []))

    @builtins.property
    @jsii.member(jsii_name="additionalSubnetsInput")
    def additional_subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalSubnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsDomainNamesInput")
    def dns_domain_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsDomainNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="primarySubnetInput")
    def primary_subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primarySubnetInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalSubnets")
    def additional_subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalSubnets"))

    @additional_subnets.setter
    def additional_subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d828e8a25ae830f804bb19f2200f4da2d02a190da336729bfe1bb6c4627227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsDomainNames")
    def dns_domain_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsDomainNames"))

    @dns_domain_names.setter
    def dns_domain_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07614ef4cd0dd87fe2d73b053f8eb0b2bdd5362263c36d7118d80692a79428c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsDomainNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primarySubnet")
    def primary_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primarySubnet"))

    @primary_subnet.setter
    def primary_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f2dc979a50c9b1cd6b0cb47c1d9ccad66e4ebbce8b6f78adf3b63947c4d2d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primarySubnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd862725560860d0473cfbc4ace2ad2c78d0866a6dcbd0b6d889c5c8a8bb6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleManagedKafkaConnectClusterGcpConfigAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterGcpConfigAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__933ec4435d9653f7981ef10a32ab670326080611f083585f46306c4bfc8f3609)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkConfigs")
    def put_network_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f299bd4811c14d90d2b0acf5f4713a904bed6c05cb73f765f1571815ac093d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkConfigs", [value]))

    @builtins.property
    @jsii.member(jsii_name="networkConfigs")
    def network_configs(
        self,
    ) -> GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsList:
        return typing.cast(GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsList, jsii.get(self, "networkConfigs"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigsInput")
    def network_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]]], jsii.get(self, "networkConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleManagedKafkaConnectClusterGcpConfigAccessConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaConnectClusterGcpConfigAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleManagedKafkaConnectClusterGcpConfigAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701ebec4ea759cdcbc535f9171f3a47cb3200866b445d504c63bf240b4bde71f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleManagedKafkaConnectClusterGcpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterGcpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d08551d325b7cc7610ba8d266bc6db4aa6a86f48a23d66ff99abdad2e338ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        *,
        network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param network_configs: network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#network_configs GoogleManagedKafkaConnectCluster#network_configs}
        '''
        value = GoogleManagedKafkaConnectClusterGcpConfigAccessConfig(
            network_configs=network_configs
        )

        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="accessConfig")
    def access_config(
        self,
    ) -> GoogleManagedKafkaConnectClusterGcpConfigAccessConfigOutputReference:
        return typing.cast(GoogleManagedKafkaConnectClusterGcpConfigAccessConfigOutputReference, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional[GoogleManagedKafkaConnectClusterGcpConfigAccessConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaConnectClusterGcpConfigAccessConfig], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleManagedKafkaConnectClusterGcpConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaConnectClusterGcpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleManagedKafkaConnectClusterGcpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06d33b2c602fc88a90eb7bf5042d185ee896946cab6fb5c4b2fc6127dd559f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleManagedKafkaConnectClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#create GoogleManagedKafkaConnectCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#delete GoogleManagedKafkaConnectCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#update GoogleManagedKafkaConnectCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee520acbb553d8d57197eb1f0082f3aba58f8ab33075114a5476c7f335ad9e0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#create GoogleManagedKafkaConnectCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#delete GoogleManagedKafkaConnectCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_connect_cluster#update GoogleManagedKafkaConnectCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaConnectClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleManagedKafkaConnectClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaConnectCluster.GoogleManagedKafkaConnectClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb614285a9633d704833d8c6507442592fec7343701076903b192f1143a4c166)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dfac7a51d6c48b8752dd89cec3f70541f154103234aa35bccc8f36e28cfd1c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e7c66109cbe8536e5e7da2d5f472981d559d422d26266dce977cd07df38132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c21400b88fc8eeafebbfa4112afb4845dcb0d1551ff9162e41721b4a59d647f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaConnectClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaConnectClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaConnectClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3b5c32f1a2a669da075fae4b87fa547d33257cbf7e4cb122447a7fab2d6fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleManagedKafkaConnectCluster",
    "GoogleManagedKafkaConnectClusterCapacityConfig",
    "GoogleManagedKafkaConnectClusterCapacityConfigOutputReference",
    "GoogleManagedKafkaConnectClusterConfig",
    "GoogleManagedKafkaConnectClusterGcpConfig",
    "GoogleManagedKafkaConnectClusterGcpConfigAccessConfig",
    "GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs",
    "GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsList",
    "GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigsOutputReference",
    "GoogleManagedKafkaConnectClusterGcpConfigAccessConfigOutputReference",
    "GoogleManagedKafkaConnectClusterGcpConfigOutputReference",
    "GoogleManagedKafkaConnectClusterTimeouts",
    "GoogleManagedKafkaConnectClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e623b52ec3940956057ef2df769c31a726e623d57090fdb06f84b08f56e4deff(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity_config: typing.Union[GoogleManagedKafkaConnectClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
    connect_cluster_id: builtins.str,
    gcp_config: typing.Union[GoogleManagedKafkaConnectClusterGcpConfig, typing.Dict[builtins.str, typing.Any]],
    kafka_cluster: builtins.str,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleManagedKafkaConnectClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f5aced72a87b3b8a1eafa4b245bf1561af8fc47ba61edbf8433ccbda0cbd9b27(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4a6b1ed369d106da2c68a043354a1d12d405955ee1c874426b2000b2581a98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677eadf1de21694bb9835a6ef3da2364344b2180a926a78cd789aa9e4102800d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6087a0320e751774085f545500ab0f12c11f1a62aaf9d11f88ecd77676521eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd08e310bdb86b1d152309f059c21cbfe3d5faa4f589f8c8d128d8149fb1c46(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ffa8115163b2b5dfa30c551cf0530c79c21ca29a95e59553dff6bb6adbecb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c50add51c5e11563b1bbe699987fdcf605471ba71545bce4f2c55c6b4d3080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d1e5b213ccd43976dd1ea70fa357fc6e0c5d6c354c3b6bd9cf65e5b5905545(
    *,
    memory_bytes: builtins.str,
    vcpu_count: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2576466a81b098d487b33242973de776b38d8e981b1dbfec5445be8b1f6f3aa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f815dbae1d720ed5bdec0a5082fbcb082d69a8ce38d8af02aac4b75fe10467e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0716d3bca6989f152445a6fd40e4253cd622c87b2af6f3dd1b9793545d7bb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66999556043d981f1be42ccffaefe336eaa07177af61ecdca5adbc4fe02d65a(
    value: typing.Optional[GoogleManagedKafkaConnectClusterCapacityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e605cadaf54675253051d0a8bfb3480b8ede9ca3268748e5b8476b010ff736d0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity_config: typing.Union[GoogleManagedKafkaConnectClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
    connect_cluster_id: builtins.str,
    gcp_config: typing.Union[GoogleManagedKafkaConnectClusterGcpConfig, typing.Dict[builtins.str, typing.Any]],
    kafka_cluster: builtins.str,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleManagedKafkaConnectClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d4fee94beeefa18c21563199183e7a4d8a85fc8944eb3dd04c1c976ffe31a1(
    *,
    access_config: typing.Union[GoogleManagedKafkaConnectClusterGcpConfigAccessConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba36ad0380794adb8cc535ff86e9ce34a8f23251712c9a8f7923b510e95d5034(
    *,
    network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265a120d240ffe67f43c5b0b8fbb6b9d243a1a5449d847a3894e6bdb1ccf782e(
    *,
    primary_subnet: builtins.str,
    additional_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    dns_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a410ea6198126c8794f5db0e62333d65bcb6814e86691e28591c4a50d81ed1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8bbadfd34492bcdc16b724b0d9cf5f7ee2eb9a1172bf9b215885af0a0a6e03(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad081ddd474e6da7d5da91e09a27f896b9e4490e05a2648c2f6d646abae95d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340a3c638b944ef6cb9bd8b2231ee4c74db911c2e200cb293008933ae69e49fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7748b0a84be0df5270b6dae260d1fd383e1cfd810e47fd9942fa7b7bcf3d0ac5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50af8fa03d838f3b5dfbcd8f60b28fcdca7acc9b0ccbd5782a7ffd899cb7311c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a83cbef411417238c0a5011aa0a6a440f08e08585245fdc854d524cbee0651(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d828e8a25ae830f804bb19f2200f4da2d02a190da336729bfe1bb6c4627227(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07614ef4cd0dd87fe2d73b053f8eb0b2bdd5362263c36d7118d80692a79428c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2dc979a50c9b1cd6b0cb47c1d9ccad66e4ebbce8b6f78adf3b63947c4d2d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd862725560860d0473cfbc4ace2ad2c78d0866a6dcbd0b6d889c5c8a8bb6d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933ec4435d9653f7981ef10a32ab670326080611f083585f46306c4bfc8f3609(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f299bd4811c14d90d2b0acf5f4713a904bed6c05cb73f765f1571815ac093d30(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleManagedKafkaConnectClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701ebec4ea759cdcbc535f9171f3a47cb3200866b445d504c63bf240b4bde71f(
    value: typing.Optional[GoogleManagedKafkaConnectClusterGcpConfigAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d08551d325b7cc7610ba8d266bc6db4aa6a86f48a23d66ff99abdad2e338ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06d33b2c602fc88a90eb7bf5042d185ee896946cab6fb5c4b2fc6127dd559f3(
    value: typing.Optional[GoogleManagedKafkaConnectClusterGcpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee520acbb553d8d57197eb1f0082f3aba58f8ab33075114a5476c7f335ad9e0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb614285a9633d704833d8c6507442592fec7343701076903b192f1143a4c166(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfac7a51d6c48b8752dd89cec3f70541f154103234aa35bccc8f36e28cfd1c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e7c66109cbe8536e5e7da2d5f472981d559d422d26266dce977cd07df38132(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c21400b88fc8eeafebbfa4112afb4845dcb0d1551ff9162e41721b4a59d647f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3b5c32f1a2a669da075fae4b87fa547d33257cbf7e4cb122447a7fab2d6fb5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaConnectClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
