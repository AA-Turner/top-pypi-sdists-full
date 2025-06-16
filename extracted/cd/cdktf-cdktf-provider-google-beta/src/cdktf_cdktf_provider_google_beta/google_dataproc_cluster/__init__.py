r'''
# `google_dataproc_cluster`

Refer to the Terraform Registry for docs: [`google_dataproc_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster).
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


class GoogleDataprocCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster google_dataproc_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        cluster_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        graceful_decommission_timeout: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_cluster_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster google_dataproc_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the cluster, unique within the project and zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#name GoogleDataprocCluster#name}
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cluster_config GoogleDataprocCluster#cluster_config}
        :param graceful_decommission_timeout: The timeout duration which allows graceful decomissioning when you change the number of worker nodes directly through a terraform apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#graceful_decommission_timeout GoogleDataprocCluster#graceful_decommission_timeout}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#id GoogleDataprocCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The list of the labels (key/value pairs) configured on the resource and to be applied to instances in the cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#labels GoogleDataprocCluster#labels}
        :param project: The ID of the project in which the cluster will exist. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#project GoogleDataprocCluster#project}
        :param region: The region in which the cluster and associated nodes will be created in. Defaults to global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#region GoogleDataprocCluster#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#timeouts GoogleDataprocCluster#timeouts}
        :param virtual_cluster_config: virtual_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#virtual_cluster_config GoogleDataprocCluster#virtual_cluster_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6e4cf140d63fdecb4e89d18324b98a20e53ba207b7a2bea5eb6948ff3a5f59)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataprocClusterConfig(
            name=name,
            cluster_config=cluster_config,
            graceful_decommission_timeout=graceful_decommission_timeout,
            id=id,
            labels=labels,
            project=project,
            region=region,
            timeouts=timeouts,
            virtual_cluster_config=virtual_cluster_config,
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
        '''Generates CDKTF code for importing a GoogleDataprocCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataprocCluster to import.
        :param import_from_id: The id of the existing GoogleDataprocCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataprocCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3371dd236143092f68fdb0ccb52dd9310751868564539f180db1f9d58319b1eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClusterConfig")
    def put_cluster_config(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        auxiliary_node_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dataproc_metric_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigDataprocMetricConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gce_cluster_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigGceClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        initialization_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigInitializationAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigLifecycleConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        master_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigMasterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metastore_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible_worker_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        temp_bucket: typing.Optional[builtins.str] = None,
        worker_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#autoscaling_config GoogleDataprocCluster#autoscaling_config}
        :param auxiliary_node_groups: auxiliary_node_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auxiliary_node_groups GoogleDataprocCluster#auxiliary_node_groups}
        :param dataproc_metric_config: dataproc_metric_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metric_config GoogleDataprocCluster#dataproc_metric_config}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#encryption_config GoogleDataprocCluster#encryption_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#endpoint_config GoogleDataprocCluster#endpoint_config}
        :param gce_cluster_config: gce_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gce_cluster_config GoogleDataprocCluster#gce_cluster_config}
        :param initialization_action: initialization_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#initialization_action GoogleDataprocCluster#initialization_action}
        :param lifecycle_config: lifecycle_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#lifecycle_config GoogleDataprocCluster#lifecycle_config}
        :param master_config: master_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#master_config GoogleDataprocCluster#master_config}
        :param metastore_config: metastore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metastore_config GoogleDataprocCluster#metastore_config}
        :param preemptible_worker_config: preemptible_worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptible_worker_config GoogleDataprocCluster#preemptible_worker_config}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#security_config GoogleDataprocCluster#security_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#software_config GoogleDataprocCluster#software_config}
        :param staging_bucket: The Cloud Storage staging bucket used to stage files, such as Hadoop jars, between client machines and the cluster. Note: If you don't explicitly specify a staging_bucket then GCP will auto create / assign one for you. However, you are not guaranteed an auto generated bucket which is solely dedicated to your cluster; it may be shared with other clusters in the same region/zone also choosing to use the auto generation option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#staging_bucket GoogleDataprocCluster#staging_bucket}
        :param temp_bucket: The Cloud Storage temp bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files. Note: If you don't explicitly specify a temp_bucket then GCP will auto create / assign one for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#temp_bucket GoogleDataprocCluster#temp_bucket}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#worker_config GoogleDataprocCluster#worker_config}
        '''
        value = GoogleDataprocClusterClusterConfig(
            autoscaling_config=autoscaling_config,
            auxiliary_node_groups=auxiliary_node_groups,
            dataproc_metric_config=dataproc_metric_config,
            encryption_config=encryption_config,
            endpoint_config=endpoint_config,
            gce_cluster_config=gce_cluster_config,
            initialization_action=initialization_action,
            lifecycle_config=lifecycle_config,
            master_config=master_config,
            metastore_config=metastore_config,
            preemptible_worker_config=preemptible_worker_config,
            security_config=security_config,
            software_config=software_config,
            staging_bucket=staging_bucket,
            temp_bucket=temp_bucket,
            worker_config=worker_config,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#create GoogleDataprocCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#delete GoogleDataprocCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#update GoogleDataprocCluster#update}.
        '''
        value = GoogleDataprocClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualClusterConfig")
    def put_virtual_cluster_config(
        self,
        *,
        auxiliary_services_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes_cluster_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auxiliary_services_config: auxiliary_services_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auxiliary_services_config GoogleDataprocCluster#auxiliary_services_config}
        :param kubernetes_cluster_config: kubernetes_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_cluster_config GoogleDataprocCluster#kubernetes_cluster_config}
        :param staging_bucket: A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#staging_bucket GoogleDataprocCluster#staging_bucket}
        '''
        value = GoogleDataprocClusterVirtualClusterConfig(
            auxiliary_services_config=auxiliary_services_config,
            kubernetes_cluster_config=kubernetes_cluster_config,
            staging_bucket=staging_bucket,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualClusterConfig", [value]))

    @jsii.member(jsii_name="resetClusterConfig")
    def reset_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterConfig", []))

    @jsii.member(jsii_name="resetGracefulDecommissionTimeout")
    def reset_graceful_decommission_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGracefulDecommissionTimeout", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualClusterConfig")
    def reset_virtual_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualClusterConfig", []))

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
    @jsii.member(jsii_name="clusterConfig")
    def cluster_config(self) -> "GoogleDataprocClusterClusterConfigOutputReference":
        return typing.cast("GoogleDataprocClusterClusterConfigOutputReference", jsii.get(self, "clusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataprocClusterTimeoutsOutputReference":
        return typing.cast("GoogleDataprocClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="virtualClusterConfig")
    def virtual_cluster_config(
        self,
    ) -> "GoogleDataprocClusterVirtualClusterConfigOutputReference":
        return typing.cast("GoogleDataprocClusterVirtualClusterConfigOutputReference", jsii.get(self, "virtualClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="clusterConfigInput")
    def cluster_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfig"], jsii.get(self, "clusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gracefulDecommissionTimeoutInput")
    def graceful_decommission_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gracefulDecommissionTimeoutInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualClusterConfigInput")
    def virtual_cluster_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfig"], jsii.get(self, "virtualClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gracefulDecommissionTimeout")
    def graceful_decommission_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gracefulDecommissionTimeout"))

    @graceful_decommission_timeout.setter
    def graceful_decommission_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf4d03eb6a2a8dd900d01fdd49a2f17630b8d54c46990f0c7a67defb4cb5004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gracefulDecommissionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0281ff26b47c2f3672c4d0738579af6ffc5d5689147df89b0b90590cb387ff04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c62c4f010bfcb4da124830d10aae5aa087322e0ba70a87289aedf83eb926154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59be1e0232ef9034dcb7e7892f757533fd0839e778ddec3bb7e645af0f608a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3e8efdc692fff9521f0c1c6eb791862ed41aca9ad932e5dcec76c1a20455d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f61c75254bc37de97d515b7d59338e7a3531c9a53c4da894bd4330c549ad868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_config": "autoscalingConfig",
        "auxiliary_node_groups": "auxiliaryNodeGroups",
        "dataproc_metric_config": "dataprocMetricConfig",
        "encryption_config": "encryptionConfig",
        "endpoint_config": "endpointConfig",
        "gce_cluster_config": "gceClusterConfig",
        "initialization_action": "initializationAction",
        "lifecycle_config": "lifecycleConfig",
        "master_config": "masterConfig",
        "metastore_config": "metastoreConfig",
        "preemptible_worker_config": "preemptibleWorkerConfig",
        "security_config": "securityConfig",
        "software_config": "softwareConfig",
        "staging_bucket": "stagingBucket",
        "temp_bucket": "tempBucket",
        "worker_config": "workerConfig",
    },
)
class GoogleDataprocClusterClusterConfig:
    def __init__(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        auxiliary_node_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dataproc_metric_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigDataprocMetricConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gce_cluster_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigGceClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        initialization_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigInitializationAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigLifecycleConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        master_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigMasterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metastore_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible_worker_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        temp_bucket: typing.Optional[builtins.str] = None,
        worker_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#autoscaling_config GoogleDataprocCluster#autoscaling_config}
        :param auxiliary_node_groups: auxiliary_node_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auxiliary_node_groups GoogleDataprocCluster#auxiliary_node_groups}
        :param dataproc_metric_config: dataproc_metric_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metric_config GoogleDataprocCluster#dataproc_metric_config}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#encryption_config GoogleDataprocCluster#encryption_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#endpoint_config GoogleDataprocCluster#endpoint_config}
        :param gce_cluster_config: gce_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gce_cluster_config GoogleDataprocCluster#gce_cluster_config}
        :param initialization_action: initialization_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#initialization_action GoogleDataprocCluster#initialization_action}
        :param lifecycle_config: lifecycle_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#lifecycle_config GoogleDataprocCluster#lifecycle_config}
        :param master_config: master_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#master_config GoogleDataprocCluster#master_config}
        :param metastore_config: metastore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metastore_config GoogleDataprocCluster#metastore_config}
        :param preemptible_worker_config: preemptible_worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptible_worker_config GoogleDataprocCluster#preemptible_worker_config}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#security_config GoogleDataprocCluster#security_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#software_config GoogleDataprocCluster#software_config}
        :param staging_bucket: The Cloud Storage staging bucket used to stage files, such as Hadoop jars, between client machines and the cluster. Note: If you don't explicitly specify a staging_bucket then GCP will auto create / assign one for you. However, you are not guaranteed an auto generated bucket which is solely dedicated to your cluster; it may be shared with other clusters in the same region/zone also choosing to use the auto generation option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#staging_bucket GoogleDataprocCluster#staging_bucket}
        :param temp_bucket: The Cloud Storage temp bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files. Note: If you don't explicitly specify a temp_bucket then GCP will auto create / assign one for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#temp_bucket GoogleDataprocCluster#temp_bucket}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#worker_config GoogleDataprocCluster#worker_config}
        '''
        if isinstance(autoscaling_config, dict):
            autoscaling_config = GoogleDataprocClusterClusterConfigAutoscalingConfig(**autoscaling_config)
        if isinstance(dataproc_metric_config, dict):
            dataproc_metric_config = GoogleDataprocClusterClusterConfigDataprocMetricConfig(**dataproc_metric_config)
        if isinstance(encryption_config, dict):
            encryption_config = GoogleDataprocClusterClusterConfigEncryptionConfig(**encryption_config)
        if isinstance(endpoint_config, dict):
            endpoint_config = GoogleDataprocClusterClusterConfigEndpointConfig(**endpoint_config)
        if isinstance(gce_cluster_config, dict):
            gce_cluster_config = GoogleDataprocClusterClusterConfigGceClusterConfig(**gce_cluster_config)
        if isinstance(lifecycle_config, dict):
            lifecycle_config = GoogleDataprocClusterClusterConfigLifecycleConfig(**lifecycle_config)
        if isinstance(master_config, dict):
            master_config = GoogleDataprocClusterClusterConfigMasterConfig(**master_config)
        if isinstance(metastore_config, dict):
            metastore_config = GoogleDataprocClusterClusterConfigMetastoreConfig(**metastore_config)
        if isinstance(preemptible_worker_config, dict):
            preemptible_worker_config = GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig(**preemptible_worker_config)
        if isinstance(security_config, dict):
            security_config = GoogleDataprocClusterClusterConfigSecurityConfig(**security_config)
        if isinstance(software_config, dict):
            software_config = GoogleDataprocClusterClusterConfigSoftwareConfig(**software_config)
        if isinstance(worker_config, dict):
            worker_config = GoogleDataprocClusterClusterConfigWorkerConfig(**worker_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5455b5e5505a3c5e687b4a20b2d8cb9083c4f82282e901dd941a884910644ddc)
            check_type(argname="argument autoscaling_config", value=autoscaling_config, expected_type=type_hints["autoscaling_config"])
            check_type(argname="argument auxiliary_node_groups", value=auxiliary_node_groups, expected_type=type_hints["auxiliary_node_groups"])
            check_type(argname="argument dataproc_metric_config", value=dataproc_metric_config, expected_type=type_hints["dataproc_metric_config"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument endpoint_config", value=endpoint_config, expected_type=type_hints["endpoint_config"])
            check_type(argname="argument gce_cluster_config", value=gce_cluster_config, expected_type=type_hints["gce_cluster_config"])
            check_type(argname="argument initialization_action", value=initialization_action, expected_type=type_hints["initialization_action"])
            check_type(argname="argument lifecycle_config", value=lifecycle_config, expected_type=type_hints["lifecycle_config"])
            check_type(argname="argument master_config", value=master_config, expected_type=type_hints["master_config"])
            check_type(argname="argument metastore_config", value=metastore_config, expected_type=type_hints["metastore_config"])
            check_type(argname="argument preemptible_worker_config", value=preemptible_worker_config, expected_type=type_hints["preemptible_worker_config"])
            check_type(argname="argument security_config", value=security_config, expected_type=type_hints["security_config"])
            check_type(argname="argument software_config", value=software_config, expected_type=type_hints["software_config"])
            check_type(argname="argument staging_bucket", value=staging_bucket, expected_type=type_hints["staging_bucket"])
            check_type(argname="argument temp_bucket", value=temp_bucket, expected_type=type_hints["temp_bucket"])
            check_type(argname="argument worker_config", value=worker_config, expected_type=type_hints["worker_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscaling_config is not None:
            self._values["autoscaling_config"] = autoscaling_config
        if auxiliary_node_groups is not None:
            self._values["auxiliary_node_groups"] = auxiliary_node_groups
        if dataproc_metric_config is not None:
            self._values["dataproc_metric_config"] = dataproc_metric_config
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if endpoint_config is not None:
            self._values["endpoint_config"] = endpoint_config
        if gce_cluster_config is not None:
            self._values["gce_cluster_config"] = gce_cluster_config
        if initialization_action is not None:
            self._values["initialization_action"] = initialization_action
        if lifecycle_config is not None:
            self._values["lifecycle_config"] = lifecycle_config
        if master_config is not None:
            self._values["master_config"] = master_config
        if metastore_config is not None:
            self._values["metastore_config"] = metastore_config
        if preemptible_worker_config is not None:
            self._values["preemptible_worker_config"] = preemptible_worker_config
        if security_config is not None:
            self._values["security_config"] = security_config
        if software_config is not None:
            self._values["software_config"] = software_config
        if staging_bucket is not None:
            self._values["staging_bucket"] = staging_bucket
        if temp_bucket is not None:
            self._values["temp_bucket"] = temp_bucket
        if worker_config is not None:
            self._values["worker_config"] = worker_config

    @builtins.property
    def autoscaling_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigAutoscalingConfig"]:
        '''autoscaling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#autoscaling_config GoogleDataprocCluster#autoscaling_config}
        '''
        result = self._values.get("autoscaling_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigAutoscalingConfig"], result)

    @builtins.property
    def auxiliary_node_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups"]]]:
        '''auxiliary_node_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auxiliary_node_groups GoogleDataprocCluster#auxiliary_node_groups}
        '''
        result = self._values.get("auxiliary_node_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups"]]], result)

    @builtins.property
    def dataproc_metric_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigDataprocMetricConfig"]:
        '''dataproc_metric_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metric_config GoogleDataprocCluster#dataproc_metric_config}
        '''
        result = self._values.get("dataproc_metric_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigDataprocMetricConfig"], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#encryption_config GoogleDataprocCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigEncryptionConfig"], result)

    @builtins.property
    def endpoint_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigEndpointConfig"]:
        '''endpoint_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#endpoint_config GoogleDataprocCluster#endpoint_config}
        '''
        result = self._values.get("endpoint_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigEndpointConfig"], result)

    @builtins.property
    def gce_cluster_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfig"]:
        '''gce_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gce_cluster_config GoogleDataprocCluster#gce_cluster_config}
        '''
        result = self._values.get("gce_cluster_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfig"], result)

    @builtins.property
    def initialization_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigInitializationAction"]]]:
        '''initialization_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#initialization_action GoogleDataprocCluster#initialization_action}
        '''
        result = self._values.get("initialization_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigInitializationAction"]]], result)

    @builtins.property
    def lifecycle_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigLifecycleConfig"]:
        '''lifecycle_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#lifecycle_config GoogleDataprocCluster#lifecycle_config}
        '''
        result = self._values.get("lifecycle_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigLifecycleConfig"], result)

    @builtins.property
    def master_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigMasterConfig"]:
        '''master_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#master_config GoogleDataprocCluster#master_config}
        '''
        result = self._values.get("master_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigMasterConfig"], result)

    @builtins.property
    def metastore_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigMetastoreConfig"]:
        '''metastore_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metastore_config GoogleDataprocCluster#metastore_config}
        '''
        result = self._values.get("metastore_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigMetastoreConfig"], result)

    @builtins.property
    def preemptible_worker_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig"]:
        '''preemptible_worker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptible_worker_config GoogleDataprocCluster#preemptible_worker_config}
        '''
        result = self._values.get("preemptible_worker_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig"], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#security_config GoogleDataprocCluster#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigSecurityConfig"], result)

    @builtins.property
    def software_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#software_config GoogleDataprocCluster#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigSoftwareConfig"], result)

    @builtins.property
    def staging_bucket(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage staging bucket used to stage files, such as Hadoop jars, between client machines and the cluster.

        Note: If you don't explicitly specify a staging_bucket then GCP will auto create / assign one for you. However, you are not guaranteed an auto generated bucket which is solely dedicated to your cluster; it may be shared with other clusters in the same region/zone also choosing to use the auto generation option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#staging_bucket GoogleDataprocCluster#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_bucket(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage temp bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files.

        Note: If you don't explicitly specify a temp_bucket then GCP will auto create / assign one for you.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#temp_bucket GoogleDataprocCluster#temp_bucket}
        '''
        result = self._values.get("temp_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigWorkerConfig"]:
        '''worker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#worker_config GoogleDataprocCluster#worker_config}
        '''
        result = self._values.get("worker_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigWorkerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAutoscalingConfig",
    jsii_struct_bases=[],
    name_mapping={"policy_uri": "policyUri"},
)
class GoogleDataprocClusterClusterConfigAutoscalingConfig:
    def __init__(self, *, policy_uri: builtins.str) -> None:
        '''
        :param policy_uri: The autoscaling policy used by the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#policy_uri GoogleDataprocCluster#policy_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0842bb7135b9511d6a7afca06c372f50adbe0f80104e7bcfda830ed9807e258)
            check_type(argname="argument policy_uri", value=policy_uri, expected_type=type_hints["policy_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_uri": policy_uri,
        }

    @builtins.property
    def policy_uri(self) -> builtins.str:
        '''The autoscaling policy used by the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#policy_uri GoogleDataprocCluster#policy_uri}
        '''
        result = self._values.get("policy_uri")
        assert result is not None, "Required property 'policy_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigAutoscalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigAutoscalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAutoscalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe862aa86d13b0581957b211d9b05e1c6c0d87c67f322847d7ab1e4a93a0271a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="policyUriInput")
    def policy_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="policyUri")
    def policy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyUri"))

    @policy_uri.setter
    def policy_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1916d93c94aa9cb4e475d2d4b0cc52b0d8b05a221669e8e1ccffe049b52ba10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigAutoscalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigAutoscalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a19fd7b8184a414d1f34536c6655f79a6157377ee62cd7418a86fa948c1317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups",
    jsii_struct_bases=[],
    name_mapping={"node_group": "nodeGroup", "node_group_id": "nodeGroupId"},
)
class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups:
    def __init__(
        self,
        *,
        node_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup", typing.Dict[builtins.str, typing.Any]]]],
        node_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param node_group: node_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group GoogleDataprocCluster#node_group}
        :param node_group_id: A node group ID. Generated if not specified. The ID must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of from 3 to 33 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_id GoogleDataprocCluster#node_group_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9555aabd3f7d925b25ebddd748bb92ff81e5fb9c52c254570f1a7b6e668f6063)
            check_type(argname="argument node_group", value=node_group, expected_type=type_hints["node_group"])
            check_type(argname="argument node_group_id", value=node_group_id, expected_type=type_hints["node_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_group": node_group,
        }
        if node_group_id is not None:
            self._values["node_group_id"] = node_group_id

    @builtins.property
    def node_group(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup"]]:
        '''node_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group GoogleDataprocCluster#node_group}
        '''
        result = self._values.get("node_group")
        assert result is not None, "Required property 'node_group' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup"]], result)

    @builtins.property
    def node_group_id(self) -> typing.Optional[builtins.str]:
        '''A node group ID.

        Generated if not specified. The ID must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). Cannot begin or end with underscore or hyphen. Must consist of from 3 to 33 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_id GoogleDataprocCluster#node_group_id}
        '''
        result = self._values.get("node_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e31970e47d962157980cb4c82a6cb71f94234af6103a74ef56e18da7cb00ac68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f4eb757aaeded050c7a739946c2f12dd06ec4f31495e49b04e20b07cc934c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61dade7b6fc726ea16d852cc27260eb45184d9c59a9af71a3f0233fa7d28637a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bb7f20bc321b491591a0badc1ea19eb13016aa4b40e2076a74312e6b2f403a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b7a0ce1769cadb7790b6cf32b2ad15845fc98f5862d57068395a4df4bd33518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2254350dadbf4ca0a08d1310d303d3ee8b4dcdb95fb71ffd5bc3e35f5572145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup",
    jsii_struct_bases=[],
    name_mapping={"roles": "roles", "node_group_config": "nodeGroupConfig"},
)
class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup:
    def __init__(
        self,
        *,
        roles: typing.Sequence[builtins.str],
        node_group_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param roles: Node group roles. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#roles GoogleDataprocCluster#roles}
        :param node_group_config: node_group_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_config GoogleDataprocCluster#node_group_config}
        '''
        if isinstance(node_group_config, dict):
            node_group_config = GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig(**node_group_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36056f1fd973b1cbc227b5b3a30e28bd9d3f3cf790c252181b7472323dd4deb2)
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument node_group_config", value=node_group_config, expected_type=type_hints["node_group_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "roles": roles,
        }
        if node_group_config is not None:
            self._values["node_group_config"] = node_group_config

    @builtins.property
    def roles(self) -> typing.List[builtins.str]:
        '''Node group roles.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#roles GoogleDataprocCluster#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def node_group_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig"]:
        '''node_group_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_config GoogleDataprocCluster#node_group_config}
        '''
        result = self._values.get("node_group_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff0b0bfb9e19c682d42d65e432498d244e965eccc6dc1ea9506414523f55070)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73c0cde0bd57863ca86000ac94c1bc06f24e2c7e191395f9c2a88dec5906649)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22407fab5cd98aad78fd99b08a144245133facd11d22ba1638debc54c61e1c18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73efb6a85294467f51b0434e3fffa351bec594f8472ed5cd4070c999eb39155)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d28b1528fa3e32684de743e56c0f83c7671bb7ec2f60a16cfb06c663a618b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31d86b34a89a65a5d304684c4199dcc1ca85e4a9a15641042d6fa1b92483868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "disk_config": "diskConfig",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "num_instances": "numInstances",
    },
)
class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the auxiliary node group. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        :param num_instances: Specifies the number of auxiliary nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        if isinstance(disk_config, dict):
            disk_config = GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b526dc5755977cd734ad72b1f5baef4dd30c54885d6fcef69392a01581448a7)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if num_instances is not None:
            self._values["num_instances"] = num_instances

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators"]]], result)

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig"], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Google Compute Engine machine type to create for the master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''The name of a minimum generation of CPU family for the auxiliary node group.

        If not specified, GCP will default to a predetermined computed value for each zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of auxiliary nodes to create. If not specified, GCP will default to a predetermined computed value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: jsii.Number,
        accelerator_type: builtins.str,
    ) -> None:
        '''
        :param accelerator_count: The number of the accelerator cards of this type exposed to this instance. Often restricted to one of 1, 2, 4, or 8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_count GoogleDataprocCluster#accelerator_count}
        :param accelerator_type: The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_type GoogleDataprocCluster#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9587f3d804e6d350bb51862043aed63fe83e2864877100325125e21f2b06d46)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator_count": accelerator_count,
            "accelerator_type": accelerator_type,
        }

    @builtins.property
    def accelerator_count(self) -> jsii.Number:
        '''The number of the accelerator cards of this type exposed to this instance.

        Often restricted to one of 1, 2, 4, or 8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_count GoogleDataprocCluster#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        assert result is not None, "Required property 'accelerator_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def accelerator_type(self) -> builtins.str:
        '''The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_type GoogleDataprocCluster#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        assert result is not None, "Required property 'accelerator_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6642b77313a6e23de8e7660abc795d30b0ea4d97c3afda0d45b9033755189f9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f55f59c18938398ff38795558ef60d35780304b0d72edf228e8d6632f22ba0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed814afa6b0bf4306ecadef978f1c98fe0352f115ba88228e618e2103e5a0d70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc38761416ffe21163ed81daec986d4d6c726d7231723321e4cb499c5c3cfac9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b31c86c203c714ebfa1edc06d4cb37d723f89402a18980a3904a7bddc6edb2b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b24fdd2d7e820264d58a50cedb293df00c7bf7ff8ce6e4941cc90f854da523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f20b1c953a49fe75750fa008f93ab5309476bf052ec45d17bca7e1422b5b81d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac982484ae90cd5df8147abc3dccee4e9889dd054683ed849bc7d3f9ad05e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba79d5ed3ee9cbaeb127c6ea3b671cfab854243c485412cccf6e292fc0e5acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13514fd9115fe3dbd94fe347909b623f19492ce388c6939e5be483c73850288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "local_ssd_interface": "localSsdInterface",
        "num_local_ssds": "numLocalSsds",
    },
)
class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        local_ssd_interface: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        :param local_ssd_interface: Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39fbd8cd7fa8e5dcaada8bf49ed1d2f9e005cfcb0a4da08c790c0af80191dfe1)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument local_ssd_interface", value=local_ssd_interface, expected_type=type_hints["local_ssd_interface"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if local_ssd_interface is not None:
            self._values["local_ssd_interface"] = local_ssd_interface
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the primary disk attached to each node, specified in GB.

        The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_interface(self) -> typing.Optional[builtins.str]:
        '''Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        '''
        result = self._values.get("local_ssd_interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f66d7bb4076645d9ba9fbe53a2bd14232f672b9d636c7cccbe288e7d0e60240)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetLocalSsdInterface")
    def reset_local_ssd_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdInterface", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdInterfaceInput")
    def local_ssd_interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localSsdInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392579c52177929975ee73722416a31d96ad220004455e4edb61707579f66918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43b7a0d452dd143e95b658de41fbb51d0335f9543e02d2c132eede3f3e3fd48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdInterface")
    def local_ssd_interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSsdInterface"))

    @local_ssd_interface.setter
    def local_ssd_interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac78aee3ec00d42bef47129b9a0d9bc972116f32a43be6ab8a55ec25d82349a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdInterface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400c010b85ce69f14a14d45a7bf4ad95b04636d5231f83a52f3fa0b7d7dfeb7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8034b9c77202d44269a7fcdb5358f7678abc881ebca8a3941179c6eb79f0c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edd0eeebc4240a4d4c14991869245d6b6c96ca39fe3a7d22aed90bbee4e98a7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d7f2975e9e0f2aeceea1d78276e12d989226661e7aa981e6cd88a57a65f805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        local_ssd_interface: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        :param local_ssd_interface: Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        value = GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            local_ssd_interface=local_ssd_interface,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(
        self,
    ) -> GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsList:
        return typing.cast(GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab83c33a49d5cadabc3eca5b08f42cf5eb45ac2f9c48b57a94df90ff07dda042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d951ec133eee1a49203cf6af9001b16fbc11fad89f23461c424d76a8eeaf1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23dd0ac8ad27a4616e150811519e4300f5ab27dcf37c36b80c8035e7529d50d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc37b1a0301fc3ad4a20e4a05c70a0033db58b6ebd6d9e097d8c2ef8ac6c6c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f60ed5ac7832f05e90678d4c79cf062225279c4ba3af4405e6115d2cfdd6d3df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNodeGroupConfig")
    def put_node_group_config(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the auxiliary node group. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        :param num_instances: Specifies the number of auxiliary nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        value = GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig(
            accelerators=accelerators,
            disk_config=disk_config,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            num_instances=num_instances,
        )

        return typing.cast(None, jsii.invoke(self, "putNodeGroupConfig", [value]))

    @jsii.member(jsii_name="resetNodeGroupConfig")
    def reset_node_group_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeGroupConfig", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupConfig")
    def node_group_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigOutputReference, jsii.get(self, "nodeGroupConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupConfigInput")
    def node_group_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig], jsii.get(self, "nodeGroupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d9c67341fd07c057bb2a8ec0607c0c3571ad988868d49a6a8544eb1525b447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40d0cf9b7d0dc4e5ab177c879e366e153ea85e5bc1581110d0544337bc48b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa89dc63ddb336d8c6dfee7399f5b19356e9cbd80c4745c905d7205301cb462)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNodeGroup")
    def put_node_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6a677e39a30e21754cadc345bd662454da0c81794ba20d79917f2d9db7b399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeGroup", [value]))

    @jsii.member(jsii_name="resetNodeGroupId")
    def reset_node_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeGroupId", []))

    @builtins.property
    @jsii.member(jsii_name="nodeGroup")
    def node_group(
        self,
    ) -> GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupList:
        return typing.cast(GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupList, jsii.get(self, "nodeGroup"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupIdInput")
    def node_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupInput")
    def node_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]]], jsii.get(self, "nodeGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupId")
    def node_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeGroupId"))

    @node_group_id.setter
    def node_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2391cdf97f2fbd13d2409bee1a1f81a37d496911d99991379fc0298e7c5b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ceb021dc339ac1d8f2294d4676f87062c5706fabc08545990bfe4d8e219a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigDataprocMetricConfig",
    jsii_struct_bases=[],
    name_mapping={"metrics": "metrics"},
)
class GoogleDataprocClusterClusterConfigDataprocMetricConfig:
    def __init__(
        self,
        *,
        metrics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param metrics: metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metrics GoogleDataprocCluster#metrics}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beda7e73a7e7953d341d5245943e8658a42d80ca8850c2526ec5978c7e920baa)
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metrics": metrics,
        }

    @builtins.property
    def metrics(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics"]]:
        '''metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metrics GoogleDataprocCluster#metrics}
        '''
        result = self._values.get("metrics")
        assert result is not None, "Required property 'metrics' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigDataprocMetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "metric_source": "metricSource",
        "metric_overrides": "metricOverrides",
    },
)
class GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics:
    def __init__(
        self,
        *,
        metric_source: builtins.str,
        metric_overrides: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metric_source: A source for the collection of Dataproc OSS metrics (see [available OSS metrics] (https://cloud.google.com//dataproc/docs/guides/monitoring#available_oss_metrics)). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metric_source GoogleDataprocCluster#metric_source}
        :param metric_overrides: Specify one or more [available OSS metrics] (https://cloud.google.com/dataproc/docs/guides/monitoring#available_oss_metrics) to collect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metric_overrides GoogleDataprocCluster#metric_overrides}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb076274218e76a7bd1eb9f4ea18ec9bc6128a8f16c55ee67e3ac5c36a02023)
            check_type(argname="argument metric_source", value=metric_source, expected_type=type_hints["metric_source"])
            check_type(argname="argument metric_overrides", value=metric_overrides, expected_type=type_hints["metric_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_source": metric_source,
        }
        if metric_overrides is not None:
            self._values["metric_overrides"] = metric_overrides

    @builtins.property
    def metric_source(self) -> builtins.str:
        '''A source for the collection of Dataproc OSS metrics (see [available OSS metrics] (https://cloud.google.com//dataproc/docs/guides/monitoring#available_oss_metrics)).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metric_source GoogleDataprocCluster#metric_source}
        '''
        result = self._values.get("metric_source")
        assert result is not None, "Required property 'metric_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_overrides(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify one or more [available OSS metrics] (https://cloud.google.com/dataproc/docs/guides/monitoring#available_oss_metrics) to collect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metric_overrides GoogleDataprocCluster#metric_overrides}
        '''
        result = self._values.get("metric_overrides")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__879abfc10172e97c0b4f5eee853bbf2dc40ec94818bdfb0ab58ec99926720561)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__952998dc2dda240606244b89eb72e26aa60a1e9e5e9f33878027f1c25601882b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d4810541f678315fc18b5dfb754609ec369f1747fb531aa6875b26f1554521)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a1fac31636c09900ee50e7854b0f2ba3c6cdcf0790898013f8b73736504c02b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b36f832d08852c873298dd4fe1113b2f9877b9b71beab787b3ada8c0e6dd772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3c7006ca0667717a2e1b8a7359cfc291253cc682a2b456eff1ac0a9f1cc636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd098b69f6705b5c0fc4a2c4f8174dd424a55d7d1a1e4456be9e29448f665a57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMetricOverrides")
    def reset_metric_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricOverrides", []))

    @builtins.property
    @jsii.member(jsii_name="metricOverridesInput")
    def metric_overrides_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metricOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="metricSourceInput")
    def metric_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="metricOverrides")
    def metric_overrides(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metricOverrides"))

    @metric_overrides.setter
    def metric_overrides(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323c04236a172d24e1d46ba669857968232eafdd1921870ebe627bd93f7151ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricSource")
    def metric_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricSource"))

    @metric_source.setter
    def metric_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef45b982c9baf1ac9a085384517ce98feadb3455434fdea212d89af4c6f6196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87ad857dcbfe129d84f2bdafd545bccae427ba90b14d9c4e815c98fe7a3c811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigDataprocMetricConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigDataprocMetricConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__217f77ed23856ba5bdf5640cfd293f94ef3a0e80e1eb45205145770f3d5007cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetrics")
    def put_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54d62a72eb1635083dade34cd48c8f689f61024064b7c104b58e654bbbdf707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetrics", [value]))

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(
        self,
    ) -> GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsList:
        return typing.cast(GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsList, jsii.get(self, "metrics"))

    @builtins.property
    @jsii.member(jsii_name="metricsInput")
    def metrics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]]], jsii.get(self, "metricsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigDataprocMetricConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigDataprocMetricConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigDataprocMetricConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4335b9fbc6b46fe9e5c96e9d741a311a9f0f98fc968735f2c9afb1e05350a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleDataprocClusterClusterConfigEncryptionConfig:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The Cloud KMS key name to use for PD disk encryption for all instances in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kms_key_name GoogleDataprocCluster#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676c718b8b0e5e011114b79974fcb123736dc2f5c1559d49ad446521fb8e1c76)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The Cloud KMS key name to use for PD disk encryption for all instances in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kms_key_name GoogleDataprocCluster#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffdc0e41103820ddb6e30978916929737a23ccc0c20cb4194355e60efeb7507c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5034f5094066576ac56abedc086e7a7fb804435ce613c639120a314d29480304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a4257f5aca3122ef66595eeb2d950dc0e076fce45a2ab1036083ecd5ab4a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigEndpointConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_http_port_access": "enableHttpPortAccess"},
)
class GoogleDataprocClusterClusterConfigEndpointConfig:
    def __init__(
        self,
        *,
        enable_http_port_access: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_http_port_access: The flag to enable http access to specific ports on the cluster from external sources (aka Component Gateway). Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_http_port_access GoogleDataprocCluster#enable_http_port_access}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fad9874a24bdf9f76cc11ba1886754b38a0410b3e51052a8a1b5254ca4077f)
            check_type(argname="argument enable_http_port_access", value=enable_http_port_access, expected_type=type_hints["enable_http_port_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_http_port_access": enable_http_port_access,
        }

    @builtins.property
    def enable_http_port_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''The flag to enable http access to specific ports on the cluster from external sources (aka Component Gateway).

        Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_http_port_access GoogleDataprocCluster#enable_http_port_access}
        '''
        result = self._values.get("enable_http_port_access")
        assert result is not None, "Required property 'enable_http_port_access' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigEndpointConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigEndpointConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffe8dcfb5865a512d9842eec3e6c2a44d9be44e3726d248275b7f2f1a3fc34d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="httpPorts")
    def http_ports(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "httpPorts"))

    @builtins.property
    @jsii.member(jsii_name="enableHttpPortAccessInput")
    def enable_http_port_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHttpPortAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHttpPortAccess")
    def enable_http_port_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHttpPortAccess"))

    @enable_http_port_access.setter
    def enable_http_port_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81971726b44da773dab0bf75f59d833b984e9355b76876ab2547d00d1abc63dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHttpPortAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigEndpointConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigEndpointConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigEndpointConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930fea8e43930f9f12a3d90950fad3a3d495fd1917b28691090b96e8e7037305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidential_instance_config": "confidentialInstanceConfig",
        "internal_ip_only": "internalIpOnly",
        "metadata": "metadata",
        "network": "network",
        "node_group_affinity": "nodeGroupAffinity",
        "reservation_affinity": "reservationAffinity",
        "service_account": "serviceAccount",
        "service_account_scopes": "serviceAccountScopes",
        "shielded_instance_config": "shieldedInstanceConfig",
        "subnetwork": "subnetwork",
        "tags": "tags",
        "zone": "zone",
    },
)
class GoogleDataprocClusterClusterConfigGceClusterConfig:
    def __init__(
        self,
        *,
        confidential_instance_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        node_group_affinity: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        reservation_affinity: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#confidential_instance_config GoogleDataprocCluster#confidential_instance_config}
        :param internal_ip_only: By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance. If set to true, all instances in the cluster will only have internal IP addresses. Note: Private Google Access (also known as privateIpGoogleAccess) must be enabled on the subnetwork that the cluster will be launched in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#internal_ip_only GoogleDataprocCluster#internal_ip_only}
        :param metadata: A map of the Compute Engine metadata entries to add to all instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metadata GoogleDataprocCluster#metadata}
        :param network: The name or self_link of the Google Compute Engine network to the cluster will be part of. Conflicts with subnetwork. If neither is specified, this defaults to the "default" network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#network GoogleDataprocCluster#network}
        :param node_group_affinity: node_group_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_affinity GoogleDataprocCluster#node_group_affinity}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#reservation_affinity GoogleDataprocCluster#reservation_affinity}
        :param service_account: The service account to be used by the Node VMs. If not specified, the "default" service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#service_account GoogleDataprocCluster#service_account}
        :param service_account_scopes: The set of Google API scopes to be made available on all of the node VMs under the service_account specified. These can be either FQDNs, or scope aliases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#service_account_scopes GoogleDataprocCluster#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#shielded_instance_config GoogleDataprocCluster#shielded_instance_config}
        :param subnetwork: The name or self_link of the Google Compute Engine subnetwork the cluster will be part of. Conflicts with network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#subnetwork GoogleDataprocCluster#subnetwork}
        :param tags: The list of instance tags applied to instances in the cluster. Tags are used to identify valid sources or targets for network firewalls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#tags GoogleDataprocCluster#tags}
        :param zone: The GCP zone where your data is stored and used (i.e. where the master and the worker nodes will be created in). If region is set to 'global' (default) then zone is mandatory, otherwise GCP is able to make use of Auto Zone Placement to determine this automatically for you. Note: This setting additionally determines and restricts which computing resources are available for use with other configs such as cluster_config.master_config.machine_type and cluster_config.worker_config.machine_type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#zone GoogleDataprocCluster#zone}
        '''
        if isinstance(confidential_instance_config, dict):
            confidential_instance_config = GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig(**confidential_instance_config)
        if isinstance(node_group_affinity, dict):
            node_group_affinity = GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity(**node_group_affinity)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity(**reservation_affinity)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig(**shielded_instance_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ccd4ece8a87a6193f5561296c82551b8d2adcb68d917aa36d84e98da3b3501)
            check_type(argname="argument confidential_instance_config", value=confidential_instance_config, expected_type=type_hints["confidential_instance_config"])
            check_type(argname="argument internal_ip_only", value=internal_ip_only, expected_type=type_hints["internal_ip_only"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument node_group_affinity", value=node_group_affinity, expected_type=type_hints["node_group_affinity"])
            check_type(argname="argument reservation_affinity", value=reservation_affinity, expected_type=type_hints["reservation_affinity"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument service_account_scopes", value=service_account_scopes, expected_type=type_hints["service_account_scopes"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidential_instance_config is not None:
            self._values["confidential_instance_config"] = confidential_instance_config
        if internal_ip_only is not None:
            self._values["internal_ip_only"] = internal_ip_only
        if metadata is not None:
            self._values["metadata"] = metadata
        if network is not None:
            self._values["network"] = network
        if node_group_affinity is not None:
            self._values["node_group_affinity"] = node_group_affinity
        if reservation_affinity is not None:
            self._values["reservation_affinity"] = reservation_affinity
        if service_account is not None:
            self._values["service_account"] = service_account
        if service_account_scopes is not None:
            self._values["service_account_scopes"] = service_account_scopes
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if tags is not None:
            self._values["tags"] = tags
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def confidential_instance_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig"]:
        '''confidential_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#confidential_instance_config GoogleDataprocCluster#confidential_instance_config}
        '''
        result = self._values.get("confidential_instance_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig"], result)

    @builtins.property
    def internal_ip_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance.

        If set to true, all instances in the cluster will only have internal IP addresses. Note: Private Google Access (also known as privateIpGoogleAccess) must be enabled on the subnetwork that the cluster will be launched in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#internal_ip_only GoogleDataprocCluster#internal_ip_only}
        '''
        result = self._values.get("internal_ip_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of the Compute Engine metadata entries to add to all instances.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metadata GoogleDataprocCluster#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the Google Compute Engine network to the cluster will be part of.

        Conflicts with subnetwork. If neither is specified, this defaults to the "default" network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#network GoogleDataprocCluster#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_group_affinity(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity"]:
        '''node_group_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_affinity GoogleDataprocCluster#node_group_affinity}
        '''
        result = self._values.get("node_group_affinity")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity"], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#reservation_affinity GoogleDataprocCluster#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account to be used by the Node VMs. If not specified, the "default" service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#service_account GoogleDataprocCluster#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of Google API scopes to be made available on all of the node VMs under the service_account specified.

        These can be either FQDNs, or scope aliases.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#service_account_scopes GoogleDataprocCluster#service_account_scopes}
        '''
        result = self._values.get("service_account_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#shielded_instance_config GoogleDataprocCluster#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig"], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the Google Compute Engine subnetwork the cluster will be part of. Conflicts with network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#subnetwork GoogleDataprocCluster#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of instance tags applied to instances in the cluster.

        Tags are used to identify valid sources or targets for network firewalls.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#tags GoogleDataprocCluster#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The GCP zone where your data is stored and used (i.e. where the master and the worker nodes will be created in). If region is set to 'global' (default) then zone is mandatory, otherwise GCP is able to make use of Auto Zone Placement to determine this automatically for you. Note: This setting additionally determines and restricts which computing resources are available for use with other configs such as cluster_config.master_config.machine_type and cluster_config.worker_config.machine_type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#zone GoogleDataprocCluster#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigGceClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_confidential_compute": "enableConfidentialCompute"},
)
class GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig:
    def __init__(
        self,
        *,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_confidential_compute GoogleDataprocCluster#enable_confidential_compute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ce69ce1015383b9c2a4480a15f11301ec34b4f6e8594506e3f1015de2991cc)
            check_type(argname="argument enable_confidential_compute", value=enable_confidential_compute, expected_type=type_hints["enable_confidential_compute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_confidential_compute is not None:
            self._values["enable_confidential_compute"] = enable_confidential_compute

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance should have confidential compute enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_confidential_compute GoogleDataprocCluster#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc4930dbc49903c8b63a734c1b6aeaef41d28f2b87d9d195de952207abcbce90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableConfidentialCompute")
    def reset_enable_confidential_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConfidentialCompute", []))

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialComputeInput")
    def enable_confidential_compute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConfidentialComputeInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialCompute")
    def enable_confidential_compute(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConfidentialCompute"))

    @enable_confidential_compute.setter
    def enable_confidential_compute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3051644e63375122cc3402544ceb38d9549e6ee11f95ab0aa60aea76f0d3808a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174cee6af711039fd09f5cb4524f865b2e2bac7e65ba8b08b318a8cc3ffc35fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity",
    jsii_struct_bases=[],
    name_mapping={"node_group_uri": "nodeGroupUri"},
)
class GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity:
    def __init__(self, *, node_group_uri: builtins.str) -> None:
        '''
        :param node_group_uri: The URI of a sole-tenant that the cluster will be created on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_uri GoogleDataprocCluster#node_group_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bbe914cfc2551f3cfb597e375e22af3b6e5c836c46c7f3ac87786c38723bb9)
            check_type(argname="argument node_group_uri", value=node_group_uri, expected_type=type_hints["node_group_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_group_uri": node_group_uri,
        }

    @builtins.property
    def node_group_uri(self) -> builtins.str:
        '''The URI of a sole-tenant that the cluster will be created on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_uri GoogleDataprocCluster#node_group_uri}
        '''
        result = self._values.get("node_group_uri")
        assert result is not None, "Required property 'node_group_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b79bed028fe364b1677c8547b3ee4445042b1e1de50b6f415c06583c2de48bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nodeGroupUriInput")
    def node_group_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeGroupUriInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupUri")
    def node_group_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeGroupUri"))

    @node_group_uri.setter
    def node_group_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7598dea0411f20c75bdc7e3e9335ffb22496c5976c30dc2952f69d23b0aecad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeGroupUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e99098bb8f2564e137ffdb48fba54de96510ae14005f3cc7ad5c836d460f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigGceClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a483140551b56a1fece847224af3e2b01656726b3462fcb4ce37a43adbf8e948)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfidentialInstanceConfig")
    def put_confidential_instance_config(
        self,
        *,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_confidential_compute GoogleDataprocCluster#enable_confidential_compute}
        '''
        value = GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig(
            enable_confidential_compute=enable_confidential_compute
        )

        return typing.cast(None, jsii.invoke(self, "putConfidentialInstanceConfig", [value]))

    @jsii.member(jsii_name="putNodeGroupAffinity")
    def put_node_group_affinity(self, *, node_group_uri: builtins.str) -> None:
        '''
        :param node_group_uri: The URI of a sole-tenant that the cluster will be created on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_uri GoogleDataprocCluster#node_group_uri}
        '''
        value = GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity(
            node_group_uri=node_group_uri
        )

        return typing.cast(None, jsii.invoke(self, "putNodeGroupAffinity", [value]))

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        consume_reservation_type: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: Type of reservation to consume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#consume_reservation_type GoogleDataprocCluster#consume_reservation_type}
        :param key: Corresponds to the label key of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#key GoogleDataprocCluster#key}
        :param values: Corresponds to the label values of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#values GoogleDataprocCluster#values}
        '''
        value = GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity(
            consume_reservation_type=consume_reservation_type, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putReservationAffinity", [value]))

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether instances have integrity monitoring enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_integrity_monitoring GoogleDataprocCluster#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether instances have Secure Boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_secure_boot GoogleDataprocCluster#enable_secure_boot}
        :param enable_vtpm: Defines whether instances have the vTPM enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_vtpm GoogleDataprocCluster#enable_vtpm}
        '''
        value = GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
            enable_vtpm=enable_vtpm,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="resetConfidentialInstanceConfig")
    def reset_confidential_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialInstanceConfig", []))

    @jsii.member(jsii_name="resetInternalIpOnly")
    def reset_internal_ip_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIpOnly", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNodeGroupAffinity")
    def reset_node_group_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeGroupAffinity", []))

    @jsii.member(jsii_name="resetReservationAffinity")
    def reset_reservation_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationAffinity", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetServiceAccountScopes")
    def reset_service_account_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountScopes", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfig")
    def confidential_instance_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfigOutputReference, jsii.get(self, "confidentialInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupAffinity")
    def node_group_affinity(
        self,
    ) -> GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinityOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinityOutputReference, jsii.get(self, "nodeGroupAffinity"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinityOutputReference":
        return typing.cast("GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference":
        return typing.cast("GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfigInput")
    def confidential_instance_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig], jsii.get(self, "confidentialInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpOnlyInput")
    def internal_ip_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalIpOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeGroupAffinityInput")
    def node_group_affinity_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity], jsii.get(self, "nodeGroupAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityInput")
    def reservation_affinity_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopesInput")
    def service_account_scopes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceAccountScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpOnly")
    def internal_ip_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internalIpOnly"))

    @internal_ip_only.setter
    def internal_ip_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381bfc30b65d7cf70621ad3d3fcea5e88b43e37121433d8cf8939f43ba8b7a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d588f18d83318d5fa213b7b0007bc87c49f004467012cb1c584b4f6782720750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5220794514b9e30f78363bee8bd1fb743dbba431aa062da941198c2023b5b65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a423b28514605964b8ab95a7739c70e8b654da4e1061caf0a3887502b3040835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopes")
    def service_account_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAccountScopes"))

    @service_account_scopes.setter
    def service_account_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dcc3b3868dff7f4a426486dbdd0b0aead679fdeb7d719a332e819199606d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75871a7edef071e36acd075b693c66f989ea62e343f3d42ec0f7236648de1171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea82b6f95bc33492a74d9b91f5d18229672a8590374f186bcd1570a9a6e7047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ddf5cb7d19293ca8f2009ed14a93a9f18012c772be6e4f0c0e34e0f2606611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d7cca7910e08bde9d93c075c5c5242af0111875fa31df4c54ffcf19f4546cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={
        "consume_reservation_type": "consumeReservationType",
        "key": "key",
        "values": "values",
    },
)
class GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity:
    def __init__(
        self,
        *,
        consume_reservation_type: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: Type of reservation to consume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#consume_reservation_type GoogleDataprocCluster#consume_reservation_type}
        :param key: Corresponds to the label key of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#key GoogleDataprocCluster#key}
        :param values: Corresponds to the label values of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#values GoogleDataprocCluster#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa86bb9aa1d29241c91d9e5b79e02ca4944d5b9cb1868cb1f6fcd57ba4291d4e)
            check_type(argname="argument consume_reservation_type", value=consume_reservation_type, expected_type=type_hints["consume_reservation_type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consume_reservation_type is not None:
            self._values["consume_reservation_type"] = consume_reservation_type
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def consume_reservation_type(self) -> typing.Optional[builtins.str]:
        '''Type of reservation to consume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#consume_reservation_type GoogleDataprocCluster#consume_reservation_type}
        '''
        result = self._values.get("consume_reservation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Corresponds to the label key of reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#key GoogleDataprocCluster#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Corresponds to the label values of reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#values GoogleDataprocCluster#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed6ad63051e7e23ddd986602994c8661ec4ce97f0c30b5e22bf0d5948725efc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConsumeReservationType")
    def reset_consume_reservation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumeReservationType", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="consumeReservationTypeInput")
    def consume_reservation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumeReservationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="consumeReservationType")
    def consume_reservation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumeReservationType"))

    @consume_reservation_type.setter
    def consume_reservation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f33c00b2579254da3885c4b9fc41552429353f6f71724c7ab3942b3b0599f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumeReservationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6080081f4f7fb1a91e3cbea5c5f214ebce19ed535f01cfd28025ab1c9c50b7be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1345d7e02325495d9e4a9947af71e29baffd567e80c8ff4fa3b7fb0470f3fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b61bcc31efbdc206952e75b579c5b66040352ce324601037eaa2583b50768e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether instances have integrity monitoring enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_integrity_monitoring GoogleDataprocCluster#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether instances have Secure Boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_secure_boot GoogleDataprocCluster#enable_secure_boot}
        :param enable_vtpm: Defines whether instances have the vTPM enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_vtpm GoogleDataprocCluster#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28884a542ef5b7f8d3bf2f07e0be3de9bbdecffee8270f470c6c0e1435d939eb)
            check_type(argname="argument enable_integrity_monitoring", value=enable_integrity_monitoring, expected_type=type_hints["enable_integrity_monitoring"])
            check_type(argname="argument enable_secure_boot", value=enable_secure_boot, expected_type=type_hints["enable_secure_boot"])
            check_type(argname="argument enable_vtpm", value=enable_vtpm, expected_type=type_hints["enable_vtpm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_integrity_monitoring is not None:
            self._values["enable_integrity_monitoring"] = enable_integrity_monitoring
        if enable_secure_boot is not None:
            self._values["enable_secure_boot"] = enable_secure_boot
        if enable_vtpm is not None:
            self._values["enable_vtpm"] = enable_vtpm

    @builtins.property
    def enable_integrity_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether instances have integrity monitoring enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_integrity_monitoring GoogleDataprocCluster#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether instances have Secure Boot enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_secure_boot GoogleDataprocCluster#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether instances have the vTPM enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_vtpm GoogleDataprocCluster#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e089c67a0d4b49a3c7422afaaabef32ee31944162e1b923f7aaf49aa5e1238f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableIntegrityMonitoring")
    def reset_enable_integrity_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIntegrityMonitoring", []))

    @jsii.member(jsii_name="resetEnableSecureBoot")
    def reset_enable_secure_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSecureBoot", []))

    @jsii.member(jsii_name="resetEnableVtpm")
    def reset_enable_vtpm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableVtpm", []))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoringInput")
    def enable_integrity_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIntegrityMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSecureBootInput")
    def enable_secure_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSecureBootInput"))

    @builtins.property
    @jsii.member(jsii_name="enableVtpmInput")
    def enable_vtpm_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableVtpmInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoring")
    def enable_integrity_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIntegrityMonitoring"))

    @enable_integrity_monitoring.setter
    def enable_integrity_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe804983b682aa2b1b4f0dc391e0f311b26d76482f839a214009462ba30bcd01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIntegrityMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSecureBoot")
    def enable_secure_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSecureBoot"))

    @enable_secure_boot.setter
    def enable_secure_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afba53be4e2e67f7825fff40f95bc368f02a8f405b969cac50550b824076fe0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableVtpm")
    def enable_vtpm(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableVtpm"))

    @enable_vtpm.setter
    def enable_vtpm(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12df3567229927ddff78e208cf738d099ae01e268230fa897ce4f25de0c386e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9b6474b43ae159f1cb4db8858130d9dc46832418ee4320c40ed2dcfd1a2641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigInitializationAction",
    jsii_struct_bases=[],
    name_mapping={"script": "script", "timeout_sec": "timeoutSec"},
)
class GoogleDataprocClusterClusterConfigInitializationAction:
    def __init__(
        self,
        *,
        script: builtins.str,
        timeout_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param script: The script to be executed during initialization of the cluster. The script must be a GCS file with a gs:// prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#script GoogleDataprocCluster#script}
        :param timeout_sec: The maximum duration (in seconds) which script is allowed to take to execute its action. GCP will default to a predetermined computed value if not set (currently 300). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#timeout_sec GoogleDataprocCluster#timeout_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659b33e16c14ef406ada41a0041df9c37b8d50246d4c9d2cf6ec24f6ba455ca6)
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument timeout_sec", value=timeout_sec, expected_type=type_hints["timeout_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script": script,
        }
        if timeout_sec is not None:
            self._values["timeout_sec"] = timeout_sec

    @builtins.property
    def script(self) -> builtins.str:
        '''The script to be executed during initialization of the cluster.

        The script must be a GCS file with a gs:// prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#script GoogleDataprocCluster#script}
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''The maximum duration (in seconds) which script is allowed to take to execute its action.

        GCP will default to a predetermined computed value if not set (currently 300).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#timeout_sec GoogleDataprocCluster#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigInitializationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigInitializationActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigInitializationActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb66e145e1f08df64eaf70d447ff4bc72d6253054a8f82cefab6f708afbccb68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigInitializationActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588bc9f76c15593bddebc4e3a8cbae97355d37c798f1a8d4106eea9ecf64f889)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigInitializationActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c2f755172ceadb0967a9c8ec707a837aa0bd6696d435dea33c10ab05b37407)
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
            type_hints = typing.get_type_hints(_typecheckingstub__041c7c1c5db028538665f67ccc5ec92e0ea575770df2f60bece7560e857f4811)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8856854cf53e9b545d6588b50d32aeab7330b6f912690bdb6cf52971c8979c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigInitializationAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigInitializationAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigInitializationAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a8df7b1b026df7398c5f802c1afc2d53c9a5aabc1a035cfba0eff58a3c92b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigInitializationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigInitializationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ec71f17038c6b2b64c2f6d63556b67782d6442ef3f6d14b21d5e8c85f6e7c26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTimeoutSec")
    def reset_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSec", []))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d31d42b7cad9841212a8260262b8526f661212793561bb88c8b7d56c9a78092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b500e9197f76f5d3f141fd5a21e385291c0af8eabff66b4cf44716a68b02985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigInitializationAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigInitializationAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigInitializationAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d923af4379022cd3c4ad50746875115f5aed945c33afd074d338bfaa5d32971d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigLifecycleConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auto_delete_time": "autoDeleteTime",
        "idle_delete_ttl": "idleDeleteTtl",
    },
)
class GoogleDataprocClusterClusterConfigLifecycleConfig:
    def __init__(
        self,
        *,
        auto_delete_time: typing.Optional[builtins.str] = None,
        idle_delete_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete_time: The time when cluster will be auto-deleted. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auto_delete_time GoogleDataprocCluster#auto_delete_time}
        :param idle_delete_ttl: The duration to keep the cluster alive while idling (no jobs running). After this TTL, the cluster will be deleted. Valid range: [10m, 14d]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#idle_delete_ttl GoogleDataprocCluster#idle_delete_ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc090b9c9c305aafa91be95aa1ee32350111197c3d79a358c888530da02014c)
            check_type(argname="argument auto_delete_time", value=auto_delete_time, expected_type=type_hints["auto_delete_time"])
            check_type(argname="argument idle_delete_ttl", value=idle_delete_ttl, expected_type=type_hints["idle_delete_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_delete_time is not None:
            self._values["auto_delete_time"] = auto_delete_time
        if idle_delete_ttl is not None:
            self._values["idle_delete_ttl"] = idle_delete_ttl

    @builtins.property
    def auto_delete_time(self) -> typing.Optional[builtins.str]:
        '''The time when cluster will be auto-deleted. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auto_delete_time GoogleDataprocCluster#auto_delete_time}
        '''
        result = self._values.get("auto_delete_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_delete_ttl(self) -> typing.Optional[builtins.str]:
        '''The duration to keep the cluster alive while idling (no jobs running).

        After this TTL, the cluster will be deleted. Valid range: [10m, 14d].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#idle_delete_ttl GoogleDataprocCluster#idle_delete_ttl}
        '''
        result = self._values.get("idle_delete_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigLifecycleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigLifecycleConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigLifecycleConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9393c89cd620d8d0738ab0ec23482bbcadbe3ab982ce5c9af4c823d4e39257e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutoDeleteTime")
    def reset_auto_delete_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeleteTime", []))

    @jsii.member(jsii_name="resetIdleDeleteTtl")
    def reset_idle_delete_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleDeleteTtl", []))

    @builtins.property
    @jsii.member(jsii_name="idleStartTime")
    def idle_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleStartTime"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteTimeInput")
    def auto_delete_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDeleteTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idleDeleteTtlInput")
    def idle_delete_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idleDeleteTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteTime")
    def auto_delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDeleteTime"))

    @auto_delete_time.setter
    def auto_delete_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe519ae923c6eb15b5aa73fa2acd0f5251ebba0676cae81c6b40741ecb3948b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeleteTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleDeleteTtl")
    def idle_delete_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleDeleteTtl"))

    @idle_delete_ttl.setter
    def idle_delete_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76db7a1d5f300b036a70fc3026655464910e3a3d02f5ba2e1b933cf6d310835f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleDeleteTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigLifecycleConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigLifecycleConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigLifecycleConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2a710e3bf92eff50e037a0e6aa731539db42eac1ebf021e11f96409b995877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMasterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "disk_config": "diskConfig",
        "image_uri": "imageUri",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "num_instances": "numInstances",
    },
)
class GoogleDataprocClusterClusterConfigMasterConfig:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigMasterConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigMasterConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        :param image_uri: The URI for the image to use for this master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_uri GoogleDataprocCluster#image_uri}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the master. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        :param num_instances: Specifies the number of master nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        if isinstance(disk_config, dict):
            disk_config = GoogleDataprocClusterClusterConfigMasterConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e196828a7c9e00bd778f8a343e1681548ff5c68d180c14af0a0b1fc6a63520)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if num_instances is not None:
            self._values["num_instances"] = num_instances

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigMasterConfigAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigMasterConfigAccelerators"]]], result)

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigMasterConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigMasterConfigDiskConfig"], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''The URI for the image to use for this master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_uri GoogleDataprocCluster#image_uri}
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Google Compute Engine machine type to create for the master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''The name of a minimum generation of CPU family for the master.

        If not specified, GCP will default to a predetermined computed value for each zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of master nodes to create. If not specified, GCP will default to a predetermined computed value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigMasterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMasterConfigAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class GoogleDataprocClusterClusterConfigMasterConfigAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: jsii.Number,
        accelerator_type: builtins.str,
    ) -> None:
        '''
        :param accelerator_count: The number of the accelerator cards of this type exposed to this instance. Often restricted to one of 1, 2, 4, or 8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_count GoogleDataprocCluster#accelerator_count}
        :param accelerator_type: The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_type GoogleDataprocCluster#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768ad4ae9b7ff6aa47d8aa51b1154db39c2f635f1342ff0757ddb16cef8ad72d)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator_count": accelerator_count,
            "accelerator_type": accelerator_type,
        }

    @builtins.property
    def accelerator_count(self) -> jsii.Number:
        '''The number of the accelerator cards of this type exposed to this instance.

        Often restricted to one of 1, 2, 4, or 8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_count GoogleDataprocCluster#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        assert result is not None, "Required property 'accelerator_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def accelerator_type(self) -> builtins.str:
        '''The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_type GoogleDataprocCluster#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        assert result is not None, "Required property 'accelerator_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigMasterConfigAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a897c7500967fc4d5cb3975b18e8857264dc9b6dbe3625e9e874ea9628b3d0ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253dad92f8c5f1e975d64038754b4c7d99dbfacd371b7ee87f1bb2834b371c22)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9abbf2aa332989e1510181b171f15befd89e98ce9f8b06f4e8a94355e21ef66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d43071ccef4d6a567950c95ce332aadb3a6c9a026247aac0a968b309c5f6527b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a5f24d2df668722e9cdd038454f5cf6d6f96241284fd5b89f954bfaf347f980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigMasterConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigMasterConfigAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigMasterConfigAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14373c33777131a54827a0c9cf46ccd802f4ce47dbc6f4f9ac21e13e7a06dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d240c179f6cd65343f604a85324b88b3f159da0474c7ff759ceed5775a356d3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c3aa89e40f6e38a81801be49e11e1483b3743890038075e28751279f3fc8eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10754e7ef56eb230233078851af5f1064c540214432077606ab2ea1d9363bcec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigMasterConfigAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigMasterConfigAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigMasterConfigAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e851337853f2db6d0918b4eba1ff1525e397753170f50f740d75ab043ee5ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMasterConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "local_ssd_interface": "localSsdInterface",
        "num_local_ssds": "numLocalSsds",
    },
)
class GoogleDataprocClusterClusterConfigMasterConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        local_ssd_interface: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        :param local_ssd_interface: Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83ee1cb361f3123c1551d4e665df599b78de9d308954194c484d91e971f97ed)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument local_ssd_interface", value=local_ssd_interface, expected_type=type_hints["local_ssd_interface"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if local_ssd_interface is not None:
            self._values["local_ssd_interface"] = local_ssd_interface
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the primary disk attached to each node, specified in GB.

        The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_interface(self) -> typing.Optional[builtins.str]:
        '''Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        '''
        result = self._values.get("local_ssd_interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigMasterConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigMasterConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMasterConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc564a723307527677a76e99bc513c10d08749de0d5532899a85521f76ef493a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetLocalSsdInterface")
    def reset_local_ssd_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdInterface", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdInterfaceInput")
    def local_ssd_interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localSsdInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466675fbf16c3d7bb5c8934112402d40ca5bc3cc3265b514c235f2b290e98160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0aca0577b9ce17858796790a303c2890b945f8d0b45b7922b11e87351f78984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdInterface")
    def local_ssd_interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSsdInterface"))

    @local_ssd_interface.setter
    def local_ssd_interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532e542ae3b8c2c5bd84bf43ad387a9ac84d694f6efa720651bb18b9105d9788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdInterface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b48b4f0ce80efd4065914cf257353bfe0d5bab3e3e455f749ab62338644b259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigMasterConfigDiskConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigMasterConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigMasterConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88f05883f47d43d41cfc8fb6031d3fa355c9c3adc66097daa516c7f3f0632f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigMasterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMasterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06cbd02100dd8d8db8d92e5ca5bc87f3a1b5f2a52327b6a322fd71c148e34072)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862590ff032949c781ff519081489967dce0494eadd50569e206bb65f19e10a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        local_ssd_interface: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        :param local_ssd_interface: Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        value = GoogleDataprocClusterClusterConfigMasterConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            local_ssd_interface=local_ssd_interface,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetImageUri")
    def reset_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageUri", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(
        self,
    ) -> GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsList:
        return typing.cast(GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigMasterConfigDiskConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigMasterConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigMasterConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigMasterConfigAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigMasterConfigDiskConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigMasterConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6186420810dd196962e217770fc288f25bb384eaa055108c92ea0960ed69c843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bccd98bc1f216ba633b53595692c60c6b397c8021797875af2395677715dba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f02c72e6cd51479556d6b5ac257472d9e437f8fd2e343702d4a0931eec0196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac2d526b1db82b25941fa87ea4f0a4278f8043938096ba22746fe70ab945479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigMasterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigMasterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigMasterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d3be3837f9580f1ac44e887ed9dda817eae11016eee5674547a0c3af212bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMetastoreConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_metastore_service": "dataprocMetastoreService"},
)
class GoogleDataprocClusterClusterConfigMetastoreConfig:
    def __init__(self, *, dataproc_metastore_service: builtins.str) -> None:
        '''
        :param dataproc_metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metastore_service GoogleDataprocCluster#dataproc_metastore_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af6f1f2562942a28441a143249b0de5b201011d54781ddd71511f7ac4bcfab7)
            check_type(argname="argument dataproc_metastore_service", value=dataproc_metastore_service, expected_type=type_hints["dataproc_metastore_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataproc_metastore_service": dataproc_metastore_service,
        }

    @builtins.property
    def dataproc_metastore_service(self) -> builtins.str:
        '''Resource name of an existing Dataproc Metastore service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metastore_service GoogleDataprocCluster#dataproc_metastore_service}
        '''
        result = self._values.get("dataproc_metastore_service")
        assert result is not None, "Required property 'dataproc_metastore_service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigMetastoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigMetastoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigMetastoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83eb0195b53ef372615c887a8f1988d9d7575e3a9fb013a92aef47487ff47286)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreServiceInput")
    def dataproc_metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocMetastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreService")
    def dataproc_metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocMetastoreService"))

    @dataproc_metastore_service.setter
    def dataproc_metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598ab8004081cf9fbbea8e318f56e158228e51d156048890693737ca85fd4f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocMetastoreService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigMetastoreConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigMetastoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigMetastoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd2dd6f5dabd7f8b76d96de789e6fbb017ae5fc7f0e76d09ca19eeb11f109a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__886115185668638aae8095aed624911717ca01583ce0494265d3f64be5d0b376)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingConfig")
    def put_autoscaling_config(self, *, policy_uri: builtins.str) -> None:
        '''
        :param policy_uri: The autoscaling policy used by the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#policy_uri GoogleDataprocCluster#policy_uri}
        '''
        value = GoogleDataprocClusterClusterConfigAutoscalingConfig(
            policy_uri=policy_uri
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscalingConfig", [value]))

    @jsii.member(jsii_name="putAuxiliaryNodeGroups")
    def put_auxiliary_node_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f28ea5517fbab250f16746181f4f7b4762ad5bfcca83340524b7c190f7a615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuxiliaryNodeGroups", [value]))

    @jsii.member(jsii_name="putDataprocMetricConfig")
    def put_dataproc_metric_config(
        self,
        *,
        metrics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param metrics: metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metrics GoogleDataprocCluster#metrics}
        '''
        value = GoogleDataprocClusterClusterConfigDataprocMetricConfig(metrics=metrics)

        return typing.cast(None, jsii.invoke(self, "putDataprocMetricConfig", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The Cloud KMS key name to use for PD disk encryption for all instances in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kms_key_name GoogleDataprocCluster#kms_key_name}
        '''
        value = GoogleDataprocClusterClusterConfigEncryptionConfig(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putEndpointConfig")
    def put_endpoint_config(
        self,
        *,
        enable_http_port_access: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_http_port_access: The flag to enable http access to specific ports on the cluster from external sources (aka Component Gateway). Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_http_port_access GoogleDataprocCluster#enable_http_port_access}
        '''
        value = GoogleDataprocClusterClusterConfigEndpointConfig(
            enable_http_port_access=enable_http_port_access
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointConfig", [value]))

    @jsii.member(jsii_name="putGceClusterConfig")
    def put_gce_cluster_config(
        self,
        *,
        confidential_instance_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        node_group_affinity: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
        reservation_affinity: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#confidential_instance_config GoogleDataprocCluster#confidential_instance_config}
        :param internal_ip_only: By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance. If set to true, all instances in the cluster will only have internal IP addresses. Note: Private Google Access (also known as privateIpGoogleAccess) must be enabled on the subnetwork that the cluster will be launched in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#internal_ip_only GoogleDataprocCluster#internal_ip_only}
        :param metadata: A map of the Compute Engine metadata entries to add to all instances. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metadata GoogleDataprocCluster#metadata}
        :param network: The name or self_link of the Google Compute Engine network to the cluster will be part of. Conflicts with subnetwork. If neither is specified, this defaults to the "default" network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#network GoogleDataprocCluster#network}
        :param node_group_affinity: node_group_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_group_affinity GoogleDataprocCluster#node_group_affinity}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#reservation_affinity GoogleDataprocCluster#reservation_affinity}
        :param service_account: The service account to be used by the Node VMs. If not specified, the "default" service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#service_account GoogleDataprocCluster#service_account}
        :param service_account_scopes: The set of Google API scopes to be made available on all of the node VMs under the service_account specified. These can be either FQDNs, or scope aliases. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#service_account_scopes GoogleDataprocCluster#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#shielded_instance_config GoogleDataprocCluster#shielded_instance_config}
        :param subnetwork: The name or self_link of the Google Compute Engine subnetwork the cluster will be part of. Conflicts with network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#subnetwork GoogleDataprocCluster#subnetwork}
        :param tags: The list of instance tags applied to instances in the cluster. Tags are used to identify valid sources or targets for network firewalls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#tags GoogleDataprocCluster#tags}
        :param zone: The GCP zone where your data is stored and used (i.e. where the master and the worker nodes will be created in). If region is set to 'global' (default) then zone is mandatory, otherwise GCP is able to make use of Auto Zone Placement to determine this automatically for you. Note: This setting additionally determines and restricts which computing resources are available for use with other configs such as cluster_config.master_config.machine_type and cluster_config.worker_config.machine_type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#zone GoogleDataprocCluster#zone}
        '''
        value = GoogleDataprocClusterClusterConfigGceClusterConfig(
            confidential_instance_config=confidential_instance_config,
            internal_ip_only=internal_ip_only,
            metadata=metadata,
            network=network,
            node_group_affinity=node_group_affinity,
            reservation_affinity=reservation_affinity,
            service_account=service_account,
            service_account_scopes=service_account_scopes,
            shielded_instance_config=shielded_instance_config,
            subnetwork=subnetwork,
            tags=tags,
            zone=zone,
        )

        return typing.cast(None, jsii.invoke(self, "putGceClusterConfig", [value]))

    @jsii.member(jsii_name="putInitializationAction")
    def put_initialization_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigInitializationAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ed339f3b9ebb7727f3f2bcca681c70eb7d4f9bbb56676798503c8364fa9b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitializationAction", [value]))

    @jsii.member(jsii_name="putLifecycleConfig")
    def put_lifecycle_config(
        self,
        *,
        auto_delete_time: typing.Optional[builtins.str] = None,
        idle_delete_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete_time: The time when cluster will be auto-deleted. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auto_delete_time GoogleDataprocCluster#auto_delete_time}
        :param idle_delete_ttl: The duration to keep the cluster alive while idling (no jobs running). After this TTL, the cluster will be deleted. Valid range: [10m, 14d]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#idle_delete_ttl GoogleDataprocCluster#idle_delete_ttl}
        '''
        value = GoogleDataprocClusterClusterConfigLifecycleConfig(
            auto_delete_time=auto_delete_time, idle_delete_ttl=idle_delete_ttl
        )

        return typing.cast(None, jsii.invoke(self, "putLifecycleConfig", [value]))

    @jsii.member(jsii_name="putMasterConfig")
    def put_master_config(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigMasterConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        :param image_uri: The URI for the image to use for this master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_uri GoogleDataprocCluster#image_uri}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the master. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        :param num_instances: Specifies the number of master nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        value = GoogleDataprocClusterClusterConfigMasterConfig(
            accelerators=accelerators,
            disk_config=disk_config,
            image_uri=image_uri,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            num_instances=num_instances,
        )

        return typing.cast(None, jsii.invoke(self, "putMasterConfig", [value]))

    @jsii.member(jsii_name="putMetastoreConfig")
    def put_metastore_config(self, *, dataproc_metastore_service: builtins.str) -> None:
        '''
        :param dataproc_metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metastore_service GoogleDataprocCluster#dataproc_metastore_service}
        '''
        value = GoogleDataprocClusterClusterConfigMetastoreConfig(
            dataproc_metastore_service=dataproc_metastore_service
        )

        return typing.cast(None, jsii.invoke(self, "putMetastoreConfig", [value]))

    @jsii.member(jsii_name="putPreemptibleWorkerConfig")
    def put_preemptible_worker_config(
        self,
        *,
        disk_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_flexibility_policy: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        :param instance_flexibility_policy: instance_flexibility_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#instance_flexibility_policy GoogleDataprocCluster#instance_flexibility_policy}
        :param num_instances: Specifies the number of preemptible nodes to create. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        :param preemptibility: Specifies the preemptibility of the secondary nodes. Defaults to PREEMPTIBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptibility GoogleDataprocCluster#preemptibility}
        '''
        value = GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig(
            disk_config=disk_config,
            instance_flexibility_policy=instance_flexibility_policy,
            num_instances=num_instances,
            preemptibility=preemptibility,
        )

        return typing.cast(None, jsii.invoke(self, "putPreemptibleWorkerConfig", [value]))

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        kerberos_config: typing.Union["GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kerberos_config GoogleDataprocCluster#kerberos_config}
        '''
        value = GoogleDataprocClusterClusterConfigSecurityConfig(
            kerberos_config=kerberos_config
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putSoftwareConfig")
    def put_software_config(
        self,
        *,
        image_version: typing.Optional[builtins.str] = None,
        optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
        override_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param image_version: The Cloud Dataproc image version to use for the cluster - this controls the sets of software versions installed onto the nodes when you create clusters. If not specified, defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_version GoogleDataprocCluster#image_version}
        :param optional_components: The set of optional components to activate on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#optional_components GoogleDataprocCluster#optional_components}
        :param override_properties: A list of override and additional properties (key/value pairs) used to modify various aspects of the common configuration files used when creating a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#override_properties GoogleDataprocCluster#override_properties}
        '''
        value = GoogleDataprocClusterClusterConfigSoftwareConfig(
            image_version=image_version,
            optional_components=optional_components,
            override_properties=override_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putSoftwareConfig", [value]))

    @jsii.member(jsii_name="putWorkerConfig")
    def put_worker_config(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigWorkerConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        min_num_instances: typing.Optional[jsii.Number] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        :param image_uri: The URI for the image to use for this master/worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_uri GoogleDataprocCluster#image_uri}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master/worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the master/worker. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        :param min_num_instances: The minimum number of primary worker instances to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_num_instances GoogleDataprocCluster#min_num_instances}
        :param num_instances: Specifies the number of worker nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        value = GoogleDataprocClusterClusterConfigWorkerConfig(
            accelerators=accelerators,
            disk_config=disk_config,
            image_uri=image_uri,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            min_num_instances=min_num_instances,
            num_instances=num_instances,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerConfig", [value]))

    @jsii.member(jsii_name="resetAutoscalingConfig")
    def reset_autoscaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingConfig", []))

    @jsii.member(jsii_name="resetAuxiliaryNodeGroups")
    def reset_auxiliary_node_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuxiliaryNodeGroups", []))

    @jsii.member(jsii_name="resetDataprocMetricConfig")
    def reset_dataproc_metric_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocMetricConfig", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetEndpointConfig")
    def reset_endpoint_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointConfig", []))

    @jsii.member(jsii_name="resetGceClusterConfig")
    def reset_gce_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGceClusterConfig", []))

    @jsii.member(jsii_name="resetInitializationAction")
    def reset_initialization_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializationAction", []))

    @jsii.member(jsii_name="resetLifecycleConfig")
    def reset_lifecycle_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfig", []))

    @jsii.member(jsii_name="resetMasterConfig")
    def reset_master_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterConfig", []))

    @jsii.member(jsii_name="resetMetastoreConfig")
    def reset_metastore_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreConfig", []))

    @jsii.member(jsii_name="resetPreemptibleWorkerConfig")
    def reset_preemptible_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptibleWorkerConfig", []))

    @jsii.member(jsii_name="resetSecurityConfig")
    def reset_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfig", []))

    @jsii.member(jsii_name="resetSoftwareConfig")
    def reset_software_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftwareConfig", []))

    @jsii.member(jsii_name="resetStagingBucket")
    def reset_staging_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingBucket", []))

    @jsii.member(jsii_name="resetTempBucket")
    def reset_temp_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTempBucket", []))

    @jsii.member(jsii_name="resetWorkerConfig")
    def reset_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfig")
    def autoscaling_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigAutoscalingConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigAutoscalingConfigOutputReference, jsii.get(self, "autoscalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryNodeGroups")
    def auxiliary_node_groups(
        self,
    ) -> GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsList:
        return typing.cast(GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsList, jsii.get(self, "auxiliaryNodeGroups"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetricConfig")
    def dataproc_metric_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigDataprocMetricConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigDataprocMetricConfigOutputReference, jsii.get(self, "dataprocMetricConfig"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigEncryptionConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfig")
    def endpoint_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigEndpointConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigEndpointConfigOutputReference, jsii.get(self, "endpointConfig"))

    @builtins.property
    @jsii.member(jsii_name="gceClusterConfig")
    def gce_cluster_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigGceClusterConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigGceClusterConfigOutputReference, jsii.get(self, "gceClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="initializationAction")
    def initialization_action(
        self,
    ) -> GoogleDataprocClusterClusterConfigInitializationActionList:
        return typing.cast(GoogleDataprocClusterClusterConfigInitializationActionList, jsii.get(self, "initializationAction"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfig")
    def lifecycle_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigLifecycleConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigLifecycleConfigOutputReference, jsii.get(self, "lifecycleConfig"))

    @builtins.property
    @jsii.member(jsii_name="masterConfig")
    def master_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigMasterConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigMasterConfigOutputReference, jsii.get(self, "masterConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreConfig")
    def metastore_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigMetastoreConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigMetastoreConfigOutputReference, jsii.get(self, "metastoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="preemptibleWorkerConfig")
    def preemptible_worker_config(
        self,
    ) -> "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference":
        return typing.cast("GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference", jsii.get(self, "preemptibleWorkerConfig"))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "GoogleDataprocClusterClusterConfigSecurityConfigOutputReference":
        return typing.cast("GoogleDataprocClusterClusterConfigSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(
        self,
    ) -> "GoogleDataprocClusterClusterConfigSoftwareConfigOutputReference":
        return typing.cast("GoogleDataprocClusterClusterConfigSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="workerConfig")
    def worker_config(
        self,
    ) -> "GoogleDataprocClusterClusterConfigWorkerConfigOutputReference":
        return typing.cast("GoogleDataprocClusterClusterConfigWorkerConfigOutputReference", jsii.get(self, "workerConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfigInput")
    def autoscaling_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigAutoscalingConfig], jsii.get(self, "autoscalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryNodeGroupsInput")
    def auxiliary_node_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]]], jsii.get(self, "auxiliaryNodeGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetricConfigInput")
    def dataproc_metric_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigDataprocMetricConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigDataprocMetricConfig], jsii.get(self, "dataprocMetricConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigInput")
    def endpoint_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigEndpointConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigEndpointConfig], jsii.get(self, "endpointConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gceClusterConfigInput")
    def gce_cluster_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfig], jsii.get(self, "gceClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="initializationActionInput")
    def initialization_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigInitializationAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigInitializationAction]]], jsii.get(self, "initializationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigInput")
    def lifecycle_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigLifecycleConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigLifecycleConfig], jsii.get(self, "lifecycleConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="masterConfigInput")
    def master_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigMasterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigMasterConfig], jsii.get(self, "masterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreConfigInput")
    def metastore_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigMetastoreConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigMetastoreConfig], jsii.get(self, "metastoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibleWorkerConfigInput")
    def preemptible_worker_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig"], jsii.get(self, "preemptibleWorkerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigSecurityConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfigInput")
    def software_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigSoftwareConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucketInput")
    def staging_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="tempBucketInput")
    def temp_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tempBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigInput")
    def worker_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigWorkerConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigWorkerConfig"], jsii.get(self, "workerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6145eea8103675c6cd52d0a0c6e58e97919e08c86b6f83d662ec3a31caf0fefc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tempBucket")
    def temp_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempBucket"))

    @temp_bucket.setter
    def temp_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b502e745a475c0b0fedee059b8bcd0552a5729e7241fd88257b04fb7153c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocClusterClusterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e1e78ea6a75a225ff15764deb7da91fc2819acfb1066d22d4becf2b63df47d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disk_config": "diskConfig",
        "instance_flexibility_policy": "instanceFlexibilityPolicy",
        "num_instances": "numInstances",
        "preemptibility": "preemptibility",
    },
)
class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig:
    def __init__(
        self,
        *,
        disk_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_flexibility_policy: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        :param instance_flexibility_policy: instance_flexibility_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#instance_flexibility_policy GoogleDataprocCluster#instance_flexibility_policy}
        :param num_instances: Specifies the number of preemptible nodes to create. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        :param preemptibility: Specifies the preemptibility of the secondary nodes. Defaults to PREEMPTIBLE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptibility GoogleDataprocCluster#preemptibility}
        '''
        if isinstance(disk_config, dict):
            disk_config = GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig(**disk_config)
        if isinstance(instance_flexibility_policy, dict):
            instance_flexibility_policy = GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy(**instance_flexibility_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76b040ff125fabff02112d4f9eb142c08527bc6e237f2eef78327ea82553ef6)
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument instance_flexibility_policy", value=instance_flexibility_policy, expected_type=type_hints["instance_flexibility_policy"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
            check_type(argname="argument preemptibility", value=preemptibility, expected_type=type_hints["preemptibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if instance_flexibility_policy is not None:
            self._values["instance_flexibility_policy"] = instance_flexibility_policy
        if num_instances is not None:
            self._values["num_instances"] = num_instances
        if preemptibility is not None:
            self._values["preemptibility"] = preemptibility

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig"], result)

    @builtins.property
    def instance_flexibility_policy(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy"]:
        '''instance_flexibility_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#instance_flexibility_policy GoogleDataprocCluster#instance_flexibility_policy}
        '''
        result = self._values.get("instance_flexibility_policy")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy"], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of preemptible nodes to create. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preemptibility(self) -> typing.Optional[builtins.str]:
        '''Specifies the preemptibility of the secondary nodes. Defaults to PREEMPTIBLE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptibility GoogleDataprocCluster#preemptibility}
        '''
        result = self._values.get("preemptibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "local_ssd_interface": "localSsdInterface",
        "num_local_ssds": "numLocalSsds",
    },
)
class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        local_ssd_interface: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each preemptible worker node, specified in GB. The smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each preemptible worker node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        :param local_ssd_interface: Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each preemptible worker node. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5bccb9f2e86c922412ee98d7aa40dfb2d68d74e6d6ba1e96c7721290872c67)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument local_ssd_interface", value=local_ssd_interface, expected_type=type_hints["local_ssd_interface"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if local_ssd_interface is not None:
            self._values["local_ssd_interface"] = local_ssd_interface
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the primary disk attached to each preemptible worker node, specified in GB.

        The smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''The disk type of the primary disk attached to each preemptible worker node.

        Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_interface(self) -> typing.Optional[builtins.str]:
        '''Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        '''
        result = self._values.get("local_ssd_interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''The amount of local SSD disks that will be attached to each preemptible worker node. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbb86b0217aad5934a5d1508e2abb3173dda65c4c831604b0e3b15e5aec85ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetLocalSsdInterface")
    def reset_local_ssd_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdInterface", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdInterfaceInput")
    def local_ssd_interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localSsdInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b358e9d68c006a49f288492853791e19dfd9d290c37afc1981f405fb7fbcc0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa904adb1efa8b1e07eaf40e94c40f71ef6dd1425f92f9e5ed2299f56f08f286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdInterface")
    def local_ssd_interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSsdInterface"))

    @local_ssd_interface.setter
    def local_ssd_interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8677951b9c8370d15fd26c633aca9bd639127da8f43336753f36d582ada269d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdInterface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33cca773879d5506f0d1dc423d6d599d7c1349272626be8d8e5674565a3eaf51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea293759e12d5c052f8496dd6cede1f0620852cdc50e2433c18c989cfc78d91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "instance_selection_list": "instanceSelectionList",
        "provisioning_model_mix": "provisioningModelMix",
    },
)
class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy:
    def __init__(
        self,
        *,
        instance_selection_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        provisioning_model_mix: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param instance_selection_list: instance_selection_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#instance_selection_list GoogleDataprocCluster#instance_selection_list}
        :param provisioning_model_mix: provisioning_model_mix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#provisioning_model_mix GoogleDataprocCluster#provisioning_model_mix}
        '''
        if isinstance(provisioning_model_mix, dict):
            provisioning_model_mix = GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix(**provisioning_model_mix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f99cf738f5c54f4cbf256b6bd0a9f68bd1a0f12676523154394586aa6fbdbe)
            check_type(argname="argument instance_selection_list", value=instance_selection_list, expected_type=type_hints["instance_selection_list"])
            check_type(argname="argument provisioning_model_mix", value=provisioning_model_mix, expected_type=type_hints["provisioning_model_mix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_selection_list is not None:
            self._values["instance_selection_list"] = instance_selection_list
        if provisioning_model_mix is not None:
            self._values["provisioning_model_mix"] = provisioning_model_mix

    @builtins.property
    def instance_selection_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct"]]]:
        '''instance_selection_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#instance_selection_list GoogleDataprocCluster#instance_selection_list}
        '''
        result = self._values.get("instance_selection_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct"]]], result)

    @builtins.property
    def provisioning_model_mix(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix"]:
        '''provisioning_model_mix block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#provisioning_model_mix GoogleDataprocCluster#provisioning_model_mix}
        '''
        result = self._values.get("provisioning_model_mix")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct",
    jsii_struct_bases=[],
    name_mapping={"machine_types": "machineTypes", "rank": "rank"},
)
class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct:
    def __init__(
        self,
        *,
        machine_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        rank: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_types: Full machine-type names, e.g. "n1-standard-16". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_types GoogleDataprocCluster#machine_types}
        :param rank: Preference of this instance selection. Lower number means higher preference. Dataproc will first try to create a VM based on the machine-type with priority rank and fallback to next rank based on availability. Machine types and instance selections with the same priority have the same preference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#rank GoogleDataprocCluster#rank}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e5989d8fd4e8309dbfc4aab098f37130af863a380ea6fcdb04f55c0b9d8617e)
            check_type(argname="argument machine_types", value=machine_types, expected_type=type_hints["machine_types"])
            check_type(argname="argument rank", value=rank, expected_type=type_hints["rank"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if machine_types is not None:
            self._values["machine_types"] = machine_types
        if rank is not None:
            self._values["rank"] = rank

    @builtins.property
    def machine_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Full machine-type names, e.g. "n1-standard-16".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_types GoogleDataprocCluster#machine_types}
        '''
        result = self._values.get("machine_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rank(self) -> typing.Optional[jsii.Number]:
        '''Preference of this instance selection.

        Lower number means higher preference. Dataproc will first try to create a VM based on the machine-type with priority rank and fallback to next rank based on availability. Machine types and instance selections with the same priority have the same preference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#rank GoogleDataprocCluster#rank}
        '''
        result = self._values.get("rank")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d072897664a3377051bcd7b8a8cabbb5ca92957052329f3f41308c1d97da7e0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__952abe0ccddc8ff4f32f8ef5825f3d7a4e81075a6c4236b8a3b60cfcd2316d6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7371b6ad550bc3656db6a610277e1ad323a07b5ae816706d13f3b3b338c27192)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10f673585403aa063baded1090153b39bc40372fbd833838eea733162a8f0b15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4694a9c56043e40ea0c84974c0581bf59e54435c61dffa56a75ad3d93f363cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1efe112e81c823c5c3dc9e3acfe86e1a15c2be6f3390fe4d8581c1f01d6fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fc4785b8af997b2942d6c07420844407a15244b94f2fb9c88a922952481265c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMachineTypes")
    def reset_machine_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineTypes", []))

    @jsii.member(jsii_name="resetRank")
    def reset_rank(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRank", []))

    @builtins.property
    @jsii.member(jsii_name="machineTypesInput")
    def machine_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "machineTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="rankInput")
    def rank_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rankInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypes")
    def machine_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "machineTypes"))

    @machine_types.setter
    def machine_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67957d03bd67d5988d1aba1a539801fc4f67156c81b90ba0b7ab4b4bec27d993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rank")
    def rank(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rank"))

    @rank.setter
    def rank(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df957055249b32b2d4b67f24641593af807523b2ec0b52c9af5b4a340c4d798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rank", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b8e95c8854604a1a8d0049ed49172e617aa3e39424496328402f87aaa1c086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResults",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResults:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0a29094428b922ca35274bb3464a98ddfb27832b98bd3888d0f8c65fd9dab67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada9723b0947ea40951c1f8fad82c2c01564cf31357128974788cf89a5741729)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f79a1dd0e681275b6c06439e8c760db71eb2183119fa9e0a64be03333c3d41a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4feef1b50bb445d686e8b9f0a40e9ec215b1f5dc93b8d6ac085367509b28c5ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25404ca3bdf677b37f92bbf71b77a2c1bf8ec314fc85c11dfc87d78832df9230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dde1c2b74cbe69a3c03fa1d28ed6fffdfaa88c2f0c49f021f1ccc433605f26e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @builtins.property
    @jsii.member(jsii_name="vmCount")
    def vm_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResults]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResults], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResults],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a933a8e8d4b63861136a24c2909b574a1845e7f3e634c82217a662781783ac2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e9766e17eee02f2c4f87f5296f244e979ec1db1e6cebf2d4d5b5fd20fadd3b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceSelectionList")
    def put_instance_selection_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc233141c00021e118e534b6bca4a96ce3e4799257b992d687efa184be4b05f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInstanceSelectionList", [value]))

    @jsii.member(jsii_name="putProvisioningModelMix")
    def put_provisioning_model_mix(
        self,
        *,
        standard_capacity_base: typing.Optional[jsii.Number] = None,
        standard_capacity_percent_above_base: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param standard_capacity_base: The base capacity that will always use Standard VMs to avoid risk of more preemption than the minimum capacity you need. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#standard_capacity_base GoogleDataprocCluster#standard_capacity_base}
        :param standard_capacity_percent_above_base: The percentage of target capacity that should use Standard VM. The remaining percentage will use Spot VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#standard_capacity_percent_above_base GoogleDataprocCluster#standard_capacity_percent_above_base}
        '''
        value = GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix(
            standard_capacity_base=standard_capacity_base,
            standard_capacity_percent_above_base=standard_capacity_percent_above_base,
        )

        return typing.cast(None, jsii.invoke(self, "putProvisioningModelMix", [value]))

    @jsii.member(jsii_name="resetInstanceSelectionList")
    def reset_instance_selection_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceSelectionList", []))

    @jsii.member(jsii_name="resetProvisioningModelMix")
    def reset_provisioning_model_mix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisioningModelMix", []))

    @builtins.property
    @jsii.member(jsii_name="instanceSelectionList")
    def instance_selection_list(
        self,
    ) -> GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructList:
        return typing.cast(GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructList, jsii.get(self, "instanceSelectionList"))

    @builtins.property
    @jsii.member(jsii_name="instanceSelectionResults")
    def instance_selection_results(
        self,
    ) -> GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsList:
        return typing.cast(GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsList, jsii.get(self, "instanceSelectionResults"))

    @builtins.property
    @jsii.member(jsii_name="provisioningModelMix")
    def provisioning_model_mix(
        self,
    ) -> "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMixOutputReference":
        return typing.cast("GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMixOutputReference", jsii.get(self, "provisioningModelMix"))

    @builtins.property
    @jsii.member(jsii_name="instanceSelectionListInput")
    def instance_selection_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]]], jsii.get(self, "instanceSelectionListInput"))

    @builtins.property
    @jsii.member(jsii_name="provisioningModelMixInput")
    def provisioning_model_mix_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix"], jsii.get(self, "provisioningModelMixInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219e5cdd4ffae17e3e0fdd0cac1ddb557a2bb43c4da641f48197aa977c4cb970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix",
    jsii_struct_bases=[],
    name_mapping={
        "standard_capacity_base": "standardCapacityBase",
        "standard_capacity_percent_above_base": "standardCapacityPercentAboveBase",
    },
)
class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix:
    def __init__(
        self,
        *,
        standard_capacity_base: typing.Optional[jsii.Number] = None,
        standard_capacity_percent_above_base: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param standard_capacity_base: The base capacity that will always use Standard VMs to avoid risk of more preemption than the minimum capacity you need. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#standard_capacity_base GoogleDataprocCluster#standard_capacity_base}
        :param standard_capacity_percent_above_base: The percentage of target capacity that should use Standard VM. The remaining percentage will use Spot VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#standard_capacity_percent_above_base GoogleDataprocCluster#standard_capacity_percent_above_base}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3b3e772e571a948230716ccaff1dce05375fc747c3d3b0602cacb4c152419c)
            check_type(argname="argument standard_capacity_base", value=standard_capacity_base, expected_type=type_hints["standard_capacity_base"])
            check_type(argname="argument standard_capacity_percent_above_base", value=standard_capacity_percent_above_base, expected_type=type_hints["standard_capacity_percent_above_base"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if standard_capacity_base is not None:
            self._values["standard_capacity_base"] = standard_capacity_base
        if standard_capacity_percent_above_base is not None:
            self._values["standard_capacity_percent_above_base"] = standard_capacity_percent_above_base

    @builtins.property
    def standard_capacity_base(self) -> typing.Optional[jsii.Number]:
        '''The base capacity that will always use Standard VMs to avoid risk of more preemption than the minimum capacity you need.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#standard_capacity_base GoogleDataprocCluster#standard_capacity_base}
        '''
        result = self._values.get("standard_capacity_base")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def standard_capacity_percent_above_base(self) -> typing.Optional[jsii.Number]:
        '''The percentage of target capacity that should use Standard VM. The remaining percentage will use Spot VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#standard_capacity_percent_above_base GoogleDataprocCluster#standard_capacity_percent_above_base}
        '''
        result = self._values.get("standard_capacity_percent_above_base")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMixOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMixOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc955f6e4798a4871bc8290316d14d3bb3b82971e533d1521e5acc608c2fa3f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStandardCapacityBase")
    def reset_standard_capacity_base(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandardCapacityBase", []))

    @jsii.member(jsii_name="resetStandardCapacityPercentAboveBase")
    def reset_standard_capacity_percent_above_base(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandardCapacityPercentAboveBase", []))

    @builtins.property
    @jsii.member(jsii_name="standardCapacityBaseInput")
    def standard_capacity_base_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "standardCapacityBaseInput"))

    @builtins.property
    @jsii.member(jsii_name="standardCapacityPercentAboveBaseInput")
    def standard_capacity_percent_above_base_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "standardCapacityPercentAboveBaseInput"))

    @builtins.property
    @jsii.member(jsii_name="standardCapacityBase")
    def standard_capacity_base(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "standardCapacityBase"))

    @standard_capacity_base.setter
    def standard_capacity_base(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0046d0a86e6b73ea35c6a4a911bb927d6b974a96a8a06773038909fd9078786a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standardCapacityBase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="standardCapacityPercentAboveBase")
    def standard_capacity_percent_above_base(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "standardCapacityPercentAboveBase"))

    @standard_capacity_percent_above_base.setter
    def standard_capacity_percent_above_base(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb652e114f64266d17e009e94287edeb4b93ace39e15598f7e73df1aada71b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standardCapacityPercentAboveBase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3c13bc629aeb63e0ece311a0aed1322c8cc91236a2c9ecfb079ca638d494c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c9fc9deb2486edf870fcfa4104e2aca8c38b6a42b3a04c677d8a19f9105150)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        local_ssd_interface: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each preemptible worker node, specified in GB. The smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each preemptible worker node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        :param local_ssd_interface: Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each preemptible worker node. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        value = GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            local_ssd_interface=local_ssd_interface,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="putInstanceFlexibilityPolicy")
    def put_instance_flexibility_policy(
        self,
        *,
        instance_selection_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
        provisioning_model_mix: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param instance_selection_list: instance_selection_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#instance_selection_list GoogleDataprocCluster#instance_selection_list}
        :param provisioning_model_mix: provisioning_model_mix block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#provisioning_model_mix GoogleDataprocCluster#provisioning_model_mix}
        '''
        value = GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy(
            instance_selection_list=instance_selection_list,
            provisioning_model_mix=provisioning_model_mix,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFlexibilityPolicy", [value]))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetInstanceFlexibilityPolicy")
    def reset_instance_flexibility_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceFlexibilityPolicy", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @jsii.member(jsii_name="resetPreemptibility")
    def reset_preemptibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptibility", []))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceFlexibilityPolicy")
    def instance_flexibility_policy(
        self,
    ) -> GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyOutputReference, jsii.get(self, "instanceFlexibilityPolicy"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceFlexibilityPolicyInput")
    def instance_flexibility_policy_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy], jsii.get(self, "instanceFlexibilityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibilityInput")
    def preemptibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1f89b45949f2a176c84c79db85e1842e5f3ff898ca2ec139e5caa298df7ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptibility")
    def preemptibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptibility"))

    @preemptibility.setter
    def preemptibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983b62165824bb966ba31d9f19c34fa7b4a8a86a289b8fd37dac00bd84cc958f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f858076c07e992db40863acac2dcec53a49cb02fc1e9a0ada36b9587f82158d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"kerberos_config": "kerberosConfig"},
)
class GoogleDataprocClusterClusterConfigSecurityConfig:
    def __init__(
        self,
        *,
        kerberos_config: typing.Union["GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kerberos_config GoogleDataprocCluster#kerberos_config}
        '''
        if isinstance(kerberos_config, dict):
            kerberos_config = GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig(**kerberos_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1b4eaa78ad66e94bbad8c04478ae604ecd32e6ec812583364fe1c8f0b5b2f2)
            check_type(argname="argument kerberos_config", value=kerberos_config, expected_type=type_hints["kerberos_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kerberos_config": kerberos_config,
        }

    @builtins.property
    def kerberos_config(
        self,
    ) -> "GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig":
        '''kerberos_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kerberos_config GoogleDataprocCluster#kerberos_config}
        '''
        result = self._values.get("kerberos_config")
        assert result is not None, "Required property 'kerberos_config' is missing"
        return typing.cast("GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_uri": "kmsKeyUri",
        "root_principal_password_uri": "rootPrincipalPasswordUri",
        "cross_realm_trust_admin_server": "crossRealmTrustAdminServer",
        "cross_realm_trust_kdc": "crossRealmTrustKdc",
        "cross_realm_trust_realm": "crossRealmTrustRealm",
        "cross_realm_trust_shared_password_uri": "crossRealmTrustSharedPasswordUri",
        "enable_kerberos": "enableKerberos",
        "kdc_db_key_uri": "kdcDbKeyUri",
        "key_password_uri": "keyPasswordUri",
        "keystore_password_uri": "keystorePasswordUri",
        "keystore_uri": "keystoreUri",
        "realm": "realm",
        "tgt_lifetime_hours": "tgtLifetimeHours",
        "truststore_password_uri": "truststorePasswordUri",
        "truststore_uri": "truststoreUri",
    },
)
class GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig:
    def __init__(
        self,
        *,
        kms_key_uri: builtins.str,
        root_principal_password_uri: builtins.str,
        cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
        cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
        cross_realm_trust_realm: typing.Optional[builtins.str] = None,
        cross_realm_trust_shared_password_uri: typing.Optional[builtins.str] = None,
        enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kdc_db_key_uri: typing.Optional[builtins.str] = None,
        key_password_uri: typing.Optional[builtins.str] = None,
        keystore_password_uri: typing.Optional[builtins.str] = None,
        keystore_uri: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
        truststore_password_uri: typing.Optional[builtins.str] = None,
        truststore_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_uri: The uri of the KMS key used to encrypt various sensitive files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kms_key_uri GoogleDataprocCluster#kms_key_uri}
        :param root_principal_password_uri: The cloud Storage URI of a KMS encrypted file containing the root principal password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#root_principal_password_uri GoogleDataprocCluster#root_principal_password_uri}
        :param cross_realm_trust_admin_server: The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_admin_server GoogleDataprocCluster#cross_realm_trust_admin_server}
        :param cross_realm_trust_kdc: The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_kdc GoogleDataprocCluster#cross_realm_trust_kdc}
        :param cross_realm_trust_realm: The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_realm GoogleDataprocCluster#cross_realm_trust_realm}
        :param cross_realm_trust_shared_password_uri: The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_shared_password_uri GoogleDataprocCluster#cross_realm_trust_shared_password_uri}
        :param enable_kerberos: Flag to indicate whether to Kerberize the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_kerberos GoogleDataprocCluster#enable_kerberos}
        :param kdc_db_key_uri: The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kdc_db_key_uri GoogleDataprocCluster#kdc_db_key_uri}
        :param key_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#key_password_uri GoogleDataprocCluster#key_password_uri}
        :param keystore_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore. For the self-signed certificate, this password is generated by Dataproc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#keystore_password_uri GoogleDataprocCluster#keystore_password_uri}
        :param keystore_uri: The Cloud Storage URI of the keystore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#keystore_uri GoogleDataprocCluster#keystore_uri}
        :param realm: The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#realm GoogleDataprocCluster#realm}
        :param tgt_lifetime_hours: The lifetime of the ticket granting ticket, in hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#tgt_lifetime_hours GoogleDataprocCluster#tgt_lifetime_hours}
        :param truststore_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#truststore_password_uri GoogleDataprocCluster#truststore_password_uri}
        :param truststore_uri: The Cloud Storage URI of the truststore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#truststore_uri GoogleDataprocCluster#truststore_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1da887f121399393b012e113b3a6075afe00babab2df70bb39039593976694d)
            check_type(argname="argument kms_key_uri", value=kms_key_uri, expected_type=type_hints["kms_key_uri"])
            check_type(argname="argument root_principal_password_uri", value=root_principal_password_uri, expected_type=type_hints["root_principal_password_uri"])
            check_type(argname="argument cross_realm_trust_admin_server", value=cross_realm_trust_admin_server, expected_type=type_hints["cross_realm_trust_admin_server"])
            check_type(argname="argument cross_realm_trust_kdc", value=cross_realm_trust_kdc, expected_type=type_hints["cross_realm_trust_kdc"])
            check_type(argname="argument cross_realm_trust_realm", value=cross_realm_trust_realm, expected_type=type_hints["cross_realm_trust_realm"])
            check_type(argname="argument cross_realm_trust_shared_password_uri", value=cross_realm_trust_shared_password_uri, expected_type=type_hints["cross_realm_trust_shared_password_uri"])
            check_type(argname="argument enable_kerberos", value=enable_kerberos, expected_type=type_hints["enable_kerberos"])
            check_type(argname="argument kdc_db_key_uri", value=kdc_db_key_uri, expected_type=type_hints["kdc_db_key_uri"])
            check_type(argname="argument key_password_uri", value=key_password_uri, expected_type=type_hints["key_password_uri"])
            check_type(argname="argument keystore_password_uri", value=keystore_password_uri, expected_type=type_hints["keystore_password_uri"])
            check_type(argname="argument keystore_uri", value=keystore_uri, expected_type=type_hints["keystore_uri"])
            check_type(argname="argument realm", value=realm, expected_type=type_hints["realm"])
            check_type(argname="argument tgt_lifetime_hours", value=tgt_lifetime_hours, expected_type=type_hints["tgt_lifetime_hours"])
            check_type(argname="argument truststore_password_uri", value=truststore_password_uri, expected_type=type_hints["truststore_password_uri"])
            check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_uri": kms_key_uri,
            "root_principal_password_uri": root_principal_password_uri,
        }
        if cross_realm_trust_admin_server is not None:
            self._values["cross_realm_trust_admin_server"] = cross_realm_trust_admin_server
        if cross_realm_trust_kdc is not None:
            self._values["cross_realm_trust_kdc"] = cross_realm_trust_kdc
        if cross_realm_trust_realm is not None:
            self._values["cross_realm_trust_realm"] = cross_realm_trust_realm
        if cross_realm_trust_shared_password_uri is not None:
            self._values["cross_realm_trust_shared_password_uri"] = cross_realm_trust_shared_password_uri
        if enable_kerberos is not None:
            self._values["enable_kerberos"] = enable_kerberos
        if kdc_db_key_uri is not None:
            self._values["kdc_db_key_uri"] = kdc_db_key_uri
        if key_password_uri is not None:
            self._values["key_password_uri"] = key_password_uri
        if keystore_password_uri is not None:
            self._values["keystore_password_uri"] = keystore_password_uri
        if keystore_uri is not None:
            self._values["keystore_uri"] = keystore_uri
        if realm is not None:
            self._values["realm"] = realm
        if tgt_lifetime_hours is not None:
            self._values["tgt_lifetime_hours"] = tgt_lifetime_hours
        if truststore_password_uri is not None:
            self._values["truststore_password_uri"] = truststore_password_uri
        if truststore_uri is not None:
            self._values["truststore_uri"] = truststore_uri

    @builtins.property
    def kms_key_uri(self) -> builtins.str:
        '''The uri of the KMS key used to encrypt various sensitive files.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kms_key_uri GoogleDataprocCluster#kms_key_uri}
        '''
        result = self._values.get("kms_key_uri")
        assert result is not None, "Required property 'kms_key_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_principal_password_uri(self) -> builtins.str:
        '''The cloud Storage URI of a KMS encrypted file containing the root principal password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#root_principal_password_uri GoogleDataprocCluster#root_principal_password_uri}
        '''
        result = self._values.get("root_principal_password_uri")
        assert result is not None, "Required property 'root_principal_password_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cross_realm_trust_admin_server(self) -> typing.Optional[builtins.str]:
        '''The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_admin_server GoogleDataprocCluster#cross_realm_trust_admin_server}
        '''
        result = self._values.get("cross_realm_trust_admin_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_kdc(self) -> typing.Optional[builtins.str]:
        '''The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_kdc GoogleDataprocCluster#cross_realm_trust_kdc}
        '''
        result = self._values.get("cross_realm_trust_kdc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_realm(self) -> typing.Optional[builtins.str]:
        '''The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_realm GoogleDataprocCluster#cross_realm_trust_realm}
        '''
        result = self._values.get("cross_realm_trust_realm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_shared_password_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_shared_password_uri GoogleDataprocCluster#cross_realm_trust_shared_password_uri}
        '''
        result = self._values.get("cross_realm_trust_shared_password_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_kerberos(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag to indicate whether to Kerberize the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_kerberos GoogleDataprocCluster#enable_kerberos}
        '''
        result = self._values.get("enable_kerberos")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kdc_db_key_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kdc_db_key_uri GoogleDataprocCluster#kdc_db_key_uri}
        '''
        result = self._values.get("kdc_db_key_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_password_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key.

        For the self-signed certificate, this password is generated by Dataproc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#key_password_uri GoogleDataprocCluster#key_password_uri}
        '''
        result = self._values.get("key_password_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keystore_password_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore.

        For the self-signed certificate, this password is generated
        by Dataproc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#keystore_password_uri GoogleDataprocCluster#keystore_password_uri}
        '''
        result = self._values.get("keystore_password_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keystore_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of the keystore file used for SSL encryption.

        If not provided, Dataproc will provide a self-signed certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#keystore_uri GoogleDataprocCluster#keystore_uri}
        '''
        result = self._values.get("keystore_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realm(self) -> typing.Optional[builtins.str]:
        '''The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#realm GoogleDataprocCluster#realm}
        '''
        result = self._values.get("realm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tgt_lifetime_hours(self) -> typing.Optional[jsii.Number]:
        '''The lifetime of the ticket granting ticket, in hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#tgt_lifetime_hours GoogleDataprocCluster#tgt_lifetime_hours}
        '''
        result = self._values.get("tgt_lifetime_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def truststore_password_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore.

        For the self-signed certificate, this password is generated by Dataproc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#truststore_password_uri GoogleDataprocCluster#truststore_password_uri}
        '''
        result = self._values.get("truststore_password_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def truststore_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of the truststore file used for SSL encryption.

        If not provided, Dataproc will provide a self-signed certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#truststore_uri GoogleDataprocCluster#truststore_uri}
        '''
        result = self._values.get("truststore_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a9b1c4079e3e1c62821691ccc6091303d4c11303a1aed64162af93952b84507)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCrossRealmTrustAdminServer")
    def reset_cross_realm_trust_admin_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustAdminServer", []))

    @jsii.member(jsii_name="resetCrossRealmTrustKdc")
    def reset_cross_realm_trust_kdc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustKdc", []))

    @jsii.member(jsii_name="resetCrossRealmTrustRealm")
    def reset_cross_realm_trust_realm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustRealm", []))

    @jsii.member(jsii_name="resetCrossRealmTrustSharedPasswordUri")
    def reset_cross_realm_trust_shared_password_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustSharedPasswordUri", []))

    @jsii.member(jsii_name="resetEnableKerberos")
    def reset_enable_kerberos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableKerberos", []))

    @jsii.member(jsii_name="resetKdcDbKeyUri")
    def reset_kdc_db_key_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKdcDbKeyUri", []))

    @jsii.member(jsii_name="resetKeyPasswordUri")
    def reset_key_password_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPasswordUri", []))

    @jsii.member(jsii_name="resetKeystorePasswordUri")
    def reset_keystore_password_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeystorePasswordUri", []))

    @jsii.member(jsii_name="resetKeystoreUri")
    def reset_keystore_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeystoreUri", []))

    @jsii.member(jsii_name="resetRealm")
    def reset_realm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealm", []))

    @jsii.member(jsii_name="resetTgtLifetimeHours")
    def reset_tgt_lifetime_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTgtLifetimeHours", []))

    @jsii.member(jsii_name="resetTruststorePasswordUri")
    def reset_truststore_password_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTruststorePasswordUri", []))

    @jsii.member(jsii_name="resetTruststoreUri")
    def reset_truststore_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTruststoreUri", []))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustAdminServerInput")
    def cross_realm_trust_admin_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustAdminServerInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustKdcInput")
    def cross_realm_trust_kdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustKdcInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustRealmInput")
    def cross_realm_trust_realm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustRealmInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustSharedPasswordUriInput")
    def cross_realm_trust_shared_password_uri_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustSharedPasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="enableKerberosInput")
    def enable_kerberos_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableKerberosInput"))

    @builtins.property
    @jsii.member(jsii_name="kdcDbKeyUriInput")
    def kdc_db_key_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kdcDbKeyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPasswordUriInput")
    def key_password_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="keystorePasswordUriInput")
    def keystore_password_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keystorePasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="keystoreUriInput")
    def keystore_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keystoreUriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyUriInput")
    def kms_key_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="realmInput")
    def realm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "realmInput"))

    @builtins.property
    @jsii.member(jsii_name="rootPrincipalPasswordUriInput")
    def root_principal_password_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootPrincipalPasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="tgtLifetimeHoursInput")
    def tgt_lifetime_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tgtLifetimeHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="truststorePasswordUriInput")
    def truststore_password_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "truststorePasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="truststoreUriInput")
    def truststore_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "truststoreUriInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustAdminServer")
    def cross_realm_trust_admin_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustAdminServer"))

    @cross_realm_trust_admin_server.setter
    def cross_realm_trust_admin_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__516a3c747637fff16acfbda19f09b023ad8c6118d6eecce133c12891b86e56e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustAdminServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustKdc")
    def cross_realm_trust_kdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustKdc"))

    @cross_realm_trust_kdc.setter
    def cross_realm_trust_kdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1dd545374e2f7b1903865531f47449eda9365497fc8bd993b3fd739ae45b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustKdc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustRealm")
    def cross_realm_trust_realm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustRealm"))

    @cross_realm_trust_realm.setter
    def cross_realm_trust_realm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9dba19e73824fe66655092e2bfd333e8b876d8dd8cbbb6880b7568498db1b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustRealm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustSharedPasswordUri")
    def cross_realm_trust_shared_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustSharedPasswordUri"))

    @cross_realm_trust_shared_password_uri.setter
    def cross_realm_trust_shared_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db1e7456f80d21fbbb9399af19481908ddf8a6616e3258696f96b005ad41ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustSharedPasswordUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableKerberos")
    def enable_kerberos(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableKerberos"))

    @enable_kerberos.setter
    def enable_kerberos(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db25da7daaf3b53742381b6b0adf8defbddbed888ae7d31c3bc9899d0b2c1e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableKerberos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kdcDbKeyUri")
    def kdc_db_key_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kdcDbKeyUri"))

    @kdc_db_key_uri.setter
    def kdc_db_key_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccd79e68ecd7874b8dfa72aa404bbf96d10578096babcbc83d51db6609cee30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kdcDbKeyUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPasswordUri")
    def key_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPasswordUri"))

    @key_password_uri.setter
    def key_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b291215d402ee52dd871753def0339eef0c1e0fd0d9c23b195f51c156230d09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPasswordUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keystorePasswordUri")
    def keystore_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystorePasswordUri"))

    @keystore_password_uri.setter
    def keystore_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb23e65c9c097c851dad8c9411ffc274492ef59c73474841e230b1b709e9458a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystorePasswordUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keystoreUri")
    def keystore_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystoreUri"))

    @keystore_uri.setter
    def keystore_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15b6667f1fb328a697f7a0307da4ef5998858325ca5d44b66f037376b4ffae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystoreUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyUri")
    def kms_key_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyUri"))

    @kms_key_uri.setter
    def kms_key_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27c91bf200cb2f594608420646667d665ec71fc8fbea62b73de8509f69d29e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realm")
    def realm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realm"))

    @realm.setter
    def realm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49158f8dcbc736838244016d8d8c739dbce7d0783dcaf009cb3c893dbcb4399a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootPrincipalPasswordUri")
    def root_principal_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPrincipalPasswordUri"))

    @root_principal_password_uri.setter
    def root_principal_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecb4c28ad1519c4d509e3e1755483edf70faf685f2f4580d4ee1e3b5666d140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPrincipalPasswordUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tgtLifetimeHours")
    def tgt_lifetime_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tgtLifetimeHours"))

    @tgt_lifetime_hours.setter
    def tgt_lifetime_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54bed848a4efcf815bb5c6c7467adc72778176fde8e54e8c3fbbfffe21b2ec87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tgtLifetimeHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="truststorePasswordUri")
    def truststore_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "truststorePasswordUri"))

    @truststore_password_uri.setter
    def truststore_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675c909007b4847f7078c2c41dcf1c134c87c5a919763898ca1aeb8a6e96afe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "truststorePasswordUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="truststoreUri")
    def truststore_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "truststoreUri"))

    @truststore_uri.setter
    def truststore_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f85fa46261123ee7f5889e9f1b264fbf7da1cf1a2e8b773a39e7a89b6fb0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "truststoreUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028a83fdb14e240c72bd6234b0ea00d480837821766eaa5afb27be91c72eac4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecf15ac78f233a75d8ca3d2f26a6e2f4914165eab69901b89ab060adb68e82f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKerberosConfig")
    def put_kerberos_config(
        self,
        *,
        kms_key_uri: builtins.str,
        root_principal_password_uri: builtins.str,
        cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
        cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
        cross_realm_trust_realm: typing.Optional[builtins.str] = None,
        cross_realm_trust_shared_password_uri: typing.Optional[builtins.str] = None,
        enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kdc_db_key_uri: typing.Optional[builtins.str] = None,
        key_password_uri: typing.Optional[builtins.str] = None,
        keystore_password_uri: typing.Optional[builtins.str] = None,
        keystore_uri: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
        truststore_password_uri: typing.Optional[builtins.str] = None,
        truststore_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_uri: The uri of the KMS key used to encrypt various sensitive files. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kms_key_uri GoogleDataprocCluster#kms_key_uri}
        :param root_principal_password_uri: The cloud Storage URI of a KMS encrypted file containing the root principal password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#root_principal_password_uri GoogleDataprocCluster#root_principal_password_uri}
        :param cross_realm_trust_admin_server: The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_admin_server GoogleDataprocCluster#cross_realm_trust_admin_server}
        :param cross_realm_trust_kdc: The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_kdc GoogleDataprocCluster#cross_realm_trust_kdc}
        :param cross_realm_trust_realm: The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_realm GoogleDataprocCluster#cross_realm_trust_realm}
        :param cross_realm_trust_shared_password_uri: The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cross_realm_trust_shared_password_uri GoogleDataprocCluster#cross_realm_trust_shared_password_uri}
        :param enable_kerberos: Flag to indicate whether to Kerberize the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#enable_kerberos GoogleDataprocCluster#enable_kerberos}
        :param kdc_db_key_uri: The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kdc_db_key_uri GoogleDataprocCluster#kdc_db_key_uri}
        :param key_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#key_password_uri GoogleDataprocCluster#key_password_uri}
        :param keystore_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore. For the self-signed certificate, this password is generated by Dataproc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#keystore_password_uri GoogleDataprocCluster#keystore_password_uri}
        :param keystore_uri: The Cloud Storage URI of the keystore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#keystore_uri GoogleDataprocCluster#keystore_uri}
        :param realm: The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#realm GoogleDataprocCluster#realm}
        :param tgt_lifetime_hours: The lifetime of the ticket granting ticket, in hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#tgt_lifetime_hours GoogleDataprocCluster#tgt_lifetime_hours}
        :param truststore_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#truststore_password_uri GoogleDataprocCluster#truststore_password_uri}
        :param truststore_uri: The Cloud Storage URI of the truststore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#truststore_uri GoogleDataprocCluster#truststore_uri}
        '''
        value = GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig(
            kms_key_uri=kms_key_uri,
            root_principal_password_uri=root_principal_password_uri,
            cross_realm_trust_admin_server=cross_realm_trust_admin_server,
            cross_realm_trust_kdc=cross_realm_trust_kdc,
            cross_realm_trust_realm=cross_realm_trust_realm,
            cross_realm_trust_shared_password_uri=cross_realm_trust_shared_password_uri,
            enable_kerberos=enable_kerberos,
            kdc_db_key_uri=kdc_db_key_uri,
            key_password_uri=key_password_uri,
            keystore_password_uri=keystore_password_uri,
            keystore_uri=keystore_uri,
            realm=realm,
            tgt_lifetime_hours=tgt_lifetime_hours,
            truststore_password_uri=truststore_password_uri,
            truststore_uri=truststore_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putKerberosConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfig")
    def kerberos_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference, jsii.get(self, "kerberosConfig"))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfigInput")
    def kerberos_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig], jsii.get(self, "kerberosConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dfd0825f3c6407ffe233fe6a0d85b8ddd45e80e4fd92a8dfeb163bbb4a6164e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "image_version": "imageVersion",
        "optional_components": "optionalComponents",
        "override_properties": "overrideProperties",
    },
)
class GoogleDataprocClusterClusterConfigSoftwareConfig:
    def __init__(
        self,
        *,
        image_version: typing.Optional[builtins.str] = None,
        optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
        override_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param image_version: The Cloud Dataproc image version to use for the cluster - this controls the sets of software versions installed onto the nodes when you create clusters. If not specified, defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_version GoogleDataprocCluster#image_version}
        :param optional_components: The set of optional components to activate on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#optional_components GoogleDataprocCluster#optional_components}
        :param override_properties: A list of override and additional properties (key/value pairs) used to modify various aspects of the common configuration files used when creating a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#override_properties GoogleDataprocCluster#override_properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d726f20d286a49a4195472e3047ada75f2186074e259f7a77d20886eba1a4c)
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
            check_type(argname="argument optional_components", value=optional_components, expected_type=type_hints["optional_components"])
            check_type(argname="argument override_properties", value=override_properties, expected_type=type_hints["override_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image_version is not None:
            self._values["image_version"] = image_version
        if optional_components is not None:
            self._values["optional_components"] = optional_components
        if override_properties is not None:
            self._values["override_properties"] = override_properties

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''The Cloud Dataproc image version to use for the cluster - this controls the sets of software versions installed onto the nodes when you create clusters.

        If not specified, defaults to the latest version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_version GoogleDataprocCluster#image_version}
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of optional components to activate on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#optional_components GoogleDataprocCluster#optional_components}
        '''
        result = self._values.get("optional_components")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def override_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of override and additional properties (key/value pairs) used to modify various aspects of the common configuration files used when creating a cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#override_properties GoogleDataprocCluster#override_properties}
        '''
        result = self._values.get("override_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4483b1b7db2fe4bc652e650ba0498398d32c8707ef371577e2408ff543ad9595)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImageVersion")
    def reset_image_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersion", []))

    @jsii.member(jsii_name="resetOptionalComponents")
    def reset_optional_components(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionalComponents", []))

    @jsii.member(jsii_name="resetOverrideProperties")
    def reset_override_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideProperties", []))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionInput")
    def image_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalComponentsInput")
    def optional_components_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "optionalComponentsInput"))

    @builtins.property
    @jsii.member(jsii_name="overridePropertiesInput")
    def override_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "overridePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @image_version.setter
    def image_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846d4758a3cec9b782ea11ea37539a43b48cb80c34cddc0b64b21982851f5487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionalComponents")
    def optional_components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "optionalComponents"))

    @optional_components.setter
    def optional_components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abaa3551f1c1a5f74046e486a44106a86774d5efaeeb3b4edb3dfd30831370f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalComponents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideProperties")
    def override_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "overrideProperties"))

    @override_properties.setter
    def override_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e620127669a4f81dbf9b3f3d0d77bde63042af8318183ca294707bfe157a7d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigSoftwareConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018dd58a23b34e8f098681877834b03bdbf610f6f48c840a2cd8fd504034aa36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "disk_config": "diskConfig",
        "image_uri": "imageUri",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "min_num_instances": "minNumInstances",
        "num_instances": "numInstances",
    },
)
class GoogleDataprocClusterClusterConfigWorkerConfig:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterClusterConfigWorkerConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        min_num_instances: typing.Optional[jsii.Number] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        :param image_uri: The URI for the image to use for this master/worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_uri GoogleDataprocCluster#image_uri}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master/worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the master/worker. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        :param min_num_instances: The minimum number of primary worker instances to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_num_instances GoogleDataprocCluster#min_num_instances}
        :param num_instances: Specifies the number of worker nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        if isinstance(disk_config, dict):
            disk_config = GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b228ea6131006ecebfa8e7bd39e18e0040934b86367c56c878ff8158a3349370)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument min_num_instances", value=min_num_instances, expected_type=type_hints["min_num_instances"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if min_num_instances is not None:
            self._values["min_num_instances"] = min_num_instances
        if num_instances is not None:
            self._values["num_instances"] = num_instances

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigWorkerConfigAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerators GoogleDataprocCluster#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterClusterConfigWorkerConfigAccelerators"]]], result)

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#disk_config GoogleDataprocCluster#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig"], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''The URI for the image to use for this master/worker.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#image_uri GoogleDataprocCluster#image_uri}
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Google Compute Engine machine type to create for the master/worker.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''The name of a minimum generation of CPU family for the master/worker.

        If not specified, GCP will default to a predetermined computed value for each zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_num_instances(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of primary worker instances to create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_num_instances GoogleDataprocCluster#min_num_instances}
        '''
        result = self._values.get("min_num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of worker nodes to create. If not specified, GCP will default to a predetermined computed value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_instances GoogleDataprocCluster#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigWorkerConfigAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class GoogleDataprocClusterClusterConfigWorkerConfigAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: jsii.Number,
        accelerator_type: builtins.str,
    ) -> None:
        '''
        :param accelerator_count: The number of the accelerator cards of this type exposed to this instance. Often restricted to one of 1, 2, 4, or 8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_count GoogleDataprocCluster#accelerator_count}
        :param accelerator_type: The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_type GoogleDataprocCluster#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68054f22aff98abf7ea8ca1a19c10cfdeba78f1d655eb51686a5f9afc2945660)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator_count": accelerator_count,
            "accelerator_type": accelerator_type,
        }

    @builtins.property
    def accelerator_count(self) -> jsii.Number:
        '''The number of the accelerator cards of this type exposed to this instance.

        Often restricted to one of 1, 2, 4, or 8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_count GoogleDataprocCluster#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        assert result is not None, "Required property 'accelerator_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def accelerator_type(self) -> builtins.str:
        '''The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#accelerator_type GoogleDataprocCluster#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        assert result is not None, "Required property 'accelerator_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigWorkerConfigAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6ac02a2f695e2360dc03eff326093c7e7d4f0bf9e29b72d43a8a8389e497c9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b140652aaf8383f0a8b5e70fe947a0b1ab1df860e39a1620d77391d8f5de8c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9e9f1c6e19742fa8a55c493a3333df67d4556bdfbdea146d6c71b55753e361)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35beb363fb9c23e70a8e5b7708da01c6c198be682580798716aa16f0dc131d5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34f0db3256b84926d3cf0e8309deb6d3d9a301b370067f107df0897003e9249b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf311a5aaf7618e93d63e9d5bd62edf80606ca6ea57b56a3b0905736318c8961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cf64b3b2ce80675ddfe8e476156d92921083e219c7973744a7dc911d753a8f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ead2b3bf2a69953adcf54834add3897fa71fffa51edeff9bd2d7cdf56a235fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e51c088446445ae0f05551cb5f67e83026f1e8effb4a62dad5fc6275425469e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146aaa2154026cd8ef1b83007fb16936defacf0c78de8d540bbce71124aec0f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "local_ssd_interface": "localSsdInterface",
        "num_local_ssds": "numLocalSsds",
    },
)
class GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        local_ssd_interface: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        :param local_ssd_interface: Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0035a455829a02e384052ea9f5367d76f19790f0927a8020778e312247e1366)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument local_ssd_interface", value=local_ssd_interface, expected_type=type_hints["local_ssd_interface"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if local_ssd_interface is not None:
            self._values["local_ssd_interface"] = local_ssd_interface
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the primary disk attached to each node, specified in GB.

        The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_interface(self) -> typing.Optional[builtins.str]:
        '''Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        '''
        result = self._values.get("local_ssd_interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f07779734eb1506c2d905bbda50d6714d71e5c644d3719915624fedf0e390e09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetLocalSsdInterface")
    def reset_local_ssd_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdInterface", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdInterfaceInput")
    def local_ssd_interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localSsdInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7411716a839ba5c1b1004f330efd84e82b8ed2b483e463a2f30f268f24410db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e430099562eb020018548bd1e53966716b0a85cb35117d5c7986e2a2546de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdInterface")
    def local_ssd_interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSsdInterface"))

    @local_ssd_interface.setter
    def local_ssd_interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08619a1ee12a1d05fb9f847dc1b3ee9512fc150472cb29cae296dc3d2ecf91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdInterface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71871b19ceeb8447c2febecd78314aa037b7579e3ffc729e7aa58c4e7af82c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92330b323f79212c261b7ab64904d784226436d44f819212884ec61677ed0e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterClusterConfigWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterClusterConfigWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e84d47c36575dbe83f9011e98cf803c3bef5d2f20edc5814993d2d6f0f48368c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a9ce12183d92d0d252ae4ad2a5fa20d0235409b0c9957d07cab437bef2dc0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        local_ssd_interface: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_size_gb GoogleDataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#boot_disk_type GoogleDataprocCluster#boot_disk_type}
        :param local_ssd_interface: Interface type of local SSDs (default is "scsi"). Valid values: "scsi" (Small Computer System Interface), "nvme" (Non-Volatile Memory Express). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_interface GoogleDataprocCluster#local_ssd_interface}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#num_local_ssds GoogleDataprocCluster#num_local_ssds}
        '''
        value = GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            local_ssd_interface=local_ssd_interface,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetImageUri")
    def reset_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageUri", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetMinNumInstances")
    def reset_min_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNumInstances", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(
        self,
    ) -> GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsList:
        return typing.cast(GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> GoogleDataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference:
        return typing.cast(GoogleDataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="minNumInstancesInput")
    def min_num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNumInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86956c6381dc9b5ab99ab320285b5f4761cb4b687ed1ebe0e7e07b463fc1ca94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6943146cc1b9cbb2718b5562f4b97ad4182535ce3955135d00346481ee9d9268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ee9905ba31e9a5754a091de0716386ab0f7568445f8e3241afbb624604ec13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNumInstances")
    def min_num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNumInstances"))

    @min_num_instances.setter
    def min_num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8322b3b207c75e798e0e71d2ae16bf27674514f232d42e5320bdf3439aac232d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNumInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa43691b00bc6cb462bd1ca1a02cf690eddef5b27b62090e2b530419926c06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c8cc512235bf841f02c3d603dd062404ebc304601aea6b72b8047b5d1caac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterConfig",
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
        "cluster_config": "clusterConfig",
        "graceful_decommission_timeout": "gracefulDecommissionTimeout",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
        "virtual_cluster_config": "virtualClusterConfig",
    },
)
class GoogleDataprocClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        graceful_decommission_timeout: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_cluster_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the cluster, unique within the project and zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#name GoogleDataprocCluster#name}
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cluster_config GoogleDataprocCluster#cluster_config}
        :param graceful_decommission_timeout: The timeout duration which allows graceful decomissioning when you change the number of worker nodes directly through a terraform apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#graceful_decommission_timeout GoogleDataprocCluster#graceful_decommission_timeout}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#id GoogleDataprocCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The list of the labels (key/value pairs) configured on the resource and to be applied to instances in the cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#labels GoogleDataprocCluster#labels}
        :param project: The ID of the project in which the cluster will exist. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#project GoogleDataprocCluster#project}
        :param region: The region in which the cluster and associated nodes will be created in. Defaults to global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#region GoogleDataprocCluster#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#timeouts GoogleDataprocCluster#timeouts}
        :param virtual_cluster_config: virtual_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#virtual_cluster_config GoogleDataprocCluster#virtual_cluster_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cluster_config, dict):
            cluster_config = GoogleDataprocClusterClusterConfig(**cluster_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataprocClusterTimeouts(**timeouts)
        if isinstance(virtual_cluster_config, dict):
            virtual_cluster_config = GoogleDataprocClusterVirtualClusterConfig(**virtual_cluster_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e2efccb4c5966f9419ebe7ee31aee1f95026587e89160caa47377f262bdb98)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
            check_type(argname="argument graceful_decommission_timeout", value=graceful_decommission_timeout, expected_type=type_hints["graceful_decommission_timeout"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_cluster_config", value=virtual_cluster_config, expected_type=type_hints["virtual_cluster_config"])
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
        if cluster_config is not None:
            self._values["cluster_config"] = cluster_config
        if graceful_decommission_timeout is not None:
            self._values["graceful_decommission_timeout"] = graceful_decommission_timeout
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_cluster_config is not None:
            self._values["virtual_cluster_config"] = virtual_cluster_config

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
        '''The name of the cluster, unique within the project and zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#name GoogleDataprocCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_config(self) -> typing.Optional[GoogleDataprocClusterClusterConfig]:
        '''cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#cluster_config GoogleDataprocCluster#cluster_config}
        '''
        result = self._values.get("cluster_config")
        return typing.cast(typing.Optional[GoogleDataprocClusterClusterConfig], result)

    @builtins.property
    def graceful_decommission_timeout(self) -> typing.Optional[builtins.str]:
        '''The timeout duration which allows graceful decomissioning when you change the number of worker nodes directly through a terraform apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#graceful_decommission_timeout GoogleDataprocCluster#graceful_decommission_timeout}
        '''
        result = self._values.get("graceful_decommission_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#id GoogleDataprocCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The list of the labels (key/value pairs) configured on the resource and to be applied to instances in the cluster.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#labels GoogleDataprocCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the cluster will exist.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#project GoogleDataprocCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region in which the cluster and associated nodes will be created in. Defaults to global.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#region GoogleDataprocCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataprocClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#timeouts GoogleDataprocCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataprocClusterTimeouts"], result)

    @builtins.property
    def virtual_cluster_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfig"]:
        '''virtual_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#virtual_cluster_config GoogleDataprocCluster#virtual_cluster_config}
        '''
        result = self._values.get("virtual_cluster_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataprocClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#create GoogleDataprocCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#delete GoogleDataprocCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#update GoogleDataprocCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29812e67b977274a75209050cb7035f6879405aa04d3a07f668ef6f44880590e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#create GoogleDataprocCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#delete GoogleDataprocCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#update GoogleDataprocCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3821da276cd34bf07e3dd945307e622f1f1585eb14edad1561427af7559b356)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d99914f870dcdf3f7c465cbd998580ce3aad2560974845af65a3809871617c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712f29410e33407317561d76117f6e7cb927ce63900146caa52106ebfd66fedf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4969fb4031241b2f7b38334271de77e1a1b3ba4ca3794751fab0dc95a4289084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d282550e818ce80be9fa098e7c6d63a2e263b446cc99f1c540a34e95ef5ce292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auxiliary_services_config": "auxiliaryServicesConfig",
        "kubernetes_cluster_config": "kubernetesClusterConfig",
        "staging_bucket": "stagingBucket",
    },
)
class GoogleDataprocClusterVirtualClusterConfig:
    def __init__(
        self,
        *,
        auxiliary_services_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes_cluster_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auxiliary_services_config: auxiliary_services_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auxiliary_services_config GoogleDataprocCluster#auxiliary_services_config}
        :param kubernetes_cluster_config: kubernetes_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_cluster_config GoogleDataprocCluster#kubernetes_cluster_config}
        :param staging_bucket: A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#staging_bucket GoogleDataprocCluster#staging_bucket}
        '''
        if isinstance(auxiliary_services_config, dict):
            auxiliary_services_config = GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig(**auxiliary_services_config)
        if isinstance(kubernetes_cluster_config, dict):
            kubernetes_cluster_config = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig(**kubernetes_cluster_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9375db8791120629cfeb7dffe56ba48d4f7ca6b3a205173975270acb6283078e)
            check_type(argname="argument auxiliary_services_config", value=auxiliary_services_config, expected_type=type_hints["auxiliary_services_config"])
            check_type(argname="argument kubernetes_cluster_config", value=kubernetes_cluster_config, expected_type=type_hints["kubernetes_cluster_config"])
            check_type(argname="argument staging_bucket", value=staging_bucket, expected_type=type_hints["staging_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auxiliary_services_config is not None:
            self._values["auxiliary_services_config"] = auxiliary_services_config
        if kubernetes_cluster_config is not None:
            self._values["kubernetes_cluster_config"] = kubernetes_cluster_config
        if staging_bucket is not None:
            self._values["staging_bucket"] = staging_bucket

    @builtins.property
    def auxiliary_services_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig"]:
        '''auxiliary_services_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#auxiliary_services_config GoogleDataprocCluster#auxiliary_services_config}
        '''
        result = self._values.get("auxiliary_services_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig"], result)

    @builtins.property
    def kubernetes_cluster_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig"]:
        '''kubernetes_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_cluster_config GoogleDataprocCluster#kubernetes_cluster_config}
        '''
        result = self._values.get("kubernetes_cluster_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig"], result)

    @builtins.property
    def staging_bucket(self) -> typing.Optional[builtins.str]:
        '''A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output.

        If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#staging_bucket GoogleDataprocCluster#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metastore_config": "metastoreConfig",
        "spark_history_server_config": "sparkHistoryServerConfig",
    },
)
class GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig:
    def __init__(
        self,
        *,
        metastore_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_history_server_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_config: metastore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metastore_config GoogleDataprocCluster#metastore_config}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#spark_history_server_config GoogleDataprocCluster#spark_history_server_config}
        '''
        if isinstance(metastore_config, dict):
            metastore_config = GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig(**metastore_config)
        if isinstance(spark_history_server_config, dict):
            spark_history_server_config = GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig(**spark_history_server_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a76eaa9e092ed747fb84c4c12a594aae73cd89d9c402f047bc8b8f43f3d2b2b)
            check_type(argname="argument metastore_config", value=metastore_config, expected_type=type_hints["metastore_config"])
            check_type(argname="argument spark_history_server_config", value=spark_history_server_config, expected_type=type_hints["spark_history_server_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metastore_config is not None:
            self._values["metastore_config"] = metastore_config
        if spark_history_server_config is not None:
            self._values["spark_history_server_config"] = spark_history_server_config

    @builtins.property
    def metastore_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig"]:
        '''metastore_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metastore_config GoogleDataprocCluster#metastore_config}
        '''
        result = self._values.get("metastore_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig"], result)

    @builtins.property
    def spark_history_server_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig"]:
        '''spark_history_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#spark_history_server_config GoogleDataprocCluster#spark_history_server_config}
        '''
        result = self._values.get("spark_history_server_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_metastore_service": "dataprocMetastoreService"},
)
class GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig:
    def __init__(
        self,
        *,
        dataproc_metastore_service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_metastore_service: The Hive Metastore configuration for this workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metastore_service GoogleDataprocCluster#dataproc_metastore_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d335dd11e53e08ea4d84dce38729c1c38cbdb52347ba02fabe359476e58dd73)
            check_type(argname="argument dataproc_metastore_service", value=dataproc_metastore_service, expected_type=type_hints["dataproc_metastore_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_metastore_service is not None:
            self._values["dataproc_metastore_service"] = dataproc_metastore_service

    @builtins.property
    def dataproc_metastore_service(self) -> typing.Optional[builtins.str]:
        '''The Hive Metastore configuration for this workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metastore_service GoogleDataprocCluster#dataproc_metastore_service}
        '''
        result = self._values.get("dataproc_metastore_service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d737d9190f6dcb4393c9716e0c5224c9c5ee7e730ce9b60f691373ce3173faf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataprocMetastoreService")
    def reset_dataproc_metastore_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocMetastoreService", []))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreServiceInput")
    def dataproc_metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocMetastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreService")
    def dataproc_metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocMetastoreService"))

    @dataproc_metastore_service.setter
    def dataproc_metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cb0428ed80db5570aaebdf2d81061d450441aaa622a174d959fa506d2740ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocMetastoreService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19394319f7a920e7fb6a48f7eb1eb313d54a022cabde3148ec88c2e0a3222f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01be3985d429dce1ed77373316f32c1557075a2f9c4c95391048c36229a2bf09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetastoreConfig")
    def put_metastore_config(
        self,
        *,
        dataproc_metastore_service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_metastore_service: The Hive Metastore configuration for this workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_metastore_service GoogleDataprocCluster#dataproc_metastore_service}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig(
            dataproc_metastore_service=dataproc_metastore_service
        )

        return typing.cast(None, jsii.invoke(self, "putMetastoreConfig", [value]))

    @jsii.member(jsii_name="putSparkHistoryServerConfig")
    def put_spark_history_server_config(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_cluster GoogleDataprocCluster#dataproc_cluster}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig(
            dataproc_cluster=dataproc_cluster
        )

        return typing.cast(None, jsii.invoke(self, "putSparkHistoryServerConfig", [value]))

    @jsii.member(jsii_name="resetMetastoreConfig")
    def reset_metastore_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreConfig", []))

    @jsii.member(jsii_name="resetSparkHistoryServerConfig")
    def reset_spark_history_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkHistoryServerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="metastoreConfig")
    def metastore_config(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference, jsii.get(self, "metastoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfig")
    def spark_history_server_config(
        self,
    ) -> "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference":
        return typing.cast("GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference", jsii.get(self, "sparkHistoryServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreConfigInput")
    def metastore_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig], jsii.get(self, "metastoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfigInput")
    def spark_history_server_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig"], jsii.get(self, "sparkHistoryServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa959ec0b75fff6816352642632346628a70137142dcbf0408bb01492c809ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_cluster": "dataprocCluster"},
)
class GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig:
    def __init__(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_cluster GoogleDataprocCluster#dataproc_cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e36840832b5f11b5df7f763027a50adbdc70e034212b890dbcf9e18b81c161)
            check_type(argname="argument dataproc_cluster", value=dataproc_cluster, expected_type=type_hints["dataproc_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_cluster is not None:
            self._values["dataproc_cluster"] = dataproc_cluster

    @builtins.property
    def dataproc_cluster(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#dataproc_cluster GoogleDataprocCluster#dataproc_cluster}
        '''
        result = self._values.get("dataproc_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5991989304e0e915e75d5f427fab74906950136879a959fcf7b4acf091af3373)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataprocCluster")
    def reset_dataproc_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocCluster", []))

    @builtins.property
    @jsii.member(jsii_name="dataprocClusterInput")
    def dataproc_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocCluster")
    def dataproc_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocCluster"))

    @dataproc_cluster.setter
    def dataproc_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8fd5ce9569dba5824bd52ea86742fbad79b44ac14ae0352c3bdcccf7cf763a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca23ed6ebd03033f838eb106149155ff3612504a0e9fe94ce2ae70302f9b9781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "gke_cluster_config": "gkeClusterConfig",
        "kubernetes_software_config": "kubernetesSoftwareConfig",
        "kubernetes_namespace": "kubernetesNamespace",
    },
)
class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig:
    def __init__(
        self,
        *,
        gke_cluster_config: typing.Union["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig", typing.Dict[builtins.str, typing.Any]],
        kubernetes_software_config: typing.Union["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig", typing.Dict[builtins.str, typing.Any]],
        kubernetes_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gke_cluster_config: gke_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gke_cluster_config GoogleDataprocCluster#gke_cluster_config}
        :param kubernetes_software_config: kubernetes_software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_software_config GoogleDataprocCluster#kubernetes_software_config}
        :param kubernetes_namespace: A namespace within the Kubernetes cluster to deploy into. If this namespace does not exist, it is created. If it exists, Dataproc verifies that another Dataproc VirtualCluster is not installed into it. If not specified, the name of the Dataproc Cluster is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_namespace GoogleDataprocCluster#kubernetes_namespace}
        '''
        if isinstance(gke_cluster_config, dict):
            gke_cluster_config = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig(**gke_cluster_config)
        if isinstance(kubernetes_software_config, dict):
            kubernetes_software_config = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig(**kubernetes_software_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17580f49e01f3e70e3730ce85c5995594f102476d77ddadb9dcc416be3e97028)
            check_type(argname="argument gke_cluster_config", value=gke_cluster_config, expected_type=type_hints["gke_cluster_config"])
            check_type(argname="argument kubernetes_software_config", value=kubernetes_software_config, expected_type=type_hints["kubernetes_software_config"])
            check_type(argname="argument kubernetes_namespace", value=kubernetes_namespace, expected_type=type_hints["kubernetes_namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gke_cluster_config": gke_cluster_config,
            "kubernetes_software_config": kubernetes_software_config,
        }
        if kubernetes_namespace is not None:
            self._values["kubernetes_namespace"] = kubernetes_namespace

    @builtins.property
    def gke_cluster_config(
        self,
    ) -> "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig":
        '''gke_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gke_cluster_config GoogleDataprocCluster#gke_cluster_config}
        '''
        result = self._values.get("gke_cluster_config")
        assert result is not None, "Required property 'gke_cluster_config' is missing"
        return typing.cast("GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig", result)

    @builtins.property
    def kubernetes_software_config(
        self,
    ) -> "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig":
        '''kubernetes_software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_software_config GoogleDataprocCluster#kubernetes_software_config}
        '''
        result = self._values.get("kubernetes_software_config")
        assert result is not None, "Required property 'kubernetes_software_config' is missing"
        return typing.cast("GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig", result)

    @builtins.property
    def kubernetes_namespace(self) -> typing.Optional[builtins.str]:
        '''A namespace within the Kubernetes cluster to deploy into.

        If this namespace does not exist, it is created. If it exists, Dataproc verifies that another Dataproc VirtualCluster is not installed into it. If not specified, the name of the Dataproc Cluster is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_namespace GoogleDataprocCluster#kubernetes_namespace}
        '''
        result = self._values.get("kubernetes_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "gke_cluster_target": "gkeClusterTarget",
        "node_pool_target": "nodePoolTarget",
    },
)
class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig:
    def __init__(
        self,
        *,
        gke_cluster_target: typing.Optional[builtins.str] = None,
        node_pool_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gke_cluster_target: A target GKE cluster to deploy to. It must be in the same project and region as the Dataproc cluster (the GKE cluster can be zonal or regional). Format: 'projects/{project}/locations/{location}/clusters/{cluster_id}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gke_cluster_target GoogleDataprocCluster#gke_cluster_target}
        :param node_pool_target: node_pool_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_pool_target GoogleDataprocCluster#node_pool_target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4877ac9de35753ea78d4e8d906d67147cdf5be7c71f7de7540ea51a73aa30530)
            check_type(argname="argument gke_cluster_target", value=gke_cluster_target, expected_type=type_hints["gke_cluster_target"])
            check_type(argname="argument node_pool_target", value=node_pool_target, expected_type=type_hints["node_pool_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gke_cluster_target is not None:
            self._values["gke_cluster_target"] = gke_cluster_target
        if node_pool_target is not None:
            self._values["node_pool_target"] = node_pool_target

    @builtins.property
    def gke_cluster_target(self) -> typing.Optional[builtins.str]:
        '''A target GKE cluster to deploy to.

        It must be in the same project and region as the Dataproc cluster (the GKE cluster can be zonal or regional). Format: 'projects/{project}/locations/{location}/clusters/{cluster_id}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gke_cluster_target GoogleDataprocCluster#gke_cluster_target}
        '''
        result = self._values.get("gke_cluster_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_pool_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget"]]]:
        '''node_pool_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_pool_target GoogleDataprocCluster#node_pool_target}
        '''
        result = self._values.get("node_pool_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget",
    jsii_struct_bases=[],
    name_mapping={
        "node_pool": "nodePool",
        "roles": "roles",
        "node_pool_config": "nodePoolConfig",
    },
)
class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget:
    def __init__(
        self,
        *,
        node_pool: builtins.str,
        roles: typing.Sequence[builtins.str],
        node_pool_config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool: The target GKE node pool. Format: 'projects/{project}/locations/{location}/clusters/{cluster}/nodePools/{nodePool}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_pool GoogleDataprocCluster#node_pool}
        :param roles: The roles associated with the GKE node pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#roles GoogleDataprocCluster#roles}
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_pool_config GoogleDataprocCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d860262fb535697e10d9a3c15def134789c4e811edef3451d7cebeb85bd26ce9)
            check_type(argname="argument node_pool", value=node_pool, expected_type=type_hints["node_pool"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_pool": node_pool,
            "roles": roles,
        }
        if node_pool_config is not None:
            self._values["node_pool_config"] = node_pool_config

    @builtins.property
    def node_pool(self) -> builtins.str:
        '''The target GKE node pool. Format: 'projects/{project}/locations/{location}/clusters/{cluster}/nodePools/{nodePool}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_pool GoogleDataprocCluster#node_pool}
        '''
        result = self._values.get("node_pool")
        assert result is not None, "Required property 'node_pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(self) -> typing.List[builtins.str]:
        '''The roles associated with the GKE node pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#roles GoogleDataprocCluster#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def node_pool_config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig"]:
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_pool_config GoogleDataprocCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66d07078c247c181dea6b87b27bad4289dd5bfeccbfc627fc0cf8201e769ff96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61eaff8d3cbb1b63b5683b0f4aeeff5d1b169759fad9080d6dafcafc398e8dde)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7b57e55e1dfa7293eb40563009c14845b3dbc57c56e32aca315ae39e419df4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d246776c52c1c6610b0178ff0807ac585f41601757052abea7073099c03d6e5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__958c28d6e719e955a0e05ef490c54f5287b5a1230856a51c9cf8758f348d16ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e735605cdf7c746b431856d35b6454edb46148dc586c27f5ada34958ca07be27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "locations": "locations",
        "autoscaling": "autoscaling",
        "config": "config",
    },
)
class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig:
    def __init__(
        self,
        *,
        locations: typing.Sequence[builtins.str],
        autoscaling: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling", typing.Dict[builtins.str, typing.Any]]] = None,
        config: typing.Optional[typing.Union["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param locations: The list of Compute Engine zones where node pool nodes associated with a Dataproc on GKE virtual cluster will be located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#locations GoogleDataprocCluster#locations}
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#autoscaling GoogleDataprocCluster#autoscaling}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#config GoogleDataprocCluster#config}
        '''
        if isinstance(autoscaling, dict):
            autoscaling = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling(**autoscaling)
        if isinstance(config, dict):
            config = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13996631c51c0e6ccc110a68ec1e34edaf706505c59f5d4731f130f372362c5)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument autoscaling", value=autoscaling, expected_type=type_hints["autoscaling"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }
        if autoscaling is not None:
            self._values["autoscaling"] = autoscaling
        if config is not None:
            self._values["config"] = config

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''The list of Compute Engine zones where node pool nodes associated with a Dataproc on GKE virtual cluster will be located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#locations GoogleDataprocCluster#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def autoscaling(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling"]:
        '''autoscaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#autoscaling GoogleDataprocCluster#autoscaling}
        '''
        result = self._values.get("autoscaling")
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling"], result)

    @builtins.property
    def config(
        self,
    ) -> typing.Optional["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#config GoogleDataprocCluster#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling:
    def __init__(
        self,
        *,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum number of nodes in the node pool. Must be >= minNodeCount, and must be > 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#max_node_count GoogleDataprocCluster#max_node_count}
        :param min_node_count: The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_node_count GoogleDataprocCluster#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c28b01521bb85c40902a4d7cd84f72f129625edf8f2b2472df0effaf01f6d3e)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_node_count is not None:
            self._values["max_node_count"] = max_node_count
        if min_node_count is not None:
            self._values["min_node_count"] = min_node_count

    @builtins.property
    def max_node_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of nodes in the node pool. Must be >= minNodeCount, and must be > 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#max_node_count GoogleDataprocCluster#max_node_count}
        '''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_node_count GoogleDataprocCluster#min_node_count}
        '''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6826447bdb2b3ea0e53f5d531a35ac71f1b58ff52cf90ff4b21d9f541f135670)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxNodeCount")
    def reset_max_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodeCount", []))

    @jsii.member(jsii_name="resetMinNodeCount")
    def reset_min_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d294f57cc8a230c68db929f72479fcf5a0652b62df907de4455c17eec155d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341c61c067d4488d58e2ae4bfa68332367625a3445573fdbde0b8f77887c6d8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b112adce23bc8d21406bb163834d86d8cd23a95d82b027831473eff201b6a344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig",
    jsii_struct_bases=[],
    name_mapping={
        "local_ssd_count": "localSsdCount",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "preemptible": "preemptible",
        "spot": "spot",
    },
)
class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig:
    def __init__(
        self,
        *,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_ssd_count: The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_count GoogleDataprocCluster#local_ssd_count}
        :param machine_type: The name of a Compute Engine machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        :param min_cpu_platform: Minimum CPU platform to be used by this instance. The instance may be scheduled on the specified or a newer CPU platform. Specify the friendly names of CPU platforms, such as "Intel Haswell" or "Intel Sandy Bridge". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        :param preemptible: Whether the nodes are created as preemptible VM instances. Preemptible nodes cannot be used in a node pool with the CONTROLLER role or in the DEFAULT node pool if the CONTROLLER role is not assigned (the DEFAULT node pool will assume the CONTROLLER role). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptible GoogleDataprocCluster#preemptible}
        :param spot: Spot flag for enabling Spot VM, which is a rebrand of the existing preemptible flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#spot GoogleDataprocCluster#spot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7af4aa5f220eaad9d6f4351903326f6069d0f035395201b8c8be74f6d497119)
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument preemptible", value=preemptible, expected_type=type_hints["preemptible"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if local_ssd_count is not None:
            self._values["local_ssd_count"] = local_ssd_count
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if preemptible is not None:
            self._values["preemptible"] = preemptible
        if spot is not None:
            self._values["spot"] = spot

    @builtins.property
    def local_ssd_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_count GoogleDataprocCluster#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Compute Engine machine type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Minimum CPU platform to be used by this instance.

        The instance may be scheduled on the specified or a newer CPU platform. Specify the friendly names of CPU platforms, such as "Intel Haswell" or "Intel Sandy Bridge".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preemptible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes are created as preemptible VM instances.

        Preemptible nodes cannot be used in a node pool with the CONTROLLER role or in the DEFAULT node pool if the CONTROLLER role is not assigned (the DEFAULT node pool will assume the CONTROLLER role).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptible GoogleDataprocCluster#preemptible}
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def spot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Spot flag for enabling Spot VM, which is a rebrand of the existing preemptible flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#spot GoogleDataprocCluster#spot}
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9527cc7ad79b3d3f56009f7b6aea425e98d9eaad46f3f1bfe1368cf387fbaabd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocalSsdCount")
    def reset_local_ssd_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdCount", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetPreemptible")
    def reset_preemptible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptible", []))

    @jsii.member(jsii_name="resetSpot")
    def reset_spot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpot", []))

    @builtins.property
    @jsii.member(jsii_name="localSsdCountInput")
    def local_ssd_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "localSsdCountInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibleInput")
    def preemptible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preemptibleInput"))

    @builtins.property
    @jsii.member(jsii_name="spotInput")
    def spot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "spotInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd101dfa48e91d257e1bd82ef354dda7aa74133993a9c285f421a1e3eeefd59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a33ee07bf6a8e9a229a51559493e54ddb73ca6e351bb40065ffd56b5c3dc13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c59d7a7e10c913dc94ce6d9e96e7fc9592c2a925e56e1f1fb93f3b7ce603572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptible")
    def preemptible(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preemptible"))

    @preemptible.setter
    def preemptible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de35983218ebcc8d8dfcd3e1fcb8defe035c1d52bd7adccd1f810a303d0479dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "spot"))

    @spot.setter
    def spot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0622046780134b6fdfdcffc2fb0954f7f2d08fb30877bf7803bb67676fc75a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772bf7b93bbb754792542d3ad60fb4c3e89b88fa4f526ccf5dd2ec3c379b6c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9ae2cd57670f4e63b3482077bfb9373568e0534f7c5dadcff6dbd9e586abea3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscaling")
    def put_autoscaling(
        self,
        *,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum number of nodes in the node pool. Must be >= minNodeCount, and must be > 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#max_node_count GoogleDataprocCluster#max_node_count}
        :param min_node_count: The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_node_count GoogleDataprocCluster#min_node_count}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaling", [value]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_ssd_count: The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#local_ssd_count GoogleDataprocCluster#local_ssd_count}
        :param machine_type: The name of a Compute Engine machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#machine_type GoogleDataprocCluster#machine_type}
        :param min_cpu_platform: Minimum CPU platform to be used by this instance. The instance may be scheduled on the specified or a newer CPU platform. Specify the friendly names of CPU platforms, such as "Intel Haswell" or "Intel Sandy Bridge". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#min_cpu_platform GoogleDataprocCluster#min_cpu_platform}
        :param preemptible: Whether the nodes are created as preemptible VM instances. Preemptible nodes cannot be used in a node pool with the CONTROLLER role or in the DEFAULT node pool if the CONTROLLER role is not assigned (the DEFAULT node pool will assume the CONTROLLER role). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#preemptible GoogleDataprocCluster#preemptible}
        :param spot: Spot flag for enabling Spot VM, which is a rebrand of the existing preemptible flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#spot GoogleDataprocCluster#spot}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig(
            local_ssd_count=local_ssd_count,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            preemptible=preemptible,
            spot=spot,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetAutoscaling")
    def reset_autoscaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaling", []))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoscaling")
    def autoscaling(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference, jsii.get(self, "autoscaling"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingInput")
    def autoscaling_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling], jsii.get(self, "autoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f659d9a7d817b7be7437d5611ef7fadd9bedee4afd52bce7e1f55562a95e2183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff7a7d2a397799f224008e4ec24c3f7fbf41265e269a138b9e64dd06494bcc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__407001a7614a800255af67361d6e4346cab15264dfeef16009ac807366b1502b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        locations: typing.Sequence[builtins.str],
        autoscaling: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
        config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param locations: The list of Compute Engine zones where node pool nodes associated with a Dataproc on GKE virtual cluster will be located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#locations GoogleDataprocCluster#locations}
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#autoscaling GoogleDataprocCluster#autoscaling}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#config GoogleDataprocCluster#config}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig(
            locations=locations, autoscaling=autoscaling, config=config
        )

        return typing.cast(None, jsii.invoke(self, "putNodePoolConfig", [value]))

    @jsii.member(jsii_name="resetNodePoolConfig")
    def reset_node_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePoolConfig", []))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfig")
    def node_pool_config(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolInput")
    def node_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePool")
    def node_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodePool"))

    @node_pool.setter
    def node_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4db279234a98c87d95057c692a586794de1224c10af7676f9193fac2fe9c083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd23ba3fc4c9dddf8e6d1acb8d5eb08aa3092cf6bb34890b09a6714b6e6cb369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aeb1701a1b5fceb2ec7940a7dc0b30bb800523509aecb2fd788b805967e6117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fde588c384d20becea82dce1a4723cd2d10ea048efd3944ebbfa5a7b4ebd9f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolTarget")
    def put_node_pool_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673247c88091356832030d8519e0352121d23d710052c2e91e617d98b65d9a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodePoolTarget", [value]))

    @jsii.member(jsii_name="resetGkeClusterTarget")
    def reset_gke_cluster_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeClusterTarget", []))

    @jsii.member(jsii_name="resetNodePoolTarget")
    def reset_node_pool_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePoolTarget", []))

    @builtins.property
    @jsii.member(jsii_name="nodePoolTarget")
    def node_pool_target(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList, jsii.get(self, "nodePoolTarget"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterTargetInput")
    def gke_cluster_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeClusterTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolTargetInput")
    def node_pool_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]], jsii.get(self, "nodePoolTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterTarget")
    def gke_cluster_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gkeClusterTarget"))

    @gke_cluster_target.setter
    def gke_cluster_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9030371ca24fe25035118e2a8cb3beccbe64fd11966e2967fb602d4bbfd8e3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeClusterTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e1b5e679b4d5ca5277cb2bf9aebf13d8af9bfa850eb86aa3becf894b12c326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={"component_version": "componentVersion", "properties": "properties"},
)
class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig:
    def __init__(
        self,
        *,
        component_version: typing.Mapping[builtins.str, builtins.str],
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param component_version: The components that should be installed in this Dataproc cluster. The key must be a string from the KubernetesComponent enumeration. The value is the version of the software to be installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#component_version GoogleDataprocCluster#component_version}
        :param properties: The properties to set on daemon config files. Property keys are specified in prefix:property format, for example spark:spark.kubernetes.container.image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#properties GoogleDataprocCluster#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfe4c5c0dbddce37aa72e290c764f017c615be4ac761968dfcb61ff1fe6c42e)
            check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_version": component_version,
        }
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def component_version(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The components that should be installed in this Dataproc cluster.

        The key must be a string from the KubernetesComponent enumeration. The value is the version of the software to be installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#component_version GoogleDataprocCluster#component_version}
        '''
        result = self._values.get("component_version")
        assert result is not None, "Required property 'component_version' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The properties to set on daemon config files. Property keys are specified in prefix:property format, for example spark:spark.kubernetes.container.image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#properties GoogleDataprocCluster#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd6a4e5c3bab38ed8bdb0a08a969e49c36267b3988abcb28b2c366c8e12e002c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="componentVersionInput")
    def component_version_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "componentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="componentVersion")
    def component_version(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "componentVersion"))

    @component_version.setter
    def component_version(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df533a87b8c6de7144fe6ca7052a71203be8b8b8ace9276ad3d30566f69fe4a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9556ef2e4bb459c66faa74c491cc79dfdfe34f01b9735d0c1232f06420d6d094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c1cc12da44f49bc54be94e797d7d2969917604b97b6b189de40a885cb564cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62bf99a95e107cfc6d66fd80374f2ded7c1bef5aff060ea6a211b921b67f1d30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGkeClusterConfig")
    def put_gke_cluster_config(
        self,
        *,
        gke_cluster_target: typing.Optional[builtins.str] = None,
        node_pool_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gke_cluster_target: A target GKE cluster to deploy to. It must be in the same project and region as the Dataproc cluster (the GKE cluster can be zonal or regional). Format: 'projects/{project}/locations/{location}/clusters/{cluster_id}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gke_cluster_target GoogleDataprocCluster#gke_cluster_target}
        :param node_pool_target: node_pool_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#node_pool_target GoogleDataprocCluster#node_pool_target}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig(
            gke_cluster_target=gke_cluster_target, node_pool_target=node_pool_target
        )

        return typing.cast(None, jsii.invoke(self, "putGkeClusterConfig", [value]))

    @jsii.member(jsii_name="putKubernetesSoftwareConfig")
    def put_kubernetes_software_config(
        self,
        *,
        component_version: typing.Mapping[builtins.str, builtins.str],
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param component_version: The components that should be installed in this Dataproc cluster. The key must be a string from the KubernetesComponent enumeration. The value is the version of the software to be installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#component_version GoogleDataprocCluster#component_version}
        :param properties: The properties to set on daemon config files. Property keys are specified in prefix:property format, for example spark:spark.kubernetes.container.image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#properties GoogleDataprocCluster#properties}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig(
            component_version=component_version, properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetesSoftwareConfig", [value]))

    @jsii.member(jsii_name="resetKubernetesNamespace")
    def reset_kubernetes_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterConfig")
    def gke_cluster_config(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference, jsii.get(self, "gkeClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesSoftwareConfig")
    def kubernetes_software_config(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference, jsii.get(self, "kubernetesSoftwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterConfigInput")
    def gke_cluster_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig], jsii.get(self, "gkeClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNamespaceInput")
    def kubernetes_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesSoftwareConfigInput")
    def kubernetes_software_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig], jsii.get(self, "kubernetesSoftwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNamespace")
    def kubernetes_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesNamespace"))

    @kubernetes_namespace.setter
    def kubernetes_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c496771208ea553bb361e32f2ab0601002aa08ac49a7aa5e854612350351a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473d063e592d4e160787abf9a6a1c64a531b633f3d235aec655369a8a9394825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocClusterVirtualClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocCluster.GoogleDataprocClusterVirtualClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acc73a2e6c2927d25c214a11db20a1dad7f0972ed865dad22ca6fcacbc633a47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuxiliaryServicesConfig")
    def put_auxiliary_services_config(
        self,
        *,
        metastore_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        spark_history_server_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_config: metastore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#metastore_config GoogleDataprocCluster#metastore_config}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#spark_history_server_config GoogleDataprocCluster#spark_history_server_config}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig(
            metastore_config=metastore_config,
            spark_history_server_config=spark_history_server_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAuxiliaryServicesConfig", [value]))

    @jsii.member(jsii_name="putKubernetesClusterConfig")
    def put_kubernetes_cluster_config(
        self,
        *,
        gke_cluster_config: typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig, typing.Dict[builtins.str, typing.Any]],
        kubernetes_software_config: typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig, typing.Dict[builtins.str, typing.Any]],
        kubernetes_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gke_cluster_config: gke_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#gke_cluster_config GoogleDataprocCluster#gke_cluster_config}
        :param kubernetes_software_config: kubernetes_software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_software_config GoogleDataprocCluster#kubernetes_software_config}
        :param kubernetes_namespace: A namespace within the Kubernetes cluster to deploy into. If this namespace does not exist, it is created. If it exists, Dataproc verifies that another Dataproc VirtualCluster is not installed into it. If not specified, the name of the Dataproc Cluster is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_cluster#kubernetes_namespace GoogleDataprocCluster#kubernetes_namespace}
        '''
        value = GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig(
            gke_cluster_config=gke_cluster_config,
            kubernetes_software_config=kubernetes_software_config,
            kubernetes_namespace=kubernetes_namespace,
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetesClusterConfig", [value]))

    @jsii.member(jsii_name="resetAuxiliaryServicesConfig")
    def reset_auxiliary_services_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuxiliaryServicesConfig", []))

    @jsii.member(jsii_name="resetKubernetesClusterConfig")
    def reset_kubernetes_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesClusterConfig", []))

    @jsii.member(jsii_name="resetStagingBucket")
    def reset_staging_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingBucket", []))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryServicesConfig")
    def auxiliary_services_config(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference, jsii.get(self, "auxiliaryServicesConfig"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesClusterConfig")
    def kubernetes_cluster_config(
        self,
    ) -> GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference:
        return typing.cast(GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference, jsii.get(self, "kubernetesClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryServicesConfigInput")
    def auxiliary_services_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig], jsii.get(self, "auxiliaryServicesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesClusterConfigInput")
    def kubernetes_cluster_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig], jsii.get(self, "kubernetesClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucketInput")
    def staging_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e184bc7d3483615a39029379d6b38f8687355b867fb657c638bfa78c619cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocClusterVirtualClusterConfig]:
        return typing.cast(typing.Optional[GoogleDataprocClusterVirtualClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocClusterVirtualClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb01824e257485a4dbfa6411aaeb0c9995f9b548acec2e344a9887c177ef9d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataprocCluster",
    "GoogleDataprocClusterClusterConfig",
    "GoogleDataprocClusterClusterConfigAutoscalingConfig",
    "GoogleDataprocClusterClusterConfigAutoscalingConfigOutputReference",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsList",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupList",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsList",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAcceleratorsOutputReference",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfigOutputReference",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigOutputReference",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupOutputReference",
    "GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsOutputReference",
    "GoogleDataprocClusterClusterConfigDataprocMetricConfig",
    "GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics",
    "GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsList",
    "GoogleDataprocClusterClusterConfigDataprocMetricConfigMetricsOutputReference",
    "GoogleDataprocClusterClusterConfigDataprocMetricConfigOutputReference",
    "GoogleDataprocClusterClusterConfigEncryptionConfig",
    "GoogleDataprocClusterClusterConfigEncryptionConfigOutputReference",
    "GoogleDataprocClusterClusterConfigEndpointConfig",
    "GoogleDataprocClusterClusterConfigEndpointConfigOutputReference",
    "GoogleDataprocClusterClusterConfigGceClusterConfig",
    "GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig",
    "GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfigOutputReference",
    "GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity",
    "GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinityOutputReference",
    "GoogleDataprocClusterClusterConfigGceClusterConfigOutputReference",
    "GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity",
    "GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinityOutputReference",
    "GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig",
    "GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference",
    "GoogleDataprocClusterClusterConfigInitializationAction",
    "GoogleDataprocClusterClusterConfigInitializationActionList",
    "GoogleDataprocClusterClusterConfigInitializationActionOutputReference",
    "GoogleDataprocClusterClusterConfigLifecycleConfig",
    "GoogleDataprocClusterClusterConfigLifecycleConfigOutputReference",
    "GoogleDataprocClusterClusterConfigMasterConfig",
    "GoogleDataprocClusterClusterConfigMasterConfigAccelerators",
    "GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsList",
    "GoogleDataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference",
    "GoogleDataprocClusterClusterConfigMasterConfigDiskConfig",
    "GoogleDataprocClusterClusterConfigMasterConfigDiskConfigOutputReference",
    "GoogleDataprocClusterClusterConfigMasterConfigOutputReference",
    "GoogleDataprocClusterClusterConfigMetastoreConfig",
    "GoogleDataprocClusterClusterConfigMetastoreConfigOutputReference",
    "GoogleDataprocClusterClusterConfigOutputReference",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructList",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStructOutputReference",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResults",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsList",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResultsOutputReference",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyOutputReference",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMixOutputReference",
    "GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference",
    "GoogleDataprocClusterClusterConfigSecurityConfig",
    "GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig",
    "GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference",
    "GoogleDataprocClusterClusterConfigSecurityConfigOutputReference",
    "GoogleDataprocClusterClusterConfigSoftwareConfig",
    "GoogleDataprocClusterClusterConfigSoftwareConfigOutputReference",
    "GoogleDataprocClusterClusterConfigWorkerConfig",
    "GoogleDataprocClusterClusterConfigWorkerConfigAccelerators",
    "GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsList",
    "GoogleDataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference",
    "GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig",
    "GoogleDataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference",
    "GoogleDataprocClusterClusterConfigWorkerConfigOutputReference",
    "GoogleDataprocClusterConfig",
    "GoogleDataprocClusterTimeouts",
    "GoogleDataprocClusterTimeoutsOutputReference",
    "GoogleDataprocClusterVirtualClusterConfig",
    "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig",
    "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig",
    "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig",
    "GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference",
    "GoogleDataprocClusterVirtualClusterConfigOutputReference",
]

publication.publish()

def _typecheckingstub__1e6e4cf140d63fdecb4e89d18324b98a20e53ba207b7a2bea5eb6948ff3a5f59(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    cluster_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    graceful_decommission_timeout: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_cluster_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3371dd236143092f68fdb0ccb52dd9310751868564539f180db1f9d58319b1eb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf4d03eb6a2a8dd900d01fdd49a2f17630b8d54c46990f0c7a67defb4cb5004(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0281ff26b47c2f3672c4d0738579af6ffc5d5689147df89b0b90590cb387ff04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c62c4f010bfcb4da124830d10aae5aa087322e0ba70a87289aedf83eb926154(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59be1e0232ef9034dcb7e7892f757533fd0839e778ddec3bb7e645af0f608a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3e8efdc692fff9521f0c1c6eb791862ed41aca9ad932e5dcec76c1a20455d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f61c75254bc37de97d515b7d59338e7a3531c9a53c4da894bd4330c549ad868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5455b5e5505a3c5e687b4a20b2d8cb9083c4f82282e901dd941a884910644ddc(
    *,
    autoscaling_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auxiliary_node_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataproc_metric_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigDataprocMetricConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gce_cluster_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    initialization_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigInitializationAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lifecycle_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigLifecycleConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    master_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigMasterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metastore_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preemptible_worker_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    software_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    staging_bucket: typing.Optional[builtins.str] = None,
    temp_bucket: typing.Optional[builtins.str] = None,
    worker_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0842bb7135b9511d6a7afca06c372f50adbe0f80104e7bcfda830ed9807e258(
    *,
    policy_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe862aa86d13b0581957b211d9b05e1c6c0d87c67f322847d7ab1e4a93a0271a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1916d93c94aa9cb4e475d2d4b0cc52b0d8b05a221669e8e1ccffe049b52ba10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a19fd7b8184a414d1f34536c6655f79a6157377ee62cd7418a86fa948c1317(
    value: typing.Optional[GoogleDataprocClusterClusterConfigAutoscalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9555aabd3f7d925b25ebddd748bb92ff81e5fb9c52c254570f1a7b6e668f6063(
    *,
    node_group: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup, typing.Dict[builtins.str, typing.Any]]]],
    node_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31970e47d962157980cb4c82a6cb71f94234af6103a74ef56e18da7cb00ac68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f4eb757aaeded050c7a739946c2f12dd06ec4f31495e49b04e20b07cc934c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61dade7b6fc726ea16d852cc27260eb45184d9c59a9af71a3f0233fa7d28637a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb7f20bc321b491591a0badc1ea19eb13016aa4b40e2076a74312e6b2f403a6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7a0ce1769cadb7790b6cf32b2ad15845fc98f5862d57068395a4df4bd33518(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2254350dadbf4ca0a08d1310d303d3ee8b4dcdb95fb71ffd5bc3e35f5572145(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36056f1fd973b1cbc227b5b3a30e28bd9d3f3cf790c252181b7472323dd4deb2(
    *,
    roles: typing.Sequence[builtins.str],
    node_group_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff0b0bfb9e19c682d42d65e432498d244e965eccc6dc1ea9506414523f55070(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73c0cde0bd57863ca86000ac94c1bc06f24e2c7e191395f9c2a88dec5906649(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22407fab5cd98aad78fd99b08a144245133facd11d22ba1638debc54c61e1c18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73efb6a85294467f51b0434e3fffa351bec594f8472ed5cd4070c999eb39155(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d28b1528fa3e32684de743e56c0f83c7671bb7ec2f60a16cfb06c663a618b58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31d86b34a89a65a5d304684c4199dcc1ca85e4a9a15641042d6fa1b92483868(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b526dc5755977cd734ad72b1f5baef4dd30c54885d6fcef69392a01581448a7(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    num_instances: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9587f3d804e6d350bb51862043aed63fe83e2864877100325125e21f2b06d46(
    *,
    accelerator_count: jsii.Number,
    accelerator_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6642b77313a6e23de8e7660abc795d30b0ea4d97c3afda0d45b9033755189f9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f55f59c18938398ff38795558ef60d35780304b0d72edf228e8d6632f22ba0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed814afa6b0bf4306ecadef978f1c98fe0352f115ba88228e618e2103e5a0d70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc38761416ffe21163ed81daec986d4d6c726d7231723321e4cb499c5c3cfac9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31c86c203c714ebfa1edc06d4cb37d723f89402a18980a3904a7bddc6edb2b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b24fdd2d7e820264d58a50cedb293df00c7bf7ff8ce6e4941cc90f854da523(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f20b1c953a49fe75750fa008f93ab5309476bf052ec45d17bca7e1422b5b81d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac982484ae90cd5df8147abc3dccee4e9889dd054683ed849bc7d3f9ad05e92(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba79d5ed3ee9cbaeb127c6ea3b671cfab854243c485412cccf6e292fc0e5acb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13514fd9115fe3dbd94fe347909b623f19492ce388c6939e5be483c73850288(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fbd8cd7fa8e5dcaada8bf49ed1d2f9e005cfcb0a4da08c790c0af80191dfe1(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    local_ssd_interface: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f66d7bb4076645d9ba9fbe53a2bd14232f672b9d636c7cccbe288e7d0e60240(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392579c52177929975ee73722416a31d96ad220004455e4edb61707579f66918(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43b7a0d452dd143e95b658de41fbb51d0335f9543e02d2c132eede3f3e3fd48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac78aee3ec00d42bef47129b9a0d9bc972116f32a43be6ab8a55ec25d82349a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400c010b85ce69f14a14d45a7bf4ad95b04636d5231f83a52f3fa0b7d7dfeb7c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8034b9c77202d44269a7fcdb5358f7678abc881ebca8a3941179c6eb79f0c33(
    value: typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd0eeebc4240a4d4c14991869245d6b6c96ca39fe3a7d22aed90bbee4e98a7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d7f2975e9e0f2aeceea1d78276e12d989226661e7aa981e6cd88a57a65f805(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab83c33a49d5cadabc3eca5b08f42cf5eb45ac2f9c48b57a94df90ff07dda042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d951ec133eee1a49203cf6af9001b16fbc11fad89f23461c424d76a8eeaf1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23dd0ac8ad27a4616e150811519e4300f5ab27dcf37c36b80c8035e7529d50d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc37b1a0301fc3ad4a20e4a05c70a0033db58b6ebd6d9e097d8c2ef8ac6c6c0(
    value: typing.Optional[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroupNodeGroupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60ed5ac7832f05e90678d4c79cf062225279c4ba3af4405e6115d2cfdd6d3df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d9c67341fd07c057bb2a8ec0607c0c3571ad988868d49a6a8544eb1525b447(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40d0cf9b7d0dc4e5ab177c879e366e153ea85e5bc1581110d0544337bc48b3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa89dc63ddb336d8c6dfee7399f5b19356e9cbd80c4745c905d7205301cb462(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6a677e39a30e21754cadc345bd662454da0c81794ba20d79917f2d9db7b399(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroupsNodeGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2391cdf97f2fbd13d2409bee1a1f81a37d496911d99991379fc0298e7c5b97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ceb021dc339ac1d8f2294d4676f87062c5706fabc08545990bfe4d8e219a94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beda7e73a7e7953d341d5245943e8658a42d80ca8850c2526ec5978c7e920baa(
    *,
    metrics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb076274218e76a7bd1eb9f4ea18ec9bc6128a8f16c55ee67e3ac5c36a02023(
    *,
    metric_source: builtins.str,
    metric_overrides: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879abfc10172e97c0b4f5eee853bbf2dc40ec94818bdfb0ab58ec99926720561(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952998dc2dda240606244b89eb72e26aa60a1e9e5e9f33878027f1c25601882b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d4810541f678315fc18b5dfb754609ec369f1747fb531aa6875b26f1554521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1fac31636c09900ee50e7854b0f2ba3c6cdcf0790898013f8b73736504c02b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b36f832d08852c873298dd4fe1113b2f9877b9b71beab787b3ada8c0e6dd772(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3c7006ca0667717a2e1b8a7359cfc291253cc682a2b456eff1ac0a9f1cc636(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd098b69f6705b5c0fc4a2c4f8174dd424a55d7d1a1e4456be9e29448f665a57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323c04236a172d24e1d46ba669857968232eafdd1921870ebe627bd93f7151ac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef45b982c9baf1ac9a085384517ce98feadb3455434fdea212d89af4c6f6196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87ad857dcbfe129d84f2bdafd545bccae427ba90b14d9c4e815c98fe7a3c811(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217f77ed23856ba5bdf5640cfd293f94ef3a0e80e1eb45205145770f3d5007cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54d62a72eb1635083dade34cd48c8f689f61024064b7c104b58e654bbbdf707(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigDataprocMetricConfigMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4335b9fbc6b46fe9e5c96e9d741a311a9f0f98fc968735f2c9afb1e05350a9f(
    value: typing.Optional[GoogleDataprocClusterClusterConfigDataprocMetricConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676c718b8b0e5e011114b79974fcb123736dc2f5c1559d49ad446521fb8e1c76(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdc0e41103820ddb6e30978916929737a23ccc0c20cb4194355e60efeb7507c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5034f5094066576ac56abedc086e7a7fb804435ce613c639120a314d29480304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a4257f5aca3122ef66595eeb2d950dc0e076fce45a2ab1036083ecd5ab4a03(
    value: typing.Optional[GoogleDataprocClusterClusterConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fad9874a24bdf9f76cc11ba1886754b38a0410b3e51052a8a1b5254ca4077f(
    *,
    enable_http_port_access: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe8dcfb5865a512d9842eec3e6c2a44d9be44e3726d248275b7f2f1a3fc34d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81971726b44da773dab0bf75f59d833b984e9355b76876ab2547d00d1abc63dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930fea8e43930f9f12a3d90950fad3a3d495fd1917b28691090b96e8e7037305(
    value: typing.Optional[GoogleDataprocClusterClusterConfigEndpointConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ccd4ece8a87a6193f5561296c82551b8d2adcb68d917aa36d84e98da3b3501(
    *,
    confidential_instance_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    node_group_affinity: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    reservation_affinity: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    shielded_instance_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ce69ce1015383b9c2a4480a15f11301ec34b4f6e8594506e3f1015de2991cc(
    *,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4930dbc49903c8b63a734c1b6aeaef41d28f2b87d9d195de952207abcbce90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3051644e63375122cc3402544ceb38d9549e6ee11f95ab0aa60aea76f0d3808a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174cee6af711039fd09f5cb4524f865b2e2bac7e65ba8b08b318a8cc3ffc35fd(
    value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigConfidentialInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bbe914cfc2551f3cfb597e375e22af3b6e5c836c46c7f3ac87786c38723bb9(
    *,
    node_group_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b79bed028fe364b1677c8547b3ee4445042b1e1de50b6f415c06583c2de48bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7598dea0411f20c75bdc7e3e9335ffb22496c5976c30dc2952f69d23b0aecad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e99098bb8f2564e137ffdb48fba54de96510ae14005f3cc7ad5c836d460f44(
    value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigNodeGroupAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a483140551b56a1fece847224af3e2b01656726b3462fcb4ce37a43adbf8e948(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381bfc30b65d7cf70621ad3d3fcea5e88b43e37121433d8cf8939f43ba8b7a18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d588f18d83318d5fa213b7b0007bc87c49f004467012cb1c584b4f6782720750(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5220794514b9e30f78363bee8bd1fb743dbba431aa062da941198c2023b5b65f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a423b28514605964b8ab95a7739c70e8b654da4e1061caf0a3887502b3040835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dcc3b3868dff7f4a426486dbdd0b0aead679fdeb7d719a332e819199606d51(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75871a7edef071e36acd075b693c66f989ea62e343f3d42ec0f7236648de1171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea82b6f95bc33492a74d9b91f5d18229672a8590374f186bcd1570a9a6e7047(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ddf5cb7d19293ca8f2009ed14a93a9f18012c772be6e4f0c0e34e0f2606611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d7cca7910e08bde9d93c075c5c5242af0111875fa31df4c54ffcf19f4546cd(
    value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa86bb9aa1d29241c91d9e5b79e02ca4944d5b9cb1868cb1f6fcd57ba4291d4e(
    *,
    consume_reservation_type: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed6ad63051e7e23ddd986602994c8661ec4ce97f0c30b5e22bf0d5948725efc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f33c00b2579254da3885c4b9fc41552429353f6f71724c7ab3942b3b0599f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6080081f4f7fb1a91e3cbea5c5f214ebce19ed535f01cfd28025ab1c9c50b7be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1345d7e02325495d9e4a9947af71e29baffd567e80c8ff4fa3b7fb0470f3fd2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b61bcc31efbdc206952e75b579c5b66040352ce324601037eaa2583b50768e(
    value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28884a542ef5b7f8d3bf2f07e0be3de9bbdecffee8270f470c6c0e1435d939eb(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e089c67a0d4b49a3c7422afaaabef32ee31944162e1b923f7aaf49aa5e1238f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe804983b682aa2b1b4f0dc391e0f311b26d76482f839a214009462ba30bcd01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afba53be4e2e67f7825fff40f95bc368f02a8f405b969cac50550b824076fe0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12df3567229927ddff78e208cf738d099ae01e268230fa897ce4f25de0c386e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9b6474b43ae159f1cb4db8858130d9dc46832418ee4320c40ed2dcfd1a2641(
    value: typing.Optional[GoogleDataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659b33e16c14ef406ada41a0041df9c37b8d50246d4c9d2cf6ec24f6ba455ca6(
    *,
    script: builtins.str,
    timeout_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb66e145e1f08df64eaf70d447ff4bc72d6253054a8f82cefab6f708afbccb68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588bc9f76c15593bddebc4e3a8cbae97355d37c798f1a8d4106eea9ecf64f889(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c2f755172ceadb0967a9c8ec707a837aa0bd6696d435dea33c10ab05b37407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041c7c1c5db028538665f67ccc5ec92e0ea575770df2f60bece7560e857f4811(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8856854cf53e9b545d6588b50d32aeab7330b6f912690bdb6cf52971c8979c85(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a8df7b1b026df7398c5f802c1afc2d53c9a5aabc1a035cfba0eff58a3c92b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigInitializationAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec71f17038c6b2b64c2f6d63556b67782d6442ef3f6d14b21d5e8c85f6e7c26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d31d42b7cad9841212a8260262b8526f661212793561bb88c8b7d56c9a78092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b500e9197f76f5d3f141fd5a21e385291c0af8eabff66b4cf44716a68b02985(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d923af4379022cd3c4ad50746875115f5aed945c33afd074d338bfaa5d32971d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigInitializationAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc090b9c9c305aafa91be95aa1ee32350111197c3d79a358c888530da02014c(
    *,
    auto_delete_time: typing.Optional[builtins.str] = None,
    idle_delete_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9393c89cd620d8d0738ab0ec23482bbcadbe3ab982ce5c9af4c823d4e39257e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe519ae923c6eb15b5aa73fa2acd0f5251ebba0676cae81c6b40741ecb3948b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76db7a1d5f300b036a70fc3026655464910e3a3d02f5ba2e1b933cf6d310835f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2a710e3bf92eff50e037a0e6aa731539db42eac1ebf021e11f96409b995877(
    value: typing.Optional[GoogleDataprocClusterClusterConfigLifecycleConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e196828a7c9e00bd778f8a343e1681548ff5c68d180c14af0a0b1fc6a63520(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigMasterConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    num_instances: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768ad4ae9b7ff6aa47d8aa51b1154db39c2f635f1342ff0757ddb16cef8ad72d(
    *,
    accelerator_count: jsii.Number,
    accelerator_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a897c7500967fc4d5cb3975b18e8857264dc9b6dbe3625e9e874ea9628b3d0ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253dad92f8c5f1e975d64038754b4c7d99dbfacd371b7ee87f1bb2834b371c22(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9abbf2aa332989e1510181b171f15befd89e98ce9f8b06f4e8a94355e21ef66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43071ccef4d6a567950c95ce332aadb3a6c9a026247aac0a968b309c5f6527b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5f24d2df668722e9cdd038454f5cf6d6f96241284fd5b89f954bfaf347f980(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14373c33777131a54827a0c9cf46ccd802f4ce47dbc6f4f9ac21e13e7a06dbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigMasterConfigAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d240c179f6cd65343f604a85324b88b3f159da0474c7ff759ceed5775a356d3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3aa89e40f6e38a81801be49e11e1483b3743890038075e28751279f3fc8eb9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10754e7ef56eb230233078851af5f1064c540214432077606ab2ea1d9363bcec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e851337853f2db6d0918b4eba1ff1525e397753170f50f740d75ab043ee5ba3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigMasterConfigAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83ee1cb361f3123c1551d4e665df599b78de9d308954194c484d91e971f97ed(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    local_ssd_interface: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc564a723307527677a76e99bc513c10d08749de0d5532899a85521f76ef493a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466675fbf16c3d7bb5c8934112402d40ca5bc3cc3265b514c235f2b290e98160(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0aca0577b9ce17858796790a303c2890b945f8d0b45b7922b11e87351f78984(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532e542ae3b8c2c5bd84bf43ad387a9ac84d694f6efa720651bb18b9105d9788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b48b4f0ce80efd4065914cf257353bfe0d5bab3e3e455f749ab62338644b259(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88f05883f47d43d41cfc8fb6031d3fa355c9c3adc66097daa516c7f3f0632f5(
    value: typing.Optional[GoogleDataprocClusterClusterConfigMasterConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cbd02100dd8d8db8d92e5ca5bc87f3a1b5f2a52327b6a322fd71c148e34072(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862590ff032949c781ff519081489967dce0494eadd50569e206bb65f19e10a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6186420810dd196962e217770fc288f25bb384eaa055108c92ea0960ed69c843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bccd98bc1f216ba633b53595692c60c6b397c8021797875af2395677715dba6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f02c72e6cd51479556d6b5ac257472d9e437f8fd2e343702d4a0931eec0196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac2d526b1db82b25941fa87ea4f0a4278f8043938096ba22746fe70ab945479(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d3be3837f9580f1ac44e887ed9dda817eae11016eee5674547a0c3af212bb1(
    value: typing.Optional[GoogleDataprocClusterClusterConfigMasterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af6f1f2562942a28441a143249b0de5b201011d54781ddd71511f7ac4bcfab7(
    *,
    dataproc_metastore_service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83eb0195b53ef372615c887a8f1988d9d7575e3a9fb013a92aef47487ff47286(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598ab8004081cf9fbbea8e318f56e158228e51d156048890693737ca85fd4f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd2dd6f5dabd7f8b76d96de789e6fbb017ae5fc7f0e76d09ca19eeb11f109a7(
    value: typing.Optional[GoogleDataprocClusterClusterConfigMetastoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886115185668638aae8095aed624911717ca01583ce0494265d3f64be5d0b376(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f28ea5517fbab250f16746181f4f7b4762ad5bfcca83340524b7c190f7a615(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigAuxiliaryNodeGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ed339f3b9ebb7727f3f2bcca681c70eb7d4f9bbb56676798503c8364fa9b7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigInitializationAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6145eea8103675c6cd52d0a0c6e58e97919e08c86b6f83d662ec3a31caf0fefc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b502e745a475c0b0fedee059b8bcd0552a5729e7241fd88257b04fb7153c69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e1e78ea6a75a225ff15764deb7da91fc2819acfb1066d22d4becf2b63df47d(
    value: typing.Optional[GoogleDataprocClusterClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76b040ff125fabff02112d4f9eb142c08527bc6e237f2eef78327ea82553ef6(
    *,
    disk_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_flexibility_policy: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    num_instances: typing.Optional[jsii.Number] = None,
    preemptibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5bccb9f2e86c922412ee98d7aa40dfb2d68d74e6d6ba1e96c7721290872c67(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    local_ssd_interface: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbb86b0217aad5934a5d1508e2abb3173dda65c4c831604b0e3b15e5aec85ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b358e9d68c006a49f288492853791e19dfd9d290c37afc1981f405fb7fbcc0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa904adb1efa8b1e07eaf40e94c40f71ef6dd1425f92f9e5ed2299f56f08f286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8677951b9c8370d15fd26c633aca9bd639127da8f43336753f36d582ada269d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33cca773879d5506f0d1dc423d6d599d7c1349272626be8d8e5674565a3eaf51(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea293759e12d5c052f8496dd6cede1f0620852cdc50e2433c18c989cfc78d91e(
    value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f99cf738f5c54f4cbf256b6bd0a9f68bd1a0f12676523154394586aa6fbdbe(
    *,
    instance_selection_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    provisioning_model_mix: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5989d8fd4e8309dbfc4aab098f37130af863a380ea6fcdb04f55c0b9d8617e(
    *,
    machine_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    rank: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d072897664a3377051bcd7b8a8cabbb5ca92957052329f3f41308c1d97da7e0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952abe0ccddc8ff4f32f8ef5825f3d7a4e81075a6c4236b8a3b60cfcd2316d6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7371b6ad550bc3656db6a610277e1ad323a07b5ae816706d13f3b3b338c27192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f673585403aa063baded1090153b39bc40372fbd833838eea733162a8f0b15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4694a9c56043e40ea0c84974c0581bf59e54435c61dffa56a75ad3d93f363cf4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1efe112e81c823c5c3dc9e3acfe86e1a15c2be6f3390fe4d8581c1f01d6fa8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc4785b8af997b2942d6c07420844407a15244b94f2fb9c88a922952481265c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67957d03bd67d5988d1aba1a539801fc4f67156c81b90ba0b7ab4b4bec27d993(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df957055249b32b2d4b67f24641593af807523b2ec0b52c9af5b4a340c4d798(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b8e95c8854604a1a8d0049ed49172e617aa3e39424496328402f87aaa1c086(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a29094428b922ca35274bb3464a98ddfb27832b98bd3888d0f8c65fd9dab67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada9723b0947ea40951c1f8fad82c2c01564cf31357128974788cf89a5741729(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f79a1dd0e681275b6c06439e8c760db71eb2183119fa9e0a64be03333c3d41a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feef1b50bb445d686e8b9f0a40e9ec215b1f5dc93b8d6ac085367509b28c5ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25404ca3bdf677b37f92bbf71b77a2c1bf8ec314fc85c11dfc87d78832df9230(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dde1c2b74cbe69a3c03fa1d28ed6fffdfaa88c2f0c49f021f1ccc433605f26e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a933a8e8d4b63861136a24c2909b574a1845e7f3e634c82217a662781783ac2c(
    value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionResults],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9766e17eee02f2c4f87f5296f244e979ec1db1e6cebf2d4d5b5fd20fadd3b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc233141c00021e118e534b6bca4a96ce3e4799257b992d687efa184be4b05f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyInstanceSelectionListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219e5cdd4ffae17e3e0fdd0cac1ddb557a2bb43c4da641f48197aa977c4cb970(
    value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3b3e772e571a948230716ccaff1dce05375fc747c3d3b0602cacb4c152419c(
    *,
    standard_capacity_base: typing.Optional[jsii.Number] = None,
    standard_capacity_percent_above_base: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc955f6e4798a4871bc8290316d14d3bb3b82971e533d1521e5acc608c2fa3f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0046d0a86e6b73ea35c6a4a911bb927d6b974a96a8a06773038909fd9078786a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb652e114f64266d17e009e94287edeb4b93ace39e15598f7e73df1aada71b3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3c13bc629aeb63e0ece311a0aed1322c8cc91236a2c9ecfb079ca638d494c3(
    value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfigInstanceFlexibilityPolicyProvisioningModelMix],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c9fc9deb2486edf870fcfa4104e2aca8c38b6a42b3a04c677d8a19f9105150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1f89b45949f2a176c84c79db85e1842e5f3ff898ca2ec139e5caa298df7ce9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983b62165824bb966ba31d9f19c34fa7b4a8a86a289b8fd37dac00bd84cc958f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f858076c07e992db40863acac2dcec53a49cb02fc1e9a0ada36b9587f82158d(
    value: typing.Optional[GoogleDataprocClusterClusterConfigPreemptibleWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1b4eaa78ad66e94bbad8c04478ae604ecd32e6ec812583364fe1c8f0b5b2f2(
    *,
    kerberos_config: typing.Union[GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1da887f121399393b012e113b3a6075afe00babab2df70bb39039593976694d(
    *,
    kms_key_uri: builtins.str,
    root_principal_password_uri: builtins.str,
    cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
    cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
    cross_realm_trust_realm: typing.Optional[builtins.str] = None,
    cross_realm_trust_shared_password_uri: typing.Optional[builtins.str] = None,
    enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kdc_db_key_uri: typing.Optional[builtins.str] = None,
    key_password_uri: typing.Optional[builtins.str] = None,
    keystore_password_uri: typing.Optional[builtins.str] = None,
    keystore_uri: typing.Optional[builtins.str] = None,
    realm: typing.Optional[builtins.str] = None,
    tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
    truststore_password_uri: typing.Optional[builtins.str] = None,
    truststore_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9b1c4079e3e1c62821691ccc6091303d4c11303a1aed64162af93952b84507(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516a3c747637fff16acfbda19f09b023ad8c6118d6eecce133c12891b86e56e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1dd545374e2f7b1903865531f47449eda9365497fc8bd993b3fd739ae45b86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9dba19e73824fe66655092e2bfd333e8b876d8dd8cbbb6880b7568498db1b24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db1e7456f80d21fbbb9399af19481908ddf8a6616e3258696f96b005ad41ffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db25da7daaf3b53742381b6b0adf8defbddbed888ae7d31c3bc9899d0b2c1e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccd79e68ecd7874b8dfa72aa404bbf96d10578096babcbc83d51db6609cee30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b291215d402ee52dd871753def0339eef0c1e0fd0d9c23b195f51c156230d09c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb23e65c9c097c851dad8c9411ffc274492ef59c73474841e230b1b709e9458a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15b6667f1fb328a697f7a0307da4ef5998858325ca5d44b66f037376b4ffae8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27c91bf200cb2f594608420646667d665ec71fc8fbea62b73de8509f69d29e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49158f8dcbc736838244016d8d8c739dbce7d0783dcaf009cb3c893dbcb4399a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecb4c28ad1519c4d509e3e1755483edf70faf685f2f4580d4ee1e3b5666d140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bed848a4efcf815bb5c6c7467adc72778176fde8e54e8c3fbbfffe21b2ec87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675c909007b4847f7078c2c41dcf1c134c87c5a919763898ca1aeb8a6e96afe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f85fa46261123ee7f5889e9f1b264fbf7da1cf1a2e8b773a39e7a89b6fb0eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028a83fdb14e240c72bd6234b0ea00d480837821766eaa5afb27be91c72eac4e(
    value: typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfigKerberosConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf15ac78f233a75d8ca3d2f26a6e2f4914165eab69901b89ab060adb68e82f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfd0825f3c6407ffe233fe6a0d85b8ddd45e80e4fd92a8dfeb163bbb4a6164e(
    value: typing.Optional[GoogleDataprocClusterClusterConfigSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d726f20d286a49a4195472e3047ada75f2186074e259f7a77d20886eba1a4c(
    *,
    image_version: typing.Optional[builtins.str] = None,
    optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    override_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4483b1b7db2fe4bc652e650ba0498398d32c8707ef371577e2408ff543ad9595(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846d4758a3cec9b782ea11ea37539a43b48cb80c34cddc0b64b21982851f5487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abaa3551f1c1a5f74046e486a44106a86774d5efaeeb3b4edb3dfd30831370f5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e620127669a4f81dbf9b3f3d0d77bde63042af8318183ca294707bfe157a7d79(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018dd58a23b34e8f098681877834b03bdbf610f6f48c840a2cd8fd504034aa36(
    value: typing.Optional[GoogleDataprocClusterClusterConfigSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b228ea6131006ecebfa8e7bd39e18e0040934b86367c56c878ff8158a3349370(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    min_num_instances: typing.Optional[jsii.Number] = None,
    num_instances: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68054f22aff98abf7ea8ca1a19c10cfdeba78f1d655eb51686a5f9afc2945660(
    *,
    accelerator_count: jsii.Number,
    accelerator_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ac02a2f695e2360dc03eff326093c7e7d4f0bf9e29b72d43a8a8389e497c9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b140652aaf8383f0a8b5e70fe947a0b1ab1df860e39a1620d77391d8f5de8c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9e9f1c6e19742fa8a55c493a3333df67d4556bdfbdea146d6c71b55753e361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35beb363fb9c23e70a8e5b7708da01c6c198be682580798716aa16f0dc131d5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f0db3256b84926d3cf0e8309deb6d3d9a301b370067f107df0897003e9249b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf311a5aaf7618e93d63e9d5bd62edf80606ca6ea57b56a3b0905736318c8961(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf64b3b2ce80675ddfe8e476156d92921083e219c7973744a7dc911d753a8f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead2b3bf2a69953adcf54834add3897fa71fffa51edeff9bd2d7cdf56a235fd7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e51c088446445ae0f05551cb5f67e83026f1e8effb4a62dad5fc6275425469e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146aaa2154026cd8ef1b83007fb16936defacf0c78de8d540bbce71124aec0f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterClusterConfigWorkerConfigAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0035a455829a02e384052ea9f5367d76f19790f0927a8020778e312247e1366(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    local_ssd_interface: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07779734eb1506c2d905bbda50d6714d71e5c644d3719915624fedf0e390e09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7411716a839ba5c1b1004f330efd84e82b8ed2b483e463a2f30f268f24410db7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e430099562eb020018548bd1e53966716b0a85cb35117d5c7986e2a2546de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08619a1ee12a1d05fb9f847dc1b3ee9512fc150472cb29cae296dc3d2ecf91e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71871b19ceeb8447c2febecd78314aa037b7579e3ffc729e7aa58c4e7af82c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92330b323f79212c261b7ab64904d784226436d44f819212884ec61677ed0e4b(
    value: typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84d47c36575dbe83f9011e98cf803c3bef5d2f20edc5814993d2d6f0f48368c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a9ce12183d92d0d252ae4ad2a5fa20d0235409b0c9957d07cab437bef2dc0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86956c6381dc9b5ab99ab320285b5f4761cb4b687ed1ebe0e7e07b463fc1ca94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6943146cc1b9cbb2718b5562f4b97ad4182535ce3955135d00346481ee9d9268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ee9905ba31e9a5754a091de0716386ab0f7568445f8e3241afbb624604ec13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8322b3b207c75e798e0e71d2ae16bf27674514f232d42e5320bdf3439aac232d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa43691b00bc6cb462bd1ca1a02cf690eddef5b27b62090e2b530419926c06a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c8cc512235bf841f02c3d603dd062404ebc304601aea6b72b8047b5d1caac9(
    value: typing.Optional[GoogleDataprocClusterClusterConfigWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e2efccb4c5966f9419ebe7ee31aee1f95026587e89160caa47377f262bdb98(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    cluster_config: typing.Optional[typing.Union[GoogleDataprocClusterClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    graceful_decommission_timeout: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_cluster_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29812e67b977274a75209050cb7035f6879405aa04d3a07f668ef6f44880590e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3821da276cd34bf07e3dd945307e622f1f1585eb14edad1561427af7559b356(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d99914f870dcdf3f7c465cbd998580ce3aad2560974845af65a3809871617c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712f29410e33407317561d76117f6e7cb927ce63900146caa52106ebfd66fedf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4969fb4031241b2f7b38334271de77e1a1b3ba4ca3794751fab0dc95a4289084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d282550e818ce80be9fa098e7c6d63a2e263b446cc99f1c540a34e95ef5ce292(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9375db8791120629cfeb7dffe56ba48d4f7ca6b3a205173975270acb6283078e(
    *,
    auxiliary_services_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes_cluster_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    staging_bucket: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a76eaa9e092ed747fb84c4c12a594aae73cd89d9c402f047bc8b8f43f3d2b2b(
    *,
    metastore_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_history_server_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d335dd11e53e08ea4d84dce38729c1c38cbdb52347ba02fabe359476e58dd73(
    *,
    dataproc_metastore_service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d737d9190f6dcb4393c9716e0c5224c9c5ee7e730ce9b60f691373ce3173faf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cb0428ed80db5570aaebdf2d81061d450441aaa622a174d959fa506d2740ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19394319f7a920e7fb6a48f7eb1eb313d54a022cabde3148ec88c2e0a3222f15(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01be3985d429dce1ed77373316f32c1557075a2f9c4c95391048c36229a2bf09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa959ec0b75fff6816352642632346628a70137142dcbf0408bb01492c809ee2(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e36840832b5f11b5df7f763027a50adbdc70e034212b890dbcf9e18b81c161(
    *,
    dataproc_cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5991989304e0e915e75d5f427fab74906950136879a959fcf7b4acf091af3373(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8fd5ce9569dba5824bd52ea86742fbad79b44ac14ae0352c3bdcccf7cf763a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca23ed6ebd03033f838eb106149155ff3612504a0e9fe94ce2ae70302f9b9781(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17580f49e01f3e70e3730ce85c5995594f102476d77ddadb9dcc416be3e97028(
    *,
    gke_cluster_config: typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig, typing.Dict[builtins.str, typing.Any]],
    kubernetes_software_config: typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig, typing.Dict[builtins.str, typing.Any]],
    kubernetes_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4877ac9de35753ea78d4e8d906d67147cdf5be7c71f7de7540ea51a73aa30530(
    *,
    gke_cluster_target: typing.Optional[builtins.str] = None,
    node_pool_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d860262fb535697e10d9a3c15def134789c4e811edef3451d7cebeb85bd26ce9(
    *,
    node_pool: builtins.str,
    roles: typing.Sequence[builtins.str],
    node_pool_config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d07078c247c181dea6b87b27bad4289dd5bfeccbfc627fc0cf8201e769ff96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61eaff8d3cbb1b63b5683b0f4aeeff5d1b169759fad9080d6dafcafc398e8dde(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7b57e55e1dfa7293eb40563009c14845b3dbc57c56e32aca315ae39e419df4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d246776c52c1c6610b0178ff0807ac585f41601757052abea7073099c03d6e5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958c28d6e719e955a0e05ef490c54f5287b5a1230856a51c9cf8758f348d16ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e735605cdf7c746b431856d35b6454edb46148dc586c27f5ada34958ca07be27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13996631c51c0e6ccc110a68ec1e34edaf706505c59f5d4731f130f372362c5(
    *,
    locations: typing.Sequence[builtins.str],
    autoscaling: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    config: typing.Optional[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c28b01521bb85c40902a4d7cd84f72f129625edf8f2b2472df0effaf01f6d3e(
    *,
    max_node_count: typing.Optional[jsii.Number] = None,
    min_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6826447bdb2b3ea0e53f5d531a35ac71f1b58ff52cf90ff4b21d9f541f135670(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d294f57cc8a230c68db929f72479fcf5a0652b62df907de4455c17eec155d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341c61c067d4488d58e2ae4bfa68332367625a3445573fdbde0b8f77887c6d8a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b112adce23bc8d21406bb163834d86d8cd23a95d82b027831473eff201b6a344(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7af4aa5f220eaad9d6f4351903326f6069d0f035395201b8c8be74f6d497119(
    *,
    local_ssd_count: typing.Optional[jsii.Number] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9527cc7ad79b3d3f56009f7b6aea425e98d9eaad46f3f1bfe1368cf387fbaabd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd101dfa48e91d257e1bd82ef354dda7aa74133993a9c285f421a1e3eeefd59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a33ee07bf6a8e9a229a51559493e54ddb73ca6e351bb40065ffd56b5c3dc13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c59d7a7e10c913dc94ce6d9e96e7fc9592c2a925e56e1f1fb93f3b7ce603572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de35983218ebcc8d8dfcd3e1fcb8defe035c1d52bd7adccd1f810a303d0479dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0622046780134b6fdfdcffc2fb0954f7f2d08fb30877bf7803bb67676fc75a1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772bf7b93bbb754792542d3ad60fb4c3e89b88fa4f526ccf5dd2ec3c379b6c9a(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ae2cd57670f4e63b3482077bfb9373568e0534f7c5dadcff6dbd9e586abea3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f659d9a7d817b7be7437d5611ef7fadd9bedee4afd52bce7e1f55562a95e2183(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff7a7d2a397799f224008e4ec24c3f7fbf41265e269a138b9e64dd06494bcc1(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407001a7614a800255af67361d6e4346cab15264dfeef16009ac807366b1502b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4db279234a98c87d95057c692a586794de1224c10af7676f9193fac2fe9c083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd23ba3fc4c9dddf8e6d1acb8d5eb08aa3092cf6bb34890b09a6714b6e6cb369(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aeb1701a1b5fceb2ec7940a7dc0b30bb800523509aecb2fd788b805967e6117(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fde588c384d20becea82dce1a4723cd2d10ea048efd3944ebbfa5a7b4ebd9f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673247c88091356832030d8519e0352121d23d710052c2e91e617d98b65d9a40(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9030371ca24fe25035118e2a8cb3beccbe64fd11966e2967fb602d4bbfd8e3ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e1b5e679b4d5ca5277cb2bf9aebf13d8af9bfa850eb86aa3becf894b12c326(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfe4c5c0dbddce37aa72e290c764f017c615be4ac761968dfcb61ff1fe6c42e(
    *,
    component_version: typing.Mapping[builtins.str, builtins.str],
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6a4e5c3bab38ed8bdb0a08a969e49c36267b3988abcb28b2c366c8e12e002c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df533a87b8c6de7144fe6ca7052a71203be8b8b8ace9276ad3d30566f69fe4a0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9556ef2e4bb459c66faa74c491cc79dfdfe34f01b9735d0c1232f06420d6d094(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c1cc12da44f49bc54be94e797d7d2969917604b97b6b189de40a885cb564cf(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bf99a95e107cfc6d66fd80374f2ded7c1bef5aff060ea6a211b921b67f1d30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c496771208ea553bb361e32f2ab0601002aa08ac49a7aa5e854612350351a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473d063e592d4e160787abf9a6a1c64a531b633f3d235aec655369a8a9394825(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfigKubernetesClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc73a2e6c2927d25c214a11db20a1dad7f0972ed865dad22ca6fcacbc633a47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e184bc7d3483615a39029379d6b38f8687355b867fb657c638bfa78c619cea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb01824e257485a4dbfa6411aaeb0c9995f9b548acec2e344a9887c177ef9d8(
    value: typing.Optional[GoogleDataprocClusterVirtualClusterConfig],
) -> None:
    """Type checking stubs"""
    pass
