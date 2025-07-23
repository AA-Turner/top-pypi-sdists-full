r'''
# `google_clouddeploy_target`

Refer to the Terraform Registry for docs: [`google_clouddeploy_target`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target).
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


class ClouddeployTarget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTarget",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target google_clouddeploy_target}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anthos_cluster: typing.Optional[typing.Union["ClouddeployTargetAnthosCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        associated_entities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployTargetAssociatedEntities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_target: typing.Optional[typing.Union["ClouddeployTargetCustomTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        deploy_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployTargetExecutionConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gke: typing.Optional[typing.Union["ClouddeployTargetGke", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        multi_target: typing.Optional[typing.Union["ClouddeployTargetMultiTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run: typing.Optional[typing.Union["ClouddeployTargetRun", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployTargetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target google_clouddeploy_target} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#location ClouddeployTarget#location}
        :param name: Name of the ``Target``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#name ClouddeployTarget#name}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#annotations ClouddeployTarget#annotations}
        :param anthos_cluster: anthos_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#anthos_cluster ClouddeployTarget#anthos_cluster}
        :param associated_entities: associated_entities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#associated_entities ClouddeployTarget#associated_entities}
        :param custom_target: custom_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#custom_target ClouddeployTarget#custom_target}
        :param deploy_parameters: Optional. The deploy parameters to use for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#deploy_parameters ClouddeployTarget#deploy_parameters}
        :param description: Optional. Description of the ``Target``. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#description ClouddeployTarget#description}
        :param execution_configs: execution_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#execution_configs ClouddeployTarget#execution_configs}
        :param gke: gke block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#gke ClouddeployTarget#gke}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#id ClouddeployTarget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#labels ClouddeployTarget#labels}
        :param multi_target: multi_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#multi_target ClouddeployTarget#multi_target}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#project ClouddeployTarget#project}
        :param require_approval: Optional. Whether or not the ``Target`` requires approval. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#require_approval ClouddeployTarget#require_approval}
        :param run: run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#run ClouddeployTarget#run}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#timeouts ClouddeployTarget#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335bf03e4270efe72a15ee1d747146fdd20839f223fa162df689621ca355a29b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ClouddeployTargetConfig(
            location=location,
            name=name,
            annotations=annotations,
            anthos_cluster=anthos_cluster,
            associated_entities=associated_entities,
            custom_target=custom_target,
            deploy_parameters=deploy_parameters,
            description=description,
            execution_configs=execution_configs,
            gke=gke,
            id=id,
            labels=labels,
            multi_target=multi_target,
            project=project,
            require_approval=require_approval,
            run=run,
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
        '''Generates CDKTF code for importing a ClouddeployTarget resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ClouddeployTarget to import.
        :param import_from_id: The id of the existing ClouddeployTarget that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ClouddeployTarget to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38af56ad058a2af1d57d6cfe41af57a06e8bf581a2fa24399abffdeece52460)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAnthosCluster")
    def put_anthos_cluster(
        self,
        *,
        membership: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param membership: Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#membership ClouddeployTarget#membership}
        '''
        value = ClouddeployTargetAnthosCluster(membership=membership)

        return typing.cast(None, jsii.invoke(self, "putAnthosCluster", [value]))

    @jsii.member(jsii_name="putAssociatedEntities")
    def put_associated_entities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployTargetAssociatedEntities", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a83a1acb6694b00f7a91ffdaae564dee1354e31cb665c1e5e1c8602b80b508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAssociatedEntities", [value]))

    @jsii.member(jsii_name="putCustomTarget")
    def put_custom_target(self, *, custom_target_type: builtins.str) -> None:
        '''
        :param custom_target_type: Required. The name of the CustomTargetType. Format must be ``projects/{project}/locations/{location}/customTargetTypes/{custom_target_type}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#custom_target_type ClouddeployTarget#custom_target_type}
        '''
        value = ClouddeployTargetCustomTarget(custom_target_type=custom_target_type)

        return typing.cast(None, jsii.invoke(self, "putCustomTarget", [value]))

    @jsii.member(jsii_name="putExecutionConfigs")
    def put_execution_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployTargetExecutionConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eee78930adcecf319d10fdb483db87a360d58853f2d85c14539cf9737ce2790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExecutionConfigs", [value]))

    @jsii.member(jsii_name="putGke")
    def put_gke(
        self,
        *,
        cluster: typing.Optional[builtins.str] = None,
        dns_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: Information specifying a GKE Cluster. Format is `projects/{project_id}/locations/{location_id}/clusters/{cluster_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#cluster ClouddeployTarget#cluster}
        :param dns_endpoint: Optional. If set, the cluster will be accessed using the DNS endpoint. Note that both ``dns_endpoint`` and ``internal_ip`` cannot be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#dns_endpoint ClouddeployTarget#dns_endpoint}
        :param internal_ip: Optional. If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#internal_ip ClouddeployTarget#internal_ip}
        :param proxy_url: Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#proxy_url ClouddeployTarget#proxy_url}
        '''
        value = ClouddeployTargetGke(
            cluster=cluster,
            dns_endpoint=dns_endpoint,
            internal_ip=internal_ip,
            proxy_url=proxy_url,
        )

        return typing.cast(None, jsii.invoke(self, "putGke", [value]))

    @jsii.member(jsii_name="putMultiTarget")
    def put_multi_target(self, *, target_ids: typing.Sequence[builtins.str]) -> None:
        '''
        :param target_ids: Required. The target_ids of this multiTarget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#target_ids ClouddeployTarget#target_ids}
        '''
        value = ClouddeployTargetMultiTarget(target_ids=target_ids)

        return typing.cast(None, jsii.invoke(self, "putMultiTarget", [value]))

    @jsii.member(jsii_name="putRun")
    def put_run(self, *, location: builtins.str) -> None:
        '''
        :param location: Required. The location where the Cloud Run Service should be located. Format is ``projects/{project}/locations/{location}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#location ClouddeployTarget#location}
        '''
        value = ClouddeployTargetRun(location=location)

        return typing.cast(None, jsii.invoke(self, "putRun", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#create ClouddeployTarget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#delete ClouddeployTarget#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#update ClouddeployTarget#update}.
        '''
        value = ClouddeployTargetTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAnthosCluster")
    def reset_anthos_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnthosCluster", []))

    @jsii.member(jsii_name="resetAssociatedEntities")
    def reset_associated_entities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssociatedEntities", []))

    @jsii.member(jsii_name="resetCustomTarget")
    def reset_custom_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomTarget", []))

    @jsii.member(jsii_name="resetDeployParameters")
    def reset_deploy_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeployParameters", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExecutionConfigs")
    def reset_execution_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionConfigs", []))

    @jsii.member(jsii_name="resetGke")
    def reset_gke(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGke", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMultiTarget")
    def reset_multi_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiTarget", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRequireApproval")
    def reset_require_approval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireApproval", []))

    @jsii.member(jsii_name="resetRun")
    def reset_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRun", []))

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
    @jsii.member(jsii_name="anthosCluster")
    def anthos_cluster(self) -> "ClouddeployTargetAnthosClusterOutputReference":
        return typing.cast("ClouddeployTargetAnthosClusterOutputReference", jsii.get(self, "anthosCluster"))

    @builtins.property
    @jsii.member(jsii_name="associatedEntities")
    def associated_entities(self) -> "ClouddeployTargetAssociatedEntitiesList":
        return typing.cast("ClouddeployTargetAssociatedEntitiesList", jsii.get(self, "associatedEntities"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="customTarget")
    def custom_target(self) -> "ClouddeployTargetCustomTargetOutputReference":
        return typing.cast("ClouddeployTargetCustomTargetOutputReference", jsii.get(self, "customTarget"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="executionConfigs")
    def execution_configs(self) -> "ClouddeployTargetExecutionConfigsList":
        return typing.cast("ClouddeployTargetExecutionConfigsList", jsii.get(self, "executionConfigs"))

    @builtins.property
    @jsii.member(jsii_name="gke")
    def gke(self) -> "ClouddeployTargetGkeOutputReference":
        return typing.cast("ClouddeployTargetGkeOutputReference", jsii.get(self, "gke"))

    @builtins.property
    @jsii.member(jsii_name="multiTarget")
    def multi_target(self) -> "ClouddeployTargetMultiTargetOutputReference":
        return typing.cast("ClouddeployTargetMultiTargetOutputReference", jsii.get(self, "multiTarget"))

    @builtins.property
    @jsii.member(jsii_name="run")
    def run(self) -> "ClouddeployTargetRunOutputReference":
        return typing.cast("ClouddeployTargetRunOutputReference", jsii.get(self, "run"))

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetId"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ClouddeployTargetTimeoutsOutputReference":
        return typing.cast("ClouddeployTargetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="anthosClusterInput")
    def anthos_cluster_input(self) -> typing.Optional["ClouddeployTargetAnthosCluster"]:
        return typing.cast(typing.Optional["ClouddeployTargetAnthosCluster"], jsii.get(self, "anthosClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedEntitiesInput")
    def associated_entities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetAssociatedEntities"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetAssociatedEntities"]]], jsii.get(self, "associatedEntitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="customTargetInput")
    def custom_target_input(self) -> typing.Optional["ClouddeployTargetCustomTarget"]:
        return typing.cast(typing.Optional["ClouddeployTargetCustomTarget"], jsii.get(self, "customTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="deployParametersInput")
    def deploy_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "deployParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="executionConfigsInput")
    def execution_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetExecutionConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetExecutionConfigs"]]], jsii.get(self, "executionConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeInput")
    def gke_input(self) -> typing.Optional["ClouddeployTargetGke"]:
        return typing.cast(typing.Optional["ClouddeployTargetGke"], jsii.get(self, "gkeInput"))

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
    @jsii.member(jsii_name="multiTargetInput")
    def multi_target_input(self) -> typing.Optional["ClouddeployTargetMultiTarget"]:
        return typing.cast(typing.Optional["ClouddeployTargetMultiTarget"], jsii.get(self, "multiTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="requireApprovalInput")
    def require_approval_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireApprovalInput"))

    @builtins.property
    @jsii.member(jsii_name="runInput")
    def run_input(self) -> typing.Optional["ClouddeployTargetRun"]:
        return typing.cast(typing.Optional["ClouddeployTargetRun"], jsii.get(self, "runInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployTargetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployTargetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d09480dc9cc263f5bed4c40420e927acc711b09922cffe09d2575fcb5e3c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deployParameters")
    def deploy_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "deployParameters"))

    @deploy_parameters.setter
    def deploy_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6454df26bf956a9e1f1cbd1b0190aed4e513a95ade4ec2c9945a20596d92bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1c30c4449358203ae1a056bf2700b43b62e471c4527e36858cb75572161f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c953722a628e98aa5f06b3f08d69263e1dc15bf2aa8001200cc1c2e58844028e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0271f9243ccba1e0736f6ccd9dc11819fa6473f3c8069fe63f3d65b89769e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdefe4eb33f30ebc41fb56b554133cf95fc53f06a69626d3a9f61449716fe42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22f10bf1f0d9dc36ff7b8dc096a2385389287e6b061679f7c690758685e945e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7ce556bec2d9f500e10d0a1ef1fa7e689337f56201f672189cd2fadc16ce7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireApproval")
    def require_approval(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireApproval"))

    @require_approval.setter
    def require_approval(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47172b979875fdb56f9209644b82a8308f9e41900756abcf0bf9a1e8ba19b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireApproval", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAnthosCluster",
    jsii_struct_bases=[],
    name_mapping={"membership": "membership"},
)
class ClouddeployTargetAnthosCluster:
    def __init__(self, *, membership: typing.Optional[builtins.str] = None) -> None:
        '''
        :param membership: Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#membership ClouddeployTarget#membership}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5174e11b7c9291b623072a3255afa79ab2e5ac64cf64a2557b40ae8bb43b73)
            check_type(argname="argument membership", value=membership, expected_type=type_hints["membership"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if membership is not None:
            self._values["membership"] = membership

    @builtins.property
    def membership(self) -> typing.Optional[builtins.str]:
        '''Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#membership ClouddeployTarget#membership}
        '''
        result = self._values.get("membership")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetAnthosCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetAnthosClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAnthosClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1745c03716abe1fada29d2f26a96aba9b7b3a07399a9a777a994d74211d190fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMembership")
    def reset_membership(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembership", []))

    @builtins.property
    @jsii.member(jsii_name="membershipInput")
    def membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "membershipInput"))

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @membership.setter
    def membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ffe975523899eae50cb4911e3d7b5f9b61c77089b46911a54e5c1a67ad73452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployTargetAnthosCluster]:
        return typing.cast(typing.Optional[ClouddeployTargetAnthosCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployTargetAnthosCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd01fe66f326b18c95cc100744bc9abed2d4990f49410932ff831dbbd40cd0d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntities",
    jsii_struct_bases=[],
    name_mapping={
        "entity_id": "entityId",
        "anthos_clusters": "anthosClusters",
        "gke_clusters": "gkeClusters",
    },
)
class ClouddeployTargetAssociatedEntities:
    def __init__(
        self,
        *,
        entity_id: builtins.str,
        anthos_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployTargetAssociatedEntitiesAnthosClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployTargetAssociatedEntitiesGkeClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entity_id: The name for the key in the map for which this object is mapped to in the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#entity_id ClouddeployTarget#entity_id}
        :param anthos_clusters: anthos_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#anthos_clusters ClouddeployTarget#anthos_clusters}
        :param gke_clusters: gke_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#gke_clusters ClouddeployTarget#gke_clusters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6752143ddd9e2c0b275effc566588b2737a49de51bee61e1822f91c98d1b7f08)
            check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
            check_type(argname="argument anthos_clusters", value=anthos_clusters, expected_type=type_hints["anthos_clusters"])
            check_type(argname="argument gke_clusters", value=gke_clusters, expected_type=type_hints["gke_clusters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_id": entity_id,
        }
        if anthos_clusters is not None:
            self._values["anthos_clusters"] = anthos_clusters
        if gke_clusters is not None:
            self._values["gke_clusters"] = gke_clusters

    @builtins.property
    def entity_id(self) -> builtins.str:
        '''The name for the key in the map for which this object is mapped to in the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#entity_id ClouddeployTarget#entity_id}
        '''
        result = self._values.get("entity_id")
        assert result is not None, "Required property 'entity_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def anthos_clusters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetAssociatedEntitiesAnthosClusters"]]]:
        '''anthos_clusters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#anthos_clusters ClouddeployTarget#anthos_clusters}
        '''
        result = self._values.get("anthos_clusters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetAssociatedEntitiesAnthosClusters"]]], result)

    @builtins.property
    def gke_clusters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetAssociatedEntitiesGkeClusters"]]]:
        '''gke_clusters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#gke_clusters ClouddeployTarget#gke_clusters}
        '''
        result = self._values.get("gke_clusters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetAssociatedEntitiesGkeClusters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetAssociatedEntities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntitiesAnthosClusters",
    jsii_struct_bases=[],
    name_mapping={"membership": "membership"},
)
class ClouddeployTargetAssociatedEntitiesAnthosClusters:
    def __init__(self, *, membership: typing.Optional[builtins.str] = None) -> None:
        '''
        :param membership: Optional. Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#membership ClouddeployTarget#membership}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae446c436f417873a91f6ee3d04ee11a3c0cd7413cdd68efd7e0397ac5fd2bf)
            check_type(argname="argument membership", value=membership, expected_type=type_hints["membership"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if membership is not None:
            self._values["membership"] = membership

    @builtins.property
    def membership(self) -> typing.Optional[builtins.str]:
        '''Optional. Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#membership ClouddeployTarget#membership}
        '''
        result = self._values.get("membership")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetAssociatedEntitiesAnthosClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetAssociatedEntitiesAnthosClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntitiesAnthosClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__765d3d66cda46d4820e58c2a68493311064531f0c82cf6ab621761cf8233eb77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a46b0910c3a57ebe3d3004fbacf6e013ce198562708aabbd8f27b6638949dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb876e9822ed1712ffdaefd1d550c190e4e8315c41a225de8f20dffab63c20b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e83a55529370238345d6db81272cd9bdf61cf8a8b3ad4e6dbb40f7ffa0f05e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5cbd5ae3371e79ee5fed9ed47cffd9da3bbb0741a9a9a069bbac13b962968f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesAnthosClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesAnthosClusters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesAnthosClusters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8752e235b296383107d4c1a3c508ca767862b25347d3700e30a39fb3a247e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c07dcb20ea882239ec693cf6b28fbdbfae529684f48452d37f88746042ef0c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMembership")
    def reset_membership(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembership", []))

    @builtins.property
    @jsii.member(jsii_name="membershipInput")
    def membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "membershipInput"))

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @membership.setter
    def membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0da0d7473446b89dbb1507732ed7798d243a27c5c6b1247996d0b05ed6f0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntitiesAnthosClusters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntitiesAnthosClusters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntitiesAnthosClusters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabcb7c76674e13b0a7ca20c8273047c1d4f1975d259d1cddcd698eeaccb4cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntitiesGkeClusters",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "internal_ip": "internalIp",
        "proxy_url": "proxyUrl",
    },
)
class ClouddeployTargetAssociatedEntitiesGkeClusters:
    def __init__(
        self,
        *,
        cluster: typing.Optional[builtins.str] = None,
        internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: Optional. Information specifying a GKE Cluster. Format is ``projects/{project_id}/locations/{location_id}/clusters/{cluster_id}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#cluster ClouddeployTarget#cluster}
        :param internal_ip: Optional. If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#internal_ip ClouddeployTarget#internal_ip}
        :param proxy_url: Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#proxy_url ClouddeployTarget#proxy_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf07d60ca5078cc394e094cae14c9cff0908c065ecc33fe26441c93606bb26f)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument internal_ip", value=internal_ip, expected_type=type_hints["internal_ip"])
            check_type(argname="argument proxy_url", value=proxy_url, expected_type=type_hints["proxy_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster
        if internal_ip is not None:
            self._values["internal_ip"] = internal_ip
        if proxy_url is not None:
            self._values["proxy_url"] = proxy_url

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''Optional. Information specifying a GKE Cluster. Format is ``projects/{project_id}/locations/{location_id}/clusters/{cluster_id}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#cluster ClouddeployTarget#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#internal_ip ClouddeployTarget#internal_ip}
        '''
        result = self._values.get("internal_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#proxy_url ClouddeployTarget#proxy_url}
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetAssociatedEntitiesGkeClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetAssociatedEntitiesGkeClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntitiesGkeClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e9013ddf277b0ae3066cd287ed406ef9b6f1c81ab2cecebc61a80426c040be8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployTargetAssociatedEntitiesGkeClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91ff8493a4391c729bc6a51afc5c7349f15c4a4b63c94b47aa903dccf30a6b3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployTargetAssociatedEntitiesGkeClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2c528780876944ec2eb5bc0252cae69436cbe16ac6f737c3e44487964c9b80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f31aa255ff056117f5799a3c8e4ba2501b20687036a02b6de7a6946695bf7b83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__435a33b0e202dfa639c8973e99fd5398233af29c50225f3db8e951c97da72a16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesGkeClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesGkeClusters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesGkeClusters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229dc7e0a321bb61239f634040848ef274672b67b37a096ba825acd2bb51e597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployTargetAssociatedEntitiesGkeClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntitiesGkeClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c183e33c97c9f554816b0fa14b92679ebda0ce1857d4b3ddd693c84d3cfdf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCluster")
    def reset_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCluster", []))

    @jsii.member(jsii_name="resetInternalIp")
    def reset_internal_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIp", []))

    @jsii.member(jsii_name="resetProxyUrl")
    def reset_proxy_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyUrl", []))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpInput")
    def internal_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyUrlInput")
    def proxy_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37a3ac4aaba90d9fdfd0f7e40b4c1151004af3ed5526cd2062df2018de83864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalIp")
    def internal_ip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internalIp"))

    @internal_ip.setter
    def internal_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519c4cc217fa50be8a1282a58734ea966ad63c28b97022455d04100fe4964a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyUrl")
    def proxy_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyUrl"))

    @proxy_url.setter
    def proxy_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a95b598bde816d1d91f9b00eebc1c769307c2ece9fb5ebbe4de782c6184c155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntitiesGkeClusters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntitiesGkeClusters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntitiesGkeClusters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee5aff2829a2d15474069e05fffba78338fbd1cbc25434d08853fd521a01e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployTargetAssociatedEntitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d5cfb9c5d969208f357bad9f828523413817c3b9984ef15a2345e43db7bf2a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployTargetAssociatedEntitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb605c17167b4f80f9acff01a6cc4e6af68ab889cf3f2c8f9b5b3b85e9e9efa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployTargetAssociatedEntitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3162205158e354a6b5444b888291df00301548f19268fea6a42fa29f265031e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83c27d6c5cedc32b89c784e16e695064cfec8cae6bb30a86743153efa565cd48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90e853d6c409a1461ef0f3031483903f66bd15d75a0e46658e3e26ab3d8b731f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8c64dee230a0af3f15ba20823f3de230d86347d66f25bc45d7292471f74454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployTargetAssociatedEntitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetAssociatedEntitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f12be70c813dd7579f2ba315274d421a78364c6574d819299abb1b937f3dbc6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAnthosClusters")
    def put_anthos_clusters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntitiesAnthosClusters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9736a5227dc275274af0cac9fa02a2a3b29792763639499019c53b59a193f5fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnthosClusters", [value]))

    @jsii.member(jsii_name="putGkeClusters")
    def put_gke_clusters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntitiesGkeClusters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ad56bb59bc06038a4c1223ae1032bbd0cdb78e2e3aac5b061e36d03fccd7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGkeClusters", [value]))

    @jsii.member(jsii_name="resetAnthosClusters")
    def reset_anthos_clusters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnthosClusters", []))

    @jsii.member(jsii_name="resetGkeClusters")
    def reset_gke_clusters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeClusters", []))

    @builtins.property
    @jsii.member(jsii_name="anthosClusters")
    def anthos_clusters(self) -> ClouddeployTargetAssociatedEntitiesAnthosClustersList:
        return typing.cast(ClouddeployTargetAssociatedEntitiesAnthosClustersList, jsii.get(self, "anthosClusters"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusters")
    def gke_clusters(self) -> ClouddeployTargetAssociatedEntitiesGkeClustersList:
        return typing.cast(ClouddeployTargetAssociatedEntitiesGkeClustersList, jsii.get(self, "gkeClusters"))

    @builtins.property
    @jsii.member(jsii_name="anthosClustersInput")
    def anthos_clusters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesAnthosClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesAnthosClusters]]], jsii.get(self, "anthosClustersInput"))

    @builtins.property
    @jsii.member(jsii_name="entityIdInput")
    def entity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeClustersInput")
    def gke_clusters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesGkeClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesGkeClusters]]], jsii.get(self, "gkeClustersInput"))

    @builtins.property
    @jsii.member(jsii_name="entityId")
    def entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityId"))

    @entity_id.setter
    def entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9894d76e60ff8ec1de8792aa0152ea4ef25f1154620b3050656cdc24356b8f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39dd1f10daf43d42abdb718af3a51f7241fd06d81f7f3447d79b23869ceeea83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetConfig",
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
        "annotations": "annotations",
        "anthos_cluster": "anthosCluster",
        "associated_entities": "associatedEntities",
        "custom_target": "customTarget",
        "deploy_parameters": "deployParameters",
        "description": "description",
        "execution_configs": "executionConfigs",
        "gke": "gke",
        "id": "id",
        "labels": "labels",
        "multi_target": "multiTarget",
        "project": "project",
        "require_approval": "requireApproval",
        "run": "run",
        "timeouts": "timeouts",
    },
)
class ClouddeployTargetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anthos_cluster: typing.Optional[typing.Union[ClouddeployTargetAnthosCluster, typing.Dict[builtins.str, typing.Any]]] = None,
        associated_entities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntities, typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_target: typing.Optional[typing.Union["ClouddeployTargetCustomTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        deploy_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployTargetExecutionConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gke: typing.Optional[typing.Union["ClouddeployTargetGke", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        multi_target: typing.Optional[typing.Union["ClouddeployTargetMultiTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run: typing.Optional[typing.Union["ClouddeployTargetRun", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployTargetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#location ClouddeployTarget#location}
        :param name: Name of the ``Target``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#name ClouddeployTarget#name}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#annotations ClouddeployTarget#annotations}
        :param anthos_cluster: anthos_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#anthos_cluster ClouddeployTarget#anthos_cluster}
        :param associated_entities: associated_entities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#associated_entities ClouddeployTarget#associated_entities}
        :param custom_target: custom_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#custom_target ClouddeployTarget#custom_target}
        :param deploy_parameters: Optional. The deploy parameters to use for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#deploy_parameters ClouddeployTarget#deploy_parameters}
        :param description: Optional. Description of the ``Target``. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#description ClouddeployTarget#description}
        :param execution_configs: execution_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#execution_configs ClouddeployTarget#execution_configs}
        :param gke: gke block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#gke ClouddeployTarget#gke}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#id ClouddeployTarget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#labels ClouddeployTarget#labels}
        :param multi_target: multi_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#multi_target ClouddeployTarget#multi_target}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#project ClouddeployTarget#project}
        :param require_approval: Optional. Whether or not the ``Target`` requires approval. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#require_approval ClouddeployTarget#require_approval}
        :param run: run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#run ClouddeployTarget#run}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#timeouts ClouddeployTarget#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(anthos_cluster, dict):
            anthos_cluster = ClouddeployTargetAnthosCluster(**anthos_cluster)
        if isinstance(custom_target, dict):
            custom_target = ClouddeployTargetCustomTarget(**custom_target)
        if isinstance(gke, dict):
            gke = ClouddeployTargetGke(**gke)
        if isinstance(multi_target, dict):
            multi_target = ClouddeployTargetMultiTarget(**multi_target)
        if isinstance(run, dict):
            run = ClouddeployTargetRun(**run)
        if isinstance(timeouts, dict):
            timeouts = ClouddeployTargetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9378670a678b371adb2b7bf70ad7c247d15d672ddde04fde93e6c2a778f0c09)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument anthos_cluster", value=anthos_cluster, expected_type=type_hints["anthos_cluster"])
            check_type(argname="argument associated_entities", value=associated_entities, expected_type=type_hints["associated_entities"])
            check_type(argname="argument custom_target", value=custom_target, expected_type=type_hints["custom_target"])
            check_type(argname="argument deploy_parameters", value=deploy_parameters, expected_type=type_hints["deploy_parameters"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_configs", value=execution_configs, expected_type=type_hints["execution_configs"])
            check_type(argname="argument gke", value=gke, expected_type=type_hints["gke"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument multi_target", value=multi_target, expected_type=type_hints["multi_target"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if anthos_cluster is not None:
            self._values["anthos_cluster"] = anthos_cluster
        if associated_entities is not None:
            self._values["associated_entities"] = associated_entities
        if custom_target is not None:
            self._values["custom_target"] = custom_target
        if deploy_parameters is not None:
            self._values["deploy_parameters"] = deploy_parameters
        if description is not None:
            self._values["description"] = description
        if execution_configs is not None:
            self._values["execution_configs"] = execution_configs
        if gke is not None:
            self._values["gke"] = gke
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if multi_target is not None:
            self._values["multi_target"] = multi_target
        if project is not None:
            self._values["project"] = project
        if require_approval is not None:
            self._values["require_approval"] = require_approval
        if run is not None:
            self._values["run"] = run
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
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#location ClouddeployTarget#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the ``Target``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#name ClouddeployTarget#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field ``effective_annotations`` for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#annotations ClouddeployTarget#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def anthos_cluster(self) -> typing.Optional[ClouddeployTargetAnthosCluster]:
        '''anthos_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#anthos_cluster ClouddeployTarget#anthos_cluster}
        '''
        result = self._values.get("anthos_cluster")
        return typing.cast(typing.Optional[ClouddeployTargetAnthosCluster], result)

    @builtins.property
    def associated_entities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntities]]]:
        '''associated_entities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#associated_entities ClouddeployTarget#associated_entities}
        '''
        result = self._values.get("associated_entities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntities]]], result)

    @builtins.property
    def custom_target(self) -> typing.Optional["ClouddeployTargetCustomTarget"]:
        '''custom_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#custom_target ClouddeployTarget#custom_target}
        '''
        result = self._values.get("custom_target")
        return typing.cast(typing.Optional["ClouddeployTargetCustomTarget"], result)

    @builtins.property
    def deploy_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. The deploy parameters to use for this target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#deploy_parameters ClouddeployTarget#deploy_parameters}
        '''
        result = self._values.get("deploy_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the ``Target``. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#description ClouddeployTarget#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetExecutionConfigs"]]]:
        '''execution_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#execution_configs ClouddeployTarget#execution_configs}
        '''
        result = self._values.get("execution_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployTargetExecutionConfigs"]]], result)

    @builtins.property
    def gke(self) -> typing.Optional["ClouddeployTargetGke"]:
        '''gke block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#gke ClouddeployTarget#gke}
        '''
        result = self._values.get("gke")
        return typing.cast(typing.Optional["ClouddeployTargetGke"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#id ClouddeployTarget#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field ``effective_labels`` for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#labels ClouddeployTarget#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def multi_target(self) -> typing.Optional["ClouddeployTargetMultiTarget"]:
        '''multi_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#multi_target ClouddeployTarget#multi_target}
        '''
        result = self._values.get("multi_target")
        return typing.cast(typing.Optional["ClouddeployTargetMultiTarget"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#project ClouddeployTarget#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Whether or not the ``Target`` requires approval.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#require_approval ClouddeployTarget#require_approval}
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run(self) -> typing.Optional["ClouddeployTargetRun"]:
        '''run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#run ClouddeployTarget#run}
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional["ClouddeployTargetRun"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ClouddeployTargetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#timeouts ClouddeployTarget#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ClouddeployTargetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetCustomTarget",
    jsii_struct_bases=[],
    name_mapping={"custom_target_type": "customTargetType"},
)
class ClouddeployTargetCustomTarget:
    def __init__(self, *, custom_target_type: builtins.str) -> None:
        '''
        :param custom_target_type: Required. The name of the CustomTargetType. Format must be ``projects/{project}/locations/{location}/customTargetTypes/{custom_target_type}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#custom_target_type ClouddeployTarget#custom_target_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3462772cdd7530dca155e010376898f9bd192120868cd70ae9d89bafed04c8a)
            check_type(argname="argument custom_target_type", value=custom_target_type, expected_type=type_hints["custom_target_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_target_type": custom_target_type,
        }

    @builtins.property
    def custom_target_type(self) -> builtins.str:
        '''Required. The name of the CustomTargetType. Format must be ``projects/{project}/locations/{location}/customTargetTypes/{custom_target_type}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#custom_target_type ClouddeployTarget#custom_target_type}
        '''
        result = self._values.get("custom_target_type")
        assert result is not None, "Required property 'custom_target_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetCustomTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetCustomTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetCustomTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__471d307a87e424cb12235000a5773dea9f49558b290662a85c9960e8b16eb0b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="customTargetTypeInput")
    def custom_target_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customTargetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customTargetType")
    def custom_target_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customTargetType"))

    @custom_target_type.setter
    def custom_target_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e410c2dbe8171b857fb0049199016e2681dd7552516fe4f01019609e61358fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTargetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployTargetCustomTarget]:
        return typing.cast(typing.Optional[ClouddeployTargetCustomTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployTargetCustomTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c7ab3ddbc0c442c1cbe96785193ff42067840b77046bc39b89d845cd097e44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetExecutionConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "usages": "usages",
        "artifact_storage": "artifactStorage",
        "execution_timeout": "executionTimeout",
        "service_account": "serviceAccount",
        "verbose": "verbose",
        "worker_pool": "workerPool",
    },
)
class ClouddeployTargetExecutionConfigs:
    def __init__(
        self,
        *,
        usages: typing.Sequence[builtins.str],
        artifact_storage: typing.Optional[builtins.str] = None,
        execution_timeout: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        verbose: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param usages: Required. Usages when this configuration should be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#usages ClouddeployTarget#usages}
        :param artifact_storage: Optional. Cloud Storage location in which to store execution outputs. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#artifact_storage ClouddeployTarget#artifact_storage}
        :param execution_timeout: Optional. Execution timeout for a Cloud Build Execution. This must be between 10m and 24h in seconds format. If unspecified, a default timeout of 1h is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#execution_timeout ClouddeployTarget#execution_timeout}
        :param service_account: Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#service_account ClouddeployTarget#service_account}
        :param verbose: Optional. If true, additional logging will be enabled when running builds in this execution environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#verbose ClouddeployTarget#verbose}
        :param worker_pool: Optional. The resource name of the ``WorkerPool``, with the format ``projects/{project}/locations/{location}/workerPools/{worker_pool}``. If this optional field is unspecified, the default Cloud Build pool will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#worker_pool ClouddeployTarget#worker_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84998a1ce110d9974daf959c6c5847bdf564bd6ed4dae1c9a1a3548be2ed1c9b)
            check_type(argname="argument usages", value=usages, expected_type=type_hints["usages"])
            check_type(argname="argument artifact_storage", value=artifact_storage, expected_type=type_hints["artifact_storage"])
            check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
            check_type(argname="argument worker_pool", value=worker_pool, expected_type=type_hints["worker_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "usages": usages,
        }
        if artifact_storage is not None:
            self._values["artifact_storage"] = artifact_storage
        if execution_timeout is not None:
            self._values["execution_timeout"] = execution_timeout
        if service_account is not None:
            self._values["service_account"] = service_account
        if verbose is not None:
            self._values["verbose"] = verbose
        if worker_pool is not None:
            self._values["worker_pool"] = worker_pool

    @builtins.property
    def usages(self) -> typing.List[builtins.str]:
        '''Required. Usages when this configuration should be applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#usages ClouddeployTarget#usages}
        '''
        result = self._values.get("usages")
        assert result is not None, "Required property 'usages' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def artifact_storage(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Cloud Storage location in which to store execution outputs. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#artifact_storage ClouddeployTarget#artifact_storage}
        '''
        result = self._values.get("artifact_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Execution timeout for a Cloud Build Execution. This must be between 10m and 24h in seconds format. If unspecified, a default timeout of 1h is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#execution_timeout ClouddeployTarget#execution_timeout}
        '''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#service_account ClouddeployTarget#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verbose(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, additional logging will be enabled when running builds in this execution environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#verbose ClouddeployTarget#verbose}
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def worker_pool(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The resource name of the ``WorkerPool``, with the format ``projects/{project}/locations/{location}/workerPools/{worker_pool}``. If this optional field is unspecified, the default Cloud Build pool will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#worker_pool ClouddeployTarget#worker_pool}
        '''
        result = self._values.get("worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetExecutionConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetExecutionConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetExecutionConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6639cb0edc87ccd852f22d4e1b251f60be431a1dcef9f63f2ecd6dc3312d5b2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployTargetExecutionConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5952f7aa637f41cd7212ee25a75b323abb607d9945bac50858c921c85a3fda)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployTargetExecutionConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ab6aa9f68ebec0a63b98eb75eae77ff8f75aba94565363629403714230ae03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d710c2b48047f3e4c08d931874dc21466218b760258ca496100e89fbbae82821)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6407c67a7264a039aaa8e26555c51e573df860571f1c0d71321f58b520662dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetExecutionConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetExecutionConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetExecutionConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3196bba6ed93ebce5a3c8f1e3a8af8a6829a02ab43f6cd023a1bf94983242e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployTargetExecutionConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetExecutionConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77f3802bf66d1273c4d5610fe58143b2e9815235fa8afdc256fa6981714ae4b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetArtifactStorage")
    def reset_artifact_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifactStorage", []))

    @jsii.member(jsii_name="resetExecutionTimeout")
    def reset_execution_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionTimeout", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetVerbose")
    def reset_verbose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerbose", []))

    @jsii.member(jsii_name="resetWorkerPool")
    def reset_worker_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerPool", []))

    @builtins.property
    @jsii.member(jsii_name="artifactStorageInput")
    def artifact_storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="executionTimeoutInput")
    def execution_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="usagesInput")
    def usages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usagesInput"))

    @builtins.property
    @jsii.member(jsii_name="verboseInput")
    def verbose_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verboseInput"))

    @builtins.property
    @jsii.member(jsii_name="workerPoolInput")
    def worker_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactStorage")
    def artifact_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactStorage"))

    @artifact_storage.setter
    def artifact_storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54c4f59dbf928bcc88ff06789c4765791224a26dbb0c6dcf968cb798d7205c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e929512078b5bf2d036f3429a6824fec5d4fbc5a52cf692ddb5f3db1f094b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ded4cfaa947e450caa069d560e535cbfb4741626038b4e957202b28466acd04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usages")
    def usages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usages"))

    @usages.setter
    def usages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a50aa3604201e35be8653e586cc3dd741819c4caaa855146280d1c03c4c89a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verbose")
    def verbose(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verbose"))

    @verbose.setter
    def verbose(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc9ef01cd5f6054a51d4c78d2528bcdcb8038f81c371f0c70f6e34a3e2ab75e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verbose", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerPool"))

    @worker_pool.setter
    def worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79bf750ed996805ec2b6b33960483efa4a3a821ec07c36349a8b0fde3010fd6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetExecutionConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetExecutionConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetExecutionConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b283c22f55814a805d2b37320c1f045f21ddd996408d2baec5ded8492d1645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetGke",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "dns_endpoint": "dnsEndpoint",
        "internal_ip": "internalIp",
        "proxy_url": "proxyUrl",
    },
)
class ClouddeployTargetGke:
    def __init__(
        self,
        *,
        cluster: typing.Optional[builtins.str] = None,
        dns_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: Information specifying a GKE Cluster. Format is `projects/{project_id}/locations/{location_id}/clusters/{cluster_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#cluster ClouddeployTarget#cluster}
        :param dns_endpoint: Optional. If set, the cluster will be accessed using the DNS endpoint. Note that both ``dns_endpoint`` and ``internal_ip`` cannot be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#dns_endpoint ClouddeployTarget#dns_endpoint}
        :param internal_ip: Optional. If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#internal_ip ClouddeployTarget#internal_ip}
        :param proxy_url: Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#proxy_url ClouddeployTarget#proxy_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08270d82f024df8ce96291cf9ed4bf0bd76d97d9fe539bc471f2dbc9dd229b43)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument dns_endpoint", value=dns_endpoint, expected_type=type_hints["dns_endpoint"])
            check_type(argname="argument internal_ip", value=internal_ip, expected_type=type_hints["internal_ip"])
            check_type(argname="argument proxy_url", value=proxy_url, expected_type=type_hints["proxy_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster
        if dns_endpoint is not None:
            self._values["dns_endpoint"] = dns_endpoint
        if internal_ip is not None:
            self._values["internal_ip"] = internal_ip
        if proxy_url is not None:
            self._values["proxy_url"] = proxy_url

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''Information specifying a GKE Cluster. Format is `projects/{project_id}/locations/{location_id}/clusters/{cluster_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#cluster ClouddeployTarget#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If set, the cluster will be accessed using the DNS endpoint. Note that both ``dns_endpoint`` and ``internal_ip`` cannot be set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#dns_endpoint ClouddeployTarget#dns_endpoint}
        '''
        result = self._values.get("dns_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def internal_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#internal_ip ClouddeployTarget#internal_ip}
        '''
        result = self._values.get("internal_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#proxy_url ClouddeployTarget#proxy_url}
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetGke(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetGkeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetGkeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b14b83d2182e0769cffcdfb60bc6cfdafded14cd10d44ba1c7ec7277dbe43c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCluster")
    def reset_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCluster", []))

    @jsii.member(jsii_name="resetDnsEndpoint")
    def reset_dns_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsEndpoint", []))

    @jsii.member(jsii_name="resetInternalIp")
    def reset_internal_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIp", []))

    @jsii.member(jsii_name="resetProxyUrl")
    def reset_proxy_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyUrl", []))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsEndpointInput")
    def dns_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dnsEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpInput")
    def internal_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalIpInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyUrlInput")
    def proxy_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53536d5b0277653e46800f86913e7c79c1d45d9f48f269acee8d4917983f1c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsEndpoint")
    def dns_endpoint(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dnsEndpoint"))

    @dns_endpoint.setter
    def dns_endpoint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ac1a7618c0881bf87ded676f38ea553240a1e8bb2f53b6a464bb42a13499e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalIp")
    def internal_ip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internalIp"))

    @internal_ip.setter
    def internal_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74fb0512462075290f6affc4aefa81cca85da326f08aa4d5a70df03f1fc140a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyUrl")
    def proxy_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyUrl"))

    @proxy_url.setter
    def proxy_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473f91a1424b23e1e3927281fcd24d5e0ace250e670d8414f775b80425cae742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployTargetGke]:
        return typing.cast(typing.Optional[ClouddeployTargetGke], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ClouddeployTargetGke]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfcee9cb2a53145dc2229efa23f7c6e2d7ed0cc908e9b3fd35c5e629f3e72982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetMultiTarget",
    jsii_struct_bases=[],
    name_mapping={"target_ids": "targetIds"},
)
class ClouddeployTargetMultiTarget:
    def __init__(self, *, target_ids: typing.Sequence[builtins.str]) -> None:
        '''
        :param target_ids: Required. The target_ids of this multiTarget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#target_ids ClouddeployTarget#target_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc298b149b1d6dedace6aa307c975d42f8c6ad3c7ebe6c6b3830d9b3004ebad)
            check_type(argname="argument target_ids", value=target_ids, expected_type=type_hints["target_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_ids": target_ids,
        }

    @builtins.property
    def target_ids(self) -> typing.List[builtins.str]:
        '''Required. The target_ids of this multiTarget.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#target_ids ClouddeployTarget#target_ids}
        '''
        result = self._values.get("target_ids")
        assert result is not None, "Required property 'target_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetMultiTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetMultiTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetMultiTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0248840f6304f9910103ed5287d0f8231299d5916ee3270b892056a043dc9c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="targetIdsInput")
    def target_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetIds")
    def target_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetIds"))

    @target_ids.setter
    def target_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d21d84e7670091747bd64122329c7eb8484525f1e5d54cfb8f51aadfc11a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployTargetMultiTarget]:
        return typing.cast(typing.Optional[ClouddeployTargetMultiTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployTargetMultiTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0954e12fc9e028eabf28c40cf07396df42b7ab7eaa41b107e6cd296e9c4034d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetRun",
    jsii_struct_bases=[],
    name_mapping={"location": "location"},
)
class ClouddeployTargetRun:
    def __init__(self, *, location: builtins.str) -> None:
        '''
        :param location: Required. The location where the Cloud Run Service should be located. Format is ``projects/{project}/locations/{location}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#location ClouddeployTarget#location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b24c377b86c0dfa744f401b03d41c83cceb0b6d168f74ae4f1804806f228d51)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }

    @builtins.property
    def location(self) -> builtins.str:
        '''Required. The location where the Cloud Run Service should be located. Format is ``projects/{project}/locations/{location}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#location ClouddeployTarget#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0c5b274bbd65550c49426c8756cb6854e90228e912d1b9d47574847db3b2b70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ac16ceb3ba9300ac862d9a38e7768bc4d2a05c070030da91a1a6834f63dcc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployTargetRun]:
        return typing.cast(typing.Optional[ClouddeployTargetRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ClouddeployTargetRun]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a48c6baa8835823065740a1df22f728029d6bd3a17b1b9d0ea596ca3c023e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ClouddeployTargetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#create ClouddeployTarget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#delete ClouddeployTarget#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#update ClouddeployTarget#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b736c785504f29a9a635c805715812d69ee7894299c7c007477fb9d6844ff223)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#create ClouddeployTarget#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#delete ClouddeployTarget#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_target#update ClouddeployTarget#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployTargetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployTargetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployTarget.ClouddeployTargetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83629de513867b11319fc8b56ba250b9b448ed2bea6a4a2e392814c5545db3c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f01f7fbed9ea35e3e80b90e7e886e6dd26d4340d2522122634d3eee13c4114ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de2200e2c87e927b2e7069373cc25803320a90ebb054fa416da9439d3eabec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899fd2fc730561aba7961b0cac03a4a60a1a45ca26bce4821d9eedb307c7c5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc6a0547c236ee263f78d2a6ef1da7eaf42fe54f9938ebba3b7759d44837701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ClouddeployTarget",
    "ClouddeployTargetAnthosCluster",
    "ClouddeployTargetAnthosClusterOutputReference",
    "ClouddeployTargetAssociatedEntities",
    "ClouddeployTargetAssociatedEntitiesAnthosClusters",
    "ClouddeployTargetAssociatedEntitiesAnthosClustersList",
    "ClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference",
    "ClouddeployTargetAssociatedEntitiesGkeClusters",
    "ClouddeployTargetAssociatedEntitiesGkeClustersList",
    "ClouddeployTargetAssociatedEntitiesGkeClustersOutputReference",
    "ClouddeployTargetAssociatedEntitiesList",
    "ClouddeployTargetAssociatedEntitiesOutputReference",
    "ClouddeployTargetConfig",
    "ClouddeployTargetCustomTarget",
    "ClouddeployTargetCustomTargetOutputReference",
    "ClouddeployTargetExecutionConfigs",
    "ClouddeployTargetExecutionConfigsList",
    "ClouddeployTargetExecutionConfigsOutputReference",
    "ClouddeployTargetGke",
    "ClouddeployTargetGkeOutputReference",
    "ClouddeployTargetMultiTarget",
    "ClouddeployTargetMultiTargetOutputReference",
    "ClouddeployTargetRun",
    "ClouddeployTargetRunOutputReference",
    "ClouddeployTargetTimeouts",
    "ClouddeployTargetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__335bf03e4270efe72a15ee1d747146fdd20839f223fa162df689621ca355a29b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anthos_cluster: typing.Optional[typing.Union[ClouddeployTargetAnthosCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    associated_entities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_target: typing.Optional[typing.Union[ClouddeployTargetCustomTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    deploy_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetExecutionConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gke: typing.Optional[typing.Union[ClouddeployTargetGke, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    multi_target: typing.Optional[typing.Union[ClouddeployTargetMultiTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run: typing.Optional[typing.Union[ClouddeployTargetRun, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployTargetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b38af56ad058a2af1d57d6cfe41af57a06e8bf581a2fa24399abffdeece52460(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a83a1acb6694b00f7a91ffdaae564dee1354e31cb665c1e5e1c8602b80b508(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eee78930adcecf319d10fdb483db87a360d58853f2d85c14539cf9737ce2790(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetExecutionConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d09480dc9cc263f5bed4c40420e927acc711b09922cffe09d2575fcb5e3c58(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6454df26bf956a9e1f1cbd1b0190aed4e513a95ade4ec2c9945a20596d92bc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1c30c4449358203ae1a056bf2700b43b62e471c4527e36858cb75572161f8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c953722a628e98aa5f06b3f08d69263e1dc15bf2aa8001200cc1c2e58844028e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0271f9243ccba1e0736f6ccd9dc11819fa6473f3c8069fe63f3d65b89769e6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdefe4eb33f30ebc41fb56b554133cf95fc53f06a69626d3a9f61449716fe42b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22f10bf1f0d9dc36ff7b8dc096a2385389287e6b061679f7c690758685e945e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7ce556bec2d9f500e10d0a1ef1fa7e689337f56201f672189cd2fadc16ce7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47172b979875fdb56f9209644b82a8308f9e41900756abcf0bf9a1e8ba19b36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5174e11b7c9291b623072a3255afa79ab2e5ac64cf64a2557b40ae8bb43b73(
    *,
    membership: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1745c03716abe1fada29d2f26a96aba9b7b3a07399a9a777a994d74211d190fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ffe975523899eae50cb4911e3d7b5f9b61c77089b46911a54e5c1a67ad73452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd01fe66f326b18c95cc100744bc9abed2d4990f49410932ff831dbbd40cd0d8(
    value: typing.Optional[ClouddeployTargetAnthosCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6752143ddd9e2c0b275effc566588b2737a49de51bee61e1822f91c98d1b7f08(
    *,
    entity_id: builtins.str,
    anthos_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntitiesAnthosClusters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntitiesGkeClusters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae446c436f417873a91f6ee3d04ee11a3c0cd7413cdd68efd7e0397ac5fd2bf(
    *,
    membership: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765d3d66cda46d4820e58c2a68493311064531f0c82cf6ab621761cf8233eb77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a46b0910c3a57ebe3d3004fbacf6e013ce198562708aabbd8f27b6638949dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb876e9822ed1712ffdaefd1d550c190e4e8315c41a225de8f20dffab63c20b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e83a55529370238345d6db81272cd9bdf61cf8a8b3ad4e6dbb40f7ffa0f05e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5cbd5ae3371e79ee5fed9ed47cffd9da3bbb0741a9a9a069bbac13b962968f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8752e235b296383107d4c1a3c508ca767862b25347d3700e30a39fb3a247e69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesAnthosClusters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c07dcb20ea882239ec693cf6b28fbdbfae529684f48452d37f88746042ef0c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0da0d7473446b89dbb1507732ed7798d243a27c5c6b1247996d0b05ed6f0f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabcb7c76674e13b0a7ca20c8273047c1d4f1975d259d1cddcd698eeaccb4cc9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntitiesAnthosClusters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf07d60ca5078cc394e094cae14c9cff0908c065ecc33fe26441c93606bb26f(
    *,
    cluster: typing.Optional[builtins.str] = None,
    internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proxy_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9013ddf277b0ae3066cd287ed406ef9b6f1c81ab2cecebc61a80426c040be8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91ff8493a4391c729bc6a51afc5c7349f15c4a4b63c94b47aa903dccf30a6b3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2c528780876944ec2eb5bc0252cae69436cbe16ac6f737c3e44487964c9b80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31aa255ff056117f5799a3c8e4ba2501b20687036a02b6de7a6946695bf7b83(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435a33b0e202dfa639c8973e99fd5398233af29c50225f3db8e951c97da72a16(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229dc7e0a321bb61239f634040848ef274672b67b37a096ba825acd2bb51e597(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntitiesGkeClusters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c183e33c97c9f554816b0fa14b92679ebda0ce1857d4b3ddd693c84d3cfdf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37a3ac4aaba90d9fdfd0f7e40b4c1151004af3ed5526cd2062df2018de83864(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519c4cc217fa50be8a1282a58734ea966ad63c28b97022455d04100fe4964a22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a95b598bde816d1d91f9b00eebc1c769307c2ece9fb5ebbe4de782c6184c155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee5aff2829a2d15474069e05fffba78338fbd1cbc25434d08853fd521a01e68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntitiesGkeClusters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5cfb9c5d969208f357bad9f828523413817c3b9984ef15a2345e43db7bf2a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb605c17167b4f80f9acff01a6cc4e6af68ab889cf3f2c8f9b5b3b85e9e9efa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3162205158e354a6b5444b888291df00301548f19268fea6a42fa29f265031e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c27d6c5cedc32b89c784e16e695064cfec8cae6bb30a86743153efa565cd48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e853d6c409a1461ef0f3031483903f66bd15d75a0e46658e3e26ab3d8b731f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8c64dee230a0af3f15ba20823f3de230d86347d66f25bc45d7292471f74454(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetAssociatedEntities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12be70c813dd7579f2ba315274d421a78364c6574d819299abb1b937f3dbc6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9736a5227dc275274af0cac9fa02a2a3b29792763639499019c53b59a193f5fd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntitiesAnthosClusters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ad56bb59bc06038a4c1223ae1032bbd0cdb78e2e3aac5b061e36d03fccd7b7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntitiesGkeClusters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9894d76e60ff8ec1de8792aa0152ea4ef25f1154620b3050656cdc24356b8f47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39dd1f10daf43d42abdb718af3a51f7241fd06d81f7f3447d79b23869ceeea83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetAssociatedEntities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9378670a678b371adb2b7bf70ad7c247d15d672ddde04fde93e6c2a778f0c09(
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
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anthos_cluster: typing.Optional[typing.Union[ClouddeployTargetAnthosCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    associated_entities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetAssociatedEntities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_target: typing.Optional[typing.Union[ClouddeployTargetCustomTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    deploy_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployTargetExecutionConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gke: typing.Optional[typing.Union[ClouddeployTargetGke, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    multi_target: typing.Optional[typing.Union[ClouddeployTargetMultiTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run: typing.Optional[typing.Union[ClouddeployTargetRun, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployTargetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3462772cdd7530dca155e010376898f9bd192120868cd70ae9d89bafed04c8a(
    *,
    custom_target_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471d307a87e424cb12235000a5773dea9f49558b290662a85c9960e8b16eb0b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e410c2dbe8171b857fb0049199016e2681dd7552516fe4f01019609e61358fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c7ab3ddbc0c442c1cbe96785193ff42067840b77046bc39b89d845cd097e44(
    value: typing.Optional[ClouddeployTargetCustomTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84998a1ce110d9974daf959c6c5847bdf564bd6ed4dae1c9a1a3548be2ed1c9b(
    *,
    usages: typing.Sequence[builtins.str],
    artifact_storage: typing.Optional[builtins.str] = None,
    execution_timeout: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    verbose: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    worker_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6639cb0edc87ccd852f22d4e1b251f60be431a1dcef9f63f2ecd6dc3312d5b2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5952f7aa637f41cd7212ee25a75b323abb607d9945bac50858c921c85a3fda(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ab6aa9f68ebec0a63b98eb75eae77ff8f75aba94565363629403714230ae03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d710c2b48047f3e4c08d931874dc21466218b760258ca496100e89fbbae82821(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6407c67a7264a039aaa8e26555c51e573df860571f1c0d71321f58b520662dd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3196bba6ed93ebce5a3c8f1e3a8af8a6829a02ab43f6cd023a1bf94983242e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployTargetExecutionConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f3802bf66d1273c4d5610fe58143b2e9815235fa8afdc256fa6981714ae4b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54c4f59dbf928bcc88ff06789c4765791224a26dbb0c6dcf968cb798d7205c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e929512078b5bf2d036f3429a6824fec5d4fbc5a52cf692ddb5f3db1f094b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ded4cfaa947e450caa069d560e535cbfb4741626038b4e957202b28466acd04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a50aa3604201e35be8653e586cc3dd741819c4caaa855146280d1c03c4c89a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9ef01cd5f6054a51d4c78d2528bcdcb8038f81c371f0c70f6e34a3e2ab75e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bf750ed996805ec2b6b33960483efa4a3a821ec07c36349a8b0fde3010fd6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b283c22f55814a805d2b37320c1f045f21ddd996408d2baec5ded8492d1645(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetExecutionConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08270d82f024df8ce96291cf9ed4bf0bd76d97d9fe539bc471f2dbc9dd229b43(
    *,
    cluster: typing.Optional[builtins.str] = None,
    dns_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proxy_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b14b83d2182e0769cffcdfb60bc6cfdafded14cd10d44ba1c7ec7277dbe43c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53536d5b0277653e46800f86913e7c79c1d45d9f48f269acee8d4917983f1c52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ac1a7618c0881bf87ded676f38ea553240a1e8bb2f53b6a464bb42a13499e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74fb0512462075290f6affc4aefa81cca85da326f08aa4d5a70df03f1fc140a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473f91a1424b23e1e3927281fcd24d5e0ace250e670d8414f775b80425cae742(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfcee9cb2a53145dc2229efa23f7c6e2d7ed0cc908e9b3fd35c5e629f3e72982(
    value: typing.Optional[ClouddeployTargetGke],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc298b149b1d6dedace6aa307c975d42f8c6ad3c7ebe6c6b3830d9b3004ebad(
    *,
    target_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0248840f6304f9910103ed5287d0f8231299d5916ee3270b892056a043dc9c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d21d84e7670091747bd64122329c7eb8484525f1e5d54cfb8f51aadfc11a05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0954e12fc9e028eabf28c40cf07396df42b7ab7eaa41b107e6cd296e9c4034d6(
    value: typing.Optional[ClouddeployTargetMultiTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b24c377b86c0dfa744f401b03d41c83cceb0b6d168f74ae4f1804806f228d51(
    *,
    location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c5b274bbd65550c49426c8756cb6854e90228e912d1b9d47574847db3b2b70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ac16ceb3ba9300ac862d9a38e7768bc4d2a05c070030da91a1a6834f63dcc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a48c6baa8835823065740a1df22f728029d6bd3a17b1b9d0ea596ca3c023e5a(
    value: typing.Optional[ClouddeployTargetRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b736c785504f29a9a635c805715812d69ee7894299c7c007477fb9d6844ff223(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83629de513867b11319fc8b56ba250b9b448ed2bea6a4a2e392814c5545db3c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01f7fbed9ea35e3e80b90e7e886e6dd26d4340d2522122634d3eee13c4114ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de2200e2c87e927b2e7069373cc25803320a90ebb054fa416da9439d3eabec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899fd2fc730561aba7961b0cac03a4a60a1a45ca26bce4821d9eedb307c7c5f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc6a0547c236ee263f78d2a6ef1da7eaf42fe54f9938ebba3b7759d44837701(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployTargetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
