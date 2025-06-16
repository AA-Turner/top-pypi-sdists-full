r'''
# `google_cloud_run_service`

Refer to the Terraform Registry for docs: [`google_cloud_run_service`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service).
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


class GoogleCloudRunService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service google_cloud_run_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        autogenerate_revision_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Union["GoogleCloudRunServiceMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        template: typing.Optional[typing.Union["GoogleCloudRunServiceTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudRunServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTraffic", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service google_cloud_run_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the cloud run instance. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#location GoogleCloudRunService#location}
        :param name: Name must be unique within a Google Cloud project and region. Is required when creating resources. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param autogenerate_revision_name: If set to 'true', the revision name (template.metadata.name) will be omitted and autogenerated by Cloud Run. This cannot be set to 'true' while 'template.metadata.name' is also set. (For legacy support, if 'template.metadata.name' is unset in state while this field is set to false, the revision name will still autogenerate.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#autogenerate_revision_name GoogleCloudRunService#autogenerate_revision_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#id GoogleCloudRunService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#metadata GoogleCloudRunService#metadata}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#project GoogleCloudRunService#project}.
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#template GoogleCloudRunService#template}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeouts GoogleCloudRunService#timeouts}
        :param traffic: traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#traffic GoogleCloudRunService#traffic}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d2ed89fd467086f78cbcbbb34afe5b23f929335d3471637dbfe0051c5e309c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudRunServiceConfig(
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
        '''Generates CDKTF code for importing a GoogleCloudRunService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudRunService to import.
        :param import_from_id: The id of the existing GoogleCloudRunService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudRunService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e65d7fe6f0669122d0ec5e1fc4ae88147026bde960426d1106a528ccd13715)
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
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations **Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation keys to configure features on a Service: - 'run.googleapis.com/binary-authorization-breakglass' sets the `Binary Authorization breakglass <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--breakglass>`_. - 'run.googleapis.com/binary-authorization' sets the `Binary Authorization <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--binary-authorization>`_. - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API. - 'run.googleapis.com/custom-audiences' sets the `custom audiences <https://cloud.google.com/sdk/gcloud/reference/alpha/run/deploy#--add-custom-audiences>`_ that can be used in the audience field of ID token for authenticated requests. - 'run.googleapis.com/description' sets a user defined description for the Service. - 'run.googleapis.com/ingress' sets the `ingress settings <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--ingress>`_ for the Service. For example, '"run.googleapis.com/ingress" = "all"'. - 'run.googleapis.com/launch-stage' sets the `launch stage <https://cloud.google.com/run/docs/troubleshooting#launch-stage-validation>`_ when a preview feature is used. For example, '"run.googleapis.com/launch-stage": "BETA"' - 'run.googleapis.com/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min>`_ of the Service. - 'run.googleapis.com/scalingMode' sets the type of scaling mode for the service. The supported values for scaling mode are "manual" and "automatic". If not provided, it defaults to "automatic". - 'run.googleapis.com/manualInstanceCount' sets the total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#annotations GoogleCloudRunService#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and routes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#labels GoogleCloudRunService#labels}
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#namespace GoogleCloudRunService#namespace}
        '''
        value = GoogleCloudRunServiceMetadata(
            annotations=annotations, labels=labels, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        metadata: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        spec: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#metadata GoogleCloudRunService#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#spec GoogleCloudRunService#spec}
        '''
        value = GoogleCloudRunServiceTemplate(metadata=metadata, spec=spec)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#create GoogleCloudRunService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#delete GoogleCloudRunService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#update GoogleCloudRunService#update}.
        '''
        value = GoogleCloudRunServiceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTraffic")
    def put_traffic(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTraffic", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5870d9097d9921e96e26fa7c92c58fc9c5fc2b14367fbaf1b4bfbaa0ca747f)
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
    def metadata(self) -> "GoogleCloudRunServiceMetadataOutputReference":
        return typing.cast("GoogleCloudRunServiceMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleCloudRunServiceStatusList":
        return typing.cast("GoogleCloudRunServiceStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "GoogleCloudRunServiceTemplateOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudRunServiceTimeoutsOutputReference":
        return typing.cast("GoogleCloudRunServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="traffic")
    def traffic(self) -> "GoogleCloudRunServiceTrafficList":
        return typing.cast("GoogleCloudRunServiceTrafficList", jsii.get(self, "traffic"))

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
    def metadata_input(self) -> typing.Optional["GoogleCloudRunServiceMetadata"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceMetadata"], jsii.get(self, "metadataInput"))

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
    def template_input(self) -> typing.Optional["GoogleCloudRunServiceTemplate"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudRunServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudRunServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficInput")
    def traffic_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTraffic"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTraffic"]]], jsii.get(self, "trafficInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__025e85fb396c347e68555afa8720000ffe54ac46508ce4608b8a72027288283e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autogenerateRevisionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5323fbfe7fed4c6ddc549ed2faf70a94f60a08c45693cc0ddb6b9250b97b4bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf461d942c56db368e6a729c96b21812ceb58cc26d55a7aa0390c2725079ff80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbe006108d3f4ac61a6f1c7ccac220eb53131413e8fe2366e0c35bdeacecbc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d0cd912443862a5d596e6d113c93b7e7855c9bb7630296960a86bcebeff042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceConfig",
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
class GoogleCloudRunServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Optional[typing.Union["GoogleCloudRunServiceMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        template: typing.Optional[typing.Union["GoogleCloudRunServiceTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudRunServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTraffic", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the cloud run instance. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#location GoogleCloudRunService#location}
        :param name: Name must be unique within a Google Cloud project and region. Is required when creating resources. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param autogenerate_revision_name: If set to 'true', the revision name (template.metadata.name) will be omitted and autogenerated by Cloud Run. This cannot be set to 'true' while 'template.metadata.name' is also set. (For legacy support, if 'template.metadata.name' is unset in state while this field is set to false, the revision name will still autogenerate.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#autogenerate_revision_name GoogleCloudRunService#autogenerate_revision_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#id GoogleCloudRunService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#metadata GoogleCloudRunService#metadata}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#project GoogleCloudRunService#project}.
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#template GoogleCloudRunService#template}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeouts GoogleCloudRunService#timeouts}
        :param traffic: traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#traffic GoogleCloudRunService#traffic}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = GoogleCloudRunServiceMetadata(**metadata)
        if isinstance(template, dict):
            template = GoogleCloudRunServiceTemplate(**template)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudRunServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621f0e5d33a9e3443fdbac725be17560a7ea5d3b43fc300198b83bcea0a129f1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#location GoogleCloudRunService#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autogenerate_revision_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', the revision name (template.metadata.name) will be omitted and autogenerated by Cloud Run. This cannot be set to 'true' while 'template.metadata.name' is also set. (For legacy support, if 'template.metadata.name' is unset in state while this field is set to false, the revision name will still autogenerate.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#autogenerate_revision_name GoogleCloudRunService#autogenerate_revision_name}
        '''
        result = self._values.get("autogenerate_revision_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#id GoogleCloudRunService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional["GoogleCloudRunServiceMetadata"]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#metadata GoogleCloudRunService#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["GoogleCloudRunServiceMetadata"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#project GoogleCloudRunService#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional["GoogleCloudRunServiceTemplate"]:
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#template GoogleCloudRunService#template}
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplate"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudRunServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeouts GoogleCloudRunService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTimeouts"], result)

    @builtins.property
    def traffic(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTraffic"]]]:
        '''traffic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#traffic GoogleCloudRunService#traffic}
        '''
        result = self._values.get("traffic")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTraffic"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "labels": "labels",
        "namespace": "namespace",
    },
)
class GoogleCloudRunServiceMetadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations **Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation keys to configure features on a Service: - 'run.googleapis.com/binary-authorization-breakglass' sets the `Binary Authorization breakglass <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--breakglass>`_. - 'run.googleapis.com/binary-authorization' sets the `Binary Authorization <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--binary-authorization>`_. - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API. - 'run.googleapis.com/custom-audiences' sets the `custom audiences <https://cloud.google.com/sdk/gcloud/reference/alpha/run/deploy#--add-custom-audiences>`_ that can be used in the audience field of ID token for authenticated requests. - 'run.googleapis.com/description' sets a user defined description for the Service. - 'run.googleapis.com/ingress' sets the `ingress settings <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--ingress>`_ for the Service. For example, '"run.googleapis.com/ingress" = "all"'. - 'run.googleapis.com/launch-stage' sets the `launch stage <https://cloud.google.com/run/docs/troubleshooting#launch-stage-validation>`_ when a preview feature is used. For example, '"run.googleapis.com/launch-stage": "BETA"' - 'run.googleapis.com/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min>`_ of the Service. - 'run.googleapis.com/scalingMode' sets the type of scaling mode for the service. The supported values for scaling mode are "manual" and "automatic". If not provided, it defaults to "automatic". - 'run.googleapis.com/manualInstanceCount' sets the total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#annotations GoogleCloudRunService#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and routes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#labels GoogleCloudRunService#labels}
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#namespace GoogleCloudRunService#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172b04faf5ad0aff248612878a41de11a00ab28bbd510a19e74879f75b46356d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#annotations GoogleCloudRunService#annotations}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#labels GoogleCloudRunService#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''In Cloud Run the namespace must be equal to either the project ID or project number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#namespace GoogleCloudRunService#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a12e712f09473f6ad952f7dede80f0e0bcaae147642cb4b4843f38fb648d4cb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c2d44472ec1d5d266449823860c4eb634ebb420e779ec73cb401c631dc94527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f723f4d5f3987a32ca3fd20fa1f717a7714fffb05fae4913b7a3df51907ed2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546f92be2f03f17c142b3ebc0fe6a7ae06ed2dd041033b67f5612a0e083b07a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunServiceMetadata]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096c890e07e6557cf4bfd6ce78db8f0bee601662865e3ae4cae28ee4a2959437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudRunServiceStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudRunServiceStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a1e57dde0b295368fd3fd1adc9262087756d4edb60c08e9c8acaf8bea8145af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195f0d8a18a89134bbdceca850a6778dcd8c89e7cca6e23a494e636e9bff1684)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b54e086878c84c9ec53891f338e79d2766860c7df1d442a4b92ffe675472b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68cb7469aa80fc6170e885578d6c3c9c5a544166dd8f68cd8239e26cb70ec047)
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
            type_hints = typing.get_type_hints(_typecheckingstub__144db441a6b0fb33cb17077e8904bc4a1ab7c28a59d3c42fbbbe7b7c6384c194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b95334158a78302a4a43e0b811231fab2c43e123f7afaa7204b8a749fb88fa16)
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
    def internal_value(self) -> typing.Optional[GoogleCloudRunServiceStatusConditions]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff96f10301e776bebefc369c23b106acbe2b2edef741145de1d6e9a0052ac31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1da3237a8281fc48cf196d99506c6da7be77e7c31ebe91455e201696a594cb50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleCloudRunServiceStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9bf74c7c218b33827d664d1e3e86be2245834c6e82d1b57146e9c6290f67c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50c9b1617939d6e816d6cd1e13f247e2eb121858790de63cdb3fd4b48960c5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aef103dbde9f380d2299d1c95d50d381fb098b6f3c0c4340db8fff48f2121de8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bc81790e818619180451db51fc749da2b4cf05000d74ac0c372ab6e320e4f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e4d5254b207a403f61b1559ca77e6a399d4e5634213ca9a42aba121009788f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GoogleCloudRunServiceStatusConditionsList:
        return typing.cast(GoogleCloudRunServiceStatusConditionsList, jsii.get(self, "conditions"))

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
    def traffic(self) -> "GoogleCloudRunServiceStatusTrafficList":
        return typing.cast("GoogleCloudRunServiceStatusTrafficList", jsii.get(self, "traffic"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunServiceStatus]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cbeb816148467141bd3adc31afa13dddecf45e64149a915aaaac0e0ffccf0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatusTraffic",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudRunServiceStatusTraffic:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceStatusTraffic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceStatusTrafficList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatusTrafficList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__417a720633a30b70b0027ea9a1ca0b9b8fa3fc5727d9d459557ce97cd92f9092)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceStatusTrafficOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ece676bbab1d48812995fd9a0417dd2a4c9992fc0ef132d0e98d3313900334)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceStatusTrafficOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99fd5e31a7777aad452c35247e90196430c2a935ff60b6a4218b4d54593a346)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f293e0e5318b25b67859f6c2d461472b7576f9dcf76e831f518dea7bf6d079dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ea6870819437d6cff3cfdfb261171546e4f765a1f33d1a268bf59badcef9c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceStatusTrafficOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceStatusTrafficOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8077b170a04ff65f843142dd0b2b047f43b6468e2f940834f99fcad6796e24ee)
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
    def internal_value(self) -> typing.Optional[GoogleCloudRunServiceStatusTraffic]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceStatusTraffic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceStatusTraffic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d03b2bd8fdc4e747ac1d7e5be836438938a9dc7a874eaa4b639aa699374f4d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplate",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata", "spec": "spec"},
)
class GoogleCloudRunServiceTemplate:
    def __init__(
        self,
        *,
        metadata: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        spec: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#metadata GoogleCloudRunService#metadata}
        :param spec: spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#spec GoogleCloudRunService#spec}
        '''
        if isinstance(metadata, dict):
            metadata = GoogleCloudRunServiceTemplateMetadata(**metadata)
        if isinstance(spec, dict):
            spec = GoogleCloudRunServiceTemplateSpec(**spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78dee0b856ac0265d54533a853d79a452b45e196be04024dc42f25d85ba31b0)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata
        if spec is not None:
            self._values["spec"] = spec

    @builtins.property
    def metadata(self) -> typing.Optional["GoogleCloudRunServiceTemplateMetadata"]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#metadata GoogleCloudRunService#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateMetadata"], result)

    @builtins.property
    def spec(self) -> typing.Optional["GoogleCloudRunServiceTemplateSpec"]:
        '''spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#spec GoogleCloudRunService#spec}
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class GoogleCloudRunServiceTemplateMetadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations **Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation keys to configure features on a Revision template: - 'autoscaling.knative.dev/maxScale' sets the `maximum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--max-instances>`_ of the Revision to run. - 'autoscaling.knative.dev/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min-instances>`_ of the Revision to run. - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API. - 'run.googleapis.com/cloudsql-instances' sets the `Cloud SQL instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--add-cloudsql-instances>`_ the Revision connects to. - 'run.googleapis.com/cpu-throttling' sets whether to throttle the CPU when the container is not actively serving requests. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-throttling. - 'run.googleapis.com/encryption-key-shutdown-hours' sets the number of hours to wait before an automatic shutdown server after CMEK key revocation is detected. - 'run.googleapis.com/encryption-key' sets the `CMEK key <https://cloud.google.com/run/docs/securing/using-cmek>`_ reference to encrypt the container with. - 'run.googleapis.com/execution-environment' sets the `execution environment <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--execution-environment>`_ where the application will run. - 'run.googleapis.com/post-key-revocation-action-type' sets the `action type <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--post-key-revocation-action-type>`_ after CMEK key revocation. - 'run.googleapis.com/secrets' sets a list of key-value pairs to set as `secrets <https://cloud.google.com/run/docs/configuring/secrets#yaml>`_. - 'run.googleapis.com/sessionAffinity' sets whether to enable `session affinity <https://cloud.google.com/sdk/gcloud/reference/beta/run/deploy#--%5Bno-%5Dsession-affinity>`_ for connections to the Revision. - 'run.googleapis.com/startup-cpu-boost' sets whether to allocate extra CPU to containers on startup. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-boost. - 'run.googleapis.com/network-interfaces' sets `Direct VPC egress <https://cloud.google.com/run/docs/configuring/vpc-direct-vpc#yaml>`_ for the Revision. - 'run.googleapis.com/vpc-access-connector' sets a `VPC connector <https://cloud.google.com/run/docs/configuring/connecting-vpc#terraform_1>`_ for the Revision. - 'run.googleapis.com/vpc-access-egress' sets the outbound traffic to send through the VPC connector for this resource. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--vpc-egress. - 'run.googleapis.com/gpu-zonal-redundancy-disabled' sets `GPU zonal redundancy <https://cloud.google.com/run/docs/configuring/services/gpu-zonal-redundancy>`_ for the Revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#annotations GoogleCloudRunService#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#labels GoogleCloudRunService#labels}
        :param name: Name must be unique within a Google Cloud project and region. Is required when creating resources. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. It will default to the resource's project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#namespace GoogleCloudRunService#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2a5844ac50a2823b9649917655a46ff7fff58156c875a348dc4e0bc9f2bee5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#annotations GoogleCloudRunService#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#labels GoogleCloudRunService#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name must be unique within a Google Cloud project and region.

        Is required when creating resources. Name is primarily intended
        for creation idempotence and configuration definition. Cannot be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''In Cloud Run the namespace must be equal to either the project ID or project number.

        It will default to the resource's project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#namespace GoogleCloudRunService#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f966ed3c569a31290819c18afea701826ee7c1c51cdbe8d30d00e53494d4e8a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cee234fa995a9014bf4f91086fe570d74e0bd9d77f169214ef07100097bb42e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3877b97b55cdd4db2bf4db0586a9eaaf8da2430d02dafbb58f30af15d8094091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe41ce4f97143d9ddcbc64040d343c27e601a9498e4e3b346216ca760a40fc6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1c18984a046b8506454a65cc53b10e2d71b1e981fd80dfd1c7c01f49258edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunServiceTemplateMetadata]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3b1b74fd9d7cc6cdaa26c05c93c59f2174c451e99dc0a86f2a7deb1bf3d3ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48ea92773a84b30e35fc1ad6b6707d269b648d8eb0dd4c7759eedd26817b7cc7)
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
        :param annotations: Annotations is a key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations **Note**: The Cloud Run API may add additional annotations that were not provided in your config. If terraform plan shows a diff where a server-side annotation is added, you can add it to your config or apply the lifecycle.ignore_changes rule to the metadata.0.annotations field. Annotations with 'run.googleapis.com/' and 'autoscaling.knative.dev' are restricted. Use the following annotation keys to configure features on a Revision template: - 'autoscaling.knative.dev/maxScale' sets the `maximum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--max-instances>`_ of the Revision to run. - 'autoscaling.knative.dev/minScale' sets the `minimum number of container instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--min-instances>`_ of the Revision to run. - 'run.googleapis.com/client-name' sets the client name calling the Cloud Run API. - 'run.googleapis.com/cloudsql-instances' sets the `Cloud SQL instances <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--add-cloudsql-instances>`_ the Revision connects to. - 'run.googleapis.com/cpu-throttling' sets whether to throttle the CPU when the container is not actively serving requests. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-throttling. - 'run.googleapis.com/encryption-key-shutdown-hours' sets the number of hours to wait before an automatic shutdown server after CMEK key revocation is detected. - 'run.googleapis.com/encryption-key' sets the `CMEK key <https://cloud.google.com/run/docs/securing/using-cmek>`_ reference to encrypt the container with. - 'run.googleapis.com/execution-environment' sets the `execution environment <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--execution-environment>`_ where the application will run. - 'run.googleapis.com/post-key-revocation-action-type' sets the `action type <https://cloud.google.com/sdk/gcloud/reference/run/deploy#--post-key-revocation-action-type>`_ after CMEK key revocation. - 'run.googleapis.com/secrets' sets a list of key-value pairs to set as `secrets <https://cloud.google.com/run/docs/configuring/secrets#yaml>`_. - 'run.googleapis.com/sessionAffinity' sets whether to enable `session affinity <https://cloud.google.com/sdk/gcloud/reference/beta/run/deploy#--%5Bno-%5Dsession-affinity>`_ for connections to the Revision. - 'run.googleapis.com/startup-cpu-boost' sets whether to allocate extra CPU to containers on startup. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--[no-]cpu-boost. - 'run.googleapis.com/network-interfaces' sets `Direct VPC egress <https://cloud.google.com/run/docs/configuring/vpc-direct-vpc#yaml>`_ for the Revision. - 'run.googleapis.com/vpc-access-connector' sets a `VPC connector <https://cloud.google.com/run/docs/configuring/connecting-vpc#terraform_1>`_ for the Revision. - 'run.googleapis.com/vpc-access-egress' sets the outbound traffic to send through the VPC connector for this resource. See https://cloud.google.com/sdk/gcloud/reference/run/deploy#--vpc-egress. - 'run.googleapis.com/gpu-zonal-redundancy-disabled' sets `GPU zonal redundancy <https://cloud.google.com/run/docs/configuring/services/gpu-zonal-redundancy>`_ for the Revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#annotations GoogleCloudRunService#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#labels GoogleCloudRunService#labels}
        :param name: Name must be unique within a Google Cloud project and region. Is required when creating resources. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param namespace: In Cloud Run the namespace must be equal to either the project ID or project number. It will default to the resource's project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#namespace GoogleCloudRunService#namespace}
        '''
        value = GoogleCloudRunServiceTemplateMetadata(
            annotations=annotations, labels=labels, name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        container_concurrency: typing.Optional[jsii.Number] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param container_concurrency: ContainerConcurrency specifies the maximum allowed in-flight (concurrent) requests per container of the Revision. If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#container_concurrency GoogleCloudRunService#container_concurrency}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#containers GoogleCloudRunService#containers}
        :param node_selector: Node Selector describes the hardware requirements of the resources. Use the following node selector keys to configure features on a Revision: - 'run.googleapis.com/accelerator' sets the `type of GPU <https://cloud.google.com/run/docs/configuring/services/gpu>`_ required by the Revision to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#node_selector GoogleCloudRunService#node_selector}
        :param service_account_name: Email address of the IAM service account associated with the revision of the service. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service_account_name GoogleCloudRunService#service_account_name}
        :param timeout_seconds: TimeoutSeconds holds the max duration the instance is allowed for responding to a request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#volumes GoogleCloudRunService#volumes}
        '''
        value = GoogleCloudRunServiceTemplateSpec(
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
    def metadata(self) -> GoogleCloudRunServiceTemplateMetadataOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateMetadataOutputReference, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> "GoogleCloudRunServiceTemplateSpecOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[GoogleCloudRunServiceTemplateMetadata]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateMetadata], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(self) -> typing.Optional["GoogleCloudRunServiceTemplateSpec"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpec"], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunServiceTemplate]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3466fdb9d56c58beb5514af4ffbbc4452ae33ecec6b7d09d0c48c916976997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpec",
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
class GoogleCloudRunServiceTemplateSpec:
    def __init__(
        self,
        *,
        container_concurrency: typing.Optional[jsii.Number] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param container_concurrency: ContainerConcurrency specifies the maximum allowed in-flight (concurrent) requests per container of the Revision. If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#container_concurrency GoogleCloudRunService#container_concurrency}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#containers GoogleCloudRunService#containers}
        :param node_selector: Node Selector describes the hardware requirements of the resources. Use the following node selector keys to configure features on a Revision: - 'run.googleapis.com/accelerator' sets the `type of GPU <https://cloud.google.com/run/docs/configuring/services/gpu>`_ required by the Revision to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#node_selector GoogleCloudRunService#node_selector}
        :param service_account_name: Email address of the IAM service account associated with the revision of the service. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service_account_name GoogleCloudRunService#service_account_name}
        :param timeout_seconds: TimeoutSeconds holds the max duration the instance is allowed for responding to a request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#volumes GoogleCloudRunService#volumes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493e99862a83e30f9ae0dfc0bc8f31dc4c5fa4201a8bd5234a3f427b2cb546ca)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#container_concurrency GoogleCloudRunService#container_concurrency}
        '''
        result = self._values.get("container_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def containers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainers"]]]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#containers GoogleCloudRunService#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainers"]]], result)

    @builtins.property
    def node_selector(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Node Selector describes the hardware requirements of the resources.

        Use the following node selector keys to configure features on a Revision:

        - 'run.googleapis.com/accelerator' sets the `type of GPU <https://cloud.google.com/run/docs/configuring/services/gpu>`_ required by the Revision to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#node_selector GoogleCloudRunService#node_selector}
        '''
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        '''Email address of the IAM service account associated with the revision of the service.

        The service account represents the identity of the running revision,
        and determines what permissions the revision has. If not provided, the revision
        will use the project's default service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service_account_name GoogleCloudRunService#service_account_name}
        '''
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''TimeoutSeconds holds the max duration the instance is allowed for responding to a request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#volumes GoogleCloudRunService#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecVolumes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainers",
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
class GoogleCloudRunServiceTemplateSpecContainers:
    def __init__(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        env_from: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvFrom", typing.Dict[builtins.str, typing.Any]]]]] = None,
        liveness_probe: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersLivenessProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainersPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersResources", typing.Dict[builtins.str, typing.Any]]] = None,
        startup_probe: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersStartupProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: Docker image name. This is most often a reference to a container located in the container registry, such as gcr.io/cloudrun/hello. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#image GoogleCloudRunService#image}
        :param args: Arguments to the entrypoint. The docker image's CMD is used if this is not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#args GoogleCloudRunService#args}
        :param command: Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#command GoogleCloudRunService#command}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#env GoogleCloudRunService#env}
        :param env_from: env_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#env_from GoogleCloudRunService#env_from}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#liveness_probe GoogleCloudRunService#liveness_probe}
        :param name: Name of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#ports GoogleCloudRunService#ports}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#resources GoogleCloudRunService#resources}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#startup_probe GoogleCloudRunService#startup_probe}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#volume_mounts GoogleCloudRunService#volume_mounts}
        :param working_dir: Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#working_dir GoogleCloudRunService#working_dir}
        '''
        if isinstance(liveness_probe, dict):
            liveness_probe = GoogleCloudRunServiceTemplateSpecContainersLivenessProbe(**liveness_probe)
        if isinstance(resources, dict):
            resources = GoogleCloudRunServiceTemplateSpecContainersResources(**resources)
        if isinstance(startup_probe, dict):
            startup_probe = GoogleCloudRunServiceTemplateSpecContainersStartupProbe(**startup_probe)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e3a4c2ebcf60b389d782ff1b2688da08afc9475faa9d0953c15155f4abbba0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#image GoogleCloudRunService#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to the entrypoint. The docker image's CMD is used if this is not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#args GoogleCloudRunService#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#command GoogleCloudRunService#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#env GoogleCloudRunService#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersEnv"]]], result)

    @builtins.property
    def env_from(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersEnvFrom"]]]:
        '''env_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#env_from GoogleCloudRunService#env_from}
        '''
        result = self._values.get("env_from")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersEnvFrom"]]], result)

    @builtins.property
    def liveness_probe(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersLivenessProbe"]:
        '''liveness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#liveness_probe GoogleCloudRunService#liveness_probe}
        '''
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersLivenessProbe"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersPorts"]]]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#ports GoogleCloudRunService#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersPorts"]]], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#resources GoogleCloudRunService#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersResources"], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbe"]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#startup_probe GoogleCloudRunService#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbe"], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#volume_mounts GoogleCloudRunService#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersVolumeMounts"]]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#working_dir GoogleCloudRunService#working_dir}
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "value_from": "valueFrom"},
)
class GoogleCloudRunServiceTemplateSpecContainersEnv:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        value_from: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param value: Defaults to "". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#value GoogleCloudRunService#value}
        :param value_from: value_from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#value_from GoogleCloudRunService#value_from}
        '''
        if isinstance(value_from, dict):
            value_from = GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom(**value_from)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af5176b492eed4d50ba285f4435198dbe2db95e6940ba25020ecc45e4ed08ff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Defaults to "".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#value GoogleCloudRunService#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_from(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom"]:
        '''value_from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#value_from GoogleCloudRunService#value_from}
        '''
        result = self._values.get("value_from")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFrom",
    jsii_struct_bases=[],
    name_mapping={
        "config_map_ref": "configMapRef",
        "prefix": "prefix",
        "secret_ref": "secretRef",
    },
)
class GoogleCloudRunServiceTemplateSpecContainersEnvFrom:
    def __init__(
        self,
        *,
        config_map_ref: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef", typing.Dict[builtins.str, typing.Any]]] = None,
        prefix: typing.Optional[builtins.str] = None,
        secret_ref: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_map_ref: config_map_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#config_map_ref GoogleCloudRunService#config_map_ref}
        :param prefix: An optional identifier to prepend to each key in the ConfigMap. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#prefix GoogleCloudRunService#prefix}
        :param secret_ref: secret_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret_ref GoogleCloudRunService#secret_ref}
        '''
        if isinstance(config_map_ref, dict):
            config_map_ref = GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef(**config_map_ref)
        if isinstance(secret_ref, dict):
            secret_ref = GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef(**secret_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9346af924680ba4d67a00f4ec2aed80d910c087a23755d4e051e6b0168f15844)
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
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef"]:
        '''config_map_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#config_map_ref GoogleCloudRunService#config_map_ref}
        '''
        result = self._values.get("config_map_ref")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef"], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''An optional identifier to prepend to each key in the ConfigMap.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#prefix GoogleCloudRunService#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_ref(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef"]:
        '''secret_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret_ref GoogleCloudRunService#secret_ref}
        '''
        result = self._values.get("secret_ref")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersEnvFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef",
    jsii_struct_bases=[],
    name_mapping={
        "local_object_reference": "localObjectReference",
        "optional": "optional",
    },
)
class GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef:
    def __init__(
        self,
        *,
        local_object_reference: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference", typing.Dict[builtins.str, typing.Any]]] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_object_reference: local_object_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#local_object_reference GoogleCloudRunService#local_object_reference}
        :param optional: Specify whether the ConfigMap must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#optional GoogleCloudRunService#optional}
        '''
        if isinstance(local_object_reference, dict):
            local_object_reference = GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference(**local_object_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bce12b90443c16bbf6b5831225361ae6f7b64bb65b8ce7d163d28b921f40961)
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
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference"]:
        '''local_object_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#local_object_reference GoogleCloudRunService#local_object_reference}
        '''
        result = self._values.get("local_object_reference")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference"], result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify whether the ConfigMap must be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#optional GoogleCloudRunService#optional}
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a1600870d1597ca8143a1e2fe38987eaa16af80c130ee103da0851aefbd937)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ee01f998c30534e8b452be315302864da79694616e915a7f8ab9def982e9466)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe104e9ce6f766fd4ce395e32213bdf59539188ee4e03e2a36d95c6b64ebf626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff4022060b1526925b219cf53ceb5c35708ff33291ddb89c7a5f9e0a7d68f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eb06e27930246d6e2919ad1bf4e270efd70c50c87728a3affa3b307587dc1f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalObjectReference")
    def put_local_object_reference(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference(
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
    ) -> GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference, jsii.get(self, "localObjectReference"))

    @builtins.property
    @jsii.member(jsii_name="localObjectReferenceInput")
    def local_object_reference_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference], jsii.get(self, "localObjectReferenceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__641a84c94554008804c632221ceffef6ea2c1064c59227d9354800eef0e3f68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe76324a7ecc40409a81793ff8455d5fb9eb266b970aa6b6c71fd0fe5e23b2a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersEnvFromList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bc1b653940d1e3d1ab2c4922edd459febdb74d70c3351e2fc8c15a945ae3f4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersEnvFromOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e36ce4cb15693e31e0fd7b9c3bac887ab8c011bdacdc0c80c202164e0ff7a26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersEnvFromOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63c4c366e212f1d2cee7cbf36a56bc70bc275afdac877264dc26a684efb759f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30bca170b8124ff1aa804e94445d80f41405f51210d7280d8676cd8287257e52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__206e1a8bda20b35d06d5fa5be4c6819b9714bca6018083e3b973db4dd14393e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnvFrom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnvFrom]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnvFrom]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5e91fb2cd814d088fd5661e332646cebce4354e7b1de26bd4e4b56627864fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersEnvFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04f5f75cd2d88f9678cecb61e0e089924fc3d33a8e72f8b97645c6c6d98bfe6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConfigMapRef")
    def put_config_map_ref(
        self,
        *,
        local_object_reference: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference, typing.Dict[builtins.str, typing.Any]]] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_object_reference: local_object_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#local_object_reference GoogleCloudRunService#local_object_reference}
        :param optional: Specify whether the ConfigMap must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#optional GoogleCloudRunService#optional}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef(
            local_object_reference=local_object_reference, optional=optional
        )

        return typing.cast(None, jsii.invoke(self, "putConfigMapRef", [value]))

    @jsii.member(jsii_name="putSecretRef")
    def put_secret_ref(
        self,
        *,
        local_object_reference: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference", typing.Dict[builtins.str, typing.Any]]] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_object_reference: local_object_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#local_object_reference GoogleCloudRunService#local_object_reference}
        :param optional: Specify whether the Secret must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#optional GoogleCloudRunService#optional}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef(
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
    ) -> GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference, jsii.get(self, "configMapRef"))

    @builtins.property
    @jsii.member(jsii_name="secretRef")
    def secret_ref(
        self,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference", jsii.get(self, "secretRef"))

    @builtins.property
    @jsii.member(jsii_name="configMapRefInput")
    def config_map_ref_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef], jsii.get(self, "configMapRefInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="secretRefInput")
    def secret_ref_input(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef"], jsii.get(self, "secretRefInput"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fdcbd1bf65973b3a591e5a09fd12b55ab8c8d79784a2d1e157518f240b4284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersEnvFrom]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersEnvFrom]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersEnvFrom]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a461bf66497c831a69ec6f7e647d6cd0316e2aeb4238376bcba5d02414a66ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef",
    jsii_struct_bases=[],
    name_mapping={
        "local_object_reference": "localObjectReference",
        "optional": "optional",
    },
)
class GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef:
    def __init__(
        self,
        *,
        local_object_reference: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference", typing.Dict[builtins.str, typing.Any]]] = None,
        optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_object_reference: local_object_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#local_object_reference GoogleCloudRunService#local_object_reference}
        :param optional: Specify whether the Secret must be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#optional GoogleCloudRunService#optional}
        '''
        if isinstance(local_object_reference, dict):
            local_object_reference = GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference(**local_object_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906e77e68683ea2c419e9f46945299f514e89d12874f6ff28e8e3253ae0dd0b4)
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
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference"]:
        '''local_object_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#local_object_reference GoogleCloudRunService#local_object_reference}
        '''
        result = self._values.get("local_object_reference")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference"], result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify whether the Secret must be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#optional GoogleCloudRunService#optional}
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce341d1a0223f46d6463ceecd6052c77fbbf7d7434cefd8d2a3744b872028291)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__643e53f61dcf476f381278600e127216e8e51aecaf8a7a772f7ac65959d55d0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d92b594ba857bfefb11d87cb5d2afd379267f1b3e0c3fbe910a7db6adff4a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0673e3b62872d777f076638712ffc476a17bc70cd2cc8cf7259ba55f0294d631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29dc902ced2b2144a6aca84cc3cf467c5b6a7b81d68184654d33367e9de3f52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalObjectReference")
    def put_local_object_reference(self, *, name: builtins.str) -> None:
        '''
        :param name: Name of the referent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference(
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
    ) -> GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference, jsii.get(self, "localObjectReference"))

    @builtins.property
    @jsii.member(jsii_name="localObjectReferenceInput")
    def local_object_reference_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference], jsii.get(self, "localObjectReferenceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5ed9e0f0db5b58442d5619b1d0fc357c8af5e495c936ffeef6915dc6d73595d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6670f6b3b9baa1f09e32e9e9eea06d24917f6411e291237d71a700c12ddf302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6dd6471ebd4776131405cdb98f8468ac83cd0ecc912a9503a842d6cb062c224)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe200a5649008717a37282b1c1575b67f26d2393bdea94f2e3922d3117d20c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd42819ba9f293d4eab8967c39c836c0919176c9662718c8a6a6d6b93c34b8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__607fa1dc9ab499ac45bc122a245d754d541b9fb0b1cda27b250f8ceb500d7f45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1786fc2882d8f2b79320c202fb2bcc578e0469363bc0610c9c84f2b7fdb30108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543932251355235ec10ba4dcc406cc05c92861e98933090ca99d56e7e1f6375c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a06e76c3c896e778e692f0d52f823fe514f9fed6a104295dbc76e6a6c05290f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueFrom")
    def put_value_from(
        self,
        *,
        secret_key_ref: typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret_key_ref GoogleCloudRunService#secret_key_ref}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom(
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
    ) -> "GoogleCloudRunServiceTemplateSpecContainersEnvValueFromOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersEnvValueFromOutputReference", jsii.get(self, "valueFrom"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueFromInput")
    def value_from_input(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom"], jsii.get(self, "valueFromInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5f1319ecdf1e6a0fa0320f672e989eda55cc2d38692a80e3d7a9015f989f239c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1142ac7935e0cb0a9e11649beec82183941718d8a26b2717fe488d8b0b13a8e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9bce1191e0e30631bc569ce5d8bf0e8b3d767b03dcebdda6f8e16195d4e0b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom",
    jsii_struct_bases=[],
    name_mapping={"secret_key_ref": "secretKeyRef"},
)
class GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom:
    def __init__(
        self,
        *,
        secret_key_ref: typing.Union["GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret_key_ref GoogleCloudRunService#secret_key_ref}
        '''
        if isinstance(secret_key_ref, dict):
            secret_key_ref = GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef(**secret_key_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dcc1660a07f02665c71a333521f452fdfe1c29f425ad653aa8813f777b9673f)
            check_type(argname="argument secret_key_ref", value=secret_key_ref, expected_type=type_hints["secret_key_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_key_ref": secret_key_ref,
        }

    @builtins.property
    def secret_key_ref(
        self,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef":
        '''secret_key_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret_key_ref GoogleCloudRunService#secret_key_ref}
        '''
        result = self._values.get("secret_key_ref")
        assert result is not None, "Required property 'secret_key_ref' is missing"
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersEnvValueFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvValueFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e0c707fb7c39432723f4b17c74f4e77c1e69147dff36977b825434f3541e450)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretKeyRef")
    def put_secret_key_ref(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: A Cloud Secret Manager secret version. Must be 'latest' for the latest version or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#key GoogleCloudRunService#key}
        :param name: The name of the secret in Cloud Secret Manager. By default, the secret is assumed to be in the same project. If the secret is in another project, you must define an alias. An alias definition has the form: {alias}:projects/{project-id|project-number}/secrets/{secret-name}. If multiple alias definitions are needed, they must be separated by commas. The alias definitions must be set on the run.googleapis.com/secrets annotation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef(
            key=key, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putSecretKeyRef", [value]))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRef")
    def secret_key_ref(
        self,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference", jsii.get(self, "secretKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRefInput")
    def secret_key_ref_input(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef"], jsii.get(self, "secretKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ad54a06c5baadd22f830be7ccfa1d4b0c6f8a627cf7060664161e92306f859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name"},
)
class GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef:
    def __init__(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: A Cloud Secret Manager secret version. Must be 'latest' for the latest version or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#key GoogleCloudRunService#key}
        :param name: The name of the secret in Cloud Secret Manager. By default, the secret is assumed to be in the same project. If the secret is in another project, you must define an alias. An alias definition has the form: {alias}:projects/{project-id|project-number}/secrets/{secret-name}. If multiple alias definitions are needed, they must be separated by commas. The alias definitions must be set on the run.googleapis.com/secrets annotation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e60bf194288693289ded6b43c5abc6e6cab52d0aadc7e790c3a5a07b02acaa)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "name": name,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''A Cloud Secret Manager secret version. Must be 'latest' for the latest version or an integer for a specific version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#key GoogleCloudRunService#key}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e4cbd8ddfbde6abdbdeed6290acdb64c787ae879bdd9bd87b2157ef66cfd0b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2b12fa4c86f35bf8ced33631c9829bfa7e91ff3adf27eab25e82cb9a3a437ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce64953c3aa2b76ad6c6387d1ae5cce3a49b9900c559924e0ed0f18e5ab1327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903e46aac4200d48f55091be549ccd92b29788d943333333a026eabfde46e5f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4b4703f3b2cf05f37d85752c3993e80f36f74fbe0928036c37d7f1912493476)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2316c9d9380dea010c3c9589ddacf89e390dc70e76e98298f24cec6d26f66f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c712b83321bfd79a1529f9ec8b509dbb32abbf623dc084d1309581d6fef1056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22bc506e8d0aece04abdf9f53d83b5615aa37c62fbd299f5fa5ec1891d475111)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d5f2518bae68b0650d16afe0f4e23c4d1d36ae9dd88e2aa4e808cd7844e81c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356ccd795bb07ba784d439727710352aa5969547f941c4ac4082ef75358e56b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbe",
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
class GoogleCloudRunServiceTemplateSpecContainersLivenessProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#failure_threshold GoogleCloudRunService#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#grpc GoogleCloudRunService#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_get GoogleCloudRunService#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#initial_delay_seconds GoogleCloudRunService#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#period_seconds GoogleCloudRunService#period_seconds}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than period_seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet(**http_get)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34552097e70e2bfc7763acfdaf53059f1e59156e43f41ab4b16291d7bcea40d8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#failure_threshold GoogleCloudRunService#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#grpc GoogleCloudRunService#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_get GoogleCloudRunService#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value is 3600.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#initial_delay_seconds GoogleCloudRunService#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 3600.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#period_seconds GoogleCloudRunService#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600.
        Must be smaller than period_seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersLivenessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service GoogleCloudRunService#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b430be3aa8480d0fdad6e81186883dc8e47982080eff7b6008eb80529d2ce8f5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service GoogleCloudRunService#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fda182c9aeea79c9939cd5667dcbdbfb76322317df8141b7794f884d4eaa629f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b07abdae65ef45f03660a2aa052123206659d73a268eb1e859a659e5d22ba28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385c5ce4e0c5d8423cbd52f71b1db05391e002754450060c48cb06dc0f092cd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d548f0c915e531c9b27ce7f2d2ced3b6b8cd06e1aaac2c34a483fd294eccd86a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_headers GoogleCloudRunService#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52904953f3b3fbfe3a0bd01413cc3f77141b5f9af4d5065234a41841ee82b5e9)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_headers GoogleCloudRunService#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. If set, it should not be empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#value GoogleCloudRunService#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6bc91644e3f2a9c410ddf9de86e1db20125e2373d9ac82f43fc909a6419c36c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#value GoogleCloudRunService#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e12383e21c8b4e995faeaca18a7b956b5c2a3d839fdfc70ceefa8bd528fe443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79163fdb519c8392a4bb46b7a293f80f6c2657aa5a6a69fc655c9c1d96b904c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f1aced315f1bd8a719b9738e55f80d4cefb07767606c52bebac214ca2a149a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3964bf8d6aefcb69d13fc583bcde040c4e620235d2a5d900ebafe31c37e9717e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2be1f962887cfd094c5c7a4284223b930d697af034e4ea0de5b322b580a7ba47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3843c7e8cecec42836e465eb9a30f9ff7d8afb103d09059a844ab978d2158e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__906ddb98a550fcfa188610fd8b07eb8fdf75473a44641c0b44c807f225f5d90e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33b50e5069cbd076dcb3e579968d11a6a6b5566cf4e3d15e8d5fb2d78b7fadb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89a4070a31492a2899c72f45b2ba75b65e89926cc428f0e0f77acfa58f22a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39aa053b5f393c1b85325aff6baea7b261b76f0c06cde6fcf96256bbeb4e8129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be941effed564bc42ee5a0094ed822b112a5cb82dc7b336a8a125c1b88fcc300)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b82d83ed925fa13306a24125eb24a9760784f0047daef6ccb270d9dd725a116)
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
    ) -> GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7f34a01448a3c67ba4ea2eea508acfdbdd24325600f0115bc3a4613082671639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7992a98edb90c774a4700631345cd51729137fdc0f2d25ddea996433e83dabee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948092c6602c9a5f2ef8cddef9eb0170987b7710a788d62e6abd937558a85b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersLivenessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersLivenessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8365283ed2fe6c4595f43be0ad142d709cb39c20c5b7b13712fec3a51f41307)
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
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service GoogleCloudRunService#service}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_headers GoogleCloudRunService#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet(
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
    ) -> GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet], jsii.get(self, "httpGetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b315e6eaf045f089ebd2a6cfc8e13f2e2dcbacbab61492d7bdfeb0f9f976a4a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee9f6e5b2adcb943a9be818b87413431bc05ba99996aede53b6b344f74543c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d564aadd6ad06e0c0debffa90a82ca6f97a718848a96b250ec2a16328053cd30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83fe56af9cea0c67754bf57639f9d242ed281c799f7146ece6ed9afbc683e522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbe]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac8d8253d6ba5afc4ac9f3af35966a5e03328b10c6f91bac6906eba5b6c8d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eea810ecc04592554b66dd07fc6b4df73350c4f33111147e64e8b66d3f2c2773)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4664ebbe0d56738e337b0ff1e9fa7fb2f6d400d252798457a50b2dd0ffdd5dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putEnvFrom")
    def put_env_from(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvFrom, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcd8935ac424fc4fddc620457ab9b4d0d695155c4de4e873168a10d2c754f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvFrom", [value]))

    @jsii.member(jsii_name="putLivenessProbe")
    def put_liveness_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#failure_threshold GoogleCloudRunService#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#grpc GoogleCloudRunService#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_get GoogleCloudRunService#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#initial_delay_seconds GoogleCloudRunService#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 3600. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#period_seconds GoogleCloudRunService#period_seconds}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than period_seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersLivenessProbe(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainersPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09933438689390b2f25f4dd110ae26cba35c76a1a5bebe28c60096be25023e3e)
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
        :param limits: Limits describes the maximum amount of compute resources allowed. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#limits GoogleCloudRunService#limits}
        :param requests: Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#requests GoogleCloudRunService#requests}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersResources(
            limits=limits, requests=requests
        )

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#failure_threshold GoogleCloudRunService#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#grpc GoogleCloudRunService#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_get GoogleCloudRunService#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#initial_delay_seconds GoogleCloudRunService#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#period_seconds GoogleCloudRunService#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#tcp_socket GoogleCloudRunService#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersStartupProbe(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95bcd488db6ee25922ca1764a1150942f2a079d73f20c58f239ad6ef3aa7fc66)
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
    def env(self) -> GoogleCloudRunServiceTemplateSpecContainersEnvList:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="envFrom")
    def env_from(self) -> GoogleCloudRunServiceTemplateSpecContainersEnvFromList:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersEnvFromList, jsii.get(self, "envFrom"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbe")
    def liveness_probe(
        self,
    ) -> GoogleCloudRunServiceTemplateSpecContainersLivenessProbeOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersLivenessProbeOutputReference, jsii.get(self, "livenessProbe"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> "GoogleCloudRunServiceTemplateSpecContainersPortsList":
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersPortsList", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersResourcesOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(
        self,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersStartupProbeOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersStartupProbeOutputReference", jsii.get(self, "startupProbe"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(
        self,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersVolumeMountsList":
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersVolumeMountsList", jsii.get(self, "volumeMounts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnvFrom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnvFrom]]], jsii.get(self, "envFromInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbeInput")
    def liveness_probe_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbe]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbe], jsii.get(self, "livenessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersPorts"]]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersResources"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="startupProbeInput")
    def startup_probe_input(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbe"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbe"], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__67df94ad8c7b7bb3529a308cc1ee11267c7de9fa81e4a25974aaefc1cd8769f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1ae95382e4f4a65bc8473de872a8c62cf77ff2efeddc4ecf1fb83e743c48c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185dee28fcd55098556ca1fce3c746f22a6500bb3b9cd6fe23ab48690b02e68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fe5d887e74a1b28925e6cca311fd66e25c802f8e75abd00f4bc21381040457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc647ee6445c6b4ef81ed330ba3ba0e46c373ebd6cd581ca4066b0afce79c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd7d00cf8d998eb32182707f0136002fac6c9f803e7116e9e5e412c50ef383f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersPorts",
    jsii_struct_bases=[],
    name_mapping={
        "container_port": "containerPort",
        "name": "name",
        "protocol": "protocol",
    },
)
class GoogleCloudRunServiceTemplateSpecContainersPorts:
    def __init__(
        self,
        *,
        container_port: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_port: Port number the container listens on. This must be a valid port number (between 1 and 65535). Defaults to "8080". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#container_port GoogleCloudRunService#container_port}
        :param name: If specified, used to specify which protocol to use. Allowed values are "http1" (HTTP/1) and "h2c" (HTTP/2 end-to-end). Defaults to "http1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param protocol: Protocol for port. Must be "TCP". Defaults to "TCP". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#protocol GoogleCloudRunService#protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30dc6f5d45c5ccb81c00cf9e8671983f91a8e599a32f9a66b51843454f57316e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#container_port GoogleCloudRunService#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''If specified, used to specify which protocol to use.

        Allowed values are "http1" (HTTP/1) and "h2c" (HTTP/2 end-to-end). Defaults to "http1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Protocol for port. Must be "TCP". Defaults to "TCP".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#protocol GoogleCloudRunService#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__088c14876441a7745c290972d232246718c63a377c9bb93d229b76c37ee53af3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7b2e3d39066236b06382c51d08a0b69caf0be65d59ede4ee92e1aa6244e969)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0abfdd454f63765013881bd9d33e69c51ec56b75e46101ba35a08e689644b4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a7855a729d4e0b346fd0caf7792efba3c52b17c2bfbb6676a50813eb7b9604c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c918915560777b0d44a3edc4e0a48daabc0b5aa351a0946e3050d23ae8ee700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c7b2773b1ca9e2ed64ac97c255bd4aea163e99889f2d1b91eae0b8fb4dd6ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee71737b923f6ccd05ad33d32069b59769caf45914e3f2108a94afc300c98289)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19f631d4bf988225c516da2595d1d76e96362d1f9a687425f848dcfe2a1ccb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800fe85c9f6e7f7ed28aa0bdcb1de05aa25030abf26e31ff0ce991bff2f0450e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d71f73a449bcdb584bfd0aade8f67df14f883b130a54ebd6bf1b45325b98d437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6505b145f1f462901ecf80315851332fd2e49b37efddd2e5046c3a2a9fc2a2ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "requests": "requests"},
)
class GoogleCloudRunServiceTemplateSpecContainersResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        requests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param limits: Limits describes the maximum amount of compute resources allowed. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#limits GoogleCloudRunService#limits}
        :param requests: Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#requests GoogleCloudRunService#requests}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe72a9029a3268bdd7356961ae6d3685ecdd93205092c73be3fe5fceca76d69)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#limits GoogleCloudRunService#limits}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#requests GoogleCloudRunService#requests}
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44dbe56401f9c091749c4283e27320df6506bd4d877c2b35f6de8260a9366c26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c692274612cecec9e0507291d358497e7ae1ccca5980a4e2cbcec1cb9de6bf66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requests")
    def requests(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requests"))

    @requests.setter
    def requests(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e0fbb50ebe5b112986bde32b5fc97a5c3a22c11425c9648c7f52cc88d470e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersResources]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3380cc00aed43ba31419146edd26b8b1a928ed03db26ff1b2f82fb33216625d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbe",
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
class GoogleCloudRunServiceTemplateSpecContainersStartupProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#failure_threshold GoogleCloudRunService#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#grpc GoogleCloudRunService#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_get GoogleCloudRunService#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#initial_delay_seconds GoogleCloudRunService#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#period_seconds GoogleCloudRunService#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#tcp_socket GoogleCloudRunService#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c251c5bf94c713ad0d63a368a6542b61207e866fe4d9818317025424375d5490)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#failure_threshold GoogleCloudRunService#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#grpc GoogleCloudRunService#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_get GoogleCloudRunService#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value is 240.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#initial_delay_seconds GoogleCloudRunService#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#period_seconds GoogleCloudRunService#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#tcp_socket GoogleCloudRunService#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600.
        Must be smaller than periodSeconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#timeout_seconds GoogleCloudRunService#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service GoogleCloudRunService#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88f4b37d4458c03bf2ba69fd5400df6b3da82447dc7770c8da620764db54461)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service GoogleCloudRunService#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbbcf8d7a3a54282ebe354ce5b20c9b37522a8901daa0aee817fbb6bba7ff8ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8af767a37f8b2ca852e6125c5c01272913b88e64e8ca05004d449af2c1d2b4d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b614477406a59a28b9764b6b09a56d20551fd020c410a0941f8d7fa9d6f596aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd1f4333be456abfe682ae34818c90e62b61fc466320a73c9f5c93fecdcec8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_headers GoogleCloudRunService#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db98367a2f8beb41f72dbf0859b436f83e35906aeafb4b1e914e396b67156b1e)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_headers GoogleCloudRunService#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. If set, it should not be empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#value GoogleCloudRunService#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3e65034c958e784b624a75893bca70050fe134674033b65787f79fdeacc946)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#value GoogleCloudRunService#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84163819879cc956ced8ed6cc3f92a6afca09998fab7dfd982cebd82ff4384dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8728cd3ee45509b2aa82b840983f64721e92efee125aaa9a230b0189e06bff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9037cff93eea5759e225f34c2b618c7506e930bf4926dc2a9000c0e101bad81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd28ae43856b436ffceb9a858285fa9ed5b5b72892c2ec482b75a343a536676f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef72a9cb097b204aa488c8b3186e12a314310743fd23b9ae6bbff20e74806154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac4eb20620da5c4cb3d5eb3d4964f323ceba56cb9878ed956a319c2c0b73386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46aaa5df76710708e8465e5883eb781f0f1c1e4b542b577851d2b1426ee2ebc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__950989626d1606a090f7ba2a8317ce1156e6f3e6c4d8cf5d0faf6badd60ba89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205dffde5ed73ce50905cf6f17210affa1188916bd48863cbbdeaa19d2e09eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0dd8c6776d5efbff7f783d986304aa3244d2358797ae5ed21629c5c2bd18fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37973d3dca2f66e2bbd5befc05edf3a2b78919aa8dbbc7e9ef4ed8d9ba84bf27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584733789b609ceaf1c2e4384d69f3ebc250b87904e2a9fe56a9a695d0f53683)
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
    ) -> GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__272854963e7a1a6f9c839ebc4d0a91906ca4e5bfcf1f54648e7d9fb4d17c43c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e049a6a6ff14d317c6d374465c6c1309f1ec4523f205816e3d88388d88934ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e076a1103915174640cc59120391a0ff9dccb4cac2bbd1ea28042d8c2eb2770b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1da232fc9e3a50e162423433a5633d072213cb6274a2e443acbf144c50c4c151)
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
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#service GoogleCloudRunService#service}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#http_headers GoogleCloudRunService#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet(
            http_headers=http_headers, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        value = GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket(
            port=port
        )

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
    ) -> GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet], jsii.get(self, "httpGetInput"))

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
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__aa33fe4b37cd9e1be3d37b6aaf224c64e9653cd7fda0e8e4cc79dd9b503f1dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7304577167748b8aa034d9543e15242def966903e6c594f2efffabeb681c47d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a12c8424c49deb8d1b8c258c7089c87e81ec8b45317d036430b6c996d06942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79736303938b76e3443ba591d862cbb21c8f42c434f72bad21bdf87e1042ca4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbe]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42dfd32299ed7d5bc687bf9642034698121129b8e621a7a1858e7aafccd3616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"port": "port"},
)
class GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket:
    def __init__(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db57c86b10e92168660751815a9f882eb510f7d5c1af7ac39bb7444c3892969c)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#port GoogleCloudRunService#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8341ce0361fddca08264f7deef0919600b86e3b685fceb70156bb08060c81d4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5f1c3c840beae6281631585ad3d966f9f7c94173e924fbb5ec8abcaf6ca116f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cef55eab9a6e237d537e018793325d60093f033ae3f932464f51b0534367e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"mount_path": "mountPath", "name": "name"},
)
class GoogleCloudRunServiceTemplateSpecContainersVolumeMounts:
    def __init__(self, *, mount_path: builtins.str, name: builtins.str) -> None:
        '''
        :param mount_path: Path within the container at which the volume should be mounted. Must not contain ':'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#mount_path GoogleCloudRunService#mount_path}
        :param name: This must match the Name of a Volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721d9512885423698a41477887e281e4584e5d046fe340f5288f477a4d3c3dae)
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mount_path": mount_path,
            "name": name,
        }

    @builtins.property
    def mount_path(self) -> builtins.str:
        '''Path within the container at which the volume should be mounted.  Must not contain ':'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#mount_path GoogleCloudRunService#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''This must match the Name of a Volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecContainersVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecContainersVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd54142112cb267ddb3d69a6165f4f14b6789d00d0557dad445e2a3f54045355)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecContainersVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88309848f7b1339d5dec3f20f7734621bcea6d4178770cbf55cbf644413799f2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecContainersVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdaf2e5f011531268c7add1dcb6e68b29e0d7799967f03f397d79dd8bc918bee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc5ba62211f04b37e00d9877b1a2d7a599f98b74c9e96af59cedab13f976fd09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7aea3182a9e6ab349f8ddbf394543dda839e79f8a8e69ac65a95d75d931ae8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4d7120e3690825d9844026990eed496a24c53db6b45a2af5c72c617730b94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecContainersVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecContainersVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__685d6a1af64396a3b70d50b976b6440abd0608141d15308952654187bec8d4fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6311a078abe5a2bf959f9355a960bd3d0d3b8c67ea0cd3200ea90d8538b3db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f66457a0becd190f5bca92c911fec983b0cad3b4d7a88e2f46de95eb53d00a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3931250160491189b716a43fbdfc0ae7387588ff961e6e4132ac32445c641d38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6e47a9e16a8a12e074f55c04fad59e89c7b195bdd8ea355886642a22f7a9f61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f53117791bf97337c420a6bc3e79619ba4fae874c2b6a8445aac3e0cbbf854d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainers", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7516fc8b50a7ac1c76c594373d93a5041c999a42fdb565893c865b416bad66c)
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
    def containers(self) -> GoogleCloudRunServiceTemplateSpecContainersList:
        return typing.cast(GoogleCloudRunServiceTemplateSpecContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="servingState")
    def serving_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servingState"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "GoogleCloudRunServiceTemplateSpecVolumesList":
        return typing.cast("GoogleCloudRunServiceTemplateSpecVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="containerConcurrencyInput")
    def container_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="containersInput")
    def containers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainers]]], jsii.get(self, "containersInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerConcurrency")
    def container_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerConcurrency"))

    @container_concurrency.setter
    def container_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aecd3e9630859a5e25dfd43c28f05474c5e59cefbc6b945fed7532f652635ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeSelector")
    def node_selector(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nodeSelector"))

    @node_selector.setter
    def node_selector(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26fefb31684380f296298d03aded484d1edd316a5c644a96166756b7bc3e94c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeSelector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountName"))

    @service_account_name.setter
    def service_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc63a0b0ebfa3a4381d0734e6869ea7d93bb63575f0419ef9fe4aea448fea9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4aefc524f62e0b6c3325b831fb0836d6f12241d2b4df81c995cda08d5e42b4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunServiceTemplateSpec]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4533c470889376fa51e45fc3618f6c6d9fdc377e5f0341b14b4a949c18cb7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "csi": "csi",
        "empty_dir": "emptyDir",
        "nfs": "nfs",
        "secret": "secret",
    },
)
class GoogleCloudRunServiceTemplateSpecVolumes:
    def __init__(
        self,
        *,
        name: builtins.str,
        csi: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecVolumesCsi", typing.Dict[builtins.str, typing.Any]]] = None,
        empty_dir: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecVolumesEmptyDir", typing.Dict[builtins.str, typing.Any]]] = None,
        nfs: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecVolumesNfs", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["GoogleCloudRunServiceTemplateSpecVolumesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Volume's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        :param csi: csi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#csi GoogleCloudRunService#csi}
        :param empty_dir: empty_dir block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#empty_dir GoogleCloudRunService#empty_dir}
        :param nfs: nfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#nfs GoogleCloudRunService#nfs}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret GoogleCloudRunService#secret}
        '''
        if isinstance(csi, dict):
            csi = GoogleCloudRunServiceTemplateSpecVolumesCsi(**csi)
        if isinstance(empty_dir, dict):
            empty_dir = GoogleCloudRunServiceTemplateSpecVolumesEmptyDir(**empty_dir)
        if isinstance(nfs, dict):
            nfs = GoogleCloudRunServiceTemplateSpecVolumesNfs(**nfs)
        if isinstance(secret, dict):
            secret = GoogleCloudRunServiceTemplateSpecVolumesSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59a67e677535f56a315858587dd85577965b47e649cfec91f55c40954975a9f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#name GoogleCloudRunService#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def csi(self) -> typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesCsi"]:
        '''csi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#csi GoogleCloudRunService#csi}
        '''
        result = self._values.get("csi")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesCsi"], result)

    @builtins.property
    def empty_dir(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesEmptyDir"]:
        '''empty_dir block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#empty_dir GoogleCloudRunService#empty_dir}
        '''
        result = self._values.get("empty_dir")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesEmptyDir"], result)

    @builtins.property
    def nfs(self) -> typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesNfs"]:
        '''nfs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#nfs GoogleCloudRunService#nfs}
        '''
        result = self._values.get("nfs")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesNfs"], result)

    @builtins.property
    def secret(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesSecret"]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret GoogleCloudRunService#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesCsi",
    jsii_struct_bases=[],
    name_mapping={
        "driver": "driver",
        "read_only": "readOnly",
        "volume_attributes": "volumeAttributes",
    },
)
class GoogleCloudRunServiceTemplateSpecVolumesCsi:
    def __init__(
        self,
        *,
        driver: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param driver: Unique name representing the type of file system to be created. Cloud Run supports the following values: - gcsfuse.run.googleapis.com: Mount a Google Cloud Storage bucket using GCSFuse. This driver requires the run.googleapis.com/execution-environment annotation to be unset or set to "gen2" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#driver GoogleCloudRunService#driver}
        :param read_only: If true, all mounts created from this volume will be read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#read_only GoogleCloudRunService#read_only}
        :param volume_attributes: Driver-specific attributes. The following options are supported for available drivers: - gcsfuse.run.googleapis.com - bucketName: The name of the Cloud Storage Bucket that backs this volume. The Cloud Run Service identity must have access to this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#volume_attributes GoogleCloudRunService#volume_attributes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1402a2a54ecd74b32ca3445f537beba4338f66ab864447500aff186aa63fb0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#driver GoogleCloudRunService#driver}
        '''
        result = self._values.get("driver")
        assert result is not None, "Required property 'driver' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, all mounts created from this volume will be read-only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#read_only GoogleCloudRunService#read_only}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#volume_attributes GoogleCloudRunService#volume_attributes}
        '''
        result = self._values.get("volume_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecVolumesCsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecVolumesCsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesCsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3694709379e781204cde7eb96bb6a4e25ddc959b918d9aa1d369ef47b6d59a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd78a7b65e6145b75f4ecaecfe9cb0eece8d4d6103230184b89acd3a3b085d47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4af5628f3352f3202e206afae61c6527853d5291decf43acae4a7b4b5afe85cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed5246afb86775452e4822ce97e7b242ac332b15c9bcd8f0297190e5a44d2648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeAttributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesCsi]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesCsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesCsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db7e57a18946a95c5344c28dfbedc101b9f10cb402c7e9c1a55238ad30da926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesEmptyDir",
    jsii_struct_bases=[],
    name_mapping={"medium": "medium", "size_limit": "sizeLimit"},
)
class GoogleCloudRunServiceTemplateSpecVolumesEmptyDir:
    def __init__(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The medium on which the data is stored. The default is "" which means to use the node's default medium. Must be an empty string (default) or Memory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#medium GoogleCloudRunService#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#size_limit GoogleCloudRunService#size_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3faaac1adddb005a4a795b0ed570f50e5b8b6d3513fa2dae97afa57c5927798e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#medium GoogleCloudRunService#medium}
        '''
        result = self._values.get("medium")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_limit(self) -> typing.Optional[builtins.str]:
        '''Limit on the storage usable by this EmptyDir volume.

        The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#size_limit GoogleCloudRunService#size_limit}
        '''
        result = self._values.get("size_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecVolumesEmptyDir(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecVolumesEmptyDirOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesEmptyDirOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca61045155edf8e998e796cc67a2161e0407e8952493c043bd19c8218817b139)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d00cc391b0c8f6802431701ebd114fa9d5804f5339040d41e5f132e5df52c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "medium", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeLimit")
    def size_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeLimit"))

    @size_limit.setter
    def size_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d4dd9589ab2bf8ca312252c6f505a5a36b831fdc999282ea41020e08f020c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesEmptyDir]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesEmptyDir], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesEmptyDir],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6eca628c9dcf4db98918304f27aa82dbb6a95eef4d425c7271ed4b999066d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c57bf04100cfb154648a7d527b38a871ea27fc4e0817ba476b1f91bef636080)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9604611b37670d975e812f4367e6693fe9c43c13d058e3cfae43ff96f8ff7c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86acbe1f4bfeaa0b399584d45a5150dd4c40afb21c16728bfdba4a48121ba204)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43e5a286e32396e9113d2a81a0bd7929e7ad452b380b5f9d977598df9da1ca84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a13504d64e353b701f40a35ee936aae228839509e0735a3db509d232e1879731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fa450e7b85d71374d26eda9efc082e19b6aea0a719990f76c36c2ab127302c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesNfs",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "server": "server", "read_only": "readOnly"},
)
class GoogleCloudRunServiceTemplateSpecVolumesNfs:
    def __init__(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        :param server: IP address or hostname of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#server GoogleCloudRunService#server}
        :param read_only: If true, mount the NFS volume as read only in all mounts. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#read_only GoogleCloudRunService#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f29cd43c1935383e172ab695b3993709d9caeef7627e80d8508ffd9ff0c6c74)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''IP address or hostname of the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#server GoogleCloudRunService#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount the NFS volume as read only in all mounts. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#read_only GoogleCloudRunService#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecVolumesNfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecVolumesNfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesNfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7495da1c4a66596ea96a6cb5eeaa7ec44d54570eaebcd2de14de61a8b65a145a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce18e5c99aa93b07dd738cb29aa005f51c373d72778f7becba71a290d5fec092)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2233eef865191f5e53a3a9e5535f501b386bfdf604173673e688d84dd84dbbac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098242fdd54c394d405c142f9c99afa9fe59331670c0620d6e312e066ac09762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesNfs]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesNfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesNfs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b570f30c018f8f799fd5e6bd915e34cf1694f15f877c82f7c67fb9b169ba3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6324bb4f7be710443c393a8f1c019117ab2c6834d4dc62e420397460f0f8a0d3)
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
        :param driver: Unique name representing the type of file system to be created. Cloud Run supports the following values: - gcsfuse.run.googleapis.com: Mount a Google Cloud Storage bucket using GCSFuse. This driver requires the run.googleapis.com/execution-environment annotation to be unset or set to "gen2" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#driver GoogleCloudRunService#driver}
        :param read_only: If true, all mounts created from this volume will be read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#read_only GoogleCloudRunService#read_only}
        :param volume_attributes: Driver-specific attributes. The following options are supported for available drivers: - gcsfuse.run.googleapis.com - bucketName: The name of the Cloud Storage Bucket that backs this volume. The Cloud Run Service identity must have access to this bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#volume_attributes GoogleCloudRunService#volume_attributes}
        '''
        value = GoogleCloudRunServiceTemplateSpecVolumesCsi(
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
        :param medium: The medium on which the data is stored. The default is "" which means to use the node's default medium. Must be an empty string (default) or Memory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#medium GoogleCloudRunService#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#size_limit GoogleCloudRunService#size_limit}
        '''
        value = GoogleCloudRunServiceTemplateSpecVolumesEmptyDir(
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
        :param path: Path exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        :param server: IP address or hostname of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#server GoogleCloudRunService#server}
        :param read_only: If true, mount the NFS volume as read only in all mounts. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#read_only GoogleCloudRunService#read_only}
        '''
        value = GoogleCloudRunServiceTemplateSpecVolumesNfs(
            path=path, server=server, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putNfs", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        *,
        secret_name: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret_name: The name of the secret in Cloud Secret Manager. By default, the secret is assumed to be in the same project. If the secret is in another project, you must define an alias. An alias definition has the form: {alias}:projects/{project-id|project-number}/secrets/{secret-name}. If multiple alias definitions are needed, they must be separated by commas. The alias definitions must be set on the run.googleapis.com/secrets annotation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret_name GoogleCloudRunService#secret_name}
        :param default_mode: Mode bits to use on created files by default. Must be a value between 0000 and 0777. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#default_mode GoogleCloudRunService#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#items GoogleCloudRunService#items}
        '''
        value = GoogleCloudRunServiceTemplateSpecVolumesSecret(
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
    def csi(self) -> GoogleCloudRunServiceTemplateSpecVolumesCsiOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecVolumesCsiOutputReference, jsii.get(self, "csi"))

    @builtins.property
    @jsii.member(jsii_name="emptyDir")
    def empty_dir(
        self,
    ) -> GoogleCloudRunServiceTemplateSpecVolumesEmptyDirOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecVolumesEmptyDirOutputReference, jsii.get(self, "emptyDir"))

    @builtins.property
    @jsii.member(jsii_name="nfs")
    def nfs(self) -> GoogleCloudRunServiceTemplateSpecVolumesNfsOutputReference:
        return typing.cast(GoogleCloudRunServiceTemplateSpecVolumesNfsOutputReference, jsii.get(self, "nfs"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "GoogleCloudRunServiceTemplateSpecVolumesSecretOutputReference":
        return typing.cast("GoogleCloudRunServiceTemplateSpecVolumesSecretOutputReference", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="csiInput")
    def csi_input(self) -> typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesCsi]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesCsi], jsii.get(self, "csiInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyDirInput")
    def empty_dir_input(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesEmptyDir]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesEmptyDir], jsii.get(self, "emptyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsInput")
    def nfs_input(self) -> typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesNfs]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesNfs], jsii.get(self, "nfsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesSecret"]:
        return typing.cast(typing.Optional["GoogleCloudRunServiceTemplateSpecVolumesSecret"], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690f5d5dfbc9e7d16834238961d3ce319783cafd4550fe97cf215ca62ed554b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc4d4f009b3ad2e32d30ddc3c1216a4c53edd9fe9d4160ee82cd134f6cadd28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesSecret",
    jsii_struct_bases=[],
    name_mapping={
        "secret_name": "secretName",
        "default_mode": "defaultMode",
        "items": "items",
    },
)
class GoogleCloudRunServiceTemplateSpecVolumesSecret:
    def __init__(
        self,
        *,
        secret_name: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunServiceTemplateSpecVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret_name: The name of the secret in Cloud Secret Manager. By default, the secret is assumed to be in the same project. If the secret is in another project, you must define an alias. An alias definition has the form: {alias}:projects/{project-id|project-number}/secrets/{secret-name}. If multiple alias definitions are needed, they must be separated by commas. The alias definitions must be set on the run.googleapis.com/secrets annotation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret_name GoogleCloudRunService#secret_name}
        :param default_mode: Mode bits to use on created files by default. Must be a value between 0000 and 0777. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#default_mode GoogleCloudRunService#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#items GoogleCloudRunService#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d43342828fdc9f57ec70fef882d7c16523dc1bf833e93b2033ad1cb3f5d81f4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#secret_name GoogleCloudRunService#secret_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#default_mode GoogleCloudRunService#default_mode}
        '''
        result = self._values.get("default_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecVolumesSecretItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#items GoogleCloudRunService#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunServiceTemplateSpecVolumesSecretItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecVolumesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesSecretItems",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "path": "path", "mode": "mode"},
)
class GoogleCloudRunServiceTemplateSpecVolumesSecretItems:
    def __init__(
        self,
        *,
        key: builtins.str,
        path: builtins.str,
        mode: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param key: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#key GoogleCloudRunService#key}
        :param path: The relative path of the file to map the key to. May not be an absolute path. May not contain the path element '..'. May not start with the string '..'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
        :param mode: Mode bits to use on this file, must be a value between 0000 and 0777. If not specified, the volume defaultMode will be used. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#mode GoogleCloudRunService#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f1eb31394e3ee9fb53dcc4375da57b6b76e33416c5d973bde24dee753463ed)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#key GoogleCloudRunService#key}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#path GoogleCloudRunService#path}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#mode GoogleCloudRunService#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTemplateSpecVolumesSecretItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTemplateSpecVolumesSecretItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesSecretItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd8ba654c6706d7362293a160cde863900934a31f4cda778e8c7d4c7b5c844f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunServiceTemplateSpecVolumesSecretItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42c519dd8db5205cec2cf9d5be5fbbce84b4a2e7902b7c55c75a3c893cb877b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTemplateSpecVolumesSecretItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac64ea96963be7a6e23ff7ef63629f80caee7128d3005b9adfc9d7856e43861)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de32fbfe4120ccd4b2dce52c44af5e77950c8320fe6aaba0d4e83ed84d3f2478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f31c38af5ca19481a94716a8a72d5bdf7dce2a4183757476be264a78f7150244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumesSecretItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumesSecretItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbbed8f2a34ea17e69a7f8bafd2e97941c18997e59fad9d7e15d396994f7ca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecVolumesSecretItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesSecretItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2aa650325201e6f3c9629368d4c058bb92c4b312309dcd2b1d34123334694ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__685d157b368f36c4340313bb500b3c8f49588a67502616376b713a875c14a5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bb1828f9acb9d64821f155b419ad7fb2246ccdbf9548271b49dc2440e39178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754754dd75a2e6c3f57dfd6ce651a549431ca6a33e0e150de11c0dd9f8e1486e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecVolumesSecretItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecVolumesSecretItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecVolumesSecretItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f995cd3fd5648ca014cb016089d707fd0368aaf0f7db0bc65ff50a2f8d4397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTemplateSpecVolumesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTemplateSpecVolumesSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97a950a3314d022f1ffa18b8b29981b168cb7b6145f7d8b1887d7d610fbeb418)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d304151f74fa6e2d826b64e763f8ecb1a00d4628cd8334da5bca4b08e805fc4)
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
    def items(self) -> GoogleCloudRunServiceTemplateSpecVolumesSecretItemsList:
        return typing.cast(GoogleCloudRunServiceTemplateSpecVolumesSecretItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="defaultModeInput")
    def default_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultModeInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumesSecretItems]]], jsii.get(self, "itemsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4283b82fa216c140683cdde0cdf5d983584a314290c3b80098cbfdc7e093f942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07cb2126e5052a951803bf48125c543fe021011b858dab5e92289e2e7d510038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesSecret]:
        return typing.cast(typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb6e8a01c888948bccd0f56002495c80c442a5c5581e338b08135e1c1b979a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudRunServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#create GoogleCloudRunService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#delete GoogleCloudRunService#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#update GoogleCloudRunService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1958a5da499f06ef1bac80cbe16d8eaea154765ae76eb9fc7156049ed23ea4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#create GoogleCloudRunService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#delete GoogleCloudRunService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#update GoogleCloudRunService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1c01ff3dec53ce411ba596cc0af5640a28ab9f0d5f9258e1d473a936bc708fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22d5fa9d2473d0ec8c3f2bd1dd90b39e765793ada7cad93ae359cfeb3bd324cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0d02e9b1d2fa22d4037828188214c24ba4798fdab33d478d5e2603cf0ea848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25410ba0596337a5b079cc15a7a0a2eeefb242c9e3703a75d78325dad7002dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4e86fa72307edb0bebfef9bdd75f4a7ec8fe0a4d952b33b52f76ae04db0ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTraffic",
    jsii_struct_bases=[],
    name_mapping={
        "percent": "percent",
        "latest_revision": "latestRevision",
        "revision_name": "revisionName",
        "tag": "tag",
    },
)
class GoogleCloudRunServiceTraffic:
    def __init__(
        self,
        *,
        percent: jsii.Number,
        latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        revision_name: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param percent: Percent specifies percent of the traffic to this Revision or Configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#percent GoogleCloudRunService#percent}
        :param latest_revision: LatestRevision may be optionally provided to indicate that the latest ready Revision of the Configuration should be used for this traffic target. When provided LatestRevision must be true if RevisionName is empty; it must be false when RevisionName is non-empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#latest_revision GoogleCloudRunService#latest_revision}
        :param revision_name: RevisionName of a specific revision to which to send this portion of traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#revision_name GoogleCloudRunService#revision_name}
        :param tag: Tag is optionally used to expose a dedicated url for referencing this target exclusively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#tag GoogleCloudRunService#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3370043868e96bbc63a9f06677c1850c4173da6b8f9b41b833e465830e800f34)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#percent GoogleCloudRunService#percent}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#latest_revision GoogleCloudRunService#latest_revision}
        '''
        result = self._values.get("latest_revision")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def revision_name(self) -> typing.Optional[builtins.str]:
        '''RevisionName of a specific revision to which to send this portion of traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#revision_name GoogleCloudRunService#revision_name}
        '''
        result = self._values.get("revision_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Tag is optionally used to expose a dedicated url for referencing this target exclusively.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_service#tag GoogleCloudRunService#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunServiceTraffic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunServiceTrafficList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTrafficList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c8f6446d256071325af68bf9ab3cf569c7ff752d8c509daae70099cadea8f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleCloudRunServiceTrafficOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e214c9a0afe37d6a242f69d3f1c990ccc187895c59de02e4ea2b6ebfe95e2d71)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunServiceTrafficOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32261dd292a640095fbdc14d0988918ab55b55a8690d7d43e8e706005d03efd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cbc951ff76bbd18d23f39c144caef96930c0f829609c2e5206e342a1b73d14e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8681f494cca7c8da846bd0bd2d43d1d5872779b4daa3aca6a147a7768829e2f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTraffic]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTraffic]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTraffic]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5880587b906b9876fde2b5ba2f0cc98c4e5a461e7d7f6149e5b11e5681130f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunServiceTrafficOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunService.GoogleCloudRunServiceTrafficOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdfc810e9252cf401d02f7cbec935c100d24396aeb62a1a75dfb395f92c4f092)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4421183bd3ebb1e74a3e2551992edfaef77dfd1a7d005fa4ac47daaafa7df0b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latestRevision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89dea73bf96d6d8bcf0f00e72aba7ebf2fbd442ac22f869e64ef20c361ed865e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revisionName")
    def revision_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionName"))

    @revision_name.setter
    def revision_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31c45971f362d3c528dfcc78863a5d5370b4460a5deb8e498ad0275bd9c1dce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revisionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84fdfb65f7d92c2dc2de79a9b7c3af3116a47ce300221e6af3c3a87792e2c5ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTraffic]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTraffic]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTraffic]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd867cb1baaaf82e5fd6e69fcf6c242d1da23d58db95c1fef5ec9328ec048cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudRunService",
    "GoogleCloudRunServiceConfig",
    "GoogleCloudRunServiceMetadata",
    "GoogleCloudRunServiceMetadataOutputReference",
    "GoogleCloudRunServiceStatus",
    "GoogleCloudRunServiceStatusConditions",
    "GoogleCloudRunServiceStatusConditionsList",
    "GoogleCloudRunServiceStatusConditionsOutputReference",
    "GoogleCloudRunServiceStatusList",
    "GoogleCloudRunServiceStatusOutputReference",
    "GoogleCloudRunServiceStatusTraffic",
    "GoogleCloudRunServiceStatusTrafficList",
    "GoogleCloudRunServiceStatusTrafficOutputReference",
    "GoogleCloudRunServiceTemplate",
    "GoogleCloudRunServiceTemplateMetadata",
    "GoogleCloudRunServiceTemplateMetadataOutputReference",
    "GoogleCloudRunServiceTemplateOutputReference",
    "GoogleCloudRunServiceTemplateSpec",
    "GoogleCloudRunServiceTemplateSpecContainers",
    "GoogleCloudRunServiceTemplateSpecContainersEnv",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFrom",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReferenceOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromList",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReferenceOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvList",
    "GoogleCloudRunServiceTemplateSpecContainersEnvOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom",
    "GoogleCloudRunServiceTemplateSpecContainersEnvValueFromOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef",
    "GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRefOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersList",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbe",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpcOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersList",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeadersOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersLivenessProbeOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersPorts",
    "GoogleCloudRunServiceTemplateSpecContainersPortsList",
    "GoogleCloudRunServiceTemplateSpecContainersPortsOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersResources",
    "GoogleCloudRunServiceTemplateSpecContainersResourcesOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbe",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpcOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersList",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeadersOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket",
    "GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocketOutputReference",
    "GoogleCloudRunServiceTemplateSpecContainersVolumeMounts",
    "GoogleCloudRunServiceTemplateSpecContainersVolumeMountsList",
    "GoogleCloudRunServiceTemplateSpecContainersVolumeMountsOutputReference",
    "GoogleCloudRunServiceTemplateSpecOutputReference",
    "GoogleCloudRunServiceTemplateSpecVolumes",
    "GoogleCloudRunServiceTemplateSpecVolumesCsi",
    "GoogleCloudRunServiceTemplateSpecVolumesCsiOutputReference",
    "GoogleCloudRunServiceTemplateSpecVolumesEmptyDir",
    "GoogleCloudRunServiceTemplateSpecVolumesEmptyDirOutputReference",
    "GoogleCloudRunServiceTemplateSpecVolumesList",
    "GoogleCloudRunServiceTemplateSpecVolumesNfs",
    "GoogleCloudRunServiceTemplateSpecVolumesNfsOutputReference",
    "GoogleCloudRunServiceTemplateSpecVolumesOutputReference",
    "GoogleCloudRunServiceTemplateSpecVolumesSecret",
    "GoogleCloudRunServiceTemplateSpecVolumesSecretItems",
    "GoogleCloudRunServiceTemplateSpecVolumesSecretItemsList",
    "GoogleCloudRunServiceTemplateSpecVolumesSecretItemsOutputReference",
    "GoogleCloudRunServiceTemplateSpecVolumesSecretOutputReference",
    "GoogleCloudRunServiceTimeouts",
    "GoogleCloudRunServiceTimeoutsOutputReference",
    "GoogleCloudRunServiceTraffic",
    "GoogleCloudRunServiceTrafficList",
    "GoogleCloudRunServiceTrafficOutputReference",
]

publication.publish()

def _typecheckingstub__a2d2ed89fd467086f78cbcbbb34afe5b23f929335d3471637dbfe0051c5e309c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    autogenerate_revision_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Union[GoogleCloudRunServiceMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    template: typing.Optional[typing.Union[GoogleCloudRunServiceTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudRunServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTraffic, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__c0e65d7fe6f0669122d0ec5e1fc4ae88147026bde960426d1106a528ccd13715(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5870d9097d9921e96e26fa7c92c58fc9c5fc2b14367fbaf1b4bfbaa0ca747f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTraffic, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025e85fb396c347e68555afa8720000ffe54ac46508ce4608b8a72027288283e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5323fbfe7fed4c6ddc549ed2faf70a94f60a08c45693cc0ddb6b9250b97b4bdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf461d942c56db368e6a729c96b21812ceb58cc26d55a7aa0390c2725079ff80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbe006108d3f4ac61a6f1c7ccac220eb53131413e8fe2366e0c35bdeacecbc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d0cd912443862a5d596e6d113c93b7e7855c9bb7630296960a86bcebeff042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621f0e5d33a9e3443fdbac725be17560a7ea5d3b43fc300198b83bcea0a129f1(
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
    metadata: typing.Optional[typing.Union[GoogleCloudRunServiceMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    template: typing.Optional[typing.Union[GoogleCloudRunServiceTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudRunServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTraffic, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172b04faf5ad0aff248612878a41de11a00ab28bbd510a19e74879f75b46356d(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12e712f09473f6ad952f7dede80f0e0bcaae147642cb4b4843f38fb648d4cb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2d44472ec1d5d266449823860c4eb634ebb420e779ec73cb401c631dc94527(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f723f4d5f3987a32ca3fd20fa1f717a7714fffb05fae4913b7a3df51907ed2d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546f92be2f03f17c142b3ebc0fe6a7ae06ed2dd041033b67f5612a0e083b07a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096c890e07e6557cf4bfd6ce78db8f0bee601662865e3ae4cae28ee4a2959437(
    value: typing.Optional[GoogleCloudRunServiceMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1e57dde0b295368fd3fd1adc9262087756d4edb60c08e9c8acaf8bea8145af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195f0d8a18a89134bbdceca850a6778dcd8c89e7cca6e23a494e636e9bff1684(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b54e086878c84c9ec53891f338e79d2766860c7df1d442a4b92ffe675472b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68cb7469aa80fc6170e885578d6c3c9c5a544166dd8f68cd8239e26cb70ec047(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144db441a6b0fb33cb17077e8904bc4a1ab7c28a59d3c42fbbbe7b7c6384c194(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95334158a78302a4a43e0b811231fab2c43e123f7afaa7204b8a749fb88fa16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff96f10301e776bebefc369c23b106acbe2b2edef741145de1d6e9a0052ac31(
    value: typing.Optional[GoogleCloudRunServiceStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da3237a8281fc48cf196d99506c6da7be77e7c31ebe91455e201696a594cb50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9bf74c7c218b33827d664d1e3e86be2245834c6e82d1b57146e9c6290f67c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50c9b1617939d6e816d6cd1e13f247e2eb121858790de63cdb3fd4b48960c5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef103dbde9f380d2299d1c95d50d381fb098b6f3c0c4340db8fff48f2121de8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc81790e818619180451db51fc749da2b4cf05000d74ac0c372ab6e320e4f4e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e4d5254b207a403f61b1559ca77e6a399d4e5634213ca9a42aba121009788f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cbeb816148467141bd3adc31afa13dddecf45e64149a915aaaac0e0ffccf0ed(
    value: typing.Optional[GoogleCloudRunServiceStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417a720633a30b70b0027ea9a1ca0b9b8fa3fc5727d9d459557ce97cd92f9092(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ece676bbab1d48812995fd9a0417dd2a4c9992fc0ef132d0e98d3313900334(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99fd5e31a7777aad452c35247e90196430c2a935ff60b6a4218b4d54593a346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f293e0e5318b25b67859f6c2d461472b7576f9dcf76e831f518dea7bf6d079dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea6870819437d6cff3cfdfb261171546e4f765a1f33d1a268bf59badcef9c32(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8077b170a04ff65f843142dd0b2b047f43b6468e2f940834f99fcad6796e24ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d03b2bd8fdc4e747ac1d7e5be836438938a9dc7a874eaa4b639aa699374f4d8(
    value: typing.Optional[GoogleCloudRunServiceStatusTraffic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78dee0b856ac0265d54533a853d79a452b45e196be04024dc42f25d85ba31b0(
    *,
    metadata: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    spec: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2a5844ac50a2823b9649917655a46ff7fff58156c875a348dc4e0bc9f2bee5(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f966ed3c569a31290819c18afea701826ee7c1c51cdbe8d30d00e53494d4e8a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cee234fa995a9014bf4f91086fe570d74e0bd9d77f169214ef07100097bb42e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3877b97b55cdd4db2bf4db0586a9eaaf8da2430d02dafbb58f30af15d8094091(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe41ce4f97143d9ddcbc64040d343c27e601a9498e4e3b346216ca760a40fc6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1c18984a046b8506454a65cc53b10e2d71b1e981fd80dfd1c7c01f49258edc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3b1b74fd9d7cc6cdaa26c05c93c59f2174c451e99dc0a86f2a7deb1bf3d3ff(
    value: typing.Optional[GoogleCloudRunServiceTemplateMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ea92773a84b30e35fc1ad6b6707d269b648d8eb0dd4c7759eedd26817b7cc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3466fdb9d56c58beb5514af4ffbbc4452ae33ecec6b7d09d0c48c916976997(
    value: typing.Optional[GoogleCloudRunServiceTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493e99862a83e30f9ae0dfc0bc8f31dc4c5fa4201a8bd5234a3f427b2cb546ca(
    *,
    container_concurrency: typing.Optional[jsii.Number] = None,
    containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    service_account_name: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e3a4c2ebcf60b389d782ff1b2688da08afc9475faa9d0953c15155f4abbba0(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_from: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvFrom, typing.Dict[builtins.str, typing.Any]]]]] = None,
    liveness_probe: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersResources, typing.Dict[builtins.str, typing.Any]]] = None,
    startup_probe: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af5176b492eed4d50ba285f4435198dbe2db95e6940ba25020ecc45e4ed08ff(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
    value_from: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9346af924680ba4d67a00f4ec2aed80d910c087a23755d4e051e6b0168f15844(
    *,
    config_map_ref: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef, typing.Dict[builtins.str, typing.Any]]] = None,
    prefix: typing.Optional[builtins.str] = None,
    secret_ref: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bce12b90443c16bbf6b5831225361ae6f7b64bb65b8ce7d163d28b921f40961(
    *,
    local_object_reference: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference, typing.Dict[builtins.str, typing.Any]]] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a1600870d1597ca8143a1e2fe38987eaa16af80c130ee103da0851aefbd937(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee01f998c30534e8b452be315302864da79694616e915a7f8ab9def982e9466(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe104e9ce6f766fd4ce395e32213bdf59539188ee4e03e2a36d95c6b64ebf626(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff4022060b1526925b219cf53ceb5c35708ff33291ddb89c7a5f9e0a7d68f6d(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRefLocalObjectReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb06e27930246d6e2919ad1bf4e270efd70c50c87728a3affa3b307587dc1f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641a84c94554008804c632221ceffef6ea2c1064c59227d9354800eef0e3f68d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe76324a7ecc40409a81793ff8455d5fb9eb266b970aa6b6c71fd0fe5e23b2a5(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromConfigMapRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc1b653940d1e3d1ab2c4922edd459febdb74d70c3351e2fc8c15a945ae3f4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e36ce4cb15693e31e0fd7b9c3bac887ab8c011bdacdc0c80c202164e0ff7a26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63c4c366e212f1d2cee7cbf36a56bc70bc275afdac877264dc26a684efb759f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bca170b8124ff1aa804e94445d80f41405f51210d7280d8676cd8287257e52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206e1a8bda20b35d06d5fa5be4c6819b9714bca6018083e3b973db4dd14393e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5e91fb2cd814d088fd5661e332646cebce4354e7b1de26bd4e4b56627864fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnvFrom]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f5f75cd2d88f9678cecb61e0e089924fc3d33a8e72f8b97645c6c6d98bfe6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fdcbd1bf65973b3a591e5a09fd12b55ab8c8d79784a2d1e157518f240b4284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a461bf66497c831a69ec6f7e647d6cd0316e2aeb4238376bcba5d02414a66ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersEnvFrom]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906e77e68683ea2c419e9f46945299f514e89d12874f6ff28e8e3253ae0dd0b4(
    *,
    local_object_reference: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference, typing.Dict[builtins.str, typing.Any]]] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce341d1a0223f46d6463ceecd6052c77fbbf7d7434cefd8d2a3744b872028291(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643e53f61dcf476f381278600e127216e8e51aecaf8a7a772f7ac65959d55d0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d92b594ba857bfefb11d87cb5d2afd379267f1b3e0c3fbe910a7db6adff4a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0673e3b62872d777f076638712ffc476a17bc70cd2cc8cf7259ba55f0294d631(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRefLocalObjectReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29dc902ced2b2144a6aca84cc3cf467c5b6a7b81d68184654d33367e9de3f52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed9e0f0db5b58442d5619b1d0fc357c8af5e495c936ffeef6915dc6d73595d1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6670f6b3b9baa1f09e32e9e9eea06d24917f6411e291237d71a700c12ddf302(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvFromSecretRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dd6471ebd4776131405cdb98f8468ac83cd0ecc912a9503a842d6cb062c224(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe200a5649008717a37282b1c1575b67f26d2393bdea94f2e3922d3117d20c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd42819ba9f293d4eab8967c39c836c0919176c9662718c8a6a6d6b93c34b8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607fa1dc9ab499ac45bc122a245d754d541b9fb0b1cda27b250f8ceb500d7f45(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1786fc2882d8f2b79320c202fb2bcc578e0469363bc0610c9c84f2b7fdb30108(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543932251355235ec10ba4dcc406cc05c92861e98933090ca99d56e7e1f6375c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06e76c3c896e778e692f0d52f823fe514f9fed6a104295dbc76e6a6c05290f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1319ecdf1e6a0fa0320f672e989eda55cc2d38692a80e3d7a9015f989f239c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1142ac7935e0cb0a9e11649beec82183941718d8a26b2717fe488d8b0b13a8e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9bce1191e0e30631bc569ce5d8bf0e8b3d767b03dcebdda6f8e16195d4e0b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dcc1660a07f02665c71a333521f452fdfe1c29f425ad653aa8813f777b9673f(
    *,
    secret_key_ref: typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0c707fb7c39432723f4b17c74f4e77c1e69147dff36977b825434f3541e450(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ad54a06c5baadd22f830be7ccfa1d4b0c6f8a627cf7060664161e92306f859(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvValueFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e60bf194288693289ded6b43c5abc6e6cab52d0aadc7e790c3a5a07b02acaa(
    *,
    key: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4cbd8ddfbde6abdbdeed6290acdb64c787ae879bdd9bd87b2157ef66cfd0b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b12fa4c86f35bf8ced33631c9829bfa7e91ff3adf27eab25e82cb9a3a437ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce64953c3aa2b76ad6c6387d1ae5cce3a49b9900c559924e0ed0f18e5ab1327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903e46aac4200d48f55091be549ccd92b29788d943333333a026eabfde46e5f6(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersEnvValueFromSecretKeyRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b4703f3b2cf05f37d85752c3993e80f36f74fbe0928036c37d7f1912493476(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2316c9d9380dea010c3c9589ddacf89e390dc70e76e98298f24cec6d26f66f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c712b83321bfd79a1529f9ec8b509dbb32abbf623dc084d1309581d6fef1056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bc506e8d0aece04abdf9f53d83b5615aa37c62fbd299f5fa5ec1891d475111(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5f2518bae68b0650d16afe0f4e23c4d1d36ae9dd88e2aa4e808cd7844e81c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356ccd795bb07ba784d439727710352aa5969547f941c4ac4082ef75358e56b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34552097e70e2bfc7763acfdaf53059f1e59156e43f41ab4b16291d7bcea40d8(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b430be3aa8480d0fdad6e81186883dc8e47982080eff7b6008eb80529d2ce8f5(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda182c9aeea79c9939cd5667dcbdbfb76322317df8141b7794f884d4eaa629f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b07abdae65ef45f03660a2aa052123206659d73a268eb1e859a659e5d22ba28(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385c5ce4e0c5d8423cbd52f71b1db05391e002754450060c48cb06dc0f092cd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d548f0c915e531c9b27ce7f2d2ced3b6b8cd06e1aaac2c34a483fd294eccd86a(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52904953f3b3fbfe3a0bd01413cc3f77141b5f9af4d5065234a41841ee82b5e9(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bc91644e3f2a9c410ddf9de86e1db20125e2373d9ac82f43fc909a6419c36c(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e12383e21c8b4e995faeaca18a7b956b5c2a3d839fdfc70ceefa8bd528fe443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79163fdb519c8392a4bb46b7a293f80f6c2657aa5a6a69fc655c9c1d96b904c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f1aced315f1bd8a719b9738e55f80d4cefb07767606c52bebac214ca2a149a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3964bf8d6aefcb69d13fc583bcde040c4e620235d2a5d900ebafe31c37e9717e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be1f962887cfd094c5c7a4284223b930d697af034e4ea0de5b322b580a7ba47(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3843c7e8cecec42836e465eb9a30f9ff7d8afb103d09059a844ab978d2158e30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906ddb98a550fcfa188610fd8b07eb8fdf75473a44641c0b44c807f225f5d90e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b50e5069cbd076dcb3e579968d11a6a6b5566cf4e3d15e8d5fb2d78b7fadb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89a4070a31492a2899c72f45b2ba75b65e89926cc428f0e0f77acfa58f22a7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39aa053b5f393c1b85325aff6baea7b261b76f0c06cde6fcf96256bbeb4e8129(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be941effed564bc42ee5a0094ed822b112a5cb82dc7b336a8a125c1b88fcc300(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b82d83ed925fa13306a24125eb24a9760784f0047daef6ccb270d9dd725a116(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f34a01448a3c67ba4ea2eea508acfdbdd24325600f0115bc3a4613082671639(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7992a98edb90c774a4700631345cd51729137fdc0f2d25ddea996433e83dabee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948092c6602c9a5f2ef8cddef9eb0170987b7710a788d62e6abd937558a85b95(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8365283ed2fe6c4595f43be0ad142d709cb39c20c5b7b13712fec3a51f41307(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b315e6eaf045f089ebd2a6cfc8e13f2e2dcbacbab61492d7bdfeb0f9f976a4a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee9f6e5b2adcb943a9be818b87413431bc05ba99996aede53b6b344f74543c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d564aadd6ad06e0c0debffa90a82ca6f97a718848a96b250ec2a16328053cd30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83fe56af9cea0c67754bf57639f9d242ed281c799f7146ece6ed9afbc683e522(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac8d8253d6ba5afc4ac9f3af35966a5e03328b10c6f91bac6906eba5b6c8d4e(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersLivenessProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea810ecc04592554b66dd07fc6b4df73350c4f33111147e64e8b66d3f2c2773(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4664ebbe0d56738e337b0ff1e9fa7fb2f6d400d252798457a50b2dd0ffdd5dd0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcd8935ac424fc4fddc620457ab9b4d0d695155c4de4e873168a10d2c754f88(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersEnvFrom, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09933438689390b2f25f4dd110ae26cba35c76a1a5bebe28c60096be25023e3e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95bcd488db6ee25922ca1764a1150942f2a079d73f20c58f239ad6ef3aa7fc66(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67df94ad8c7b7bb3529a308cc1ee11267c7de9fa81e4a25974aaefc1cd8769f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1ae95382e4f4a65bc8473de872a8c62cf77ff2efeddc4ecf1fb83e743c48c3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185dee28fcd55098556ca1fce3c746f22a6500bb3b9cd6fe23ab48690b02e68f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fe5d887e74a1b28925e6cca311fd66e25c802f8e75abd00f4bc21381040457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc647ee6445c6b4ef81ed330ba3ba0e46c373ebd6cd581ca4066b0afce79c6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd7d00cf8d998eb32182707f0136002fac6c9f803e7116e9e5e412c50ef383f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30dc6f5d45c5ccb81c00cf9e8671983f91a8e599a32f9a66b51843454f57316e(
    *,
    container_port: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088c14876441a7745c290972d232246718c63a377c9bb93d229b76c37ee53af3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7b2e3d39066236b06382c51d08a0b69caf0be65d59ede4ee92e1aa6244e969(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0abfdd454f63765013881bd9d33e69c51ec56b75e46101ba35a08e689644b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7855a729d4e0b346fd0caf7792efba3c52b17c2bfbb6676a50813eb7b9604c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c918915560777b0d44a3edc4e0a48daabc0b5aa351a0946e3050d23ae8ee700(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c7b2773b1ca9e2ed64ac97c255bd4aea163e99889f2d1b91eae0b8fb4dd6ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee71737b923f6ccd05ad33d32069b59769caf45914e3f2108a94afc300c98289(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19f631d4bf988225c516da2595d1d76e96362d1f9a687425f848dcfe2a1ccb3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800fe85c9f6e7f7ed28aa0bdcb1de05aa25030abf26e31ff0ce991bff2f0450e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71f73a449bcdb584bfd0aade8f67df14f883b130a54ebd6bf1b45325b98d437(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6505b145f1f462901ecf80315851332fd2e49b37efddd2e5046c3a2a9fc2a2ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe72a9029a3268bdd7356961ae6d3685ecdd93205092c73be3fe5fceca76d69(
    *,
    limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    requests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dbe56401f9c091749c4283e27320df6506bd4d877c2b35f6de8260a9366c26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c692274612cecec9e0507291d358497e7ae1ccca5980a4e2cbcec1cb9de6bf66(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e0fbb50ebe5b112986bde32b5fc97a5c3a22c11425c9648c7f52cc88d470e9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3380cc00aed43ba31419146edd26b8b1a928ed03db26ff1b2f82fb33216625d4(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c251c5bf94c713ad0d63a368a6542b61207e866fe4d9818317025424375d5490(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88f4b37d4458c03bf2ba69fd5400df6b3da82447dc7770c8da620764db54461(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbcf8d7a3a54282ebe354ce5b20c9b37522a8901daa0aee817fbb6bba7ff8ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af767a37f8b2ca852e6125c5c01272913b88e64e8ca05004d449af2c1d2b4d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b614477406a59a28b9764b6b09a56d20551fd020c410a0941f8d7fa9d6f596aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd1f4333be456abfe682ae34818c90e62b61fc466320a73c9f5c93fecdcec8b(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db98367a2f8beb41f72dbf0859b436f83e35906aeafb4b1e914e396b67156b1e(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3e65034c958e784b624a75893bca70050fe134674033b65787f79fdeacc946(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84163819879cc956ced8ed6cc3f92a6afca09998fab7dfd982cebd82ff4384dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8728cd3ee45509b2aa82b840983f64721e92efee125aaa9a230b0189e06bff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9037cff93eea5759e225f34c2b618c7506e930bf4926dc2a9000c0e101bad81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd28ae43856b436ffceb9a858285fa9ed5b5b72892c2ec482b75a343a536676f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef72a9cb097b204aa488c8b3186e12a314310743fd23b9ae6bbff20e74806154(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac4eb20620da5c4cb3d5eb3d4964f323ceba56cb9878ed956a319c2c0b73386(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46aaa5df76710708e8465e5883eb781f0f1c1e4b542b577851d2b1426ee2ebc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950989626d1606a090f7ba2a8317ce1156e6f3e6c4d8cf5d0faf6badd60ba89b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205dffde5ed73ce50905cf6f17210affa1188916bd48863cbbdeaa19d2e09eed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dd8c6776d5efbff7f783d986304aa3244d2358797ae5ed21629c5c2bd18fe0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37973d3dca2f66e2bbd5befc05edf3a2b78919aa8dbbc7e9ef4ed8d9ba84bf27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584733789b609ceaf1c2e4384d69f3ebc250b87904e2a9fe56a9a695d0f53683(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272854963e7a1a6f9c839ebc4d0a91906ca4e5bfcf1f54648e7d9fb4d17c43c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e049a6a6ff14d317c6d374465c6c1309f1ec4523f205816e3d88388d88934ebf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e076a1103915174640cc59120391a0ff9dccb4cac2bbd1ea28042d8c2eb2770b(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da232fc9e3a50e162423433a5633d072213cb6274a2e443acbf144c50c4c151(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa33fe4b37cd9e1be3d37b6aaf224c64e9653cd7fda0e8e4cc79dd9b503f1dcc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7304577167748b8aa034d9543e15242def966903e6c594f2efffabeb681c47d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a12c8424c49deb8d1b8c258c7089c87e81ec8b45317d036430b6c996d06942(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79736303938b76e3443ba591d862cbb21c8f42c434f72bad21bdf87e1042ca4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42dfd32299ed7d5bc687bf9642034698121129b8e621a7a1858e7aafccd3616(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db57c86b10e92168660751815a9f882eb510f7d5c1af7ac39bb7444c3892969c(
    *,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8341ce0361fddca08264f7deef0919600b86e3b685fceb70156bb08060c81d4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f1c3c840beae6281631585ad3d966f9f7c94173e924fbb5ec8abcaf6ca116f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cef55eab9a6e237d537e018793325d60093f033ae3f932464f51b0534367e8f(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecContainersStartupProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721d9512885423698a41477887e281e4584e5d046fe340f5288f477a4d3c3dae(
    *,
    mount_path: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd54142112cb267ddb3d69a6165f4f14b6789d00d0557dad445e2a3f54045355(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88309848f7b1339d5dec3f20f7734621bcea6d4178770cbf55cbf644413799f2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdaf2e5f011531268c7add1dcb6e68b29e0d7799967f03f397d79dd8bc918bee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5ba62211f04b37e00d9877b1a2d7a599f98b74c9e96af59cedab13f976fd09(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7aea3182a9e6ab349f8ddbf394543dda839e79f8a8e69ac65a95d75d931ae8a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4d7120e3690825d9844026990eed496a24c53db6b45a2af5c72c617730b94a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecContainersVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685d6a1af64396a3b70d50b976b6440abd0608141d15308952654187bec8d4fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6311a078abe5a2bf959f9355a960bd3d0d3b8c67ea0cd3200ea90d8538b3db7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f66457a0becd190f5bca92c911fec983b0cad3b4d7a88e2f46de95eb53d00a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3931250160491189b716a43fbdfc0ae7387588ff961e6e4132ac32445c641d38(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecContainersVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e47a9e16a8a12e074f55c04fad59e89c7b195bdd8ea355886642a22f7a9f61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f53117791bf97337c420a6bc3e79619ba4fae874c2b6a8445aac3e0cbbf854d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecContainers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7516fc8b50a7ac1c76c594373d93a5041c999a42fdb565893c865b416bad66c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aecd3e9630859a5e25dfd43c28f05474c5e59cefbc6b945fed7532f652635ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26fefb31684380f296298d03aded484d1edd316a5c644a96166756b7bc3e94c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc63a0b0ebfa3a4381d0734e6869ea7d93bb63575f0419ef9fe4aea448fea9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4aefc524f62e0b6c3325b831fb0836d6f12241d2b4df81c995cda08d5e42b4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4533c470889376fa51e45fc3618f6c6d9fdc377e5f0341b14b4a949c18cb7ee(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59a67e677535f56a315858587dd85577965b47e649cfec91f55c40954975a9f(
    *,
    name: builtins.str,
    csi: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecVolumesCsi, typing.Dict[builtins.str, typing.Any]]] = None,
    empty_dir: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecVolumesEmptyDir, typing.Dict[builtins.str, typing.Any]]] = None,
    nfs: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecVolumesNfs, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[GoogleCloudRunServiceTemplateSpecVolumesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1402a2a54ecd74b32ca3445f537beba4338f66ab864447500aff186aa63fb0(
    *,
    driver: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    volume_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3694709379e781204cde7eb96bb6a4e25ddc959b918d9aa1d369ef47b6d59a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd78a7b65e6145b75f4ecaecfe9cb0eece8d4d6103230184b89acd3a3b085d47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af5628f3352f3202e206afae61c6527853d5291decf43acae4a7b4b5afe85cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5246afb86775452e4822ce97e7b242ac332b15c9bcd8f0297190e5a44d2648(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db7e57a18946a95c5344c28dfbedc101b9f10cb402c7e9c1a55238ad30da926(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesCsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3faaac1adddb005a4a795b0ed570f50e5b8b6d3513fa2dae97afa57c5927798e(
    *,
    medium: typing.Optional[builtins.str] = None,
    size_limit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca61045155edf8e998e796cc67a2161e0407e8952493c043bd19c8218817b139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d00cc391b0c8f6802431701ebd114fa9d5804f5339040d41e5f132e5df52c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4dd9589ab2bf8ca312252c6f505a5a36b831fdc999282ea41020e08f020c1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6eca628c9dcf4db98918304f27aa82dbb6a95eef4d425c7271ed4b999066d4(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesEmptyDir],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c57bf04100cfb154648a7d527b38a871ea27fc4e0817ba476b1f91bef636080(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9604611b37670d975e812f4367e6693fe9c43c13d058e3cfae43ff96f8ff7c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86acbe1f4bfeaa0b399584d45a5150dd4c40afb21c16728bfdba4a48121ba204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e5a286e32396e9113d2a81a0bd7929e7ad452b380b5f9d977598df9da1ca84(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13504d64e353b701f40a35ee936aae228839509e0735a3db509d232e1879731(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fa450e7b85d71374d26eda9efc082e19b6aea0a719990f76c36c2ab127302c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f29cd43c1935383e172ab695b3993709d9caeef7627e80d8508ffd9ff0c6c74(
    *,
    path: builtins.str,
    server: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7495da1c4a66596ea96a6cb5eeaa7ec44d54570eaebcd2de14de61a8b65a145a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce18e5c99aa93b07dd738cb29aa005f51c373d72778f7becba71a290d5fec092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2233eef865191f5e53a3a9e5535f501b386bfdf604173673e688d84dd84dbbac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098242fdd54c394d405c142f9c99afa9fe59331670c0620d6e312e066ac09762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b570f30c018f8f799fd5e6bd915e34cf1694f15f877c82f7c67fb9b169ba3ca(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesNfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6324bb4f7be710443c393a8f1c019117ab2c6834d4dc62e420397460f0f8a0d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690f5d5dfbc9e7d16834238961d3ce319783cafd4550fe97cf215ca62ed554b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc4d4f009b3ad2e32d30ddc3c1216a4c53edd9fe9d4160ee82cd134f6cadd28(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d43342828fdc9f57ec70fef882d7c16523dc1bf833e93b2033ad1cb3f5d81f4(
    *,
    secret_name: builtins.str,
    default_mode: typing.Optional[jsii.Number] = None,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f1eb31394e3ee9fb53dcc4375da57b6b76e33416c5d973bde24dee753463ed(
    *,
    key: builtins.str,
    path: builtins.str,
    mode: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8ba654c6706d7362293a160cde863900934a31f4cda778e8c7d4c7b5c844f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42c519dd8db5205cec2cf9d5be5fbbce84b4a2e7902b7c55c75a3c893cb877b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac64ea96963be7a6e23ff7ef63629f80caee7128d3005b9adfc9d7856e43861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de32fbfe4120ccd4b2dce52c44af5e77950c8320fe6aaba0d4e83ed84d3f2478(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31c38af5ca19481a94716a8a72d5bdf7dce2a4183757476be264a78f7150244(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbbed8f2a34ea17e69a7f8bafd2e97941c18997e59fad9d7e15d396994f7ca6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTemplateSpecVolumesSecretItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2aa650325201e6f3c9629368d4c058bb92c4b312309dcd2b1d34123334694ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685d157b368f36c4340313bb500b3c8f49588a67502616376b713a875c14a5f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bb1828f9acb9d64821f155b419ad7fb2246ccdbf9548271b49dc2440e39178(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754754dd75a2e6c3f57dfd6ce651a549431ca6a33e0e150de11c0dd9f8e1486e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f995cd3fd5648ca014cb016089d707fd0368aaf0f7db0bc65ff50a2f8d4397(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTemplateSpecVolumesSecretItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a950a3314d022f1ffa18b8b29981b168cb7b6145f7d8b1887d7d610fbeb418(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d304151f74fa6e2d826b64e763f8ecb1a00d4628cd8334da5bca4b08e805fc4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunServiceTemplateSpecVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4283b82fa216c140683cdde0cdf5d983584a314290c3b80098cbfdc7e093f942(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07cb2126e5052a951803bf48125c543fe021011b858dab5e92289e2e7d510038(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb6e8a01c888948bccd0f56002495c80c442a5c5581e338b08135e1c1b979a9(
    value: typing.Optional[GoogleCloudRunServiceTemplateSpecVolumesSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1958a5da499f06ef1bac80cbe16d8eaea154765ae76eb9fc7156049ed23ea4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c01ff3dec53ce411ba596cc0af5640a28ab9f0d5f9258e1d473a936bc708fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d5fa9d2473d0ec8c3f2bd1dd90b39e765793ada7cad93ae359cfeb3bd324cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0d02e9b1d2fa22d4037828188214c24ba4798fdab33d478d5e2603cf0ea848(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25410ba0596337a5b079cc15a7a0a2eeefb242c9e3703a75d78325dad7002dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4e86fa72307edb0bebfef9bdd75f4a7ec8fe0a4d952b33b52f76ae04db0ba4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3370043868e96bbc63a9f06677c1850c4173da6b8f9b41b833e465830e800f34(
    *,
    percent: jsii.Number,
    latest_revision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    revision_name: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c8f6446d256071325af68bf9ab3cf569c7ff752d8c509daae70099cadea8f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e214c9a0afe37d6a242f69d3f1c990ccc187895c59de02e4ea2b6ebfe95e2d71(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32261dd292a640095fbdc14d0988918ab55b55a8690d7d43e8e706005d03efd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbc951ff76bbd18d23f39c144caef96930c0f829609c2e5206e342a1b73d14e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8681f494cca7c8da846bd0bd2d43d1d5872779b4daa3aca6a147a7768829e2f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5880587b906b9876fde2b5ba2f0cc98c4e5a461e7d7f6149e5b11e5681130f20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunServiceTraffic]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfc810e9252cf401d02f7cbec935c100d24396aeb62a1a75dfb395f92c4f092(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4421183bd3ebb1e74a3e2551992edfaef77dfd1a7d005fa4ac47daaafa7df0b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89dea73bf96d6d8bcf0f00e72aba7ebf2fbd442ac22f869e64ef20c361ed865e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31c45971f362d3c528dfcc78863a5d5370b4460a5deb8e498ad0275bd9c1dce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84fdfb65f7d92c2dc2de79a9b7c3af3116a47ce300221e6af3c3a87792e2c5ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd867cb1baaaf82e5fd6e69fcf6c242d1da23d58db95c1fef5ec9328ec048cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunServiceTraffic]],
) -> None:
    """Type checking stubs"""
    pass
