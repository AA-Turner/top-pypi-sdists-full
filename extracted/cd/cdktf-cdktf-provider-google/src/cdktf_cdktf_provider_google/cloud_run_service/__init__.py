r'''
# `google_cloud_run_service`

Refer to the Terraform Registry for docs: [`google_cloud_run_service`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service).
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


class CloudRunService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service google_cloud_run_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        autogenerate_revision_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["CloudRunServiceMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        template: typing.Optional[typing.Union["CloudRunServiceTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudRunServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTraffic", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service google_cloud_run_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the cloud run instance. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#location CloudRunService#location}
        :param name: Name must be unique within a Google Cloud project and region. Is required when creating resources. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param autogenerate_revision_name: If set to 'true', the revision name (template.metadata.name) will be omitted and autogenerated by Cloud Run. This cannot be set to 'true' while 'template.metadata.name' is also set. (For legacy support, if 'template.metadata.name' is unset in state while this field is set to false, the revision name will still autogenerate.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#autogenerate_revision_name CloudRunService#autogenerate_revision_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#id CloudRunService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#metadata CloudRunService#metadata}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#project CloudRunService#project}.
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#template CloudRunService#template}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeouts CloudRunService#timeouts}
        :param traffic: traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#traffic CloudRunService#traffic}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae7f44c196d582ff867d90e3e725809d7c7414de600e93ea3686128ad3a50c8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudRunServiceConfig(
            location=location,
            name=name,
            autogenerate_revision_name=autogenerate_revision_name,
            id=id,
            metadata=metadata,
            project=project,
            template=template,
            timeouts=timeouts,
            traffic=traffic,
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
        '''Generates CDKTF code for importing a CloudRunService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudRunService to import.
        :param import_from_id: The id of the existing CloudRunService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudRunService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1dc21af59308423bb3755a2284a6bb78369b37afcfae94cb96fe0a73b999c1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations **Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation keys to configure features on a Service: - 'run.googleapis.com/binary-authorization-breakglass' sets the `Binary Authorization breakglass <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--breakglass>`_. - 'run.googleapis.com/binary-authorization' sets the `Binary Authorization <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--binary-authorization>`_. - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API. - 'run.googleapis.com/custom-audiences' sets the `custom audiences <https://cloud.google.com/sdk/gcloud/reference/alpha/run/deploy#--add-custom-audiences>`_ that can be used in the audience field of ID token for authenticated requests. - 'run.googleapis.com/description' sets a user defined description for the Service. - 'run.googleapis.com/ingress' sets the `ingress settings <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--ingress>`_ for the Service. For example, '"run.googleapis.com/ingress" = "all"'. - 'run.googleapis.com/launch-stage' sets the `launch stage <https://cloud.google.com/run/docs/troubleshooting#launch-stage-validation>`_ when a preview feature is used. For example, '"run.googleapis.com/launch-stage": "BETA"' - 'run.googleapis.com/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min>`_ of the Service. - 'run.googleapis.com/scalingMode' sets the type of scaling mode for the service. The supported values for scaling mode are "manual" and "automatic". If not provided, it defaults to "automatic". - 'run.googleapis.com/manualInstanceCount' sets the total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#annotations CloudRunService#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and routes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#labels CloudRunService#labels}
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#namespace CloudRunService#namespace}
        '''
        value = CloudRunServiceMetadata(
            annotations=annotations, labels=labels, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        metadata: typing.Optional[typing.Union["CloudRunServiceTemplateMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        spec: typing.Optional[typing.Union["CloudRunServiceTemplateSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#metadata CloudRunService#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#spec CloudRunService#spec}
        '''
        value = CloudRunServiceTemplate(metadata=metadata, spec=spec)

        return typing.cast(None, jsii.invoke(self, "putTemplate", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#create CloudRunService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#delete CloudRunService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#update CloudRunService#update}.
        '''
        value = CloudRunServiceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTraffic")
    def put_traffic(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTraffic", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dea454bc2f330287360cd25cfc6eddc032ef80312cab392619f93f2746545f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTraffic", [value]))

    @jsii.member(jsii_name="resetAutogenerateRevisionName")
    def reset_autogenerate_revision_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutogenerateRevisionName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTemplate")
    def reset_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplate", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTraffic")
    def reset_traffic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraffic", []))

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
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "CloudRunServiceMetadataOutputReference":
        return typing.cast("CloudRunServiceMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "CloudRunServiceStatusList":
        return typing.cast("CloudRunServiceStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "CloudRunServiceTemplateOutputReference":
        return typing.cast("CloudRunServiceTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudRunServiceTimeoutsOutputReference":
        return typing.cast("CloudRunServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="traffic")
    def traffic(self) -> "CloudRunServiceTrafficList":
        return typing.cast("CloudRunServiceTrafficList", jsii.get(self, "traffic"))

    @builtins.property
    @jsii.member(jsii_name="autogenerateRevisionNameInput")
    def autogenerate_revision_name_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autogenerateRevisionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["CloudRunServiceMetadata"]:
        return typing.cast(typing.Optional["CloudRunServiceMetadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["CloudRunServiceTemplate"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudRunServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudRunServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficInput")
    def traffic_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTraffic"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTraffic"]]], jsii.get(self, "trafficInput"))

    @builtins.property
    @jsii.member(jsii_name="autogenerateRevisionName")
    def autogenerate_revision_name(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autogenerateRevisionName"))

    @autogenerate_revision_name.setter
    def autogenerate_revision_name(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f642ed35b9d19937df2832584471493620d3b6f90ae9f5fa013c956d70c8e5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autogenerateRevisionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47e604eaa020c95864a5eeb431eec687b6d27d7d6d4feabb2c3e30a02d755db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4004ea2ab9cbd1d79eea8edb0b1e03c710aefd762b1e88a052dd4d472e0a52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d761526537f908a49ce279db8038e1270febfec15ca865bf3c533b1873adc303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cac4186e06590708dc151bf47b064d94369d6bb90ef99e175fa7919bc4cef91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceConfig",
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
        "autogenerate_revision_name": "autogenerateRevisionName",
        "id": "id",
        "metadata": "metadata",
        "project": "project",
        "template": "template",
        "timeouts": "timeouts",
        "traffic": "traffic",
    },
)
class CloudRunServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autogenerate_revision_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["CloudRunServiceMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        template: typing.Optional[typing.Union["CloudRunServiceTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudRunServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTraffic", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the cloud run instance. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#location CloudRunService#location}
        :param name: Name must be unique within a Google Cloud project and region. Is required when creating resources. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param autogenerate_revision_name: If set to 'true', the revision name (template.metadata.name) will be omitted and autogenerated by Cloud Run. This cannot be set to 'true' while 'template.metadata.name' is also set. (For legacy support, if 'template.metadata.name' is unset in state while this field is set to false, the revision name will still autogenerate.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#autogenerate_revision_name CloudRunService#autogenerate_revision_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#id CloudRunService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#metadata CloudRunService#metadata}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#project CloudRunService#project}.
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#template CloudRunService#template}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeouts CloudRunService#timeouts}
        :param traffic: traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#traffic CloudRunService#traffic}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = CloudRunServiceMetadata(**metadata)
        if isinstance(template, dict):
            template = CloudRunServiceTemplate(**template)
        if isinstance(timeouts, dict):
            timeouts = CloudRunServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a3fabddea5d800abd6a935a28df7243edd8a33f009ad8bc8d20de8a0a75185)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument autogenerate_revision_name", value=autogenerate_revision_name, expected_type=type_hints["autogenerate_revision_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument traffic", value=traffic, expected_type=type_hints["traffic"])
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
        if autogenerate_revision_name is not None:
            self._values["autogenerate_revision_name"] = autogenerate_revision_name
        if id is not None:
            self._values["id"] = id
        if metadata is not None:
            self._values["metadata"] = metadata
        if project is not None:
            self._values["project"] = project
        if template is not None:
            self._values["template"] = template
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if traffic is not None:
            self._values["traffic"] = traffic

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
        '''The location of the cloud run instance. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#location CloudRunService#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name must be unique within a Google Cloud project and region.

        Is required when creating resources. Name is primarily intended
        for creation idempotence and configuration definition. Cannot be updated.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autogenerate_revision_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the revision name (template.metadata.name) will be omitted and autogenerated by Cloud Run. This cannot be set to 'true' while 'template.metadata.name' is also set. (For legacy support, if 'template.metadata.name' is unset in state while this field is set to false, the revision name will still autogenerate.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#autogenerate_revision_name CloudRunService#autogenerate_revision_name}
        '''
        result = self._values.get("autogenerate_revision_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#id CloudRunService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional["CloudRunServiceMetadata"]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#metadata CloudRunService#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["CloudRunServiceMetadata"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#project CloudRunService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional["CloudRunServiceTemplate"]:
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#template CloudRunService#template}
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional["CloudRunServiceTemplate"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudRunServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeouts CloudRunService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudRunServiceTimeouts"], result)

    @builtins.property
    def traffic(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTraffic"]]]:
        '''traffic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#traffic CloudRunService#traffic}
        '''
        result = self._values.get("traffic")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTraffic"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "labels": "labels",
        "namespace": "namespace",
    },
)
class CloudRunServiceMetadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations **Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation keys to configure features on a Service: - 'run.googleapis.com/binary-authorization-breakglass' sets the `Binary Authorization breakglass <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--breakglass>`_. - 'run.googleapis.com/binary-authorization' sets the `Binary Authorization <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--binary-authorization>`_. - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API. - 'run.googleapis.com/custom-audiences' sets the `custom audiences <https://cloud.google.com/sdk/gcloud/reference/alpha/run/deploy#--add-custom-audiences>`_ that can be used in the audience field of ID token for authenticated requests. - 'run.googleapis.com/description' sets a user defined description for the Service. - 'run.googleapis.com/ingress' sets the `ingress settings <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--ingress>`_ for the Service. For example, '"run.googleapis.com/ingress" = "all"'. - 'run.googleapis.com/launch-stage' sets the `launch stage <https://cloud.google.com/run/docs/troubleshooting#launch-stage-validation>`_ when a preview feature is used. For example, '"run.googleapis.com/launch-stage": "BETA"' - 'run.googleapis.com/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min>`_ of the Service. - 'run.googleapis.com/scalingMode' sets the type of scaling mode for the service. The supported values for scaling mode are "manual" and "automatic". If not provided, it defaults to "automatic". - 'run.googleapis.com/manualInstanceCount' sets the total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#annotations CloudRunService#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and routes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#labels CloudRunService#labels}
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#namespace CloudRunService#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b04bcb078cfb7f54797b5371324d0ab3d7dcec34a978ba547cc40f4325a2a81)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata.

        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations

        **Note**: The Cloud Run API may add additional annotations that were not provided in your config.
        If terraform plan shows a diff where a server-side annotation is added, you can add it to your config
        or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field.

        Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation
        keys to configure features on a Service:

        - 'run.googleapis.com/binary-authorization-breakglass' sets the `Binary Authorization breakglass <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--breakglass>`_.
        - 'run.googleapis.com/binary-authorization' sets the `Binary Authorization <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--binary-authorization>`_.
        - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API.
        - 'run.googleapis.com/custom-audiences' sets the `custom audiences <https://cloud.google.com/sdk/gcloud/reference/alpha/run/deploy#--add-custom-audiences>`_
          that can be used in the audience field of ID token for authenticated requests.
        - 'run.googleapis.com/description' sets a user defined description for the Service.
        - 'run.googleapis.com/ingress' sets the `ingress settings <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--ingress>`_
          for the Service. For example, '"run.googleapis.com/ingress" = "all"'.
        - 'run.googleapis.com/launch-stage' sets the `launch stage <https://cloud.google.com/run/docs/troubleshooting#launch-stage-validation>`_
          when a preview feature is used. For example, '"run.googleapis.com/launch-stage": "BETA"'
        - 'run.googleapis.com/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min>`_ of the Service.
        - 'run.googleapis.com/scalingMode' sets the type of scaling mode for the service. The supported values for scaling mode are "manual" and "automatic". If not provided, it defaults to "automatic".
        - 'run.googleapis.com/manualInstanceCount' sets the total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#annotations CloudRunService#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) objects.

        May match selectors of replication controllers
        and routes.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#labels CloudRunService#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''In Cloud Run the namespace must be equal to either the project ID or project number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#namespace CloudRunService#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6545f54fc24c3b3a3cb6de8288f7bda846906d43cb6a0a5fb00b79e98a78f90b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="resourceVersion")
    def resource_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceVersion"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de2504a154992caaf0d6dc044fb9fe56052e0096d0a2f0ec0415aec667adca24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a33bb17c61834bfabcf9fb6afdd71840c6cba2b78d93ab995466e0b23b80be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc79d97c25e7551a9c3dab87ae24240edf9a0947505f4ce618793e7fcba0e501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceMetadata]:
        return typing.cast(typing.Optional[CloudRunServiceMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudRunServiceMetadata]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ffdf428b470ca2493f35ca04b460e8b21ba0e01a0a8def25a9fa6b43ce25e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunServiceStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunServiceStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fbc4bdf0098f364e61cdb7f6c599f2b6971aac8a2f6359e82963192e95a4ef5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a80bc90b9b0b1f3327d3bcc180d315793c49b3d0094ad4073d25f2ed1ddf8c74)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b97ce5c9352d8c69da06bf55c319d5cf1cca6fdbb6388da838957c15420a2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90e0c813acfc218b4f0ff0d8602bc4b8b7378fb2a2215bed187180f02f3ea5b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3770913764d64bb9dbd9f63dccd25e18ed520fdbcdf97a10cdfd06320bc1ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__998bb5f74672ccf4fd5d4e591cd8409831bd77a11d3d35f087f4e126ae10c1b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceStatusConditions]:
        return typing.cast(typing.Optional[CloudRunServiceStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2247cacb7087be7eacfd271be485d9b9a66e2f294b349a61ee2df15c5235ed12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cde9a136fa6d92298c4200206e90554e2be9ee894964f72624146d4c2941996)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudRunServiceStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b708560dde61e0f06529f6a264129ec333c157ff24e1bdc843673f7d207718aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c057a49efda62d5a46bd3a5630c10a57a86d3f632104fe4460fbdf4dc1276811)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eb966cb876964775091f82e663d10f709c2ac122fcd8b5f14464ffc2a000dc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0984ef65af89f3cb6b0f77899b5ec1900fa8f27d003d19cf1fdba0d2c545e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f930654bdefbfde4d9915daf4b3c8afcf18424f7813845c6756c38e0f83fd19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> CloudRunServiceStatusConditionsList:
        return typing.cast(CloudRunServiceStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="latestCreatedRevisionName")
    def latest_created_revision_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestCreatedRevisionName"))

    @builtins.property
    @jsii.member(jsii_name="latestReadyRevisionName")
    def latest_ready_revision_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestReadyRevisionName"))

    @builtins.property
    @jsii.member(jsii_name="observedGeneration")
    def observed_generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "observedGeneration"))

    @builtins.property
    @jsii.member(jsii_name="traffic")
    def traffic(self) -> "CloudRunServiceStatusTrafficList":
        return typing.cast("CloudRunServiceStatusTrafficList", jsii.get(self, "traffic"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceStatus]:
        return typing.cast(typing.Optional[CloudRunServiceStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudRunServiceStatus]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ec8528c3c28ec5f40755bf419bb6e1c01cfd35368c2de7db7f3c4f10398c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatusTraffic",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunServiceStatusTraffic:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceStatusTraffic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceStatusTrafficList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatusTrafficList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33ab4962f8e71abfc4ed060672ae98360bca12f0ed69555ff76689a4057f67ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudRunServiceStatusTrafficOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64dd5a69de837ab89b28f911c7e285bab05ecaa58f47eaed76e4cbcf516157f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceStatusTrafficOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e348c816476e0fde7bfa9d468f33d97e778498a958e645f202be82e46bb48f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc9ee2804d73a3b6582419e12e0ec27916e83f0c9762edf257b8c7481f299e8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1d32d12ad864763759a1c82ebe64b1285f794f9aafbd00e2971c079a58b0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceStatusTrafficOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceStatusTrafficOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d5c3aa7a5ecaf72f77c0fb1688cc0114a78d8d4f255871729253ed42d8b4a80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="latestRevision")
    def latest_revision(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "latestRevision"))

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @builtins.property
    @jsii.member(jsii_name="revisionName")
    def revision_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionName"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceStatusTraffic]:
        return typing.cast(typing.Optional[CloudRunServiceStatusTraffic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceStatusTraffic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d78c9b77199a2929bdeb18b9adfcc9d47f8f3ed8545758444438920f0fe5360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplate",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata", "spec": "spec"},
)
class CloudRunServiceTemplate:
    def __init__(
        self,
        *,
        metadata: typing.Optional[typing.Union["CloudRunServiceTemplateMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        spec: typing.Optional[typing.Union["CloudRunServiceTemplateSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#metadata CloudRunService#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#spec CloudRunService#spec}
        '''
        if isinstance(metadata, dict):
            metadata = CloudRunServiceTemplateMetadata(**metadata)
        if isinstance(spec, dict):
            spec = CloudRunServiceTemplateSpec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4ec5e736d99c55dd0328f6b0150776740f1c55d1e392c2a5408205b781ab82)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata
        if spec is not None:
            self._values["spec"] = spec

    @builtins.property
    def metadata(self) -> typing.Optional["CloudRunServiceTemplateMetadata"]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#metadata CloudRunService#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["CloudRunServiceTemplateMetadata"], result)

    @builtins.property
    def spec(self) -> typing.Optional["CloudRunServiceTemplateSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#spec CloudRunService#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class CloudRunServiceTemplateMetadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations **Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation keys to configure features on a Revision template: - 'autoscaling.knative.dev/maxScale' sets the `maximum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--max-instances>`_ of the Revision to run. - 'autoscaling.knative.dev/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min-instances>`_ of the Revision to run. - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API. - 'run.googleapis.com/cloudsql-instances' sets the `Cloud SQL instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--add-cloudsql-instances>`_ the Revision connects to. - 'run.googleapis.com/cpu-throttling' sets whether to throttle the CPU when the container is not actively serving requests. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-throttling. - 'run.googleapis.com/encryption-key-shutdown-hours' sets the number of hours to wait before an automatic shutdown server after CMEK key revocation is detected. - 'run.googleapis.com/encryption-key' sets the `CMEK key <https://cloud.google.com/run/docs/securing/using-cmek>`_ reference to encrypt the container with. - 'run.googleapis.com/execution-environment' sets the `execution environment <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--execution-environment>`_ where the application will run. - 'run.googleapis.com/post-key-revocation-action-type' sets the `action type <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--post-key-revocation-action-type>`_ after CMEK key revocation. - 'run.googleapis.com/secrets' sets a list of key-value pairs to set as `secrets <https://cloud.google.com/run/docs/configuring/secrets#yaml>`_. - 'run.googleapis.com/sessionAffinity' sets whether to enable `session affinity <https://cloud.google.com/sdk/gcloud/reference/beta/run/deploy#--%5Bno-%5Dsession-affinity>`_ for connections to the Revision. - 'run.googleapis.com/startup-cpu-boost' sets whether to allocate extra CPU to containers on startup. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-boost. - 'run.googleapis.com/network-interfaces' sets `Direct VPC egress <https://cloud.google.com/run/docs/configuring/vpc-direct-vpc#yaml>`_ for the Revision. - 'run.googleapis.com/vpc-access-connector' sets a `VPC connector <https://cloud.google.com/run/docs/configuring/connecting-vpc#terraform_1>`_ for the Revision. - 'run.googleapis.com/vpc-access-egress' sets the outbound traffic to send through the VPC connector for this resource. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--vpc-egress. - 'run.googleapis.com/gpu-zonal-redundancy-disabled' sets `GPU zonal redundancy <https://cloud.google.com/run/docs/configuring/services/gpu-zonal-redundancy>`_ for the Revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#annotations CloudRunService#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#labels CloudRunService#labels}
        :param name: Name must be unique within a Google Cloud project and region. Is required when creating resources. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. It will default to the resource's project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#namespace CloudRunService#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f834bde54df86b749730414799d969dc329c57fb1684e38d3e1637cea370100)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata.

        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations

        **Note**: The Cloud Run API may add additional annotations that were not provided in your config.
        If terraform plan shows a diff where a server-side annotation is added, you can add it to your config
        or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field.

        Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation
        keys to configure features on a Revision template:

        - 'autoscaling.knative.dev/maxScale' sets the `maximum number of container
          instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--max-instances>`_ of the Revision to run.
        - 'autoscaling.knative.dev/minScale' sets the `minimum number of container
          instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min-instances>`_ of the Revision to run.
        - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API.
        - 'run.googleapis.com/cloudsql-instances' sets the `Cloud SQL
          instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--add-cloudsql-instances>`_ the Revision connects to.
        - 'run.googleapis.com/cpu-throttling' sets whether to throttle the CPU when the container is not actively serving
          requests. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-throttling.
        - 'run.googleapis.com/encryption-key-shutdown-hours' sets the number of hours to wait before an automatic shutdown
          server after CMEK key revocation is detected.
        - 'run.googleapis.com/encryption-key' sets the `CMEK key <https://cloud.google.com/run/docs/securing/using-cmek>`_
          reference to encrypt the container with.
        - 'run.googleapis.com/execution-environment' sets the `execution
          environment <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--execution-environment>`_
          where the application will run.
        - 'run.googleapis.com/post-key-revocation-action-type' sets the
          `action type <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--post-key-revocation-action-type>`_
          after CMEK key revocation.
        - 'run.googleapis.com/secrets' sets a list of key-value pairs to set as
          `secrets <https://cloud.google.com/run/docs/configuring/secrets#yaml>`_.
        - 'run.googleapis.com/sessionAffinity' sets whether to enable
          `session affinity <https://cloud.google.com/sdk/gcloud/reference/beta/run/deploy#--%5Bno-%5Dsession-affinity>`_
          for connections to the Revision.
        - 'run.googleapis.com/startup-cpu-boost' sets whether to allocate extra CPU to containers on startup.
          See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-boost.
        - 'run.googleapis.com/network-interfaces' sets `Direct VPC egress <https://cloud.google.com/run/docs/configuring/vpc-direct-vpc#yaml>`_
          for the Revision.
        - 'run.googleapis.com/vpc-access-connector' sets a `VPC connector <https://cloud.google.com/run/docs/configuring/connecting-vpc#terraform_1>`_
          for the Revision.
        - 'run.googleapis.com/vpc-access-egress' sets the outbound traffic to send through the VPC connector for this resource.
          See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--vpc-egress.
        - 'run.googleapis.com/gpu-zonal-redundancy-disabled' sets
          `GPU zonal redundancy <https://cloud.google.com/run/docs/configuring/services/gpu-zonal-redundancy>`_ for the Revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#annotations CloudRunService#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#labels CloudRunService#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name must be unique within a Google Cloud project and region.

        Is required when creating resources. Name is primarily intended
        for creation idempotence and configuration definition. Cannot be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''In Cloud Run the namespace must be equal to either the project ID or project number.

        It will default to the resource's project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#namespace CloudRunService#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac95393d10eada96576bb66fae9bc3fc6c0604c3d240d5f1750d3f211a2973a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="resourceVersion")
    def resource_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceVersion"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

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
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067f2ede065640e6548242fcfc6db2e13be87034a4e19fc845c5256fb3c64339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea1a896cbce4892c721dfdbddc02210d66800cb295f1eb2a440299b25f77bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9e43e6adc550c3a2df7bfabed81743ff64676067b6821da014938448298081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01bb11e4931e0338a2a3b441235e27a9fc068daf3f91e65880dfcf20f3255ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceTemplateMetadata]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da15b66007e3383d8cd69d932fddfe536baa9f7ad347aa34fdcf90792e86b93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f10463316140bb78e036e9cf8fd281b7b9ec9bdc7ee265c1241b5d091b6c687b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations **Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation keys to configure features on a Revision template: - 'autoscaling.knative.dev/maxScale' sets the `maximum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--max-instances>`_ of the Revision to run. - 'autoscaling.knative.dev/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min-instances>`_ of the Revision to run. - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API. - 'run.googleapis.com/cloudsql-instances' sets the `Cloud SQL instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--add-cloudsql-instances>`_ the Revision connects to. - 'run.googleapis.com/cpu-throttling' sets whether to throttle the CPU when the container is not actively serving requests. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-throttling. - 'run.googleapis.com/encryption-key-shutdown-hours' sets the number of hours to wait before an automatic shutdown server after CMEK key revocation is detected. - 'run.googleapis.com/encryption-key' sets the `CMEK key <https://cloud.google.com/run/docs/securing/using-cmek>`_ reference to encrypt the container with. - 'run.googleapis.com/execution-environment' sets the `execution environment <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--execution-environment>`_ where the application will run. - 'run.googleapis.com/post-key-revocation-action-type' sets the `action type <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--post-key-revocation-action-type>`_ after CMEK key revocation. - 'run.googleapis.com/secrets' sets a list of key-value pairs to set as `secrets <https://cloud.google.com/run/docs/configuring/secrets#yaml>`_. - 'run.googleapis.com/sessionAffinity' sets whether to enable `session affinity <https://cloud.google.com/sdk/gcloud/reference/beta/run/deploy#--%5Bno-%5Dsession-affinity>`_ for connections to the Revision. - 'run.googleapis.com/startup-cpu-boost' sets whether to allocate extra CPU to containers on startup. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-boost. - 'run.googleapis.com/network-interfaces' sets `Direct VPC egress <https://cloud.google.com/run/docs/configuring/vpc-direct-vpc#yaml>`_ for the Revision. - 'run.googleapis.com/vpc-access-connector' sets a `VPC connector <https://cloud.google.com/run/docs/configuring/connecting-vpc#terraform_1>`_ for the Revision. - 'run.googleapis.com/vpc-access-egress' sets the outbound traffic to send through the VPC connector for this resource. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--vpc-egress. - 'run.googleapis.com/gpu-zonal-redundancy-disabled' sets `GPU zonal redundancy <https://cloud.google.com/run/docs/configuring/services/gpu-zonal-redundancy>`_ for the Revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#annotations CloudRunService#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#labels CloudRunService#labels}
        :param name: Name must be unique within a Google Cloud project and region. Is required when creating resources. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. It will default to the resource's project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#namespace CloudRunService#namespace}
        '''
        value = CloudRunServiceTemplateMetadata(
            annotations=annotations, labels=labels, name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        container_concurrency: typing.Optional[jsii.Number] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param container_concurrency: ContainerConcurrency specifies the maximum allowed in-flight (concurrent) requests per container of the Revision. If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#container_concurrency CloudRunService#container_concurrency}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#containers CloudRunService#containers}
        :param node_selector: Node Selector describes the hardware requirements of the resources. Use the following node selector keys to configure features on a Revision: - 'run.googleapis.com/accelerator' sets the `type of GPU <https://cloud.google.com/run/docs/configuring/services/gpu>`_ required by the Revision to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#node_selector CloudRunService#node_selector}
        :param service_account_name: Email address of the IAM service account associated with the revision of the service. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service_account_name CloudRunService#service_account_name}
        :param timeout_seconds: TimeoutSeconds holds the max duration the instance is allowed for responding to a request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#volumes CloudRunService#volumes}
        '''
        value = CloudRunServiceTemplateSpec(
            container_concurrency=container_concurrency,
            containers=containers,
            node_selector=node_selector,
            service_account_name=service_account_name,
            timeout_seconds=timeout_seconds,
            volumes=volumes,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> CloudRunServiceTemplateMetadataOutputReference:
        return typing.cast(CloudRunServiceTemplateMetadataOutputReference, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "CloudRunServiceTemplateSpecOutputReference":
        return typing.cast("CloudRunServiceTemplateSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[CloudRunServiceTemplateMetadata]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateMetadata], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["CloudRunServiceTemplateSpec"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceTemplate]:
        return typing.cast(typing.Optional[CloudRunServiceTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudRunServiceTemplate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81bff54959f55d0cd6580dce3ad85192112e95a78ab88caaff2246343b7d80d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpec",
    jsii_struct_bases=[],
    name_mapping={
        "container_concurrency": "containerConcurrency",
        "containers": "containers",
        "node_selector": "nodeSelector",
        "service_account_name": "serviceAccountName",
        "timeout_seconds": "timeoutSeconds",
        "volumes": "volumes",
    },
)
class CloudRunServiceTemplateSpec:
    def __init__(
        self,
        *,
        container_concurrency: typing.Optional[jsii.Number] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param container_concurrency: ContainerConcurrency specifies the maximum allowed in-flight (concurrent) requests per container of the Revision. If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#container_concurrency CloudRunService#container_concurrency}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#containers CloudRunService#containers}
        :param node_selector: Node Selector describes the hardware requirements of the resources. Use the following node selector keys to configure features on a Revision: - 'run.googleapis.com/accelerator' sets the `type of GPU <https://cloud.google.com/run/docs/configuring/services/gpu>`_ required by the Revision to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#node_selector CloudRunService#node_selector}
        :param service_account_name: Email address of the IAM service account associated with the revision of the service. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service_account_name CloudRunService#service_account_name}
        :param timeout_seconds: TimeoutSeconds holds the max duration the instance is allowed for responding to a request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#volumes CloudRunService#volumes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5838f957840a38ec56f0a4e13a94eca22332c63bf658d5cd596c54642b0be0b4)
            check_type(argname="argument container_concurrency", value=container_concurrency, expected_type=type_hints["container_concurrency"])
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument node_selector", value=node_selector, expected_type=type_hints["node_selector"])
            check_type(argname="argument service_account_name", value=service_account_name, expected_type=type_hints["service_account_name"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_concurrency is not None:
            self._values["container_concurrency"] = container_concurrency
        if containers is not None:
            self._values["containers"] = containers
        if node_selector is not None:
            self._values["node_selector"] = node_selector
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def container_concurrency(self) -> typing.Optional[jsii.Number]:
        '''ContainerConcurrency specifies the maximum allowed in-flight (concurrent) requests per container of the Revision.

        If not specified or 0, defaults to 80 when
        requested CPU >= 1 and defaults to 1 when requested CPU < 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#container_concurrency CloudRunService#container_concurrency}
        '''
        result = self._values.get("container_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def containers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainers"]]]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#containers CloudRunService#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainers"]]], result)

    @builtins.property
    def node_selector(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Node Selector describes the hardware requirements of the resources.

        Use the following node selector keys to configure features on a Revision:

        - 'run.googleapis.com/accelerator' sets the `type of GPU <https://cloud.google.com/run/docs/configuring/services/gpu>`_ required by the Revision to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#node_selector CloudRunService#node_selector}
        '''
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        '''Email address of the IAM service account associated with the revision of the service.

        The service account represents the identity of the running revision,
        and determines what permissions the revision has. If not provided, the revision
        will use the project's default service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service_account_name CloudRunService#service_account_name}
        '''
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''TimeoutSeconds holds the max duration the instance is allowed for responding to a request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#volumes CloudRunService#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecVolumes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainers",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "command": "command",
        "env": "env",
        "env_from": "envFrom",
        "liveness_probe": "livenessProbe",
        "name": "name",
        "ports": "ports",
        "resources": "resources",
        "startup_probe": "startupProbe",
        "volume_mounts": "volumeMounts",
        "working_dir": "workingDir",
    },
)
class CloudRunServiceTemplateSpecContainers:
    def __init__(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainersEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        env_from: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainersEnvFrom", typing.Dict[builtins.str, typing.Any]]]]] = None,
        liveness_probe: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersLivenessProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainersPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersResources", typing.Dict[builtins.str, typing.Any]]] = None,
        startup_probe: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersStartupProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: Docker image name. This is most often a reference to a container located in the container registry, such as gcr.io/cloudrun/hello. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#image CloudRunService#image}
        :param args: Arguments to the entrypoint. The docker image's CMD is used if this is not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#args CloudRunService#args}
        :param command: Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#command CloudRunService#command}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#env CloudRunService#env}
        :param env_from: env_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#env_from CloudRunService#env_from}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#liveness_probe CloudRunService#liveness_probe}
        :param name: Name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#ports CloudRunService#ports}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#resources CloudRunService#resources}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#startup_probe CloudRunService#startup_probe}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#volume_mounts CloudRunService#volume_mounts}
        :param working_dir: Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#working_dir CloudRunService#working_dir}
        '''
        if isinstance(liveness_probe, dict):
            liveness_probe = CloudRunServiceTemplateSpecContainersLivenessProbe(**liveness_probe)
        if isinstance(resources, dict):
            resources = CloudRunServiceTemplateSpecContainersResources(**resources)
        if isinstance(startup_probe, dict):
            startup_probe = CloudRunServiceTemplateSpecContainersStartupProbe(**startup_probe)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2e52c5f8ff57440df5b0bd86cd7f4c1da3bc56f98cc45677e5c62473cb9b20)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument env_from", value=env_from, expected_type=type_hints["env_from"])
            check_type(argname="argument liveness_probe", value=liveness_probe, expected_type=type_hints["liveness_probe"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument startup_probe", value=startup_probe, expected_type=type_hints["startup_probe"])
            check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
            check_type(argname="argument working_dir", value=working_dir, expected_type=type_hints["working_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if env is not None:
            self._values["env"] = env
        if env_from is not None:
            self._values["env_from"] = env_from
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
        if name is not None:
            self._values["name"] = name
        if ports is not None:
            self._values["ports"] = ports
        if resources is not None:
            self._values["resources"] = resources
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def image(self) -> builtins.str:
        '''Docker image name. This is most often a reference to a container located in the container registry, such as gcr.io/cloudrun/hello.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#image CloudRunService#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to the entrypoint. The docker image's CMD is used if this is not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#args CloudRunService#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#command CloudRunService#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#env CloudRunService#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersEnv"]]], result)

    @builtins.property
    def env_from(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersEnvFrom"]]]:
        '''env_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#env_from CloudRunService#env_from}
        '''
        result = self._values.get("env_from")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersEnvFrom"]]], result)

    @builtins.property
    def liveness_probe(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersLivenessProbe"]:
        '''liveness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#liveness_probe CloudRunService#liveness_probe}
        '''
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersLivenessProbe"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersPorts"]]]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#ports CloudRunService#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersPorts"]]], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#resources CloudRunService#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersResources"], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbe"]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#startup_probe CloudRunService#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbe"], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#volume_mounts CloudRunService#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersVolumeMounts"]]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#working_dir CloudRunService#working_dir}
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "value_from": "valueFrom"},
)
class CloudRunServiceTemplateSpecContainersEnv:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        value_from: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersEnvValueFrom", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param value: Defaults to "". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#value CloudRunService#value}
        :param value_from: value_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#value_from CloudRunService#value_from}
        '''
        if isinstance(value_from, dict):
            value_from = CloudRunServiceTemplateSpecContainersEnvValueFrom(**value_from)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b9fea8b476713a56a0d91dc0fa642e9467d674ab65d3bba7c478e04402c8f1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument value_from", value=value_from, expected_type=type_hints["value_from"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value
        if value_from is not None:
            self._values["value_from"] = value_from

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Defaults to "".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#value CloudRunService#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_from(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersEnvValueFrom"]:
        '''value_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#value_from CloudRunService#value_from}
        '''
        result = self._values.get("value_from")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersEnvValueFrom"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFrom",
    jsii_struct_bases=[],
    name_mapping={
        "config_map_ref": "configMapRef",
        "prefix": "prefix",
        "secret_ref": "secretRef",
    },
)
class CloudRunServiceTemplateSpecContainersEnvFrom:
    def __init__(
        self,
        *,
        config_map_ref: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[builtins.str] = None,
        secret_ref: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersEnvFromSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_map_ref: config_map_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#config_map_ref CloudRunService#config_map_ref}
        :param prefix: An optional identifier to prepend to each key in the ConfigMap. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#prefix CloudRunService#prefix}
        :param secret_ref: secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret_ref CloudRunService#secret_ref}
        '''
        if isinstance(config_map_ref, dict):
            config_map_ref = CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef(**config_map_ref)
        if isinstance(secret_ref, dict):
            secret_ref = CloudRunServiceTemplateSpecContainersEnvFromSecretRef(**secret_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ca57a1cb426ed214907d569917bd63fd5306fe7196391b7fd2d6fe0db1bdfc)
            check_type(argname="argument config_map_ref", value=config_map_ref, expected_type=type_hints["config_map_ref"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument secret_ref", value=secret_ref, expected_type=type_hints["secret_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_map_ref is not None:
            self._values["config_map_ref"] = config_map_ref
        if prefix is not None:
            self._values["prefix"] = prefix
        if secret_ref is not None:
            self._values["secret_ref"] = secret_ref

    @builtins.property
    def config_map_ref(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef"]:
        '''config_map_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#config_map_ref CloudRunService#config_map_ref}
        '''
        result = self._values.get("config_map_ref")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef"], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''An optional identifier to prepend to each key in the ConfigMap.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#prefix CloudRunService#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_ref(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromSecretRef"]:
        '''secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret_ref CloudRunService#secret_ref}
        '''
        result = self._values.get("secret_ref")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromSecretRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersEnvFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef",
    jsii_struct_bases=[],
    name_mapping={
        "local_object_reference": "localObjectReference",
        "optional": "optional",
    },
)
class CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef:
    def __init__(
        self,
        *,
        local_object_reference: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference", typing.Dict[builtins.str, typing.Any]]] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_object_reference: local_object_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#local_object_reference CloudRunService#local_object_reference}
        :param optional: Specify whether the ConfigMap must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#optional CloudRunService#optional}
        '''
        if isinstance(local_object_reference, dict):
            local_object_reference = CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference(**local_object_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718d99fd56878745b9812c60e0bfb10ac75d174bd0cde2b819f74f70c68cf0c2)
            check_type(argname="argument local_object_reference", value=local_object_reference, expected_type=type_hints["local_object_reference"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if local_object_reference is not None:
            self._values["local_object_reference"] = local_object_reference
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def local_object_reference(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference"]:
        '''local_object_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#local_object_reference CloudRunService#local_object_reference}
        '''
        result = self._values.get("local_object_reference")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference"], result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify whether the ConfigMap must be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#optional CloudRunService#optional}
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f207a9b36721f0d23d998f1c0f1f4082af3b968d0351216fe6dd9267e29bb2af)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__930a42fa888526e23bc77c39d5799ad98c5e1572069b1f4ce6029e04aba57990)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac465a9a141c8b2c8fd5ee7a9532ac0e0b60d2b627e87270fc8b4f76d6e3ffbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acae57cf2e5b7706a3d1d8dccb27f9f720f788f3af15d2797bee246bb7e349f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68afb93b3a23d7615f1f80318435bb37da206964d542c117f88752c7bafddcfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalObjectReference")
    def put_local_object_reference(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        value = CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putLocalObjectReference", [value]))

    @jsii.member(jsii_name="resetLocalObjectReference")
    def reset_local_object_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalObjectReference", []))

    @jsii.member(jsii_name="resetOptional")
    def reset_optional(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptional", []))

    @builtins.property
    @jsii.member(jsii_name="localObjectReference")
    def local_object_reference(
        self,
    ) -> CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference, jsii.get(self, "localObjectReference"))

    @builtins.property
    @jsii.member(jsii_name="localObjectReferenceInput")
    def local_object_reference_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference], jsii.get(self, "localObjectReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalInput")
    def optional_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optionalInput"))

    @builtins.property
    @jsii.member(jsii_name="optional")
    def optional(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optional"))

    @optional.setter
    def optional(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a0579a2deb2ce8f2f4cbcbe8145bec64eefea8f1a062fac8579e4617aecbae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1032233525ead0ab4614e2762ef6d0160b670b860a75be4ec7c300a62aa1d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersEnvFromList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df9b2d7ad819ad839d24c46089213b157b7c7b35200414cd98bdd4e35d02a502)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecContainersEnvFromOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd912dec96a58f365562cde845e3f37b7c13d1902ebcff9d37b802d8d9b7126)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecContainersEnvFromOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08045bd0d897f7430254dfa37b5b33a67b5cea977fc2754cb5a1934e2eb172d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e0cac7e2e8e5526ebd65be22ed171b57c0851553a6c8a64ec07be97ec0933ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38c22f182df94fe6978bd2df0f1d72bdb1cb4a40252c6874d1340993f5c074e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnvFrom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnvFrom]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnvFrom]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a420df1c169642d04b5821a9c2bfee606eb8b0a6237dfe24d4537caf8cf280e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersEnvFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f78e4c4a07bdb25474ba08bab048fa14a476045187fb50f6d5b50531216ad06c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConfigMapRef")
    def put_config_map_ref(
        self,
        *,
        local_object_reference: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference, typing.Dict[builtins.str, typing.Any]]] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_object_reference: local_object_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#local_object_reference CloudRunService#local_object_reference}
        :param optional: Specify whether the ConfigMap must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#optional CloudRunService#optional}
        '''
        value = CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef(
            local_object_reference=local_object_reference, optional=optional
        )

        return typing.cast(None, jsii.invoke(self, "putConfigMapRef", [value]))

    @jsii.member(jsii_name="putSecretRef")
    def put_secret_ref(
        self,
        *,
        local_object_reference: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference", typing.Dict[builtins.str, typing.Any]]] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_object_reference: local_object_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#local_object_reference CloudRunService#local_object_reference}
        :param optional: Specify whether the Secret must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#optional CloudRunService#optional}
        '''
        value = CloudRunServiceTemplateSpecContainersEnvFromSecretRef(
            local_object_reference=local_object_reference, optional=optional
        )

        return typing.cast(None, jsii.invoke(self, "putSecretRef", [value]))

    @jsii.member(jsii_name="resetConfigMapRef")
    def reset_config_map_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigMapRef", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetSecretRef")
    def reset_secret_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretRef", []))

    @builtins.property
    @jsii.member(jsii_name="configMapRef")
    def config_map_ref(
        self,
    ) -> CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference, jsii.get(self, "configMapRef"))

    @builtins.property
    @jsii.member(jsii_name="secretRef")
    def secret_ref(
        self,
    ) -> "CloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference":
        return typing.cast("CloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference", jsii.get(self, "secretRef"))

    @builtins.property
    @jsii.member(jsii_name="configMapRefInput")
    def config_map_ref_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef], jsii.get(self, "configMapRefInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="secretRefInput")
    def secret_ref_input(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromSecretRef"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromSecretRef"], jsii.get(self, "secretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5186f9c09e4a9bdbbb957378f057ddcbb4b925f72be34f3bc92e9132725fa8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersEnvFrom]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersEnvFrom]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersEnvFrom]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d591bcc0462a212ce6e290e4ed2d3c8bb3c390422e951089cf5d700233d9517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromSecretRef",
    jsii_struct_bases=[],
    name_mapping={
        "local_object_reference": "localObjectReference",
        "optional": "optional",
    },
)
class CloudRunServiceTemplateSpecContainersEnvFromSecretRef:
    def __init__(
        self,
        *,
        local_object_reference: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference", typing.Dict[builtins.str, typing.Any]]] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_object_reference: local_object_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#local_object_reference CloudRunService#local_object_reference}
        :param optional: Specify whether the Secret must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#optional CloudRunService#optional}
        '''
        if isinstance(local_object_reference, dict):
            local_object_reference = CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference(**local_object_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa31b0af72bf754ec21e1c9a1dcd4a959bf2b729da0b7b84b1ed94b3dfb29d0)
            check_type(argname="argument local_object_reference", value=local_object_reference, expected_type=type_hints["local_object_reference"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if local_object_reference is not None:
            self._values["local_object_reference"] = local_object_reference
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def local_object_reference(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference"]:
        '''local_object_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#local_object_reference CloudRunService#local_object_reference}
        '''
        result = self._values.get("local_object_reference")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference"], result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify whether the Secret must be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#optional CloudRunService#optional}
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersEnvFromSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066b98c3b55dd711623d91b37655de4a2b362c14ee6a98d6568689f56839bf62)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45ca6e46d073028eb9bb743bf106f1cb40343b74f66c8d7041c1850d9cd330ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366d81c51194ddb7738e46004e2d542a98dadb8c4041fa22a804f902ee943f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf6d4d8a161b2cf71e91961dc24e3251ff7d33a25ae723d481a0886419e36d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38da2473c35dfa8b186fe3b76179badac9d7a3702e18c5429a841f91d8c073a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalObjectReference")
    def put_local_object_reference(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        value = CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putLocalObjectReference", [value]))

    @jsii.member(jsii_name="resetLocalObjectReference")
    def reset_local_object_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalObjectReference", []))

    @jsii.member(jsii_name="resetOptional")
    def reset_optional(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptional", []))

    @builtins.property
    @jsii.member(jsii_name="localObjectReference")
    def local_object_reference(
        self,
    ) -> CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference, jsii.get(self, "localObjectReference"))

    @builtins.property
    @jsii.member(jsii_name="localObjectReferenceInput")
    def local_object_reference_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference], jsii.get(self, "localObjectReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalInput")
    def optional_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optionalInput"))

    @builtins.property
    @jsii.member(jsii_name="optional")
    def optional(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optional"))

    @optional.setter
    def optional(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67047bd2eb4bfd2ff0f8de0f768cad24655217b0b374b130539ecaccdba52a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRef]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c540ed58f87069e19c08f8cda016f33144d1ef159aba7a28300825c270e97b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6547c0c79f33e75da64e4700299c9f5c4e8a27a72e175bd2fd3280d188199aa6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecContainersEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43070440bdbfc00ba49d98fff9111f8f8316bf7e557eef2f09b939445101444a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecContainersEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd33ecbf52ab748d33268938992c6a55747456f0e8af4eee588b39f6cd851b92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89e9d09d7970e881a39c00ea53bdf5b57fd7c59f28fa4c1523eac1b808d754f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f0705c427af2fa38810f8610caf60206e4182a2814442b3546996441402b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27873054352eb5b6d4f959a26ded4b0136a6690368985ac61125f57dc15822c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b735be375e8394d1ccb3cc7defbf261652f0c124fd4a607a142488d3e4bed3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueFrom")
    def put_value_from(
        self,
        *,
        secret_key_ref: typing.Union["CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret_key_ref CloudRunService#secret_key_ref}
        '''
        value = CloudRunServiceTemplateSpecContainersEnvValueFrom(
            secret_key_ref=secret_key_ref
        )

        return typing.cast(None, jsii.invoke(self, "putValueFrom", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValueFrom")
    def reset_value_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueFrom", []))

    @builtins.property
    @jsii.member(jsii_name="valueFrom")
    def value_from(
        self,
    ) -> "CloudRunServiceTemplateSpecContainersEnvValueFromOutputReference":
        return typing.cast("CloudRunServiceTemplateSpecContainersEnvValueFromOutputReference", jsii.get(self, "valueFrom"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueFromInput")
    def value_from_input(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersEnvValueFrom"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersEnvValueFrom"], jsii.get(self, "valueFromInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755f26b74fc2e348ec6805352df298551ad6c9027e6504f1ca82f87892cda713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4f79965136e0511b4e563a0f71f9c8c2d79259ab21fc6f794f0865fbb9e7a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad652fca181c1e653b8d7f709f0e9844a17c5c76e95682a5d4ca58f90139cb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvValueFrom",
    jsii_struct_bases=[],
    name_mapping={"secret_key_ref": "secretKeyRef"},
)
class CloudRunServiceTemplateSpecContainersEnvValueFrom:
    def __init__(
        self,
        *,
        secret_key_ref: typing.Union["CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret_key_ref CloudRunService#secret_key_ref}
        '''
        if isinstance(secret_key_ref, dict):
            secret_key_ref = CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef(**secret_key_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc66d421389e90bbbb7a1c2d8d0973910a98d7270d554237b58a0f98056afc4)
            check_type(argname="argument secret_key_ref", value=secret_key_ref, expected_type=type_hints["secret_key_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_key_ref": secret_key_ref,
        }

    @builtins.property
    def secret_key_ref(
        self,
    ) -> "CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef":
        '''secret_key_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret_key_ref CloudRunService#secret_key_ref}
        '''
        result = self._values.get("secret_key_ref")
        assert result is not None, "Required property 'secret_key_ref' is missing"
        return typing.cast("CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersEnvValueFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersEnvValueFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvValueFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f4ab3c1fc109d063e9c4fd38106ccadae2bb6db572dd81aad2ec4716b1ee53c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretKeyRef")
    def put_secret_key_ref(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: A Cloud Secret Manager secret version. Must be 'latest' for the latest version or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#key CloudRunService#key}
        :param name: The name of the secret in Cloud Secret Manager. By default, the secret is assumed to be in the same project. If the secret is in another project, you must define an alias. An alias definition has the form: {alias}:projects/{project-id|project-number}/secrets/{secret-name}. If multiple alias definitions are needed, they must be separated by commas. The alias definitions must be set on the run.googleapis.com/secrets annotation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        value = CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef(
            key=key, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putSecretKeyRef", [value]))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRef")
    def secret_key_ref(
        self,
    ) -> "CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference":
        return typing.cast("CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference", jsii.get(self, "secretKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRefInput")
    def secret_key_ref_input(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef"], jsii.get(self, "secretKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvValueFrom]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvValueFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvValueFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec06b8fec91e3ecd763b1c9e807a8eaa5d4eb2469c3a93bd5a98bcf00a4f621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name"},
)
class CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef:
    def __init__(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: A Cloud Secret Manager secret version. Must be 'latest' for the latest version or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#key CloudRunService#key}
        :param name: The name of the secret in Cloud Secret Manager. By default, the secret is assumed to be in the same project. If the secret is in another project, you must define an alias. An alias definition has the form: {alias}:projects/{project-id|project-number}/secrets/{secret-name}. If multiple alias definitions are needed, they must be separated by commas. The alias definitions must be set on the run.googleapis.com/secrets annotation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc92c33c3d649f494017704a7ccc3708b036a4049e41b3a31059ebbe0bd8214c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "name": name,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''A Cloud Secret Manager secret version. Must be 'latest' for the latest version or an integer for a specific version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#key CloudRunService#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the secret in Cloud Secret Manager.

        By default, the secret is assumed to be in the same project.
        If the secret is in another project, you must define an alias.
        An alias definition has the form:
        {alias}:projects/{project-id|project-number}/secrets/{secret-name}.
        If multiple alias definitions are needed, they must be separated by commas.
        The alias definitions must be set on the run.googleapis.com/secrets annotation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c43c4d15eb7c8356390d3aa22cec0452371ce5aa0c7acb59a78ff7948ccc0ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6366666f487dca34df6785d9c1b9bf8a4faedb1ce252aea75327bb9db1308a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac83aa2af9c011b6fa97d44a73065efd8be8655553a66db19b03c191fc3d26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f058bb799186f22f252fc2f367a02d8b145d10cd515a1ba00f232506ac0db9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41db2ccbea3f45a939113afad154f5473dfa2951a6d60e837057467a0d9e87a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d033d0e8a8c0f3e87c9c4acf656455a158fae39091b9936370e0549decbaa2f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1c9c61c59971057b0184bf8fbf38c0f7980e9ea24b6f47697b94d2085a7d26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__180c64df493ebe4e8df9c4bbdc699e31ffaf82d1c5fb7cebf768f459a1561cbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db68708e27323e9a3a293a1f25b5b332a89de7a6f895c8825e0aa576ddb49892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14adb70ed7ce3603bfc9b0d8d3151db9e5ba07e3bcd44cb942ab8421649ec196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbe",
    jsii_struct_bases=[],
    name_mapping={
        "failure_threshold": "failureThreshold",
        "grpc": "grpc",
        "http_get": "httpGet",
        "initial_delay_seconds": "initialDelaySeconds",
        "period_seconds": "periodSeconds",
        "timeout_seconds": "timeoutSeconds",
    },
)
class CloudRunServiceTemplateSpecContainersLivenessProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersLivenessProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#failure_threshold CloudRunService#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#grpc CloudRunService#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_get CloudRunService#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#initial_delay_seconds CloudRunService#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#period_seconds CloudRunService#period_seconds}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than period_seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = CloudRunServiceTemplateSpecContainersLivenessProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet(**http_get)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a596cada56c167fec619a1d83579b426ea332bea91b1138de89bf5d59285c2)
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http_get", value=http_get, expected_type=type_hints["http_get"])
            check_type(argname="argument initial_delay_seconds", value=initial_delay_seconds, expected_type=type_hints["initial_delay_seconds"])
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if grpc is not None:
            self._values["grpc"] = grpc
        if http_get is not None:
            self._values["http_get"] = http_get
        if initial_delay_seconds is not None:
            self._values["initial_delay_seconds"] = initial_delay_seconds
        if period_seconds is not None:
            self._values["period_seconds"] = period_seconds
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#failure_threshold CloudRunService#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersLivenessProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#grpc CloudRunService#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersLivenessProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_get CloudRunService#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value is 3600.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#initial_delay_seconds CloudRunService#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 3600.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#period_seconds CloudRunService#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600.
        Must be smaller than period_seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersLivenessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class CloudRunServiceTemplateSpecContainersLivenessProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service CloudRunService#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902d99e5afa82d26505456a113ac2bddf986c6aa0d6411e364a9a66c5e0304a7)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service CloudRunService#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersLivenessProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff1a21e5b2608e2446e988853769211d7386a696d1ee134727de75c2f5204f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__452a83553fc9db899f93e80c0ee80e4f3bb04b395a574fe6aecac3a6c29f5175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf44d64b2ddd2b20096adcfc730444faccb16f99e8a2da04f3f17cbb004ff2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1769f189040a7dc28349a73b5d5020433f5e4458f888b3e6d4003339f9528d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_headers CloudRunService#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b73c8fb726e9ab31cc99df89cea1201e46fbe12eca684111c874bbb180112fb)
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_headers CloudRunService#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. If set, it should not be empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#value CloudRunService#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf85c0b992c026e44e6d5cda296d43f15f60f3636c995e33d4e47900b0cf066)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The header field name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#value CloudRunService#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f284136cdcfd595f4c994a672ee3dfbc9787befc8d715da50f2a328094b75f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d89e2fd393c70767aaa05ef809f5edf04a44ecab1d65cea64a0b825de982c7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd144b5ae5fa6c931c1d407cc0e26a13d255ef3b7425ceb11bd5a5d5564a85e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69a1a7e0c313efba31dfa3e6607d870c89911c11700938bf31c6034c6547c987)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78efe6a640b4dceaa4c3aab437dc9ffaaefc5b17f59ec3e3ef424994ff805f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a15bf4c0cdc34982b45e7449e4acc0e0f96b69a739c113aac93754f909ec83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3538fd1d36b3588f2745dd7aea6fbf7742972505314764eb53e022e44f00f840)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea91b63adc325005b7c48f31f9f8add890845e795f5331ccb0ad3d2bd9bcf04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3205c9d25dfb0cdda69d1b5f1edc87f24511a09aac7658415fe64e456c2f6b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1703ad88a4308f64f820a58f5c2c5122bfedd00c7069cdcd46ab6dedb3df74b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2110bad5acddbc17651371dad8ea731d3bb00514080a74133713621b900f17e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5faaad0a910248fa1791f77d679e7a39640978ab7ddfecaae7b5d76e5dedde37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeaders", [value]))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(
        self,
    ) -> CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList:
        return typing.cast(CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4523bec5c47b7ede5d40b3ea0aff0f583f57760c9d0c5f1150aa02bfba91c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d570f3555fcf64f9c423a0396500ef00f0ca6c7634b4e01cf983bbc9a37d3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7483554e512270f6e04a71d605bedf53f6bf32f4e51e49d18e0adf02ec77433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersLivenessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersLivenessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a3de912c6313f11d0c82e44e11cc0288cd724ccbfb4a0c10839be7a5d02c5f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service CloudRunService#service}
        '''
        value = CloudRunServiceTemplateSpecContainersLivenessProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_headers CloudRunService#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        value = CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet(
            http_headers=http_headers, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttpGet")
    def reset_http_get(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpGet", []))

    @jsii.member(jsii_name="resetInitialDelaySeconds")
    def reset_initial_delay_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySeconds", []))

    @jsii.member(jsii_name="resetPeriodSeconds")
    def reset_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodSeconds", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> CloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet], jsii.get(self, "httpGetInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecondsInput")
    def initial_delay_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852da826cea8094fd8212f502c408428edfac0aa721ea509aa7a95fe122325f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d64bd5752052d74fd20bb1b830d679f875ed611a05bdd92d76a64676b2e7b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aec391b29409b5602e63f13c1c4007a95af529041fb58784385f2d3cf1deac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedc2025713d4287ce9458ca5f54e75a0b441c53977976e127672ab6876fe7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbe]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f931000e02af3d6db9cf2a9c06594fcc6ac3d237853333a0da5467b55360256d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9467789d51e335350ea9bd4ec45b09d6b4e00cc2f9bdb2c8a74d6541490d8c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5483256df8a6ac2bcf2acf0b77fad8060f1232cabe293b1405b9afad107f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putEnvFrom")
    def put_env_from(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersEnvFrom, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794eb07ba4585d2cee01320f766bfe62d934134a05a56cdcc9bdd9fb8f9f1b05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvFrom", [value]))

    @jsii.member(jsii_name="putLivenessProbe")
    def put_liveness_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#failure_threshold CloudRunService#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#grpc CloudRunService#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_get CloudRunService#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#initial_delay_seconds CloudRunService#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#period_seconds CloudRunService#period_seconds}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than period_seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        '''
        value = CloudRunServiceTemplateSpecContainersLivenessProbe(
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putLivenessProbe", [value]))

    @jsii.member(jsii_name="putPorts")
    def put_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainersPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec66e6542f9034c6271c5537cb6bc66af620b12e2abb8d146484c065242aee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        *,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        requests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param limits: Limits describes the maximum amount of compute resources allowed. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#limits CloudRunService#limits}
        :param requests: Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#requests CloudRunService#requests}
        '''
        value = CloudRunServiceTemplateSpecContainersResources(
            limits=limits, requests=requests
        )

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#failure_threshold CloudRunService#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#grpc CloudRunService#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_get CloudRunService#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#initial_delay_seconds CloudRunService#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#period_seconds CloudRunService#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#tcp_socket CloudRunService#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        '''
        value = CloudRunServiceTemplateSpecContainersStartupProbe(
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            tcp_socket=tcp_socket,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putStartupProbe", [value]))

    @jsii.member(jsii_name="putVolumeMounts")
    def put_volume_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f954766915d52b2817f44971eb2b0deb0d0294126c3ebbbed608b5ec88dbbeec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeMounts", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetEnvFrom")
    def reset_env_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvFrom", []))

    @jsii.member(jsii_name="resetLivenessProbe")
    def reset_liveness_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivenessProbe", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetStartupProbe")
    def reset_startup_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupProbe", []))

    @jsii.member(jsii_name="resetVolumeMounts")
    def reset_volume_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMounts", []))

    @jsii.member(jsii_name="resetWorkingDir")
    def reset_working_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDir", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> CloudRunServiceTemplateSpecContainersEnvList:
        return typing.cast(CloudRunServiceTemplateSpecContainersEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="envFrom")
    def env_from(self) -> CloudRunServiceTemplateSpecContainersEnvFromList:
        return typing.cast(CloudRunServiceTemplateSpecContainersEnvFromList, jsii.get(self, "envFrom"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbe")
    def liveness_probe(
        self,
    ) -> CloudRunServiceTemplateSpecContainersLivenessProbeOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecContainersLivenessProbeOutputReference, jsii.get(self, "livenessProbe"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> "CloudRunServiceTemplateSpecContainersPortsList":
        return typing.cast("CloudRunServiceTemplateSpecContainersPortsList", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "CloudRunServiceTemplateSpecContainersResourcesOutputReference":
        return typing.cast("CloudRunServiceTemplateSpecContainersResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(
        self,
    ) -> "CloudRunServiceTemplateSpecContainersStartupProbeOutputReference":
        return typing.cast("CloudRunServiceTemplateSpecContainersStartupProbeOutputReference", jsii.get(self, "startupProbe"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(self) -> "CloudRunServiceTemplateSpecContainersVolumeMountsList":
        return typing.cast("CloudRunServiceTemplateSpecContainersVolumeMountsList", jsii.get(self, "volumeMounts"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="envFromInput")
    def env_from_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnvFrom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnvFrom]]], jsii.get(self, "envFromInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbeInput")
    def liveness_probe_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbe]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbe], jsii.get(self, "livenessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersPorts"]]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersResources"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="startupProbeInput")
    def startup_probe_input(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbe"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbe"], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirInput")
    def working_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54299d1726b24dee083131380063a8dedcd9e3623b4453db345f8a9bbf7a02c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c9b7cb72c4f904de42f94135b6f0e7e19e92ad99e68f677d58b243d5f982db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5360ca4aa376d55f5085c86a3a89597c02a8783d345c14f7c437934031eda93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5e90d4319a2264f41ccd5312919d0dce8feac8cf5e44f69f78222095e21731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0203c03ea8eb5700a6caa1c370f1502263ae08d3fb80bcfc50d294e2e4d32cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df21024ed38634f2b61c399b48cb70da95a6eb00eb6b88fcd9175e8b99b5c184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersPorts",
    jsii_struct_bases=[],
    name_mapping={
        "container_port": "containerPort",
        "name": "name",
        "protocol": "protocol",
    },
)
class CloudRunServiceTemplateSpecContainersPorts:
    def __init__(
        self,
        *,
        container_port: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_port: Port number the container listens on. This must be a valid port number (between 1 and 65535). Defaults to "8080". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#container_port CloudRunService#container_port}
        :param name: If specified, used to specify which protocol to use. Allowed values are "http1" (HTTP/1) and "h2c" (HTTP/2 end-to-end). Defaults to "http1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param protocol: Protocol for port. Must be "TCP". Defaults to "TCP". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#protocol CloudRunService#protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88315be7b5e7fd6083a45ae4c248f3d0c4100419f4ec9dca5e0a9b973aa9e260)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_port is not None:
            self._values["container_port"] = container_port
        if name is not None:
            self._values["name"] = name
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''Port number the container listens on.

        This must be a valid port number (between 1 and 65535). Defaults to "8080".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#container_port CloudRunService#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''If specified, used to specify which protocol to use.

        Allowed values are "http1" (HTTP/1) and "h2c" (HTTP/2 end-to-end). Defaults to "http1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Protocol for port. Must be "TCP". Defaults to "TCP".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#protocol CloudRunService#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6489d8160e02d8ac84dfe95695b06b3c0a00ac0fb7b4ce2905a05812261c414a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecContainersPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d99581100b1cc8e7552e4a4a509ee63b93d1a6285fb98157a8df95636419256)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecContainersPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631f6ed9f6ef691cd7fe7c71e59769c9bef159ccda9b7400d4072e97bddd1fcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43167935ec0da932de6ce135f60241d99a1d591d71806c1d1fe550d89d879221)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e9bc693d3b27d6de9eec6a51982bbbd78edce2012b54660f6fd333ba0afa928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8e022abf5ea1f2db20be02cff9115f9df28cc4a6f4afd22e7c608220b993f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e427e760cfe18e53013a695fe1e042182751981dd392e49f8bdb690cd385638)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContainerPort")
    def reset_container_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerPort", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="containerPortInput")
    def container_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerPort"))

    @container_port.setter
    def container_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f66e194b9f196c1370f9855fca263c43425c308d2a6b9aed66941155801be4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c334c47fc8ac0619f85cefd46f3cff6951157f345d4edca17ee145f7589835e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3de7138a1872c4fcd9bb641a6ace18042a118f9d07106e4489e1eaea000d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5dff792de215cdbcda459f4aa5591d934d85da3b7b793b997cd889b26145367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "requests": "requests"},
)
class CloudRunServiceTemplateSpecContainersResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        requests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param limits: Limits describes the maximum amount of compute resources allowed. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#limits CloudRunService#limits}
        :param requests: Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#requests CloudRunService#requests}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed3e0413cfd9dd992013b708c171e3c3768cff7a50706eca2fd62704bdd8144)
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument requests", value=requests, expected_type=type_hints["requests"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limits is not None:
            self._values["limits"] = limits
        if requests is not None:
            self._values["requests"] = requests

    @builtins.property
    def limits(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Limits describes the maximum amount of compute resources allowed.

        The values of the map is string form of the 'quantity' k8s type:
        https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#limits CloudRunService#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def requests(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Requests describes the minimum amount of compute resources required.

        If Requests is omitted for a container, it defaults to Limits if that is
        explicitly specified, otherwise to an implementation-defined value.
        The values of the map is string form of the 'quantity' k8s type:
        https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#requests CloudRunService#requests}
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c45ae6ad43baa4d7fed74bd2e7fa5db0eedcbc8b7f296b34e6646d56cf0b2ead)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetRequests")
    def reset_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequests", []))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="requestsInput")
    def requests_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "requestsInput"))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "limits"))

    @limits.setter
    def limits(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ca662ff79d6efac12972782035a0724f5a61b415a16bcdd7869f2a32bbb7d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requests")
    def requests(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requests"))

    @requests.setter
    def requests(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99d774e7963a0227dddd425c628bf1556d36cc793eb1d45236b15170cdf19e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersResources]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277a01af45ef7b8158f6f7a6d8c434c001824adfaa02475b6c22341293ff321a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbe",
    jsii_struct_bases=[],
    name_mapping={
        "failure_threshold": "failureThreshold",
        "grpc": "grpc",
        "http_get": "httpGet",
        "initial_delay_seconds": "initialDelaySeconds",
        "period_seconds": "periodSeconds",
        "tcp_socket": "tcpSocket",
        "timeout_seconds": "timeoutSeconds",
    },
)
class CloudRunServiceTemplateSpecContainersStartupProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#failure_threshold CloudRunService#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#grpc CloudRunService#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_get CloudRunService#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#initial_delay_seconds CloudRunService#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#period_seconds CloudRunService#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#tcp_socket CloudRunService#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = CloudRunServiceTemplateSpecContainersStartupProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = CloudRunServiceTemplateSpecContainersStartupProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b77154acea3164f73de0f88141d5a26ae80ff5c676029ffc3bfc1a0f293659)
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http_get", value=http_get, expected_type=type_hints["http_get"])
            check_type(argname="argument initial_delay_seconds", value=initial_delay_seconds, expected_type=type_hints["initial_delay_seconds"])
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument tcp_socket", value=tcp_socket, expected_type=type_hints["tcp_socket"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if grpc is not None:
            self._values["grpc"] = grpc
        if http_get is not None:
            self._values["http_get"] = http_get
        if initial_delay_seconds is not None:
            self._values["initial_delay_seconds"] = initial_delay_seconds
        if period_seconds is not None:
            self._values["period_seconds"] = period_seconds
        if tcp_socket is not None:
            self._values["tcp_socket"] = tcp_socket
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#failure_threshold CloudRunService#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#grpc CloudRunService#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_get CloudRunService#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value is 240.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#initial_delay_seconds CloudRunService#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#period_seconds CloudRunService#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#tcp_socket CloudRunService#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600.
        Must be smaller than periodSeconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#timeout_seconds CloudRunService#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class CloudRunServiceTemplateSpecContainersStartupProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service CloudRunService#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1767d3af955882ed74b7f7d707d95c6fe162975d6457f353714e0feead2e3c)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service CloudRunService#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersStartupProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__267e3abbdd12a5e4685cf8e388dca23a9c38d2bdf38f977a97edb4f2b0ec3bf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f8b048d8dfc94fbad066612cbe522954d31561e4dc24334a516b6162cf4a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c490ba1d9e51d66834875566bf36ef85298c0d2a39a36de15e09b29aff61e203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715994e4709913dd46bd3058f24098481f37d9966b4dbc066a432399877d1760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class CloudRunServiceTemplateSpecContainersStartupProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_headers CloudRunService#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab4e35d821881544e3a074b17e48f86430ed406e2ad8b1578831af24f62d66f)
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_headers CloudRunService#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. If set, it should not be empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersStartupProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#value CloudRunService#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a301f0c05c0fd9c9c64ca31c910b2a7024e8c23d35c30eb6d0b312a901ee1489)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The header field name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#value CloudRunService#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e52bcf9e9e77d5bb129d8c7f7272ff3575fd5f12590c5715baa2c311b1beebca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55b93f2a5ff2e28aa78b81b4d3e77c6b2c464429d8fdcd3b650018ba84b4c7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13839702d295578b9c430979f48daf73b4cc1f3e33dcc45624dc4c5acc6dbd23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9acf5e1b02834b68568dce49665827a861459512afeb7ea1bd2eb85ebaa0e907)
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
            type_hints = typing.get_type_hints(_typecheckingstub__771b84bdac311a44b0597ec688199ffb5c14573a2b6fdbd14acb4c611cdc1d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a88ebeb8f07dba2c5dc6bdd38fb03e5be0c69199cdc33e7ef4d222ddaff324e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61c4a9496d500db79ca3232727c76bed7c671607cb3f470b3f0538540262a8e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ffbce2304774465bedebdb60f53d957ce33a6b6f375960a2a885f7d32a2a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533fc9b69b9371f8d8363d16717feab2713d1cb0509f3df8f0e4b36066a65379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445953d281d9fb6c372673ef02464f043124fcd27a8336bfb54c6b59a4bfdaf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__124cde0f32ab3ab781282455907a15931387b34e61132e43a2d3e6d780cc3f8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8368ca50bce24744bb62cbf425c17a3829709e07094d189a111ecd92fbde120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeaders", [value]))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(
        self,
    ) -> CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList:
        return typing.cast(CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cebec45ed8ae5dbd1da8c01fb8398c384fa8a057e6c38dba6282f1b56744c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1323ede1b448f49843bfe7e8982346b444c60c0aced719a3fa9258246095207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46a366662af1e9ed20dfc6886a6966b0d4897acfacf7d5221af9e1c973c3583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc6f24be73e08531987debc614290dc28863fe0c8f479005daca284cd3c6a144)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#service CloudRunService#service}
        '''
        value = CloudRunServiceTemplateSpecContainersStartupProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#http_headers CloudRunService#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        value = CloudRunServiceTemplateSpecContainersStartupProbeHttpGet(
            http_headers=http_headers, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        value = CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket(port=port)

        return typing.cast(None, jsii.invoke(self, "putTcpSocket", [value]))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttpGet")
    def reset_http_get(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpGet", []))

    @jsii.member(jsii_name="resetInitialDelaySeconds")
    def reset_initial_delay_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySeconds", []))

    @jsii.member(jsii_name="resetPeriodSeconds")
    def reset_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodSeconds", []))

    @jsii.member(jsii_name="resetTcpSocket")
    def reset_tcp_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpSocket", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> CloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> CloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "CloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference":
        return typing.cast("CloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeHttpGet], jsii.get(self, "httpGetInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecondsInput")
    def initial_delay_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocketInput")
    def tcp_socket_input(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57984fac9a0a18aa41a86684ad5b68f869d9ffdee98257140474161846d2a540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd46fde0f85fe8dede6076831ee91905e34851eead67aad2a4ac5850b50bc14b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25594c56fd509a6161712070888c42c81da237062872854811fa52beb56374a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36a5149a43fb41e105f9e0d127ea9a81db1254ec4be6aa5630c3d193cb6b9d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbe]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de09dbe05dd5e69d34bd37248774543649c5185fe8e2c1349a817bb13ffbb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"port": "port"},
)
class CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket:
    def __init__(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ee69358fb38860559199994424633ac205e66c5b572ba0ad8af778c82eaaaa)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#port CloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e98f90f51ec6f41f6b0dbc284a4394e0240711e41bd5a23b220ba40ca97d223)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb4d7fe693d6076a865b92c38bbc5e0b2faecd1cf561f597a58a123a271a2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41bb6be8be926b15ca2702a28a1c7ed7c7426572912c4dab0063f7ae511652d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"mount_path": "mountPath", "name": "name"},
)
class CloudRunServiceTemplateSpecContainersVolumeMounts:
    def __init__(self, *, mount_path: builtins.str, name: builtins.str) -> None:
        '''
        :param mount_path: Path within the container at which the volume should be mounted. Must not contain ':'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#mount_path CloudRunService#mount_path}
        :param name: This must match the Name of a Volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0509cc7eb512cf9493edb7356a232bb7ef8caa1c82265e6a218dcb47a51c96d2)
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mount_path": mount_path,
            "name": name,
        }

    @builtins.property
    def mount_path(self) -> builtins.str:
        '''Path within the container at which the volume should be mounted.  Must not contain ':'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#mount_path CloudRunService#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''This must match the Name of a Volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecContainersVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecContainersVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a4a71871f7f41d3a3938b08cd1158538e96217a687143a3d7ac3a3b2fa59d3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecContainersVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbfdbaef20222e4db6b722c5a5d9310b308e789f419d184d9d1fa2a1c3cb7d3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecContainersVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f21f481cce56b4320b5b7a132f8b03493d118808b9f9e46290583f977a4aff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcec92b6ff47d80546417882b36fe26984207d01d7d777772af43e4a6e4403e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc6c376a9cce4db402ceb446e33942c604c9361993637811c0b8624da08eb531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42dfb918b76f5f118372d7e9e12d724dcc3fdcfa17c4403ee62347f5d6c2ef09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecContainersVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecContainersVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6885bbabdc6f8b31171405c49f6933de3378e10297784b493580623e7a44947a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0194845bb71318ac4f6e583aad1a441b81d71d999d253b38c1eee10394c16d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23245c4267a770f2235a029bc44cbb9a959c3e13a79b54d03eb1035e749735e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45a39f3a01f173e31d4ff24a0836174cd5563591c3cbe716e67dfd75bd69d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72539577b9c7dd086428c31253e992a8edb68a43947c54faa3c04e90ae4bcfed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f420af45c153af7f8e9466b02b5bc23e662d349720f919d7112af19eaeda17a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainers", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd6bc1e41f00df9a74fc5650a12aad393209f1e469549593237140743b1e74f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="resetContainerConcurrency")
    def reset_container_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerConcurrency", []))

    @jsii.member(jsii_name="resetContainers")
    def reset_containers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainers", []))

    @jsii.member(jsii_name="resetNodeSelector")
    def reset_node_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeSelector", []))

    @jsii.member(jsii_name="resetServiceAccountName")
    def reset_service_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountName", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(self) -> CloudRunServiceTemplateSpecContainersList:
        return typing.cast(CloudRunServiceTemplateSpecContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="servingState")
    def serving_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servingState"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "CloudRunServiceTemplateSpecVolumesList":
        return typing.cast("CloudRunServiceTemplateSpecVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="containerConcurrencyInput")
    def container_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="containersInput")
    def containers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainers]]], jsii.get(self, "containersInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelectorInput")
    def node_selector_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nodeSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountNameInput")
    def service_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerConcurrency")
    def container_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerConcurrency"))

    @container_concurrency.setter
    def container_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f1c4a44e1d40287cdd3a6c0413e137d9db348ba1431225804a28bb0567d8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeSelector")
    def node_selector(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nodeSelector"))

    @node_selector.setter
    def node_selector(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4edf4e8f253a2cf3f0f7a70b9ff6219de67f027aaf2450b4c9e3a142b4f9c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeSelector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountName"))

    @service_account_name.setter
    def service_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e23afa55a8c917138610595479f4c0843735bfb69f00877e403b6c53b5d4380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9486747cb3e5dce397a66bd3fb4f8479832847d292727bde2175681236f5d5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceTemplateSpec]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2abd2eb55322cce09b7f1348328c5a6d2d0afb62507799b369ec1aa979fc059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "csi": "csi",
        "empty_dir": "emptyDir",
        "nfs": "nfs",
        "secret": "secret",
    },
)
class CloudRunServiceTemplateSpecVolumes:
    def __init__(
        self,
        *,
        name: builtins.str,
        csi: typing.Optional[typing.Union["CloudRunServiceTemplateSpecVolumesCsi", typing.Dict[builtins.str, typing.Any]]] = None,
        empty_dir: typing.Optional[typing.Union["CloudRunServiceTemplateSpecVolumesEmptyDir", typing.Dict[builtins.str, typing.Any]]] = None,
        nfs: typing.Optional[typing.Union["CloudRunServiceTemplateSpecVolumesNfs", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["CloudRunServiceTemplateSpecVolumesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Volume's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        :param csi: csi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#csi CloudRunService#csi}
        :param empty_dir: empty_dir block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#empty_dir CloudRunService#empty_dir}
        :param nfs: nfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#nfs CloudRunService#nfs}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret CloudRunService#secret}
        '''
        if isinstance(csi, dict):
            csi = CloudRunServiceTemplateSpecVolumesCsi(**csi)
        if isinstance(empty_dir, dict):
            empty_dir = CloudRunServiceTemplateSpecVolumesEmptyDir(**empty_dir)
        if isinstance(nfs, dict):
            nfs = CloudRunServiceTemplateSpecVolumesNfs(**nfs)
        if isinstance(secret, dict):
            secret = CloudRunServiceTemplateSpecVolumesSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2cdc203ec4e76583173840157e8c6b1c279c557438d7dd1c47e6ebc548c629)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument csi", value=csi, expected_type=type_hints["csi"])
            check_type(argname="argument empty_dir", value=empty_dir, expected_type=type_hints["empty_dir"])
            check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if csi is not None:
            self._values["csi"] = csi
        if empty_dir is not None:
            self._values["empty_dir"] = empty_dir
        if nfs is not None:
            self._values["nfs"] = nfs
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def name(self) -> builtins.str:
        '''Volume's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#name CloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def csi(self) -> typing.Optional["CloudRunServiceTemplateSpecVolumesCsi"]:
        '''csi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#csi CloudRunService#csi}
        '''
        result = self._values.get("csi")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecVolumesCsi"], result)

    @builtins.property
    def empty_dir(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecVolumesEmptyDir"]:
        '''empty_dir block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#empty_dir CloudRunService#empty_dir}
        '''
        result = self._values.get("empty_dir")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecVolumesEmptyDir"], result)

    @builtins.property
    def nfs(self) -> typing.Optional["CloudRunServiceTemplateSpecVolumesNfs"]:
        '''nfs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#nfs CloudRunService#nfs}
        '''
        result = self._values.get("nfs")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecVolumesNfs"], result)

    @builtins.property
    def secret(self) -> typing.Optional["CloudRunServiceTemplateSpecVolumesSecret"]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret CloudRunService#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecVolumesSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesCsi",
    jsii_struct_bases=[],
    name_mapping={
        "driver": "driver",
        "read_only": "readOnly",
        "volume_attributes": "volumeAttributes",
    },
)
class CloudRunServiceTemplateSpecVolumesCsi:
    def __init__(
        self,
        *,
        driver: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver: Unique name representing the type of file system to be created. Cloud Run supports the following values: - gcsfuse.run.googleapis.com: Mount a Google Cloud Storage bucket using GCSFuse. This driver requires the run.googleapis.com/execution-environment annotation to be unset or set to "gen2" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#driver CloudRunService#driver}
        :param read_only: If true, all mounts created from this volume will be read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#read_only CloudRunService#read_only}
        :param volume_attributes: Driver-specific attributes. The following options are supported for available drivers: - gcsfuse.run.googleapis.com - bucketName: The name of the Cloud Storage Bucket that backs this volume. The Cloud Run Service identity must have access to this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#volume_attributes CloudRunService#volume_attributes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d54f95ddc388d8019d958c4bb38479002c6bd6a7d2e3740f0c4d9c194fc19d6)
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument volume_attributes", value=volume_attributes, expected_type=type_hints["volume_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver": driver,
        }
        if read_only is not None:
            self._values["read_only"] = read_only
        if volume_attributes is not None:
            self._values["volume_attributes"] = volume_attributes

    @builtins.property
    def driver(self) -> builtins.str:
        '''Unique name representing the type of file system to be created.

        Cloud Run supports the following values:

        - gcsfuse.run.googleapis.com: Mount a Google Cloud Storage bucket using GCSFuse. This driver requires the
          run.googleapis.com/execution-environment annotation to be unset or set to "gen2"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#driver CloudRunService#driver}
        '''
        result = self._values.get("driver")
        assert result is not None, "Required property 'driver' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, all mounts created from this volume will be read-only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#read_only CloudRunService#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def volume_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Driver-specific attributes.

        The following options are supported for available drivers:

        - gcsfuse.run.googleapis.com

          - bucketName: The name of the Cloud Storage Bucket that backs this volume. The Cloud Run Service identity must have access to this bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#volume_attributes CloudRunService#volume_attributes}
        '''
        result = self._values.get("volume_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecVolumesCsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecVolumesCsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesCsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3017098248c52b5d0cabc1a145bb997be68f12857c3a74b552e8509bee5cdcbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetVolumeAttributes")
    def reset_volume_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="driverInput")
    def driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeAttributesInput")
    def volume_attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "volumeAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driver"))

    @driver.setter
    def driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c982d6e354f595a0a16e37227924c28501d22a8da768d449de1cf9c90999ebd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8deb4ae762d0b4412e65ae3db139ddf4190944c595d0dd4aab764ac8f674d24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeAttributes")
    def volume_attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "volumeAttributes"))

    @volume_attributes.setter
    def volume_attributes(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff44a0363af55315a64c829be8e0e5a0e810a9fe84a8e3b9ac72122a118a890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceTemplateSpecVolumesCsi]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecVolumesCsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecVolumesCsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d282cb92b202af24e451521c3dcbcf2ced03d84cedf1cebac5063989fa7a176d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesEmptyDir",
    jsii_struct_bases=[],
    name_mapping={"medium": "medium", "size_limit": "sizeLimit"},
)
class CloudRunServiceTemplateSpecVolumesEmptyDir:
    def __init__(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The medium on which the data is stored. The default is "" which means to use the node's default medium. Must be an empty string (default) or Memory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#medium CloudRunService#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#size_limit CloudRunService#size_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360f8465807cc8e9d75d50cd1d524538df5c5e053c381dd7b19dd1f68765f6bc)
            check_type(argname="argument medium", value=medium, expected_type=type_hints["medium"])
            check_type(argname="argument size_limit", value=size_limit, expected_type=type_hints["size_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if medium is not None:
            self._values["medium"] = medium
        if size_limit is not None:
            self._values["size_limit"] = size_limit

    @builtins.property
    def medium(self) -> typing.Optional[builtins.str]:
        '''The medium on which the data is stored.

        The default is "" which means to use the node's default medium. Must be an empty string (default) or Memory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#medium CloudRunService#medium}
        '''
        result = self._values.get("medium")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_limit(self) -> typing.Optional[builtins.str]:
        '''Limit on the storage usable by this EmptyDir volume.

        The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#size_limit CloudRunService#size_limit}
        '''
        result = self._values.get("size_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecVolumesEmptyDir(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecVolumesEmptyDirOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesEmptyDirOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9dbf33ae311c3d45abe7dafebc2a40c76e7775e5e37e351f951a933ced3949)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMedium")
    def reset_medium(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMedium", []))

    @jsii.member(jsii_name="resetSizeLimit")
    def reset_size_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeLimit", []))

    @builtins.property
    @jsii.member(jsii_name="mediumInput")
    def medium_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediumInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeLimitInput")
    def size_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="medium")
    def medium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "medium"))

    @medium.setter
    def medium(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c2b7eac67a261ac6a987a872c8ced2953ebb177853bdaa76f13c24f23d3bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "medium", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeLimit")
    def size_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeLimit"))

    @size_limit.setter
    def size_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73dc20aa62586f59e6507e117e5ef82da6a166d9a43713bada12cff69241ec3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecVolumesEmptyDir]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecVolumesEmptyDir], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecVolumesEmptyDir],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c62ce7ec49419f3b2b21acdd6a5c5984f6cf4178b4b5078ef036a52af3d464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21f2647a1e5182b6a01d62e0c28c209f35e057c11e55f42bb3a95b83c4d6c8d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b051a9ef8775a387b6f92d3fdfdc7dd7220686db90f99b82d372fad27dcb77e7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1984efe7b0b9368a19517ccb3dd292c466d940b018a3fcef75e13a0dd3f7adeb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d01ba0861fde637971b94481ed27da1bab9633faaa5ca42ba43d19c3d56b88d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aebb633a354d1e3d2591cddc4fe615cbcd9b71171915982e18b02db145bc8317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd568ed42cb77039a405c426ec56e3b03d45fd90ba42402d83becb9c3fd64987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesNfs",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "server": "server", "read_only": "readOnly"},
)
class CloudRunServiceTemplateSpecVolumesNfs:
    def __init__(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        :param server: IP address or hostname of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#server CloudRunService#server}
        :param read_only: If true, mount the NFS volume as read only in all mounts. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#read_only CloudRunService#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d6d3133dbec2e28e84721090252a5404738012b44d1f0d4409867f0a909df0)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "server": server,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def path(self) -> builtins.str:
        '''Path exported by the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''IP address or hostname of the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#server CloudRunService#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount the NFS volume as read only in all mounts. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#read_only CloudRunService#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecVolumesNfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecVolumesNfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesNfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__028c3e11fea5c57ddce971ff2ae2d6373f6e760fe1d90e206ac2759373183c78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74b72379540621d095bd3d1311df92eda86b2804344b775a02d4c45caa457db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebf7c5318c2dcda55f39dcfa406a8391a6dadaa03277c53f87bb9b74d36717a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187c0bb5847438654c648f2acb6528020daa691e22117e719cf8385ee7cfd0d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunServiceTemplateSpecVolumesNfs]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecVolumesNfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecVolumesNfs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3327be927abceb61337d0e1a2afa0d9aae08a4d350d5ff053879af98eb03001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__956a40b24eef5856e124acc0d2e21d516c8be4c86faf5f175c4c7332ad8d16a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCsi")
    def put_csi(
        self,
        *,
        driver: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver: Unique name representing the type of file system to be created. Cloud Run supports the following values: - gcsfuse.run.googleapis.com: Mount a Google Cloud Storage bucket using GCSFuse. This driver requires the run.googleapis.com/execution-environment annotation to be unset or set to "gen2" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#driver CloudRunService#driver}
        :param read_only: If true, all mounts created from this volume will be read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#read_only CloudRunService#read_only}
        :param volume_attributes: Driver-specific attributes. The following options are supported for available drivers: - gcsfuse.run.googleapis.com - bucketName: The name of the Cloud Storage Bucket that backs this volume. The Cloud Run Service identity must have access to this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#volume_attributes CloudRunService#volume_attributes}
        '''
        value = CloudRunServiceTemplateSpecVolumesCsi(
            driver=driver, read_only=read_only, volume_attributes=volume_attributes
        )

        return typing.cast(None, jsii.invoke(self, "putCsi", [value]))

    @jsii.member(jsii_name="putEmptyDir")
    def put_empty_dir(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The medium on which the data is stored. The default is "" which means to use the node's default medium. Must be an empty string (default) or Memory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#medium CloudRunService#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#size_limit CloudRunService#size_limit}
        '''
        value = CloudRunServiceTemplateSpecVolumesEmptyDir(
            medium=medium, size_limit=size_limit
        )

        return typing.cast(None, jsii.invoke(self, "putEmptyDir", [value]))

    @jsii.member(jsii_name="putNfs")
    def put_nfs(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        :param server: IP address or hostname of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#server CloudRunService#server}
        :param read_only: If true, mount the NFS volume as read only in all mounts. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#read_only CloudRunService#read_only}
        '''
        value = CloudRunServiceTemplateSpecVolumesNfs(
            path=path, server=server, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putNfs", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        *,
        secret_name: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret_name: The name of the secret in Cloud Secret Manager. By default, the secret is assumed to be in the same project. If the secret is in another project, you must define an alias. An alias definition has the form: {alias}:projects/{project-id|project-number}/secrets/{secret-name}. If multiple alias definitions are needed, they must be separated by commas. The alias definitions must be set on the run.googleapis.com/secrets annotation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret_name CloudRunService#secret_name}
        :param default_mode: Mode bits to use on created files by default. Must be a value between 0000 and 0777. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#default_mode CloudRunService#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#items CloudRunService#items}
        '''
        value = CloudRunServiceTemplateSpecVolumesSecret(
            secret_name=secret_name, default_mode=default_mode, items=items
        )

        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="resetCsi")
    def reset_csi(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsi", []))

    @jsii.member(jsii_name="resetEmptyDir")
    def reset_empty_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmptyDir", []))

    @jsii.member(jsii_name="resetNfs")
    def reset_nfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfs", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @builtins.property
    @jsii.member(jsii_name="csi")
    def csi(self) -> CloudRunServiceTemplateSpecVolumesCsiOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecVolumesCsiOutputReference, jsii.get(self, "csi"))

    @builtins.property
    @jsii.member(jsii_name="emptyDir")
    def empty_dir(self) -> CloudRunServiceTemplateSpecVolumesEmptyDirOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecVolumesEmptyDirOutputReference, jsii.get(self, "emptyDir"))

    @builtins.property
    @jsii.member(jsii_name="nfs")
    def nfs(self) -> CloudRunServiceTemplateSpecVolumesNfsOutputReference:
        return typing.cast(CloudRunServiceTemplateSpecVolumesNfsOutputReference, jsii.get(self, "nfs"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "CloudRunServiceTemplateSpecVolumesSecretOutputReference":
        return typing.cast("CloudRunServiceTemplateSpecVolumesSecretOutputReference", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="csiInput")
    def csi_input(self) -> typing.Optional[CloudRunServiceTemplateSpecVolumesCsi]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecVolumesCsi], jsii.get(self, "csiInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyDirInput")
    def empty_dir_input(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecVolumesEmptyDir]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecVolumesEmptyDir], jsii.get(self, "emptyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsInput")
    def nfs_input(self) -> typing.Optional[CloudRunServiceTemplateSpecVolumesNfs]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecVolumesNfs], jsii.get(self, "nfsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional["CloudRunServiceTemplateSpecVolumesSecret"]:
        return typing.cast(typing.Optional["CloudRunServiceTemplateSpecVolumesSecret"], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b198c3848ba1d41889574d659c34879ba8ed4a16202493f39e0788cdea4303c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a415af08a45ab811ca123934c76fb26696af384437a027f66a15055d8716f917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesSecret",
    jsii_struct_bases=[],
    name_mapping={
        "secret_name": "secretName",
        "default_mode": "defaultMode",
        "items": "items",
    },
)
class CloudRunServiceTemplateSpecVolumesSecret:
    def __init__(
        self,
        *,
        secret_name: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunServiceTemplateSpecVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret_name: The name of the secret in Cloud Secret Manager. By default, the secret is assumed to be in the same project. If the secret is in another project, you must define an alias. An alias definition has the form: {alias}:projects/{project-id|project-number}/secrets/{secret-name}. If multiple alias definitions are needed, they must be separated by commas. The alias definitions must be set on the run.googleapis.com/secrets annotation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret_name CloudRunService#secret_name}
        :param default_mode: Mode bits to use on created files by default. Must be a value between 0000 and 0777. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#default_mode CloudRunService#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#items CloudRunService#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1606e01cdb81bf5b77ba9add43a4445d13bdbfc57acdcec29bf0c086f9c4f69)
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument default_mode", value=default_mode, expected_type=type_hints["default_mode"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_name": secret_name,
        }
        if default_mode is not None:
            self._values["default_mode"] = default_mode
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''The name of the secret in Cloud Secret Manager.

        By default, the secret
        is assumed to be in the same project.
        If the secret is in another project, you must define an alias.
        An alias definition has the form:
        {alias}:projects/{project-id|project-number}/secrets/{secret-name}.
        If multiple alias definitions are needed, they must be separated by
        commas.
        The alias definitions must be set on the run.googleapis.com/secrets
        annotation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#secret_name CloudRunService#secret_name}
        '''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_mode(self) -> typing.Optional[jsii.Number]:
        '''Mode bits to use on created files by default.

        Must be a value between 0000
        and 0777. Defaults to 0644. Directories within the path are not affected by
        this setting. This might be in conflict with other options that affect the
        file mode, like fsGroup, and the result can be other mode bits set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#default_mode CloudRunService#default_mode}
        '''
        result = self._values.get("default_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecVolumesSecretItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#items CloudRunService#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunServiceTemplateSpecVolumesSecretItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecVolumesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesSecretItems",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "path": "path", "mode": "mode"},
)
class CloudRunServiceTemplateSpecVolumesSecretItems:
    def __init__(
        self,
        *,
        key: builtins.str,
        path: builtins.str,
        mode: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param key: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#key CloudRunService#key}
        :param path: The relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        :param mode: Mode bits to use on this file, must be a value between 0000 and 0777. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#mode CloudRunService#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30da389e193407fb74bd08d496b7fabb0119dd0137f9f57e4c153d23d74aef04)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "path": path,
        }
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def key(self) -> builtins.str:
        '''The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#key CloudRunService#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The relative path of the file to map the key to.

        May not be an absolute path.
        May not contain the path element '..'.
        May not start with the string '..'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#path CloudRunService#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        '''Mode bits to use on this file, must be a value between 0000 and 0777.

        If
        not specified, the volume defaultMode will be used. This might be in
        conflict with other options that affect the file mode, like fsGroup, and
        the result can be other mode bits set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#mode CloudRunService#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTemplateSpecVolumesSecretItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTemplateSpecVolumesSecretItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesSecretItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4a99b625205f5837ea37a47132d02b7b7fb998058110051e16a847790498b68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunServiceTemplateSpecVolumesSecretItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aee5550330a5c2d40b7856bd068210753249ab0ba9ac6dc2ce245d9e76aa3f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTemplateSpecVolumesSecretItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430bf63038c24bb27eff53e4bc21ac82dcba8918d223dd9d4286e7c426effa35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__840247e6c2e027af25dfbdbce31547d28509a33a4e37c15e585b87818c3b8a7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eb1dc13f9f7ce364071c5e3117a7a5fd2bf13692dc59cf3b8603bee48988cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumesSecretItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumesSecretItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262b57af771125fb22e63dad94e2dda6f5b8fb884c4e786d707ba6638c9c68d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecVolumesSecretItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesSecretItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f8441bf603774e42825337b16c4da3045fefc6ab3940a74c3a890b8a9de3e4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50414e533f998427dd00163467173d150ba47092c666486275e8a103c2cefb3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf009a0461d8227d1b3781b95f7b9c1729039948d4a5d47a2e5e6648fb82cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1e90ecabf4eaa1f78ff2fcde13e6654d2e996e93676515afb7ddb6ce94ee3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecVolumesSecretItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecVolumesSecretItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecVolumesSecretItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__521fd8067949f3198c259349d9153b370be93628ec9e575f811b4a655c688611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTemplateSpecVolumesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTemplateSpecVolumesSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__857eadbdf5df56a1d02d3ed73cba44c03b86cbf18ee851ff4d403908c3ea134c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33f80cfb8c02bbc205392c905f70154caa2d1b555cce9bd4c29c0a676de144f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetDefaultMode")
    def reset_default_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultMode", []))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudRunServiceTemplateSpecVolumesSecretItemsList:
        return typing.cast(CloudRunServiceTemplateSpecVolumesSecretItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="defaultModeInput")
    def default_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultModeInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumesSecretItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultMode")
    def default_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultMode"))

    @default_mode.setter
    def default_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d77f514a5d2f31b1bdd8f51146b84b5f5d959f6f6389a82e29fabb0f97b08b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00834e9c00f50fef1551881b0f1cfd3087ef061b293f4ff858ccddf17aeee032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunServiceTemplateSpecVolumesSecret]:
        return typing.cast(typing.Optional[CloudRunServiceTemplateSpecVolumesSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunServiceTemplateSpecVolumesSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8bbfcf25efbce8498d4e95aece1345a6bc75ce7df39df82d353ba32fbb1021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudRunServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#create CloudRunService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#delete CloudRunService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#update CloudRunService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6db9da8a2f00496047f1c19dbb18d39881038084d1e003ae23b42a9d9a2d83c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#create CloudRunService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#delete CloudRunService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#update CloudRunService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9af8e2e9affcbf890484c7d2034619317abc273419ef610810bb40b3ba8d1310)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e231d52b9fe7effa4bce18aec716e55b0ef03abaec5b8cab660f1c34e358ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192158be44bdbcd6697c1de7a781650f1b9f7a855911516cb482505665eac1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ac28ab7d5653b8342e39b0caed6fb817ab3406ca345ce2edad60c99444c982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca7085c278ff6bccaee9b50de30739268901a6f5b47a3de4d117ef7d16efff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTraffic",
    jsii_struct_bases=[],
    name_mapping={
        "percent": "percent",
        "latest_revision": "latestRevision",
        "revision_name": "revisionName",
        "tag": "tag",
    },
)
class CloudRunServiceTraffic:
    def __init__(
        self,
        *,
        percent: jsii.Number,
        latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        revision_name: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param percent: Percent specifies percent of the traffic to this Revision or Configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#percent CloudRunService#percent}
        :param latest_revision: LatestRevision may be optionally provided to indicate that the latest ready Revision of the Configuration should be used for this traffic target. When provided LatestRevision must be true if RevisionName is empty; it must be false when RevisionName is non-empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#latest_revision CloudRunService#latest_revision}
        :param revision_name: RevisionName of a specific revision to which to send this portion of traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#revision_name CloudRunService#revision_name}
        :param tag: Tag is optionally used to expose a dedicated url for referencing this target exclusively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#tag CloudRunService#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1354b38534b779b16e0d0444f4751697604c49aba280898d25320075349cd0)
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
            check_type(argname="argument latest_revision", value=latest_revision, expected_type=type_hints["latest_revision"])
            check_type(argname="argument revision_name", value=revision_name, expected_type=type_hints["revision_name"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "percent": percent,
        }
        if latest_revision is not None:
            self._values["latest_revision"] = latest_revision
        if revision_name is not None:
            self._values["revision_name"] = revision_name
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def percent(self) -> jsii.Number:
        '''Percent specifies percent of the traffic to this Revision or Configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#percent CloudRunService#percent}
        '''
        result = self._values.get("percent")
        assert result is not None, "Required property 'percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def latest_revision(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''LatestRevision may be optionally provided to indicate that the latest ready Revision of the Configuration should be used for this traffic target.

        When
        provided LatestRevision must be true if RevisionName is empty; it must be
        false when RevisionName is non-empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#latest_revision CloudRunService#latest_revision}
        '''
        result = self._values.get("latest_revision")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def revision_name(self) -> typing.Optional[builtins.str]:
        '''RevisionName of a specific revision to which to send this portion of traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#revision_name CloudRunService#revision_name}
        '''
        result = self._values.get("revision_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Tag is optionally used to expose a dedicated url for referencing this target exclusively.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_service#tag CloudRunService#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunServiceTraffic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunServiceTrafficList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTrafficList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c34609aec2c70c607d487aacfd8fa5f4be1b8fcc7ac3a9dd7a12216ebad8da14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudRunServiceTrafficOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c70691149f5ee22010038cf2d960851228d193a14cb6bd0f4adc55b7b66d92)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunServiceTrafficOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e544c1f4c4f86767cb48d19054fec96322e5e81a297c67e331f66fe9832d86f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15bf46b5d7151eda699401f4b7a65cd9a7e3428b2e924fd1121e7d3f850e85bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b7cc853c48babc65f1e3611af1e1948ac96db4a4e682a98b304005c70720f8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTraffic]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTraffic]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTraffic]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0957e4662bd04946758abea6a1365bca3d80662a7e96c65a00a9537fee03255c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunServiceTrafficOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunService.CloudRunServiceTrafficOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aca3bf57545c00a6f605237007e31282d1632b6a195bd53031fb1687f10827fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLatestRevision")
    def reset_latest_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatestRevision", []))

    @jsii.member(jsii_name="resetRevisionName")
    def reset_revision_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevisionName", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="latestRevisionInput")
    def latest_revision_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "latestRevisionInput"))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionNameInput")
    def revision_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="latestRevision")
    def latest_revision(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "latestRevision"))

    @latest_revision.setter
    def latest_revision(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997589da95b69f927a7419a1b61da234f5db0e45280ec18d4fa79eaa707c4482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latestRevision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fb2961f824aaaa1c5cbd949e755fa5d22f967435257e5877a14dbc939f5c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revisionName")
    def revision_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionName"))

    @revision_name.setter
    def revision_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c6964517840588c01eaf7810ce645bb68bf2f2d6b03bb3d5a3fbcf1ff74cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revisionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3c36a8b87ccbc973eea499e9500bd17207f39f2a3846a65c64b556372649f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTraffic]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTraffic]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTraffic]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe92d6516f1d02e2f080fe16a2cafb3afb598873041b5413b8b50f9d5247f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudRunService",
    "CloudRunServiceConfig",
    "CloudRunServiceMetadata",
    "CloudRunServiceMetadataOutputReference",
    "CloudRunServiceStatus",
    "CloudRunServiceStatusConditions",
    "CloudRunServiceStatusConditionsList",
    "CloudRunServiceStatusConditionsOutputReference",
    "CloudRunServiceStatusList",
    "CloudRunServiceStatusOutputReference",
    "CloudRunServiceStatusTraffic",
    "CloudRunServiceStatusTrafficList",
    "CloudRunServiceStatusTrafficOutputReference",
    "CloudRunServiceTemplate",
    "CloudRunServiceTemplateMetadata",
    "CloudRunServiceTemplateMetadataOutputReference",
    "CloudRunServiceTemplateOutputReference",
    "CloudRunServiceTemplateSpec",
    "CloudRunServiceTemplateSpecContainers",
    "CloudRunServiceTemplateSpecContainersEnv",
    "CloudRunServiceTemplateSpecContainersEnvFrom",
    "CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef",
    "CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference",
    "CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference",
    "CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference",
    "CloudRunServiceTemplateSpecContainersEnvFromList",
    "CloudRunServiceTemplateSpecContainersEnvFromOutputReference",
    "CloudRunServiceTemplateSpecContainersEnvFromSecretRef",
    "CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference",
    "CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference",
    "CloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference",
    "CloudRunServiceTemplateSpecContainersEnvList",
    "CloudRunServiceTemplateSpecContainersEnvOutputReference",
    "CloudRunServiceTemplateSpecContainersEnvValueFrom",
    "CloudRunServiceTemplateSpecContainersEnvValueFromOutputReference",
    "CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef",
    "CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference",
    "CloudRunServiceTemplateSpecContainersList",
    "CloudRunServiceTemplateSpecContainersLivenessProbe",
    "CloudRunServiceTemplateSpecContainersLivenessProbeGrpc",
    "CloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference",
    "CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet",
    "CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders",
    "CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList",
    "CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference",
    "CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference",
    "CloudRunServiceTemplateSpecContainersLivenessProbeOutputReference",
    "CloudRunServiceTemplateSpecContainersOutputReference",
    "CloudRunServiceTemplateSpecContainersPorts",
    "CloudRunServiceTemplateSpecContainersPortsList",
    "CloudRunServiceTemplateSpecContainersPortsOutputReference",
    "CloudRunServiceTemplateSpecContainersResources",
    "CloudRunServiceTemplateSpecContainersResourcesOutputReference",
    "CloudRunServiceTemplateSpecContainersStartupProbe",
    "CloudRunServiceTemplateSpecContainersStartupProbeGrpc",
    "CloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference",
    "CloudRunServiceTemplateSpecContainersStartupProbeHttpGet",
    "CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders",
    "CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList",
    "CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference",
    "CloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference",
    "CloudRunServiceTemplateSpecContainersStartupProbeOutputReference",
    "CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket",
    "CloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference",
    "CloudRunServiceTemplateSpecContainersVolumeMounts",
    "CloudRunServiceTemplateSpecContainersVolumeMountsList",
    "CloudRunServiceTemplateSpecContainersVolumeMountsOutputReference",
    "CloudRunServiceTemplateSpecOutputReference",
    "CloudRunServiceTemplateSpecVolumes",
    "CloudRunServiceTemplateSpecVolumesCsi",
    "CloudRunServiceTemplateSpecVolumesCsiOutputReference",
    "CloudRunServiceTemplateSpecVolumesEmptyDir",
    "CloudRunServiceTemplateSpecVolumesEmptyDirOutputReference",
    "CloudRunServiceTemplateSpecVolumesList",
    "CloudRunServiceTemplateSpecVolumesNfs",
    "CloudRunServiceTemplateSpecVolumesNfsOutputReference",
    "CloudRunServiceTemplateSpecVolumesOutputReference",
    "CloudRunServiceTemplateSpecVolumesSecret",
    "CloudRunServiceTemplateSpecVolumesSecretItems",
    "CloudRunServiceTemplateSpecVolumesSecretItemsList",
    "CloudRunServiceTemplateSpecVolumesSecretItemsOutputReference",
    "CloudRunServiceTemplateSpecVolumesSecretOutputReference",
    "CloudRunServiceTimeouts",
    "CloudRunServiceTimeoutsOutputReference",
    "CloudRunServiceTraffic",
    "CloudRunServiceTrafficList",
    "CloudRunServiceTrafficOutputReference",
]

publication.publish()

def _typecheckingstub__6ae7f44c196d582ff867d90e3e725809d7c7414de600e93ea3686128ad3a50c8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    autogenerate_revision_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[CloudRunServiceMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    template: typing.Optional[typing.Union[CloudRunServiceTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudRunServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTraffic, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__4d1dc21af59308423bb3755a2284a6bb78369b37afcfae94cb96fe0a73b999c1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dea454bc2f330287360cd25cfc6eddc032ef80312cab392619f93f2746545f0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTraffic, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f642ed35b9d19937df2832584471493620d3b6f90ae9f5fa013c956d70c8e5b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47e604eaa020c95864a5eeb431eec687b6d27d7d6d4feabb2c3e30a02d755db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4004ea2ab9cbd1d79eea8edb0b1e03c710aefd762b1e88a052dd4d472e0a52a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d761526537f908a49ce279db8038e1270febfec15ca865bf3c533b1873adc303(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cac4186e06590708dc151bf47b064d94369d6bb90ef99e175fa7919bc4cef91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a3fabddea5d800abd6a935a28df7243edd8a33f009ad8bc8d20de8a0a75185(
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
    autogenerate_revision_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[CloudRunServiceMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    template: typing.Optional[typing.Union[CloudRunServiceTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudRunServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTraffic, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b04bcb078cfb7f54797b5371324d0ab3d7dcec34a978ba547cc40f4325a2a81(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6545f54fc24c3b3a3cb6de8288f7bda846906d43cb6a0a5fb00b79e98a78f90b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2504a154992caaf0d6dc044fb9fe56052e0096d0a2f0ec0415aec667adca24(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a33bb17c61834bfabcf9fb6afdd71840c6cba2b78d93ab995466e0b23b80be(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc79d97c25e7551a9c3dab87ae24240edf9a0947505f4ce618793e7fcba0e501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ffdf428b470ca2493f35ca04b460e8b21ba0e01a0a8def25a9fa6b43ce25e3(
    value: typing.Optional[CloudRunServiceMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbc4bdf0098f364e61cdb7f6c599f2b6971aac8a2f6359e82963192e95a4ef5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a80bc90b9b0b1f3327d3bcc180d315793c49b3d0094ad4073d25f2ed1ddf8c74(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b97ce5c9352d8c69da06bf55c319d5cf1cca6fdbb6388da838957c15420a2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e0c813acfc218b4f0ff0d8602bc4b8b7378fb2a2215bed187180f02f3ea5b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3770913764d64bb9dbd9f63dccd25e18ed520fdbcdf97a10cdfd06320bc1ec5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998bb5f74672ccf4fd5d4e591cd8409831bd77a11d3d35f087f4e126ae10c1b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2247cacb7087be7eacfd271be485d9b9a66e2f294b349a61ee2df15c5235ed12(
    value: typing.Optional[CloudRunServiceStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cde9a136fa6d92298c4200206e90554e2be9ee894964f72624146d4c2941996(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b708560dde61e0f06529f6a264129ec333c157ff24e1bdc843673f7d207718aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c057a49efda62d5a46bd3a5630c10a57a86d3f632104fe4460fbdf4dc1276811(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb966cb876964775091f82e663d10f709c2ac122fcd8b5f14464ffc2a000dc1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0984ef65af89f3cb6b0f77899b5ec1900fa8f27d003d19cf1fdba0d2c545e62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f930654bdefbfde4d9915daf4b3c8afcf18424f7813845c6756c38e0f83fd19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ec8528c3c28ec5f40755bf419bb6e1c01cfd35368c2de7db7f3c4f10398c5a(
    value: typing.Optional[CloudRunServiceStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ab4962f8e71abfc4ed060672ae98360bca12f0ed69555ff76689a4057f67ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64dd5a69de837ab89b28f911c7e285bab05ecaa58f47eaed76e4cbcf516157f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e348c816476e0fde7bfa9d468f33d97e778498a958e645f202be82e46bb48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9ee2804d73a3b6582419e12e0ec27916e83f0c9762edf257b8c7481f299e8e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1d32d12ad864763759a1c82ebe64b1285f794f9aafbd00e2971c079a58b0ff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5c3aa7a5ecaf72f77c0fb1688cc0114a78d8d4f255871729253ed42d8b4a80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d78c9b77199a2929bdeb18b9adfcc9d47f8f3ed8545758444438920f0fe5360(
    value: typing.Optional[CloudRunServiceStatusTraffic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4ec5e736d99c55dd0328f6b0150776740f1c55d1e392c2a5408205b781ab82(
    *,
    metadata: typing.Optional[typing.Union[CloudRunServiceTemplateMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    spec: typing.Optional[typing.Union[CloudRunServiceTemplateSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f834bde54df86b749730414799d969dc329c57fb1684e38d3e1637cea370100(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac95393d10eada96576bb66fae9bc3fc6c0604c3d240d5f1750d3f211a2973a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067f2ede065640e6548242fcfc6db2e13be87034a4e19fc845c5256fb3c64339(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea1a896cbce4892c721dfdbddc02210d66800cb295f1eb2a440299b25f77bf7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9e43e6adc550c3a2df7bfabed81743ff64676067b6821da014938448298081(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01bb11e4931e0338a2a3b441235e27a9fc068daf3f91e65880dfcf20f3255ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da15b66007e3383d8cd69d932fddfe536baa9f7ad347aa34fdcf90792e86b93f(
    value: typing.Optional[CloudRunServiceTemplateMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10463316140bb78e036e9cf8fd281b7b9ec9bdc7ee265c1241b5d091b6c687b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81bff54959f55d0cd6580dce3ad85192112e95a78ab88caaff2246343b7d80d9(
    value: typing.Optional[CloudRunServiceTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5838f957840a38ec56f0a4e13a94eca22332c63bf658d5cd596c54642b0be0b4(
    *,
    container_concurrency: typing.Optional[jsii.Number] = None,
    containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    service_account_name: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2e52c5f8ff57440df5b0bd86cd7f4c1da3bc56f98cc45677e5c62473cb9b20(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_from: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersEnvFrom, typing.Dict[builtins.str, typing.Any]]]]] = None,
    liveness_probe: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersResources, typing.Dict[builtins.str, typing.Any]]] = None,
    startup_probe: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b9fea8b476713a56a0d91dc0fa642e9467d674ab65d3bba7c478e04402c8f1(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    value_from: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersEnvValueFrom, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ca57a1cb426ed214907d569917bd63fd5306fe7196391b7fd2d6fe0db1bdfc(
    *,
    config_map_ref: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[builtins.str] = None,
    secret_ref: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersEnvFromSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718d99fd56878745b9812c60e0bfb10ac75d174bd0cde2b819f74f70c68cf0c2(
    *,
    local_object_reference: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference, typing.Dict[builtins.str, typing.Any]]] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f207a9b36721f0d23d998f1c0f1f4082af3b968d0351216fe6dd9267e29bb2af(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930a42fa888526e23bc77c39d5799ad98c5e1572069b1f4ce6029e04aba57990(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac465a9a141c8b2c8fd5ee7a9532ac0e0b60d2b627e87270fc8b4f76d6e3ffbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acae57cf2e5b7706a3d1d8dccb27f9f720f788f3af15d2797bee246bb7e349f1(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68afb93b3a23d7615f1f80318435bb37da206964d542c117f88752c7bafddcfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a0579a2deb2ce8f2f4cbcbe8145bec64eefea8f1a062fac8579e4617aecbae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1032233525ead0ab4614e2762ef6d0160b670b860a75be4ec7c300a62aa1d6e(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromConfigMapRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9b2d7ad819ad839d24c46089213b157b7c7b35200414cd98bdd4e35d02a502(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd912dec96a58f365562cde845e3f37b7c13d1902ebcff9d37b802d8d9b7126(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08045bd0d897f7430254dfa37b5b33a67b5cea977fc2754cb5a1934e2eb172d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0cac7e2e8e5526ebd65be22ed171b57c0851553a6c8a64ec07be97ec0933ce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c22f182df94fe6978bd2df0f1d72bdb1cb4a40252c6874d1340993f5c074e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a420df1c169642d04b5821a9c2bfee606eb8b0a6237dfe24d4537caf8cf280e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnvFrom]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78e4c4a07bdb25474ba08bab048fa14a476045187fb50f6d5b50531216ad06c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5186f9c09e4a9bdbbb957378f057ddcbb4b925f72be34f3bc92e9132725fa8ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d591bcc0462a212ce6e290e4ed2d3c8bb3c390422e951089cf5d700233d9517(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersEnvFrom]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa31b0af72bf754ec21e1c9a1dcd4a959bf2b729da0b7b84b1ed94b3dfb29d0(
    *,
    local_object_reference: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference, typing.Dict[builtins.str, typing.Any]]] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066b98c3b55dd711623d91b37655de4a2b362c14ee6a98d6568689f56839bf62(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ca6e46d073028eb9bb743bf106f1cb40343b74f66c8d7041c1850d9cd330ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366d81c51194ddb7738e46004e2d542a98dadb8c4041fa22a804f902ee943f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf6d4d8a161b2cf71e91961dc24e3251ff7d33a25ae723d481a0886419e36d6(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38da2473c35dfa8b186fe3b76179badac9d7a3702e18c5429a841f91d8c073a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67047bd2eb4bfd2ff0f8de0f768cad24655217b0b374b130539ecaccdba52a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c540ed58f87069e19c08f8cda016f33144d1ef159aba7a28300825c270e97b73(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvFromSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6547c0c79f33e75da64e4700299c9f5c4e8a27a72e175bd2fd3280d188199aa6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43070440bdbfc00ba49d98fff9111f8f8316bf7e557eef2f09b939445101444a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd33ecbf52ab748d33268938992c6a55747456f0e8af4eee588b39f6cd851b92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e9d09d7970e881a39c00ea53bdf5b57fd7c59f28fa4c1523eac1b808d754f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f0705c427af2fa38810f8610caf60206e4182a2814442b3546996441402b26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27873054352eb5b6d4f959a26ded4b0136a6690368985ac61125f57dc15822c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b735be375e8394d1ccb3cc7defbf261652f0c124fd4a607a142488d3e4bed3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755f26b74fc2e348ec6805352df298551ad6c9027e6504f1ca82f87892cda713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4f79965136e0511b4e563a0f71f9c8c2d79259ab21fc6f794f0865fbb9e7a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad652fca181c1e653b8d7f709f0e9844a17c5c76e95682a5d4ca58f90139cb71(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc66d421389e90bbbb7a1c2d8d0973910a98d7270d554237b58a0f98056afc4(
    *,
    secret_key_ref: typing.Union[CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4ab3c1fc109d063e9c4fd38106ccadae2bb6db572dd81aad2ec4716b1ee53c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec06b8fec91e3ecd763b1c9e807a8eaa5d4eb2469c3a93bd5a98bcf00a4f621(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvValueFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc92c33c3d649f494017704a7ccc3708b036a4049e41b3a31059ebbe0bd8214c(
    *,
    key: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c43c4d15eb7c8356390d3aa22cec0452371ce5aa0c7acb59a78ff7948ccc0ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6366666f487dca34df6785d9c1b9bf8a4faedb1ce252aea75327bb9db1308a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac83aa2af9c011b6fa97d44a73065efd8be8655553a66db19b03c191fc3d26a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f058bb799186f22f252fc2f367a02d8b145d10cd515a1ba00f232506ac0db9f1(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41db2ccbea3f45a939113afad154f5473dfa2951a6d60e837057467a0d9e87a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d033d0e8a8c0f3e87c9c4acf656455a158fae39091b9936370e0549decbaa2f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1c9c61c59971057b0184bf8fbf38c0f7980e9ea24b6f47697b94d2085a7d26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180c64df493ebe4e8df9c4bbdc699e31ffaf82d1c5fb7cebf768f459a1561cbf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db68708e27323e9a3a293a1f25b5b332a89de7a6f895c8825e0aa576ddb49892(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14adb70ed7ce3603bfc9b0d8d3151db9e5ba07e3bcd44cb942ab8421649ec196(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a596cada56c167fec619a1d83579b426ea332bea91b1138de89bf5d59285c2(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902d99e5afa82d26505456a113ac2bddf986c6aa0d6411e364a9a66c5e0304a7(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff1a21e5b2608e2446e988853769211d7386a696d1ee134727de75c2f5204f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452a83553fc9db899f93e80c0ee80e4f3bb04b395a574fe6aecac3a6c29f5175(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf44d64b2ddd2b20096adcfc730444faccb16f99e8a2da04f3f17cbb004ff2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1769f189040a7dc28349a73b5d5020433f5e4458f888b3e6d4003339f9528d2(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b73c8fb726e9ab31cc99df89cea1201e46fbe12eca684111c874bbb180112fb(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf85c0b992c026e44e6d5cda296d43f15f60f3636c995e33d4e47900b0cf066(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f284136cdcfd595f4c994a672ee3dfbc9787befc8d715da50f2a328094b75f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d89e2fd393c70767aaa05ef809f5edf04a44ecab1d65cea64a0b825de982c7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd144b5ae5fa6c931c1d407cc0e26a13d255ef3b7425ceb11bd5a5d5564a85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a1a7e0c313efba31dfa3e6607d870c89911c11700938bf31c6034c6547c987(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78efe6a640b4dceaa4c3aab437dc9ffaaefc5b17f59ec3e3ef424994ff805f61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a15bf4c0cdc34982b45e7449e4acc0e0f96b69a739c113aac93754f909ec83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3538fd1d36b3588f2745dd7aea6fbf7742972505314764eb53e022e44f00f840(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea91b63adc325005b7c48f31f9f8add890845e795f5331ccb0ad3d2bd9bcf04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3205c9d25dfb0cdda69d1b5f1edc87f24511a09aac7658415fe64e456c2f6b2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1703ad88a4308f64f820a58f5c2c5122bfedd00c7069cdcd46ab6dedb3df74b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2110bad5acddbc17651371dad8ea731d3bb00514080a74133713621b900f17e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5faaad0a910248fa1791f77d679e7a39640978ab7ddfecaae7b5d76e5dedde37(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4523bec5c47b7ede5d40b3ea0aff0f583f57760c9d0c5f1150aa02bfba91c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d570f3555fcf64f9c423a0396500ef00f0ca6c7634b4e01cf983bbc9a37d3ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7483554e512270f6e04a71d605bedf53f6bf32f4e51e49d18e0adf02ec77433(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3de912c6313f11d0c82e44e11cc0288cd724ccbfb4a0c10839be7a5d02c5f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852da826cea8094fd8212f502c408428edfac0aa721ea509aa7a95fe122325f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d64bd5752052d74fd20bb1b830d679f875ed611a05bdd92d76a64676b2e7b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aec391b29409b5602e63f13c1c4007a95af529041fb58784385f2d3cf1deac6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedc2025713d4287ce9458ca5f54e75a0b441c53977976e127672ab6876fe7f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f931000e02af3d6db9cf2a9c06594fcc6ac3d237853333a0da5467b55360256d(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersLivenessProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9467789d51e335350ea9bd4ec45b09d6b4e00cc2f9bdb2c8a74d6541490d8c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5483256df8a6ac2bcf2acf0b77fad8060f1232cabe293b1405b9afad107f01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794eb07ba4585d2cee01320f766bfe62d934134a05a56cdcc9bdd9fb8f9f1b05(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersEnvFrom, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec66e6542f9034c6271c5537cb6bc66af620b12e2abb8d146484c065242aee0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f954766915d52b2817f44971eb2b0deb0d0294126c3ebbbed608b5ec88dbbeec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54299d1726b24dee083131380063a8dedcd9e3623b4453db345f8a9bbf7a02c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c9b7cb72c4f904de42f94135b6f0e7e19e92ad99e68f677d58b243d5f982db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5360ca4aa376d55f5085c86a3a89597c02a8783d345c14f7c437934031eda93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5e90d4319a2264f41ccd5312919d0dce8feac8cf5e44f69f78222095e21731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0203c03ea8eb5700a6caa1c370f1502263ae08d3fb80bcfc50d294e2e4d32cdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df21024ed38634f2b61c399b48cb70da95a6eb00eb6b88fcd9175e8b99b5c184(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88315be7b5e7fd6083a45ae4c248f3d0c4100419f4ec9dca5e0a9b973aa9e260(
    *,
    container_port: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6489d8160e02d8ac84dfe95695b06b3c0a00ac0fb7b4ce2905a05812261c414a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d99581100b1cc8e7552e4a4a509ee63b93d1a6285fb98157a8df95636419256(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631f6ed9f6ef691cd7fe7c71e59769c9bef159ccda9b7400d4072e97bddd1fcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43167935ec0da932de6ce135f60241d99a1d591d71806c1d1fe550d89d879221(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9bc693d3b27d6de9eec6a51982bbbd78edce2012b54660f6fd333ba0afa928(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8e022abf5ea1f2db20be02cff9115f9df28cc4a6f4afd22e7c608220b993f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e427e760cfe18e53013a695fe1e042182751981dd392e49f8bdb690cd385638(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f66e194b9f196c1370f9855fca263c43425c308d2a6b9aed66941155801be4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c334c47fc8ac0619f85cefd46f3cff6951157f345d4edca17ee145f7589835e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3de7138a1872c4fcd9bb641a6ace18042a118f9d07106e4489e1eaea000d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5dff792de215cdbcda459f4aa5591d934d85da3b7b793b997cd889b26145367(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed3e0413cfd9dd992013b708c171e3c3768cff7a50706eca2fd62704bdd8144(
    *,
    limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    requests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45ae6ad43baa4d7fed74bd2e7fa5db0eedcbc8b7f296b34e6646d56cf0b2ead(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ca662ff79d6efac12972782035a0724f5a61b415a16bcdd7869f2a32bbb7d4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99d774e7963a0227dddd425c628bf1556d36cc793eb1d45236b15170cdf19e2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277a01af45ef7b8158f6f7a6d8c434c001824adfaa02475b6c22341293ff321a(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b77154acea3164f73de0f88141d5a26ae80ff5c676029ffc3bfc1a0f293659(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersStartupProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersStartupProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1767d3af955882ed74b7f7d707d95c6fe162975d6457f353714e0feead2e3c(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267e3abbdd12a5e4685cf8e388dca23a9c38d2bdf38f977a97edb4f2b0ec3bf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f8b048d8dfc94fbad066612cbe522954d31561e4dc24334a516b6162cf4a12(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c490ba1d9e51d66834875566bf36ef85298c0d2a39a36de15e09b29aff61e203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715994e4709913dd46bd3058f24098481f37d9966b4dbc066a432399877d1760(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab4e35d821881544e3a074b17e48f86430ed406e2ad8b1578831af24f62d66f(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a301f0c05c0fd9c9c64ca31c910b2a7024e8c23d35c30eb6d0b312a901ee1489(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52bcf9e9e77d5bb129d8c7f7272ff3575fd5f12590c5715baa2c311b1beebca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55b93f2a5ff2e28aa78b81b4d3e77c6b2c464429d8fdcd3b650018ba84b4c7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13839702d295578b9c430979f48daf73b4cc1f3e33dcc45624dc4c5acc6dbd23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acf5e1b02834b68568dce49665827a861459512afeb7ea1bd2eb85ebaa0e907(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771b84bdac311a44b0597ec688199ffb5c14573a2b6fdbd14acb4c611cdc1d93(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a88ebeb8f07dba2c5dc6bdd38fb03e5be0c69199cdc33e7ef4d222ddaff324e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c4a9496d500db79ca3232727c76bed7c671607cb3f470b3f0538540262a8e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ffbce2304774465bedebdb60f53d957ce33a6b6f375960a2a885f7d32a2a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533fc9b69b9371f8d8363d16717feab2713d1cb0509f3df8f0e4b36066a65379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445953d281d9fb6c372673ef02464f043124fcd27a8336bfb54c6b59a4bfdaf5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124cde0f32ab3ab781282455907a15931387b34e61132e43a2d3e6d780cc3f8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8368ca50bce24744bb62cbf425c17a3829709e07094d189a111ecd92fbde120(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cebec45ed8ae5dbd1da8c01fb8398c384fa8a057e6c38dba6282f1b56744c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1323ede1b448f49843bfe7e8982346b444c60c0aced719a3fa9258246095207(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46a366662af1e9ed20dfc6886a6966b0d4897acfacf7d5221af9e1c973c3583(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6f24be73e08531987debc614290dc28863fe0c8f479005daca284cd3c6a144(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57984fac9a0a18aa41a86684ad5b68f869d9ffdee98257140474161846d2a540(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd46fde0f85fe8dede6076831ee91905e34851eead67aad2a4ac5850b50bc14b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25594c56fd509a6161712070888c42c81da237062872854811fa52beb56374a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36a5149a43fb41e105f9e0d127ea9a81db1254ec4be6aa5630c3d193cb6b9d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de09dbe05dd5e69d34bd37248774543649c5185fe8e2c1349a817bb13ffbb4a(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ee69358fb38860559199994424633ac205e66c5b572ba0ad8af778c82eaaaa(
    *,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e98f90f51ec6f41f6b0dbc284a4394e0240711e41bd5a23b220ba40ca97d223(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb4d7fe693d6076a865b92c38bbc5e0b2faecd1cf561f597a58a123a271a2f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41bb6be8be926b15ca2702a28a1c7ed7c7426572912c4dab0063f7ae511652d(
    value: typing.Optional[CloudRunServiceTemplateSpecContainersStartupProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0509cc7eb512cf9493edb7356a232bb7ef8caa1c82265e6a218dcb47a51c96d2(
    *,
    mount_path: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4a71871f7f41d3a3938b08cd1158538e96217a687143a3d7ac3a3b2fa59d3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbfdbaef20222e4db6b722c5a5d9310b308e789f419d184d9d1fa2a1c3cb7d3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f21f481cce56b4320b5b7a132f8b03493d118808b9f9e46290583f977a4aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcec92b6ff47d80546417882b36fe26984207d01d7d777772af43e4a6e4403e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6c376a9cce4db402ceb446e33942c604c9361993637811c0b8624da08eb531(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42dfb918b76f5f118372d7e9e12d724dcc3fdcfa17c4403ee62347f5d6c2ef09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecContainersVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6885bbabdc6f8b31171405c49f6933de3378e10297784b493580623e7a44947a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0194845bb71318ac4f6e583aad1a441b81d71d999d253b38c1eee10394c16d46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23245c4267a770f2235a029bc44cbb9a959c3e13a79b54d03eb1035e749735e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45a39f3a01f173e31d4ff24a0836174cd5563591c3cbe716e67dfd75bd69d57(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecContainersVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72539577b9c7dd086428c31253e992a8edb68a43947c54faa3c04e90ae4bcfed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f420af45c153af7f8e9466b02b5bc23e662d349720f919d7112af19eaeda17a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecContainers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd6bc1e41f00df9a74fc5650a12aad393209f1e469549593237140743b1e74f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f1c4a44e1d40287cdd3a6c0413e137d9db348ba1431225804a28bb0567d8ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4edf4e8f253a2cf3f0f7a70b9ff6219de67f027aaf2450b4c9e3a142b4f9c39(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e23afa55a8c917138610595479f4c0843735bfb69f00877e403b6c53b5d4380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9486747cb3e5dce397a66bd3fb4f8479832847d292727bde2175681236f5d5b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2abd2eb55322cce09b7f1348328c5a6d2d0afb62507799b369ec1aa979fc059(
    value: typing.Optional[CloudRunServiceTemplateSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2cdc203ec4e76583173840157e8c6b1c279c557438d7dd1c47e6ebc548c629(
    *,
    name: builtins.str,
    csi: typing.Optional[typing.Union[CloudRunServiceTemplateSpecVolumesCsi, typing.Dict[builtins.str, typing.Any]]] = None,
    empty_dir: typing.Optional[typing.Union[CloudRunServiceTemplateSpecVolumesEmptyDir, typing.Dict[builtins.str, typing.Any]]] = None,
    nfs: typing.Optional[typing.Union[CloudRunServiceTemplateSpecVolumesNfs, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[CloudRunServiceTemplateSpecVolumesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d54f95ddc388d8019d958c4bb38479002c6bd6a7d2e3740f0c4d9c194fc19d6(
    *,
    driver: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    volume_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3017098248c52b5d0cabc1a145bb997be68f12857c3a74b552e8509bee5cdcbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c982d6e354f595a0a16e37227924c28501d22a8da768d449de1cf9c90999ebd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8deb4ae762d0b4412e65ae3db139ddf4190944c595d0dd4aab764ac8f674d24(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff44a0363af55315a64c829be8e0e5a0e810a9fe84a8e3b9ac72122a118a890(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d282cb92b202af24e451521c3dcbcf2ced03d84cedf1cebac5063989fa7a176d(
    value: typing.Optional[CloudRunServiceTemplateSpecVolumesCsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360f8465807cc8e9d75d50cd1d524538df5c5e053c381dd7b19dd1f68765f6bc(
    *,
    medium: typing.Optional[builtins.str] = None,
    size_limit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9dbf33ae311c3d45abe7dafebc2a40c76e7775e5e37e351f951a933ced3949(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c2b7eac67a261ac6a987a872c8ced2953ebb177853bdaa76f13c24f23d3bdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73dc20aa62586f59e6507e117e5ef82da6a166d9a43713bada12cff69241ec3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c62ce7ec49419f3b2b21acdd6a5c5984f6cf4178b4b5078ef036a52af3d464(
    value: typing.Optional[CloudRunServiceTemplateSpecVolumesEmptyDir],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f2647a1e5182b6a01d62e0c28c209f35e057c11e55f42bb3a95b83c4d6c8d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b051a9ef8775a387b6f92d3fdfdc7dd7220686db90f99b82d372fad27dcb77e7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1984efe7b0b9368a19517ccb3dd292c466d940b018a3fcef75e13a0dd3f7adeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01ba0861fde637971b94481ed27da1bab9633faaa5ca42ba43d19c3d56b88d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebb633a354d1e3d2591cddc4fe615cbcd9b71171915982e18b02db145bc8317(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd568ed42cb77039a405c426ec56e3b03d45fd90ba42402d83becb9c3fd64987(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d6d3133dbec2e28e84721090252a5404738012b44d1f0d4409867f0a909df0(
    *,
    path: builtins.str,
    server: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028c3e11fea5c57ddce971ff2ae2d6373f6e760fe1d90e206ac2759373183c78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74b72379540621d095bd3d1311df92eda86b2804344b775a02d4c45caa457db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebf7c5318c2dcda55f39dcfa406a8391a6dadaa03277c53f87bb9b74d36717a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187c0bb5847438654c648f2acb6528020daa691e22117e719cf8385ee7cfd0d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3327be927abceb61337d0e1a2afa0d9aae08a4d350d5ff053879af98eb03001(
    value: typing.Optional[CloudRunServiceTemplateSpecVolumesNfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956a40b24eef5856e124acc0d2e21d516c8be4c86faf5f175c4c7332ad8d16a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b198c3848ba1d41889574d659c34879ba8ed4a16202493f39e0788cdea4303c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a415af08a45ab811ca123934c76fb26696af384437a027f66a15055d8716f917(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1606e01cdb81bf5b77ba9add43a4445d13bdbfc57acdcec29bf0c086f9c4f69(
    *,
    secret_name: builtins.str,
    default_mode: typing.Optional[jsii.Number] = None,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30da389e193407fb74bd08d496b7fabb0119dd0137f9f57e4c153d23d74aef04(
    *,
    key: builtins.str,
    path: builtins.str,
    mode: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a99b625205f5837ea37a47132d02b7b7fb998058110051e16a847790498b68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aee5550330a5c2d40b7856bd068210753249ab0ba9ac6dc2ce245d9e76aa3f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430bf63038c24bb27eff53e4bc21ac82dcba8918d223dd9d4286e7c426effa35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840247e6c2e027af25dfbdbce31547d28509a33a4e37c15e585b87818c3b8a7c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb1dc13f9f7ce364071c5e3117a7a5fd2bf13692dc59cf3b8603bee48988cbd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262b57af771125fb22e63dad94e2dda6f5b8fb884c4e786d707ba6638c9c68d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTemplateSpecVolumesSecretItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8441bf603774e42825337b16c4da3045fefc6ab3940a74c3a890b8a9de3e4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50414e533f998427dd00163467173d150ba47092c666486275e8a103c2cefb3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf009a0461d8227d1b3781b95f7b9c1729039948d4a5d47a2e5e6648fb82cec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1e90ecabf4eaa1f78ff2fcde13e6654d2e996e93676515afb7ddb6ce94ee3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521fd8067949f3198c259349d9153b370be93628ec9e575f811b4a655c688611(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTemplateSpecVolumesSecretItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857eadbdf5df56a1d02d3ed73cba44c03b86cbf18ee851ff4d403908c3ea134c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33f80cfb8c02bbc205392c905f70154caa2d1b555cce9bd4c29c0a676de144f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunServiceTemplateSpecVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d77f514a5d2f31b1bdd8f51146b84b5f5d959f6f6389a82e29fabb0f97b08b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00834e9c00f50fef1551881b0f1cfd3087ef061b293f4ff858ccddf17aeee032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8bbfcf25efbce8498d4e95aece1345a6bc75ce7df39df82d353ba32fbb1021(
    value: typing.Optional[CloudRunServiceTemplateSpecVolumesSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6db9da8a2f00496047f1c19dbb18d39881038084d1e003ae23b42a9d9a2d83c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af8e2e9affcbf890484c7d2034619317abc273419ef610810bb40b3ba8d1310(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e231d52b9fe7effa4bce18aec716e55b0ef03abaec5b8cab660f1c34e358ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192158be44bdbcd6697c1de7a781650f1b9f7a855911516cb482505665eac1a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ac28ab7d5653b8342e39b0caed6fb817ab3406ca345ce2edad60c99444c982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca7085c278ff6bccaee9b50de30739268901a6f5b47a3de4d117ef7d16efff7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1354b38534b779b16e0d0444f4751697604c49aba280898d25320075349cd0(
    *,
    percent: jsii.Number,
    latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    revision_name: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34609aec2c70c607d487aacfd8fa5f4be1b8fcc7ac3a9dd7a12216ebad8da14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c70691149f5ee22010038cf2d960851228d193a14cb6bd0f4adc55b7b66d92(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e544c1f4c4f86767cb48d19054fec96322e5e81a297c67e331f66fe9832d86f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bf46b5d7151eda699401f4b7a65cd9a7e3428b2e924fd1121e7d3f850e85bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7cc853c48babc65f1e3611af1e1948ac96db4a4e682a98b304005c70720f8f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0957e4662bd04946758abea6a1365bca3d80662a7e96c65a00a9537fee03255c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunServiceTraffic]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca3bf57545c00a6f605237007e31282d1632b6a195bd53031fb1687f10827fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997589da95b69f927a7419a1b61da234f5db0e45280ec18d4fa79eaa707c4482(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fb2961f824aaaa1c5cbd949e755fa5d22f967435257e5877a14dbc939f5c0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c6964517840588c01eaf7810ce645bb68bf2f2d6b03bb3d5a3fbcf1ff74cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3c36a8b87ccbc973eea499e9500bd17207f39f2a3846a65c64b556372649f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe92d6516f1d02e2f080fe16a2cafb3afb598873041b5413b8b50f9d5247f2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunServiceTraffic]],
) -> None:
    """Type checking stubs"""
    pass
