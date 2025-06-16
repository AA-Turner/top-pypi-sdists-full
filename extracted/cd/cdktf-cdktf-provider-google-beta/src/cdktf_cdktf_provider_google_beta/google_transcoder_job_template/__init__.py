r'''
# `google_transcoder_job_template`

Refer to the Terraform Registry for docs: [`google_transcoder_job_template`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template).
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


class GoogleTranscoderJobTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template google_transcoder_job_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        job_template_id: builtins.str,
        location: builtins.str,
        config: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleTranscoderJobTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template google_transcoder_job_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param job_template_id: ID to use for the Transcoding job template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#job_template_id GoogleTranscoderJobTemplate#job_template_id}
        :param location: The location of the transcoding job template resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#location GoogleTranscoderJobTemplate#location}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#config GoogleTranscoderJobTemplate#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#id GoogleTranscoderJobTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this job template. You can use these to organize and group your job templates. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#labels GoogleTranscoderJobTemplate#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#project GoogleTranscoderJobTemplate#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#timeouts GoogleTranscoderJobTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4f17b171551d51cc1b1d55d96641a1e0834f51b667c2e06d9f17070907ed4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = GoogleTranscoderJobTemplateConfig(
            job_template_id=job_template_id,
            location=location,
            config=config,
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

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a GoogleTranscoderJobTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleTranscoderJobTemplate to import.
        :param import_from_id: The id of the existing GoogleTranscoderJobTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleTranscoderJobTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8f8616519348bc1f1e4bd1afdbcb9475b6055344a7ffc2547a549a5607ae92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigInputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigManifests", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigOverlays", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pubsub_destination: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_breaks: ad_breaks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#ad_breaks GoogleTranscoderJobTemplate#ad_breaks}
        :param edit_list: edit_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#edit_list GoogleTranscoderJobTemplate#edit_list}
        :param elementary_streams: elementary_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#elementary_streams GoogleTranscoderJobTemplate#elementary_streams}
        :param encryptions: encryptions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#encryptions GoogleTranscoderJobTemplate#encryptions}
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#inputs GoogleTranscoderJobTemplate#inputs}
        :param manifests: manifests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#manifests GoogleTranscoderJobTemplate#manifests}
        :param mux_streams: mux_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#mux_streams GoogleTranscoderJobTemplate#mux_streams}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#output GoogleTranscoderJobTemplate#output}
        :param overlays: overlays block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#overlays GoogleTranscoderJobTemplate#overlays}
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#pubsub_destination GoogleTranscoderJobTemplate#pubsub_destination}
        '''
        value = GoogleTranscoderJobTemplateConfigA(
            ad_breaks=ad_breaks,
            edit_list=edit_list,
            elementary_streams=elementary_streams,
            encryptions=encryptions,
            inputs=inputs,
            manifests=manifests,
            mux_streams=mux_streams,
            output=output,
            overlays=overlays,
            pubsub_destination=pubsub_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#create GoogleTranscoderJobTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#delete GoogleTranscoderJobTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#update GoogleTranscoderJobTemplate#update}.
        '''
        value = GoogleTranscoderJobTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

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
    @jsii.member(jsii_name="config")
    def config(self) -> "GoogleTranscoderJobTemplateConfigAOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleTranscoderJobTemplateTimeoutsOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["GoogleTranscoderJobTemplateConfigA"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTemplateIdInput")
    def job_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobTemplateIdInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleTranscoderJobTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleTranscoderJobTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ec0e68ba7587540a7c9d3158086554a5dfd0348bebadbe540b6f2b976b24f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobTemplateId")
    def job_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobTemplateId"))

    @job_template_id.setter
    def job_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2338cdcfc0779706570fd153fa794af7eaeb4a05164a3b58247b247a74e8528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobTemplateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca590331e648758d43d0c821ee42fa55fb2a3d12b2317b948a620555eb60169d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2234994cd7e74a2811d362aad8452bf8b0a198c036be114d4cc30f320eb751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e38cfcf5860e17d7943d99ab54827bb7508a693f1c8414d25290682be9e82fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "job_template_id": "jobTemplateId",
        "location": "location",
        "config": "config",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleTranscoderJobTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        job_template_id: builtins.str,
        location: builtins.str,
        config: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleTranscoderJobTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param job_template_id: ID to use for the Transcoding job template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#job_template_id GoogleTranscoderJobTemplate#job_template_id}
        :param location: The location of the transcoding job template resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#location GoogleTranscoderJobTemplate#location}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#config GoogleTranscoderJobTemplate#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#id GoogleTranscoderJobTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this job template. You can use these to organize and group your job templates. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#labels GoogleTranscoderJobTemplate#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#project GoogleTranscoderJobTemplate#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#timeouts GoogleTranscoderJobTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = GoogleTranscoderJobTemplateConfigA(**config)
        if isinstance(timeouts, dict):
            timeouts = GoogleTranscoderJobTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49c0d212aa10ba6dbc85c20a6cbbcffd8b574005d0f00e551e37798601c78e3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument job_template_id", value=job_template_id, expected_type=type_hints["job_template_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_template_id": job_template_id,
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
        if config is not None:
            self._values["config"] = config
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
    def job_template_id(self) -> builtins.str:
        '''ID to use for the Transcoding job template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#job_template_id GoogleTranscoderJobTemplate#job_template_id}
        '''
        result = self._values.get("job_template_id")
        assert result is not None, "Required property 'job_template_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the transcoding job template resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#location GoogleTranscoderJobTemplate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["GoogleTranscoderJobTemplateConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#config GoogleTranscoderJobTemplate#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#id GoogleTranscoderJobTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels associated with this job template. You can use these to organize and group your job templates.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#labels GoogleTranscoderJobTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#project GoogleTranscoderJobTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleTranscoderJobTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#timeouts GoogleTranscoderJobTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "ad_breaks": "adBreaks",
        "edit_list": "editList",
        "elementary_streams": "elementaryStreams",
        "encryptions": "encryptions",
        "inputs": "inputs",
        "manifests": "manifests",
        "mux_streams": "muxStreams",
        "output": "output",
        "overlays": "overlays",
        "pubsub_destination": "pubsubDestination",
    },
)
class GoogleTranscoderJobTemplateConfigA:
    def __init__(
        self,
        *,
        ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigInputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigManifests", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigOverlays", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pubsub_destination: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_breaks: ad_breaks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#ad_breaks GoogleTranscoderJobTemplate#ad_breaks}
        :param edit_list: edit_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#edit_list GoogleTranscoderJobTemplate#edit_list}
        :param elementary_streams: elementary_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#elementary_streams GoogleTranscoderJobTemplate#elementary_streams}
        :param encryptions: encryptions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#encryptions GoogleTranscoderJobTemplate#encryptions}
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#inputs GoogleTranscoderJobTemplate#inputs}
        :param manifests: manifests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#manifests GoogleTranscoderJobTemplate#manifests}
        :param mux_streams: mux_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#mux_streams GoogleTranscoderJobTemplate#mux_streams}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#output GoogleTranscoderJobTemplate#output}
        :param overlays: overlays block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#overlays GoogleTranscoderJobTemplate#overlays}
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#pubsub_destination GoogleTranscoderJobTemplate#pubsub_destination}
        '''
        if isinstance(output, dict):
            output = GoogleTranscoderJobTemplateConfigOutput(**output)
        if isinstance(pubsub_destination, dict):
            pubsub_destination = GoogleTranscoderJobTemplateConfigPubsubDestination(**pubsub_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac7696d23bb024e9ffbab187a2cb6f3bbff533be14dac917e883371265f3f5c)
            check_type(argname="argument ad_breaks", value=ad_breaks, expected_type=type_hints["ad_breaks"])
            check_type(argname="argument edit_list", value=edit_list, expected_type=type_hints["edit_list"])
            check_type(argname="argument elementary_streams", value=elementary_streams, expected_type=type_hints["elementary_streams"])
            check_type(argname="argument encryptions", value=encryptions, expected_type=type_hints["encryptions"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument manifests", value=manifests, expected_type=type_hints["manifests"])
            check_type(argname="argument mux_streams", value=mux_streams, expected_type=type_hints["mux_streams"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument overlays", value=overlays, expected_type=type_hints["overlays"])
            check_type(argname="argument pubsub_destination", value=pubsub_destination, expected_type=type_hints["pubsub_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ad_breaks is not None:
            self._values["ad_breaks"] = ad_breaks
        if edit_list is not None:
            self._values["edit_list"] = edit_list
        if elementary_streams is not None:
            self._values["elementary_streams"] = elementary_streams
        if encryptions is not None:
            self._values["encryptions"] = encryptions
        if inputs is not None:
            self._values["inputs"] = inputs
        if manifests is not None:
            self._values["manifests"] = manifests
        if mux_streams is not None:
            self._values["mux_streams"] = mux_streams
        if output is not None:
            self._values["output"] = output
        if overlays is not None:
            self._values["overlays"] = overlays
        if pubsub_destination is not None:
            self._values["pubsub_destination"] = pubsub_destination

    @builtins.property
    def ad_breaks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigAdBreaks"]]]:
        '''ad_breaks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#ad_breaks GoogleTranscoderJobTemplate#ad_breaks}
        '''
        result = self._values.get("ad_breaks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigAdBreaks"]]], result)

    @builtins.property
    def edit_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigEditListStruct"]]]:
        '''edit_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#edit_list GoogleTranscoderJobTemplate#edit_list}
        '''
        result = self._values.get("edit_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigEditListStruct"]]], result)

    @builtins.property
    def elementary_streams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigElementaryStreams"]]]:
        '''elementary_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#elementary_streams GoogleTranscoderJobTemplate#elementary_streams}
        '''
        result = self._values.get("elementary_streams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigElementaryStreams"]]], result)

    @builtins.property
    def encryptions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigEncryptions"]]]:
        '''encryptions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#encryptions GoogleTranscoderJobTemplate#encryptions}
        '''
        result = self._values.get("encryptions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigEncryptions"]]], result)

    @builtins.property
    def inputs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigInputs"]]]:
        '''inputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#inputs GoogleTranscoderJobTemplate#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigInputs"]]], result)

    @builtins.property
    def manifests(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigManifests"]]]:
        '''manifests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#manifests GoogleTranscoderJobTemplate#manifests}
        '''
        result = self._values.get("manifests")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigManifests"]]], result)

    @builtins.property
    def mux_streams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigMuxStreams"]]]:
        '''mux_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#mux_streams GoogleTranscoderJobTemplate#mux_streams}
        '''
        result = self._values.get("mux_streams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigMuxStreams"]]], result)

    @builtins.property
    def output(self) -> typing.Optional["GoogleTranscoderJobTemplateConfigOutput"]:
        '''output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#output GoogleTranscoderJobTemplate#output}
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigOutput"], result)

    @builtins.property
    def overlays(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigOverlays"]]]:
        '''overlays block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#overlays GoogleTranscoderJobTemplate#overlays}
        '''
        result = self._values.get("overlays")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigOverlays"]]], result)

    @builtins.property
    def pubsub_destination(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigPubsubDestination"]:
        '''pubsub_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#pubsub_destination GoogleTranscoderJobTemplate#pubsub_destination}
        '''
        result = self._values.get("pubsub_destination")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigPubsubDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc15465606740a48ae3ca8131d25b95e29bceb1c01b2f078345a9023a430e59d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdBreaks")
    def put_ad_breaks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bdd864dc9333d85ee8444271a75a6c3b04e027b56226f577ac14f31ced94e9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdBreaks", [value]))

    @jsii.member(jsii_name="putEditList")
    def put_edit_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0386e902ec08410e4c9204f5a7401a94eb94cfb0f33540884a07732495f77c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEditList", [value]))

    @jsii.member(jsii_name="putElementaryStreams")
    def put_elementary_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda44e96cc1360a263b262153ae14ad080e7ea227a73ed72b866e16a818a6218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElementaryStreams", [value]))

    @jsii.member(jsii_name="putEncryptions")
    def put_encryptions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30ff52d147da2d915460141c672ab7d756b49d13a1f7c7272ed80ab046e8a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEncryptions", [value]))

    @jsii.member(jsii_name="putInputs")
    def put_inputs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigInputs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157a1dd1920af133d8079deb54eda891c122d398b903e2516a27222c016437bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputs", [value]))

    @jsii.member(jsii_name="putManifests")
    def put_manifests(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigManifests", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc6f39b6c8caa1df8ba845ff4d2e64c9980053aee71d904dfc57d13525c35ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManifests", [value]))

    @jsii.member(jsii_name="putMuxStreams")
    def put_mux_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671e74d7c5c59df922ee844abe86e643b75bc5de9765c771a38899fc02ace595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMuxStreams", [value]))

    @jsii.member(jsii_name="putOutput")
    def put_output(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: URI for the output file(s). For example, gs://my-bucket/outputs/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#uri GoogleTranscoderJobTemplate#uri}
        '''
        value = GoogleTranscoderJobTemplateConfigOutput(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putOutput", [value]))

    @jsii.member(jsii_name="putOverlays")
    def put_overlays(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigOverlays", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcabaad0cdc159ea4a9b51d60ffb79a296ebba5ed5ca4e73a2bd91a8a32f338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOverlays", [value]))

    @jsii.member(jsii_name="putPubsubDestination")
    def put_pubsub_destination(
        self,
        *,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic: The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#topic GoogleTranscoderJobTemplate#topic}
        '''
        value = GoogleTranscoderJobTemplateConfigPubsubDestination(topic=topic)

        return typing.cast(None, jsii.invoke(self, "putPubsubDestination", [value]))

    @jsii.member(jsii_name="resetAdBreaks")
    def reset_ad_breaks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdBreaks", []))

    @jsii.member(jsii_name="resetEditList")
    def reset_edit_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEditList", []))

    @jsii.member(jsii_name="resetElementaryStreams")
    def reset_elementary_streams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElementaryStreams", []))

    @jsii.member(jsii_name="resetEncryptions")
    def reset_encryptions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptions", []))

    @jsii.member(jsii_name="resetInputs")
    def reset_inputs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputs", []))

    @jsii.member(jsii_name="resetManifests")
    def reset_manifests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManifests", []))

    @jsii.member(jsii_name="resetMuxStreams")
    def reset_mux_streams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMuxStreams", []))

    @jsii.member(jsii_name="resetOutput")
    def reset_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutput", []))

    @jsii.member(jsii_name="resetOverlays")
    def reset_overlays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverlays", []))

    @jsii.member(jsii_name="resetPubsubDestination")
    def reset_pubsub_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubsubDestination", []))

    @builtins.property
    @jsii.member(jsii_name="adBreaks")
    def ad_breaks(self) -> "GoogleTranscoderJobTemplateConfigAdBreaksList":
        return typing.cast("GoogleTranscoderJobTemplateConfigAdBreaksList", jsii.get(self, "adBreaks"))

    @builtins.property
    @jsii.member(jsii_name="editList")
    def edit_list(self) -> "GoogleTranscoderJobTemplateConfigEditListStructList":
        return typing.cast("GoogleTranscoderJobTemplateConfigEditListStructList", jsii.get(self, "editList"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreams")
    def elementary_streams(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigElementaryStreamsList":
        return typing.cast("GoogleTranscoderJobTemplateConfigElementaryStreamsList", jsii.get(self, "elementaryStreams"))

    @builtins.property
    @jsii.member(jsii_name="encryptions")
    def encryptions(self) -> "GoogleTranscoderJobTemplateConfigEncryptionsList":
        return typing.cast("GoogleTranscoderJobTemplateConfigEncryptionsList", jsii.get(self, "encryptions"))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> "GoogleTranscoderJobTemplateConfigInputsList":
        return typing.cast("GoogleTranscoderJobTemplateConfigInputsList", jsii.get(self, "inputs"))

    @builtins.property
    @jsii.member(jsii_name="manifests")
    def manifests(self) -> "GoogleTranscoderJobTemplateConfigManifestsList":
        return typing.cast("GoogleTranscoderJobTemplateConfigManifestsList", jsii.get(self, "manifests"))

    @builtins.property
    @jsii.member(jsii_name="muxStreams")
    def mux_streams(self) -> "GoogleTranscoderJobTemplateConfigMuxStreamsList":
        return typing.cast("GoogleTranscoderJobTemplateConfigMuxStreamsList", jsii.get(self, "muxStreams"))

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> "GoogleTranscoderJobTemplateConfigOutputOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigOutputOutputReference", jsii.get(self, "output"))

    @builtins.property
    @jsii.member(jsii_name="overlays")
    def overlays(self) -> "GoogleTranscoderJobTemplateConfigOverlaysList":
        return typing.cast("GoogleTranscoderJobTemplateConfigOverlaysList", jsii.get(self, "overlays"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestination")
    def pubsub_destination(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigPubsubDestinationOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigPubsubDestinationOutputReference", jsii.get(self, "pubsubDestination"))

    @builtins.property
    @jsii.member(jsii_name="adBreaksInput")
    def ad_breaks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigAdBreaks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigAdBreaks"]]], jsii.get(self, "adBreaksInput"))

    @builtins.property
    @jsii.member(jsii_name="editListInput")
    def edit_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigEditListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigEditListStruct"]]], jsii.get(self, "editListInput"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreamsInput")
    def elementary_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigElementaryStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigElementaryStreams"]]], jsii.get(self, "elementaryStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionsInput")
    def encryptions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigEncryptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigEncryptions"]]], jsii.get(self, "encryptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigInputs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigInputs"]]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestsInput")
    def manifests_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigManifests"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigManifests"]]], jsii.get(self, "manifestsInput"))

    @builtins.property
    @jsii.member(jsii_name="muxStreamsInput")
    def mux_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigMuxStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigMuxStreams"]]], jsii.get(self, "muxStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="outputInput")
    def output_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigOutput"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigOutput"], jsii.get(self, "outputInput"))

    @builtins.property
    @jsii.member(jsii_name="overlaysInput")
    def overlays_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigOverlays"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigOverlays"]]], jsii.get(self, "overlaysInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestinationInput")
    def pubsub_destination_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigPubsubDestination"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigPubsubDestination"], jsii.get(self, "pubsubDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleTranscoderJobTemplateConfigA]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc08d868a2eef28d2b0c5ba8b2acfc64a8985b52a84939d07b6b628cc13e55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigAdBreaks",
    jsii_struct_bases=[],
    name_mapping={"start_time_offset": "startTimeOffset"},
)
class GoogleTranscoderJobTemplateConfigAdBreaks:
    def __init__(
        self,
        *,
        start_time_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_time_offset: Start time in seconds for the ad break, relative to the output file timeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#start_time_offset GoogleTranscoderJobTemplate#start_time_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4b02b79c23aeb4fe9646fa69509ac5699d9df62d9c9cd1b26157a388a231e6)
            check_type(argname="argument start_time_offset", value=start_time_offset, expected_type=type_hints["start_time_offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if start_time_offset is not None:
            self._values["start_time_offset"] = start_time_offset

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''Start time in seconds for the ad break, relative to the output file timeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#start_time_offset GoogleTranscoderJobTemplate#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigAdBreaks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigAdBreaksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigAdBreaksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c17c4f82937c53ad216e7687d2afd871df18cd90d5af69d0cf7fc38b8e3ddcb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigAdBreaksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923ff92946a72fd216f1f9eaa622e17580744a190957261076c28173ade99089)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigAdBreaksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ea22876b5963d71a9f41e5f251975fa90683215afbc2890488c7a497caeb7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecfbc4905530c70915f72dc8f8e30d86c3be6ca1e75587c0f9ac6e34fb5a8aa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82c8980da4079294d8e13c0c4761aef8d102b05ec2ed78068a51c0d89106f503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigAdBreaks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigAdBreaks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigAdBreaks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d385f218dc177ff5b9bb815867ef92776eb54c6904c3af66625263a2841516d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigAdBreaksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigAdBreaksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__917d709f39e7373f6e6ab4954157f647f871da181129e1c7ad1570a16ae2124c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStartTimeOffset")
    def reset_start_time_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimeOffset", []))

    @builtins.property
    @jsii.member(jsii_name="startTimeOffsetInput")
    def start_time_offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028a2ceec547f30f2d29fabaec5c57b7cea9cbd64247027d64fd3ff05744671f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigAdBreaks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigAdBreaks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigAdBreaks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f97d43de025782272a83bd2571e7f21628b26fd3dca240e48e27b437cffc57b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEditListStruct",
    jsii_struct_bases=[],
    name_mapping={
        "inputs": "inputs",
        "key": "key",
        "start_time_offset": "startTimeOffset",
    },
)
class GoogleTranscoderJobTemplateConfigEditListStruct:
    def __init__(
        self,
        *,
        inputs: typing.Optional[typing.Sequence[builtins.str]] = None,
        key: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inputs: List of values identifying files that should be used in this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#inputs GoogleTranscoderJobTemplate#inputs}
        :param key: A unique key for this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#key GoogleTranscoderJobTemplate#key}
        :param start_time_offset: Start time in seconds for the atom, relative to the input file timeline. The default is '0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#start_time_offset GoogleTranscoderJobTemplate#start_time_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fe2bfbb2b9ab3eee71ecfc28c9e78caf4b4c8b789cb2fa4797b3eeee2d7b27)
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument start_time_offset", value=start_time_offset, expected_type=type_hints["start_time_offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inputs is not None:
            self._values["inputs"] = inputs
        if key is not None:
            self._values["key"] = key
        if start_time_offset is not None:
            self._values["start_time_offset"] = start_time_offset

    @builtins.property
    def inputs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values identifying files that should be used in this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#inputs GoogleTranscoderJobTemplate#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#key GoogleTranscoderJobTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''Start time in seconds for the atom, relative to the input file timeline.  The default is '0s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#start_time_offset GoogleTranscoderJobTemplate#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEditListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEditListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEditListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__409bde7b1316629c094c4ba331336b4939a4e433b1ad9e12f8c156756773654f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigEditListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebdf7a4257e166cd53b6f833fa33d3b4b1d975f1c1c83054662f6093a905cb4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigEditListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b474b6a39f9e68e7e2c25d819c07c3a2409621e642a6da9e17aab6d7967e5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af5bd1f3d26154b824aaf68d3373fff596de7b50b41890cab913f157f8d897b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeabd1aa5ab336bdb0362fd1e65af23c0e67b73ba799d4334d912dfac3679a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigEditListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigEditListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigEditListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebea8a4c16a1d9ff1d2a4143b144db74896179789a1461a30c325d78b7eb6928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigEditListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEditListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__802a84afe7f35fe5c8cee7f37dfe53c2e4417624029ae80256aa01c7493bfe8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInputs")
    def reset_inputs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputs", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetStartTimeOffset")
    def reset_start_time_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimeOffset", []))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOffsetInput")
    def start_time_offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887f8492ab5f783d36f892249625e388251f213b059446264c38b7912ebc356c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d304f9a6acdbdf58adafc7ad9dd030a979c4d54c733fa10c2448a012b548095b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a32759d21861075d543fc33c707be659c7942042815912af836d25b91dda32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigEditListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigEditListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigEditListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b5bd2b17907de50090b8462a49e09dc2b9a9d879746312e681d2ee0b611c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreams",
    jsii_struct_bases=[],
    name_mapping={
        "audio_stream": "audioStream",
        "key": "key",
        "video_stream": "videoStream",
    },
)
class GoogleTranscoderJobTemplateConfigElementaryStreams:
    def __init__(
        self,
        *,
        audio_stream: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream", typing.Dict[builtins.str, typing.Any]]] = None,
        key: typing.Optional[builtins.str] = None,
        video_stream: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_stream: audio_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#audio_stream GoogleTranscoderJobTemplate#audio_stream}
        :param key: A unique key for this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#key GoogleTranscoderJobTemplate#key}
        :param video_stream: video_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#video_stream GoogleTranscoderJobTemplate#video_stream}
        '''
        if isinstance(audio_stream, dict):
            audio_stream = GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream(**audio_stream)
        if isinstance(video_stream, dict):
            video_stream = GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream(**video_stream)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9365d4f036b59438abdcac0404980a5757db8aa4db677f17ab84d2e06b0a5df6)
            check_type(argname="argument audio_stream", value=audio_stream, expected_type=type_hints["audio_stream"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument video_stream", value=video_stream, expected_type=type_hints["video_stream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_stream is not None:
            self._values["audio_stream"] = audio_stream
        if key is not None:
            self._values["key"] = key
        if video_stream is not None:
            self._values["video_stream"] = video_stream

    @builtins.property
    def audio_stream(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream"]:
        '''audio_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#audio_stream GoogleTranscoderJobTemplate#audio_stream}
        '''
        result = self._values.get("audio_stream")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream"], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#key GoogleTranscoderJobTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def video_stream(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream"]:
        '''video_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#video_stream GoogleTranscoderJobTemplate#video_stream}
        '''
        result = self._values.get("video_stream")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigElementaryStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream",
    jsii_struct_bases=[],
    name_mapping={
        "bitrate_bps": "bitrateBps",
        "channel_count": "channelCount",
        "channel_layout": "channelLayout",
        "codec": "codec",
        "sample_rate_hertz": "sampleRateHertz",
    },
)
class GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream:
    def __init__(
        self,
        *,
        bitrate_bps: jsii.Number,
        channel_count: typing.Optional[jsii.Number] = None,
        channel_layout: typing.Optional[typing.Sequence[builtins.str]] = None,
        codec: typing.Optional[builtins.str] = None,
        sample_rate_hertz: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: Audio bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#bitrate_bps GoogleTranscoderJobTemplate#bitrate_bps}
        :param channel_count: Number of audio channels. The default is '2'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#channel_count GoogleTranscoderJobTemplate#channel_count}
        :param channel_layout: A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#channel_layout GoogleTranscoderJobTemplate#channel_layout}
        :param codec: The codec for this audio stream. The default is 'aac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#codec GoogleTranscoderJobTemplate#codec}
        :param sample_rate_hertz: The audio sample rate in Hertz. The default is '48000'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#sample_rate_hertz GoogleTranscoderJobTemplate#sample_rate_hertz}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f20a89c23a527ece35d2fe46214ed6493be169fda0c00ef90e87d0531e4028f)
            check_type(argname="argument bitrate_bps", value=bitrate_bps, expected_type=type_hints["bitrate_bps"])
            check_type(argname="argument channel_count", value=channel_count, expected_type=type_hints["channel_count"])
            check_type(argname="argument channel_layout", value=channel_layout, expected_type=type_hints["channel_layout"])
            check_type(argname="argument codec", value=codec, expected_type=type_hints["codec"])
            check_type(argname="argument sample_rate_hertz", value=sample_rate_hertz, expected_type=type_hints["sample_rate_hertz"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bitrate_bps": bitrate_bps,
        }
        if channel_count is not None:
            self._values["channel_count"] = channel_count
        if channel_layout is not None:
            self._values["channel_layout"] = channel_layout
        if codec is not None:
            self._values["codec"] = codec
        if sample_rate_hertz is not None:
            self._values["sample_rate_hertz"] = sample_rate_hertz

    @builtins.property
    def bitrate_bps(self) -> jsii.Number:
        '''Audio bitrate in bits per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#bitrate_bps GoogleTranscoderJobTemplate#bitrate_bps}
        '''
        result = self._values.get("bitrate_bps")
        assert result is not None, "Required property 'bitrate_bps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def channel_count(self) -> typing.Optional[jsii.Number]:
        '''Number of audio channels. The default is '2'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#channel_count GoogleTranscoderJobTemplate#channel_count}
        '''
        result = self._values.get("channel_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def channel_layout(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of channel names specifying layout of the audio channels.  The default is ["fl", "fr"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#channel_layout GoogleTranscoderJobTemplate#channel_layout}
        '''
        result = self._values.get("channel_layout")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def codec(self) -> typing.Optional[builtins.str]:
        '''The codec for this audio stream. The default is 'aac'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#codec GoogleTranscoderJobTemplate#codec}
        '''
        result = self._values.get("codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate_hertz(self) -> typing.Optional[jsii.Number]:
        '''The audio sample rate in Hertz. The default is '48000'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#sample_rate_hertz GoogleTranscoderJobTemplate#sample_rate_hertz}
        '''
        result = self._values.get("sample_rate_hertz")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b0231d84419055313578ca9e071bdb496cf20cc3a578fc43658369a6f1cee0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChannelCount")
    def reset_channel_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannelCount", []))

    @jsii.member(jsii_name="resetChannelLayout")
    def reset_channel_layout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannelLayout", []))

    @jsii.member(jsii_name="resetCodec")
    def reset_codec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodec", []))

    @jsii.member(jsii_name="resetSampleRateHertz")
    def reset_sample_rate_hertz(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleRateHertz", []))

    @builtins.property
    @jsii.member(jsii_name="bitrateBpsInput")
    def bitrate_bps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bitrateBpsInput"))

    @builtins.property
    @jsii.member(jsii_name="channelCountInput")
    def channel_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "channelCountInput"))

    @builtins.property
    @jsii.member(jsii_name="channelLayoutInput")
    def channel_layout_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "channelLayoutInput"))

    @builtins.property
    @jsii.member(jsii_name="codecInput")
    def codec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codecInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleRateHertzInput")
    def sample_rate_hertz_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleRateHertzInput"))

    @builtins.property
    @jsii.member(jsii_name="bitrateBps")
    def bitrate_bps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bitrateBps"))

    @bitrate_bps.setter
    def bitrate_bps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc65baae4fbb73f981b2ff4e39b85acdb7956683e868dad7ce6a88d3c06d104f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitrateBps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelCount")
    def channel_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "channelCount"))

    @channel_count.setter
    def channel_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a547ae6d996aa833a09560f5ef5a35624934da75756822492c9dbc7fdc134076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelLayout")
    def channel_layout(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "channelLayout"))

    @channel_layout.setter
    def channel_layout(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b351ff1e7f4ab9c8fa41953d8e1c56c3f600e8e80e9341acb95f1a6eac0529c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelLayout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codec")
    def codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codec"))

    @codec.setter
    def codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f5e38012608ddab19bf34b1c3022663ba7736ab955dd4d6b7e98d8fba6deae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRateHertz")
    def sample_rate_hertz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRateHertz"))

    @sample_rate_hertz.setter
    def sample_rate_hertz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4075069a1e7351f4a4267811e4f44c13715bfaa34a3650477deb632a3f2f5913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRateHertz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca8ba51cdbf4833496d9361fc27b00c1eb685fa6102357d7960fb866693f11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigElementaryStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29cc14acbe063b7e27f35fb739eb78e6c5a3402555110cfac4d840971e48206c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigElementaryStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18aec9795e2073e1a265ba8586cdd548b6fe228157cf51db9e8f17e9d667073b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigElementaryStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cda6d7a029e8471c9c46a3f518f9f5cade777e25d9a8ed4371aa7ed5301c558)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e669ab5fccca9998ec594afdfb23011b13e59df5251ec6f571ad7624a03685d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__514b88417d291a8c0a5f8cf819acb94c2224dffba997e12de83c24c196086e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigElementaryStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigElementaryStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigElementaryStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c8c06d3e14dfc93024e136e3cdf6e10af100909c3da09ed0dc3280b01dbe50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigElementaryStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1990a4bc00b39328ad264b8f2068467688bca4b5df9aff44d30f8e97916697c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAudioStream")
    def put_audio_stream(
        self,
        *,
        bitrate_bps: jsii.Number,
        channel_count: typing.Optional[jsii.Number] = None,
        channel_layout: typing.Optional[typing.Sequence[builtins.str]] = None,
        codec: typing.Optional[builtins.str] = None,
        sample_rate_hertz: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: Audio bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#bitrate_bps GoogleTranscoderJobTemplate#bitrate_bps}
        :param channel_count: Number of audio channels. The default is '2'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#channel_count GoogleTranscoderJobTemplate#channel_count}
        :param channel_layout: A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#channel_layout GoogleTranscoderJobTemplate#channel_layout}
        :param codec: The codec for this audio stream. The default is 'aac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#codec GoogleTranscoderJobTemplate#codec}
        :param sample_rate_hertz: The audio sample rate in Hertz. The default is '48000'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#sample_rate_hertz GoogleTranscoderJobTemplate#sample_rate_hertz}
        '''
        value = GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream(
            bitrate_bps=bitrate_bps,
            channel_count=channel_count,
            channel_layout=channel_layout,
            codec=codec,
            sample_rate_hertz=sample_rate_hertz,
        )

        return typing.cast(None, jsii.invoke(self, "putAudioStream", [value]))

    @jsii.member(jsii_name="putVideoStream")
    def put_video_stream(
        self,
        *,
        h264: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param h264: h264 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#h264 GoogleTranscoderJobTemplate#h264}
        '''
        value = GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream(
            h264=h264
        )

        return typing.cast(None, jsii.invoke(self, "putVideoStream", [value]))

    @jsii.member(jsii_name="resetAudioStream")
    def reset_audio_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioStream", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetVideoStream")
    def reset_video_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVideoStream", []))

    @builtins.property
    @jsii.member(jsii_name="audioStream")
    def audio_stream(
        self,
    ) -> GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference, jsii.get(self, "audioStream"))

    @builtins.property
    @jsii.member(jsii_name="videoStream")
    def video_stream(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference", jsii.get(self, "videoStream"))

    @builtins.property
    @jsii.member(jsii_name="audioStreamInput")
    def audio_stream_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream], jsii.get(self, "audioStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="videoStreamInput")
    def video_stream_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream"], jsii.get(self, "videoStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab191b72235414332a43773fb2d6689b85cc164d8b3cac5f628daff97d573d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigElementaryStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigElementaryStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigElementaryStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88b74a25fd6e7fc0ea1cd17ac407f1add746c908b2f99b2cd6e38bc2df2719d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream",
    jsii_struct_bases=[],
    name_mapping={"h264": "h264"},
)
class GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream:
    def __init__(
        self,
        *,
        h264: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param h264: h264 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#h264 GoogleTranscoderJobTemplate#h264}
        '''
        if isinstance(h264, dict):
            h264 = GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264(**h264)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f458bb35fcf84bcbb6d3eef56d26dfaa33736b895d90ad8f99ee443d0467923e)
            check_type(argname="argument h264", value=h264, expected_type=type_hints["h264"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if h264 is not None:
            self._values["h264"] = h264

    @builtins.property
    def h264(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264"]:
        '''h264 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#h264 GoogleTranscoderJobTemplate#h264}
        '''
        result = self._values.get("h264")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264",
    jsii_struct_bases=[],
    name_mapping={
        "bitrate_bps": "bitrateBps",
        "frame_rate": "frameRate",
        "crf_level": "crfLevel",
        "entropy_coder": "entropyCoder",
        "gop_duration": "gopDuration",
        "height_pixels": "heightPixels",
        "hlg": "hlg",
        "pixel_format": "pixelFormat",
        "preset": "preset",
        "profile": "profile",
        "rate_control_mode": "rateControlMode",
        "sdr": "sdr",
        "vbv_fullness_bits": "vbvFullnessBits",
        "vbv_size_bits": "vbvSizeBits",
        "width_pixels": "widthPixels",
    },
)
class GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264:
    def __init__(
        self,
        *,
        bitrate_bps: jsii.Number,
        frame_rate: jsii.Number,
        crf_level: typing.Optional[jsii.Number] = None,
        entropy_coder: typing.Optional[builtins.str] = None,
        gop_duration: typing.Optional[builtins.str] = None,
        height_pixels: typing.Optional[jsii.Number] = None,
        hlg: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg", typing.Dict[builtins.str, typing.Any]]] = None,
        pixel_format: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        rate_control_mode: typing.Optional[builtins.str] = None,
        sdr: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr", typing.Dict[builtins.str, typing.Any]]] = None,
        vbv_fullness_bits: typing.Optional[jsii.Number] = None,
        vbv_size_bits: typing.Optional[jsii.Number] = None,
        width_pixels: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: The video bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#bitrate_bps GoogleTranscoderJobTemplate#bitrate_bps}
        :param frame_rate: The target video frame rate in frames per second (FPS). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#frame_rate GoogleTranscoderJobTemplate#frame_rate}
        :param crf_level: Target CRF level. The default is '21'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#crf_level GoogleTranscoderJobTemplate#crf_level}
        :param entropy_coder: The entropy coder to use. The default is 'cabac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#entropy_coder GoogleTranscoderJobTemplate#entropy_coder}
        :param gop_duration: Select the GOP size based on the specified duration. The default is '3s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#gop_duration GoogleTranscoderJobTemplate#gop_duration}
        :param height_pixels: The height of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#height_pixels GoogleTranscoderJobTemplate#height_pixels}
        :param hlg: hlg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#hlg GoogleTranscoderJobTemplate#hlg}
        :param pixel_format: Pixel format to use. The default is 'yuv420p'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#pixel_format GoogleTranscoderJobTemplate#pixel_format}
        :param preset: Enforces the specified codec preset. The default is 'veryfast'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#preset GoogleTranscoderJobTemplate#preset}
        :param profile: Enforces the specified codec profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#profile GoogleTranscoderJobTemplate#profile}
        :param rate_control_mode: Specify the mode. The default is 'vbr'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#rate_control_mode GoogleTranscoderJobTemplate#rate_control_mode}
        :param sdr: sdr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#sdr GoogleTranscoderJobTemplate#sdr}
        :param vbv_fullness_bits: Initial fullness of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#vbv_fullness_bits GoogleTranscoderJobTemplate#vbv_fullness_bits}
        :param vbv_size_bits: Size of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#vbv_size_bits GoogleTranscoderJobTemplate#vbv_size_bits}
        :param width_pixels: The width of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#width_pixels GoogleTranscoderJobTemplate#width_pixels}
        '''
        if isinstance(hlg, dict):
            hlg = GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg(**hlg)
        if isinstance(sdr, dict):
            sdr = GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr(**sdr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722749e293b435d48c477399b20610d2057d48f1cd3f9bae7ec09f2d444ff67c)
            check_type(argname="argument bitrate_bps", value=bitrate_bps, expected_type=type_hints["bitrate_bps"])
            check_type(argname="argument frame_rate", value=frame_rate, expected_type=type_hints["frame_rate"])
            check_type(argname="argument crf_level", value=crf_level, expected_type=type_hints["crf_level"])
            check_type(argname="argument entropy_coder", value=entropy_coder, expected_type=type_hints["entropy_coder"])
            check_type(argname="argument gop_duration", value=gop_duration, expected_type=type_hints["gop_duration"])
            check_type(argname="argument height_pixels", value=height_pixels, expected_type=type_hints["height_pixels"])
            check_type(argname="argument hlg", value=hlg, expected_type=type_hints["hlg"])
            check_type(argname="argument pixel_format", value=pixel_format, expected_type=type_hints["pixel_format"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument rate_control_mode", value=rate_control_mode, expected_type=type_hints["rate_control_mode"])
            check_type(argname="argument sdr", value=sdr, expected_type=type_hints["sdr"])
            check_type(argname="argument vbv_fullness_bits", value=vbv_fullness_bits, expected_type=type_hints["vbv_fullness_bits"])
            check_type(argname="argument vbv_size_bits", value=vbv_size_bits, expected_type=type_hints["vbv_size_bits"])
            check_type(argname="argument width_pixels", value=width_pixels, expected_type=type_hints["width_pixels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bitrate_bps": bitrate_bps,
            "frame_rate": frame_rate,
        }
        if crf_level is not None:
            self._values["crf_level"] = crf_level
        if entropy_coder is not None:
            self._values["entropy_coder"] = entropy_coder
        if gop_duration is not None:
            self._values["gop_duration"] = gop_duration
        if height_pixels is not None:
            self._values["height_pixels"] = height_pixels
        if hlg is not None:
            self._values["hlg"] = hlg
        if pixel_format is not None:
            self._values["pixel_format"] = pixel_format
        if preset is not None:
            self._values["preset"] = preset
        if profile is not None:
            self._values["profile"] = profile
        if rate_control_mode is not None:
            self._values["rate_control_mode"] = rate_control_mode
        if sdr is not None:
            self._values["sdr"] = sdr
        if vbv_fullness_bits is not None:
            self._values["vbv_fullness_bits"] = vbv_fullness_bits
        if vbv_size_bits is not None:
            self._values["vbv_size_bits"] = vbv_size_bits
        if width_pixels is not None:
            self._values["width_pixels"] = width_pixels

    @builtins.property
    def bitrate_bps(self) -> jsii.Number:
        '''The video bitrate in bits per second.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#bitrate_bps GoogleTranscoderJobTemplate#bitrate_bps}
        '''
        result = self._values.get("bitrate_bps")
        assert result is not None, "Required property 'bitrate_bps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frame_rate(self) -> jsii.Number:
        '''The target video frame rate in frames per second (FPS).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#frame_rate GoogleTranscoderJobTemplate#frame_rate}
        '''
        result = self._values.get("frame_rate")
        assert result is not None, "Required property 'frame_rate' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def crf_level(self) -> typing.Optional[jsii.Number]:
        '''Target CRF level. The default is '21'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#crf_level GoogleTranscoderJobTemplate#crf_level}
        '''
        result = self._values.get("crf_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def entropy_coder(self) -> typing.Optional[builtins.str]:
        '''The entropy coder to use. The default is 'cabac'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#entropy_coder GoogleTranscoderJobTemplate#entropy_coder}
        '''
        result = self._values.get("entropy_coder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gop_duration(self) -> typing.Optional[builtins.str]:
        '''Select the GOP size based on the specified duration. The default is '3s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#gop_duration GoogleTranscoderJobTemplate#gop_duration}
        '''
        result = self._values.get("gop_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def height_pixels(self) -> typing.Optional[jsii.Number]:
        '''The height of the video in pixels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#height_pixels GoogleTranscoderJobTemplate#height_pixels}
        '''
        result = self._values.get("height_pixels")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hlg(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg"]:
        '''hlg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#hlg GoogleTranscoderJobTemplate#hlg}
        '''
        result = self._values.get("hlg")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg"], result)

    @builtins.property
    def pixel_format(self) -> typing.Optional[builtins.str]:
        '''Pixel format to use. The default is 'yuv420p'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#pixel_format GoogleTranscoderJobTemplate#pixel_format}
        '''
        result = self._values.get("pixel_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preset(self) -> typing.Optional[builtins.str]:
        '''Enforces the specified codec preset. The default is 'veryfast'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#preset GoogleTranscoderJobTemplate#preset}
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Enforces the specified codec profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#profile GoogleTranscoderJobTemplate#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_control_mode(self) -> typing.Optional[builtins.str]:
        '''Specify the mode. The default is 'vbr'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#rate_control_mode GoogleTranscoderJobTemplate#rate_control_mode}
        '''
        result = self._values.get("rate_control_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sdr(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr"]:
        '''sdr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#sdr GoogleTranscoderJobTemplate#sdr}
        '''
        result = self._values.get("sdr")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr"], result)

    @builtins.property
    def vbv_fullness_bits(self) -> typing.Optional[jsii.Number]:
        '''Initial fullness of the Video Buffering Verifier (VBV) buffer in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#vbv_fullness_bits GoogleTranscoderJobTemplate#vbv_fullness_bits}
        '''
        result = self._values.get("vbv_fullness_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vbv_size_bits(self) -> typing.Optional[jsii.Number]:
        '''Size of the Video Buffering Verifier (VBV) buffer in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#vbv_size_bits GoogleTranscoderJobTemplate#vbv_size_bits}
        '''
        result = self._values.get("vbv_size_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def width_pixels(self) -> typing.Optional[jsii.Number]:
        '''The width of the video in pixels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#width_pixels GoogleTranscoderJobTemplate#width_pixels}
        '''
        result = self._values.get("width_pixels")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41c7c79c2d4e338d0734c562cae0762ae0445e86dd843f76eb70151c968c88f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250b4739b5ad8a4b5f04d20b0dc83d71c07875da3f024f2a0f27cee37de5dacc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d81faee6600a38a1548cdaefc7f7c0054bf4a60cfa695af28993e43b30df5c43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHlg")
    def put_hlg(self) -> None:
        value = GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg()

        return typing.cast(None, jsii.invoke(self, "putHlg", [value]))

    @jsii.member(jsii_name="putSdr")
    def put_sdr(self) -> None:
        value = GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr()

        return typing.cast(None, jsii.invoke(self, "putSdr", [value]))

    @jsii.member(jsii_name="resetCrfLevel")
    def reset_crf_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrfLevel", []))

    @jsii.member(jsii_name="resetEntropyCoder")
    def reset_entropy_coder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntropyCoder", []))

    @jsii.member(jsii_name="resetGopDuration")
    def reset_gop_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGopDuration", []))

    @jsii.member(jsii_name="resetHeightPixels")
    def reset_height_pixels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeightPixels", []))

    @jsii.member(jsii_name="resetHlg")
    def reset_hlg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHlg", []))

    @jsii.member(jsii_name="resetPixelFormat")
    def reset_pixel_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPixelFormat", []))

    @jsii.member(jsii_name="resetPreset")
    def reset_preset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreset", []))

    @jsii.member(jsii_name="resetProfile")
    def reset_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfile", []))

    @jsii.member(jsii_name="resetRateControlMode")
    def reset_rate_control_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateControlMode", []))

    @jsii.member(jsii_name="resetSdr")
    def reset_sdr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSdr", []))

    @jsii.member(jsii_name="resetVbvFullnessBits")
    def reset_vbv_fullness_bits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVbvFullnessBits", []))

    @jsii.member(jsii_name="resetVbvSizeBits")
    def reset_vbv_size_bits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVbvSizeBits", []))

    @jsii.member(jsii_name="resetWidthPixels")
    def reset_width_pixels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidthPixels", []))

    @builtins.property
    @jsii.member(jsii_name="hlg")
    def hlg(
        self,
    ) -> GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference, jsii.get(self, "hlg"))

    @builtins.property
    @jsii.member(jsii_name="sdr")
    def sdr(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference", jsii.get(self, "sdr"))

    @builtins.property
    @jsii.member(jsii_name="bitrateBpsInput")
    def bitrate_bps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bitrateBpsInput"))

    @builtins.property
    @jsii.member(jsii_name="crfLevelInput")
    def crf_level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "crfLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="entropyCoderInput")
    def entropy_coder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entropyCoderInput"))

    @builtins.property
    @jsii.member(jsii_name="frameRateInput")
    def frame_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frameRateInput"))

    @builtins.property
    @jsii.member(jsii_name="gopDurationInput")
    def gop_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gopDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="heightPixelsInput")
    def height_pixels_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightPixelsInput"))

    @builtins.property
    @jsii.member(jsii_name="hlgInput")
    def hlg_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg], jsii.get(self, "hlgInput"))

    @builtins.property
    @jsii.member(jsii_name="pixelFormatInput")
    def pixel_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pixelFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="presetInput")
    def preset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "presetInput"))

    @builtins.property
    @jsii.member(jsii_name="profileInput")
    def profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileInput"))

    @builtins.property
    @jsii.member(jsii_name="rateControlModeInput")
    def rate_control_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rateControlModeInput"))

    @builtins.property
    @jsii.member(jsii_name="sdrInput")
    def sdr_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr"], jsii.get(self, "sdrInput"))

    @builtins.property
    @jsii.member(jsii_name="vbvFullnessBitsInput")
    def vbv_fullness_bits_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vbvFullnessBitsInput"))

    @builtins.property
    @jsii.member(jsii_name="vbvSizeBitsInput")
    def vbv_size_bits_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vbvSizeBitsInput"))

    @builtins.property
    @jsii.member(jsii_name="widthPixelsInput")
    def width_pixels_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthPixelsInput"))

    @builtins.property
    @jsii.member(jsii_name="bitrateBps")
    def bitrate_bps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bitrateBps"))

    @bitrate_bps.setter
    def bitrate_bps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7540900af3764b20fda022d8ad6af5f1fb483bfe15b6a40f89469b6c904727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitrateBps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crfLevel")
    def crf_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "crfLevel"))

    @crf_level.setter
    def crf_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722be86802126a9536607a6ee3de9cc0644f9bf55ccc5461bb63c4b54811f02c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crfLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entropyCoder")
    def entropy_coder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entropyCoder"))

    @entropy_coder.setter
    def entropy_coder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88fc1a6f2b3178d270cd2b52efe4461ad558c33be7e04c2609fc126e04efab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entropyCoder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frameRate")
    def frame_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frameRate"))

    @frame_rate.setter
    def frame_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d492c21e32d33b827681393dd05b2eec36a81227478eceee152641c949fb3851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gopDuration")
    def gop_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gopDuration"))

    @gop_duration.setter
    def gop_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2e5a82284faa5f0d4ca9d7e1c9016a952c0cbc03945e736043e981ded73898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gopDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="heightPixels")
    def height_pixels(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "heightPixels"))

    @height_pixels.setter
    def height_pixels(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9096a1b8d05fc63f4d7bc56a78f3f86b0d0179f2ab08369e79123355cd55495b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "heightPixels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pixelFormat")
    def pixel_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pixelFormat"))

    @pixel_format.setter
    def pixel_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b256989c23e133cb14dbb28b80f9297eb10ebbca934de718672af2e53daebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pixelFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preset")
    def preset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preset"))

    @preset.setter
    def preset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0913d012c277198825ea71ff06f7895ffd47734e431e1fd110f81aaaec0c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea0266db84d47a949974cac569bf3e3c54baeda440881428d4b4caeeb2df9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rateControlMode")
    def rate_control_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rateControlMode"))

    @rate_control_mode.setter
    def rate_control_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1f873fbb8e28f5ab40457088e8a8afd845c4a87a45d19bc0024df6b8cea9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateControlMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vbvFullnessBits")
    def vbv_fullness_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vbvFullnessBits"))

    @vbv_fullness_bits.setter
    def vbv_fullness_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c54428fa89b8efb928ce29b87fbac52c16d01c4d0f0cb75a1f3a01999d91b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vbvFullnessBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vbvSizeBits")
    def vbv_size_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vbvSizeBits"))

    @vbv_size_bits.setter
    def vbv_size_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5334ac196c46faf9cf11eb7e3f5dfca069082e33534e3a37c89b87814ecd512c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vbvSizeBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="widthPixels")
    def width_pixels(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "widthPixels"))

    @width_pixels.setter
    def width_pixels(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c14bc9557b1f8c336b02599f822a485c86001b9889dceb14024f44770197c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "widthPixels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c986507fe697b5e803eb3ab715bebeacaa564c45b95e6c6e64452631a2a83f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__224ff07087ba509664881972ab0f355faa8b97a37295d9b0c88b2dfe9e42bf70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d485c324067a2ae8c201e55dc28c167f1247e5a685419ddabcd64045296d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52cfa51833dd6b60549141331fbe2487563c17f7846a04457bc945cf38f4e64e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putH264")
    def put_h264(
        self,
        *,
        bitrate_bps: jsii.Number,
        frame_rate: jsii.Number,
        crf_level: typing.Optional[jsii.Number] = None,
        entropy_coder: typing.Optional[builtins.str] = None,
        gop_duration: typing.Optional[builtins.str] = None,
        height_pixels: typing.Optional[jsii.Number] = None,
        hlg: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg, typing.Dict[builtins.str, typing.Any]]] = None,
        pixel_format: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        rate_control_mode: typing.Optional[builtins.str] = None,
        sdr: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr, typing.Dict[builtins.str, typing.Any]]] = None,
        vbv_fullness_bits: typing.Optional[jsii.Number] = None,
        vbv_size_bits: typing.Optional[jsii.Number] = None,
        width_pixels: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: The video bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#bitrate_bps GoogleTranscoderJobTemplate#bitrate_bps}
        :param frame_rate: The target video frame rate in frames per second (FPS). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#frame_rate GoogleTranscoderJobTemplate#frame_rate}
        :param crf_level: Target CRF level. The default is '21'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#crf_level GoogleTranscoderJobTemplate#crf_level}
        :param entropy_coder: The entropy coder to use. The default is 'cabac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#entropy_coder GoogleTranscoderJobTemplate#entropy_coder}
        :param gop_duration: Select the GOP size based on the specified duration. The default is '3s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#gop_duration GoogleTranscoderJobTemplate#gop_duration}
        :param height_pixels: The height of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#height_pixels GoogleTranscoderJobTemplate#height_pixels}
        :param hlg: hlg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#hlg GoogleTranscoderJobTemplate#hlg}
        :param pixel_format: Pixel format to use. The default is 'yuv420p'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#pixel_format GoogleTranscoderJobTemplate#pixel_format}
        :param preset: Enforces the specified codec preset. The default is 'veryfast'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#preset GoogleTranscoderJobTemplate#preset}
        :param profile: Enforces the specified codec profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#profile GoogleTranscoderJobTemplate#profile}
        :param rate_control_mode: Specify the mode. The default is 'vbr'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#rate_control_mode GoogleTranscoderJobTemplate#rate_control_mode}
        :param sdr: sdr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#sdr GoogleTranscoderJobTemplate#sdr}
        :param vbv_fullness_bits: Initial fullness of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#vbv_fullness_bits GoogleTranscoderJobTemplate#vbv_fullness_bits}
        :param vbv_size_bits: Size of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#vbv_size_bits GoogleTranscoderJobTemplate#vbv_size_bits}
        :param width_pixels: The width of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#width_pixels GoogleTranscoderJobTemplate#width_pixels}
        '''
        value = GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264(
            bitrate_bps=bitrate_bps,
            frame_rate=frame_rate,
            crf_level=crf_level,
            entropy_coder=entropy_coder,
            gop_duration=gop_duration,
            height_pixels=height_pixels,
            hlg=hlg,
            pixel_format=pixel_format,
            preset=preset,
            profile=profile,
            rate_control_mode=rate_control_mode,
            sdr=sdr,
            vbv_fullness_bits=vbv_fullness_bits,
            vbv_size_bits=vbv_size_bits,
            width_pixels=width_pixels,
        )

        return typing.cast(None, jsii.invoke(self, "putH264", [value]))

    @jsii.member(jsii_name="resetH264")
    def reset_h264(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetH264", []))

    @builtins.property
    @jsii.member(jsii_name="h264")
    def h264(
        self,
    ) -> GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference, jsii.get(self, "h264"))

    @builtins.property
    @jsii.member(jsii_name="h264Input")
    def h264_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264], jsii.get(self, "h264Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe1dede1bd281ffb643ad70fd3c554f53fe827afce432e8052477418dcbadde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptions",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "aes128": "aes128",
        "drm_systems": "drmSystems",
        "mpeg_cenc": "mpegCenc",
        "sample_aes": "sampleAes",
        "secret_manager_key_source": "secretManagerKeySource",
    },
)
class GoogleTranscoderJobTemplateConfigEncryptions:
    def __init__(
        self,
        *,
        id: builtins.str,
        aes128: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsAes128", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_systems: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems", typing.Dict[builtins.str, typing.Any]]] = None,
        mpeg_cenc: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc", typing.Dict[builtins.str, typing.Any]]] = None,
        sample_aes: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsSampleAes", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_manager_key_source: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Identifier for this set of encryption options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#id GoogleTranscoderJobTemplate#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param aes128: aes128 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#aes128 GoogleTranscoderJobTemplate#aes128}
        :param drm_systems: drm_systems block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#drm_systems GoogleTranscoderJobTemplate#drm_systems}
        :param mpeg_cenc: mpeg_cenc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#mpeg_cenc GoogleTranscoderJobTemplate#mpeg_cenc}
        :param sample_aes: sample_aes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#sample_aes GoogleTranscoderJobTemplate#sample_aes}
        :param secret_manager_key_source: secret_manager_key_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#secret_manager_key_source GoogleTranscoderJobTemplate#secret_manager_key_source}
        '''
        if isinstance(aes128, dict):
            aes128 = GoogleTranscoderJobTemplateConfigEncryptionsAes128(**aes128)
        if isinstance(drm_systems, dict):
            drm_systems = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems(**drm_systems)
        if isinstance(mpeg_cenc, dict):
            mpeg_cenc = GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc(**mpeg_cenc)
        if isinstance(sample_aes, dict):
            sample_aes = GoogleTranscoderJobTemplateConfigEncryptionsSampleAes(**sample_aes)
        if isinstance(secret_manager_key_source, dict):
            secret_manager_key_source = GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource(**secret_manager_key_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830a422d027cd6f3ede301748de99284117b07d82d6d37ff5e10fdfb0c03ead8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument aes128", value=aes128, expected_type=type_hints["aes128"])
            check_type(argname="argument drm_systems", value=drm_systems, expected_type=type_hints["drm_systems"])
            check_type(argname="argument mpeg_cenc", value=mpeg_cenc, expected_type=type_hints["mpeg_cenc"])
            check_type(argname="argument sample_aes", value=sample_aes, expected_type=type_hints["sample_aes"])
            check_type(argname="argument secret_manager_key_source", value=secret_manager_key_source, expected_type=type_hints["secret_manager_key_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if aes128 is not None:
            self._values["aes128"] = aes128
        if drm_systems is not None:
            self._values["drm_systems"] = drm_systems
        if mpeg_cenc is not None:
            self._values["mpeg_cenc"] = mpeg_cenc
        if sample_aes is not None:
            self._values["sample_aes"] = sample_aes
        if secret_manager_key_source is not None:
            self._values["secret_manager_key_source"] = secret_manager_key_source

    @builtins.property
    def id(self) -> builtins.str:
        '''Identifier for this set of encryption options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#id GoogleTranscoderJobTemplate#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aes128(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsAes128"]:
        '''aes128 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#aes128 GoogleTranscoderJobTemplate#aes128}
        '''
        result = self._values.get("aes128")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsAes128"], result)

    @builtins.property
    def drm_systems(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems"]:
        '''drm_systems block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#drm_systems GoogleTranscoderJobTemplate#drm_systems}
        '''
        result = self._values.get("drm_systems")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems"], result)

    @builtins.property
    def mpeg_cenc(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc"]:
        '''mpeg_cenc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#mpeg_cenc GoogleTranscoderJobTemplate#mpeg_cenc}
        '''
        result = self._values.get("mpeg_cenc")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc"], result)

    @builtins.property
    def sample_aes(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsSampleAes"]:
        '''sample_aes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#sample_aes GoogleTranscoderJobTemplate#sample_aes}
        '''
        result = self._values.get("sample_aes")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsSampleAes"], result)

    @builtins.property
    def secret_manager_key_source(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource"]:
        '''secret_manager_key_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#secret_manager_key_source GoogleTranscoderJobTemplate#secret_manager_key_source}
        '''
        result = self._values.get("secret_manager_key_source")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsAes128",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobTemplateConfigEncryptionsAes128:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsAes128(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEncryptionsAes128OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsAes128OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aac406a877a8690483e1c85fac2811b4bdc2f343ea1f9e7cd83eb807622baad7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsAes128]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsAes128], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsAes128],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d2a5e2377b8aa896067dff0ebfe993e5fdf41a6e4a3598d49367472518dcbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems",
    jsii_struct_bases=[],
    name_mapping={
        "clearkey": "clearkey",
        "fairplay": "fairplay",
        "playready": "playready",
        "widevine": "widevine",
    },
)
class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems:
    def __init__(
        self,
        *,
        clearkey: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey", typing.Dict[builtins.str, typing.Any]]] = None,
        fairplay: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay", typing.Dict[builtins.str, typing.Any]]] = None,
        playready: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready", typing.Dict[builtins.str, typing.Any]]] = None,
        widevine: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clearkey: clearkey block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#clearkey GoogleTranscoderJobTemplate#clearkey}
        :param fairplay: fairplay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#fairplay GoogleTranscoderJobTemplate#fairplay}
        :param playready: playready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#playready GoogleTranscoderJobTemplate#playready}
        :param widevine: widevine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#widevine GoogleTranscoderJobTemplate#widevine}
        '''
        if isinstance(clearkey, dict):
            clearkey = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey(**clearkey)
        if isinstance(fairplay, dict):
            fairplay = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay(**fairplay)
        if isinstance(playready, dict):
            playready = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready(**playready)
        if isinstance(widevine, dict):
            widevine = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine(**widevine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53aed28f6fadcae703e52eec98cb99cc627d10c4528fd205305759ec832ffcf)
            check_type(argname="argument clearkey", value=clearkey, expected_type=type_hints["clearkey"])
            check_type(argname="argument fairplay", value=fairplay, expected_type=type_hints["fairplay"])
            check_type(argname="argument playready", value=playready, expected_type=type_hints["playready"])
            check_type(argname="argument widevine", value=widevine, expected_type=type_hints["widevine"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if clearkey is not None:
            self._values["clearkey"] = clearkey
        if fairplay is not None:
            self._values["fairplay"] = fairplay
        if playready is not None:
            self._values["playready"] = playready
        if widevine is not None:
            self._values["widevine"] = widevine

    @builtins.property
    def clearkey(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey"]:
        '''clearkey block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#clearkey GoogleTranscoderJobTemplate#clearkey}
        '''
        result = self._values.get("clearkey")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey"], result)

    @builtins.property
    def fairplay(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay"]:
        '''fairplay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#fairplay GoogleTranscoderJobTemplate#fairplay}
        '''
        result = self._values.get("fairplay")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay"], result)

    @builtins.property
    def playready(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready"]:
        '''playready block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#playready GoogleTranscoderJobTemplate#playready}
        '''
        result = self._values.get("playready")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready"], result)

    @builtins.property
    def widevine(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine"]:
        '''widevine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#widevine GoogleTranscoderJobTemplate#widevine}
        '''
        result = self._values.get("widevine")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb83e8404cc7ab244928083792bbe0fe72569966f8bd6310e5fa8fea8808afac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f934fc8cf958815fcf88698d9fb12925fc64e4c8f06c30406be2e6badc98fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0bc1eb55997f61122ebd830b56353b7ed4cd3f4bc9ac69b32541770b1a01ae8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082ff3a15b8754775f5be80b2d29c19e02f5d8cdf2ccff97812e7846af70699f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__169817df69ea7f08fb4f19ff178acc037d5fbbfb182d4a20feb00017e876967e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClearkey")
    def put_clearkey(self) -> None:
        value = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey()

        return typing.cast(None, jsii.invoke(self, "putClearkey", [value]))

    @jsii.member(jsii_name="putFairplay")
    def put_fairplay(self) -> None:
        value = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay()

        return typing.cast(None, jsii.invoke(self, "putFairplay", [value]))

    @jsii.member(jsii_name="putPlayready")
    def put_playready(self) -> None:
        value = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready()

        return typing.cast(None, jsii.invoke(self, "putPlayready", [value]))

    @jsii.member(jsii_name="putWidevine")
    def put_widevine(self) -> None:
        value = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine()

        return typing.cast(None, jsii.invoke(self, "putWidevine", [value]))

    @jsii.member(jsii_name="resetClearkey")
    def reset_clearkey(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClearkey", []))

    @jsii.member(jsii_name="resetFairplay")
    def reset_fairplay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFairplay", []))

    @jsii.member(jsii_name="resetPlayready")
    def reset_playready(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlayready", []))

    @jsii.member(jsii_name="resetWidevine")
    def reset_widevine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidevine", []))

    @builtins.property
    @jsii.member(jsii_name="clearkey")
    def clearkey(
        self,
    ) -> GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference, jsii.get(self, "clearkey"))

    @builtins.property
    @jsii.member(jsii_name="fairplay")
    def fairplay(
        self,
    ) -> GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference, jsii.get(self, "fairplay"))

    @builtins.property
    @jsii.member(jsii_name="playready")
    def playready(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference", jsii.get(self, "playready"))

    @builtins.property
    @jsii.member(jsii_name="widevine")
    def widevine(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference", jsii.get(self, "widevine"))

    @builtins.property
    @jsii.member(jsii_name="clearkeyInput")
    def clearkey_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey], jsii.get(self, "clearkeyInput"))

    @builtins.property
    @jsii.member(jsii_name="fairplayInput")
    def fairplay_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay], jsii.get(self, "fairplayInput"))

    @builtins.property
    @jsii.member(jsii_name="playreadyInput")
    def playready_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready"], jsii.get(self, "playreadyInput"))

    @builtins.property
    @jsii.member(jsii_name="widevineInput")
    def widevine_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine"], jsii.get(self, "widevineInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22c56d62f139e3399b3c5406c97c9ea2f79b076f3bb1b41ff02ebe801ac725a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1895089f8206ef1a98e3cb51ae863ea3484e6c7488898db1bc7ef8579df1bb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b7b1f7b39aa2d6242c6027f304f6bdbfa3013893f53b2f34729abcd1a3d0da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b7ef10c079b877389872d1bd6e9705085ef3a0f898a65d41c17d10593a400ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a623f7da3e714bb4b5d212dcb4bbceef8732a7e24ef588c0abd29efaf1357db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigEncryptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ce95cef57cf7d7181161cd7c950e9fab9f8663fd454716aa77ae809dd687c2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigEncryptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b6f8fcb986fec21fa2950db876ec1fd390ec04d77196b8e421be9da8464ffc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigEncryptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d90407fd65d433f77e301825a8ea516a828e2d4f96d701420dc8f21945db23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17835a56a9a8751e0fe801878bbba0e7aed4c552819f10c1c3b35ea9d0e0f357)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d097dd2d9f9dd5755c99ecbc311a6c6c7d2222ae723fccc906faff1517595a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigEncryptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigEncryptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigEncryptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d76266c374212ff577d17af4fc9ed65f01d3e3c1024d28df037065569d0d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc",
    jsii_struct_bases=[],
    name_mapping={"scheme": "scheme"},
)
class GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc:
    def __init__(self, *, scheme: builtins.str) -> None:
        '''
        :param scheme: Specify the encryption scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#scheme GoogleTranscoderJobTemplate#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90c88f66339ec6fb23b98dd9fcaa1d2f74c960a950f56b4d0d644f4b47be37f)
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scheme": scheme,
        }

    @builtins.property
    def scheme(self) -> builtins.str:
        '''Specify the encryption scheme.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#scheme GoogleTranscoderJobTemplate#scheme}
        '''
        result = self._values.get("scheme")
        assert result is not None, "Required property 'scheme' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEncryptionsMpegCencOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsMpegCencOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4318f0ec17aa3117703bffb6dd673337f3e5cb5f2e0504c204ee4ef7f1025f61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be48df5dab479a7be82d909b36232347600264b7a2810a74e3a59e4108a90ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db1d6183ce5faafebd004c5b1ca54ac616ae5d510dd6b23aff094568f806747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigEncryptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5b7a007532f798f095cb5d5d609b85f2a38be7b909f35a095691164667ad80f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAes128")
    def put_aes128(self) -> None:
        value = GoogleTranscoderJobTemplateConfigEncryptionsAes128()

        return typing.cast(None, jsii.invoke(self, "putAes128", [value]))

    @jsii.member(jsii_name="putDrmSystems")
    def put_drm_systems(
        self,
        *,
        clearkey: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey, typing.Dict[builtins.str, typing.Any]]] = None,
        fairplay: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
        playready: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
        widevine: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clearkey: clearkey block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#clearkey GoogleTranscoderJobTemplate#clearkey}
        :param fairplay: fairplay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#fairplay GoogleTranscoderJobTemplate#fairplay}
        :param playready: playready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#playready GoogleTranscoderJobTemplate#playready}
        :param widevine: widevine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#widevine GoogleTranscoderJobTemplate#widevine}
        '''
        value = GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems(
            clearkey=clearkey,
            fairplay=fairplay,
            playready=playready,
            widevine=widevine,
        )

        return typing.cast(None, jsii.invoke(self, "putDrmSystems", [value]))

    @jsii.member(jsii_name="putMpegCenc")
    def put_mpeg_cenc(self, *, scheme: builtins.str) -> None:
        '''
        :param scheme: Specify the encryption scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#scheme GoogleTranscoderJobTemplate#scheme}
        '''
        value = GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc(scheme=scheme)

        return typing.cast(None, jsii.invoke(self, "putMpegCenc", [value]))

    @jsii.member(jsii_name="putSampleAes")
    def put_sample_aes(self) -> None:
        value = GoogleTranscoderJobTemplateConfigEncryptionsSampleAes()

        return typing.cast(None, jsii.invoke(self, "putSampleAes", [value]))

    @jsii.member(jsii_name="putSecretManagerKeySource")
    def put_secret_manager_key_source(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#secret_version GoogleTranscoderJobTemplate#secret_version}
        '''
        value = GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSecretManagerKeySource", [value]))

    @jsii.member(jsii_name="resetAes128")
    def reset_aes128(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAes128", []))

    @jsii.member(jsii_name="resetDrmSystems")
    def reset_drm_systems(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrmSystems", []))

    @jsii.member(jsii_name="resetMpegCenc")
    def reset_mpeg_cenc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMpegCenc", []))

    @jsii.member(jsii_name="resetSampleAes")
    def reset_sample_aes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleAes", []))

    @jsii.member(jsii_name="resetSecretManagerKeySource")
    def reset_secret_manager_key_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretManagerKeySource", []))

    @builtins.property
    @jsii.member(jsii_name="aes128")
    def aes128(
        self,
    ) -> GoogleTranscoderJobTemplateConfigEncryptionsAes128OutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigEncryptionsAes128OutputReference, jsii.get(self, "aes128"))

    @builtins.property
    @jsii.member(jsii_name="drmSystems")
    def drm_systems(
        self,
    ) -> GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference, jsii.get(self, "drmSystems"))

    @builtins.property
    @jsii.member(jsii_name="mpegCenc")
    def mpeg_cenc(
        self,
    ) -> GoogleTranscoderJobTemplateConfigEncryptionsMpegCencOutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigEncryptionsMpegCencOutputReference, jsii.get(self, "mpegCenc"))

    @builtins.property
    @jsii.member(jsii_name="sampleAes")
    def sample_aes(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigEncryptionsSampleAesOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigEncryptionsSampleAesOutputReference", jsii.get(self, "sampleAes"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerKeySource")
    def secret_manager_key_source(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference", jsii.get(self, "secretManagerKeySource"))

    @builtins.property
    @jsii.member(jsii_name="aes128Input")
    def aes128_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsAes128]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsAes128], jsii.get(self, "aes128Input"))

    @builtins.property
    @jsii.member(jsii_name="drmSystemsInput")
    def drm_systems_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems], jsii.get(self, "drmSystemsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mpegCencInput")
    def mpeg_cenc_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc], jsii.get(self, "mpegCencInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleAesInput")
    def sample_aes_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsSampleAes"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsSampleAes"], jsii.get(self, "sampleAesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerKeySourceInput")
    def secret_manager_key_source_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource"], jsii.get(self, "secretManagerKeySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1171ca056dfc1dec94fd642d7362f20165ffda099db389cf722154853430548e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigEncryptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigEncryptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigEncryptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5737cf9e4ddbd154b2f6d6deb1c60bc8b837f0e7f65e0c2760db32ca084eb59a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsSampleAes",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobTemplateConfigEncryptionsSampleAes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsSampleAes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEncryptionsSampleAesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsSampleAesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bc04953bf10a2dfe525feb994d145b93a28cc831bdb5a8aeb103ccabe3562e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsSampleAes]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsSampleAes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsSampleAes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d71c3f5587444b4025ecfc11cded2bf94e5aac358152d589c9ee4c455a5945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#secret_version GoogleTranscoderJobTemplate#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d95ee8c3b2ff03f7aa113b5d8301f35d73aefcf05d2abbc40e90c7b4366c27b)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#secret_version GoogleTranscoderJobTemplate#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32a866c51a88286dfd748fbe0aea756b29c5783dd472a9c328b1a7b2739aca64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbaff92cb448063fecc67b3628665d83ffb5b050ac4963b1c0c9fb2020337ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef26f425ebbf1209b122ccbca345f2f54b01bdb16d514364eebf1e5ac4c6592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigInputs",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "uri": "uri"},
)
class GoogleTranscoderJobTemplateConfigInputs:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: A unique key for this input. Must be specified when using advanced mapping and edit lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#key GoogleTranscoderJobTemplate#key}
        :param uri: URI of the media. Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, gs://bucket/inputs/file.mp4). If empty, the value is populated from Job.input_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#uri GoogleTranscoderJobTemplate#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4fcaf97a56b47d76f05551e80b89a38c4d955a203af8e10c1081e51461d1fbd)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this input. Must be specified when using advanced mapping and edit lists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#key GoogleTranscoderJobTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI of the media.

        Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, gs://bucket/inputs/file.mp4).
        If empty, the value is populated from Job.input_uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#uri GoogleTranscoderJobTemplate#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigInputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigInputsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigInputsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3015f35d94e60c158dbad08d84c253a1d6df9896d4a0351a78e343f5e2044a64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigInputsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556d04e93ba8c64df43dde974742361ba1b66bb74afce777c53d4eb0fb2ef706)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigInputsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c936a4b382cddd3f35c34c06554cd74d48975d026026865a43859b74e1c0d6b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97709a2733e8e94cee0587d08adf2a561c74d32ddb44dd31816d9436a13b8fdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e60d600e60623853c6e35808f8b19b320de41e949a44eb0c2063c05b875e025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigInputs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigInputs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigInputs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5576842863641d833f5547f1edde0a018bae9709afc87cd675e78fc315395909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigInputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigInputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e4570869b82339572d3436b8da90fc027edbb4a33c6bacca53fbfabc3500431)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a707aa2d6076dfb45cf31de5f9732751a9bd452fd168e7c0355c638ae07bf264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab41ec202afab31c7c9632f14a6e0e2764ab9b1f1b82bbaa5ee4575f2eb8d014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigInputs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigInputs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigInputs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e992b2dd5bf2c1f86e4596616d670dbb917a31527649e22153c62d0c6087fd63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigManifests",
    jsii_struct_bases=[],
    name_mapping={
        "file_name": "fileName",
        "mux_streams": "muxStreams",
        "type": "type",
    },
)
class GoogleTranscoderJobTemplateConfigManifests:
    def __init__(
        self,
        *,
        file_name: typing.Optional[builtins.str] = None,
        mux_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_name: The name of the generated file. The default is 'manifest'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#file_name GoogleTranscoderJobTemplate#file_name}
        :param mux_streams: List of user supplied MuxStream.key values that should appear in this manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#mux_streams GoogleTranscoderJobTemplate#mux_streams}
        :param type: Type of the manifest. Possible values: ["MANIFEST_TYPE_UNSPECIFIED", "HLS", "DASH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#type GoogleTranscoderJobTemplate#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ee6b8a007520df1d0d98f58682e3a4106360f31ca310c68183adca5e869e7c)
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument mux_streams", value=mux_streams, expected_type=type_hints["mux_streams"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_name is not None:
            self._values["file_name"] = file_name
        if mux_streams is not None:
            self._values["mux_streams"] = mux_streams
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def file_name(self) -> typing.Optional[builtins.str]:
        '''The name of the generated file. The default is 'manifest'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#file_name GoogleTranscoderJobTemplate#file_name}
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mux_streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user supplied MuxStream.key values that should appear in this manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#mux_streams GoogleTranscoderJobTemplate#mux_streams}
        '''
        result = self._values.get("mux_streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of the manifest. Possible values: ["MANIFEST_TYPE_UNSPECIFIED", "HLS", "DASH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#type GoogleTranscoderJobTemplate#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigManifests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigManifestsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigManifestsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d96aa2d46daaef4c748aa969306255624fb4cf4ad43fbb25743fa7909a2b85f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigManifestsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a755739e25d0eb2d8f33ca39e6cfa98be8f84c0f7b1835353336197d834630)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigManifestsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef47d722332136fd465ecedb4b8d35e816a1c6ffa9c6a6abf96db1a063a1da90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d146374a58053d65d57879430a5a744adf4fb539e1443318a69496e4ca7885eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d807696f270a556761d396295a8aff85cfa653a30ded9cb14cff145cd88d986c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigManifests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigManifests]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigManifests]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783e40b9e4096f73fc90d68b37fc80b6f11967e3c358f3f96468a373c02439b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigManifestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigManifestsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d51ff8adaf375d1871659aab3fad94bd12dcabf183cee1aeb5cf06616e0c79ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFileName")
    def reset_file_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileName", []))

    @jsii.member(jsii_name="resetMuxStreams")
    def reset_mux_streams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMuxStreams", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="fileNameInput")
    def file_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="muxStreamsInput")
    def mux_streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "muxStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e816828fbf48c88138c206590fcfad9c4997e968ca931da636051e014ef0503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="muxStreams")
    def mux_streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "muxStreams"))

    @mux_streams.setter
    def mux_streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6e8f060d99cbc3a7cc4b27ffd6f6be4bccc70d28d027720e69e14465338dcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "muxStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262ab5ccc88910a3683f2949fbf9ed77c88207ba4e46b152a0c0d3393d743030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigManifests]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigManifests]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigManifests]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05ca866b6d90382390b86b6542ba6b7504ea7d0265ebbf7a86c9a414b6b40cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigMuxStreams",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "elementary_streams": "elementaryStreams",
        "encryption_id": "encryptionId",
        "file_name": "fileName",
        "key": "key",
        "segment_settings": "segmentSettings",
    },
)
class GoogleTranscoderJobTemplateConfigMuxStreams:
    def __init__(
        self,
        *,
        container: typing.Optional[builtins.str] = None,
        elementary_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
        encryption_id: typing.Optional[builtins.str] = None,
        file_name: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        segment_settings: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: The container format. The default is 'mp4'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#container GoogleTranscoderJobTemplate#container}
        :param elementary_streams: List of ElementaryStream.key values multiplexed in this stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#elementary_streams GoogleTranscoderJobTemplate#elementary_streams}
        :param encryption_id: Identifier of the encryption configuration to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#encryption_id GoogleTranscoderJobTemplate#encryption_id}
        :param file_name: The name of the generated file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#file_name GoogleTranscoderJobTemplate#file_name}
        :param key: A unique key for this multiplexed stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#key GoogleTranscoderJobTemplate#key}
        :param segment_settings: segment_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#segment_settings GoogleTranscoderJobTemplate#segment_settings}
        '''
        if isinstance(segment_settings, dict):
            segment_settings = GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings(**segment_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f87daacee7cd781a487d9af20d439ba42d7cfc6373146f972e101129459830a)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument elementary_streams", value=elementary_streams, expected_type=type_hints["elementary_streams"])
            check_type(argname="argument encryption_id", value=encryption_id, expected_type=type_hints["encryption_id"])
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument segment_settings", value=segment_settings, expected_type=type_hints["segment_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container is not None:
            self._values["container"] = container
        if elementary_streams is not None:
            self._values["elementary_streams"] = elementary_streams
        if encryption_id is not None:
            self._values["encryption_id"] = encryption_id
        if file_name is not None:
            self._values["file_name"] = file_name
        if key is not None:
            self._values["key"] = key
        if segment_settings is not None:
            self._values["segment_settings"] = segment_settings

    @builtins.property
    def container(self) -> typing.Optional[builtins.str]:
        '''The container format. The default is 'mp4'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#container GoogleTranscoderJobTemplate#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elementary_streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of ElementaryStream.key values multiplexed in this stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#elementary_streams GoogleTranscoderJobTemplate#elementary_streams}
        '''
        result = self._values.get("elementary_streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def encryption_id(self) -> typing.Optional[builtins.str]:
        '''Identifier of the encryption configuration to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#encryption_id GoogleTranscoderJobTemplate#encryption_id}
        '''
        result = self._values.get("encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_name(self) -> typing.Optional[builtins.str]:
        '''The name of the generated file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#file_name GoogleTranscoderJobTemplate#file_name}
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this multiplexed stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#key GoogleTranscoderJobTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_settings(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings"]:
        '''segment_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#segment_settings GoogleTranscoderJobTemplate#segment_settings}
        '''
        result = self._values.get("segment_settings")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigMuxStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigMuxStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigMuxStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0878cf1ae5363f7cc7005dd2d8ccebcce15ca31af2430aa0c152a463dcd05939)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigMuxStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7da193a76cdd014c715c70c91269d478c6f9ba8c590307359c29e4615c808d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigMuxStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e90e719ed4046f1786445792a1672352abc00bc227fa1d2e2fc4423a93f1e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f38783cc0e05d96ccff3f496624cf0fb21d6171bd03ee957aa83c44d28435351)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9c2a2bbe75e00f9e027b1d28122d7bdd5e41d73388cd4352b630f9def7267ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigMuxStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigMuxStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigMuxStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71657caf5a4bc945c6188d47461de021854069a9f680aeb4eb529496334f5d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigMuxStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigMuxStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__774815268f53c86ddc56806cdf60a9b2ff1b35ac3f2659f7a6343ea53f5e4c59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSegmentSettings")
    def put_segment_settings(
        self,
        *,
        segment_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param segment_duration: Duration of the segments in seconds. The default is '6.0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#segment_duration GoogleTranscoderJobTemplate#segment_duration}
        '''
        value = GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings(
            segment_duration=segment_duration
        )

        return typing.cast(None, jsii.invoke(self, "putSegmentSettings", [value]))

    @jsii.member(jsii_name="resetContainer")
    def reset_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainer", []))

    @jsii.member(jsii_name="resetElementaryStreams")
    def reset_elementary_streams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElementaryStreams", []))

    @jsii.member(jsii_name="resetEncryptionId")
    def reset_encryption_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionId", []))

    @jsii.member(jsii_name="resetFileName")
    def reset_file_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileName", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetSegmentSettings")
    def reset_segment_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegmentSettings", []))

    @builtins.property
    @jsii.member(jsii_name="segmentSettings")
    def segment_settings(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference", jsii.get(self, "segmentSettings"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreamsInput")
    def elementary_streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "elementaryStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionIdInput")
    def encryption_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="fileNameInput")
    def file_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentSettingsInput")
    def segment_settings_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings"], jsii.get(self, "segmentSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3dda482ad0e4c560a1db2a88c77628e66f035f0af3037735a7b170fbf3f0fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elementaryStreams")
    def elementary_streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "elementaryStreams"))

    @elementary_streams.setter
    def elementary_streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf407a8671b9d0484046b4308808dc82233c55ab6262c34eddac450e425f698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elementaryStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionId")
    def encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionId"))

    @encryption_id.setter
    def encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aae8e2e7a184335585fa165d46c4292799ef1d3b189dd7497108c809edbf469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c573afcbccc8c764cc2b3d6cbe080352b2b889b0c5b37b5e86a4a59b74303a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9edf01af9f5c32f0be733bd69a2e131ab2129004c13a52bbaaff7c465b51342b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigMuxStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigMuxStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigMuxStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9ec2979ce67c1a3263825b67f726d683219ef76543dba41aed6a05590d9417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings",
    jsii_struct_bases=[],
    name_mapping={"segment_duration": "segmentDuration"},
)
class GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings:
    def __init__(
        self,
        *,
        segment_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param segment_duration: Duration of the segments in seconds. The default is '6.0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#segment_duration GoogleTranscoderJobTemplate#segment_duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775b229cd77969c0e3a4523dcc3e97c0235eeee4546ce1cc0f985346c9fe90e2)
            check_type(argname="argument segment_duration", value=segment_duration, expected_type=type_hints["segment_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if segment_duration is not None:
            self._values["segment_duration"] = segment_duration

    @builtins.property
    def segment_duration(self) -> typing.Optional[builtins.str]:
        '''Duration of the segments in seconds. The default is '6.0s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#segment_duration GoogleTranscoderJobTemplate#segment_duration}
        '''
        result = self._values.get("segment_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__409c9d8662795ac84e01ad323f4c6482ec4e857a5d3cfff756d1a38a358ae553)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSegmentDuration")
    def reset_segment_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegmentDuration", []))

    @builtins.property
    @jsii.member(jsii_name="segmentDurationInput")
    def segment_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "segmentDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentDuration")
    def segment_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segmentDuration"))

    @segment_duration.setter
    def segment_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ede5feac21dfbbede352c4b069aac3f9930b4167c17d9a071599b6afd0d793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a4748b3c12b8b872bea82f202f513cf0800da607d7bb8adba61d1f1d5c61b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOutput",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleTranscoderJobTemplateConfigOutput:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: URI for the output file(s). For example, gs://my-bucket/outputs/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#uri GoogleTranscoderJobTemplate#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6187420e9c9db0d9708ff5b380192a2a38ca4a765ba8b5343d8298df8bfcc9)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI for the output file(s). For example, gs://my-bucket/outputs/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#uri GoogleTranscoderJobTemplate#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe28deaf565436ad95b20928bd8fe41e64ad59db3f38aea83120eea43659387e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7149a6a4d73cbbca1be061fb2c36b5c119acf02fca3102c217e3a48f97bd0ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigOutput]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c268a6c6e7c32fea2ec77f3b4fe8176e1891ddc498f6290cd11297270bf3dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlays",
    jsii_struct_bases=[],
    name_mapping={"animations": "animations", "image": "image"},
)
class GoogleTranscoderJobTemplateConfigOverlays:
    def __init__(
        self,
        *,
        animations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobTemplateConfigOverlaysAnimations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        image: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigOverlaysImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param animations: animations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#animations GoogleTranscoderJobTemplate#animations}
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#image GoogleTranscoderJobTemplate#image}
        '''
        if isinstance(image, dict):
            image = GoogleTranscoderJobTemplateConfigOverlaysImage(**image)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ae310201a21a9eaa5476e410deee9c970ecb9f7d449d6b6ed2d951d0c9d733)
            check_type(argname="argument animations", value=animations, expected_type=type_hints["animations"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if animations is not None:
            self._values["animations"] = animations
        if image is not None:
            self._values["image"] = image

    @builtins.property
    def animations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigOverlaysAnimations"]]]:
        '''animations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#animations GoogleTranscoderJobTemplate#animations}
        '''
        result = self._values.get("animations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobTemplateConfigOverlaysAnimations"]]], result)

    @builtins.property
    def image(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigOverlaysImage"]:
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#image GoogleTranscoderJobTemplate#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigOverlaysImage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigOverlays(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysAnimations",
    jsii_struct_bases=[],
    name_mapping={"animation_fade": "animationFade"},
)
class GoogleTranscoderJobTemplateConfigOverlaysAnimations:
    def __init__(
        self,
        *,
        animation_fade: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param animation_fade: animation_fade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#animation_fade GoogleTranscoderJobTemplate#animation_fade}
        '''
        if isinstance(animation_fade, dict):
            animation_fade = GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade(**animation_fade)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b932787ae39e77c35b11ffd53f845a589acd6cc4a2cb815028740fe24f22c4b)
            check_type(argname="argument animation_fade", value=animation_fade, expected_type=type_hints["animation_fade"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if animation_fade is not None:
            self._values["animation_fade"] = animation_fade

    @builtins.property
    def animation_fade(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade"]:
        '''animation_fade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#animation_fade GoogleTranscoderJobTemplate#animation_fade}
        '''
        result = self._values.get("animation_fade")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigOverlaysAnimations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade",
    jsii_struct_bases=[],
    name_mapping={
        "fade_type": "fadeType",
        "end_time_offset": "endTimeOffset",
        "start_time_offset": "startTimeOffset",
        "xy": "xy",
    },
)
class GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade:
    def __init__(
        self,
        *,
        fade_type: builtins.str,
        end_time_offset: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
        xy: typing.Optional[typing.Union["GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fade_type: Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:. - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified. - 'FADE_IN': Fade the overlay object into view. - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#fade_type GoogleTranscoderJobTemplate#fade_type}
        :param end_time_offset: The time to end the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#end_time_offset GoogleTranscoderJobTemplate#end_time_offset}
        :param start_time_offset: The time to start the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#start_time_offset GoogleTranscoderJobTemplate#start_time_offset}
        :param xy: xy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#xy GoogleTranscoderJobTemplate#xy}
        '''
        if isinstance(xy, dict):
            xy = GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy(**xy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ae8a94533d753aad8c1f399608ae3306347c0541ace480a233227e3ce85078)
            check_type(argname="argument fade_type", value=fade_type, expected_type=type_hints["fade_type"])
            check_type(argname="argument end_time_offset", value=end_time_offset, expected_type=type_hints["end_time_offset"])
            check_type(argname="argument start_time_offset", value=start_time_offset, expected_type=type_hints["start_time_offset"])
            check_type(argname="argument xy", value=xy, expected_type=type_hints["xy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fade_type": fade_type,
        }
        if end_time_offset is not None:
            self._values["end_time_offset"] = end_time_offset
        if start_time_offset is not None:
            self._values["start_time_offset"] = start_time_offset
        if xy is not None:
            self._values["xy"] = xy

    @builtins.property
    def fade_type(self) -> builtins.str:
        '''Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:.

        - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified.
        - 'FADE_IN': Fade the overlay object into view.
        - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#fade_type GoogleTranscoderJobTemplate#fade_type}
        '''
        result = self._values.get("fade_type")
        assert result is not None, "Required property 'fade_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_time_offset(self) -> typing.Optional[builtins.str]:
        '''The time to end the fade animation, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#end_time_offset GoogleTranscoderJobTemplate#end_time_offset}
        '''
        result = self._values.get("end_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''The time to start the fade animation, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#start_time_offset GoogleTranscoderJobTemplate#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xy(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy"]:
        '''xy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#xy GoogleTranscoderJobTemplate#xy}
        '''
        result = self._values.get("xy")
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3ac0e38f0a6c090ceebc7d1ef8b7b9f2a59ecd71d4d56db33f53ae53bc0fd46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putXy")
    def put_xy(
        self,
        *,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param x: Normalized x coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#x GoogleTranscoderJobTemplate#x}
        :param y: Normalized y coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#y GoogleTranscoderJobTemplate#y}
        '''
        value = GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy(
            x=x, y=y
        )

        return typing.cast(None, jsii.invoke(self, "putXy", [value]))

    @jsii.member(jsii_name="resetEndTimeOffset")
    def reset_end_time_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTimeOffset", []))

    @jsii.member(jsii_name="resetStartTimeOffset")
    def reset_start_time_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimeOffset", []))

    @jsii.member(jsii_name="resetXy")
    def reset_xy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXy", []))

    @builtins.property
    @jsii.member(jsii_name="xy")
    def xy(
        self,
    ) -> "GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference":
        return typing.cast("GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference", jsii.get(self, "xy"))

    @builtins.property
    @jsii.member(jsii_name="endTimeOffsetInput")
    def end_time_offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="fadeTypeInput")
    def fade_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fadeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeOffsetInput")
    def start_time_offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="xyInput")
    def xy_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy"], jsii.get(self, "xyInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeOffset")
    def end_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTimeOffset"))

    @end_time_offset.setter
    def end_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd9d40578c8436d884cb95227c6c3ef17e1fe2f8b97e0220c23851365a4d1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fadeType")
    def fade_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fadeType"))

    @fade_type.setter
    def fade_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d4721bae386ee353a2052ef6980a68d1dbed78630e8a92ef9e9ae8ad12efe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fadeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68033e22327cdae003913be95e934dbcf44817532e1b64d51080f417ba7563e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5faad8641b9c45e833c91c5c8b3b4761b1897a4a5abf038a662b6f27c8a357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy",
    jsii_struct_bases=[],
    name_mapping={"x": "x", "y": "y"},
)
class GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy:
    def __init__(
        self,
        *,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param x: Normalized x coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#x GoogleTranscoderJobTemplate#x}
        :param y: Normalized y coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#y GoogleTranscoderJobTemplate#y}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec840e61afa6ff82d45f552c8c4010ef901037d4364ec2969ec2d60c86314c62)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
            check_type(argname="argument y", value=y, expected_type=type_hints["y"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x is not None:
            self._values["x"] = x
        if y is not None:
            self._values["y"] = y

    @builtins.property
    def x(self) -> typing.Optional[jsii.Number]:
        '''Normalized x coordinate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#x GoogleTranscoderJobTemplate#x}
        '''
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        '''Normalized y coordinate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#y GoogleTranscoderJobTemplate#y}
        '''
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ad5045459ce55ab6a546f718d11455a394da653932c656e2ecedd3bbc68ecf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetX")
    def reset_x(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetX", []))

    @jsii.member(jsii_name="resetY")
    def reset_y(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetY", []))

    @builtins.property
    @jsii.member(jsii_name="xInput")
    def x_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "xInput"))

    @builtins.property
    @jsii.member(jsii_name="yInput")
    def y_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yInput"))

    @builtins.property
    @jsii.member(jsii_name="x")
    def x(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "x"))

    @x.setter
    def x(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85882f51501775243a29843a4cf9afa4a217dfa64df31c9acc59a1d84d6cd629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "y"))

    @y.setter
    def y(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12e106a9033b6b9cbf4c9dc14e342b68f71c4a637b5db30dbddc77dea13748e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "y", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a75da42203a3c15571fdc0256776a07131f9365c2f47fe31ad4602dc706abe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigOverlaysAnimationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysAnimationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78de6bc5b454b9629a3f11673c16202b5b95ec5255e7e7188ce08096ea6db061)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigOverlaysAnimationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0f4ab59e2bec127a7e0e9c2028a6cd03c24aec4f1ee3280d510141af7674c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigOverlaysAnimationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de3fe3f9a655578da6137aed5a5054d9979a3839cc929852ece9a17d8072438)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab872d31070572af569112e2273364576543fad5ada97301f333c9f1237a9c20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d1b3eb33acbb6dfbcbb7644e6e9f483e1ea9e9706d8287e61c4563960f82e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlaysAnimations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlaysAnimations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlaysAnimations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249d409b7b7989b0fb7968aee524634ec1327b891c89adcd3e59921968b1faa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigOverlaysAnimationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysAnimationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__616eb94ff58c38e2e9ebb915dd7a1cc06c26aa4ce2947104c9ea680abdba6b3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAnimationFade")
    def put_animation_fade(
        self,
        *,
        fade_type: builtins.str,
        end_time_offset: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
        xy: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fade_type: Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:. - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified. - 'FADE_IN': Fade the overlay object into view. - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#fade_type GoogleTranscoderJobTemplate#fade_type}
        :param end_time_offset: The time to end the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#end_time_offset GoogleTranscoderJobTemplate#end_time_offset}
        :param start_time_offset: The time to start the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#start_time_offset GoogleTranscoderJobTemplate#start_time_offset}
        :param xy: xy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#xy GoogleTranscoderJobTemplate#xy}
        '''
        value = GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade(
            fade_type=fade_type,
            end_time_offset=end_time_offset,
            start_time_offset=start_time_offset,
            xy=xy,
        )

        return typing.cast(None, jsii.invoke(self, "putAnimationFade", [value]))

    @jsii.member(jsii_name="resetAnimationFade")
    def reset_animation_fade(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnimationFade", []))

    @builtins.property
    @jsii.member(jsii_name="animationFade")
    def animation_fade(
        self,
    ) -> GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference, jsii.get(self, "animationFade"))

    @builtins.property
    @jsii.member(jsii_name="animationFadeInput")
    def animation_fade_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade], jsii.get(self, "animationFadeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigOverlaysAnimations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigOverlaysAnimations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigOverlaysAnimations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6907e568420879d3ddd28f409b8774673f147bf1343d9fd8c17af5059cbdbc8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysImage",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleTranscoderJobTemplateConfigOverlaysImage:
    def __init__(self, *, uri: builtins.str) -> None:
        '''
        :param uri: URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#uri GoogleTranscoderJobTemplate#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2b65ccc68f673c5ba8d9870d98d1ec722542bdb459071e6a4e880afb2d15a7)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#uri GoogleTranscoderJobTemplate#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigOverlaysImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigOverlaysImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c4e3e1a303c666c44c0a257723425be16633659890d7ceeb81527e80bdeea3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db13be07ba82d1fd4c163710a35b7f08b1da7cffdd0bf9fa1dc4dfb8f57050f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysImage]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba91a1b5322de701c496b1cf3ed5b39c825cf4ab5ee10377649d363c41cf5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigOverlaysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82b1c7912648368c96364d1d5cf3b0a1521f143c8ed0b14ff8e8b5593184cfb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobTemplateConfigOverlaysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65566b51c25a5eb39bb34919a78d6e2ad508cd67ad35ade192c86fcaa2ca024)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobTemplateConfigOverlaysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3877061a2d6eed05fb70fa00f7a5c8e9c9c4c06b19a1945ff6063a216d6b20b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3d44d97962b739b433caf0165d500a05159438839276c3bba8e0480f3c29314)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e7503d6a3c5d7414f05ba531164893867fdb164e495383107a327812f01b4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlays]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlays]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlays]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bacbe35f8cf829fd8573a34ebf5c65035b42bf605f9aa33b1f5e20ea7926ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobTemplateConfigOverlaysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigOverlaysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c192858fdc50459f0969894159c95b05f2fcb3c85040760a04f492c1a4ba0c32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAnimations")
    def put_animations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a16c29d17055c1d7676ca075fceee9d86d3faf48372430ca10e94fe2699fdba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnimations", [value]))

    @jsii.member(jsii_name="putImage")
    def put_image(self, *, uri: builtins.str) -> None:
        '''
        :param uri: URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#uri GoogleTranscoderJobTemplate#uri}
        '''
        value = GoogleTranscoderJobTemplateConfigOverlaysImage(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="resetAnimations")
    def reset_animations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnimations", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @builtins.property
    @jsii.member(jsii_name="animations")
    def animations(self) -> GoogleTranscoderJobTemplateConfigOverlaysAnimationsList:
        return typing.cast(GoogleTranscoderJobTemplateConfigOverlaysAnimationsList, jsii.get(self, "animations"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> GoogleTranscoderJobTemplateConfigOverlaysImageOutputReference:
        return typing.cast(GoogleTranscoderJobTemplateConfigOverlaysImageOutputReference, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="animationsInput")
    def animations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlaysAnimations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlaysAnimations]]], jsii.get(self, "animationsInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysImage]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysImage], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigOverlays]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigOverlays]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigOverlays]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79194aa211478a18a304d4ea2d685b81d11c3c2b27fd9e68a47b2fd08f0471f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigPubsubDestination",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class GoogleTranscoderJobTemplateConfigPubsubDestination:
    def __init__(self, *, topic: typing.Optional[builtins.str] = None) -> None:
        '''
        :param topic: The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#topic GoogleTranscoderJobTemplate#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec8be56e7809c1b7c4e117365cc77cf0490928ce26a16ebfca47328514ad85a)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#topic GoogleTranscoderJobTemplate#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateConfigPubsubDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateConfigPubsubDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateConfigPubsubDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__277861859962e7074d017ff5102467f579812ecbe66d37fe1d4b1fe84f1b9b63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTopic")
    def reset_topic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopic", []))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9beb7dcefb26da0516c0074589f98748554664e31ee6925f5c89fbad3f92ee37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobTemplateConfigPubsubDestination]:
        return typing.cast(typing.Optional[GoogleTranscoderJobTemplateConfigPubsubDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobTemplateConfigPubsubDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfde67300a698a7e3b75b884080583cf00ed783030be14f01a453f68424250a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleTranscoderJobTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#create GoogleTranscoderJobTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#delete GoogleTranscoderJobTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#update GoogleTranscoderJobTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb048b193c3778731a98a46180c5e170aa41fb2a8a8d0105b77f1de7eb96eac7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#create GoogleTranscoderJobTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#delete GoogleTranscoderJobTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job_template#update GoogleTranscoderJobTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJobTemplate.GoogleTranscoderJobTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c41bfb7504b19686de9871eeb392751e2ec40ec524ed3ee4de482c5eb4efa1a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d0579465ca7cc7de9104af45e6d4b8b5507409b9469a6a13ee9a6170a7ae203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b19869bd34cc7784db3c015ea506a17c027fbd1854a4db3d3f9325a859bc8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee3bf5460b15de1963c57284652b6b8b86cec588a9691e204f05b83ef73e6dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafda4135bd778a2131711e9ecec3a32ea6714f1bec05ca8fc8582c0b73ca95f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleTranscoderJobTemplate",
    "GoogleTranscoderJobTemplateConfig",
    "GoogleTranscoderJobTemplateConfigA",
    "GoogleTranscoderJobTemplateConfigAOutputReference",
    "GoogleTranscoderJobTemplateConfigAdBreaks",
    "GoogleTranscoderJobTemplateConfigAdBreaksList",
    "GoogleTranscoderJobTemplateConfigAdBreaksOutputReference",
    "GoogleTranscoderJobTemplateConfigEditListStruct",
    "GoogleTranscoderJobTemplateConfigEditListStructList",
    "GoogleTranscoderJobTemplateConfigEditListStructOutputReference",
    "GoogleTranscoderJobTemplateConfigElementaryStreams",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsList",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsOutputReference",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference",
    "GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptions",
    "GoogleTranscoderJobTemplateConfigEncryptionsAes128",
    "GoogleTranscoderJobTemplateConfigEncryptionsAes128OutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine",
    "GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsList",
    "GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc",
    "GoogleTranscoderJobTemplateConfigEncryptionsMpegCencOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsSampleAes",
    "GoogleTranscoderJobTemplateConfigEncryptionsSampleAesOutputReference",
    "GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource",
    "GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference",
    "GoogleTranscoderJobTemplateConfigInputs",
    "GoogleTranscoderJobTemplateConfigInputsList",
    "GoogleTranscoderJobTemplateConfigInputsOutputReference",
    "GoogleTranscoderJobTemplateConfigManifests",
    "GoogleTranscoderJobTemplateConfigManifestsList",
    "GoogleTranscoderJobTemplateConfigManifestsOutputReference",
    "GoogleTranscoderJobTemplateConfigMuxStreams",
    "GoogleTranscoderJobTemplateConfigMuxStreamsList",
    "GoogleTranscoderJobTemplateConfigMuxStreamsOutputReference",
    "GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings",
    "GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference",
    "GoogleTranscoderJobTemplateConfigOutput",
    "GoogleTranscoderJobTemplateConfigOutputOutputReference",
    "GoogleTranscoderJobTemplateConfigOverlays",
    "GoogleTranscoderJobTemplateConfigOverlaysAnimations",
    "GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade",
    "GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference",
    "GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy",
    "GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference",
    "GoogleTranscoderJobTemplateConfigOverlaysAnimationsList",
    "GoogleTranscoderJobTemplateConfigOverlaysAnimationsOutputReference",
    "GoogleTranscoderJobTemplateConfigOverlaysImage",
    "GoogleTranscoderJobTemplateConfigOverlaysImageOutputReference",
    "GoogleTranscoderJobTemplateConfigOverlaysList",
    "GoogleTranscoderJobTemplateConfigOverlaysOutputReference",
    "GoogleTranscoderJobTemplateConfigPubsubDestination",
    "GoogleTranscoderJobTemplateConfigPubsubDestinationOutputReference",
    "GoogleTranscoderJobTemplateTimeouts",
    "GoogleTranscoderJobTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__db4f17b171551d51cc1b1d55d96641a1e0834f51b667c2e06d9f17070907ed4b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    job_template_id: builtins.str,
    location: builtins.str,
    config: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleTranscoderJobTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2d8f8616519348bc1f1e4bd1afdbcb9475b6055344a7ffc2547a549a5607ae92(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ec0e68ba7587540a7c9d3158086554a5dfd0348bebadbe540b6f2b976b24f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2338cdcfc0779706570fd153fa794af7eaeb4a05164a3b58247b247a74e8528(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca590331e648758d43d0c821ee42fa55fb2a3d12b2317b948a620555eb60169d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2234994cd7e74a2811d362aad8452bf8b0a198c036be114d4cc30f320eb751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e38cfcf5860e17d7943d99ab54827bb7508a693f1c8414d25290682be9e82fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49c0d212aa10ba6dbc85c20a6cbbcffd8b574005d0f00e551e37798601c78e3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    job_template_id: builtins.str,
    location: builtins.str,
    config: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleTranscoderJobTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac7696d23bb024e9ffbab187a2cb6f3bbff533be14dac917e883371265f3f5c(
    *,
    ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigAdBreaks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigEditListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigEncryptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigInputs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigManifests, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigMuxStreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    output: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigOverlays, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pubsub_destination: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigPubsubDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc15465606740a48ae3ca8131d25b95e29bceb1c01b2f078345a9023a430e59d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bdd864dc9333d85ee8444271a75a6c3b04e027b56226f577ac14f31ced94e9e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigAdBreaks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0386e902ec08410e4c9204f5a7401a94eb94cfb0f33540884a07732495f77c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigEditListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda44e96cc1360a263b262153ae14ad080e7ea227a73ed72b866e16a818a6218(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30ff52d147da2d915460141c672ab7d756b49d13a1f7c7272ed80ab046e8a8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigEncryptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157a1dd1920af133d8079deb54eda891c122d398b903e2516a27222c016437bd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigInputs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc6f39b6c8caa1df8ba845ff4d2e64c9980053aee71d904dfc57d13525c35ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigManifests, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671e74d7c5c59df922ee844abe86e643b75bc5de9765c771a38899fc02ace595(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigMuxStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcabaad0cdc159ea4a9b51d60ffb79a296ebba5ed5ca4e73a2bd91a8a32f338(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigOverlays, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc08d868a2eef28d2b0c5ba8b2acfc64a8985b52a84939d07b6b628cc13e55a(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4b02b79c23aeb4fe9646fa69509ac5699d9df62d9c9cd1b26157a388a231e6(
    *,
    start_time_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17c4f82937c53ad216e7687d2afd871df18cd90d5af69d0cf7fc38b8e3ddcb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923ff92946a72fd216f1f9eaa622e17580744a190957261076c28173ade99089(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ea22876b5963d71a9f41e5f251975fa90683215afbc2890488c7a497caeb7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecfbc4905530c70915f72dc8f8e30d86c3be6ca1e75587c0f9ac6e34fb5a8aa9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c8980da4079294d8e13c0c4761aef8d102b05ec2ed78068a51c0d89106f503(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d385f218dc177ff5b9bb815867ef92776eb54c6904c3af66625263a2841516d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigAdBreaks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917d709f39e7373f6e6ab4954157f647f871da181129e1c7ad1570a16ae2124c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028a2ceec547f30f2d29fabaec5c57b7cea9cbd64247027d64fd3ff05744671f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f97d43de025782272a83bd2571e7f21628b26fd3dca240e48e27b437cffc57b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigAdBreaks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fe2bfbb2b9ab3eee71ecfc28c9e78caf4b4c8b789cb2fa4797b3eeee2d7b27(
    *,
    inputs: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[builtins.str] = None,
    start_time_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409bde7b1316629c094c4ba331336b4939a4e433b1ad9e12f8c156756773654f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdf7a4257e166cd53b6f833fa33d3b4b1d975f1c1c83054662f6093a905cb4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b474b6a39f9e68e7e2c25d819c07c3a2409621e642a6da9e17aab6d7967e5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5bd1f3d26154b824aaf68d3373fff596de7b50b41890cab913f157f8d897b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeabd1aa5ab336bdb0362fd1e65af23c0e67b73ba799d4334d912dfac3679a21(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebea8a4c16a1d9ff1d2a4143b144db74896179789a1461a30c325d78b7eb6928(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigEditListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802a84afe7f35fe5c8cee7f37dfe53c2e4417624029ae80256aa01c7493bfe8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887f8492ab5f783d36f892249625e388251f213b059446264c38b7912ebc356c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d304f9a6acdbdf58adafc7ad9dd030a979c4d54c733fa10c2448a012b548095b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a32759d21861075d543fc33c707be659c7942042815912af836d25b91dda32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b5bd2b17907de50090b8462a49e09dc2b9a9d879746312e681d2ee0b611c94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigEditListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9365d4f036b59438abdcac0404980a5757db8aa4db677f17ab84d2e06b0a5df6(
    *,
    audio_stream: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream, typing.Dict[builtins.str, typing.Any]]] = None,
    key: typing.Optional[builtins.str] = None,
    video_stream: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f20a89c23a527ece35d2fe46214ed6493be169fda0c00ef90e87d0531e4028f(
    *,
    bitrate_bps: jsii.Number,
    channel_count: typing.Optional[jsii.Number] = None,
    channel_layout: typing.Optional[typing.Sequence[builtins.str]] = None,
    codec: typing.Optional[builtins.str] = None,
    sample_rate_hertz: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0231d84419055313578ca9e071bdb496cf20cc3a578fc43658369a6f1cee0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc65baae4fbb73f981b2ff4e39b85acdb7956683e868dad7ce6a88d3c06d104f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a547ae6d996aa833a09560f5ef5a35624934da75756822492c9dbc7fdc134076(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b351ff1e7f4ab9c8fa41953d8e1c56c3f600e8e80e9341acb95f1a6eac0529c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f5e38012608ddab19bf34b1c3022663ba7736ab955dd4d6b7e98d8fba6deae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4075069a1e7351f4a4267811e4f44c13715bfaa34a3650477deb632a3f2f5913(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca8ba51cdbf4833496d9361fc27b00c1eb685fa6102357d7960fb866693f11b(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsAudioStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cc14acbe063b7e27f35fb739eb78e6c5a3402555110cfac4d840971e48206c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18aec9795e2073e1a265ba8586cdd548b6fe228157cf51db9e8f17e9d667073b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cda6d7a029e8471c9c46a3f518f9f5cade777e25d9a8ed4371aa7ed5301c558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e669ab5fccca9998ec594afdfb23011b13e59df5251ec6f571ad7624a03685d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514b88417d291a8c0a5f8cf819acb94c2224dffba997e12de83c24c196086e74(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c8c06d3e14dfc93024e136e3cdf6e10af100909c3da09ed0dc3280b01dbe50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigElementaryStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1990a4bc00b39328ad264b8f2068467688bca4b5df9aff44d30f8e97916697c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab191b72235414332a43773fb2d6689b85cc164d8b3cac5f628daff97d573d6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88b74a25fd6e7fc0ea1cd17ac407f1add746c908b2f99b2cd6e38bc2df2719d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigElementaryStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f458bb35fcf84bcbb6d3eef56d26dfaa33736b895d90ad8f99ee443d0467923e(
    *,
    h264: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722749e293b435d48c477399b20610d2057d48f1cd3f9bae7ec09f2d444ff67c(
    *,
    bitrate_bps: jsii.Number,
    frame_rate: jsii.Number,
    crf_level: typing.Optional[jsii.Number] = None,
    entropy_coder: typing.Optional[builtins.str] = None,
    gop_duration: typing.Optional[builtins.str] = None,
    height_pixels: typing.Optional[jsii.Number] = None,
    hlg: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg, typing.Dict[builtins.str, typing.Any]]] = None,
    pixel_format: typing.Optional[builtins.str] = None,
    preset: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    rate_control_mode: typing.Optional[builtins.str] = None,
    sdr: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr, typing.Dict[builtins.str, typing.Any]]] = None,
    vbv_fullness_bits: typing.Optional[jsii.Number] = None,
    vbv_size_bits: typing.Optional[jsii.Number] = None,
    width_pixels: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c7c79c2d4e338d0734c562cae0762ae0445e86dd843f76eb70151c968c88f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250b4739b5ad8a4b5f04d20b0dc83d71c07875da3f024f2a0f27cee37de5dacc(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81faee6600a38a1548cdaefc7f7c0054bf4a60cfa695af28993e43b30df5c43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7540900af3764b20fda022d8ad6af5f1fb483bfe15b6a40f89469b6c904727(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722be86802126a9536607a6ee3de9cc0644f9bf55ccc5461bb63c4b54811f02c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88fc1a6f2b3178d270cd2b52efe4461ad558c33be7e04c2609fc126e04efab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d492c21e32d33b827681393dd05b2eec36a81227478eceee152641c949fb3851(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2e5a82284faa5f0d4ca9d7e1c9016a952c0cbc03945e736043e981ded73898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9096a1b8d05fc63f4d7bc56a78f3f86b0d0179f2ab08369e79123355cd55495b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b256989c23e133cb14dbb28b80f9297eb10ebbca934de718672af2e53daebd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0913d012c277198825ea71ff06f7895ffd47734e431e1fd110f81aaaec0c99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea0266db84d47a949974cac569bf3e3c54baeda440881428d4b4caeeb2df9fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1f873fbb8e28f5ab40457088e8a8afd845c4a87a45d19bc0024df6b8cea9e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c54428fa89b8efb928ce29b87fbac52c16d01c4d0f0cb75a1f3a01999d91b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5334ac196c46faf9cf11eb7e3f5dfca069082e33534e3a37c89b87814ecd512c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c14bc9557b1f8c336b02599f822a485c86001b9889dceb14024f44770197c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c986507fe697b5e803eb3ab715bebeacaa564c45b95e6c6e64452631a2a83f3(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224ff07087ba509664881972ab0f355faa8b97a37295d9b0c88b2dfe9e42bf70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d485c324067a2ae8c201e55dc28c167f1247e5a685419ddabcd64045296d7c(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52cfa51833dd6b60549141331fbe2487563c17f7846a04457bc945cf38f4e64e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe1dede1bd281ffb643ad70fd3c554f53fe827afce432e8052477418dcbadde(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigElementaryStreamsVideoStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830a422d027cd6f3ede301748de99284117b07d82d6d37ff5e10fdfb0c03ead8(
    *,
    id: builtins.str,
    aes128: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsAes128, typing.Dict[builtins.str, typing.Any]]] = None,
    drm_systems: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems, typing.Dict[builtins.str, typing.Any]]] = None,
    mpeg_cenc: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc, typing.Dict[builtins.str, typing.Any]]] = None,
    sample_aes: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsSampleAes, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_manager_key_source: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac406a877a8690483e1c85fac2811b4bdc2f343ea1f9e7cd83eb807622baad7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d2a5e2377b8aa896067dff0ebfe993e5fdf41a6e4a3598d49367472518dcbe(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsAes128],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53aed28f6fadcae703e52eec98cb99cc627d10c4528fd205305759ec832ffcf(
    *,
    clearkey: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey, typing.Dict[builtins.str, typing.Any]]] = None,
    fairplay: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
    playready: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
    widevine: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb83e8404cc7ab244928083792bbe0fe72569966f8bd6310e5fa8fea8808afac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f934fc8cf958815fcf88698d9fb12925fc64e4c8f06c30406be2e6badc98fc(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bc1eb55997f61122ebd830b56353b7ed4cd3f4bc9ac69b32541770b1a01ae8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082ff3a15b8754775f5be80b2d29c19e02f5d8cdf2ccff97812e7846af70699f(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169817df69ea7f08fb4f19ff178acc037d5fbbfb182d4a20feb00017e876967e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22c56d62f139e3399b3c5406c97c9ea2f79b076f3bb1b41ff02ebe801ac725a(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystems],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1895089f8206ef1a98e3cb51ae863ea3484e6c7488898db1bc7ef8579df1bb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b7b1f7b39aa2d6242c6027f304f6bdbfa3013893f53b2f34729abcd1a3d0da(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7ef10c079b877389872d1bd6e9705085ef3a0f898a65d41c17d10593a400ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a623f7da3e714bb4b5d212dcb4bbceef8732a7e24ef588c0abd29efaf1357db(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce95cef57cf7d7181161cd7c950e9fab9f8663fd454716aa77ae809dd687c2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b6f8fcb986fec21fa2950db876ec1fd390ec04d77196b8e421be9da8464ffc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d90407fd65d433f77e301825a8ea516a828e2d4f96d701420dc8f21945db23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17835a56a9a8751e0fe801878bbba0e7aed4c552819f10c1c3b35ea9d0e0f357(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d097dd2d9f9dd5755c99ecbc311a6c6c7d2222ae723fccc906faff1517595a8a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d76266c374212ff577d17af4fc9ed65f01d3e3c1024d28df037065569d0d66(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigEncryptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90c88f66339ec6fb23b98dd9fcaa1d2f74c960a950f56b4d0d644f4b47be37f(
    *,
    scheme: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4318f0ec17aa3117703bffb6dd673337f3e5cb5f2e0504c204ee4ef7f1025f61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be48df5dab479a7be82d909b36232347600264b7a2810a74e3a59e4108a90ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db1d6183ce5faafebd004c5b1ca54ac616ae5d510dd6b23aff094568f806747(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsMpegCenc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b7a007532f798f095cb5d5d609b85f2a38be7b909f35a095691164667ad80f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1171ca056dfc1dec94fd642d7362f20165ffda099db389cf722154853430548e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5737cf9e4ddbd154b2f6d6deb1c60bc8b837f0e7f65e0c2760db32ca084eb59a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigEncryptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc04953bf10a2dfe525feb994d145b93a28cc831bdb5a8aeb103ccabe3562e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d71c3f5587444b4025ecfc11cded2bf94e5aac358152d589c9ee4c455a5945(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsSampleAes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d95ee8c3b2ff03f7aa113b5d8301f35d73aefcf05d2abbc40e90c7b4366c27b(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a866c51a88286dfd748fbe0aea756b29c5783dd472a9c328b1a7b2739aca64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbaff92cb448063fecc67b3628665d83ffb5b050ac4963b1c0c9fb2020337ecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef26f425ebbf1209b122ccbca345f2f54b01bdb16d514364eebf1e5ac4c6592(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigEncryptionsSecretManagerKeySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fcaf97a56b47d76f05551e80b89a38c4d955a203af8e10c1081e51461d1fbd(
    *,
    key: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3015f35d94e60c158dbad08d84c253a1d6df9896d4a0351a78e343f5e2044a64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556d04e93ba8c64df43dde974742361ba1b66bb74afce777c53d4eb0fb2ef706(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c936a4b382cddd3f35c34c06554cd74d48975d026026865a43859b74e1c0d6b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97709a2733e8e94cee0587d08adf2a561c74d32ddb44dd31816d9436a13b8fdd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e60d600e60623853c6e35808f8b19b320de41e949a44eb0c2063c05b875e025(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5576842863641d833f5547f1edde0a018bae9709afc87cd675e78fc315395909(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigInputs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4570869b82339572d3436b8da90fc027edbb4a33c6bacca53fbfabc3500431(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a707aa2d6076dfb45cf31de5f9732751a9bd452fd168e7c0355c638ae07bf264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab41ec202afab31c7c9632f14a6e0e2764ab9b1f1b82bbaa5ee4575f2eb8d014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e992b2dd5bf2c1f86e4596616d670dbb917a31527649e22153c62d0c6087fd63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigInputs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ee6b8a007520df1d0d98f58682e3a4106360f31ca310c68183adca5e869e7c(
    *,
    file_name: typing.Optional[builtins.str] = None,
    mux_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d96aa2d46daaef4c748aa969306255624fb4cf4ad43fbb25743fa7909a2b85f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a755739e25d0eb2d8f33ca39e6cfa98be8f84c0f7b1835353336197d834630(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef47d722332136fd465ecedb4b8d35e816a1c6ffa9c6a6abf96db1a063a1da90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d146374a58053d65d57879430a5a744adf4fb539e1443318a69496e4ca7885eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d807696f270a556761d396295a8aff85cfa653a30ded9cb14cff145cd88d986c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783e40b9e4096f73fc90d68b37fc80b6f11967e3c358f3f96468a373c02439b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigManifests]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51ff8adaf375d1871659aab3fad94bd12dcabf183cee1aeb5cf06616e0c79ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e816828fbf48c88138c206590fcfad9c4997e968ca931da636051e014ef0503(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6e8f060d99cbc3a7cc4b27ffd6f6be4bccc70d28d027720e69e14465338dcb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262ab5ccc88910a3683f2949fbf9ed77c88207ba4e46b152a0c0d3393d743030(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05ca866b6d90382390b86b6542ba6b7504ea7d0265ebbf7a86c9a414b6b40cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigManifests]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f87daacee7cd781a487d9af20d439ba42d7cfc6373146f972e101129459830a(
    *,
    container: typing.Optional[builtins.str] = None,
    elementary_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_id: typing.Optional[builtins.str] = None,
    file_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    segment_settings: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0878cf1ae5363f7cc7005dd2d8ccebcce15ca31af2430aa0c152a463dcd05939(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7da193a76cdd014c715c70c91269d478c6f9ba8c590307359c29e4615c808d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e90e719ed4046f1786445792a1672352abc00bc227fa1d2e2fc4423a93f1e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38783cc0e05d96ccff3f496624cf0fb21d6171bd03ee957aa83c44d28435351(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c2a2bbe75e00f9e027b1d28122d7bdd5e41d73388cd4352b630f9def7267ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71657caf5a4bc945c6188d47461de021854069a9f680aeb4eb529496334f5d8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigMuxStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774815268f53c86ddc56806cdf60a9b2ff1b35ac3f2659f7a6343ea53f5e4c59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3dda482ad0e4c560a1db2a88c77628e66f035f0af3037735a7b170fbf3f0fe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf407a8671b9d0484046b4308808dc82233c55ab6262c34eddac450e425f698(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aae8e2e7a184335585fa165d46c4292799ef1d3b189dd7497108c809edbf469(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c573afcbccc8c764cc2b3d6cbe080352b2b889b0c5b37b5e86a4a59b74303a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edf01af9f5c32f0be733bd69a2e131ab2129004c13a52bbaaff7c465b51342b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9ec2979ce67c1a3263825b67f726d683219ef76543dba41aed6a05590d9417(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigMuxStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775b229cd77969c0e3a4523dcc3e97c0235eeee4546ce1cc0f985346c9fe90e2(
    *,
    segment_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409c9d8662795ac84e01ad323f4c6482ec4e857a5d3cfff756d1a38a358ae553(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ede5feac21dfbbede352c4b069aac3f9930b4167c17d9a071599b6afd0d793(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a4748b3c12b8b872bea82f202f513cf0800da607d7bb8adba61d1f1d5c61b9(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigMuxStreamsSegmentSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6187420e9c9db0d9708ff5b380192a2a38ca4a765ba8b5343d8298df8bfcc9(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe28deaf565436ad95b20928bd8fe41e64ad59db3f38aea83120eea43659387e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7149a6a4d73cbbca1be061fb2c36b5c119acf02fca3102c217e3a48f97bd0ee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c268a6c6e7c32fea2ec77f3b4fe8176e1891ddc498f6290cd11297270bf3dd2(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ae310201a21a9eaa5476e410deee9c970ecb9f7d449d6b6ed2d951d0c9d733(
    *,
    animations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    image: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigOverlaysImage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b932787ae39e77c35b11ffd53f845a589acd6cc4a2cb815028740fe24f22c4b(
    *,
    animation_fade: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ae8a94533d753aad8c1f399608ae3306347c0541ace480a233227e3ce85078(
    *,
    fade_type: builtins.str,
    end_time_offset: typing.Optional[builtins.str] = None,
    start_time_offset: typing.Optional[builtins.str] = None,
    xy: typing.Optional[typing.Union[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ac0e38f0a6c090ceebc7d1ef8b7b9f2a59ecd71d4d56db33f53ae53bc0fd46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd9d40578c8436d884cb95227c6c3ef17e1fe2f8b97e0220c23851365a4d1b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d4721bae386ee353a2052ef6980a68d1dbed78630e8a92ef9e9ae8ad12efe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68033e22327cdae003913be95e934dbcf44817532e1b64d51080f417ba7563e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5faad8641b9c45e833c91c5c8b3b4761b1897a4a5abf038a662b6f27c8a357(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec840e61afa6ff82d45f552c8c4010ef901037d4364ec2969ec2d60c86314c62(
    *,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad5045459ce55ab6a546f718d11455a394da653932c656e2ecedd3bbc68ecf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85882f51501775243a29843a4cf9afa4a217dfa64df31c9acc59a1d84d6cd629(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12e106a9033b6b9cbf4c9dc14e342b68f71c4a637b5db30dbddc77dea13748e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a75da42203a3c15571fdc0256776a07131f9365c2f47fe31ad4602dc706abe5(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78de6bc5b454b9629a3f11673c16202b5b95ec5255e7e7188ce08096ea6db061(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0f4ab59e2bec127a7e0e9c2028a6cd03c24aec4f1ee3280d510141af7674c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de3fe3f9a655578da6137aed5a5054d9979a3839cc929852ece9a17d8072438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab872d31070572af569112e2273364576543fad5ada97301f333c9f1237a9c20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1b3eb33acbb6dfbcbb7644e6e9f483e1ea9e9706d8287e61c4563960f82e46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249d409b7b7989b0fb7968aee524634ec1327b891c89adcd3e59921968b1faa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlaysAnimations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616eb94ff58c38e2e9ebb915dd7a1cc06c26aa4ce2947104c9ea680abdba6b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6907e568420879d3ddd28f409b8774673f147bf1343d9fd8c17af5059cbdbc8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigOverlaysAnimations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2b65ccc68f673c5ba8d9870d98d1ec722542bdb459071e6a4e880afb2d15a7(
    *,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4e3e1a303c666c44c0a257723425be16633659890d7ceeb81527e80bdeea3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db13be07ba82d1fd4c163710a35b7f08b1da7cffdd0bf9fa1dc4dfb8f57050f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba91a1b5322de701c496b1cf3ed5b39c825cf4ab5ee10377649d363c41cf5aa(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigOverlaysImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b1c7912648368c96364d1d5cf3b0a1521f143c8ed0b14ff8e8b5593184cfb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65566b51c25a5eb39bb34919a78d6e2ad508cd67ad35ade192c86fcaa2ca024(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3877061a2d6eed05fb70fa00f7a5c8e9c9c4c06b19a1945ff6063a216d6b20b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d44d97962b739b433caf0165d500a05159438839276c3bba8e0480f3c29314(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7503d6a3c5d7414f05ba531164893867fdb164e495383107a327812f01b4d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bacbe35f8cf829fd8573a34ebf5c65035b42bf605f9aa33b1f5e20ea7926ee3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobTemplateConfigOverlays]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c192858fdc50459f0969894159c95b05f2fcb3c85040760a04f492c1a4ba0c32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a16c29d17055c1d7676ca075fceee9d86d3faf48372430ca10e94fe2699fdba(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobTemplateConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79194aa211478a18a304d4ea2d685b81d11c3c2b27fd9e68a47b2fd08f0471f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateConfigOverlays]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec8be56e7809c1b7c4e117365cc77cf0490928ce26a16ebfca47328514ad85a(
    *,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277861859962e7074d017ff5102467f579812ecbe66d37fe1d4b1fe84f1b9b63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9beb7dcefb26da0516c0074589f98748554664e31ee6925f5c89fbad3f92ee37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfde67300a698a7e3b75b884080583cf00ed783030be14f01a453f68424250a(
    value: typing.Optional[GoogleTranscoderJobTemplateConfigPubsubDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb048b193c3778731a98a46180c5e170aa41fb2a8a8d0105b77f1de7eb96eac7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41bfb7504b19686de9871eeb392751e2ec40ec524ed3ee4de482c5eb4efa1a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0579465ca7cc7de9104af45e6d4b8b5507409b9469a6a13ee9a6170a7ae203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b19869bd34cc7784db3c015ea506a17c027fbd1854a4db3d3f9325a859bc8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee3bf5460b15de1963c57284652b6b8b86cec588a9691e204f05b83ef73e6dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafda4135bd778a2131711e9ecec3a32ea6714f1bec05ca8fc8582c0b73ca95f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
