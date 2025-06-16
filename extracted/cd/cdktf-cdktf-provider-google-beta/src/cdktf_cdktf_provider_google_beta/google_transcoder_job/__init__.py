r'''
# `google_transcoder_job`

Refer to the Terraform Registry for docs: [`google_transcoder_job`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job).
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


class GoogleTranscoderJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job google_transcoder_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        config: typing.Optional[typing.Union["GoogleTranscoderJobConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleTranscoderJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job google_transcoder_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the transcoding job resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#location GoogleTranscoderJob#location}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#config GoogleTranscoderJob#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#id GoogleTranscoderJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this job. You can use these to organize and group your jobs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#labels GoogleTranscoderJob#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#project GoogleTranscoderJob#project}.
        :param template_id: Specify the templateId to use for populating Job.config. The default is preset/web-hd, which is the only supported preset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#template_id GoogleTranscoderJob#template_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#timeouts GoogleTranscoderJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf9fc8c3f9281a1d3a454c502dac0222129f7c60fb1e6f74ace3626508f3126)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = GoogleTranscoderJobConfig(
            location=location,
            config=config,
            id=id,
            labels=labels,
            project=project,
            template_id=template_id,
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
        '''Generates CDKTF code for importing a GoogleTranscoderJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleTranscoderJob to import.
        :param import_from_id: The id of the existing GoogleTranscoderJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleTranscoderJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5aaf03a2265fcd69733494fc76250715b2155463a026837f7159b4a1c46ae5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigInputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigManifests", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union["GoogleTranscoderJobConfigOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigOverlays", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pubsub_destination: typing.Optional[typing.Union["GoogleTranscoderJobConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_breaks: ad_breaks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#ad_breaks GoogleTranscoderJob#ad_breaks}
        :param edit_list: edit_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#edit_list GoogleTranscoderJob#edit_list}
        :param elementary_streams: elementary_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#elementary_streams GoogleTranscoderJob#elementary_streams}
        :param encryptions: encryptions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#encryptions GoogleTranscoderJob#encryptions}
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#inputs GoogleTranscoderJob#inputs}
        :param manifests: manifests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#manifests GoogleTranscoderJob#manifests}
        :param mux_streams: mux_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#mux_streams GoogleTranscoderJob#mux_streams}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#output GoogleTranscoderJob#output}
        :param overlays: overlays block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#overlays GoogleTranscoderJob#overlays}
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#pubsub_destination GoogleTranscoderJob#pubsub_destination}
        '''
        value = GoogleTranscoderJobConfigA(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#create GoogleTranscoderJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#delete GoogleTranscoderJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#update GoogleTranscoderJob#update}.
        '''
        value = GoogleTranscoderJobTimeouts(
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

    @jsii.member(jsii_name="resetTemplateId")
    def reset_template_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateId", []))

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
    def config(self) -> "GoogleTranscoderJobConfigAOutputReference":
        return typing.cast("GoogleTranscoderJobConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

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
    def timeouts(self) -> "GoogleTranscoderJobTimeoutsOutputReference":
        return typing.cast("GoogleTranscoderJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["GoogleTranscoderJobConfigA"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigA"], jsii.get(self, "configInput"))

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
    @jsii.member(jsii_name="templateIdInput")
    def template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleTranscoderJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleTranscoderJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50f82e1450109ac19b481bd64518900d1ea0454fbfdd7331c5d081db5005d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d747742b9d7f1d47ba32812c4c3ed1472a5fa95e6f6ab644fa9edb390d9f231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e970d25e796aee55b3f659166af344e5d5133580e809af0fffdcc9daa399dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c507cac81ff0002589729ff956a69cf82686e038426213ec0719368634a769ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateId"))

    @template_id.setter
    def template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9ab944883518bf8c5eec70c28db69321b5c17c306d2619ee375df64666aac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfig",
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
        "config": "config",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "template_id": "templateId",
        "timeouts": "timeouts",
    },
)
class GoogleTranscoderJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: typing.Optional[typing.Union["GoogleTranscoderJobConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleTranscoderJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the transcoding job resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#location GoogleTranscoderJob#location}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#config GoogleTranscoderJob#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#id GoogleTranscoderJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this job. You can use these to organize and group your jobs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#labels GoogleTranscoderJob#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#project GoogleTranscoderJob#project}.
        :param template_id: Specify the templateId to use for populating Job.config. The default is preset/web-hd, which is the only supported preset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#template_id GoogleTranscoderJob#template_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#timeouts GoogleTranscoderJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = GoogleTranscoderJobConfigA(**config)
        if isinstance(timeouts, dict):
            timeouts = GoogleTranscoderJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bf03f0cef5ee535fffe442a5962b0b411fa3d18cbabd56204a274e1b8d0054)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if template_id is not None:
            self._values["template_id"] = template_id
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
        '''The location of the transcoding job resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#location GoogleTranscoderJob#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["GoogleTranscoderJobConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#config GoogleTranscoderJob#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#id GoogleTranscoderJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels associated with this job. You can use these to organize and group your jobs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#labels GoogleTranscoderJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#project GoogleTranscoderJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_id(self) -> typing.Optional[builtins.str]:
        '''Specify the templateId to use for populating Job.config. The default is preset/web-hd, which is the only supported preset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#template_id GoogleTranscoderJob#template_id}
        '''
        result = self._values.get("template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleTranscoderJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#timeouts GoogleTranscoderJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleTranscoderJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigA",
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
class GoogleTranscoderJobConfigA:
    def __init__(
        self,
        *,
        ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigInputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigManifests", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union["GoogleTranscoderJobConfigOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigOverlays", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pubsub_destination: typing.Optional[typing.Union["GoogleTranscoderJobConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_breaks: ad_breaks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#ad_breaks GoogleTranscoderJob#ad_breaks}
        :param edit_list: edit_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#edit_list GoogleTranscoderJob#edit_list}
        :param elementary_streams: elementary_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#elementary_streams GoogleTranscoderJob#elementary_streams}
        :param encryptions: encryptions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#encryptions GoogleTranscoderJob#encryptions}
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#inputs GoogleTranscoderJob#inputs}
        :param manifests: manifests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#manifests GoogleTranscoderJob#manifests}
        :param mux_streams: mux_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#mux_streams GoogleTranscoderJob#mux_streams}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#output GoogleTranscoderJob#output}
        :param overlays: overlays block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#overlays GoogleTranscoderJob#overlays}
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#pubsub_destination GoogleTranscoderJob#pubsub_destination}
        '''
        if isinstance(output, dict):
            output = GoogleTranscoderJobConfigOutput(**output)
        if isinstance(pubsub_destination, dict):
            pubsub_destination = GoogleTranscoderJobConfigPubsubDestination(**pubsub_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd613debed1907f28e33df26d20bde8a6b06a850b74c2f8085fe74ac07101fc5)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigAdBreaks"]]]:
        '''ad_breaks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#ad_breaks GoogleTranscoderJob#ad_breaks}
        '''
        result = self._values.get("ad_breaks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigAdBreaks"]]], result)

    @builtins.property
    def edit_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigEditListStruct"]]]:
        '''edit_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#edit_list GoogleTranscoderJob#edit_list}
        '''
        result = self._values.get("edit_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigEditListStruct"]]], result)

    @builtins.property
    def elementary_streams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigElementaryStreams"]]]:
        '''elementary_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#elementary_streams GoogleTranscoderJob#elementary_streams}
        '''
        result = self._values.get("elementary_streams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigElementaryStreams"]]], result)

    @builtins.property
    def encryptions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigEncryptions"]]]:
        '''encryptions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#encryptions GoogleTranscoderJob#encryptions}
        '''
        result = self._values.get("encryptions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigEncryptions"]]], result)

    @builtins.property
    def inputs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigInputs"]]]:
        '''inputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#inputs GoogleTranscoderJob#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigInputs"]]], result)

    @builtins.property
    def manifests(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigManifests"]]]:
        '''manifests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#manifests GoogleTranscoderJob#manifests}
        '''
        result = self._values.get("manifests")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigManifests"]]], result)

    @builtins.property
    def mux_streams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigMuxStreams"]]]:
        '''mux_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#mux_streams GoogleTranscoderJob#mux_streams}
        '''
        result = self._values.get("mux_streams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigMuxStreams"]]], result)

    @builtins.property
    def output(self) -> typing.Optional["GoogleTranscoderJobConfigOutput"]:
        '''output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#output GoogleTranscoderJob#output}
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigOutput"], result)

    @builtins.property
    def overlays(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigOverlays"]]]:
        '''overlays block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#overlays GoogleTranscoderJob#overlays}
        '''
        result = self._values.get("overlays")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigOverlays"]]], result)

    @builtins.property
    def pubsub_destination(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigPubsubDestination"]:
        '''pubsub_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#pubsub_destination GoogleTranscoderJob#pubsub_destination}
        '''
        result = self._values.get("pubsub_destination")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigPubsubDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56739feae1de6818779d865a695b0dd27058bf50c17e349f78461f9390dc26cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdBreaks")
    def put_ad_breaks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b75575117334e9d5a8c8f2101d87420103e69b6b192a85b6b65dba610b4a68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdBreaks", [value]))

    @jsii.member(jsii_name="putEditList")
    def put_edit_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecce3b72520a3cfe541fbff3b086f4cf7e7dafc6eb8a74201a4d702b924442a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEditList", [value]))

    @jsii.member(jsii_name="putElementaryStreams")
    def put_elementary_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c41f09ca8992dbf090cc608129453771048cb42fed594cb95695a7f4258c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElementaryStreams", [value]))

    @jsii.member(jsii_name="putEncryptions")
    def put_encryptions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f28373cff03c3eb5963c5b275f2237364aa11d8033661b14b178275c35b26ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEncryptions", [value]))

    @jsii.member(jsii_name="putInputs")
    def put_inputs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigInputs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809027ec226e0950cbd7784df758a86e89f856f9c809e016e475e27b455ecf0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputs", [value]))

    @jsii.member(jsii_name="putManifests")
    def put_manifests(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigManifests", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3179993182399150702a04ec516f95275ea56fe9d0154ee6d22c5c02328fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManifests", [value]))

    @jsii.member(jsii_name="putMuxStreams")
    def put_mux_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65e16c38d74848eb5c72bc89af06de8ffe45ff93ed09d3cf67dcc5b08dea414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMuxStreams", [value]))

    @jsii.member(jsii_name="putOutput")
    def put_output(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: URI for the output file(s). For example, gs://my-bucket/outputs/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#uri GoogleTranscoderJob#uri}
        '''
        value = GoogleTranscoderJobConfigOutput(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putOutput", [value]))

    @jsii.member(jsii_name="putOverlays")
    def put_overlays(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigOverlays", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f41e0e64f4155657f922618768e20d5ba04aea4ae39e097eddcb6d51979d323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOverlays", [value]))

    @jsii.member(jsii_name="putPubsubDestination")
    def put_pubsub_destination(
        self,
        *,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic: The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#topic GoogleTranscoderJob#topic}
        '''
        value = GoogleTranscoderJobConfigPubsubDestination(topic=topic)

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
    def ad_breaks(self) -> "GoogleTranscoderJobConfigAdBreaksList":
        return typing.cast("GoogleTranscoderJobConfigAdBreaksList", jsii.get(self, "adBreaks"))

    @builtins.property
    @jsii.member(jsii_name="editList")
    def edit_list(self) -> "GoogleTranscoderJobConfigEditListStructList":
        return typing.cast("GoogleTranscoderJobConfigEditListStructList", jsii.get(self, "editList"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreams")
    def elementary_streams(self) -> "GoogleTranscoderJobConfigElementaryStreamsList":
        return typing.cast("GoogleTranscoderJobConfigElementaryStreamsList", jsii.get(self, "elementaryStreams"))

    @builtins.property
    @jsii.member(jsii_name="encryptions")
    def encryptions(self) -> "GoogleTranscoderJobConfigEncryptionsList":
        return typing.cast("GoogleTranscoderJobConfigEncryptionsList", jsii.get(self, "encryptions"))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> "GoogleTranscoderJobConfigInputsList":
        return typing.cast("GoogleTranscoderJobConfigInputsList", jsii.get(self, "inputs"))

    @builtins.property
    @jsii.member(jsii_name="manifests")
    def manifests(self) -> "GoogleTranscoderJobConfigManifestsList":
        return typing.cast("GoogleTranscoderJobConfigManifestsList", jsii.get(self, "manifests"))

    @builtins.property
    @jsii.member(jsii_name="muxStreams")
    def mux_streams(self) -> "GoogleTranscoderJobConfigMuxStreamsList":
        return typing.cast("GoogleTranscoderJobConfigMuxStreamsList", jsii.get(self, "muxStreams"))

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> "GoogleTranscoderJobConfigOutputOutputReference":
        return typing.cast("GoogleTranscoderJobConfigOutputOutputReference", jsii.get(self, "output"))

    @builtins.property
    @jsii.member(jsii_name="overlays")
    def overlays(self) -> "GoogleTranscoderJobConfigOverlaysList":
        return typing.cast("GoogleTranscoderJobConfigOverlaysList", jsii.get(self, "overlays"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestination")
    def pubsub_destination(
        self,
    ) -> "GoogleTranscoderJobConfigPubsubDestinationOutputReference":
        return typing.cast("GoogleTranscoderJobConfigPubsubDestinationOutputReference", jsii.get(self, "pubsubDestination"))

    @builtins.property
    @jsii.member(jsii_name="adBreaksInput")
    def ad_breaks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigAdBreaks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigAdBreaks"]]], jsii.get(self, "adBreaksInput"))

    @builtins.property
    @jsii.member(jsii_name="editListInput")
    def edit_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigEditListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigEditListStruct"]]], jsii.get(self, "editListInput"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreamsInput")
    def elementary_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigElementaryStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigElementaryStreams"]]], jsii.get(self, "elementaryStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionsInput")
    def encryptions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigEncryptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigEncryptions"]]], jsii.get(self, "encryptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigInputs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigInputs"]]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestsInput")
    def manifests_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigManifests"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigManifests"]]], jsii.get(self, "manifestsInput"))

    @builtins.property
    @jsii.member(jsii_name="muxStreamsInput")
    def mux_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigMuxStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigMuxStreams"]]], jsii.get(self, "muxStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="outputInput")
    def output_input(self) -> typing.Optional["GoogleTranscoderJobConfigOutput"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigOutput"], jsii.get(self, "outputInput"))

    @builtins.property
    @jsii.member(jsii_name="overlaysInput")
    def overlays_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigOverlays"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigOverlays"]]], jsii.get(self, "overlaysInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestinationInput")
    def pubsub_destination_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigPubsubDestination"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigPubsubDestination"], jsii.get(self, "pubsubDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleTranscoderJobConfigA]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3930858682dadfebcbf65daafe11985b7994242e376cc80c4151ae6c1c4a3280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigAdBreaks",
    jsii_struct_bases=[],
    name_mapping={"start_time_offset": "startTimeOffset"},
)
class GoogleTranscoderJobConfigAdBreaks:
    def __init__(
        self,
        *,
        start_time_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_time_offset: Start time in seconds for the ad break, relative to the output file timeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#start_time_offset GoogleTranscoderJob#start_time_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a58eec09e9e8fa02d3958e95e8f87d5cab6587a4bd00465edfd246ef4c7c48c)
            check_type(argname="argument start_time_offset", value=start_time_offset, expected_type=type_hints["start_time_offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if start_time_offset is not None:
            self._values["start_time_offset"] = start_time_offset

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''Start time in seconds for the ad break, relative to the output file timeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#start_time_offset GoogleTranscoderJob#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigAdBreaks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigAdBreaksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigAdBreaksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__257e09ce6795eb76fe64e312e57c12299deaf1c019f4c032ba4c236a95f108ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigAdBreaksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64f2e81d1c7d92c5796beac9d68ba2f409753143b3130635d108c23ecd07d64)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigAdBreaksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd725e8af2fc2ec7c0e10c20a3e7c5acde682265ae25f32769b50f5fc2dd3495)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e22f78cad728161d1b6e6f808a4b0de324dd3c40b2d5b8ef81b01287958e6dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5547a8d4eba4b0254f2addc761c3d8faa1a63550d314abc64367c218ff00c3a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigAdBreaks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigAdBreaks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigAdBreaks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ac8773312b66205806d360c2a9509889fc9733d2862f981d3beefa5d1f319d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigAdBreaksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigAdBreaksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__000704ce560d3275b926d4add962903869a7a91ba0dcea2d599b995ae31b9b94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24e08247b492f03f04cdd0ff974fd47dad23f178d08d66b65f90f7fa9c76ecd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigAdBreaks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigAdBreaks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigAdBreaks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e197f7405a024c652751d2a199506e643ed4b1aabdde0fcdf5db67c8b24b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEditListStruct",
    jsii_struct_bases=[],
    name_mapping={
        "inputs": "inputs",
        "key": "key",
        "start_time_offset": "startTimeOffset",
    },
)
class GoogleTranscoderJobConfigEditListStruct:
    def __init__(
        self,
        *,
        inputs: typing.Optional[typing.Sequence[builtins.str]] = None,
        key: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inputs: List of values identifying files that should be used in this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#inputs GoogleTranscoderJob#inputs}
        :param key: A unique key for this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#key GoogleTranscoderJob#key}
        :param start_time_offset: Start time in seconds for the atom, relative to the input file timeline. The default is '0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#start_time_offset GoogleTranscoderJob#start_time_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac72f93d9d24b522eb9a71a7c54eec3b0de062377037d10bb86fa5e5c7212f80)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#inputs GoogleTranscoderJob#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#key GoogleTranscoderJob#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''Start time in seconds for the atom, relative to the input file timeline. The default is '0s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#start_time_offset GoogleTranscoderJob#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEditListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEditListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEditListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e063adfbf9a821057caa62591301adcbd6375787da5af4944fad47eb792aa1fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigEditListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a1530863883e6228f4c9e15ced16fadbc83c7164d4cd436e6d1e7b244a0a1f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigEditListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e517d226036b5b940b7df7830115caa925e91051b34af5c41b0837d994341e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__356da80303512b4be48855f6bc1c285a790c85b0fdf302f36cf713e8ecfc6c8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57704673ca81949c54d8b64eef876a91c28fde3f6195c6786171b120c039e55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigEditListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigEditListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigEditListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f461e0766bbf90662dd6233ffeaed0e72e77728b02cf7aa7c1810cbc54263f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigEditListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEditListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7afe8cd14219aadc709a5f437ac1cf6cccfe3fc7435848faa10f802142951471)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6b56fc927331ae5620b9af28748d671b12fb80402efca0154cabf70d3a3164f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0482f40ef07b34388b2083c73fae1fad172cbf6368fb7bd81c4f39b7335c613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7dba5ccbca86416341b0d62350524e389d326cb22aa897ef6c401bc5b3eebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigEditListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigEditListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigEditListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e958e1403cf3b7b100913f326b32c1aa751f12614a2f9c8cb2a3ad07c3bdf87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreams",
    jsii_struct_bases=[],
    name_mapping={
        "audio_stream": "audioStream",
        "key": "key",
        "video_stream": "videoStream",
    },
)
class GoogleTranscoderJobConfigElementaryStreams:
    def __init__(
        self,
        *,
        audio_stream: typing.Optional[typing.Union["GoogleTranscoderJobConfigElementaryStreamsAudioStream", typing.Dict[builtins.str, typing.Any]]] = None,
        key: typing.Optional[builtins.str] = None,
        video_stream: typing.Optional[typing.Union["GoogleTranscoderJobConfigElementaryStreamsVideoStream", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_stream: audio_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#audio_stream GoogleTranscoderJob#audio_stream}
        :param key: A unique key for this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#key GoogleTranscoderJob#key}
        :param video_stream: video_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#video_stream GoogleTranscoderJob#video_stream}
        '''
        if isinstance(audio_stream, dict):
            audio_stream = GoogleTranscoderJobConfigElementaryStreamsAudioStream(**audio_stream)
        if isinstance(video_stream, dict):
            video_stream = GoogleTranscoderJobConfigElementaryStreamsVideoStream(**video_stream)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a43ddeeccd8d320f42be20926bef9d15e672f4c3ab3397c6f07dcf482240a4f)
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
    ) -> typing.Optional["GoogleTranscoderJobConfigElementaryStreamsAudioStream"]:
        '''audio_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#audio_stream GoogleTranscoderJob#audio_stream}
        '''
        result = self._values.get("audio_stream")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigElementaryStreamsAudioStream"], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#key GoogleTranscoderJob#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def video_stream(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStream"]:
        '''video_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#video_stream GoogleTranscoderJob#video_stream}
        '''
        result = self._values.get("video_stream")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStream"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigElementaryStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsAudioStream",
    jsii_struct_bases=[],
    name_mapping={
        "bitrate_bps": "bitrateBps",
        "channel_count": "channelCount",
        "channel_layout": "channelLayout",
        "codec": "codec",
        "sample_rate_hertz": "sampleRateHertz",
    },
)
class GoogleTranscoderJobConfigElementaryStreamsAudioStream:
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
        :param bitrate_bps: Audio bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#bitrate_bps GoogleTranscoderJob#bitrate_bps}
        :param channel_count: Number of audio channels. The default is '2'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#channel_count GoogleTranscoderJob#channel_count}
        :param channel_layout: A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#channel_layout GoogleTranscoderJob#channel_layout}
        :param codec: The codec for this audio stream. The default is 'aac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#codec GoogleTranscoderJob#codec}
        :param sample_rate_hertz: The audio sample rate in Hertz. The default is '48000'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#sample_rate_hertz GoogleTranscoderJob#sample_rate_hertz}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abeb3a823bfb14c35ebe5619d0b40f08afc2bdb80aeff7908155789a26da9e31)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#bitrate_bps GoogleTranscoderJob#bitrate_bps}
        '''
        result = self._values.get("bitrate_bps")
        assert result is not None, "Required property 'bitrate_bps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def channel_count(self) -> typing.Optional[jsii.Number]:
        '''Number of audio channels. The default is '2'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#channel_count GoogleTranscoderJob#channel_count}
        '''
        result = self._values.get("channel_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def channel_layout(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#channel_layout GoogleTranscoderJob#channel_layout}
        '''
        result = self._values.get("channel_layout")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def codec(self) -> typing.Optional[builtins.str]:
        '''The codec for this audio stream. The default is 'aac'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#codec GoogleTranscoderJob#codec}
        '''
        result = self._values.get("codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate_hertz(self) -> typing.Optional[jsii.Number]:
        '''The audio sample rate in Hertz. The default is '48000'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#sample_rate_hertz GoogleTranscoderJob#sample_rate_hertz}
        '''
        result = self._values.get("sample_rate_hertz")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigElementaryStreamsAudioStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigElementaryStreamsAudioStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsAudioStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eca12899e49a03a5c914313a745df05b23511c30fadd5f0f537886a8824ad6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3de85136c16d00170c38217da3062d4213fec2df3dab61d464d7b8e647ce3015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitrateBps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelCount")
    def channel_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "channelCount"))

    @channel_count.setter
    def channel_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52a224bdd56498474f1b9051303c731a428494a1d39ef510e4f2c0efa98ec97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelLayout")
    def channel_layout(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "channelLayout"))

    @channel_layout.setter
    def channel_layout(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550f5bbb3ff0e7709274aa2bdac21f4b22ebc6128aa538b7adb35a7f0174899c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelLayout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codec")
    def codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codec"))

    @codec.setter
    def codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6191455489d0093116d7c4e59bc13ed005854664a90fced960bb400751e209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRateHertz")
    def sample_rate_hertz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRateHertz"))

    @sample_rate_hertz.setter
    def sample_rate_hertz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43a997a87993256043f5dacafb04d00ceb356bb85f025747ad0a0a3de3ed8a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRateHertz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigElementaryStreamsAudioStream]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigElementaryStreamsAudioStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsAudioStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0aa1596979b9622bf0e9250d7ea035011c451ddd66c2bf330d5ebab94644df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigElementaryStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79a8b593b79f7f9b9670fe5c24f67535afcc5b219fb78be21f1acc7f965ec5a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigElementaryStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d31dfda6909d8a3522aa267257f5e18015b5ce48bb03cdf535da3824a217dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigElementaryStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d65d0419e95fe0b091c69a660ba51e1eb51dad87a6c278636f2e107dff0777e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9888eee42ac836b2421e815df3aa4623f3cc18eebb2049f4c7870c8968138c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a39b13c36f157630b4a4366f0169269daf254059d4892866e4181230febc2a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigElementaryStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigElementaryStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigElementaryStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82331e791fd341b17833220d9dcd26b372e495d36f7e6a71d445159fd3b011c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigElementaryStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__754fd465c70a966046bdbc99e42e68c84823129bc66964ba9cb0b753cada0b4d)
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
        :param bitrate_bps: Audio bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#bitrate_bps GoogleTranscoderJob#bitrate_bps}
        :param channel_count: Number of audio channels. The default is '2'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#channel_count GoogleTranscoderJob#channel_count}
        :param channel_layout: A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#channel_layout GoogleTranscoderJob#channel_layout}
        :param codec: The codec for this audio stream. The default is 'aac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#codec GoogleTranscoderJob#codec}
        :param sample_rate_hertz: The audio sample rate in Hertz. The default is '48000'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#sample_rate_hertz GoogleTranscoderJob#sample_rate_hertz}
        '''
        value = GoogleTranscoderJobConfigElementaryStreamsAudioStream(
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
        h264: typing.Optional[typing.Union["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param h264: h264 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#h264 GoogleTranscoderJob#h264}
        '''
        value = GoogleTranscoderJobConfigElementaryStreamsVideoStream(h264=h264)

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
    ) -> GoogleTranscoderJobConfigElementaryStreamsAudioStreamOutputReference:
        return typing.cast(GoogleTranscoderJobConfigElementaryStreamsAudioStreamOutputReference, jsii.get(self, "audioStream"))

    @builtins.property
    @jsii.member(jsii_name="videoStream")
    def video_stream(
        self,
    ) -> "GoogleTranscoderJobConfigElementaryStreamsVideoStreamOutputReference":
        return typing.cast("GoogleTranscoderJobConfigElementaryStreamsVideoStreamOutputReference", jsii.get(self, "videoStream"))

    @builtins.property
    @jsii.member(jsii_name="audioStreamInput")
    def audio_stream_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigElementaryStreamsAudioStream]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigElementaryStreamsAudioStream], jsii.get(self, "audioStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="videoStreamInput")
    def video_stream_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStream"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStream"], jsii.get(self, "videoStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12532e65f8983d4bd138301410486cfa20c1952053dc588897f768ad1d564b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigElementaryStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigElementaryStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigElementaryStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb2d04df35a3e0e02871ac67af6b2ecc0cc67f5868d49b398bc231166f60191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsVideoStream",
    jsii_struct_bases=[],
    name_mapping={"h264": "h264"},
)
class GoogleTranscoderJobConfigElementaryStreamsVideoStream:
    def __init__(
        self,
        *,
        h264: typing.Optional[typing.Union["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param h264: h264 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#h264 GoogleTranscoderJob#h264}
        '''
        if isinstance(h264, dict):
            h264 = GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264(**h264)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1815644e61fc07b3a0568c2e3d20df22ef479880591273176fcd7068e738e5f)
            check_type(argname="argument h264", value=h264, expected_type=type_hints["h264"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if h264 is not None:
            self._values["h264"] = h264

    @builtins.property
    def h264(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264"]:
        '''h264 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#h264 GoogleTranscoderJob#h264}
        '''
        result = self._values.get("h264")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigElementaryStreamsVideoStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264",
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
class GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264:
    def __init__(
        self,
        *,
        bitrate_bps: jsii.Number,
        frame_rate: jsii.Number,
        crf_level: typing.Optional[jsii.Number] = None,
        entropy_coder: typing.Optional[builtins.str] = None,
        gop_duration: typing.Optional[builtins.str] = None,
        height_pixels: typing.Optional[jsii.Number] = None,
        hlg: typing.Optional[typing.Union["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg", typing.Dict[builtins.str, typing.Any]]] = None,
        pixel_format: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        rate_control_mode: typing.Optional[builtins.str] = None,
        sdr: typing.Optional[typing.Union["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr", typing.Dict[builtins.str, typing.Any]]] = None,
        vbv_fullness_bits: typing.Optional[jsii.Number] = None,
        vbv_size_bits: typing.Optional[jsii.Number] = None,
        width_pixels: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: The video bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#bitrate_bps GoogleTranscoderJob#bitrate_bps}
        :param frame_rate: The target video frame rate in frames per second (FPS). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#frame_rate GoogleTranscoderJob#frame_rate}
        :param crf_level: Target CRF level. The default is '21'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#crf_level GoogleTranscoderJob#crf_level}
        :param entropy_coder: The entropy coder to use. The default is 'cabac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#entropy_coder GoogleTranscoderJob#entropy_coder}
        :param gop_duration: Select the GOP size based on the specified duration. The default is '3s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#gop_duration GoogleTranscoderJob#gop_duration}
        :param height_pixels: The height of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#height_pixels GoogleTranscoderJob#height_pixels}
        :param hlg: hlg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#hlg GoogleTranscoderJob#hlg}
        :param pixel_format: Pixel format to use. The default is 'yuv420p'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#pixel_format GoogleTranscoderJob#pixel_format}
        :param preset: Enforces the specified codec preset. The default is 'veryfast'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#preset GoogleTranscoderJob#preset}
        :param profile: Enforces the specified codec profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#profile GoogleTranscoderJob#profile}
        :param rate_control_mode: Specify the mode. The default is 'vbr'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#rate_control_mode GoogleTranscoderJob#rate_control_mode}
        :param sdr: sdr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#sdr GoogleTranscoderJob#sdr}
        :param vbv_fullness_bits: Initial fullness of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#vbv_fullness_bits GoogleTranscoderJob#vbv_fullness_bits}
        :param vbv_size_bits: Size of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#vbv_size_bits GoogleTranscoderJob#vbv_size_bits}
        :param width_pixels: The width of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#width_pixels GoogleTranscoderJob#width_pixels}
        '''
        if isinstance(hlg, dict):
            hlg = GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg(**hlg)
        if isinstance(sdr, dict):
            sdr = GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr(**sdr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803133149abc0b67aa294c85044e7b1af409850b1dac06bf9916910825284a67)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#bitrate_bps GoogleTranscoderJob#bitrate_bps}
        '''
        result = self._values.get("bitrate_bps")
        assert result is not None, "Required property 'bitrate_bps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frame_rate(self) -> jsii.Number:
        '''The target video frame rate in frames per second (FPS).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#frame_rate GoogleTranscoderJob#frame_rate}
        '''
        result = self._values.get("frame_rate")
        assert result is not None, "Required property 'frame_rate' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def crf_level(self) -> typing.Optional[jsii.Number]:
        '''Target CRF level. The default is '21'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#crf_level GoogleTranscoderJob#crf_level}
        '''
        result = self._values.get("crf_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def entropy_coder(self) -> typing.Optional[builtins.str]:
        '''The entropy coder to use. The default is 'cabac'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#entropy_coder GoogleTranscoderJob#entropy_coder}
        '''
        result = self._values.get("entropy_coder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gop_duration(self) -> typing.Optional[builtins.str]:
        '''Select the GOP size based on the specified duration. The default is '3s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#gop_duration GoogleTranscoderJob#gop_duration}
        '''
        result = self._values.get("gop_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def height_pixels(self) -> typing.Optional[jsii.Number]:
        '''The height of the video in pixels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#height_pixels GoogleTranscoderJob#height_pixels}
        '''
        result = self._values.get("height_pixels")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hlg(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg"]:
        '''hlg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#hlg GoogleTranscoderJob#hlg}
        '''
        result = self._values.get("hlg")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg"], result)

    @builtins.property
    def pixel_format(self) -> typing.Optional[builtins.str]:
        '''Pixel format to use. The default is 'yuv420p'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#pixel_format GoogleTranscoderJob#pixel_format}
        '''
        result = self._values.get("pixel_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preset(self) -> typing.Optional[builtins.str]:
        '''Enforces the specified codec preset. The default is 'veryfast'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#preset GoogleTranscoderJob#preset}
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Enforces the specified codec profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#profile GoogleTranscoderJob#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_control_mode(self) -> typing.Optional[builtins.str]:
        '''Specify the mode. The default is 'vbr'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#rate_control_mode GoogleTranscoderJob#rate_control_mode}
        '''
        result = self._values.get("rate_control_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sdr(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr"]:
        '''sdr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#sdr GoogleTranscoderJob#sdr}
        '''
        result = self._values.get("sdr")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr"], result)

    @builtins.property
    def vbv_fullness_bits(self) -> typing.Optional[jsii.Number]:
        '''Initial fullness of the Video Buffering Verifier (VBV) buffer in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#vbv_fullness_bits GoogleTranscoderJob#vbv_fullness_bits}
        '''
        result = self._values.get("vbv_fullness_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vbv_size_bits(self) -> typing.Optional[jsii.Number]:
        '''Size of the Video Buffering Verifier (VBV) buffer in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#vbv_size_bits GoogleTranscoderJob#vbv_size_bits}
        '''
        result = self._values.get("vbv_size_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def width_pixels(self) -> typing.Optional[jsii.Number]:
        '''The width of the video in pixels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#width_pixels GoogleTranscoderJob#width_pixels}
        '''
        result = self._values.get("width_pixels")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e4f3316faf1b03143a69ba84097a0ec54c3623fc8400ee472e399656f44384)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9dbf67ffbeabd61ae7cd2ab49cb1196641649223dd21bf4f3d1b4b5efd09a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3974bbc02315cec13ff0e35692c958d0bab145de4366b286994c2a14b80edc4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHlg")
    def put_hlg(self) -> None:
        value = GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg()

        return typing.cast(None, jsii.invoke(self, "putHlg", [value]))

    @jsii.member(jsii_name="putSdr")
    def put_sdr(self) -> None:
        value = GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr()

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
    ) -> GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference:
        return typing.cast(GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference, jsii.get(self, "hlg"))

    @builtins.property
    @jsii.member(jsii_name="sdr")
    def sdr(
        self,
    ) -> "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference":
        return typing.cast("GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference", jsii.get(self, "sdr"))

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
    ) -> typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg], jsii.get(self, "hlgInput"))

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
    ) -> typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr"], jsii.get(self, "sdrInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__951248351f379eca0e1f4ae0682d9ef16ae3597aa1384530ff7b5ef7c0b4c199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitrateBps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crfLevel")
    def crf_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "crfLevel"))

    @crf_level.setter
    def crf_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb68296d73a61de098af05c9cb1a7a40abea33f92c4de5a0afeba3a48427dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crfLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entropyCoder")
    def entropy_coder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entropyCoder"))

    @entropy_coder.setter
    def entropy_coder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2f09e807469b930bc95f94557081abd1b1f799e4f1a92994bee0b985638cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entropyCoder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frameRate")
    def frame_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frameRate"))

    @frame_rate.setter
    def frame_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1665becdeac566a4ca2a7a84f95771f47773381341022426c984c9d2101bb0b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gopDuration")
    def gop_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gopDuration"))

    @gop_duration.setter
    def gop_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f24502871eff3cd07131c53e3eed5c1f7b6250008afa5253608e662e4ea8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gopDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="heightPixels")
    def height_pixels(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "heightPixels"))

    @height_pixels.setter
    def height_pixels(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1003c4b262078cd77354a38df9fc9751cbdd8c0fdfe8d988b2ff65560a4f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "heightPixels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pixelFormat")
    def pixel_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pixelFormat"))

    @pixel_format.setter
    def pixel_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82faa7a134cfae24a27faf397ae515286b646851efa9e7591930dca8a6a5bbe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pixelFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preset")
    def preset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preset"))

    @preset.setter
    def preset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd3f09802e1db0c8e902d8115223c29e644f5f46d6df08ffe5029bd6406e207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87361d8d257f66d67aef82f28d600043a8614b1b3be823d83004aabd63fff1cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rateControlMode")
    def rate_control_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rateControlMode"))

    @rate_control_mode.setter
    def rate_control_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32adeecabc01795a957dae4c8e4d65c627ed2dd0561fb1b5cbc12d8b3766a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateControlMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vbvFullnessBits")
    def vbv_fullness_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vbvFullnessBits"))

    @vbv_fullness_bits.setter
    def vbv_fullness_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f3f3a25c67ebf75f4f1baccca5d09ab0e6cf5ee68dce094dd891ea07e7f231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vbvFullnessBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vbvSizeBits")
    def vbv_size_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vbvSizeBits"))

    @vbv_size_bits.setter
    def vbv_size_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c28db74d9223ee0aa7637301f79d111e1d53ed0c4785deb935104219e3e6dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vbvSizeBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="widthPixels")
    def width_pixels(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "widthPixels"))

    @width_pixels.setter
    def width_pixels(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72cb002e5c48ae1fda4731744934db37624102fe3d1fb963230ac10701123da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "widthPixels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813ef98322b79f2e49219aba10ba34b5d30f8a535c5c88990122a04a558552fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ee60a65803d474ee7eeb4acf123774546b3d58d3b62dbb2fcdc5b017eeb5df1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021aa2436e74c034e189dfc2f5896d51d80aadf2f6add38fe5e85e5aa55d74e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigElementaryStreamsVideoStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigElementaryStreamsVideoStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4503fa5c9e015d9e716b88ae7ed584ae26e6a533a1bcde4fdfaaa8403b2bb611)
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
        hlg: typing.Optional[typing.Union[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg, typing.Dict[builtins.str, typing.Any]]] = None,
        pixel_format: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        rate_control_mode: typing.Optional[builtins.str] = None,
        sdr: typing.Optional[typing.Union[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr, typing.Dict[builtins.str, typing.Any]]] = None,
        vbv_fullness_bits: typing.Optional[jsii.Number] = None,
        vbv_size_bits: typing.Optional[jsii.Number] = None,
        width_pixels: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: The video bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#bitrate_bps GoogleTranscoderJob#bitrate_bps}
        :param frame_rate: The target video frame rate in frames per second (FPS). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#frame_rate GoogleTranscoderJob#frame_rate}
        :param crf_level: Target CRF level. The default is '21'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#crf_level GoogleTranscoderJob#crf_level}
        :param entropy_coder: The entropy coder to use. The default is 'cabac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#entropy_coder GoogleTranscoderJob#entropy_coder}
        :param gop_duration: Select the GOP size based on the specified duration. The default is '3s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#gop_duration GoogleTranscoderJob#gop_duration}
        :param height_pixels: The height of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#height_pixels GoogleTranscoderJob#height_pixels}
        :param hlg: hlg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#hlg GoogleTranscoderJob#hlg}
        :param pixel_format: Pixel format to use. The default is 'yuv420p'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#pixel_format GoogleTranscoderJob#pixel_format}
        :param preset: Enforces the specified codec preset. The default is 'veryfast'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#preset GoogleTranscoderJob#preset}
        :param profile: Enforces the specified codec profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#profile GoogleTranscoderJob#profile}
        :param rate_control_mode: Specify the mode. The default is 'vbr'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#rate_control_mode GoogleTranscoderJob#rate_control_mode}
        :param sdr: sdr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#sdr GoogleTranscoderJob#sdr}
        :param vbv_fullness_bits: Initial fullness of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#vbv_fullness_bits GoogleTranscoderJob#vbv_fullness_bits}
        :param vbv_size_bits: Size of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#vbv_size_bits GoogleTranscoderJob#vbv_size_bits}
        :param width_pixels: The width of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#width_pixels GoogleTranscoderJob#width_pixels}
        '''
        value = GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264(
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
    ) -> GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference:
        return typing.cast(GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference, jsii.get(self, "h264"))

    @builtins.property
    @jsii.member(jsii_name="h264Input")
    def h264_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264], jsii.get(self, "h264Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStream]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182aa1561065fd70b99615791d9b5d967ec70e76de7e5f9943de4dcfa3c042f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptions",
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
class GoogleTranscoderJobConfigEncryptions:
    def __init__(
        self,
        *,
        id: builtins.str,
        aes128: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsAes128", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_systems: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsDrmSystems", typing.Dict[builtins.str, typing.Any]]] = None,
        mpeg_cenc: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsMpegCenc", typing.Dict[builtins.str, typing.Any]]] = None,
        sample_aes: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsSampleAes", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_manager_key_source: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Identifier for this set of encryption options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#id GoogleTranscoderJob#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param aes128: aes128 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#aes128 GoogleTranscoderJob#aes128}
        :param drm_systems: drm_systems block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#drm_systems GoogleTranscoderJob#drm_systems}
        :param mpeg_cenc: mpeg_cenc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#mpeg_cenc GoogleTranscoderJob#mpeg_cenc}
        :param sample_aes: sample_aes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#sample_aes GoogleTranscoderJob#sample_aes}
        :param secret_manager_key_source: secret_manager_key_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#secret_manager_key_source GoogleTranscoderJob#secret_manager_key_source}
        '''
        if isinstance(aes128, dict):
            aes128 = GoogleTranscoderJobConfigEncryptionsAes128(**aes128)
        if isinstance(drm_systems, dict):
            drm_systems = GoogleTranscoderJobConfigEncryptionsDrmSystems(**drm_systems)
        if isinstance(mpeg_cenc, dict):
            mpeg_cenc = GoogleTranscoderJobConfigEncryptionsMpegCenc(**mpeg_cenc)
        if isinstance(sample_aes, dict):
            sample_aes = GoogleTranscoderJobConfigEncryptionsSampleAes(**sample_aes)
        if isinstance(secret_manager_key_source, dict):
            secret_manager_key_source = GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource(**secret_manager_key_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f3d79db212ca06bfe501b93036db605ed3400a6cd00b76a165dcb0b29b2cdc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#id GoogleTranscoderJob#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aes128(self) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsAes128"]:
        '''aes128 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#aes128 GoogleTranscoderJob#aes128}
        '''
        result = self._values.get("aes128")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsAes128"], result)

    @builtins.property
    def drm_systems(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystems"]:
        '''drm_systems block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#drm_systems GoogleTranscoderJob#drm_systems}
        '''
        result = self._values.get("drm_systems")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystems"], result)

    @builtins.property
    def mpeg_cenc(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsMpegCenc"]:
        '''mpeg_cenc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#mpeg_cenc GoogleTranscoderJob#mpeg_cenc}
        '''
        result = self._values.get("mpeg_cenc")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsMpegCenc"], result)

    @builtins.property
    def sample_aes(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsSampleAes"]:
        '''sample_aes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#sample_aes GoogleTranscoderJob#sample_aes}
        '''
        result = self._values.get("sample_aes")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsSampleAes"], result)

    @builtins.property
    def secret_manager_key_source(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource"]:
        '''secret_manager_key_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#secret_manager_key_source GoogleTranscoderJob#secret_manager_key_source}
        '''
        result = self._values.get("secret_manager_key_source")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsAes128",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobConfigEncryptionsAes128:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsAes128(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEncryptionsAes128OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsAes128OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ad13e0feb41356df777c8959871085b908a7b0c9a96cf02fe193b9c110ad313)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsAes128]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsAes128], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsAes128],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f816508e1a94c92992a30e3b7baf1ad0182c50cd1b7ad812c7b8f0a093bd5b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystems",
    jsii_struct_bases=[],
    name_mapping={
        "clearkey": "clearkey",
        "fairplay": "fairplay",
        "playready": "playready",
        "widevine": "widevine",
    },
)
class GoogleTranscoderJobConfigEncryptionsDrmSystems:
    def __init__(
        self,
        *,
        clearkey: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey", typing.Dict[builtins.str, typing.Any]]] = None,
        fairplay: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay", typing.Dict[builtins.str, typing.Any]]] = None,
        playready: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready", typing.Dict[builtins.str, typing.Any]]] = None,
        widevine: typing.Optional[typing.Union["GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clearkey: clearkey block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#clearkey GoogleTranscoderJob#clearkey}
        :param fairplay: fairplay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#fairplay GoogleTranscoderJob#fairplay}
        :param playready: playready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#playready GoogleTranscoderJob#playready}
        :param widevine: widevine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#widevine GoogleTranscoderJob#widevine}
        '''
        if isinstance(clearkey, dict):
            clearkey = GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey(**clearkey)
        if isinstance(fairplay, dict):
            fairplay = GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay(**fairplay)
        if isinstance(playready, dict):
            playready = GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready(**playready)
        if isinstance(widevine, dict):
            widevine = GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine(**widevine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf9bc988aff1404abc2b55b205f421d5ddc2b224cdb5b894ab4a395c0f1e274)
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
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey"]:
        '''clearkey block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#clearkey GoogleTranscoderJob#clearkey}
        '''
        result = self._values.get("clearkey")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey"], result)

    @builtins.property
    def fairplay(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay"]:
        '''fairplay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#fairplay GoogleTranscoderJob#fairplay}
        '''
        result = self._values.get("fairplay")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay"], result)

    @builtins.property
    def playready(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready"]:
        '''playready block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#playready GoogleTranscoderJob#playready}
        '''
        result = self._values.get("playready")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready"], result)

    @builtins.property
    def widevine(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine"]:
        '''widevine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#widevine GoogleTranscoderJob#widevine}
        '''
        result = self._values.get("widevine")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsDrmSystems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b557e923d601bf1cafe924ccbaec36766f6a342332f447d7abbd8e4c17654c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f99cb76d8c68e46c462ef26555128240bea52817ad832a1a4d4fb52f33f0f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33ac55f4464d6ad10135524324e890812abebd703778b4c385957da51badd036)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc41bfaf62ea432e690b6502c7abbee357894200dc5ef664beeabe878d3c6174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigEncryptionsDrmSystemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__351cd16d747dc5edea72adee24b40713af7ec9e4d9c16e0fa12a0147f09e8f68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClearkey")
    def put_clearkey(self) -> None:
        value = GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey()

        return typing.cast(None, jsii.invoke(self, "putClearkey", [value]))

    @jsii.member(jsii_name="putFairplay")
    def put_fairplay(self) -> None:
        value = GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay()

        return typing.cast(None, jsii.invoke(self, "putFairplay", [value]))

    @jsii.member(jsii_name="putPlayready")
    def put_playready(self) -> None:
        value = GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready()

        return typing.cast(None, jsii.invoke(self, "putPlayready", [value]))

    @jsii.member(jsii_name="putWidevine")
    def put_widevine(self) -> None:
        value = GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine()

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
    ) -> GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference:
        return typing.cast(GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference, jsii.get(self, "clearkey"))

    @builtins.property
    @jsii.member(jsii_name="fairplay")
    def fairplay(
        self,
    ) -> GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference:
        return typing.cast(GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference, jsii.get(self, "fairplay"))

    @builtins.property
    @jsii.member(jsii_name="playready")
    def playready(
        self,
    ) -> "GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference":
        return typing.cast("GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference", jsii.get(self, "playready"))

    @builtins.property
    @jsii.member(jsii_name="widevine")
    def widevine(
        self,
    ) -> "GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference":
        return typing.cast("GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference", jsii.get(self, "widevine"))

    @builtins.property
    @jsii.member(jsii_name="clearkeyInput")
    def clearkey_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey], jsii.get(self, "clearkeyInput"))

    @builtins.property
    @jsii.member(jsii_name="fairplayInput")
    def fairplay_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay], jsii.get(self, "fairplayInput"))

    @builtins.property
    @jsii.member(jsii_name="playreadyInput")
    def playready_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready"], jsii.get(self, "playreadyInput"))

    @builtins.property
    @jsii.member(jsii_name="widevineInput")
    def widevine_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine"], jsii.get(self, "widevineInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystems]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystems], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystems],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4807e4e539866f01bc170b10803fe24c4293ad11239ed36f0b30b9dfd269ba3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7fc7a10a562bf8da43b5c546c653943168a20574a0431c284ac5e47fedfd58f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937d5a31058e6fb5c82df86071c6fe3be71b6c3d0b96cacc9af7626975bfbef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bac5fd943f008aa8a137338bdf7167d6025dff6f381d043d4e519006b33f6f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f57e813ecc8707d6fe0707e03335ec02bd64132eac4f85cd3c1b30fe9e1e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigEncryptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5b9db45c01229c29d9479a37048ffda701de95d8a224f939a15311b4227ed0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigEncryptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d27066a78edbd57999357c0c76083472dee99db08a9d1244c3eb3243567cefd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigEncryptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389dd13f3dd02f25ede4011131c73a39a047db592113a91c8f5d6b194e12c98d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2029807b45baab299eb626ae11cef1848870cd3e23cdd84daf7c28be55db60dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ecb8d4d8f2c4fe78745664e1f61a5ffa0ca949a6b76724b86ad61d508c27d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigEncryptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigEncryptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigEncryptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405446bc85ad14c8d073076451d1148c5f2e33241217f1f8e8e646b3fe5f88ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsMpegCenc",
    jsii_struct_bases=[],
    name_mapping={"scheme": "scheme"},
)
class GoogleTranscoderJobConfigEncryptionsMpegCenc:
    def __init__(self, *, scheme: builtins.str) -> None:
        '''
        :param scheme: Specify the encryption scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#scheme GoogleTranscoderJob#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27f4da4a478b181650ff375a2cc92bcd3cbb0e8c008fd2606233a40b6ba0b9f)
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scheme": scheme,
        }

    @builtins.property
    def scheme(self) -> builtins.str:
        '''Specify the encryption scheme.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#scheme GoogleTranscoderJob#scheme}
        '''
        result = self._values.get("scheme")
        assert result is not None, "Required property 'scheme' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsMpegCenc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEncryptionsMpegCencOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsMpegCencOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef28a1d3795c861f68cbd0654d20f808a46dc9eb10630539b3e5c6adf63331d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2dacf78de62efe18ddb2381e7c6054c7815880135374bc03cee7b3c607de174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsMpegCenc]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsMpegCenc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsMpegCenc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df3acfbf02f4abf2f56ba1a19d19fa41d1b16881d21da8eb205007c8cfaf4ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigEncryptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6ea0e4e794ae93d4a162893115c60d8a80f154346bfc3b062746f3434f235ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAes128")
    def put_aes128(self) -> None:
        value = GoogleTranscoderJobConfigEncryptionsAes128()

        return typing.cast(None, jsii.invoke(self, "putAes128", [value]))

    @jsii.member(jsii_name="putDrmSystems")
    def put_drm_systems(
        self,
        *,
        clearkey: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey, typing.Dict[builtins.str, typing.Any]]] = None,
        fairplay: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
        playready: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
        widevine: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clearkey: clearkey block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#clearkey GoogleTranscoderJob#clearkey}
        :param fairplay: fairplay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#fairplay GoogleTranscoderJob#fairplay}
        :param playready: playready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#playready GoogleTranscoderJob#playready}
        :param widevine: widevine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#widevine GoogleTranscoderJob#widevine}
        '''
        value = GoogleTranscoderJobConfigEncryptionsDrmSystems(
            clearkey=clearkey,
            fairplay=fairplay,
            playready=playready,
            widevine=widevine,
        )

        return typing.cast(None, jsii.invoke(self, "putDrmSystems", [value]))

    @jsii.member(jsii_name="putMpegCenc")
    def put_mpeg_cenc(self, *, scheme: builtins.str) -> None:
        '''
        :param scheme: Specify the encryption scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#scheme GoogleTranscoderJob#scheme}
        '''
        value = GoogleTranscoderJobConfigEncryptionsMpegCenc(scheme=scheme)

        return typing.cast(None, jsii.invoke(self, "putMpegCenc", [value]))

    @jsii.member(jsii_name="putSampleAes")
    def put_sample_aes(self) -> None:
        value = GoogleTranscoderJobConfigEncryptionsSampleAes()

        return typing.cast(None, jsii.invoke(self, "putSampleAes", [value]))

    @jsii.member(jsii_name="putSecretManagerKeySource")
    def put_secret_manager_key_source(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#secret_version GoogleTranscoderJob#secret_version}
        '''
        value = GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource(
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
    def aes128(self) -> GoogleTranscoderJobConfigEncryptionsAes128OutputReference:
        return typing.cast(GoogleTranscoderJobConfigEncryptionsAes128OutputReference, jsii.get(self, "aes128"))

    @builtins.property
    @jsii.member(jsii_name="drmSystems")
    def drm_systems(
        self,
    ) -> GoogleTranscoderJobConfigEncryptionsDrmSystemsOutputReference:
        return typing.cast(GoogleTranscoderJobConfigEncryptionsDrmSystemsOutputReference, jsii.get(self, "drmSystems"))

    @builtins.property
    @jsii.member(jsii_name="mpegCenc")
    def mpeg_cenc(self) -> GoogleTranscoderJobConfigEncryptionsMpegCencOutputReference:
        return typing.cast(GoogleTranscoderJobConfigEncryptionsMpegCencOutputReference, jsii.get(self, "mpegCenc"))

    @builtins.property
    @jsii.member(jsii_name="sampleAes")
    def sample_aes(
        self,
    ) -> "GoogleTranscoderJobConfigEncryptionsSampleAesOutputReference":
        return typing.cast("GoogleTranscoderJobConfigEncryptionsSampleAesOutputReference", jsii.get(self, "sampleAes"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerKeySource")
    def secret_manager_key_source(
        self,
    ) -> "GoogleTranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference":
        return typing.cast("GoogleTranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference", jsii.get(self, "secretManagerKeySource"))

    @builtins.property
    @jsii.member(jsii_name="aes128Input")
    def aes128_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsAes128]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsAes128], jsii.get(self, "aes128Input"))

    @builtins.property
    @jsii.member(jsii_name="drmSystemsInput")
    def drm_systems_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystems]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystems], jsii.get(self, "drmSystemsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mpegCencInput")
    def mpeg_cenc_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsMpegCenc]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsMpegCenc], jsii.get(self, "mpegCencInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleAesInput")
    def sample_aes_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsSampleAes"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsSampleAes"], jsii.get(self, "sampleAesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerKeySourceInput")
    def secret_manager_key_source_input(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource"], jsii.get(self, "secretManagerKeySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a752af6706ffeba16deab2545ae0a8c41d7c16c4001b0db26a526da9d2a8e1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigEncryptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigEncryptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigEncryptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84e44ee7ccff9b831662faaf33de081107922c99d0586dd9322ba51f464ae62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsSampleAes",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleTranscoderJobConfigEncryptionsSampleAes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsSampleAes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEncryptionsSampleAesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsSampleAesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cc05a4c47e2e58c31483008a13154c2a7d267f6cf2a32632dee6deb610b6d84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsSampleAes]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsSampleAes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsSampleAes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478d1081781cfa58ec98b79c2f3f7f9d880bebfb630ee5753c43e638d3729df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#secret_version GoogleTranscoderJob#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca75ed8a409484e9ca711934ca90145aacc7244eb2a17d9a4a4b8a189e8ad8b0)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#secret_version GoogleTranscoderJob#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__760f5a48ec91365b69f0257fae0145da225376010d7933e4ec87f3a293b54fa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b02d2a7e94b66fecc38200f9b5a974c93a1366e903247a9b1811b0e697f9d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc9b3e84bb2adda235493c9f9bf24ca759bc3a8d39df9f3e0b7b678acb24bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigInputs",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "uri": "uri"},
)
class GoogleTranscoderJobConfigInputs:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: A unique key for this input. Must be specified when using advanced mapping and edit lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#key GoogleTranscoderJob#key}
        :param uri: URI of the media. Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, gs://bucket/inputs/file.mp4). If empty, the value is populated from Job.input_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#uri GoogleTranscoderJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1561bfd057255a6eec7c99d9e723abfaac675c511548b8dadb86bc385e89f7d4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#key GoogleTranscoderJob#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI of the media.

        Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, gs://bucket/inputs/file.mp4).
        If empty, the value is populated from Job.input_uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#uri GoogleTranscoderJob#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigInputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigInputsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigInputsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2833f2ddfbdb324e391efe1cdaf6f609a527e7985ae5930c552c03155f115727)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigInputsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345b892b60cd547b48c3690fd2866d1480fcfa86f78b4f5aea5f7ee5f1ef0e76)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigInputsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f557b33dccc859f722c3159ee3d3567d039335cc73c7070fd04c992227538be5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0facabdf4a6d674e80ce28ef4f0b8ca0a8ffc88983bc2bc9e0edbdb5adfb4947)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de378309eea780a31482efbad700bc2ef75e301d4e0368b9a8dd21dd41ac2e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigInputs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigInputs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigInputs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63add1485be3f120d79517e9b0e7509e66a3eaac71d527295afb55e49b0aa5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigInputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigInputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0a5ff5d0186c7b0cb4130c0c16463a505c43454322b5a0e8776aad193576069)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34398c54630bef3e43bf245d5d35e84092350bd90584e506e810bd5c4915954c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a08ebf13b6b8ea666bb1a66dba86dc118da2b2a19b0d56c71a674f2a6236be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigInputs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigInputs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigInputs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d61d1ef93386779dde0ad8ac1e77395d36f8d3e8c3822393aa98ad928b3375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigManifests",
    jsii_struct_bases=[],
    name_mapping={
        "file_name": "fileName",
        "mux_streams": "muxStreams",
        "type": "type",
    },
)
class GoogleTranscoderJobConfigManifests:
    def __init__(
        self,
        *,
        file_name: typing.Optional[builtins.str] = None,
        mux_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_name: The name of the generated file. The default is 'manifest'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#file_name GoogleTranscoderJob#file_name}
        :param mux_streams: List of user supplied MuxStream.key values that should appear in this manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#mux_streams GoogleTranscoderJob#mux_streams}
        :param type: Type of the manifest. Possible values: ["MANIFEST_TYPE_UNSPECIFIED", "HLS", "DASH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#type GoogleTranscoderJob#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68cf7c8c2a0c1ba59cc377ccd9d31ddec8039c9eecef467091cf81d84770de31)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#file_name GoogleTranscoderJob#file_name}
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mux_streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user supplied MuxStream.key values that should appear in this manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#mux_streams GoogleTranscoderJob#mux_streams}
        '''
        result = self._values.get("mux_streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of the manifest. Possible values: ["MANIFEST_TYPE_UNSPECIFIED", "HLS", "DASH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#type GoogleTranscoderJob#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigManifests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigManifestsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigManifestsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5ea0f3214beb33855129aadf4546f000f1e9b888d97b82b3cf0601501824e51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigManifestsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e455b4c2153dad2fcca925a796434f53a819d3af4f265be735d53e87c006be60)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigManifestsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4a567840e0997d4cba74b50b8d6367fd6f702b0ce1e3b4eb7e9f8c12084ffd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c530a320f456660e4356ee861bbf7ba7f7fdcadbfcf1f79a33875b985826a52a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66be527eb6a9464ca2133bdbedb3c3855f9c7a33b767a0aea0315f34189a6afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigManifests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigManifests]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigManifests]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bef59f67396006ede3ce92a56e154ca5daa282724d2211a6864cb3ec0233a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigManifestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigManifestsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abb10538b4acce58d6745f293f8a76bc6e815f8de7b8386c9e73eecd7b1fdfe0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8ac0bf31d62cc10596f540de0b64a96caa9d6a2f4cdf31f7dfd34c5e0f82ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="muxStreams")
    def mux_streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "muxStreams"))

    @mux_streams.setter
    def mux_streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b7148a5f4804fb1a8c4d7e3b11cd1673eb1760a9577e7fd88608c4669c911e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "muxStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f5d56867d049720070678ef4459bb0ee0b302c87347f6eefcd44de450088db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigManifests]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigManifests]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigManifests]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f593bd750998f3514ba3f92388cf06bbd9116736ba7fda58dff1f54071e48ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigMuxStreams",
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
class GoogleTranscoderJobConfigMuxStreams:
    def __init__(
        self,
        *,
        container: typing.Optional[builtins.str] = None,
        elementary_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
        encryption_id: typing.Optional[builtins.str] = None,
        file_name: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        segment_settings: typing.Optional[typing.Union["GoogleTranscoderJobConfigMuxStreamsSegmentSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: The container format. The default is 'mp4'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#container GoogleTranscoderJob#container}
        :param elementary_streams: List of ElementaryStream.key values multiplexed in this stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#elementary_streams GoogleTranscoderJob#elementary_streams}
        :param encryption_id: Identifier of the encryption configuration to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#encryption_id GoogleTranscoderJob#encryption_id}
        :param file_name: The name of the generated file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#file_name GoogleTranscoderJob#file_name}
        :param key: A unique key for this multiplexed stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#key GoogleTranscoderJob#key}
        :param segment_settings: segment_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#segment_settings GoogleTranscoderJob#segment_settings}
        '''
        if isinstance(segment_settings, dict):
            segment_settings = GoogleTranscoderJobConfigMuxStreamsSegmentSettings(**segment_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f52d2c9c4521e626e196b8bd0a63d4b968daa02c63ea99606a9a5628ea1eec4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#container GoogleTranscoderJob#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elementary_streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of ElementaryStream.key values multiplexed in this stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#elementary_streams GoogleTranscoderJob#elementary_streams}
        '''
        result = self._values.get("elementary_streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def encryption_id(self) -> typing.Optional[builtins.str]:
        '''Identifier of the encryption configuration to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#encryption_id GoogleTranscoderJob#encryption_id}
        '''
        result = self._values.get("encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_name(self) -> typing.Optional[builtins.str]:
        '''The name of the generated file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#file_name GoogleTranscoderJob#file_name}
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this multiplexed stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#key GoogleTranscoderJob#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_settings(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigMuxStreamsSegmentSettings"]:
        '''segment_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#segment_settings GoogleTranscoderJob#segment_settings}
        '''
        result = self._values.get("segment_settings")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigMuxStreamsSegmentSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigMuxStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigMuxStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigMuxStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__852480ef9f371ed41680808f0b53a7d4c46cb3731cdce58fa60350827a58fdfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigMuxStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b720680c382903fc2607923725809d2a65376de641a507cbbf90eafdf5d9bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigMuxStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96797a3c48fc7460e04db14aa08f9ae014062c93020c521813d3c5fbc097d180)
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
            type_hints = typing.get_type_hints(_typecheckingstub__222855f64d95ea67d9e2cad3b344552ba568ea57c2806290d4f1d7e30bd4a632)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15cfa9e6f8e981cdbee07627452723411fc0839085d6288a060a92e417a66963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigMuxStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigMuxStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigMuxStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3347ad620bced6ed0a8f596cfbb45c2f6b69a23a47a7c407e0024fb253895e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigMuxStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigMuxStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e85bc0e8bccd397ff788c2c63a98c382633ce0eccfe30cd90693471777d169e9)
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
        :param segment_duration: Duration of the segments in seconds. The default is '6.0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#segment_duration GoogleTranscoderJob#segment_duration}
        '''
        value = GoogleTranscoderJobConfigMuxStreamsSegmentSettings(
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
    ) -> "GoogleTranscoderJobConfigMuxStreamsSegmentSettingsOutputReference":
        return typing.cast("GoogleTranscoderJobConfigMuxStreamsSegmentSettingsOutputReference", jsii.get(self, "segmentSettings"))

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
    ) -> typing.Optional["GoogleTranscoderJobConfigMuxStreamsSegmentSettings"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigMuxStreamsSegmentSettings"], jsii.get(self, "segmentSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87b52a45063dd90b83a31617ee6610169cf1a56f48ef1b0c126090d9496dff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elementaryStreams")
    def elementary_streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "elementaryStreams"))

    @elementary_streams.setter
    def elementary_streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cf6ff33dd6e030cc67e81945b0d3d88fce1efe736f00e31724a961af1b97a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elementaryStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionId")
    def encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionId"))

    @encryption_id.setter
    def encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140d60696e11f4ea13174dea9f76ff1723325202281be067c83815ae41bbffa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997ce331e4d6a6bf4d60bdde79ca873cb381a72d99b9a3a1bd49e28ea7168dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d691106d9b085be457f8f1141e64cf5f5753de105bdb918e963d41c2ee29647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigMuxStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigMuxStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigMuxStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde4aafa38b7fef894d3d5aa6bcb09ce92ab9a724db418b880efb9dc7f8b1434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigMuxStreamsSegmentSettings",
    jsii_struct_bases=[],
    name_mapping={"segment_duration": "segmentDuration"},
)
class GoogleTranscoderJobConfigMuxStreamsSegmentSettings:
    def __init__(
        self,
        *,
        segment_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param segment_duration: Duration of the segments in seconds. The default is '6.0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#segment_duration GoogleTranscoderJob#segment_duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff3e5501fc72f6db3d47212d69592ee37fd26050c4bbcc5f47988d93a18a2cf)
            check_type(argname="argument segment_duration", value=segment_duration, expected_type=type_hints["segment_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if segment_duration is not None:
            self._values["segment_duration"] = segment_duration

    @builtins.property
    def segment_duration(self) -> typing.Optional[builtins.str]:
        '''Duration of the segments in seconds. The default is '6.0s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#segment_duration GoogleTranscoderJob#segment_duration}
        '''
        result = self._values.get("segment_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigMuxStreamsSegmentSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigMuxStreamsSegmentSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigMuxStreamsSegmentSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24536136020f2d695bd3f2365178a7a1e9eab5bd00c1cd6047b2c8e1f5a92fa1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfdfbde15ebb6ce9777998a62c28c4b11990d65163153fa8de930c5fd42d27dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigMuxStreamsSegmentSettings]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigMuxStreamsSegmentSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigMuxStreamsSegmentSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98a19d81a0b8ffa8adbddf2208264419c9c01f17a26c4f0894243a08c3af270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOutput",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleTranscoderJobConfigOutput:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: URI for the output file(s). For example, gs://my-bucket/outputs/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#uri GoogleTranscoderJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e507bcd3bdc1e3554a26c879cac1d8f6b62262e9ff09edbe37885a7594ae04b)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI for the output file(s). For example, gs://my-bucket/outputs/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#uri GoogleTranscoderJob#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d196c7b05c39647298ff7b60a578c0583b128bad2f6c239577907ef9dcce05c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd854269917742f5362ed6937e2ba5fddd173955d81044bf2af4362b50b26d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleTranscoderJobConfigOutput]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b777bf110f20d9f8712774520d43e1a1d5d9c1b1297e56c85274aa337282789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlays",
    jsii_struct_bases=[],
    name_mapping={"animations": "animations", "image": "image"},
)
class GoogleTranscoderJobConfigOverlays:
    def __init__(
        self,
        *,
        animations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTranscoderJobConfigOverlaysAnimations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        image: typing.Optional[typing.Union["GoogleTranscoderJobConfigOverlaysImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param animations: animations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#animations GoogleTranscoderJob#animations}
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#image GoogleTranscoderJob#image}
        '''
        if isinstance(image, dict):
            image = GoogleTranscoderJobConfigOverlaysImage(**image)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f183820d60faab283a2f2b58de5af2a60942904001ed27a7f76b862eb6386c09)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigOverlaysAnimations"]]]:
        '''animations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#animations GoogleTranscoderJob#animations}
        '''
        result = self._values.get("animations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTranscoderJobConfigOverlaysAnimations"]]], result)

    @builtins.property
    def image(self) -> typing.Optional["GoogleTranscoderJobConfigOverlaysImage"]:
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#image GoogleTranscoderJob#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigOverlaysImage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigOverlays(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysAnimations",
    jsii_struct_bases=[],
    name_mapping={"animation_fade": "animationFade"},
)
class GoogleTranscoderJobConfigOverlaysAnimations:
    def __init__(
        self,
        *,
        animation_fade: typing.Optional[typing.Union["GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param animation_fade: animation_fade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#animation_fade GoogleTranscoderJob#animation_fade}
        '''
        if isinstance(animation_fade, dict):
            animation_fade = GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade(**animation_fade)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1914cbc54c9e67ee9b503be609e6b5b6272ff887529d4eb24094d75b6bb4bc13)
            check_type(argname="argument animation_fade", value=animation_fade, expected_type=type_hints["animation_fade"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if animation_fade is not None:
            self._values["animation_fade"] = animation_fade

    @builtins.property
    def animation_fade(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade"]:
        '''animation_fade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#animation_fade GoogleTranscoderJob#animation_fade}
        '''
        result = self._values.get("animation_fade")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigOverlaysAnimations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade",
    jsii_struct_bases=[],
    name_mapping={
        "fade_type": "fadeType",
        "end_time_offset": "endTimeOffset",
        "start_time_offset": "startTimeOffset",
        "xy": "xy",
    },
)
class GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade:
    def __init__(
        self,
        *,
        fade_type: builtins.str,
        end_time_offset: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
        xy: typing.Optional[typing.Union["GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fade_type: Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:. - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified. - 'FADE_IN': Fade the overlay object into view. - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#fade_type GoogleTranscoderJob#fade_type}
        :param end_time_offset: The time to end the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#end_time_offset GoogleTranscoderJob#end_time_offset}
        :param start_time_offset: The time to start the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#start_time_offset GoogleTranscoderJob#start_time_offset}
        :param xy: xy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#xy GoogleTranscoderJob#xy}
        '''
        if isinstance(xy, dict):
            xy = GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy(**xy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac03c4cf3ade40e7ff1673745c93775d8b214aa67f889ba9911ee1fa5d9b996e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#fade_type GoogleTranscoderJob#fade_type}
        '''
        result = self._values.get("fade_type")
        assert result is not None, "Required property 'fade_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_time_offset(self) -> typing.Optional[builtins.str]:
        '''The time to end the fade animation, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#end_time_offset GoogleTranscoderJob#end_time_offset}
        '''
        result = self._values.get("end_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''The time to start the fade animation, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#start_time_offset GoogleTranscoderJob#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xy(
        self,
    ) -> typing.Optional["GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy"]:
        '''xy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#xy GoogleTranscoderJob#xy}
        '''
        result = self._values.get("xy")
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fdc8d0004bb0bf167448a3831f531e0fde407ce104b4ad819ea73a76da6d667)
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
        :param x: Normalized x coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#x GoogleTranscoderJob#x}
        :param y: Normalized y coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#y GoogleTranscoderJob#y}
        '''
        value = GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy(x=x, y=y)

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
    ) -> "GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference":
        return typing.cast("GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference", jsii.get(self, "xy"))

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
    ) -> typing.Optional["GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy"]:
        return typing.cast(typing.Optional["GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy"], jsii.get(self, "xyInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeOffset")
    def end_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTimeOffset"))

    @end_time_offset.setter
    def end_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b30c5120d2804b060f6e35f791d894ed0ec93c35b8f97ccf78591ffab40d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fadeType")
    def fade_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fadeType"))

    @fade_type.setter
    def fade_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86262a5488f0dffd7b969ad27ea766102f47cfaa888dbfc7fd42803babe28d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fadeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e498d5f52c554a7172a0aab0639c8b9f09412fe378ed03bd000dbb6faf64b2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfecfa258e2e9146ff533b968fbf03b5b1e14b4b672796d63acd0884493a9d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy",
    jsii_struct_bases=[],
    name_mapping={"x": "x", "y": "y"},
)
class GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy:
    def __init__(
        self,
        *,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param x: Normalized x coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#x GoogleTranscoderJob#x}
        :param y: Normalized y coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#y GoogleTranscoderJob#y}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1c672d74eaafaa28a8cebf5f4fbe39f409b7e68fbdd2130a823fac797d0756)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#x GoogleTranscoderJob#x}
        '''
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        '''Normalized y coordinate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#y GoogleTranscoderJob#y}
        '''
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ac5329da3817a6ede3ddcfd192a85d1e22abc573af77c41a719a3ce884917f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5efbddfc5f6ba4d101b775e26e92b21dfbb76f71cc54388e1217530599c27766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "y"))

    @y.setter
    def y(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad22458c5cae68d470f140245f54f564f284c72f107a003f04df43d875522fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "y", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df91597fb1cd9ec78af4bc791eb17f8f6e6f9f6c424014edbfba3681d4a15781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigOverlaysAnimationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysAnimationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e4fbac7cc8ef2fcf5122169920d49ecf0e6fd14ad285f94549f7152a0e949cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigOverlaysAnimationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5411b2fd5dcac5024dd341da2c6f25fe0e461ce0e8a40887c114201758de575)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigOverlaysAnimationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4808f5d61ca28a8193e1060f0d4e3d3a266ee8bebebc3f1c22830bcec1d251)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faea652eb365d374c47bd92c3d5837fcfaec94b37634248fb7ef44e791fd236d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ab3ae5c64e746901104b80dd798bd6c91f0832a2899764ecbeaf0dfc344816c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlaysAnimations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlaysAnimations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlaysAnimations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3334ee3d3596416b4442fd85eaf9f6ad6130b0adf5cbb725afec4a9b6ca380c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigOverlaysAnimationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysAnimationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89f8e460627963779bfda4f67cbc73e65d149ec0717134c55dd57dd3e940f0df)
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
        xy: typing.Optional[typing.Union[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fade_type: Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:. - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified. - 'FADE_IN': Fade the overlay object into view. - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#fade_type GoogleTranscoderJob#fade_type}
        :param end_time_offset: The time to end the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#end_time_offset GoogleTranscoderJob#end_time_offset}
        :param start_time_offset: The time to start the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#start_time_offset GoogleTranscoderJob#start_time_offset}
        :param xy: xy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#xy GoogleTranscoderJob#xy}
        '''
        value = GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade(
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
    ) -> GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference:
        return typing.cast(GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference, jsii.get(self, "animationFade"))

    @builtins.property
    @jsii.member(jsii_name="animationFadeInput")
    def animation_fade_input(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade], jsii.get(self, "animationFadeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigOverlaysAnimations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigOverlaysAnimations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigOverlaysAnimations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60fa99f83c08be4cb5481756203ac6d07d946b92a4da326c410477afd0045592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysImage",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class GoogleTranscoderJobConfigOverlaysImage:
    def __init__(self, *, uri: builtins.str) -> None:
        '''
        :param uri: URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#uri GoogleTranscoderJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6beb5fc47520922ee5ab33e8e5c854ed51839edaf165f3b6f67decd435aaa8)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#uri GoogleTranscoderJob#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigOverlaysImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigOverlaysImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e96a22d382479e05986ed2a295a15b5e78d885422407466c3ca4e9926d58f18f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f6b8254eff38a4999c7bae3887d5113483913beb819be0a9b2bafea9d8f0bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleTranscoderJobConfigOverlaysImage]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigOverlaysImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigOverlaysImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77b669b5f380e752745309c8c744c4681a7bc970f9eeca7353694da494df024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigOverlaysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__057c03396a6bb4956969347d860af0ebb85ebdf6f8718786d58991a2f3f5897c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTranscoderJobConfigOverlaysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef15dad5317868bd703338ee08a8f6386947179bf3f7e668d674920912f584b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTranscoderJobConfigOverlaysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15cf8c4fb8be53163a8db2733732e72086ba899a064dc3c851abe80f61aa6fb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9e04a37fc097474310838830cd5147b71d5ce89d9c71b3e96aac38692aa5667)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f83b485f495871207fd163167246112aee6272f9465adaa7301f4027d3f68e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlays]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlays]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlays]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d6ccac847bbe8c596bdd51f94361befae5d111a0ce783152400aa160092b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTranscoderJobConfigOverlaysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigOverlaysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__175dcac789c01c2a34051faca14c5e224c2e9d4cbf9e05677036393eb6d838a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAnimations")
    def put_animations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea7a2a7c8a4bd4460f19b336ff4def58e6ef65803b9abfb5699aa20dce5af8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnimations", [value]))

    @jsii.member(jsii_name="putImage")
    def put_image(self, *, uri: builtins.str) -> None:
        '''
        :param uri: URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#uri GoogleTranscoderJob#uri}
        '''
        value = GoogleTranscoderJobConfigOverlaysImage(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="resetAnimations")
    def reset_animations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnimations", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @builtins.property
    @jsii.member(jsii_name="animations")
    def animations(self) -> GoogleTranscoderJobConfigOverlaysAnimationsList:
        return typing.cast(GoogleTranscoderJobConfigOverlaysAnimationsList, jsii.get(self, "animations"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> GoogleTranscoderJobConfigOverlaysImageOutputReference:
        return typing.cast(GoogleTranscoderJobConfigOverlaysImageOutputReference, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="animationsInput")
    def animations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlaysAnimations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlaysAnimations]]], jsii.get(self, "animationsInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[GoogleTranscoderJobConfigOverlaysImage]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigOverlaysImage], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigOverlays]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigOverlays]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigOverlays]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d6ce4aa6de9110c8e8e006479cee1428e2a85584049400d36a3888597f8bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigPubsubDestination",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class GoogleTranscoderJobConfigPubsubDestination:
    def __init__(self, *, topic: typing.Optional[builtins.str] = None) -> None:
        '''
        :param topic: The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#topic GoogleTranscoderJob#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b29d579cc0caaefed1169f2021320344a9ba2085bed1a8d36ef91f297b75c54)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#topic GoogleTranscoderJob#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobConfigPubsubDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobConfigPubsubDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobConfigPubsubDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__228852463a570da96a8230a1f4bed52493a3b3a099e5fca27a1edb6fe28f7f1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1879e5ae9370b2198eac78baf4210075f082eca61426fc21c1a7863d51f6842e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTranscoderJobConfigPubsubDestination]:
        return typing.cast(typing.Optional[GoogleTranscoderJobConfigPubsubDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTranscoderJobConfigPubsubDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5361c3eb6dc49600f5c27884643747b75d70a6e9390f6f23f83f7fd90b319d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleTranscoderJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#create GoogleTranscoderJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#delete GoogleTranscoderJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#update GoogleTranscoderJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05763944beedc4b73bd1ee9f7e4254899320f85f677da2c4326f5285fb71b492)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#create GoogleTranscoderJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#delete GoogleTranscoderJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_transcoder_job#update GoogleTranscoderJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTranscoderJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTranscoderJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTranscoderJob.GoogleTranscoderJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb3ec65670b8559654bef1701cf295134bf49e729eead6327ba66bf9d40d8618)
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
            type_hints = typing.get_type_hints(_typecheckingstub__178c26640f64003f2f0f6cfc5587d90a2068ac3defd77ef354524f0b408e800a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96713482cb519a13f996cd7a245e067a60f077244dc4026ad5a9ccb2774730b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343d978dc82a732f790f0fb87befb89f8ea0d1b2bffd6d9ebf7839a64ab4c551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b138de776d390b7a4230fda6f1f3822bde9993bb4c9b9fe6454a23bb7f7419b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleTranscoderJob",
    "GoogleTranscoderJobConfig",
    "GoogleTranscoderJobConfigA",
    "GoogleTranscoderJobConfigAOutputReference",
    "GoogleTranscoderJobConfigAdBreaks",
    "GoogleTranscoderJobConfigAdBreaksList",
    "GoogleTranscoderJobConfigAdBreaksOutputReference",
    "GoogleTranscoderJobConfigEditListStruct",
    "GoogleTranscoderJobConfigEditListStructList",
    "GoogleTranscoderJobConfigEditListStructOutputReference",
    "GoogleTranscoderJobConfigElementaryStreams",
    "GoogleTranscoderJobConfigElementaryStreamsAudioStream",
    "GoogleTranscoderJobConfigElementaryStreamsAudioStreamOutputReference",
    "GoogleTranscoderJobConfigElementaryStreamsList",
    "GoogleTranscoderJobConfigElementaryStreamsOutputReference",
    "GoogleTranscoderJobConfigElementaryStreamsVideoStream",
    "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264",
    "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg",
    "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference",
    "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference",
    "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr",
    "GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference",
    "GoogleTranscoderJobConfigElementaryStreamsVideoStreamOutputReference",
    "GoogleTranscoderJobConfigEncryptions",
    "GoogleTranscoderJobConfigEncryptionsAes128",
    "GoogleTranscoderJobConfigEncryptionsAes128OutputReference",
    "GoogleTranscoderJobConfigEncryptionsDrmSystems",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsOutputReference",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine",
    "GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference",
    "GoogleTranscoderJobConfigEncryptionsList",
    "GoogleTranscoderJobConfigEncryptionsMpegCenc",
    "GoogleTranscoderJobConfigEncryptionsMpegCencOutputReference",
    "GoogleTranscoderJobConfigEncryptionsOutputReference",
    "GoogleTranscoderJobConfigEncryptionsSampleAes",
    "GoogleTranscoderJobConfigEncryptionsSampleAesOutputReference",
    "GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource",
    "GoogleTranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference",
    "GoogleTranscoderJobConfigInputs",
    "GoogleTranscoderJobConfigInputsList",
    "GoogleTranscoderJobConfigInputsOutputReference",
    "GoogleTranscoderJobConfigManifests",
    "GoogleTranscoderJobConfigManifestsList",
    "GoogleTranscoderJobConfigManifestsOutputReference",
    "GoogleTranscoderJobConfigMuxStreams",
    "GoogleTranscoderJobConfigMuxStreamsList",
    "GoogleTranscoderJobConfigMuxStreamsOutputReference",
    "GoogleTranscoderJobConfigMuxStreamsSegmentSettings",
    "GoogleTranscoderJobConfigMuxStreamsSegmentSettingsOutputReference",
    "GoogleTranscoderJobConfigOutput",
    "GoogleTranscoderJobConfigOutputOutputReference",
    "GoogleTranscoderJobConfigOverlays",
    "GoogleTranscoderJobConfigOverlaysAnimations",
    "GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade",
    "GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference",
    "GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy",
    "GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference",
    "GoogleTranscoderJobConfigOverlaysAnimationsList",
    "GoogleTranscoderJobConfigOverlaysAnimationsOutputReference",
    "GoogleTranscoderJobConfigOverlaysImage",
    "GoogleTranscoderJobConfigOverlaysImageOutputReference",
    "GoogleTranscoderJobConfigOverlaysList",
    "GoogleTranscoderJobConfigOverlaysOutputReference",
    "GoogleTranscoderJobConfigPubsubDestination",
    "GoogleTranscoderJobConfigPubsubDestinationOutputReference",
    "GoogleTranscoderJobTimeouts",
    "GoogleTranscoderJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0cf9fc8c3f9281a1d3a454c502dac0222129f7c60fb1e6f74ace3626508f3126(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    config: typing.Optional[typing.Union[GoogleTranscoderJobConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleTranscoderJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3a5aaf03a2265fcd69733494fc76250715b2155463a026837f7159b4a1c46ae5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50f82e1450109ac19b481bd64518900d1ea0454fbfdd7331c5d081db5005d1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d747742b9d7f1d47ba32812c4c3ed1472a5fa95e6f6ab644fa9edb390d9f231(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e970d25e796aee55b3f659166af344e5d5133580e809af0fffdcc9daa399dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c507cac81ff0002589729ff956a69cf82686e038426213ec0719368634a769ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9ab944883518bf8c5eec70c28db69321b5c17c306d2619ee375df64666aac0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bf03f0cef5ee535fffe442a5962b0b411fa3d18cbabd56204a274e1b8d0054(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    config: typing.Optional[typing.Union[GoogleTranscoderJobConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleTranscoderJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd613debed1907f28e33df26d20bde8a6b06a850b74c2f8085fe74ac07101fc5(
    *,
    ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigAdBreaks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigEditListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigElementaryStreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigEncryptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigInputs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigManifests, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigMuxStreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    output: typing.Optional[typing.Union[GoogleTranscoderJobConfigOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigOverlays, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pubsub_destination: typing.Optional[typing.Union[GoogleTranscoderJobConfigPubsubDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56739feae1de6818779d865a695b0dd27058bf50c17e349f78461f9390dc26cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b75575117334e9d5a8c8f2101d87420103e69b6b192a85b6b65dba610b4a68f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigAdBreaks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecce3b72520a3cfe541fbff3b086f4cf7e7dafc6eb8a74201a4d702b924442a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigEditListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c41f09ca8992dbf090cc608129453771048cb42fed594cb95695a7f4258c02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigElementaryStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f28373cff03c3eb5963c5b275f2237364aa11d8033661b14b178275c35b26ed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigEncryptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809027ec226e0950cbd7784df758a86e89f856f9c809e016e475e27b455ecf0d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigInputs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3179993182399150702a04ec516f95275ea56fe9d0154ee6d22c5c02328fd3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigManifests, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65e16c38d74848eb5c72bc89af06de8ffe45ff93ed09d3cf67dcc5b08dea414(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigMuxStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f41e0e64f4155657f922618768e20d5ba04aea4ae39e097eddcb6d51979d323(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigOverlays, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3930858682dadfebcbf65daafe11985b7994242e376cc80c4151ae6c1c4a3280(
    value: typing.Optional[GoogleTranscoderJobConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a58eec09e9e8fa02d3958e95e8f87d5cab6587a4bd00465edfd246ef4c7c48c(
    *,
    start_time_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257e09ce6795eb76fe64e312e57c12299deaf1c019f4c032ba4c236a95f108ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64f2e81d1c7d92c5796beac9d68ba2f409753143b3130635d108c23ecd07d64(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd725e8af2fc2ec7c0e10c20a3e7c5acde682265ae25f32769b50f5fc2dd3495(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e22f78cad728161d1b6e6f808a4b0de324dd3c40b2d5b8ef81b01287958e6dc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5547a8d4eba4b0254f2addc761c3d8faa1a63550d314abc64367c218ff00c3a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ac8773312b66205806d360c2a9509889fc9733d2862f981d3beefa5d1f319d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigAdBreaks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000704ce560d3275b926d4add962903869a7a91ba0dcea2d599b995ae31b9b94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e08247b492f03f04cdd0ff974fd47dad23f178d08d66b65f90f7fa9c76ecd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e197f7405a024c652751d2a199506e643ed4b1aabdde0fcdf5db67c8b24b9e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigAdBreaks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac72f93d9d24b522eb9a71a7c54eec3b0de062377037d10bb86fa5e5c7212f80(
    *,
    inputs: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[builtins.str] = None,
    start_time_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e063adfbf9a821057caa62591301adcbd6375787da5af4944fad47eb792aa1fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a1530863883e6228f4c9e15ced16fadbc83c7164d4cd436e6d1e7b244a0a1f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e517d226036b5b940b7df7830115caa925e91051b34af5c41b0837d994341e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356da80303512b4be48855f6bc1c285a790c85b0fdf302f36cf713e8ecfc6c8e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57704673ca81949c54d8b64eef876a91c28fde3f6195c6786171b120c039e55a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f461e0766bbf90662dd6233ffeaed0e72e77728b02cf7aa7c1810cbc54263f0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigEditListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afe8cd14219aadc709a5f437ac1cf6cccfe3fc7435848faa10f802142951471(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b56fc927331ae5620b9af28748d671b12fb80402efca0154cabf70d3a3164f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0482f40ef07b34388b2083c73fae1fad172cbf6368fb7bd81c4f39b7335c613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7dba5ccbca86416341b0d62350524e389d326cb22aa897ef6c401bc5b3eebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e958e1403cf3b7b100913f326b32c1aa751f12614a2f9c8cb2a3ad07c3bdf87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigEditListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a43ddeeccd8d320f42be20926bef9d15e672f4c3ab3397c6f07dcf482240a4f(
    *,
    audio_stream: typing.Optional[typing.Union[GoogleTranscoderJobConfigElementaryStreamsAudioStream, typing.Dict[builtins.str, typing.Any]]] = None,
    key: typing.Optional[builtins.str] = None,
    video_stream: typing.Optional[typing.Union[GoogleTranscoderJobConfigElementaryStreamsVideoStream, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeb3a823bfb14c35ebe5619d0b40f08afc2bdb80aeff7908155789a26da9e31(
    *,
    bitrate_bps: jsii.Number,
    channel_count: typing.Optional[jsii.Number] = None,
    channel_layout: typing.Optional[typing.Sequence[builtins.str]] = None,
    codec: typing.Optional[builtins.str] = None,
    sample_rate_hertz: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eca12899e49a03a5c914313a745df05b23511c30fadd5f0f537886a8824ad6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de85136c16d00170c38217da3062d4213fec2df3dab61d464d7b8e647ce3015(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52a224bdd56498474f1b9051303c731a428494a1d39ef510e4f2c0efa98ec97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550f5bbb3ff0e7709274aa2bdac21f4b22ebc6128aa538b7adb35a7f0174899c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6191455489d0093116d7c4e59bc13ed005854664a90fced960bb400751e209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43a997a87993256043f5dacafb04d00ceb356bb85f025747ad0a0a3de3ed8a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0aa1596979b9622bf0e9250d7ea035011c451ddd66c2bf330d5ebab94644df(
    value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsAudioStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a8b593b79f7f9b9670fe5c24f67535afcc5b219fb78be21f1acc7f965ec5a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d31dfda6909d8a3522aa267257f5e18015b5ce48bb03cdf535da3824a217dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d65d0419e95fe0b091c69a660ba51e1eb51dad87a6c278636f2e107dff0777e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9888eee42ac836b2421e815df3aa4623f3cc18eebb2049f4c7870c8968138c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39b13c36f157630b4a4366f0169269daf254059d4892866e4181230febc2a25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82331e791fd341b17833220d9dcd26b372e495d36f7e6a71d445159fd3b011c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigElementaryStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754fd465c70a966046bdbc99e42e68c84823129bc66964ba9cb0b753cada0b4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12532e65f8983d4bd138301410486cfa20c1952053dc588897f768ad1d564b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb2d04df35a3e0e02871ac67af6b2ecc0cc67f5868d49b398bc231166f60191(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigElementaryStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1815644e61fc07b3a0568c2e3d20df22ef479880591273176fcd7068e738e5f(
    *,
    h264: typing.Optional[typing.Union[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803133149abc0b67aa294c85044e7b1af409850b1dac06bf9916910825284a67(
    *,
    bitrate_bps: jsii.Number,
    frame_rate: jsii.Number,
    crf_level: typing.Optional[jsii.Number] = None,
    entropy_coder: typing.Optional[builtins.str] = None,
    gop_duration: typing.Optional[builtins.str] = None,
    height_pixels: typing.Optional[jsii.Number] = None,
    hlg: typing.Optional[typing.Union[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg, typing.Dict[builtins.str, typing.Any]]] = None,
    pixel_format: typing.Optional[builtins.str] = None,
    preset: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    rate_control_mode: typing.Optional[builtins.str] = None,
    sdr: typing.Optional[typing.Union[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr, typing.Dict[builtins.str, typing.Any]]] = None,
    vbv_fullness_bits: typing.Optional[jsii.Number] = None,
    vbv_size_bits: typing.Optional[jsii.Number] = None,
    width_pixels: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e4f3316faf1b03143a69ba84097a0ec54c3623fc8400ee472e399656f44384(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9dbf67ffbeabd61ae7cd2ab49cb1196641649223dd21bf4f3d1b4b5efd09a52(
    value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Hlg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3974bbc02315cec13ff0e35692c958d0bab145de4366b286994c2a14b80edc4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951248351f379eca0e1f4ae0682d9ef16ae3597aa1384530ff7b5ef7c0b4c199(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb68296d73a61de098af05c9cb1a7a40abea33f92c4de5a0afeba3a48427dab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2f09e807469b930bc95f94557081abd1b1f799e4f1a92994bee0b985638cbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1665becdeac566a4ca2a7a84f95771f47773381341022426c984c9d2101bb0b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f24502871eff3cd07131c53e3eed5c1f7b6250008afa5253608e662e4ea8fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1003c4b262078cd77354a38df9fc9751cbdd8c0fdfe8d988b2ff65560a4f34(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82faa7a134cfae24a27faf397ae515286b646851efa9e7591930dca8a6a5bbe4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd3f09802e1db0c8e902d8115223c29e644f5f46d6df08ffe5029bd6406e207(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87361d8d257f66d67aef82f28d600043a8614b1b3be823d83004aabd63fff1cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32adeecabc01795a957dae4c8e4d65c627ed2dd0561fb1b5cbc12d8b3766a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f3f3a25c67ebf75f4f1baccca5d09ab0e6cf5ee68dce094dd891ea07e7f231(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c28db74d9223ee0aa7637301f79d111e1d53ed0c4785deb935104219e3e6dca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72cb002e5c48ae1fda4731744934db37624102fe3d1fb963230ac10701123da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813ef98322b79f2e49219aba10ba34b5d30f8a535c5c88990122a04a558552fb(
    value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee60a65803d474ee7eeb4acf123774546b3d58d3b62dbb2fcdc5b017eeb5df1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021aa2436e74c034e189dfc2f5896d51d80aadf2f6add38fe5e85e5aa55d74e2(
    value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStreamH264Sdr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4503fa5c9e015d9e716b88ae7ed584ae26e6a533a1bcde4fdfaaa8403b2bb611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182aa1561065fd70b99615791d9b5d967ec70e76de7e5f9943de4dcfa3c042f9(
    value: typing.Optional[GoogleTranscoderJobConfigElementaryStreamsVideoStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f3d79db212ca06bfe501b93036db605ed3400a6cd00b76a165dcb0b29b2cdc(
    *,
    id: builtins.str,
    aes128: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsAes128, typing.Dict[builtins.str, typing.Any]]] = None,
    drm_systems: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystems, typing.Dict[builtins.str, typing.Any]]] = None,
    mpeg_cenc: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsMpegCenc, typing.Dict[builtins.str, typing.Any]]] = None,
    sample_aes: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsSampleAes, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_manager_key_source: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad13e0feb41356df777c8959871085b908a7b0c9a96cf02fe193b9c110ad313(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f816508e1a94c92992a30e3b7baf1ad0182c50cd1b7ad812c7b8f0a093bd5b29(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsAes128],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf9bc988aff1404abc2b55b205f421d5ddc2b224cdb5b894ab4a395c0f1e274(
    *,
    clearkey: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey, typing.Dict[builtins.str, typing.Any]]] = None,
    fairplay: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
    playready: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
    widevine: typing.Optional[typing.Union[GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b557e923d601bf1cafe924ccbaec36766f6a342332f447d7abbd8e4c17654c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f99cb76d8c68e46c462ef26555128240bea52817ad832a1a4d4fb52f33f0f8e(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsClearkey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ac55f4464d6ad10135524324e890812abebd703778b4c385957da51badd036(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc41bfaf62ea432e690b6502c7abbee357894200dc5ef664beeabe878d3c6174(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsFairplay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351cd16d747dc5edea72adee24b40713af7ec9e4d9c16e0fa12a0147f09e8f68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4807e4e539866f01bc170b10803fe24c4293ad11239ed36f0b30b9dfd269ba3c(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystems],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fc7a10a562bf8da43b5c546c653943168a20574a0431c284ac5e47fedfd58f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937d5a31058e6fb5c82df86071c6fe3be71b6c3d0b96cacc9af7626975bfbef8(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsPlayready],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bac5fd943f008aa8a137338bdf7167d6025dff6f381d043d4e519006b33f6f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f57e813ecc8707d6fe0707e03335ec02bd64132eac4f85cd3c1b30fe9e1e85(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsDrmSystemsWidevine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b9db45c01229c29d9479a37048ffda701de95d8a224f939a15311b4227ed0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d27066a78edbd57999357c0c76083472dee99db08a9d1244c3eb3243567cefd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389dd13f3dd02f25ede4011131c73a39a047db592113a91c8f5d6b194e12c98d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2029807b45baab299eb626ae11cef1848870cd3e23cdd84daf7c28be55db60dc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ecb8d4d8f2c4fe78745664e1f61a5ffa0ca949a6b76724b86ad61d508c27d99(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405446bc85ad14c8d073076451d1148c5f2e33241217f1f8e8e646b3fe5f88ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigEncryptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27f4da4a478b181650ff375a2cc92bcd3cbb0e8c008fd2606233a40b6ba0b9f(
    *,
    scheme: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef28a1d3795c861f68cbd0654d20f808a46dc9eb10630539b3e5c6adf63331d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2dacf78de62efe18ddb2381e7c6054c7815880135374bc03cee7b3c607de174(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df3acfbf02f4abf2f56ba1a19d19fa41d1b16881d21da8eb205007c8cfaf4ee(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsMpegCenc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ea0e4e794ae93d4a162893115c60d8a80f154346bfc3b062746f3434f235ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a752af6706ffeba16deab2545ae0a8c41d7c16c4001b0db26a526da9d2a8e1a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84e44ee7ccff9b831662faaf33de081107922c99d0586dd9322ba51f464ae62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigEncryptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc05a4c47e2e58c31483008a13154c2a7d267f6cf2a32632dee6deb610b6d84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478d1081781cfa58ec98b79c2f3f7f9d880bebfb630ee5753c43e638d3729df6(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsSampleAes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca75ed8a409484e9ca711934ca90145aacc7244eb2a17d9a4a4b8a189e8ad8b0(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760f5a48ec91365b69f0257fae0145da225376010d7933e4ec87f3a293b54fa9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b02d2a7e94b66fecc38200f9b5a974c93a1366e903247a9b1811b0e697f9d5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc9b3e84bb2adda235493c9f9bf24ca759bc3a8d39df9f3e0b7b678acb24bb0(
    value: typing.Optional[GoogleTranscoderJobConfigEncryptionsSecretManagerKeySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1561bfd057255a6eec7c99d9e723abfaac675c511548b8dadb86bc385e89f7d4(
    *,
    key: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2833f2ddfbdb324e391efe1cdaf6f609a527e7985ae5930c552c03155f115727(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345b892b60cd547b48c3690fd2866d1480fcfa86f78b4f5aea5f7ee5f1ef0e76(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f557b33dccc859f722c3159ee3d3567d039335cc73c7070fd04c992227538be5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0facabdf4a6d674e80ce28ef4f0b8ca0a8ffc88983bc2bc9e0edbdb5adfb4947(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de378309eea780a31482efbad700bc2ef75e301d4e0368b9a8dd21dd41ac2e3b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63add1485be3f120d79517e9b0e7509e66a3eaac71d527295afb55e49b0aa5aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigInputs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a5ff5d0186c7b0cb4130c0c16463a505c43454322b5a0e8776aad193576069(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34398c54630bef3e43bf245d5d35e84092350bd90584e506e810bd5c4915954c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a08ebf13b6b8ea666bb1a66dba86dc118da2b2a19b0d56c71a674f2a6236be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d61d1ef93386779dde0ad8ac1e77395d36f8d3e8c3822393aa98ad928b3375(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigInputs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68cf7c8c2a0c1ba59cc377ccd9d31ddec8039c9eecef467091cf81d84770de31(
    *,
    file_name: typing.Optional[builtins.str] = None,
    mux_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ea0f3214beb33855129aadf4546f000f1e9b888d97b82b3cf0601501824e51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e455b4c2153dad2fcca925a796434f53a819d3af4f265be735d53e87c006be60(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4a567840e0997d4cba74b50b8d6367fd6f702b0ce1e3b4eb7e9f8c12084ffd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c530a320f456660e4356ee861bbf7ba7f7fdcadbfcf1f79a33875b985826a52a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66be527eb6a9464ca2133bdbedb3c3855f9c7a33b767a0aea0315f34189a6afc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bef59f67396006ede3ce92a56e154ca5daa282724d2211a6864cb3ec0233a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigManifests]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb10538b4acce58d6745f293f8a76bc6e815f8de7b8386c9e73eecd7b1fdfe0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ac0bf31d62cc10596f540de0b64a96caa9d6a2f4cdf31f7dfd34c5e0f82ba4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b7148a5f4804fb1a8c4d7e3b11cd1673eb1760a9577e7fd88608c4669c911e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f5d56867d049720070678ef4459bb0ee0b302c87347f6eefcd44de450088db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f593bd750998f3514ba3f92388cf06bbd9116736ba7fda58dff1f54071e48ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigManifests]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f52d2c9c4521e626e196b8bd0a63d4b968daa02c63ea99606a9a5628ea1eec4(
    *,
    container: typing.Optional[builtins.str] = None,
    elementary_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_id: typing.Optional[builtins.str] = None,
    file_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    segment_settings: typing.Optional[typing.Union[GoogleTranscoderJobConfigMuxStreamsSegmentSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852480ef9f371ed41680808f0b53a7d4c46cb3731cdce58fa60350827a58fdfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b720680c382903fc2607923725809d2a65376de641a507cbbf90eafdf5d9bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96797a3c48fc7460e04db14aa08f9ae014062c93020c521813d3c5fbc097d180(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222855f64d95ea67d9e2cad3b344552ba568ea57c2806290d4f1d7e30bd4a632(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cfa9e6f8e981cdbee07627452723411fc0839085d6288a060a92e417a66963(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3347ad620bced6ed0a8f596cfbb45c2f6b69a23a47a7c407e0024fb253895e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigMuxStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85bc0e8bccd397ff788c2c63a98c382633ce0eccfe30cd90693471777d169e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87b52a45063dd90b83a31617ee6610169cf1a56f48ef1b0c126090d9496dff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cf6ff33dd6e030cc67e81945b0d3d88fce1efe736f00e31724a961af1b97a8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140d60696e11f4ea13174dea9f76ff1723325202281be067c83815ae41bbffa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997ce331e4d6a6bf4d60bdde79ca873cb381a72d99b9a3a1bd49e28ea7168dd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d691106d9b085be457f8f1141e64cf5f5753de105bdb918e963d41c2ee29647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde4aafa38b7fef894d3d5aa6bcb09ce92ab9a724db418b880efb9dc7f8b1434(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigMuxStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff3e5501fc72f6db3d47212d69592ee37fd26050c4bbcc5f47988d93a18a2cf(
    *,
    segment_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24536136020f2d695bd3f2365178a7a1e9eab5bd00c1cd6047b2c8e1f5a92fa1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfdfbde15ebb6ce9777998a62c28c4b11990d65163153fa8de930c5fd42d27dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98a19d81a0b8ffa8adbddf2208264419c9c01f17a26c4f0894243a08c3af270(
    value: typing.Optional[GoogleTranscoderJobConfigMuxStreamsSegmentSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e507bcd3bdc1e3554a26c879cac1d8f6b62262e9ff09edbe37885a7594ae04b(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d196c7b05c39647298ff7b60a578c0583b128bad2f6c239577907ef9dcce05c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd854269917742f5362ed6937e2ba5fddd173955d81044bf2af4362b50b26d66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b777bf110f20d9f8712774520d43e1a1d5d9c1b1297e56c85274aa337282789(
    value: typing.Optional[GoogleTranscoderJobConfigOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f183820d60faab283a2f2b58de5af2a60942904001ed27a7f76b862eb6386c09(
    *,
    animations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    image: typing.Optional[typing.Union[GoogleTranscoderJobConfigOverlaysImage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1914cbc54c9e67ee9b503be609e6b5b6272ff887529d4eb24094d75b6bb4bc13(
    *,
    animation_fade: typing.Optional[typing.Union[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac03c4cf3ade40e7ff1673745c93775d8b214aa67f889ba9911ee1fa5d9b996e(
    *,
    fade_type: builtins.str,
    end_time_offset: typing.Optional[builtins.str] = None,
    start_time_offset: typing.Optional[builtins.str] = None,
    xy: typing.Optional[typing.Union[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdc8d0004bb0bf167448a3831f531e0fde407ce104b4ad819ea73a76da6d667(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b30c5120d2804b060f6e35f791d894ed0ec93c35b8f97ccf78591ffab40d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86262a5488f0dffd7b969ad27ea766102f47cfaa888dbfc7fd42803babe28d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e498d5f52c554a7172a0aab0639c8b9f09412fe378ed03bd000dbb6faf64b2ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfecfa258e2e9146ff533b968fbf03b5b1e14b4b672796d63acd0884493a9d30(
    value: typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1c672d74eaafaa28a8cebf5f4fbe39f409b7e68fbdd2130a823fac797d0756(
    *,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac5329da3817a6ede3ddcfd192a85d1e22abc573af77c41a719a3ce884917f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efbddfc5f6ba4d101b775e26e92b21dfbb76f71cc54388e1217530599c27766(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad22458c5cae68d470f140245f54f564f284c72f107a003f04df43d875522fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df91597fb1cd9ec78af4bc791eb17f8f6e6f9f6c424014edbfba3681d4a15781(
    value: typing.Optional[GoogleTranscoderJobConfigOverlaysAnimationsAnimationFadeXy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4fbac7cc8ef2fcf5122169920d49ecf0e6fd14ad285f94549f7152a0e949cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5411b2fd5dcac5024dd341da2c6f25fe0e461ce0e8a40887c114201758de575(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4808f5d61ca28a8193e1060f0d4e3d3a266ee8bebebc3f1c22830bcec1d251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faea652eb365d374c47bd92c3d5837fcfaec94b37634248fb7ef44e791fd236d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab3ae5c64e746901104b80dd798bd6c91f0832a2899764ecbeaf0dfc344816c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3334ee3d3596416b4442fd85eaf9f6ad6130b0adf5cbb725afec4a9b6ca380c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlaysAnimations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f8e460627963779bfda4f67cbc73e65d149ec0717134c55dd57dd3e940f0df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fa99f83c08be4cb5481756203ac6d07d946b92a4da326c410477afd0045592(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigOverlaysAnimations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6beb5fc47520922ee5ab33e8e5c854ed51839edaf165f3b6f67decd435aaa8(
    *,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96a22d382479e05986ed2a295a15b5e78d885422407466c3ca4e9926d58f18f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6b8254eff38a4999c7bae3887d5113483913beb819be0a9b2bafea9d8f0bec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77b669b5f380e752745309c8c744c4681a7bc970f9eeca7353694da494df024(
    value: typing.Optional[GoogleTranscoderJobConfigOverlaysImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057c03396a6bb4956969347d860af0ebb85ebdf6f8718786d58991a2f3f5897c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef15dad5317868bd703338ee08a8f6386947179bf3f7e668d674920912f584b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cf8c4fb8be53163a8db2733732e72086ba899a064dc3c851abe80f61aa6fb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e04a37fc097474310838830cd5147b71d5ce89d9c71b3e96aac38692aa5667(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f83b485f495871207fd163167246112aee6272f9465adaa7301f4027d3f68e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d6ccac847bbe8c596bdd51f94361befae5d111a0ce783152400aa160092b0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTranscoderJobConfigOverlays]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175dcac789c01c2a34051faca14c5e224c2e9d4cbf9e05677036393eb6d838a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea7a2a7c8a4bd4460f19b336ff4def58e6ef65803b9abfb5699aa20dce5af8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTranscoderJobConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d6ce4aa6de9110c8e8e006479cee1428e2a85584049400d36a3888597f8bca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobConfigOverlays]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b29d579cc0caaefed1169f2021320344a9ba2085bed1a8d36ef91f297b75c54(
    *,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228852463a570da96a8230a1f4bed52493a3b3a099e5fca27a1edb6fe28f7f1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1879e5ae9370b2198eac78baf4210075f082eca61426fc21c1a7863d51f6842e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5361c3eb6dc49600f5c27884643747b75d70a6e9390f6f23f83f7fd90b319d46(
    value: typing.Optional[GoogleTranscoderJobConfigPubsubDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05763944beedc4b73bd1ee9f7e4254899320f85f677da2c4326f5285fb71b492(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3ec65670b8559654bef1701cf295134bf49e729eead6327ba66bf9d40d8618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178c26640f64003f2f0f6cfc5587d90a2068ac3defd77ef354524f0b408e800a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96713482cb519a13f996cd7a245e067a60f077244dc4026ad5a9ccb2774730b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343d978dc82a732f790f0fb87befb89f8ea0d1b2bffd6d9ebf7839a64ab4c551(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b138de776d390b7a4230fda6f1f3822bde9993bb4c9b9fe6454a23bb7f7419b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTranscoderJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
