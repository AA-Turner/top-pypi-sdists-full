r'''
# `google_managed_kafka_cluster`

Refer to the Terraform Registry for docs: [`google_managed_kafka_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster).
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


class GoogleManagedKafkaCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster google_managed_kafka_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        capacity_config: typing.Union["GoogleManagedKafkaClusterCapacityConfig", typing.Dict[builtins.str, typing.Any]],
        cluster_id: builtins.str,
        gcp_config: typing.Union["GoogleManagedKafkaClusterGcpConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        rebalance_config: typing.Optional[typing.Union["GoogleManagedKafkaClusterRebalanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleManagedKafkaClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster google_managed_kafka_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity_config: capacity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#capacity_config GoogleManagedKafkaCluster#capacity_config}
        :param cluster_id: The ID to use for the cluster, which will become the final component of the cluster's name. The ID must be 1-63 characters long, and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' to comply with RFC 1035. This value is structured like: 'my-cluster-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#cluster_id GoogleManagedKafkaCluster#cluster_id}
        :param gcp_config: gcp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#gcp_config GoogleManagedKafkaCluster#gcp_config}
        :param location: ID of the location of the Kafka resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#location GoogleManagedKafkaCluster#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#id GoogleManagedKafkaCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: List of label KEY=VALUE pairs to add. Keys must start with a lowercase character and contain only hyphens (-), underscores ( ), lowercase characters, and numbers. Values must contain only hyphens (-), underscores ( ), lowercase characters, and numbers. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#labels GoogleManagedKafkaCluster#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#project GoogleManagedKafkaCluster#project}.
        :param rebalance_config: rebalance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#rebalance_config GoogleManagedKafkaCluster#rebalance_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#timeouts GoogleManagedKafkaCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86710a20b78f4a0bad34217125e088c6c60f94827acb0d22e9b645988835ccf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleManagedKafkaClusterConfig(
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
        '''Generates CDKTF code for importing a GoogleManagedKafkaCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleManagedKafkaCluster to import.
        :param import_from_id: The id of the existing GoogleManagedKafkaCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleManagedKafkaCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64fab6fdb9c23321521f14ad91c60b5cc5efcd52aef123a4c54bb24095f2675b)
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
        :param memory_bytes: The memory to provision for the cluster in bytes. The value must be between 1 GiB and 8 GiB per vCPU. Ex. 1024Mi, 4Gi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#memory_bytes GoogleManagedKafkaCluster#memory_bytes}
        :param vcpu_count: The number of vCPUs to provision for the cluster. The minimum is 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#vcpu_count GoogleManagedKafkaCluster#vcpu_count}
        '''
        value = GoogleManagedKafkaClusterCapacityConfig(
            memory_bytes=memory_bytes, vcpu_count=vcpu_count
        )

        return typing.cast(None, jsii.invoke(self, "putCapacityConfig", [value]))

    @jsii.member(jsii_name="putGcpConfig")
    def put_gcp_config(
        self,
        *,
        access_config: typing.Union["GoogleManagedKafkaClusterGcpConfigAccessConfig", typing.Dict[builtins.str, typing.Any]],
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#access_config GoogleManagedKafkaCluster#access_config}
        :param kms_key: The Cloud KMS Key name to use for encryption. The key must be located in the same region as the cluster and cannot be changed. Must be in the format 'projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#kms_key GoogleManagedKafkaCluster#kms_key}
        '''
        value = GoogleManagedKafkaClusterGcpConfig(
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
        :param mode: The rebalance behavior for the cluster. When not specified, defaults to 'NO_REBALANCE'. Possible values: 'MODE_UNSPECIFIED', 'NO_REBALANCE', 'AUTO_REBALANCE_ON_SCALE_UP'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#mode GoogleManagedKafkaCluster#mode}
        '''
        value = GoogleManagedKafkaClusterRebalanceConfig(mode=mode)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#create GoogleManagedKafkaCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#delete GoogleManagedKafkaCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#update GoogleManagedKafkaCluster#update}.
        '''
        value = GoogleManagedKafkaClusterTimeouts(
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
    def capacity_config(
        self,
    ) -> "GoogleManagedKafkaClusterCapacityConfigOutputReference":
        return typing.cast("GoogleManagedKafkaClusterCapacityConfigOutputReference", jsii.get(self, "capacityConfig"))

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
    def gcp_config(self) -> "GoogleManagedKafkaClusterGcpConfigOutputReference":
        return typing.cast("GoogleManagedKafkaClusterGcpConfigOutputReference", jsii.get(self, "gcpConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="rebalanceConfig")
    def rebalance_config(
        self,
    ) -> "GoogleManagedKafkaClusterRebalanceConfigOutputReference":
        return typing.cast("GoogleManagedKafkaClusterRebalanceConfigOutputReference", jsii.get(self, "rebalanceConfig"))

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
    def timeouts(self) -> "GoogleManagedKafkaClusterTimeoutsOutputReference":
        return typing.cast("GoogleManagedKafkaClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="capacityConfigInput")
    def capacity_config_input(
        self,
    ) -> typing.Optional["GoogleManagedKafkaClusterCapacityConfig"]:
        return typing.cast(typing.Optional["GoogleManagedKafkaClusterCapacityConfig"], jsii.get(self, "capacityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpConfigInput")
    def gcp_config_input(self) -> typing.Optional["GoogleManagedKafkaClusterGcpConfig"]:
        return typing.cast(typing.Optional["GoogleManagedKafkaClusterGcpConfig"], jsii.get(self, "gcpConfigInput"))

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
    ) -> typing.Optional["GoogleManagedKafkaClusterRebalanceConfig"]:
        return typing.cast(typing.Optional["GoogleManagedKafkaClusterRebalanceConfig"], jsii.get(self, "rebalanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleManagedKafkaClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleManagedKafkaClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292e8ed71fb7a0ff0eb2db15b5fe4d5ad681f1f1e64af722cb0776f95de72e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63750ef8d6b14db9c6d4bb807dba5cca6b07f8c425e755e0b60da4dc10cd0c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e759871bc542dea3aab4382020806157a5788a94faa27f15adf84962609cad6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bb2ea259cc19470b53edbfe4e85ed9227d35e461d0480254134c71fae9438d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363dbf9261e2d79cae9e9cc744cc12003df75de505aa04608431f912843c3fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterCapacityConfig",
    jsii_struct_bases=[],
    name_mapping={"memory_bytes": "memoryBytes", "vcpu_count": "vcpuCount"},
)
class GoogleManagedKafkaClusterCapacityConfig:
    def __init__(self, *, memory_bytes: builtins.str, vcpu_count: builtins.str) -> None:
        '''
        :param memory_bytes: The memory to provision for the cluster in bytes. The value must be between 1 GiB and 8 GiB per vCPU. Ex. 1024Mi, 4Gi. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#memory_bytes GoogleManagedKafkaCluster#memory_bytes}
        :param vcpu_count: The number of vCPUs to provision for the cluster. The minimum is 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#vcpu_count GoogleManagedKafkaCluster#vcpu_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce779bad556b981123779e2071415a9e11ff05fc8daf4233a85a2875884c81ff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#memory_bytes GoogleManagedKafkaCluster#memory_bytes}
        '''
        result = self._values.get("memory_bytes")
        assert result is not None, "Required property 'memory_bytes' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vcpu_count(self) -> builtins.str:
        '''The number of vCPUs to provision for the cluster. The minimum is 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#vcpu_count GoogleManagedKafkaCluster#vcpu_count}
        '''
        result = self._values.get("vcpu_count")
        assert result is not None, "Required property 'vcpu_count' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaClusterCapacityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleManagedKafkaClusterCapacityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterCapacityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c70cf722beb2384baaa47c2de673dc3f25af129a5fb9a0cc6df3a64fa4f43b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a060f46d3b5345bf910ee9b9fad0d3ea640b2d21411d89d340b636102e6fa4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcpuCount")
    def vcpu_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vcpuCount"))

    @vcpu_count.setter
    def vcpu_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b249ef2411d02b78c4b8147d9a1cac9431129e613b228f1636a6349d6d3b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleManagedKafkaClusterCapacityConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaClusterCapacityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleManagedKafkaClusterCapacityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91787577b59b4721f05bcc854e1c4c015a441a8a8f4cf270942ca8ad159a153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterConfig",
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
class GoogleManagedKafkaClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity_config: typing.Union[GoogleManagedKafkaClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
        cluster_id: builtins.str,
        gcp_config: typing.Union["GoogleManagedKafkaClusterGcpConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        rebalance_config: typing.Optional[typing.Union["GoogleManagedKafkaClusterRebalanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleManagedKafkaClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capacity_config: capacity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#capacity_config GoogleManagedKafkaCluster#capacity_config}
        :param cluster_id: The ID to use for the cluster, which will become the final component of the cluster's name. The ID must be 1-63 characters long, and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' to comply with RFC 1035. This value is structured like: 'my-cluster-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#cluster_id GoogleManagedKafkaCluster#cluster_id}
        :param gcp_config: gcp_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#gcp_config GoogleManagedKafkaCluster#gcp_config}
        :param location: ID of the location of the Kafka resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#location GoogleManagedKafkaCluster#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#id GoogleManagedKafkaCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: List of label KEY=VALUE pairs to add. Keys must start with a lowercase character and contain only hyphens (-), underscores ( ), lowercase characters, and numbers. Values must contain only hyphens (-), underscores ( ), lowercase characters, and numbers. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#labels GoogleManagedKafkaCluster#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#project GoogleManagedKafkaCluster#project}.
        :param rebalance_config: rebalance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#rebalance_config GoogleManagedKafkaCluster#rebalance_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#timeouts GoogleManagedKafkaCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(capacity_config, dict):
            capacity_config = GoogleManagedKafkaClusterCapacityConfig(**capacity_config)
        if isinstance(gcp_config, dict):
            gcp_config = GoogleManagedKafkaClusterGcpConfig(**gcp_config)
        if isinstance(rebalance_config, dict):
            rebalance_config = GoogleManagedKafkaClusterRebalanceConfig(**rebalance_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleManagedKafkaClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5450167f3fd97d06ce2fbf23a31588f6101a5699da115c81c396d7d502b0e7)
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
    def capacity_config(self) -> GoogleManagedKafkaClusterCapacityConfig:
        '''capacity_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#capacity_config GoogleManagedKafkaCluster#capacity_config}
        '''
        result = self._values.get("capacity_config")
        assert result is not None, "Required property 'capacity_config' is missing"
        return typing.cast(GoogleManagedKafkaClusterCapacityConfig, result)

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''The ID to use for the cluster, which will become the final component of the cluster's name.

        The ID must be 1-63 characters long, and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' to comply with RFC 1035. This value is structured like: 'my-cluster-id'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#cluster_id GoogleManagedKafkaCluster#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gcp_config(self) -> "GoogleManagedKafkaClusterGcpConfig":
        '''gcp_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#gcp_config GoogleManagedKafkaCluster#gcp_config}
        '''
        result = self._values.get("gcp_config")
        assert result is not None, "Required property 'gcp_config' is missing"
        return typing.cast("GoogleManagedKafkaClusterGcpConfig", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''ID of the location of the Kafka resource. See https://cloud.google.com/managed-kafka/docs/locations for a list of supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#location GoogleManagedKafkaCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#id GoogleManagedKafkaCluster#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#labels GoogleManagedKafkaCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#project GoogleManagedKafkaCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rebalance_config(
        self,
    ) -> typing.Optional["GoogleManagedKafkaClusterRebalanceConfig"]:
        '''rebalance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#rebalance_config GoogleManagedKafkaCluster#rebalance_config}
        '''
        result = self._values.get("rebalance_config")
        return typing.cast(typing.Optional["GoogleManagedKafkaClusterRebalanceConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleManagedKafkaClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#timeouts GoogleManagedKafkaCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleManagedKafkaClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterGcpConfig",
    jsii_struct_bases=[],
    name_mapping={"access_config": "accessConfig", "kms_key": "kmsKey"},
)
class GoogleManagedKafkaClusterGcpConfig:
    def __init__(
        self,
        *,
        access_config: typing.Union["GoogleManagedKafkaClusterGcpConfigAccessConfig", typing.Dict[builtins.str, typing.Any]],
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#access_config GoogleManagedKafkaCluster#access_config}
        :param kms_key: The Cloud KMS Key name to use for encryption. The key must be located in the same region as the cluster and cannot be changed. Must be in the format 'projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#kms_key GoogleManagedKafkaCluster#kms_key}
        '''
        if isinstance(access_config, dict):
            access_config = GoogleManagedKafkaClusterGcpConfigAccessConfig(**access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3f6ee11f65d404eae0430f313e6fa1f66e4ced5a426a09705ece971b65ba89)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_config": access_config,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def access_config(self) -> "GoogleManagedKafkaClusterGcpConfigAccessConfig":
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#access_config GoogleManagedKafkaCluster#access_config}
        '''
        result = self._values.get("access_config")
        assert result is not None, "Required property 'access_config' is missing"
        return typing.cast("GoogleManagedKafkaClusterGcpConfigAccessConfig", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS Key name to use for encryption.

        The key must be located in the same region as the cluster and cannot be changed. Must be in the format 'projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#kms_key GoogleManagedKafkaCluster#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaClusterGcpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterGcpConfigAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"network_configs": "networkConfigs"},
)
class GoogleManagedKafkaClusterGcpConfigAccessConfig:
    def __init__(
        self,
        *,
        network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param network_configs: network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#network_configs GoogleManagedKafkaCluster#network_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7edca6b6c427edae73c38c2a4e1ac56631bebd3d8d9c9bae501408f4964f41)
            check_type(argname="argument network_configs", value=network_configs, expected_type=type_hints["network_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_configs": network_configs,
        }

    @builtins.property
    def network_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs"]]:
        '''network_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#network_configs GoogleManagedKafkaCluster#network_configs}
        '''
        result = self._values.get("network_configs")
        assert result is not None, "Required property 'network_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaClusterGcpConfigAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs",
    jsii_struct_bases=[],
    name_mapping={"subnet": "subnet"},
)
class GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs:
    def __init__(self, *, subnet: builtins.str) -> None:
        '''
        :param subnet: Name of the VPC subnet from which the cluster is accessible. Both broker and bootstrap server IP addresses and DNS entries are automatically created in the subnet. There can only be one subnet per network, and the subnet must be located in the same region as the cluster. The project may differ. The name of the subnet must be in the format 'projects/PROJECT_ID/regions/REGION/subnetworks/SUBNET'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#subnet GoogleManagedKafkaCluster#subnet}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e368404cb6a0c93b280f21d3cc4b7f50686d1d246ac1f7581f0fe29f874954)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet": subnet,
        }

    @builtins.property
    def subnet(self) -> builtins.str:
        '''Name of the VPC subnet from which the cluster is accessible.

        Both broker and bootstrap server IP addresses and DNS entries are automatically created in the subnet. There can only be one subnet per network, and the subnet must be located in the same region as the cluster. The project may differ. The name of the subnet must be in the format 'projects/PROJECT_ID/regions/REGION/subnetworks/SUBNET'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#subnet GoogleManagedKafkaCluster#subnet}
        '''
        result = self._values.get("subnet")
        assert result is not None, "Required property 'subnet' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__beb7bc0f21bc90314a000926c5ba5fe7046483ac924558069b8d8715f74b80a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe837ced0c6592d6e7fb3592f0a9d18bfbc71a7da7fcd5c46c72a062d255819)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c0656ab1e3045ca6c448895ef13903f30d3ba3b0dc06fc7b0338e05bda7168)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa3c180324f8bc33974bb6fffa7028859119c4b8f9e20a85f8a6a97e9f21309f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97265c74e0f9018984e73bc41ba942cb66bc4c954caeca502e5bfc62e210f48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813a566e5a774131f1b00fb73605b1aa085a44c479aa9a42f765904577aa4e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d6042fff50d069a7137133f25ab4c6d4d7ede332ba3959e96bb6a7494833c4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0baec3fd0c0f8b43fe7c71d194acfdc280b07a9132a9b6a6f773dc1012dce9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57df9fed762cb7dbf940d6157ee5956d545f2a7f783f1945025603ed488e5c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleManagedKafkaClusterGcpConfigAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterGcpConfigAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02db6307523561c5162881da0d2dd7485af04a68db4ffd821a3c0e9242cd1db6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkConfigs")
    def put_network_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ded9f0f064ebd7056f452ac47772f08933df7ced5a9368b69d53d7ce098596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkConfigs", [value]))

    @builtins.property
    @jsii.member(jsii_name="networkConfigs")
    def network_configs(
        self,
    ) -> GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList:
        return typing.cast(GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList, jsii.get(self, "networkConfigs"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigsInput")
    def network_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]], jsii.get(self, "networkConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleManagedKafkaClusterGcpConfigAccessConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaClusterGcpConfigAccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleManagedKafkaClusterGcpConfigAccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea508a5c034550d6128386f3b15ba99fc75b75e83f4b0ff5902904f3fa4f7a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleManagedKafkaClusterGcpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterGcpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fd7e9f675bc7f0f799f9c4616548395a7bbabc198286bb1d6bb4f342963a49c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        *,
        network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param network_configs: network_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#network_configs GoogleManagedKafkaCluster#network_configs}
        '''
        value = GoogleManagedKafkaClusterGcpConfigAccessConfig(
            network_configs=network_configs
        )

        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @builtins.property
    @jsii.member(jsii_name="accessConfig")
    def access_config(
        self,
    ) -> GoogleManagedKafkaClusterGcpConfigAccessConfigOutputReference:
        return typing.cast(GoogleManagedKafkaClusterGcpConfigAccessConfigOutputReference, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional[GoogleManagedKafkaClusterGcpConfigAccessConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaClusterGcpConfigAccessConfig], jsii.get(self, "accessConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cf7fb8a3b74125bab6725bd83cf3e320355e8fe9d2cb3c13fbc67162165eaf05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleManagedKafkaClusterGcpConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaClusterGcpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleManagedKafkaClusterGcpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b0808c38f872fd721e3efbafeeb671e62e763743f0ae0719bfa37f9d111928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterRebalanceConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class GoogleManagedKafkaClusterRebalanceConfig:
    def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mode: The rebalance behavior for the cluster. When not specified, defaults to 'NO_REBALANCE'. Possible values: 'MODE_UNSPECIFIED', 'NO_REBALANCE', 'AUTO_REBALANCE_ON_SCALE_UP'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#mode GoogleManagedKafkaCluster#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6857520b63717fb198f4881101a9ec67ba3b97b045ab10ea55d6234e7378923)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The rebalance behavior for the cluster. When not specified, defaults to 'NO_REBALANCE'. Possible values: 'MODE_UNSPECIFIED', 'NO_REBALANCE', 'AUTO_REBALANCE_ON_SCALE_UP'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#mode GoogleManagedKafkaCluster#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaClusterRebalanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleManagedKafkaClusterRebalanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterRebalanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb219d989031114f02d2b2152b90f3e0045ddd71e65245cb9b13959c23d2a835)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71e4699280c912412d4b68931e4de6966a9439a629217b6926d8bdbc1973db3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleManagedKafkaClusterRebalanceConfig]:
        return typing.cast(typing.Optional[GoogleManagedKafkaClusterRebalanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleManagedKafkaClusterRebalanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036103f08891f2bd0e91098e7745a9c3a5b337aa00f69150eaf549ba56ee9c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleManagedKafkaClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#create GoogleManagedKafkaCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#delete GoogleManagedKafkaCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#update GoogleManagedKafkaCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8d408492ab59c2aac647a19601f9e2540b5e34347eaecb98eec80dcb09fa44)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#create GoogleManagedKafkaCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#delete GoogleManagedKafkaCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_managed_kafka_cluster#update GoogleManagedKafkaCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleManagedKafkaClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleManagedKafkaClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleManagedKafkaCluster.GoogleManagedKafkaClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd30177d1ce089643833678c290526c94dc2601fbf38909c02272b2228a1dfed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6077258ee9a97cd6be7bf32895287428b3238e4ec33adc253a1cb207cc555afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b562e215ea09405ba2c5da94161e59e0d8797b00b168b5b4012229969407aef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b23777ee6c9b43cb2f4d0d4a1b9a81542ecb1de89c94b9b89af460efcd4cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc745b025c45e27a40887d01a62ce2af1f92989378af40e80f9e89ad202a1e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleManagedKafkaCluster",
    "GoogleManagedKafkaClusterCapacityConfig",
    "GoogleManagedKafkaClusterCapacityConfigOutputReference",
    "GoogleManagedKafkaClusterConfig",
    "GoogleManagedKafkaClusterGcpConfig",
    "GoogleManagedKafkaClusterGcpConfigAccessConfig",
    "GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs",
    "GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsList",
    "GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigsOutputReference",
    "GoogleManagedKafkaClusterGcpConfigAccessConfigOutputReference",
    "GoogleManagedKafkaClusterGcpConfigOutputReference",
    "GoogleManagedKafkaClusterRebalanceConfig",
    "GoogleManagedKafkaClusterRebalanceConfigOutputReference",
    "GoogleManagedKafkaClusterTimeouts",
    "GoogleManagedKafkaClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f86710a20b78f4a0bad34217125e088c6c60f94827acb0d22e9b645988835ccf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity_config: typing.Union[GoogleManagedKafkaClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
    cluster_id: builtins.str,
    gcp_config: typing.Union[GoogleManagedKafkaClusterGcpConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    rebalance_config: typing.Optional[typing.Union[GoogleManagedKafkaClusterRebalanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleManagedKafkaClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__64fab6fdb9c23321521f14ad91c60b5cc5efcd52aef123a4c54bb24095f2675b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292e8ed71fb7a0ff0eb2db15b5fe4d5ad681f1f1e64af722cb0776f95de72e34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63750ef8d6b14db9c6d4bb807dba5cca6b07f8c425e755e0b60da4dc10cd0c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e759871bc542dea3aab4382020806157a5788a94faa27f15adf84962609cad6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bb2ea259cc19470b53edbfe4e85ed9227d35e461d0480254134c71fae9438d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363dbf9261e2d79cae9e9cc744cc12003df75de505aa04608431f912843c3fa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce779bad556b981123779e2071415a9e11ff05fc8daf4233a85a2875884c81ff(
    *,
    memory_bytes: builtins.str,
    vcpu_count: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c70cf722beb2384baaa47c2de673dc3f25af129a5fb9a0cc6df3a64fa4f43b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a060f46d3b5345bf910ee9b9fad0d3ea640b2d21411d89d340b636102e6fa4e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b249ef2411d02b78c4b8147d9a1cac9431129e613b228f1636a6349d6d3b9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91787577b59b4721f05bcc854e1c4c015a441a8a8f4cf270942ca8ad159a153(
    value: typing.Optional[GoogleManagedKafkaClusterCapacityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5450167f3fd97d06ce2fbf23a31588f6101a5699da115c81c396d7d502b0e7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity_config: typing.Union[GoogleManagedKafkaClusterCapacityConfig, typing.Dict[builtins.str, typing.Any]],
    cluster_id: builtins.str,
    gcp_config: typing.Union[GoogleManagedKafkaClusterGcpConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    rebalance_config: typing.Optional[typing.Union[GoogleManagedKafkaClusterRebalanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleManagedKafkaClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3f6ee11f65d404eae0430f313e6fa1f66e4ced5a426a09705ece971b65ba89(
    *,
    access_config: typing.Union[GoogleManagedKafkaClusterGcpConfigAccessConfig, typing.Dict[builtins.str, typing.Any]],
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7edca6b6c427edae73c38c2a4e1ac56631bebd3d8d9c9bae501408f4964f41(
    *,
    network_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e368404cb6a0c93b280f21d3cc4b7f50686d1d246ac1f7581f0fe29f874954(
    *,
    subnet: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb7bc0f21bc90314a000926c5ba5fe7046483ac924558069b8d8715f74b80a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe837ced0c6592d6e7fb3592f0a9d18bfbc71a7da7fcd5c46c72a062d255819(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c0656ab1e3045ca6c448895ef13903f30d3ba3b0dc06fc7b0338e05bda7168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3c180324f8bc33974bb6fffa7028859119c4b8f9e20a85f8a6a97e9f21309f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97265c74e0f9018984e73bc41ba942cb66bc4c954caeca502e5bfc62e210f48a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813a566e5a774131f1b00fb73605b1aa085a44c479aa9a42f765904577aa4e1d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6042fff50d069a7137133f25ab4c6d4d7ede332ba3959e96bb6a7494833c4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baec3fd0c0f8b43fe7c71d194acfdc280b07a9132a9b6a6f773dc1012dce9df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57df9fed762cb7dbf940d6157ee5956d545f2a7f783f1945025603ed488e5c20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02db6307523561c5162881da0d2dd7485af04a68db4ffd821a3c0e9242cd1db6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ded9f0f064ebd7056f452ac47772f08933df7ced5a9368b69d53d7ce098596(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleManagedKafkaClusterGcpConfigAccessConfigNetworkConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea508a5c034550d6128386f3b15ba99fc75b75e83f4b0ff5902904f3fa4f7a4(
    value: typing.Optional[GoogleManagedKafkaClusterGcpConfigAccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd7e9f675bc7f0f799f9c4616548395a7bbabc198286bb1d6bb4f342963a49c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7fb8a3b74125bab6725bd83cf3e320355e8fe9d2cb3c13fbc67162165eaf05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b0808c38f872fd721e3efbafeeb671e62e763743f0ae0719bfa37f9d111928(
    value: typing.Optional[GoogleManagedKafkaClusterGcpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6857520b63717fb198f4881101a9ec67ba3b97b045ab10ea55d6234e7378923(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb219d989031114f02d2b2152b90f3e0045ddd71e65245cb9b13959c23d2a835(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e4699280c912412d4b68931e4de6966a9439a629217b6926d8bdbc1973db3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036103f08891f2bd0e91098e7745a9c3a5b337aa00f69150eaf549ba56ee9c29(
    value: typing.Optional[GoogleManagedKafkaClusterRebalanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8d408492ab59c2aac647a19601f9e2540b5e34347eaecb98eec80dcb09fa44(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd30177d1ce089643833678c290526c94dc2601fbf38909c02272b2228a1dfed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6077258ee9a97cd6be7bf32895287428b3238e4ec33adc253a1cb207cc555afc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b562e215ea09405ba2c5da94161e59e0d8797b00b168b5b4012229969407aef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b23777ee6c9b43cb2f4d0d4a1b9a81542ecb1de89c94b9b89af460efcd4cc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc745b025c45e27a40887d01a62ce2af1f92989378af40e80f9e89ad202a1e3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleManagedKafkaClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
