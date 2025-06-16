r'''
# `google_clouddeploy_target`

Refer to the Terraform Registry for docs: [`google_clouddeploy_target`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target).
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


class GoogleClouddeployTarget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTarget",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target google_clouddeploy_target}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        anthos_cluster: typing.Optional[typing.Union["GoogleClouddeployTargetAnthosCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        associated_entities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployTargetAssociatedEntities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_target: typing.Optional[typing.Union["GoogleClouddeployTargetCustomTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        deploy_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployTargetExecutionConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gke: typing.Optional[typing.Union["GoogleClouddeployTargetGke", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        multi_target: typing.Optional[typing.Union["GoogleClouddeployTargetMultiTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run: typing.Optional[typing.Union["GoogleClouddeployTargetRun", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployTargetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target google_clouddeploy_target} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#location GoogleClouddeployTarget#location}
        :param name: Name of the ``Target``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#name GoogleClouddeployTarget#name}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#annotations GoogleClouddeployTarget#annotations}
        :param anthos_cluster: anthos_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#anthos_cluster GoogleClouddeployTarget#anthos_cluster}
        :param associated_entities: associated_entities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#associated_entities GoogleClouddeployTarget#associated_entities}
        :param custom_target: custom_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#custom_target GoogleClouddeployTarget#custom_target}
        :param deploy_parameters: Optional. The deploy parameters to use for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#deploy_parameters GoogleClouddeployTarget#deploy_parameters}
        :param description: Optional. Description of the ``Target``. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#description GoogleClouddeployTarget#description}
        :param execution_configs: execution_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#execution_configs GoogleClouddeployTarget#execution_configs}
        :param gke: gke block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#gke GoogleClouddeployTarget#gke}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#id GoogleClouddeployTarget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#labels GoogleClouddeployTarget#labels}
        :param multi_target: multi_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#multi_target GoogleClouddeployTarget#multi_target}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#project GoogleClouddeployTarget#project}
        :param require_approval: Optional. Whether or not the ``Target`` requires approval. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#require_approval GoogleClouddeployTarget#require_approval}
        :param run: run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#run GoogleClouddeployTarget#run}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#timeouts GoogleClouddeployTarget#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83a80fab5cbbb1d1a8234f82ed985400cf205bb3ca8388a5c2056e5ed2a786c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleClouddeployTargetConfig(
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
        '''Generates CDKTF code for importing a GoogleClouddeployTarget resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleClouddeployTarget to import.
        :param import_from_id: The id of the existing GoogleClouddeployTarget that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleClouddeployTarget to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e1aa1a1721ab7e9c1d1cba362cc9faa1cc66eb394fe0b0eaa5fadc042b248b)
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
        :param membership: Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#membership GoogleClouddeployTarget#membership}
        '''
        value = GoogleClouddeployTargetAnthosCluster(membership=membership)

        return typing.cast(None, jsii.invoke(self, "putAnthosCluster", [value]))

    @jsii.member(jsii_name="putAssociatedEntities")
    def put_associated_entities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployTargetAssociatedEntities", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3701f4a39242470dc62a440ace5e8a3e93381bcba09c05c8d4b11a325e1704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAssociatedEntities", [value]))

    @jsii.member(jsii_name="putCustomTarget")
    def put_custom_target(self, *, custom_target_type: builtins.str) -> None:
        '''
        :param custom_target_type: Required. The name of the CustomTargetType. Format must be ``projects/{project}/locations/{location}/customTargetTypes/{custom_target_type}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#custom_target_type GoogleClouddeployTarget#custom_target_type}
        '''
        value = GoogleClouddeployTargetCustomTarget(
            custom_target_type=custom_target_type
        )

        return typing.cast(None, jsii.invoke(self, "putCustomTarget", [value]))

    @jsii.member(jsii_name="putExecutionConfigs")
    def put_execution_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployTargetExecutionConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8289836d490025823f88a406b669bcb010c96ea2d45644364188bc70627fe13)
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
        :param cluster: Information specifying a GKE Cluster. Format is `projects/{project_id}/locations/{location_id}/clusters/{cluster_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#cluster GoogleClouddeployTarget#cluster}
        :param dns_endpoint: Optional. If set, the cluster will be accessed using the DNS endpoint. Note that both ``dns_endpoint`` and ``internal_ip`` cannot be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#dns_endpoint GoogleClouddeployTarget#dns_endpoint}
        :param internal_ip: Optional. If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#internal_ip GoogleClouddeployTarget#internal_ip}
        :param proxy_url: Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#proxy_url GoogleClouddeployTarget#proxy_url}
        '''
        value = GoogleClouddeployTargetGke(
            cluster=cluster,
            dns_endpoint=dns_endpoint,
            internal_ip=internal_ip,
            proxy_url=proxy_url,
        )

        return typing.cast(None, jsii.invoke(self, "putGke", [value]))

    @jsii.member(jsii_name="putMultiTarget")
    def put_multi_target(self, *, target_ids: typing.Sequence[builtins.str]) -> None:
        '''
        :param target_ids: Required. The target_ids of this multiTarget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#target_ids GoogleClouddeployTarget#target_ids}
        '''
        value = GoogleClouddeployTargetMultiTarget(target_ids=target_ids)

        return typing.cast(None, jsii.invoke(self, "putMultiTarget", [value]))

    @jsii.member(jsii_name="putRun")
    def put_run(self, *, location: builtins.str) -> None:
        '''
        :param location: Required. The location where the Cloud Run Service should be located. Format is ``projects/{project}/locations/{location}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#location GoogleClouddeployTarget#location}
        '''
        value = GoogleClouddeployTargetRun(location=location)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#create GoogleClouddeployTarget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#delete GoogleClouddeployTarget#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#update GoogleClouddeployTarget#update}.
        '''
        value = GoogleClouddeployTargetTimeouts(
            create=create, delete=delete, update=update
        )

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
    def anthos_cluster(self) -> "GoogleClouddeployTargetAnthosClusterOutputReference":
        return typing.cast("GoogleClouddeployTargetAnthosClusterOutputReference", jsii.get(self, "anthosCluster"))

    @builtins.property
    @jsii.member(jsii_name="associatedEntities")
    def associated_entities(self) -> "GoogleClouddeployTargetAssociatedEntitiesList":
        return typing.cast("GoogleClouddeployTargetAssociatedEntitiesList", jsii.get(self, "associatedEntities"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="customTarget")
    def custom_target(self) -> "GoogleClouddeployTargetCustomTargetOutputReference":
        return typing.cast("GoogleClouddeployTargetCustomTargetOutputReference", jsii.get(self, "customTarget"))

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
    def execution_configs(self) -> "GoogleClouddeployTargetExecutionConfigsList":
        return typing.cast("GoogleClouddeployTargetExecutionConfigsList", jsii.get(self, "executionConfigs"))

    @builtins.property
    @jsii.member(jsii_name="gke")
    def gke(self) -> "GoogleClouddeployTargetGkeOutputReference":
        return typing.cast("GoogleClouddeployTargetGkeOutputReference", jsii.get(self, "gke"))

    @builtins.property
    @jsii.member(jsii_name="multiTarget")
    def multi_target(self) -> "GoogleClouddeployTargetMultiTargetOutputReference":
        return typing.cast("GoogleClouddeployTargetMultiTargetOutputReference", jsii.get(self, "multiTarget"))

    @builtins.property
    @jsii.member(jsii_name="run")
    def run(self) -> "GoogleClouddeployTargetRunOutputReference":
        return typing.cast("GoogleClouddeployTargetRunOutputReference", jsii.get(self, "run"))

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
    def timeouts(self) -> "GoogleClouddeployTargetTimeoutsOutputReference":
        return typing.cast("GoogleClouddeployTargetTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def anthos_cluster_input(
        self,
    ) -> typing.Optional["GoogleClouddeployTargetAnthosCluster"]:
        return typing.cast(typing.Optional["GoogleClouddeployTargetAnthosCluster"], jsii.get(self, "anthosClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedEntitiesInput")
    def associated_entities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetAssociatedEntities"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetAssociatedEntities"]]], jsii.get(self, "associatedEntitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="customTargetInput")
    def custom_target_input(
        self,
    ) -> typing.Optional["GoogleClouddeployTargetCustomTarget"]:
        return typing.cast(typing.Optional["GoogleClouddeployTargetCustomTarget"], jsii.get(self, "customTargetInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetExecutionConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetExecutionConfigs"]]], jsii.get(self, "executionConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeInput")
    def gke_input(self) -> typing.Optional["GoogleClouddeployTargetGke"]:
        return typing.cast(typing.Optional["GoogleClouddeployTargetGke"], jsii.get(self, "gkeInput"))

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
    def multi_target_input(
        self,
    ) -> typing.Optional["GoogleClouddeployTargetMultiTarget"]:
        return typing.cast(typing.Optional["GoogleClouddeployTargetMultiTarget"], jsii.get(self, "multiTargetInput"))

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
    def run_input(self) -> typing.Optional["GoogleClouddeployTargetRun"]:
        return typing.cast(typing.Optional["GoogleClouddeployTargetRun"], jsii.get(self, "runInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployTargetTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployTargetTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7df951be790ab4ab2587b19e16c4a8c6c9af2aba51308609575825cd5aecf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18b88ec23314ca124980c91af9ea6a9febe107fda5b1608e995efd241bad097c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65d11c6f338c66b4b4b25ea796f25827255503cbee4ad4e966465b368831162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bcf966ebf8bea35b56f079db8fe4bf2bc44c3f9ffed2eaeb7c7cda5e5bce83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ace9c194377f9a257a098b0f6b7c869f4ed70491ad3dc71e75e1f6841ff476e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b82a3e283973bdaf8743d7eb07e4ec1756068d33a88071f17a65f75b3e2eb5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9563b021e4ae2da4a99e954dd12e35f7ddd9886033f210cfe87a90a74b1a5da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8dc22a9b95bc0fd5826f62a198a17449c543714fa939faeef075051eb8243e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0899b0cbf7269ab14ed2390b3ed679b015395f791c4720cb185bd24c1a731c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireApproval", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAnthosCluster",
    jsii_struct_bases=[],
    name_mapping={"membership": "membership"},
)
class GoogleClouddeployTargetAnthosCluster:
    def __init__(self, *, membership: typing.Optional[builtins.str] = None) -> None:
        '''
        :param membership: Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#membership GoogleClouddeployTarget#membership}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf1076ade2a45449c15e564efb6c5b96b3ef24397333cb775ac9159444faa1f)
            check_type(argname="argument membership", value=membership, expected_type=type_hints["membership"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if membership is not None:
            self._values["membership"] = membership

    @builtins.property
    def membership(self) -> typing.Optional[builtins.str]:
        '''Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#membership GoogleClouddeployTarget#membership}
        '''
        result = self._values.get("membership")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetAnthosCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetAnthosClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAnthosClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe3b7a09afa8b1245a5138116cd4365a161b067b2d18770e21307e0c2c79f4a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93076cc9f8529fabee6c08837eeafd810fe3859b2d65747abf8783042f5fd6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleClouddeployTargetAnthosCluster]:
        return typing.cast(typing.Optional[GoogleClouddeployTargetAnthosCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployTargetAnthosCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6f57ebf599a8b9ecff19d4fbd8535ae30cdd7f4c943d0049466a82f9efc35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntities",
    jsii_struct_bases=[],
    name_mapping={
        "entity_id": "entityId",
        "anthos_clusters": "anthosClusters",
        "gke_clusters": "gkeClusters",
    },
)
class GoogleClouddeployTargetAssociatedEntities:
    def __init__(
        self,
        *,
        entity_id: builtins.str,
        anthos_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployTargetAssociatedEntitiesAnthosClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployTargetAssociatedEntitiesGkeClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param entity_id: The name for the key in the map for which this object is mapped to in the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#entity_id GoogleClouddeployTarget#entity_id}
        :param anthos_clusters: anthos_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#anthos_clusters GoogleClouddeployTarget#anthos_clusters}
        :param gke_clusters: gke_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#gke_clusters GoogleClouddeployTarget#gke_clusters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27aeaa934f224ecca153fbd89b9f912fa4b644c4c6c719882610c6a2c6f9726)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#entity_id GoogleClouddeployTarget#entity_id}
        '''
        result = self._values.get("entity_id")
        assert result is not None, "Required property 'entity_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def anthos_clusters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetAssociatedEntitiesAnthosClusters"]]]:
        '''anthos_clusters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#anthos_clusters GoogleClouddeployTarget#anthos_clusters}
        '''
        result = self._values.get("anthos_clusters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetAssociatedEntitiesAnthosClusters"]]], result)

    @builtins.property
    def gke_clusters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetAssociatedEntitiesGkeClusters"]]]:
        '''gke_clusters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#gke_clusters GoogleClouddeployTarget#gke_clusters}
        '''
        result = self._values.get("gke_clusters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetAssociatedEntitiesGkeClusters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetAssociatedEntities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntitiesAnthosClusters",
    jsii_struct_bases=[],
    name_mapping={"membership": "membership"},
)
class GoogleClouddeployTargetAssociatedEntitiesAnthosClusters:
    def __init__(self, *, membership: typing.Optional[builtins.str] = None) -> None:
        '''
        :param membership: Optional. Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#membership GoogleClouddeployTarget#membership}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95387bb306e6c9d0b1372e2623cd0594e7d58d14c7f4a415bb1939a87991a69b)
            check_type(argname="argument membership", value=membership, expected_type=type_hints["membership"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if membership is not None:
            self._values["membership"] = membership

    @builtins.property
    def membership(self) -> typing.Optional[builtins.str]:
        '''Optional. Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is ``projects/{project}/locations/{location}/memberships/{membership_name}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#membership GoogleClouddeployTarget#membership}
        '''
        result = self._values.get("membership")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetAssociatedEntitiesAnthosClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetAssociatedEntitiesAnthosClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntitiesAnthosClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c89e03d3c8b1f18b1b0be6f6992cbd6996fbdf09a5200e25e8057f546bec494)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c7315256f60886405242123357ec89762ee19668ed73ca67ec47cd161c132a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c772a806a4dce3b27d7359fda5ac5c410e7c075a20fd3f90baa7fa4eebad8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b376b3792ec822f29b17a4f046432ba883d8036797686d87bb750b593dbb388)
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
            type_hints = typing.get_type_hints(_typecheckingstub__248f9fd11770110d1cbb6d9b03bdfee38786bb3c18b73d8fadc487438a48c9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e43788b8c4a3fb7eba6d6f22861a2339eed68ab35451c6ee2853e2c32155e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a5404447e3e03d6a14d3ac4bcb1198a68d707496b90db74255d3bf9d69a754d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51c336f6d9c983f4a760042b9a07139db6496c93227b12eee82f89f8d459e002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12c8b3cdd2c73360113f9d27a1f8c5b0262ac2b1cf38721917a9df770978305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntitiesGkeClusters",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "internal_ip": "internalIp",
        "proxy_url": "proxyUrl",
    },
)
class GoogleClouddeployTargetAssociatedEntitiesGkeClusters:
    def __init__(
        self,
        *,
        cluster: typing.Optional[builtins.str] = None,
        internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: Optional. Information specifying a GKE Cluster. Format is ``projects/{project_id}/locations/{location_id}/clusters/{cluster_id}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#cluster GoogleClouddeployTarget#cluster}
        :param internal_ip: Optional. If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#internal_ip GoogleClouddeployTarget#internal_ip}
        :param proxy_url: Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#proxy_url GoogleClouddeployTarget#proxy_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b570f90dd3b597b2014f47be92a9bf2ee7666477f0dfb424709a43632c00edc4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#cluster GoogleClouddeployTarget#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#internal_ip GoogleClouddeployTarget#internal_ip}
        '''
        result = self._values.get("internal_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#proxy_url GoogleClouddeployTarget#proxy_url}
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetAssociatedEntitiesGkeClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetAssociatedEntitiesGkeClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntitiesGkeClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eaa4463c6e5dc8b0739c2ee73342aab27a65a3dfce1a2bb5186d77b3327076b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployTargetAssociatedEntitiesGkeClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1354bc210f81bc437bd9c7894205d0d02f8c07d97f4b80e51668ac0cc3a9614)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployTargetAssociatedEntitiesGkeClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fc4c5c86d39f80d05e44f1303d5417713a2cdb63ffe6a04e14526d8d16120a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f29dc50909659e319b8bd1662d4b2fe4b8debe53c904abe86d5fe0b567acd7d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ecfb4112e03cd8d74ca5ef77b6f3fd4762cf3a521120c5a341ef35110a80d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesGkeClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesGkeClusters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesGkeClusters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ffda9f16b355dd97fa49c6e21948d74c51477c5128a6a16147e5ddd9eb2433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployTargetAssociatedEntitiesGkeClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntitiesGkeClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddd27505ef275fc2461b790cfae945cd63105a1e48a66fb37086048648adadf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04d7052891ed84c5d735d55b05c53e7ccb2c9b222cbfc686aefaafec171dd032)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74acc9dc33075f087d7f0643e8eb14e414259a71e88f36bf7a188bb6d5ca1c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyUrl")
    def proxy_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyUrl"))

    @proxy_url.setter
    def proxy_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1642e5e01d001b9626a4eab8fe8c89ebf851bee5759c09bcf92ced9dd4a08a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntitiesGkeClusters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntitiesGkeClusters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntitiesGkeClusters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1577d3927cb42b405b8a15dd09fc3bb2d116d2d6aa4efff7567d49d2acbf0abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployTargetAssociatedEntitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5de02b6e198579e9b18f4c677d2f49df8ff3bb40bf4e328d610de505f9025b35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployTargetAssociatedEntitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad0eded27b315947518cac8e8fd8b7c01ee7d438eee9cb4331e3468f94a8f57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployTargetAssociatedEntitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d691a7e61fe32697b51b07fc163cb67d91d8a7ca4d194d829e62df42653c619)
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
            type_hints = typing.get_type_hints(_typecheckingstub__050b3de3e4bf162e41f57fcb77e2d325411b8ce336b197fa5bc60b74615b94ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e03c3a1e61c742d9335bbfbd95133f38d224f60e20ce9dd6f3c0fb8153051717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d21cfb60e306f21c99b48ec61fdee4d385f40fbcb717c50f287873f368e632c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployTargetAssociatedEntitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetAssociatedEntitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b5f41df9d693dc39aa7e805e6e5cecc769589436f56507086c98a311741a852)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAnthosClusters")
    def put_anthos_clusters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c220724fe9ed9f5b4fbdf54f82fffac5c14b27ea456a4390cb953abeb7b172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnthosClusters", [value]))

    @jsii.member(jsii_name="putGkeClusters")
    def put_gke_clusters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntitiesGkeClusters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae51c25d7273b5d764e62ae3722c34ceec709e31361a0a3b009e0f39113b6c85)
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
    def anthos_clusters(
        self,
    ) -> GoogleClouddeployTargetAssociatedEntitiesAnthosClustersList:
        return typing.cast(GoogleClouddeployTargetAssociatedEntitiesAnthosClustersList, jsii.get(self, "anthosClusters"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusters")
    def gke_clusters(self) -> GoogleClouddeployTargetAssociatedEntitiesGkeClustersList:
        return typing.cast(GoogleClouddeployTargetAssociatedEntitiesGkeClustersList, jsii.get(self, "gkeClusters"))

    @builtins.property
    @jsii.member(jsii_name="anthosClustersInput")
    def anthos_clusters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]]], jsii.get(self, "anthosClustersInput"))

    @builtins.property
    @jsii.member(jsii_name="entityIdInput")
    def entity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeClustersInput")
    def gke_clusters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesGkeClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesGkeClusters]]], jsii.get(self, "gkeClustersInput"))

    @builtins.property
    @jsii.member(jsii_name="entityId")
    def entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityId"))

    @entity_id.setter
    def entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dda136b128123c4ac8050cbfb31f1af0bd116f685aaa3753a3cdbd8d6a91d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73cf2c680bab5e020bfbdde15b5f74950376701b49cbf263bd84c206a33cf73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetConfig",
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
class GoogleClouddeployTargetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        anthos_cluster: typing.Optional[typing.Union[GoogleClouddeployTargetAnthosCluster, typing.Dict[builtins.str, typing.Any]]] = None,
        associated_entities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntities, typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_target: typing.Optional[typing.Union["GoogleClouddeployTargetCustomTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        deploy_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployTargetExecutionConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gke: typing.Optional[typing.Union["GoogleClouddeployTargetGke", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        multi_target: typing.Optional[typing.Union["GoogleClouddeployTargetMultiTarget", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run: typing.Optional[typing.Union["GoogleClouddeployTargetRun", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployTargetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#location GoogleClouddeployTarget#location}
        :param name: Name of the ``Target``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#name GoogleClouddeployTarget#name}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#annotations GoogleClouddeployTarget#annotations}
        :param anthos_cluster: anthos_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#anthos_cluster GoogleClouddeployTarget#anthos_cluster}
        :param associated_entities: associated_entities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#associated_entities GoogleClouddeployTarget#associated_entities}
        :param custom_target: custom_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#custom_target GoogleClouddeployTarget#custom_target}
        :param deploy_parameters: Optional. The deploy parameters to use for this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#deploy_parameters GoogleClouddeployTarget#deploy_parameters}
        :param description: Optional. Description of the ``Target``. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#description GoogleClouddeployTarget#description}
        :param execution_configs: execution_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#execution_configs GoogleClouddeployTarget#execution_configs}
        :param gke: gke block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#gke GoogleClouddeployTarget#gke}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#id GoogleClouddeployTarget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#labels GoogleClouddeployTarget#labels}
        :param multi_target: multi_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#multi_target GoogleClouddeployTarget#multi_target}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#project GoogleClouddeployTarget#project}
        :param require_approval: Optional. Whether or not the ``Target`` requires approval. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#require_approval GoogleClouddeployTarget#require_approval}
        :param run: run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#run GoogleClouddeployTarget#run}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#timeouts GoogleClouddeployTarget#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(anthos_cluster, dict):
            anthos_cluster = GoogleClouddeployTargetAnthosCluster(**anthos_cluster)
        if isinstance(custom_target, dict):
            custom_target = GoogleClouddeployTargetCustomTarget(**custom_target)
        if isinstance(gke, dict):
            gke = GoogleClouddeployTargetGke(**gke)
        if isinstance(multi_target, dict):
            multi_target = GoogleClouddeployTargetMultiTarget(**multi_target)
        if isinstance(run, dict):
            run = GoogleClouddeployTargetRun(**run)
        if isinstance(timeouts, dict):
            timeouts = GoogleClouddeployTargetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef40c304de1fd46d1b5ca5ec59e8f97fed1166c36e1ee5c5f51358148856967)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#location GoogleClouddeployTarget#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the ``Target``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#name GoogleClouddeployTarget#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#annotations GoogleClouddeployTarget#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def anthos_cluster(self) -> typing.Optional[GoogleClouddeployTargetAnthosCluster]:
        '''anthos_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#anthos_cluster GoogleClouddeployTarget#anthos_cluster}
        '''
        result = self._values.get("anthos_cluster")
        return typing.cast(typing.Optional[GoogleClouddeployTargetAnthosCluster], result)

    @builtins.property
    def associated_entities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntities]]]:
        '''associated_entities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#associated_entities GoogleClouddeployTarget#associated_entities}
        '''
        result = self._values.get("associated_entities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntities]]], result)

    @builtins.property
    def custom_target(self) -> typing.Optional["GoogleClouddeployTargetCustomTarget"]:
        '''custom_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#custom_target GoogleClouddeployTarget#custom_target}
        '''
        result = self._values.get("custom_target")
        return typing.cast(typing.Optional["GoogleClouddeployTargetCustomTarget"], result)

    @builtins.property
    def deploy_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. The deploy parameters to use for this target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#deploy_parameters GoogleClouddeployTarget#deploy_parameters}
        '''
        result = self._values.get("deploy_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the ``Target``. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#description GoogleClouddeployTarget#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetExecutionConfigs"]]]:
        '''execution_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#execution_configs GoogleClouddeployTarget#execution_configs}
        '''
        result = self._values.get("execution_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployTargetExecutionConfigs"]]], result)

    @builtins.property
    def gke(self) -> typing.Optional["GoogleClouddeployTargetGke"]:
        '''gke block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#gke GoogleClouddeployTarget#gke}
        '''
        result = self._values.get("gke")
        return typing.cast(typing.Optional["GoogleClouddeployTargetGke"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#id GoogleClouddeployTarget#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#labels GoogleClouddeployTarget#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def multi_target(self) -> typing.Optional["GoogleClouddeployTargetMultiTarget"]:
        '''multi_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#multi_target GoogleClouddeployTarget#multi_target}
        '''
        result = self._values.get("multi_target")
        return typing.cast(typing.Optional["GoogleClouddeployTargetMultiTarget"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#project GoogleClouddeployTarget#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Whether or not the ``Target`` requires approval.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#require_approval GoogleClouddeployTarget#require_approval}
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run(self) -> typing.Optional["GoogleClouddeployTargetRun"]:
        '''run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#run GoogleClouddeployTarget#run}
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional["GoogleClouddeployTargetRun"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleClouddeployTargetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#timeouts GoogleClouddeployTarget#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleClouddeployTargetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetCustomTarget",
    jsii_struct_bases=[],
    name_mapping={"custom_target_type": "customTargetType"},
)
class GoogleClouddeployTargetCustomTarget:
    def __init__(self, *, custom_target_type: builtins.str) -> None:
        '''
        :param custom_target_type: Required. The name of the CustomTargetType. Format must be ``projects/{project}/locations/{location}/customTargetTypes/{custom_target_type}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#custom_target_type GoogleClouddeployTarget#custom_target_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdffaf33f8cb4965c1f9292d86618c97e78b839abbf654a8dbdd98e3505e442)
            check_type(argname="argument custom_target_type", value=custom_target_type, expected_type=type_hints["custom_target_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_target_type": custom_target_type,
        }

    @builtins.property
    def custom_target_type(self) -> builtins.str:
        '''Required. The name of the CustomTargetType. Format must be ``projects/{project}/locations/{location}/customTargetTypes/{custom_target_type}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#custom_target_type GoogleClouddeployTarget#custom_target_type}
        '''
        result = self._values.get("custom_target_type")
        assert result is not None, "Required property 'custom_target_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetCustomTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetCustomTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetCustomTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a60231188f998e9c87fa51ea6398a9d947d46dbc7ce2e66a46bb2b598266482)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8146de4aabbde78c9f86d64700f4428b5aa0b08299d6f26de42557b739505079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTargetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleClouddeployTargetCustomTarget]:
        return typing.cast(typing.Optional[GoogleClouddeployTargetCustomTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployTargetCustomTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00ea313e5892906797410b54c9630fd5cafc8c735f8d7eb7d4ca7493f1ee155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetExecutionConfigs",
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
class GoogleClouddeployTargetExecutionConfigs:
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
        :param usages: Required. Usages when this configuration should be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#usages GoogleClouddeployTarget#usages}
        :param artifact_storage: Optional. Cloud Storage location in which to store execution outputs. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#artifact_storage GoogleClouddeployTarget#artifact_storage}
        :param execution_timeout: Optional. Execution timeout for a Cloud Build Execution. This must be between 10m and 24h in seconds format. If unspecified, a default timeout of 1h is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#execution_timeout GoogleClouddeployTarget#execution_timeout}
        :param service_account: Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#service_account GoogleClouddeployTarget#service_account}
        :param verbose: Optional. If true, additional logging will be enabled when running builds in this execution environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#verbose GoogleClouddeployTarget#verbose}
        :param worker_pool: Optional. The resource name of the ``WorkerPool``, with the format ``projects/{project}/locations/{location}/workerPools/{worker_pool}``. If this optional field is unspecified, the default Cloud Build pool will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#worker_pool GoogleClouddeployTarget#worker_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996d291abddc20925de78e4646cb3ca99f55cfdc92cccb27cbd3c8e8b663385f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#usages GoogleClouddeployTarget#usages}
        '''
        result = self._values.get("usages")
        assert result is not None, "Required property 'usages' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def artifact_storage(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Cloud Storage location in which to store execution outputs. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#artifact_storage GoogleClouddeployTarget#artifact_storage}
        '''
        result = self._values.get("artifact_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_timeout(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Execution timeout for a Cloud Build Execution. This must be between 10m and 24h in seconds format. If unspecified, a default timeout of 1h is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#execution_timeout GoogleClouddeployTarget#execution_timeout}
        '''
        result = self._values.get("execution_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#service_account GoogleClouddeployTarget#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verbose(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, additional logging will be enabled when running builds in this execution environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#verbose GoogleClouddeployTarget#verbose}
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def worker_pool(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The resource name of the ``WorkerPool``, with the format ``projects/{project}/locations/{location}/workerPools/{worker_pool}``. If this optional field is unspecified, the default Cloud Build pool will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#worker_pool GoogleClouddeployTarget#worker_pool}
        '''
        result = self._values.get("worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetExecutionConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetExecutionConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetExecutionConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a973d4cdadc20d34cd7be3bc80d4b0297d705de46df72ff9826e1217d83a0342)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployTargetExecutionConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e1a8bfbc5cf9129bf6744fef63ef11638e9472eb13f7ca79c4c83325d2161f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployTargetExecutionConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47df13d2e16f273b6d22e0c898ce46ff2d70c5792161367d2d54ceae46966f9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8548a4e92fdc273d729ed4703b2f1489d2660e758704e99f5f262ef80f3ba835)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e58df2800b29c90227583322c731c882d8bb4743840b28e9773a53b6be797de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetExecutionConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetExecutionConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetExecutionConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25e19633f54f196ce1f30b6405cfb7c1c88f02c79e37bf52490fc23fe1d60c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployTargetExecutionConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetExecutionConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8087cb91e808cd37be54689cd9da76433045c03bea4e222cb261451b96b95c8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22a79c636dc7656bedc23cfc9704da51f60c096196e292a485751a85c040abda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionTimeout")
    def execution_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionTimeout"))

    @execution_timeout.setter
    def execution_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc9ceb293af634e108dc2753d3fa65c028a896b770f012999f0709032af16d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1064c7ab519ec419e5f470415aaa8bb219dda45c2c5a21dc468e13b742f6eaf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usages")
    def usages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usages"))

    @usages.setter
    def usages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58756d4239274d4d5a3dbacfc9955c51a1843e8d8faf15cf9118f926044a994)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5996ad7d19ffa73f39443f8e948b10a865f32a01a3994250e412d76181d7655a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verbose", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerPool"))

    @worker_pool.setter
    def worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077240e7efb408d6b53f6ca5930e90f9e1cb994fe2ec0193172cb56b12c9dadf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetExecutionConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetExecutionConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetExecutionConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8dcf2306936e17cfb71453819654de5bc74e541238544a28b89ac0ffbdbc73e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetGke",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "dns_endpoint": "dnsEndpoint",
        "internal_ip": "internalIp",
        "proxy_url": "proxyUrl",
    },
)
class GoogleClouddeployTargetGke:
    def __init__(
        self,
        *,
        cluster: typing.Optional[builtins.str] = None,
        dns_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: Information specifying a GKE Cluster. Format is `projects/{project_id}/locations/{location_id}/clusters/{cluster_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#cluster GoogleClouddeployTarget#cluster}
        :param dns_endpoint: Optional. If set, the cluster will be accessed using the DNS endpoint. Note that both ``dns_endpoint`` and ``internal_ip`` cannot be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#dns_endpoint GoogleClouddeployTarget#dns_endpoint}
        :param internal_ip: Optional. If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#internal_ip GoogleClouddeployTarget#internal_ip}
        :param proxy_url: Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#proxy_url GoogleClouddeployTarget#proxy_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6893e5ecd4f94b492e7950a2ba95e32004c93e56c4a320b75234d09f6675bce)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#cluster GoogleClouddeployTarget#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If set, the cluster will be accessed using the DNS endpoint. Note that both ``dns_endpoint`` and ``internal_ip`` cannot be set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#dns_endpoint GoogleClouddeployTarget#dns_endpoint}
        '''
        result = self._values.get("dns_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def internal_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If true, ``cluster`` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when ``cluster`` is a `private GKE cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#internal_ip GoogleClouddeployTarget#internal_ip}
        '''
        result = self._values.get("internal_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''Optional. If set, used to configure a `proxy <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#proxy>`_ to the Kubernetes server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#proxy_url GoogleClouddeployTarget#proxy_url}
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetGke(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetGkeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetGkeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52a99474173d19b44c17d7af2ec717f7e7fbf000e564b81b6251ea886f60cbc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0619f14545df20dfc110b9c61ee227a60496e3052dac254c90f825605c75a4a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__230a74bb6cc0503e7ba64a2c3263c352d23dc47bb38acc4c7fc6eefe0b4093be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1fc90cd27be7cedac28e1807c39c40c3b2c0b62ef0f6b1703344d6f73b3559b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyUrl")
    def proxy_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyUrl"))

    @proxy_url.setter
    def proxy_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec65bbc2c7f82f741cadcb107cebaf0f6ad5b214c3ca97077c75e8f85100982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleClouddeployTargetGke]:
        return typing.cast(typing.Optional[GoogleClouddeployTargetGke], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployTargetGke],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33412e77c685edacf8335e83cd7ed1112e28228c7e23117c76203ecd6ca4d140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetMultiTarget",
    jsii_struct_bases=[],
    name_mapping={"target_ids": "targetIds"},
)
class GoogleClouddeployTargetMultiTarget:
    def __init__(self, *, target_ids: typing.Sequence[builtins.str]) -> None:
        '''
        :param target_ids: Required. The target_ids of this multiTarget. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#target_ids GoogleClouddeployTarget#target_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbed873550459eec7e09bebf1aa9029496d9bee0a9181e30b5a075f0a0f3dce)
            check_type(argname="argument target_ids", value=target_ids, expected_type=type_hints["target_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_ids": target_ids,
        }

    @builtins.property
    def target_ids(self) -> typing.List[builtins.str]:
        '''Required. The target_ids of this multiTarget.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#target_ids GoogleClouddeployTarget#target_ids}
        '''
        result = self._values.get("target_ids")
        assert result is not None, "Required property 'target_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetMultiTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetMultiTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetMultiTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd84c7ecb4b8a2b9ec0197cce08ceb08cdc1102eef48aa07d645164890907338)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9c41911586f293aa0f303dc0638826144ad32bded952653506b5e0f57a51bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleClouddeployTargetMultiTarget]:
        return typing.cast(typing.Optional[GoogleClouddeployTargetMultiTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployTargetMultiTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56cf8ac55d83d387ffa1ae2158813b1d6cac9717f79fdd30788afeb4d7fcb45b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetRun",
    jsii_struct_bases=[],
    name_mapping={"location": "location"},
)
class GoogleClouddeployTargetRun:
    def __init__(self, *, location: builtins.str) -> None:
        '''
        :param location: Required. The location where the Cloud Run Service should be located. Format is ``projects/{project}/locations/{location}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#location GoogleClouddeployTarget#location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f238e462498cc90ed79fe7868cf0987c40341752e6a0186c5b63d93ecbc185bc)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }

    @builtins.property
    def location(self) -> builtins.str:
        '''Required. The location where the Cloud Run Service should be located. Format is ``projects/{project}/locations/{location}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#location GoogleClouddeployTarget#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12fdac4d00268ea266276bc68b5248ef4d129ec5223543bed043cf55b35545ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__610d53179df79f4e97df3d1a7db727e50b5bf803f13120afba6b918ae5959521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleClouddeployTargetRun]:
        return typing.cast(typing.Optional[GoogleClouddeployTargetRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployTargetRun],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276bc54dccd1caa72fb23236d1042ae9ed956f09ae5a5f7e3fe9343eb2f45b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleClouddeployTargetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#create GoogleClouddeployTarget#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#delete GoogleClouddeployTarget#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#update GoogleClouddeployTarget#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96715385f9223bff1af11b5c3f4614c9a49ecfb407bfadb5aa45b8c34e481061)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#create GoogleClouddeployTarget#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#delete GoogleClouddeployTarget#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_target#update GoogleClouddeployTarget#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployTargetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployTargetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployTarget.GoogleClouddeployTargetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c11268dc97880756d12e31925a56575e04c1eaaf3e0a10114adbeb999bf972)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5616a121ae0ae6609663e347f62642fa229b7ac8724118c2739cf280ed0b434a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de522ba1ca154714408bcad3a3e020750476d12d9959c3298fba6c46e09de357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832cf31f898e7cbf96c7e85c153de09b2d9082cbfd61f6127853e662da93192f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211c7ffea653b0960746123dbfd49fa4cce39a456d04dc4cb185a11b105d61b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleClouddeployTarget",
    "GoogleClouddeployTargetAnthosCluster",
    "GoogleClouddeployTargetAnthosClusterOutputReference",
    "GoogleClouddeployTargetAssociatedEntities",
    "GoogleClouddeployTargetAssociatedEntitiesAnthosClusters",
    "GoogleClouddeployTargetAssociatedEntitiesAnthosClustersList",
    "GoogleClouddeployTargetAssociatedEntitiesAnthosClustersOutputReference",
    "GoogleClouddeployTargetAssociatedEntitiesGkeClusters",
    "GoogleClouddeployTargetAssociatedEntitiesGkeClustersList",
    "GoogleClouddeployTargetAssociatedEntitiesGkeClustersOutputReference",
    "GoogleClouddeployTargetAssociatedEntitiesList",
    "GoogleClouddeployTargetAssociatedEntitiesOutputReference",
    "GoogleClouddeployTargetConfig",
    "GoogleClouddeployTargetCustomTarget",
    "GoogleClouddeployTargetCustomTargetOutputReference",
    "GoogleClouddeployTargetExecutionConfigs",
    "GoogleClouddeployTargetExecutionConfigsList",
    "GoogleClouddeployTargetExecutionConfigsOutputReference",
    "GoogleClouddeployTargetGke",
    "GoogleClouddeployTargetGkeOutputReference",
    "GoogleClouddeployTargetMultiTarget",
    "GoogleClouddeployTargetMultiTargetOutputReference",
    "GoogleClouddeployTargetRun",
    "GoogleClouddeployTargetRunOutputReference",
    "GoogleClouddeployTargetTimeouts",
    "GoogleClouddeployTargetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c83a80fab5cbbb1d1a8234f82ed985400cf205bb3ca8388a5c2056e5ed2a786c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    anthos_cluster: typing.Optional[typing.Union[GoogleClouddeployTargetAnthosCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    associated_entities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_target: typing.Optional[typing.Union[GoogleClouddeployTargetCustomTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    deploy_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetExecutionConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gke: typing.Optional[typing.Union[GoogleClouddeployTargetGke, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    multi_target: typing.Optional[typing.Union[GoogleClouddeployTargetMultiTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run: typing.Optional[typing.Union[GoogleClouddeployTargetRun, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployTargetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__91e1aa1a1721ab7e9c1d1cba362cc9faa1cc66eb394fe0b0eaa5fadc042b248b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3701f4a39242470dc62a440ace5e8a3e93381bcba09c05c8d4b11a325e1704(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8289836d490025823f88a406b669bcb010c96ea2d45644364188bc70627fe13(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetExecutionConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7df951be790ab4ab2587b19e16c4a8c6c9af2aba51308609575825cd5aecf1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b88ec23314ca124980c91af9ea6a9febe107fda5b1608e995efd241bad097c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65d11c6f338c66b4b4b25ea796f25827255503cbee4ad4e966465b368831162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bcf966ebf8bea35b56f079db8fe4bf2bc44c3f9ffed2eaeb7c7cda5e5bce83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ace9c194377f9a257a098b0f6b7c869f4ed70491ad3dc71e75e1f6841ff476e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b82a3e283973bdaf8743d7eb07e4ec1756068d33a88071f17a65f75b3e2eb5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9563b021e4ae2da4a99e954dd12e35f7ddd9886033f210cfe87a90a74b1a5da1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8dc22a9b95bc0fd5826f62a198a17449c543714fa939faeef075051eb8243e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0899b0cbf7269ab14ed2390b3ed679b015395f791c4720cb185bd24c1a731c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf1076ade2a45449c15e564efb6c5b96b3ef24397333cb775ac9159444faa1f(
    *,
    membership: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3b7a09afa8b1245a5138116cd4365a161b067b2d18770e21307e0c2c79f4a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93076cc9f8529fabee6c08837eeafd810fe3859b2d65747abf8783042f5fd6bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6f57ebf599a8b9ecff19d4fbd8535ae30cdd7f4c943d0049466a82f9efc35b(
    value: typing.Optional[GoogleClouddeployTargetAnthosCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27aeaa934f224ecca153fbd89b9f912fa4b644c4c6c719882610c6a2c6f9726(
    *,
    entity_id: builtins.str,
    anthos_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gke_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntitiesGkeClusters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95387bb306e6c9d0b1372e2623cd0594e7d58d14c7f4a415bb1939a87991a69b(
    *,
    membership: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c89e03d3c8b1f18b1b0be6f6992cbd6996fbdf09a5200e25e8057f546bec494(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c7315256f60886405242123357ec89762ee19668ed73ca67ec47cd161c132a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c772a806a4dce3b27d7359fda5ac5c410e7c075a20fd3f90baa7fa4eebad8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b376b3792ec822f29b17a4f046432ba883d8036797686d87bb750b593dbb388(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248f9fd11770110d1cbb6d9b03bdfee38786bb3c18b73d8fadc487438a48c9e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e43788b8c4a3fb7eba6d6f22861a2339eed68ab35451c6ee2853e2c32155e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5404447e3e03d6a14d3ac4bcb1198a68d707496b90db74255d3bf9d69a754d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c336f6d9c983f4a760042b9a07139db6496c93227b12eee82f89f8d459e002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12c8b3cdd2c73360113f9d27a1f8c5b0262ac2b1cf38721917a9df770978305(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntitiesAnthosClusters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b570f90dd3b597b2014f47be92a9bf2ee7666477f0dfb424709a43632c00edc4(
    *,
    cluster: typing.Optional[builtins.str] = None,
    internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proxy_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eaa4463c6e5dc8b0739c2ee73342aab27a65a3dfce1a2bb5186d77b3327076b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1354bc210f81bc437bd9c7894205d0d02f8c07d97f4b80e51668ac0cc3a9614(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fc4c5c86d39f80d05e44f1303d5417713a2cdb63ffe6a04e14526d8d16120a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29dc50909659e319b8bd1662d4b2fe4b8debe53c904abe86d5fe0b567acd7d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecfb4112e03cd8d74ca5ef77b6f3fd4762cf3a521120c5a341ef35110a80d83(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ffda9f16b355dd97fa49c6e21948d74c51477c5128a6a16147e5ddd9eb2433(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntitiesGkeClusters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd27505ef275fc2461b790cfae945cd63105a1e48a66fb37086048648adadf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d7052891ed84c5d735d55b05c53e7ccb2c9b222cbfc686aefaafec171dd032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74acc9dc33075f087d7f0643e8eb14e414259a71e88f36bf7a188bb6d5ca1c8b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1642e5e01d001b9626a4eab8fe8c89ebf851bee5759c09bcf92ced9dd4a08a11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1577d3927cb42b405b8a15dd09fc3bb2d116d2d6aa4efff7567d49d2acbf0abe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntitiesGkeClusters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de02b6e198579e9b18f4c677d2f49df8ff3bb40bf4e328d610de505f9025b35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad0eded27b315947518cac8e8fd8b7c01ee7d438eee9cb4331e3468f94a8f57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d691a7e61fe32697b51b07fc163cb67d91d8a7ca4d194d829e62df42653c619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050b3de3e4bf162e41f57fcb77e2d325411b8ce336b197fa5bc60b74615b94ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03c3a1e61c742d9335bbfbd95133f38d224f60e20ce9dd6f3c0fb8153051717(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d21cfb60e306f21c99b48ec61fdee4d385f40fbcb717c50f287873f368e632c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetAssociatedEntities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5f41df9d693dc39aa7e805e6e5cecc769589436f56507086c98a311741a852(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c220724fe9ed9f5b4fbdf54f82fffac5c14b27ea456a4390cb953abeb7b172(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntitiesAnthosClusters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae51c25d7273b5d764e62ae3722c34ceec709e31361a0a3b009e0f39113b6c85(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntitiesGkeClusters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dda136b128123c4ac8050cbfb31f1af0bd116f685aaa3753a3cdbd8d6a91d74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73cf2c680bab5e020bfbdde15b5f74950376701b49cbf263bd84c206a33cf73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetAssociatedEntities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef40c304de1fd46d1b5ca5ec59e8f97fed1166c36e1ee5c5f51358148856967(
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
    anthos_cluster: typing.Optional[typing.Union[GoogleClouddeployTargetAnthosCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    associated_entities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetAssociatedEntities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_target: typing.Optional[typing.Union[GoogleClouddeployTargetCustomTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    deploy_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployTargetExecutionConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gke: typing.Optional[typing.Union[GoogleClouddeployTargetGke, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    multi_target: typing.Optional[typing.Union[GoogleClouddeployTargetMultiTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    require_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run: typing.Optional[typing.Union[GoogleClouddeployTargetRun, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployTargetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdffaf33f8cb4965c1f9292d86618c97e78b839abbf654a8dbdd98e3505e442(
    *,
    custom_target_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a60231188f998e9c87fa51ea6398a9d947d46dbc7ce2e66a46bb2b598266482(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8146de4aabbde78c9f86d64700f4428b5aa0b08299d6f26de42557b739505079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00ea313e5892906797410b54c9630fd5cafc8c735f8d7eb7d4ca7493f1ee155(
    value: typing.Optional[GoogleClouddeployTargetCustomTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996d291abddc20925de78e4646cb3ca99f55cfdc92cccb27cbd3c8e8b663385f(
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

def _typecheckingstub__a973d4cdadc20d34cd7be3bc80d4b0297d705de46df72ff9826e1217d83a0342(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e1a8bfbc5cf9129bf6744fef63ef11638e9472eb13f7ca79c4c83325d2161f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47df13d2e16f273b6d22e0c898ce46ff2d70c5792161367d2d54ceae46966f9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8548a4e92fdc273d729ed4703b2f1489d2660e758704e99f5f262ef80f3ba835(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e58df2800b29c90227583322c731c882d8bb4743840b28e9773a53b6be797de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25e19633f54f196ce1f30b6405cfb7c1c88f02c79e37bf52490fc23fe1d60c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployTargetExecutionConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8087cb91e808cd37be54689cd9da76433045c03bea4e222cb261451b96b95c8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a79c636dc7656bedc23cfc9704da51f60c096196e292a485751a85c040abda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc9ceb293af634e108dc2753d3fa65c028a896b770f012999f0709032af16d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1064c7ab519ec419e5f470415aaa8bb219dda45c2c5a21dc468e13b742f6eaf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58756d4239274d4d5a3dbacfc9955c51a1843e8d8faf15cf9118f926044a994(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5996ad7d19ffa73f39443f8e948b10a865f32a01a3994250e412d76181d7655a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077240e7efb408d6b53f6ca5930e90f9e1cb994fe2ec0193172cb56b12c9dadf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8dcf2306936e17cfb71453819654de5bc74e541238544a28b89ac0ffbdbc73e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetExecutionConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6893e5ecd4f94b492e7950a2ba95e32004c93e56c4a320b75234d09f6675bce(
    *,
    cluster: typing.Optional[builtins.str] = None,
    dns_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    internal_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proxy_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a99474173d19b44c17d7af2ec717f7e7fbf000e564b81b6251ea886f60cbc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0619f14545df20dfc110b9c61ee227a60496e3052dac254c90f825605c75a4a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230a74bb6cc0503e7ba64a2c3263c352d23dc47bb38acc4c7fc6eefe0b4093be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fc90cd27be7cedac28e1807c39c40c3b2c0b62ef0f6b1703344d6f73b3559b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec65bbc2c7f82f741cadcb107cebaf0f6ad5b214c3ca97077c75e8f85100982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33412e77c685edacf8335e83cd7ed1112e28228c7e23117c76203ecd6ca4d140(
    value: typing.Optional[GoogleClouddeployTargetGke],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbed873550459eec7e09bebf1aa9029496d9bee0a9181e30b5a075f0a0f3dce(
    *,
    target_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd84c7ecb4b8a2b9ec0197cce08ceb08cdc1102eef48aa07d645164890907338(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c41911586f293aa0f303dc0638826144ad32bded952653506b5e0f57a51bba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56cf8ac55d83d387ffa1ae2158813b1d6cac9717f79fdd30788afeb4d7fcb45b(
    value: typing.Optional[GoogleClouddeployTargetMultiTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f238e462498cc90ed79fe7868cf0987c40341752e6a0186c5b63d93ecbc185bc(
    *,
    location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fdac4d00268ea266276bc68b5248ef4d129ec5223543bed043cf55b35545ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610d53179df79f4e97df3d1a7db727e50b5bf803f13120afba6b918ae5959521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276bc54dccd1caa72fb23236d1042ae9ed956f09ae5a5f7e3fe9343eb2f45b28(
    value: typing.Optional[GoogleClouddeployTargetRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96715385f9223bff1af11b5c3f4614c9a49ecfb407bfadb5aa45b8c34e481061(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c11268dc97880756d12e31925a56575e04c1eaaf3e0a10114adbeb999bf972(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5616a121ae0ae6609663e347f62642fa229b7ac8724118c2739cf280ed0b434a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de522ba1ca154714408bcad3a3e020750476d12d9959c3298fba6c46e09de357(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832cf31f898e7cbf96c7e85c153de09b2d9082cbfd61f6127853e662da93192f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211c7ffea653b0960746123dbfd49fa4cce39a456d04dc4cb185a11b105d61b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployTargetTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
