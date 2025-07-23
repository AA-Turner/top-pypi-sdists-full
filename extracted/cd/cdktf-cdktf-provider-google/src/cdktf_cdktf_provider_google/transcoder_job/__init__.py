r'''
# `google_transcoder_job`

Refer to the Terraform Registry for docs: [`google_transcoder_job`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job).
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


class TranscoderJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job google_transcoder_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        config: typing.Optional[typing.Union["TranscoderJobConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["TranscoderJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job google_transcoder_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the transcoding job resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#location TranscoderJob#location}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#config TranscoderJob#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#id TranscoderJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this job. You can use these to organize and group your jobs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#labels TranscoderJob#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#project TranscoderJob#project}.
        :param template_id: Specify the templateId to use for populating Job.config. The default is preset/web-hd, which is the only supported preset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#template_id TranscoderJob#template_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#timeouts TranscoderJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971d1dc92cb010fe04d99ff4ed8aeb60384f3ae236e8b139af3c268555b5e4f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = TranscoderJobConfig(
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
        '''Generates CDKTF code for importing a TranscoderJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TranscoderJob to import.
        :param import_from_id: The id of the existing TranscoderJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TranscoderJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bded4068e76980d98e558729ecf98b77cac09235400cd090d0288888238652b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigInputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigManifests", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union["TranscoderJobConfigOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigOverlays", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pubsub_destination: typing.Optional[typing.Union["TranscoderJobConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_breaks: ad_breaks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#ad_breaks TranscoderJob#ad_breaks}
        :param edit_list: edit_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#edit_list TranscoderJob#edit_list}
        :param elementary_streams: elementary_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#elementary_streams TranscoderJob#elementary_streams}
        :param encryptions: encryptions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#encryptions TranscoderJob#encryptions}
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#inputs TranscoderJob#inputs}
        :param manifests: manifests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#manifests TranscoderJob#manifests}
        :param mux_streams: mux_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#mux_streams TranscoderJob#mux_streams}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#output TranscoderJob#output}
        :param overlays: overlays block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#overlays TranscoderJob#overlays}
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#pubsub_destination TranscoderJob#pubsub_destination}
        '''
        value = TranscoderJobConfigA(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#create TranscoderJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#delete TranscoderJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#update TranscoderJob#update}.
        '''
        value = TranscoderJobTimeouts(create=create, delete=delete, update=update)

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
    def config(self) -> "TranscoderJobConfigAOutputReference":
        return typing.cast("TranscoderJobConfigAOutputReference", jsii.get(self, "config"))

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
    def timeouts(self) -> "TranscoderJobTimeoutsOutputReference":
        return typing.cast("TranscoderJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["TranscoderJobConfigA"]:
        return typing.cast(typing.Optional["TranscoderJobConfigA"], jsii.get(self, "configInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TranscoderJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TranscoderJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422731a109e56cc8bdbd7d730198b951c58ff8b29875b801bd73db1412cbaf78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0eaa1de0e6a81d1d74b71cb3c626a8872a37b0a6361d584b348973640b7f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdef19b4f73d24e8acfdd1faeda249ab9bad58d8541994da331cf46204b8fdc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b3efface0b323e2acc6b4318a1f1514e476257a8411e7faa98298f558a1de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateId"))

    @template_id.setter
    def template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7ca12e6f4ba33457a489f13a6fba44013613235b1974e8fda4d89407cf0611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfig",
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
class TranscoderJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: typing.Optional[typing.Union["TranscoderJobConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        template_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["TranscoderJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the transcoding job resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#location TranscoderJob#location}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#config TranscoderJob#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#id TranscoderJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this job. You can use these to organize and group your jobs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#labels TranscoderJob#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#project TranscoderJob#project}.
        :param template_id: Specify the templateId to use for populating Job.config. The default is preset/web-hd, which is the only supported preset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#template_id TranscoderJob#template_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#timeouts TranscoderJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = TranscoderJobConfigA(**config)
        if isinstance(timeouts, dict):
            timeouts = TranscoderJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42bd564edd919cdd4705255d48fd847adda5fe59241f3acb58cb0fd32a4fadd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#location TranscoderJob#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["TranscoderJobConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#config TranscoderJob#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["TranscoderJobConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#id TranscoderJob#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#labels TranscoderJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#project TranscoderJob#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_id(self) -> typing.Optional[builtins.str]:
        '''Specify the templateId to use for populating Job.config. The default is preset/web-hd, which is the only supported preset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#template_id TranscoderJob#template_id}
        '''
        result = self._values.get("template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["TranscoderJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#timeouts TranscoderJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["TranscoderJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigA",
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
class TranscoderJobConfigA:
    def __init__(
        self,
        *,
        ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigInputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigManifests", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union["TranscoderJobConfigOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigOverlays", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pubsub_destination: typing.Optional[typing.Union["TranscoderJobConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_breaks: ad_breaks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#ad_breaks TranscoderJob#ad_breaks}
        :param edit_list: edit_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#edit_list TranscoderJob#edit_list}
        :param elementary_streams: elementary_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#elementary_streams TranscoderJob#elementary_streams}
        :param encryptions: encryptions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#encryptions TranscoderJob#encryptions}
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#inputs TranscoderJob#inputs}
        :param manifests: manifests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#manifests TranscoderJob#manifests}
        :param mux_streams: mux_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#mux_streams TranscoderJob#mux_streams}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#output TranscoderJob#output}
        :param overlays: overlays block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#overlays TranscoderJob#overlays}
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#pubsub_destination TranscoderJob#pubsub_destination}
        '''
        if isinstance(output, dict):
            output = TranscoderJobConfigOutput(**output)
        if isinstance(pubsub_destination, dict):
            pubsub_destination = TranscoderJobConfigPubsubDestination(**pubsub_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd470cba6ce8395a7333a95e25a9c37e32c11ff2004db9b2f5cc8038934b8ca)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigAdBreaks"]]]:
        '''ad_breaks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#ad_breaks TranscoderJob#ad_breaks}
        '''
        result = self._values.get("ad_breaks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigAdBreaks"]]], result)

    @builtins.property
    def edit_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigEditListStruct"]]]:
        '''edit_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#edit_list TranscoderJob#edit_list}
        '''
        result = self._values.get("edit_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigEditListStruct"]]], result)

    @builtins.property
    def elementary_streams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigElementaryStreams"]]]:
        '''elementary_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#elementary_streams TranscoderJob#elementary_streams}
        '''
        result = self._values.get("elementary_streams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigElementaryStreams"]]], result)

    @builtins.property
    def encryptions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigEncryptions"]]]:
        '''encryptions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#encryptions TranscoderJob#encryptions}
        '''
        result = self._values.get("encryptions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigEncryptions"]]], result)

    @builtins.property
    def inputs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigInputs"]]]:
        '''inputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#inputs TranscoderJob#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigInputs"]]], result)

    @builtins.property
    def manifests(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigManifests"]]]:
        '''manifests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#manifests TranscoderJob#manifests}
        '''
        result = self._values.get("manifests")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigManifests"]]], result)

    @builtins.property
    def mux_streams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigMuxStreams"]]]:
        '''mux_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#mux_streams TranscoderJob#mux_streams}
        '''
        result = self._values.get("mux_streams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigMuxStreams"]]], result)

    @builtins.property
    def output(self) -> typing.Optional["TranscoderJobConfigOutput"]:
        '''output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#output TranscoderJob#output}
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional["TranscoderJobConfigOutput"], result)

    @builtins.property
    def overlays(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigOverlays"]]]:
        '''overlays block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#overlays TranscoderJob#overlays}
        '''
        result = self._values.get("overlays")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigOverlays"]]], result)

    @builtins.property
    def pubsub_destination(
        self,
    ) -> typing.Optional["TranscoderJobConfigPubsubDestination"]:
        '''pubsub_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#pubsub_destination TranscoderJob#pubsub_destination}
        '''
        result = self._values.get("pubsub_destination")
        return typing.cast(typing.Optional["TranscoderJobConfigPubsubDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe31edc353f9f98a99c619aa1f275f1371d2df4c2633cb6bc348ac1a8f198ec3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdBreaks")
    def put_ad_breaks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29aad383b38b203462190c4350f9e2f62f6c386871ba7373b6694161e002a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdBreaks", [value]))

    @jsii.member(jsii_name="putEditList")
    def put_edit_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a566bf0569f2d32185e74df8dad1b1747cec44e45de5d99318d877875c4a44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEditList", [value]))

    @jsii.member(jsii_name="putElementaryStreams")
    def put_elementary_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c77018f9e2f355a5272ac874db47a04c19e9820f30de718ba2f33be565c6cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElementaryStreams", [value]))

    @jsii.member(jsii_name="putEncryptions")
    def put_encryptions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596db4b0fe59205b755d725d82e6bd0438933739242e63f6e4c725863c1a9104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEncryptions", [value]))

    @jsii.member(jsii_name="putInputs")
    def put_inputs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigInputs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c8ea3a060e97796dbcc6f0ec52e9ad3f1ccac2f1895f0b89b1897f4a9754b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputs", [value]))

    @jsii.member(jsii_name="putManifests")
    def put_manifests(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigManifests", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2c2d2de13b28b540e5d5779f36853ce418bc3c1a426446d0d3995022f742a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManifests", [value]))

    @jsii.member(jsii_name="putMuxStreams")
    def put_mux_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad495963f314c5f70ea969f91c1092c7dd0bdd6193013de23e61e96acd90bded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMuxStreams", [value]))

    @jsii.member(jsii_name="putOutput")
    def put_output(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: URI for the output file(s). For example, gs://my-bucket/outputs/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#uri TranscoderJob#uri}
        '''
        value = TranscoderJobConfigOutput(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putOutput", [value]))

    @jsii.member(jsii_name="putOverlays")
    def put_overlays(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigOverlays", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f837d556c7513eb26f8f93874a46a9889d8356767230f785c2212b3b20eca08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOverlays", [value]))

    @jsii.member(jsii_name="putPubsubDestination")
    def put_pubsub_destination(
        self,
        *,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic: The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#topic TranscoderJob#topic}
        '''
        value = TranscoderJobConfigPubsubDestination(topic=topic)

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
    def ad_breaks(self) -> "TranscoderJobConfigAdBreaksList":
        return typing.cast("TranscoderJobConfigAdBreaksList", jsii.get(self, "adBreaks"))

    @builtins.property
    @jsii.member(jsii_name="editList")
    def edit_list(self) -> "TranscoderJobConfigEditListStructList":
        return typing.cast("TranscoderJobConfigEditListStructList", jsii.get(self, "editList"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreams")
    def elementary_streams(self) -> "TranscoderJobConfigElementaryStreamsList":
        return typing.cast("TranscoderJobConfigElementaryStreamsList", jsii.get(self, "elementaryStreams"))

    @builtins.property
    @jsii.member(jsii_name="encryptions")
    def encryptions(self) -> "TranscoderJobConfigEncryptionsList":
        return typing.cast("TranscoderJobConfigEncryptionsList", jsii.get(self, "encryptions"))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> "TranscoderJobConfigInputsList":
        return typing.cast("TranscoderJobConfigInputsList", jsii.get(self, "inputs"))

    @builtins.property
    @jsii.member(jsii_name="manifests")
    def manifests(self) -> "TranscoderJobConfigManifestsList":
        return typing.cast("TranscoderJobConfigManifestsList", jsii.get(self, "manifests"))

    @builtins.property
    @jsii.member(jsii_name="muxStreams")
    def mux_streams(self) -> "TranscoderJobConfigMuxStreamsList":
        return typing.cast("TranscoderJobConfigMuxStreamsList", jsii.get(self, "muxStreams"))

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> "TranscoderJobConfigOutputOutputReference":
        return typing.cast("TranscoderJobConfigOutputOutputReference", jsii.get(self, "output"))

    @builtins.property
    @jsii.member(jsii_name="overlays")
    def overlays(self) -> "TranscoderJobConfigOverlaysList":
        return typing.cast("TranscoderJobConfigOverlaysList", jsii.get(self, "overlays"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestination")
    def pubsub_destination(
        self,
    ) -> "TranscoderJobConfigPubsubDestinationOutputReference":
        return typing.cast("TranscoderJobConfigPubsubDestinationOutputReference", jsii.get(self, "pubsubDestination"))

    @builtins.property
    @jsii.member(jsii_name="adBreaksInput")
    def ad_breaks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigAdBreaks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigAdBreaks"]]], jsii.get(self, "adBreaksInput"))

    @builtins.property
    @jsii.member(jsii_name="editListInput")
    def edit_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigEditListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigEditListStruct"]]], jsii.get(self, "editListInput"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreamsInput")
    def elementary_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigElementaryStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigElementaryStreams"]]], jsii.get(self, "elementaryStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionsInput")
    def encryptions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigEncryptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigEncryptions"]]], jsii.get(self, "encryptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigInputs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigInputs"]]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestsInput")
    def manifests_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigManifests"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigManifests"]]], jsii.get(self, "manifestsInput"))

    @builtins.property
    @jsii.member(jsii_name="muxStreamsInput")
    def mux_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigMuxStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigMuxStreams"]]], jsii.get(self, "muxStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="outputInput")
    def output_input(self) -> typing.Optional["TranscoderJobConfigOutput"]:
        return typing.cast(typing.Optional["TranscoderJobConfigOutput"], jsii.get(self, "outputInput"))

    @builtins.property
    @jsii.member(jsii_name="overlaysInput")
    def overlays_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigOverlays"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigOverlays"]]], jsii.get(self, "overlaysInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestinationInput")
    def pubsub_destination_input(
        self,
    ) -> typing.Optional["TranscoderJobConfigPubsubDestination"]:
        return typing.cast(typing.Optional["TranscoderJobConfigPubsubDestination"], jsii.get(self, "pubsubDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TranscoderJobConfigA]:
        return typing.cast(typing.Optional[TranscoderJobConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TranscoderJobConfigA]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d69c1e65ed8d006fb05ee7417841c4f43f5f2829d4930698f916113df2e99bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigAdBreaks",
    jsii_struct_bases=[],
    name_mapping={"start_time_offset": "startTimeOffset"},
)
class TranscoderJobConfigAdBreaks:
    def __init__(
        self,
        *,
        start_time_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_time_offset: Start time in seconds for the ad break, relative to the output file timeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#start_time_offset TranscoderJob#start_time_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db96242575cf0088869fdafaa12e61d5f9e83462f6cac51bb94a439e134c055)
            check_type(argname="argument start_time_offset", value=start_time_offset, expected_type=type_hints["start_time_offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if start_time_offset is not None:
            self._values["start_time_offset"] = start_time_offset

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''Start time in seconds for the ad break, relative to the output file timeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#start_time_offset TranscoderJob#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigAdBreaks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigAdBreaksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigAdBreaksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4b45b9c115232ed2f7a14c1d51cac3624a9d68b0a9f48ba807ec5aa240c931f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TranscoderJobConfigAdBreaksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e734c55e281388e5cf37d57df5ee06a4e66fdf977f9ec9165ef5b767366f31)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigAdBreaksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f97a14dcf9fc3894f6e2e7f4fe1b9ffdb8d44af6e79354b144639ee477be9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed427424f409597d753ef587863e696cbd07471a2eb8a4bf05fa2939e4b57088)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60ddf4c7aac60737515ab424de3620808315249bd0e3ddc3ee91c1a0c9d837be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigAdBreaks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigAdBreaks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigAdBreaks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07be8d9eefcf274429527ad582477d831d5ba743cb1a14376e10529314bd30e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigAdBreaksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigAdBreaksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5f157f2a820597f1c4d2e61a91cb891b1b3e93ca0fa859cf83966629bd96a26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__101897ff453883031846c59fd29b4f8f2aadf14103bbe2690743b8c8bb644b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigAdBreaks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigAdBreaks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigAdBreaks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__decc06f84b2c506deefc1fb81094c5cd85e1bb624b6ceb70c2f5a977cb8ab411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEditListStruct",
    jsii_struct_bases=[],
    name_mapping={
        "inputs": "inputs",
        "key": "key",
        "start_time_offset": "startTimeOffset",
    },
)
class TranscoderJobConfigEditListStruct:
    def __init__(
        self,
        *,
        inputs: typing.Optional[typing.Sequence[builtins.str]] = None,
        key: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inputs: List of values identifying files that should be used in this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#inputs TranscoderJob#inputs}
        :param key: A unique key for this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#key TranscoderJob#key}
        :param start_time_offset: Start time in seconds for the atom, relative to the input file timeline. The default is '0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#start_time_offset TranscoderJob#start_time_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8209f79b6eb1e46e51fdeafa3cf13a8a46aa839bdd6c0c54554e6c9b418ab43f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#inputs TranscoderJob#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#key TranscoderJob#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''Start time in seconds for the atom, relative to the input file timeline. The default is '0s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#start_time_offset TranscoderJob#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEditListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEditListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEditListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fae1dd78d91538160304c26d8a4fb8c93403acb33ae4672edcd6044f63aa7196)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobConfigEditListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e5e4e76762f508ee1992a2291db0e79537b87667684f02aa4a4b78655cb19b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigEditListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1eeae247d85ed6df27c4744d8f047bc71f13ca02414e3cbafcac8ab8409e529)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73aa700a2d0c86708e628bcca6fd34cfe33edecea095f19b49553d26ab9b082e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19ad9861c17330ee552a1043d9ea513dc1bf24d1d46a924b61ef346a0f488dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigEditListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigEditListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigEditListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375cb3f24c195c7464315ccb132dce8aa3bdcdab4be5d5949b59aeeaeceafe60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigEditListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEditListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c99ee2264355349cf691f8dedc78c492e37adc2d56b345690a206b2fce8bb33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b381d841ef0ea9fe143dc39f95cfcc42f8f713171c50cb63b01aa8b0fbf1fc0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e93c8e1412201e7fd55cf0c36e4f56ce500661e0fbabf31b1b3a095ddccba3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a685fb615b8cda05d9afa29693bf51790593464d30a0893bfb843c7feed6a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigEditListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigEditListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigEditListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22564f932fe49a927198a23d4974553522a68a75ec8f849402a2beea9139a65e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreams",
    jsii_struct_bases=[],
    name_mapping={
        "audio_stream": "audioStream",
        "key": "key",
        "video_stream": "videoStream",
    },
)
class TranscoderJobConfigElementaryStreams:
    def __init__(
        self,
        *,
        audio_stream: typing.Optional[typing.Union["TranscoderJobConfigElementaryStreamsAudioStream", typing.Dict[builtins.str, typing.Any]]] = None,
        key: typing.Optional[builtins.str] = None,
        video_stream: typing.Optional[typing.Union["TranscoderJobConfigElementaryStreamsVideoStream", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_stream: audio_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#audio_stream TranscoderJob#audio_stream}
        :param key: A unique key for this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#key TranscoderJob#key}
        :param video_stream: video_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#video_stream TranscoderJob#video_stream}
        '''
        if isinstance(audio_stream, dict):
            audio_stream = TranscoderJobConfigElementaryStreamsAudioStream(**audio_stream)
        if isinstance(video_stream, dict):
            video_stream = TranscoderJobConfigElementaryStreamsVideoStream(**video_stream)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc6078443d03b78b04a4c85bfbd2aa8e7423025189fc57bad2dc1af34aa47f5)
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
    ) -> typing.Optional["TranscoderJobConfigElementaryStreamsAudioStream"]:
        '''audio_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#audio_stream TranscoderJob#audio_stream}
        '''
        result = self._values.get("audio_stream")
        return typing.cast(typing.Optional["TranscoderJobConfigElementaryStreamsAudioStream"], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#key TranscoderJob#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def video_stream(
        self,
    ) -> typing.Optional["TranscoderJobConfigElementaryStreamsVideoStream"]:
        '''video_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#video_stream TranscoderJob#video_stream}
        '''
        result = self._values.get("video_stream")
        return typing.cast(typing.Optional["TranscoderJobConfigElementaryStreamsVideoStream"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigElementaryStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsAudioStream",
    jsii_struct_bases=[],
    name_mapping={
        "bitrate_bps": "bitrateBps",
        "channel_count": "channelCount",
        "channel_layout": "channelLayout",
        "codec": "codec",
        "sample_rate_hertz": "sampleRateHertz",
    },
)
class TranscoderJobConfigElementaryStreamsAudioStream:
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
        :param bitrate_bps: Audio bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#bitrate_bps TranscoderJob#bitrate_bps}
        :param channel_count: Number of audio channels. The default is '2'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#channel_count TranscoderJob#channel_count}
        :param channel_layout: A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#channel_layout TranscoderJob#channel_layout}
        :param codec: The codec for this audio stream. The default is 'aac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#codec TranscoderJob#codec}
        :param sample_rate_hertz: The audio sample rate in Hertz. The default is '48000'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#sample_rate_hertz TranscoderJob#sample_rate_hertz}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1ba5830564d2e0063e71526b5a30684961c0ce6e00ca2ae053170ed8757ffb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#bitrate_bps TranscoderJob#bitrate_bps}
        '''
        result = self._values.get("bitrate_bps")
        assert result is not None, "Required property 'bitrate_bps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def channel_count(self) -> typing.Optional[jsii.Number]:
        '''Number of audio channels. The default is '2'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#channel_count TranscoderJob#channel_count}
        '''
        result = self._values.get("channel_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def channel_layout(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#channel_layout TranscoderJob#channel_layout}
        '''
        result = self._values.get("channel_layout")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def codec(self) -> typing.Optional[builtins.str]:
        '''The codec for this audio stream. The default is 'aac'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#codec TranscoderJob#codec}
        '''
        result = self._values.get("codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate_hertz(self) -> typing.Optional[jsii.Number]:
        '''The audio sample rate in Hertz. The default is '48000'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#sample_rate_hertz TranscoderJob#sample_rate_hertz}
        '''
        result = self._values.get("sample_rate_hertz")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigElementaryStreamsAudioStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigElementaryStreamsAudioStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsAudioStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b725d02692cd1f32b0cd6403514fd46126483b1e0486b0b5a332af9c8fde6b17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b12cfc1369cfc88920ae3c238f72c357691a6f45dd8ca5e72e6e2853a50421d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitrateBps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelCount")
    def channel_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "channelCount"))

    @channel_count.setter
    def channel_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12f6a0c257d369a602f1449ebc78f9278b0a3a84b6b5697ad3680e76f6576a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelLayout")
    def channel_layout(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "channelLayout"))

    @channel_layout.setter
    def channel_layout(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3be5018ebbb23377dfd3528a405cf01ad62fd7aa7ec04315d552ccfb4c7b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelLayout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codec")
    def codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codec"))

    @codec.setter
    def codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0e274b97604a00bb51f2f68f4ff6d2f33a437872533b1b2c9758a736c8d00d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRateHertz")
    def sample_rate_hertz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRateHertz"))

    @sample_rate_hertz.setter
    def sample_rate_hertz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b95358b48b1db40abf61b46e4d6369d5356b233b0d7474ac91041b3431168d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRateHertz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigElementaryStreamsAudioStream]:
        return typing.cast(typing.Optional[TranscoderJobConfigElementaryStreamsAudioStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigElementaryStreamsAudioStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc22565aca643bff13da0ea6b25101a9e5d2aa0ea863b8ad0362d311fe13235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigElementaryStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__378c124985075997fa9f72b8ef08c9b3736e6b0fe8a4090a60bb2efa044af1da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobConfigElementaryStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bda3212ae27df01e558b7f3bcdc3b41a6af247f7f4dda5ea8f0848eb47ceeed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigElementaryStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205cbc43099825dbef58fae61313b43adbb161af6249418641910a783f3f9c62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1a811ad663e1048d5f757f7a0749f8e3100d62bf90edbddcc7e9566569f9489)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8542aab0e448bf1363b964f888d2971236303db9bd3c224c33b09726df079d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigElementaryStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigElementaryStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigElementaryStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6814f3372da84a3e3095ec1553792990a42e951e339030c42347aa42306f05c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigElementaryStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11bcae4df33c04cca14a68971d0c57d99135bc88f3a65d04bd6a67365c2f94b0)
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
        :param bitrate_bps: Audio bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#bitrate_bps TranscoderJob#bitrate_bps}
        :param channel_count: Number of audio channels. The default is '2'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#channel_count TranscoderJob#channel_count}
        :param channel_layout: A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#channel_layout TranscoderJob#channel_layout}
        :param codec: The codec for this audio stream. The default is 'aac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#codec TranscoderJob#codec}
        :param sample_rate_hertz: The audio sample rate in Hertz. The default is '48000'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#sample_rate_hertz TranscoderJob#sample_rate_hertz}
        '''
        value = TranscoderJobConfigElementaryStreamsAudioStream(
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
        h264: typing.Optional[typing.Union["TranscoderJobConfigElementaryStreamsVideoStreamH264", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param h264: h264 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#h264 TranscoderJob#h264}
        '''
        value = TranscoderJobConfigElementaryStreamsVideoStream(h264=h264)

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
    ) -> TranscoderJobConfigElementaryStreamsAudioStreamOutputReference:
        return typing.cast(TranscoderJobConfigElementaryStreamsAudioStreamOutputReference, jsii.get(self, "audioStream"))

    @builtins.property
    @jsii.member(jsii_name="videoStream")
    def video_stream(
        self,
    ) -> "TranscoderJobConfigElementaryStreamsVideoStreamOutputReference":
        return typing.cast("TranscoderJobConfigElementaryStreamsVideoStreamOutputReference", jsii.get(self, "videoStream"))

    @builtins.property
    @jsii.member(jsii_name="audioStreamInput")
    def audio_stream_input(
        self,
    ) -> typing.Optional[TranscoderJobConfigElementaryStreamsAudioStream]:
        return typing.cast(typing.Optional[TranscoderJobConfigElementaryStreamsAudioStream], jsii.get(self, "audioStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="videoStreamInput")
    def video_stream_input(
        self,
    ) -> typing.Optional["TranscoderJobConfigElementaryStreamsVideoStream"]:
        return typing.cast(typing.Optional["TranscoderJobConfigElementaryStreamsVideoStream"], jsii.get(self, "videoStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd12d35f730a67d50abf143dc31a0a1140ed99789da87c55229da058c213163a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigElementaryStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigElementaryStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigElementaryStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352dab74637792fc248ad6bcdd17f86c5914070539badb0353535e3ded5d3d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsVideoStream",
    jsii_struct_bases=[],
    name_mapping={"h264": "h264"},
)
class TranscoderJobConfigElementaryStreamsVideoStream:
    def __init__(
        self,
        *,
        h264: typing.Optional[typing.Union["TranscoderJobConfigElementaryStreamsVideoStreamH264", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param h264: h264 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#h264 TranscoderJob#h264}
        '''
        if isinstance(h264, dict):
            h264 = TranscoderJobConfigElementaryStreamsVideoStreamH264(**h264)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738e6f6a48ea203f4501a0269cf7bbe9ecbfd393d19dac3b96859c90abb2a84d)
            check_type(argname="argument h264", value=h264, expected_type=type_hints["h264"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if h264 is not None:
            self._values["h264"] = h264

    @builtins.property
    def h264(
        self,
    ) -> typing.Optional["TranscoderJobConfigElementaryStreamsVideoStreamH264"]:
        '''h264 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#h264 TranscoderJob#h264}
        '''
        result = self._values.get("h264")
        return typing.cast(typing.Optional["TranscoderJobConfigElementaryStreamsVideoStreamH264"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigElementaryStreamsVideoStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsVideoStreamH264",
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
class TranscoderJobConfigElementaryStreamsVideoStreamH264:
    def __init__(
        self,
        *,
        bitrate_bps: jsii.Number,
        frame_rate: jsii.Number,
        crf_level: typing.Optional[jsii.Number] = None,
        entropy_coder: typing.Optional[builtins.str] = None,
        gop_duration: typing.Optional[builtins.str] = None,
        height_pixels: typing.Optional[jsii.Number] = None,
        hlg: typing.Optional[typing.Union["TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg", typing.Dict[builtins.str, typing.Any]]] = None,
        pixel_format: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        rate_control_mode: typing.Optional[builtins.str] = None,
        sdr: typing.Optional[typing.Union["TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr", typing.Dict[builtins.str, typing.Any]]] = None,
        vbv_fullness_bits: typing.Optional[jsii.Number] = None,
        vbv_size_bits: typing.Optional[jsii.Number] = None,
        width_pixels: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: The video bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#bitrate_bps TranscoderJob#bitrate_bps}
        :param frame_rate: The target video frame rate in frames per second (FPS). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#frame_rate TranscoderJob#frame_rate}
        :param crf_level: Target CRF level. The default is '21'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#crf_level TranscoderJob#crf_level}
        :param entropy_coder: The entropy coder to use. The default is 'cabac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#entropy_coder TranscoderJob#entropy_coder}
        :param gop_duration: Select the GOP size based on the specified duration. The default is '3s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#gop_duration TranscoderJob#gop_duration}
        :param height_pixels: The height of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#height_pixels TranscoderJob#height_pixels}
        :param hlg: hlg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#hlg TranscoderJob#hlg}
        :param pixel_format: Pixel format to use. The default is 'yuv420p'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#pixel_format TranscoderJob#pixel_format}
        :param preset: Enforces the specified codec preset. The default is 'veryfast'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#preset TranscoderJob#preset}
        :param profile: Enforces the specified codec profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#profile TranscoderJob#profile}
        :param rate_control_mode: Specify the mode. The default is 'vbr'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#rate_control_mode TranscoderJob#rate_control_mode}
        :param sdr: sdr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#sdr TranscoderJob#sdr}
        :param vbv_fullness_bits: Initial fullness of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#vbv_fullness_bits TranscoderJob#vbv_fullness_bits}
        :param vbv_size_bits: Size of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#vbv_size_bits TranscoderJob#vbv_size_bits}
        :param width_pixels: The width of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#width_pixels TranscoderJob#width_pixels}
        '''
        if isinstance(hlg, dict):
            hlg = TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg(**hlg)
        if isinstance(sdr, dict):
            sdr = TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr(**sdr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599b679c19e20646a42263620b47a5e6890fd19bcaec3c147c9d9e7b6d708daa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#bitrate_bps TranscoderJob#bitrate_bps}
        '''
        result = self._values.get("bitrate_bps")
        assert result is not None, "Required property 'bitrate_bps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frame_rate(self) -> jsii.Number:
        '''The target video frame rate in frames per second (FPS).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#frame_rate TranscoderJob#frame_rate}
        '''
        result = self._values.get("frame_rate")
        assert result is not None, "Required property 'frame_rate' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def crf_level(self) -> typing.Optional[jsii.Number]:
        '''Target CRF level. The default is '21'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#crf_level TranscoderJob#crf_level}
        '''
        result = self._values.get("crf_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def entropy_coder(self) -> typing.Optional[builtins.str]:
        '''The entropy coder to use. The default is 'cabac'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#entropy_coder TranscoderJob#entropy_coder}
        '''
        result = self._values.get("entropy_coder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gop_duration(self) -> typing.Optional[builtins.str]:
        '''Select the GOP size based on the specified duration. The default is '3s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#gop_duration TranscoderJob#gop_duration}
        '''
        result = self._values.get("gop_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def height_pixels(self) -> typing.Optional[jsii.Number]:
        '''The height of the video in pixels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#height_pixels TranscoderJob#height_pixels}
        '''
        result = self._values.get("height_pixels")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hlg(
        self,
    ) -> typing.Optional["TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg"]:
        '''hlg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#hlg TranscoderJob#hlg}
        '''
        result = self._values.get("hlg")
        return typing.cast(typing.Optional["TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg"], result)

    @builtins.property
    def pixel_format(self) -> typing.Optional[builtins.str]:
        '''Pixel format to use. The default is 'yuv420p'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#pixel_format TranscoderJob#pixel_format}
        '''
        result = self._values.get("pixel_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preset(self) -> typing.Optional[builtins.str]:
        '''Enforces the specified codec preset. The default is 'veryfast'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#preset TranscoderJob#preset}
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Enforces the specified codec profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#profile TranscoderJob#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_control_mode(self) -> typing.Optional[builtins.str]:
        '''Specify the mode. The default is 'vbr'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#rate_control_mode TranscoderJob#rate_control_mode}
        '''
        result = self._values.get("rate_control_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sdr(
        self,
    ) -> typing.Optional["TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr"]:
        '''sdr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#sdr TranscoderJob#sdr}
        '''
        result = self._values.get("sdr")
        return typing.cast(typing.Optional["TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr"], result)

    @builtins.property
    def vbv_fullness_bits(self) -> typing.Optional[jsii.Number]:
        '''Initial fullness of the Video Buffering Verifier (VBV) buffer in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#vbv_fullness_bits TranscoderJob#vbv_fullness_bits}
        '''
        result = self._values.get("vbv_fullness_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vbv_size_bits(self) -> typing.Optional[jsii.Number]:
        '''Size of the Video Buffering Verifier (VBV) buffer in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#vbv_size_bits TranscoderJob#vbv_size_bits}
        '''
        result = self._values.get("vbv_size_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def width_pixels(self) -> typing.Optional[jsii.Number]:
        '''The width of the video in pixels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#width_pixels TranscoderJob#width_pixels}
        '''
        result = self._values.get("width_pixels")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigElementaryStreamsVideoStreamH264(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdf31f804345c37d5cfc7a30ef66a7026ca915814dd6878e130bc2b6ecfe98d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg]:
        return typing.cast(typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8a44175d6c32b4edc6467b4d76f640f1e7f9c8a4453a17bb770e8fd9944d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__018dc2e266fd40eb398cae7d8f68c794d8ae7f2c095771ab4b8c3ced72e057fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHlg")
    def put_hlg(self) -> None:
        value = TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg()

        return typing.cast(None, jsii.invoke(self, "putHlg", [value]))

    @jsii.member(jsii_name="putSdr")
    def put_sdr(self) -> None:
        value = TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr()

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
    ) -> TranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference:
        return typing.cast(TranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference, jsii.get(self, "hlg"))

    @builtins.property
    @jsii.member(jsii_name="sdr")
    def sdr(
        self,
    ) -> "TranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference":
        return typing.cast("TranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference", jsii.get(self, "sdr"))

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
    ) -> typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg]:
        return typing.cast(typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg], jsii.get(self, "hlgInput"))

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
    ) -> typing.Optional["TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr"]:
        return typing.cast(typing.Optional["TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr"], jsii.get(self, "sdrInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a19fb8382a779f2c5459799830d5a277ef36c38ac4ec6ef70b37f831e37368fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitrateBps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crfLevel")
    def crf_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "crfLevel"))

    @crf_level.setter
    def crf_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48b0fcd4f175c3907ca271061d0ee1cb6dc5cb06baf7e2bf047eb73db4a093a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crfLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entropyCoder")
    def entropy_coder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entropyCoder"))

    @entropy_coder.setter
    def entropy_coder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028f235c20cb829306ed68ca540131007358d6e59e063c4125b55d23bdb5d144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entropyCoder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frameRate")
    def frame_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frameRate"))

    @frame_rate.setter
    def frame_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b270f18b529bd0434bd0b7f9f98411645c6eaee0ea3652c17cd66eaf47be44e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gopDuration")
    def gop_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gopDuration"))

    @gop_duration.setter
    def gop_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1de17c905088c59e6eba782b810c0efed3ce899ecfb8225edad79ac6db64ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gopDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="heightPixels")
    def height_pixels(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "heightPixels"))

    @height_pixels.setter
    def height_pixels(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc505e931e787f5ddef944204026eb02aa8ddd351af7a60df157ffab81c01d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "heightPixels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pixelFormat")
    def pixel_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pixelFormat"))

    @pixel_format.setter
    def pixel_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79463aea52344bfef79efb41ec63de1b0a89674e994b1a6f86f1edba2f941a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pixelFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preset")
    def preset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preset"))

    @preset.setter
    def preset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10c3f191c5416cf7eebca02f797086601d6de5d984161de465cbffcf974421d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79242772ae03ab48ed6b8b4ede06bc7ded16e77ebac4756296815c6e35d2434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rateControlMode")
    def rate_control_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rateControlMode"))

    @rate_control_mode.setter
    def rate_control_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b4bf5bb7f478658bfbe12a5c914fc0d1b6eb743829e48c426305300806f767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateControlMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vbvFullnessBits")
    def vbv_fullness_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vbvFullnessBits"))

    @vbv_fullness_bits.setter
    def vbv_fullness_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402ad0894cce4e0a8044f07bf7caf3170eb279ba653f0b909c219c55d9554c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vbvFullnessBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vbvSizeBits")
    def vbv_size_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vbvSizeBits"))

    @vbv_size_bits.setter
    def vbv_size_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a240e60e62ddb7f878d7d406194e426f8bc4af2ae3bda348701a38b696d04ef9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vbvSizeBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="widthPixels")
    def width_pixels(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "widthPixels"))

    @width_pixels.setter
    def width_pixels(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85bae5effac4b8f6663cfb66ca55b8b487c8529001fab7a78ecf33a6b266dcab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "widthPixels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264]:
        return typing.cast(typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f242f9cc60aaa69841e65aad4e69a2f311a95ff14c520ae33c9ff30fcad96889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1eb43436ed32eb27eaf04020ac8ba95c8a448b8f88010aa757d1da80834a70c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr]:
        return typing.cast(typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a471cb644f1ca2b6010ae3f6e1bc43da9e6074ab890b5510551a9c08c05f565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigElementaryStreamsVideoStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigElementaryStreamsVideoStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77367f26c75867c2c8695108b72af39474a10a1174e1a39b7b989b6bc4401279)
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
        hlg: typing.Optional[typing.Union[TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg, typing.Dict[builtins.str, typing.Any]]] = None,
        pixel_format: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        rate_control_mode: typing.Optional[builtins.str] = None,
        sdr: typing.Optional[typing.Union[TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr, typing.Dict[builtins.str, typing.Any]]] = None,
        vbv_fullness_bits: typing.Optional[jsii.Number] = None,
        vbv_size_bits: typing.Optional[jsii.Number] = None,
        width_pixels: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: The video bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#bitrate_bps TranscoderJob#bitrate_bps}
        :param frame_rate: The target video frame rate in frames per second (FPS). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#frame_rate TranscoderJob#frame_rate}
        :param crf_level: Target CRF level. The default is '21'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#crf_level TranscoderJob#crf_level}
        :param entropy_coder: The entropy coder to use. The default is 'cabac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#entropy_coder TranscoderJob#entropy_coder}
        :param gop_duration: Select the GOP size based on the specified duration. The default is '3s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#gop_duration TranscoderJob#gop_duration}
        :param height_pixels: The height of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#height_pixels TranscoderJob#height_pixels}
        :param hlg: hlg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#hlg TranscoderJob#hlg}
        :param pixel_format: Pixel format to use. The default is 'yuv420p'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#pixel_format TranscoderJob#pixel_format}
        :param preset: Enforces the specified codec preset. The default is 'veryfast'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#preset TranscoderJob#preset}
        :param profile: Enforces the specified codec profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#profile TranscoderJob#profile}
        :param rate_control_mode: Specify the mode. The default is 'vbr'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#rate_control_mode TranscoderJob#rate_control_mode}
        :param sdr: sdr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#sdr TranscoderJob#sdr}
        :param vbv_fullness_bits: Initial fullness of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#vbv_fullness_bits TranscoderJob#vbv_fullness_bits}
        :param vbv_size_bits: Size of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#vbv_size_bits TranscoderJob#vbv_size_bits}
        :param width_pixels: The width of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#width_pixels TranscoderJob#width_pixels}
        '''
        value = TranscoderJobConfigElementaryStreamsVideoStreamH264(
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
    ) -> TranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference:
        return typing.cast(TranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference, jsii.get(self, "h264"))

    @builtins.property
    @jsii.member(jsii_name="h264Input")
    def h264_input(
        self,
    ) -> typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264]:
        return typing.cast(typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264], jsii.get(self, "h264Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigElementaryStreamsVideoStream]:
        return typing.cast(typing.Optional[TranscoderJobConfigElementaryStreamsVideoStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigElementaryStreamsVideoStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc6a2054ff735a1dd7f573f73705ee62baedded9858f9dbc586608512ba8113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptions",
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
class TranscoderJobConfigEncryptions:
    def __init__(
        self,
        *,
        id: builtins.str,
        aes128: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsAes128", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_systems: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsDrmSystems", typing.Dict[builtins.str, typing.Any]]] = None,
        mpeg_cenc: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsMpegCenc", typing.Dict[builtins.str, typing.Any]]] = None,
        sample_aes: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsSampleAes", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_manager_key_source: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsSecretManagerKeySource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Identifier for this set of encryption options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#id TranscoderJob#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param aes128: aes128 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#aes128 TranscoderJob#aes128}
        :param drm_systems: drm_systems block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#drm_systems TranscoderJob#drm_systems}
        :param mpeg_cenc: mpeg_cenc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#mpeg_cenc TranscoderJob#mpeg_cenc}
        :param sample_aes: sample_aes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#sample_aes TranscoderJob#sample_aes}
        :param secret_manager_key_source: secret_manager_key_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#secret_manager_key_source TranscoderJob#secret_manager_key_source}
        '''
        if isinstance(aes128, dict):
            aes128 = TranscoderJobConfigEncryptionsAes128(**aes128)
        if isinstance(drm_systems, dict):
            drm_systems = TranscoderJobConfigEncryptionsDrmSystems(**drm_systems)
        if isinstance(mpeg_cenc, dict):
            mpeg_cenc = TranscoderJobConfigEncryptionsMpegCenc(**mpeg_cenc)
        if isinstance(sample_aes, dict):
            sample_aes = TranscoderJobConfigEncryptionsSampleAes(**sample_aes)
        if isinstance(secret_manager_key_source, dict):
            secret_manager_key_source = TranscoderJobConfigEncryptionsSecretManagerKeySource(**secret_manager_key_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b1bef622684aef3ddc3b2430fa49ee68bce6641a5cd87f19a7d4a99bad3644d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#id TranscoderJob#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aes128(self) -> typing.Optional["TranscoderJobConfigEncryptionsAes128"]:
        '''aes128 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#aes128 TranscoderJob#aes128}
        '''
        result = self._values.get("aes128")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsAes128"], result)

    @builtins.property
    def drm_systems(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsDrmSystems"]:
        '''drm_systems block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#drm_systems TranscoderJob#drm_systems}
        '''
        result = self._values.get("drm_systems")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsDrmSystems"], result)

    @builtins.property
    def mpeg_cenc(self) -> typing.Optional["TranscoderJobConfigEncryptionsMpegCenc"]:
        '''mpeg_cenc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#mpeg_cenc TranscoderJob#mpeg_cenc}
        '''
        result = self._values.get("mpeg_cenc")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsMpegCenc"], result)

    @builtins.property
    def sample_aes(self) -> typing.Optional["TranscoderJobConfigEncryptionsSampleAes"]:
        '''sample_aes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#sample_aes TranscoderJob#sample_aes}
        '''
        result = self._values.get("sample_aes")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsSampleAes"], result)

    @builtins.property
    def secret_manager_key_source(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsSecretManagerKeySource"]:
        '''secret_manager_key_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#secret_manager_key_source TranscoderJob#secret_manager_key_source}
        '''
        result = self._values.get("secret_manager_key_source")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsSecretManagerKeySource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsAes128",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobConfigEncryptionsAes128:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsAes128(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEncryptionsAes128OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsAes128OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d4f704d0295a4027cee658b0ed4791e123b72d44a2f73493d13d16a0e9ed6f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TranscoderJobConfigEncryptionsAes128]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsAes128], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsAes128],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4ac489dbd636d339b273be6ceacfa1182a9ff902852cac4019bf360f79954b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystems",
    jsii_struct_bases=[],
    name_mapping={
        "clearkey": "clearkey",
        "fairplay": "fairplay",
        "playready": "playready",
        "widevine": "widevine",
    },
)
class TranscoderJobConfigEncryptionsDrmSystems:
    def __init__(
        self,
        *,
        clearkey: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsDrmSystemsClearkey", typing.Dict[builtins.str, typing.Any]]] = None,
        fairplay: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsDrmSystemsFairplay", typing.Dict[builtins.str, typing.Any]]] = None,
        playready: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsDrmSystemsPlayready", typing.Dict[builtins.str, typing.Any]]] = None,
        widevine: typing.Optional[typing.Union["TranscoderJobConfigEncryptionsDrmSystemsWidevine", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clearkey: clearkey block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#clearkey TranscoderJob#clearkey}
        :param fairplay: fairplay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#fairplay TranscoderJob#fairplay}
        :param playready: playready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#playready TranscoderJob#playready}
        :param widevine: widevine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#widevine TranscoderJob#widevine}
        '''
        if isinstance(clearkey, dict):
            clearkey = TranscoderJobConfigEncryptionsDrmSystemsClearkey(**clearkey)
        if isinstance(fairplay, dict):
            fairplay = TranscoderJobConfigEncryptionsDrmSystemsFairplay(**fairplay)
        if isinstance(playready, dict):
            playready = TranscoderJobConfigEncryptionsDrmSystemsPlayready(**playready)
        if isinstance(widevine, dict):
            widevine = TranscoderJobConfigEncryptionsDrmSystemsWidevine(**widevine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b163236852b495f2ee7a47471c4c19ef6216ee5ddecf462aed65a89f5f902838)
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
    ) -> typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsClearkey"]:
        '''clearkey block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#clearkey TranscoderJob#clearkey}
        '''
        result = self._values.get("clearkey")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsClearkey"], result)

    @builtins.property
    def fairplay(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsFairplay"]:
        '''fairplay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#fairplay TranscoderJob#fairplay}
        '''
        result = self._values.get("fairplay")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsFairplay"], result)

    @builtins.property
    def playready(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsPlayready"]:
        '''playready block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#playready TranscoderJob#playready}
        '''
        result = self._values.get("playready")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsPlayready"], result)

    @builtins.property
    def widevine(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsWidevine"]:
        '''widevine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#widevine TranscoderJob#widevine}
        '''
        result = self._values.get("widevine")
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsWidevine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsDrmSystems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsClearkey",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobConfigEncryptionsDrmSystemsClearkey:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsDrmSystemsClearkey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__719497a194a592ad1fe66ace8f05889f4fa4a47f18f019d891a8e185626bf8de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsClearkey]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsClearkey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsClearkey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17346df479404674ef8813d72db7380bc55d6209526134bbbe21c875ff2eb72a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsFairplay",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobConfigEncryptionsDrmSystemsFairplay:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsDrmSystemsFairplay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60e8ece8b67785998712f1f6336a2e62b89ad4a6425589910ef9834351e783be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsFairplay]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsFairplay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsFairplay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cfdc7ea90b7ce5f6b563b0d70a9d2a74d4c0a3d587a0dd62506d18d0fbc2b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigEncryptionsDrmSystemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef7553f05f8fed5a6e02f5a080a410ec615808a0d7ff3ad2c18f83c639b717f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClearkey")
    def put_clearkey(self) -> None:
        value = TranscoderJobConfigEncryptionsDrmSystemsClearkey()

        return typing.cast(None, jsii.invoke(self, "putClearkey", [value]))

    @jsii.member(jsii_name="putFairplay")
    def put_fairplay(self) -> None:
        value = TranscoderJobConfigEncryptionsDrmSystemsFairplay()

        return typing.cast(None, jsii.invoke(self, "putFairplay", [value]))

    @jsii.member(jsii_name="putPlayready")
    def put_playready(self) -> None:
        value = TranscoderJobConfigEncryptionsDrmSystemsPlayready()

        return typing.cast(None, jsii.invoke(self, "putPlayready", [value]))

    @jsii.member(jsii_name="putWidevine")
    def put_widevine(self) -> None:
        value = TranscoderJobConfigEncryptionsDrmSystemsWidevine()

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
    ) -> TranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference:
        return typing.cast(TranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference, jsii.get(self, "clearkey"))

    @builtins.property
    @jsii.member(jsii_name="fairplay")
    def fairplay(
        self,
    ) -> TranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference:
        return typing.cast(TranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference, jsii.get(self, "fairplay"))

    @builtins.property
    @jsii.member(jsii_name="playready")
    def playready(
        self,
    ) -> "TranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference":
        return typing.cast("TranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference", jsii.get(self, "playready"))

    @builtins.property
    @jsii.member(jsii_name="widevine")
    def widevine(
        self,
    ) -> "TranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference":
        return typing.cast("TranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference", jsii.get(self, "widevine"))

    @builtins.property
    @jsii.member(jsii_name="clearkeyInput")
    def clearkey_input(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsClearkey]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsClearkey], jsii.get(self, "clearkeyInput"))

    @builtins.property
    @jsii.member(jsii_name="fairplayInput")
    def fairplay_input(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsFairplay]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsFairplay], jsii.get(self, "fairplayInput"))

    @builtins.property
    @jsii.member(jsii_name="playreadyInput")
    def playready_input(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsPlayready"]:
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsPlayready"], jsii.get(self, "playreadyInput"))

    @builtins.property
    @jsii.member(jsii_name="widevineInput")
    def widevine_input(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsWidevine"]:
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsDrmSystemsWidevine"], jsii.get(self, "widevineInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsDrmSystems]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsDrmSystems], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystems],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af2a614aa23668d9a2f4ab4ae72c280ef98b2cb8f4cc28402f394289c7906cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsPlayready",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobConfigEncryptionsDrmSystemsPlayready:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsDrmSystemsPlayready(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d25735a45ff92423a1710e418ca256980d1a9397c5f6256969610bc2dcc94d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsPlayready]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsPlayready], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsPlayready],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5159ad126578c53c7e345fbde7e4a9a835df2d966de0a42cef71889fe3847616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsWidevine",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobConfigEncryptionsDrmSystemsWidevine:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsDrmSystemsWidevine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__351759ee31e1469c19124fba7d8c3d58b89e8bff6da20c22e405bdaeca5384c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsWidevine]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsWidevine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsWidevine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de6d3566beae66d8df7870c50a1a97d39f94e4e517c3236afe3342b35cc6712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigEncryptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11ac948e5cca7831a4a670a754d0293af3a2873c3ae75e1d4676d629a123429a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobConfigEncryptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f71e48cda8428f8f26fab17e7bed005dfef8c663a08627697c57894a629ba72)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigEncryptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da3def669a5ce0c80e9517f123664595d8b21499dbb649ba2af5aa976d89030)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd5a0447041a55f0028eb38e03f1f06185e5e01e431fdeb52cd8543cd1822918)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec583aeb9e5724fc1c5e5fd4a6aa2b3144adf4bd5bc9d66d0b1425bef6e6dac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigEncryptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigEncryptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigEncryptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b7b626a5d23179cbfd35835c3c8a63592fd76e7d5699cb0f5395ac3a5480d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsMpegCenc",
    jsii_struct_bases=[],
    name_mapping={"scheme": "scheme"},
)
class TranscoderJobConfigEncryptionsMpegCenc:
    def __init__(self, *, scheme: builtins.str) -> None:
        '''
        :param scheme: Specify the encryption scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#scheme TranscoderJob#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622d33adbf2cd6f27cfc07dae7c8301ac875845434fd5af6d704b6a96f7ef5c9)
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scheme": scheme,
        }

    @builtins.property
    def scheme(self) -> builtins.str:
        '''Specify the encryption scheme.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#scheme TranscoderJob#scheme}
        '''
        result = self._values.get("scheme")
        assert result is not None, "Required property 'scheme' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsMpegCenc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEncryptionsMpegCencOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsMpegCencOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d60f273bd7ecb4c9aecf7ae9802a575391481bb1558aca482327be847e807ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa2b0ba2ee8017aba02d5a1f8e6f81b1723ff8c3c8c8cacde55ff083a3e486d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TranscoderJobConfigEncryptionsMpegCenc]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsMpegCenc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsMpegCenc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8a2571ac9a24e420772d706aa8828edabbd88f318caf0c8579ee45c5bbc96e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigEncryptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e64f2e7b9af9802f185c7521aa782b9f00d51e2bcaa27ceef64772a69c08ba3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAes128")
    def put_aes128(self) -> None:
        value = TranscoderJobConfigEncryptionsAes128()

        return typing.cast(None, jsii.invoke(self, "putAes128", [value]))

    @jsii.member(jsii_name="putDrmSystems")
    def put_drm_systems(
        self,
        *,
        clearkey: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystemsClearkey, typing.Dict[builtins.str, typing.Any]]] = None,
        fairplay: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystemsFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
        playready: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystemsPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
        widevine: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystemsWidevine, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clearkey: clearkey block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#clearkey TranscoderJob#clearkey}
        :param fairplay: fairplay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#fairplay TranscoderJob#fairplay}
        :param playready: playready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#playready TranscoderJob#playready}
        :param widevine: widevine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#widevine TranscoderJob#widevine}
        '''
        value = TranscoderJobConfigEncryptionsDrmSystems(
            clearkey=clearkey,
            fairplay=fairplay,
            playready=playready,
            widevine=widevine,
        )

        return typing.cast(None, jsii.invoke(self, "putDrmSystems", [value]))

    @jsii.member(jsii_name="putMpegCenc")
    def put_mpeg_cenc(self, *, scheme: builtins.str) -> None:
        '''
        :param scheme: Specify the encryption scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#scheme TranscoderJob#scheme}
        '''
        value = TranscoderJobConfigEncryptionsMpegCenc(scheme=scheme)

        return typing.cast(None, jsii.invoke(self, "putMpegCenc", [value]))

    @jsii.member(jsii_name="putSampleAes")
    def put_sample_aes(self) -> None:
        value = TranscoderJobConfigEncryptionsSampleAes()

        return typing.cast(None, jsii.invoke(self, "putSampleAes", [value]))

    @jsii.member(jsii_name="putSecretManagerKeySource")
    def put_secret_manager_key_source(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#secret_version TranscoderJob#secret_version}
        '''
        value = TranscoderJobConfigEncryptionsSecretManagerKeySource(
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
    def aes128(self) -> TranscoderJobConfigEncryptionsAes128OutputReference:
        return typing.cast(TranscoderJobConfigEncryptionsAes128OutputReference, jsii.get(self, "aes128"))

    @builtins.property
    @jsii.member(jsii_name="drmSystems")
    def drm_systems(self) -> TranscoderJobConfigEncryptionsDrmSystemsOutputReference:
        return typing.cast(TranscoderJobConfigEncryptionsDrmSystemsOutputReference, jsii.get(self, "drmSystems"))

    @builtins.property
    @jsii.member(jsii_name="mpegCenc")
    def mpeg_cenc(self) -> TranscoderJobConfigEncryptionsMpegCencOutputReference:
        return typing.cast(TranscoderJobConfigEncryptionsMpegCencOutputReference, jsii.get(self, "mpegCenc"))

    @builtins.property
    @jsii.member(jsii_name="sampleAes")
    def sample_aes(self) -> "TranscoderJobConfigEncryptionsSampleAesOutputReference":
        return typing.cast("TranscoderJobConfigEncryptionsSampleAesOutputReference", jsii.get(self, "sampleAes"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerKeySource")
    def secret_manager_key_source(
        self,
    ) -> "TranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference":
        return typing.cast("TranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference", jsii.get(self, "secretManagerKeySource"))

    @builtins.property
    @jsii.member(jsii_name="aes128Input")
    def aes128_input(self) -> typing.Optional[TranscoderJobConfigEncryptionsAes128]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsAes128], jsii.get(self, "aes128Input"))

    @builtins.property
    @jsii.member(jsii_name="drmSystemsInput")
    def drm_systems_input(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsDrmSystems]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsDrmSystems], jsii.get(self, "drmSystemsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mpegCencInput")
    def mpeg_cenc_input(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsMpegCenc]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsMpegCenc], jsii.get(self, "mpegCencInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleAesInput")
    def sample_aes_input(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsSampleAes"]:
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsSampleAes"], jsii.get(self, "sampleAesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerKeySourceInput")
    def secret_manager_key_source_input(
        self,
    ) -> typing.Optional["TranscoderJobConfigEncryptionsSecretManagerKeySource"]:
        return typing.cast(typing.Optional["TranscoderJobConfigEncryptionsSecretManagerKeySource"], jsii.get(self, "secretManagerKeySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99488a56cee5589cb605f0ff89c928791a2bd5eca48b25049c56761607947c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigEncryptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigEncryptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigEncryptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a959cbb7364e25302570d2a0ea9cca707ccfdddf777c84a8f90705e8b6e0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsSampleAes",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobConfigEncryptionsSampleAes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsSampleAes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEncryptionsSampleAesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsSampleAesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2071a5e6fd405f37e1eea85f78c9a12866a28ff7a7595ce9a15a0e0cfcb51d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsSampleAes]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsSampleAes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsSampleAes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b61d2cb4d769b805955ddae707235b9e6adf6a9275c283dbb290e4027165734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsSecretManagerKeySource",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class TranscoderJobConfigEncryptionsSecretManagerKeySource:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#secret_version TranscoderJob#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bde16d20d71e8787150884f9bc9680d5bd4a3d19ed6b6df2ca5a3d581dde172)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#secret_version TranscoderJob#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigEncryptionsSecretManagerKeySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aad2a6d70f43617cd732b32bc48d36dfa28f7dd4e50d8b902f5f90dfa3852c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48e8002218c38fe114c5555f3cf998e035d4bd90ee9641e94d2e415c29445be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigEncryptionsSecretManagerKeySource]:
        return typing.cast(typing.Optional[TranscoderJobConfigEncryptionsSecretManagerKeySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigEncryptionsSecretManagerKeySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c409b1b843cffae25f1810a7a885d9a69b3aefb2a6058219f132adc6ba0508f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigInputs",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "uri": "uri"},
)
class TranscoderJobConfigInputs:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: A unique key for this input. Must be specified when using advanced mapping and edit lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#key TranscoderJob#key}
        :param uri: URI of the media. Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, gs://bucket/inputs/file.mp4). If empty, the value is populated from Job.input_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#uri TranscoderJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c105cd42b1e373d56c1dc552f1604423a63c86523a5de34884d19893fd3736)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#key TranscoderJob#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI of the media.

        Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, gs://bucket/inputs/file.mp4).
        If empty, the value is populated from Job.input_uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#uri TranscoderJob#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigInputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigInputsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigInputsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f688fd5bec3fe578651eebe6c8c240fe8a9f1baf01e25f5da27dff1bdaf18f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TranscoderJobConfigInputsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb10b49eb96fb68724d4e6dc945f0b4da3a781951ab8f8bb76432e527c034f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigInputsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec881e93c48395ddc00c577b04beac2e8ab66873b3e2ad794efd8b87118f1175)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cd2e21caa777ca5c43bbbca20b9bef5e7fc3ee80b3a8c8a25d181d7a8747293)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b84464ee738c263e57e643455e054bf92a0d47b21c01b2b1df122065c6e2b20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigInputs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigInputs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigInputs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e4803bfdbf6f27f0bc5073b96754bb981e660fcbf3603a33b9bb0057ff4951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigInputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigInputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dadd041c9eb29a8e3c3a88ad631bff07cab1540ab930dec0c77a8e6438c93480)
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
            type_hints = typing.get_type_hints(_typecheckingstub__555d9fb4cd68155b7990b9d68b988c27786cbc68445dc3ad021a1e451c8b5b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9efb741ad433d07fa933151642fe87ba44f60253c2a540c6981a475b313845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigInputs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigInputs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigInputs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b10e84f0b1c9694bdb34094ba41b629a371acd9eecc14ddefb32614020c1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigManifests",
    jsii_struct_bases=[],
    name_mapping={
        "file_name": "fileName",
        "mux_streams": "muxStreams",
        "type": "type",
    },
)
class TranscoderJobConfigManifests:
    def __init__(
        self,
        *,
        file_name: typing.Optional[builtins.str] = None,
        mux_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_name: The name of the generated file. The default is 'manifest'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#file_name TranscoderJob#file_name}
        :param mux_streams: List of user supplied MuxStream.key values that should appear in this manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#mux_streams TranscoderJob#mux_streams}
        :param type: Type of the manifest. Possible values: ["MANIFEST_TYPE_UNSPECIFIED", "HLS", "DASH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#type TranscoderJob#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3299846a45fa50eb961fb3547923b9795bfda1eaf954c5b2ff5376050b814204)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#file_name TranscoderJob#file_name}
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mux_streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user supplied MuxStream.key values that should appear in this manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#mux_streams TranscoderJob#mux_streams}
        '''
        result = self._values.get("mux_streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of the manifest. Possible values: ["MANIFEST_TYPE_UNSPECIFIED", "HLS", "DASH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#type TranscoderJob#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigManifests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigManifestsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigManifestsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__747ad9d87582e871a715e9b38437082398ee80ed4859d5aea107d1a977d1693d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TranscoderJobConfigManifestsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77694167d663c3d2878ce84db2e5c2dae4f6b52092a9f498c789a69b3191921d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigManifestsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120c7e622b560664f1c0811f66895beadd9be92040d90185e4684de78625db29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fce1ed1830a64978abebacc8ea60164de16e264dc07884970d7643a8a309f9ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff1770210e3f16eeafb84f7d7a884c9a79982e6e1ddb1143e4d3798756bcae19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigManifests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigManifests]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigManifests]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee81127271a0194199d5271100396ccd10472d91e975bc47e0860421d0016f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigManifestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigManifestsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e3fa77139e506fedb18c46ebc334586ca1585d5e8fa3b1d2ece1f047f1d7b2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7063ac2bce9121d1055ff266b84a70b55b066b8a6426cfbc1835a923f459476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="muxStreams")
    def mux_streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "muxStreams"))

    @mux_streams.setter
    def mux_streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a72321cf0ede80b9708978c49382ad98d8fccbc7e4fd3a795381567acab2d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "muxStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2ab09c00c5268caf0fa6f010d5010571b8527812b88af1ed58b82d7893a1d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigManifests]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigManifests]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigManifests]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed55f941534822e884b46342041bab14d5a1d27b1d3a9c2e3e3c916bb11ce3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigMuxStreams",
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
class TranscoderJobConfigMuxStreams:
    def __init__(
        self,
        *,
        container: typing.Optional[builtins.str] = None,
        elementary_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
        encryption_id: typing.Optional[builtins.str] = None,
        file_name: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        segment_settings: typing.Optional[typing.Union["TranscoderJobConfigMuxStreamsSegmentSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: The container format. The default is 'mp4'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#container TranscoderJob#container}
        :param elementary_streams: List of ElementaryStream.key values multiplexed in this stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#elementary_streams TranscoderJob#elementary_streams}
        :param encryption_id: Identifier of the encryption configuration to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#encryption_id TranscoderJob#encryption_id}
        :param file_name: The name of the generated file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#file_name TranscoderJob#file_name}
        :param key: A unique key for this multiplexed stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#key TranscoderJob#key}
        :param segment_settings: segment_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#segment_settings TranscoderJob#segment_settings}
        '''
        if isinstance(segment_settings, dict):
            segment_settings = TranscoderJobConfigMuxStreamsSegmentSettings(**segment_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874fb7f81c2a7280bd2552ffda0535d2bc97b53cf6d18b90a9189048545a1f86)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#container TranscoderJob#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elementary_streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of ElementaryStream.key values multiplexed in this stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#elementary_streams TranscoderJob#elementary_streams}
        '''
        result = self._values.get("elementary_streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def encryption_id(self) -> typing.Optional[builtins.str]:
        '''Identifier of the encryption configuration to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#encryption_id TranscoderJob#encryption_id}
        '''
        result = self._values.get("encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_name(self) -> typing.Optional[builtins.str]:
        '''The name of the generated file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#file_name TranscoderJob#file_name}
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this multiplexed stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#key TranscoderJob#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_settings(
        self,
    ) -> typing.Optional["TranscoderJobConfigMuxStreamsSegmentSettings"]:
        '''segment_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#segment_settings TranscoderJob#segment_settings}
        '''
        result = self._values.get("segment_settings")
        return typing.cast(typing.Optional["TranscoderJobConfigMuxStreamsSegmentSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigMuxStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigMuxStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigMuxStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cdc289a275fd0ade68e4966075e22d7600211b75a390a8b6713aa992a4d448a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TranscoderJobConfigMuxStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24756aad1c3052f51634d0d3bef30910ad09d3c7c5852b89b4ea86564a8e973c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigMuxStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b5d18fe160a25680bac874f91facecacd379f29960831476274ae2495ff551)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6523eff98af9078a8b4fc8f8240fdccec64d220a8c82ab3daa082eab580eefae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20264599db2096076c88ab0f86702dd05873955076a5f74ce81178324cd6acad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigMuxStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigMuxStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigMuxStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f70af97452efa29a4f64593c177e3e58aae3cfed6bfcb44fdd3af9db6ec4f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigMuxStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigMuxStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4450cde215f7ad1e83cbd0e3e4d76ec06d668b56e5d1b6a576fa9efa0000f342)
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
        :param segment_duration: Duration of the segments in seconds. The default is '6.0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#segment_duration TranscoderJob#segment_duration}
        '''
        value = TranscoderJobConfigMuxStreamsSegmentSettings(
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
    ) -> "TranscoderJobConfigMuxStreamsSegmentSettingsOutputReference":
        return typing.cast("TranscoderJobConfigMuxStreamsSegmentSettingsOutputReference", jsii.get(self, "segmentSettings"))

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
    ) -> typing.Optional["TranscoderJobConfigMuxStreamsSegmentSettings"]:
        return typing.cast(typing.Optional["TranscoderJobConfigMuxStreamsSegmentSettings"], jsii.get(self, "segmentSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d15e106b3aeef12a64158da80c8c94ae7b0a14811fcc6d60e1e184de7755b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elementaryStreams")
    def elementary_streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "elementaryStreams"))

    @elementary_streams.setter
    def elementary_streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd464def39a764cad917378ada0005764c0476aaf07520dcdc574207378ccde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elementaryStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionId")
    def encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionId"))

    @encryption_id.setter
    def encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5507bc635297c357b387d6561ea81d37e7e1983f415272a7ae7ced44fd4e299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f6284d390f324346d35e828da450e61df71d0797447e400e047450c48829c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165e9e66a1d5c27dfbf419b566af6f4b9d489115aff8e27aea5975f0da392df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigMuxStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigMuxStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigMuxStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01d1a652a1ca5ae32b0053e5de200c0095c6725248d25b786b5a9527f32a55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigMuxStreamsSegmentSettings",
    jsii_struct_bases=[],
    name_mapping={"segment_duration": "segmentDuration"},
)
class TranscoderJobConfigMuxStreamsSegmentSettings:
    def __init__(
        self,
        *,
        segment_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param segment_duration: Duration of the segments in seconds. The default is '6.0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#segment_duration TranscoderJob#segment_duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad652bcf46247890ec104409ef12a162abfd11599635c4541767732f9a96159)
            check_type(argname="argument segment_duration", value=segment_duration, expected_type=type_hints["segment_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if segment_duration is not None:
            self._values["segment_duration"] = segment_duration

    @builtins.property
    def segment_duration(self) -> typing.Optional[builtins.str]:
        '''Duration of the segments in seconds. The default is '6.0s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#segment_duration TranscoderJob#segment_duration}
        '''
        result = self._values.get("segment_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigMuxStreamsSegmentSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigMuxStreamsSegmentSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigMuxStreamsSegmentSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc8582dd8f9a925b9f66d4e7a985f5de8637a11d2779f2036a195195135fd530)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85b0e68b9f1710bdb2aee1297303e30ffbc111ce1bd0056c95e29f1ef15b964a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigMuxStreamsSegmentSettings]:
        return typing.cast(typing.Optional[TranscoderJobConfigMuxStreamsSegmentSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigMuxStreamsSegmentSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddbdc9f55ffa1d44845863f82c2d4ee643b1b79dea81514f50a32c3f34e0565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOutput",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class TranscoderJobConfigOutput:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: URI for the output file(s). For example, gs://my-bucket/outputs/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#uri TranscoderJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d180a1d63d43109073f1924468a02537abacb7748b412c09a056fa57cdb16d53)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI for the output file(s). For example, gs://my-bucket/outputs/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#uri TranscoderJob#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb59c40a6bbe0d69820c8062cc30d30c06671d98ce57b238999b5e493bd3f745)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1420ceade537ba565715781b69a38912aac4afd994223850d257ddac54ae6cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TranscoderJobConfigOutput]:
        return typing.cast(typing.Optional[TranscoderJobConfigOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TranscoderJobConfigOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187052f28cf60587f0f1cf8c387d3b088f833f170d4a3c26ad353cb17ba59648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlays",
    jsii_struct_bases=[],
    name_mapping={"animations": "animations", "image": "image"},
)
class TranscoderJobConfigOverlays:
    def __init__(
        self,
        *,
        animations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobConfigOverlaysAnimations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        image: typing.Optional[typing.Union["TranscoderJobConfigOverlaysImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param animations: animations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#animations TranscoderJob#animations}
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#image TranscoderJob#image}
        '''
        if isinstance(image, dict):
            image = TranscoderJobConfigOverlaysImage(**image)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5150eace55f012fa9ec61ab6d77405d940c4982f64428f619110b1e44235f08)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigOverlaysAnimations"]]]:
        '''animations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#animations TranscoderJob#animations}
        '''
        result = self._values.get("animations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobConfigOverlaysAnimations"]]], result)

    @builtins.property
    def image(self) -> typing.Optional["TranscoderJobConfigOverlaysImage"]:
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#image TranscoderJob#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional["TranscoderJobConfigOverlaysImage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigOverlays(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysAnimations",
    jsii_struct_bases=[],
    name_mapping={"animation_fade": "animationFade"},
)
class TranscoderJobConfigOverlaysAnimations:
    def __init__(
        self,
        *,
        animation_fade: typing.Optional[typing.Union["TranscoderJobConfigOverlaysAnimationsAnimationFade", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param animation_fade: animation_fade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#animation_fade TranscoderJob#animation_fade}
        '''
        if isinstance(animation_fade, dict):
            animation_fade = TranscoderJobConfigOverlaysAnimationsAnimationFade(**animation_fade)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b969103d63eb101d8eab29689fb44c1994e5cb608668f0fed4a2a4a2546bd4c0)
            check_type(argname="argument animation_fade", value=animation_fade, expected_type=type_hints["animation_fade"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if animation_fade is not None:
            self._values["animation_fade"] = animation_fade

    @builtins.property
    def animation_fade(
        self,
    ) -> typing.Optional["TranscoderJobConfigOverlaysAnimationsAnimationFade"]:
        '''animation_fade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#animation_fade TranscoderJob#animation_fade}
        '''
        result = self._values.get("animation_fade")
        return typing.cast(typing.Optional["TranscoderJobConfigOverlaysAnimationsAnimationFade"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigOverlaysAnimations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysAnimationsAnimationFade",
    jsii_struct_bases=[],
    name_mapping={
        "fade_type": "fadeType",
        "end_time_offset": "endTimeOffset",
        "start_time_offset": "startTimeOffset",
        "xy": "xy",
    },
)
class TranscoderJobConfigOverlaysAnimationsAnimationFade:
    def __init__(
        self,
        *,
        fade_type: builtins.str,
        end_time_offset: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
        xy: typing.Optional[typing.Union["TranscoderJobConfigOverlaysAnimationsAnimationFadeXy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fade_type: Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:. - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified. - 'FADE_IN': Fade the overlay object into view. - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#fade_type TranscoderJob#fade_type}
        :param end_time_offset: The time to end the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#end_time_offset TranscoderJob#end_time_offset}
        :param start_time_offset: The time to start the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#start_time_offset TranscoderJob#start_time_offset}
        :param xy: xy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#xy TranscoderJob#xy}
        '''
        if isinstance(xy, dict):
            xy = TranscoderJobConfigOverlaysAnimationsAnimationFadeXy(**xy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b88d95f3ea6cb96324fac6e2e81a6a0b71d42bddb0e83ba7e22de102bcdea4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#fade_type TranscoderJob#fade_type}
        '''
        result = self._values.get("fade_type")
        assert result is not None, "Required property 'fade_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_time_offset(self) -> typing.Optional[builtins.str]:
        '''The time to end the fade animation, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#end_time_offset TranscoderJob#end_time_offset}
        '''
        result = self._values.get("end_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''The time to start the fade animation, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#start_time_offset TranscoderJob#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xy(
        self,
    ) -> typing.Optional["TranscoderJobConfigOverlaysAnimationsAnimationFadeXy"]:
        '''xy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#xy TranscoderJob#xy}
        '''
        result = self._values.get("xy")
        return typing.cast(typing.Optional["TranscoderJobConfigOverlaysAnimationsAnimationFadeXy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigOverlaysAnimationsAnimationFade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__948b849e91edbbd5eb48749aa27577c8dbec946700849194fd758ec40509de46)
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
        :param x: Normalized x coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#x TranscoderJob#x}
        :param y: Normalized y coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#y TranscoderJob#y}
        '''
        value = TranscoderJobConfigOverlaysAnimationsAnimationFadeXy(x=x, y=y)

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
    ) -> "TranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference":
        return typing.cast("TranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference", jsii.get(self, "xy"))

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
    ) -> typing.Optional["TranscoderJobConfigOverlaysAnimationsAnimationFadeXy"]:
        return typing.cast(typing.Optional["TranscoderJobConfigOverlaysAnimationsAnimationFadeXy"], jsii.get(self, "xyInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeOffset")
    def end_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTimeOffset"))

    @end_time_offset.setter
    def end_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21495c253e651d628ba959b5f92551632fa269aad8bb23a256482c0c274fa55e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fadeType")
    def fade_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fadeType"))

    @fade_type.setter
    def fade_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59603e809e5bcad35fde6a30dbc1a961f7e1c14dd43142bb7469e99e23ddf2da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fadeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6969a4ce1a67be6fbdcf3409af21c801f6b688032804ac6e1bd06b7405d055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFade]:
        return typing.cast(typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d7f5baa0be1263bf201c7ad3f0d5dfb235661f2966590126785b3e8281be50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysAnimationsAnimationFadeXy",
    jsii_struct_bases=[],
    name_mapping={"x": "x", "y": "y"},
)
class TranscoderJobConfigOverlaysAnimationsAnimationFadeXy:
    def __init__(
        self,
        *,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param x: Normalized x coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#x TranscoderJob#x}
        :param y: Normalized y coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#y TranscoderJob#y}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d9424873aa9dfc0415389819acebe48dd5384d2c1673c8598b9019d1417755)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#x TranscoderJob#x}
        '''
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        '''Normalized y coordinate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#y TranscoderJob#y}
        '''
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigOverlaysAnimationsAnimationFadeXy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1959a969f9b37b404daa106d3988639a6237b09ed3e8440389b3adbfe5b8c963)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ded68c9095298733bbb7fd70e63558d4738ac44e531ce3522430e7facd63f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "y"))

    @y.setter
    def y(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa229312b43bb724a020465b5709c83b62e53a4dfebef068877b79354bacd97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "y", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFadeXy]:
        return typing.cast(typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFadeXy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFadeXy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa00009641a6b3fc553ac7db576af56758d25d39331bf8a5f42647a42a123b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigOverlaysAnimationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysAnimationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d27875486d050a2f557dc62be840254cdc3fe76663a36e73a1497f36e11f2f6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobConfigOverlaysAnimationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9dacf948d2175c559dd6143a68955afe24bece33072f7e8f6d4aa4bf4e0138)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigOverlaysAnimationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3664649d5e7d0092a2414232e16a417877a79493e29f13bc7d9cdfa756cb5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__085e194a8b4f1386b04751b133689a92b0aa58a8bf43927770830ca64c62297f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64a31406c8c9258e6bfd4ba95e79e5489f8d48f803389cdb906bfcdcd4c61b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlaysAnimations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlaysAnimations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlaysAnimations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd8c68223bce13ef9971a2bfd531bb5d251d8377e9ad6360ac0c63f42ef4b30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigOverlaysAnimationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysAnimationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e655621cb89132261e3fa78119b016d5d982014e517873303cdd632ccf5b4f4)
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
        xy: typing.Optional[typing.Union[TranscoderJobConfigOverlaysAnimationsAnimationFadeXy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fade_type: Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:. - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified. - 'FADE_IN': Fade the overlay object into view. - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#fade_type TranscoderJob#fade_type}
        :param end_time_offset: The time to end the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#end_time_offset TranscoderJob#end_time_offset}
        :param start_time_offset: The time to start the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#start_time_offset TranscoderJob#start_time_offset}
        :param xy: xy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#xy TranscoderJob#xy}
        '''
        value = TranscoderJobConfigOverlaysAnimationsAnimationFade(
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
    ) -> TranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference:
        return typing.cast(TranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference, jsii.get(self, "animationFade"))

    @builtins.property
    @jsii.member(jsii_name="animationFadeInput")
    def animation_fade_input(
        self,
    ) -> typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFade]:
        return typing.cast(typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFade], jsii.get(self, "animationFadeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigOverlaysAnimations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigOverlaysAnimations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigOverlaysAnimations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5cab9aebb6d14516f54d102baf73d2766b5b9c208babf04ef1745f3c589838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysImage",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class TranscoderJobConfigOverlaysImage:
    def __init__(self, *, uri: builtins.str) -> None:
        '''
        :param uri: URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#uri TranscoderJob#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb758861bc1ced9f759ff906d5a3c022883f501fd77f89b3a3cde119a4936729)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#uri TranscoderJob#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigOverlaysImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigOverlaysImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3548d5a31fe8677456860ac2ca0fafa4d37be218dad4dd6a8d563be24fe1f9c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efff01684c6083fdc500d72d1cd34bb959715ee85b654bc1aa85782eb1397686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TranscoderJobConfigOverlaysImage]:
        return typing.cast(typing.Optional[TranscoderJobConfigOverlaysImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigOverlaysImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1343a1452c4ae222e6ca7e2955896f420a073a02df5c33ec236696bd3a6490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigOverlaysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e67c07c2301c770275c9172e6a58cabbd606f3fa25394cbd14c6c5af652ef3b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TranscoderJobConfigOverlaysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da34a974ef5d0bd4bfbc75e8b652d5f0adf1372912ffdcff8a43d6b265429e8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobConfigOverlaysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503d45034579db7a5994dade50f571983216080e8888d76f7a41d6cabd442026)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed76ce39b1abf68006d7db8758559a23ed1c959be8ac60bdc500659e4b23f491)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0b6cccbbd63323fda737cdf21cb017de28325be726e39436291d456f18d827e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlays]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlays]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlays]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4acc0f9a072005e98677d43072a11d06a34443311976c991964f73c1c221006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobConfigOverlaysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigOverlaysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e113d1df7945ff92dcdfbdea2bef7ea5e1f60d215633e20e7938063e1eb236)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAnimations")
    def put_animations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb20a2e34c984e8aece81a534b4daf460c0963870670c3f56337c6dd603d3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnimations", [value]))

    @jsii.member(jsii_name="putImage")
    def put_image(self, *, uri: builtins.str) -> None:
        '''
        :param uri: URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#uri TranscoderJob#uri}
        '''
        value = TranscoderJobConfigOverlaysImage(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="resetAnimations")
    def reset_animations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnimations", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @builtins.property
    @jsii.member(jsii_name="animations")
    def animations(self) -> TranscoderJobConfigOverlaysAnimationsList:
        return typing.cast(TranscoderJobConfigOverlaysAnimationsList, jsii.get(self, "animations"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> TranscoderJobConfigOverlaysImageOutputReference:
        return typing.cast(TranscoderJobConfigOverlaysImageOutputReference, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="animationsInput")
    def animations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlaysAnimations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlaysAnimations]]], jsii.get(self, "animationsInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[TranscoderJobConfigOverlaysImage]:
        return typing.cast(typing.Optional[TranscoderJobConfigOverlaysImage], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigOverlays]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigOverlays]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigOverlays]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fd38d5ca7592b9183ce1a74563b32d03fa84837840c449d6e28b37b5ee11be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigPubsubDestination",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class TranscoderJobConfigPubsubDestination:
    def __init__(self, *, topic: typing.Optional[builtins.str] = None) -> None:
        '''
        :param topic: The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#topic TranscoderJob#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988fd4178606858f608d8d73efeac9a2d8d3603e17f3925c46ad50c26c7a50e1)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#topic TranscoderJob#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobConfigPubsubDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobConfigPubsubDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobConfigPubsubDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8844f20731773e385fbed2aa3aa0aca799d04bbc291930eb422758aa096dfd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4eefcf92cfcb966cd02d03c975a6b9436f7e3e98ae077f2bbb09a7f649f9a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TranscoderJobConfigPubsubDestination]:
        return typing.cast(typing.Optional[TranscoderJobConfigPubsubDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobConfigPubsubDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de03496d81c27def52efe483eae07b95d935f0ad87e6eda529d7652e9ca2aa40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class TranscoderJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#create TranscoderJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#delete TranscoderJob#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#update TranscoderJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb34e88f78fe5823b593b6d022d6ff3b5f78ff88be761c868df8876eaed8d7cc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#create TranscoderJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#delete TranscoderJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job#update TranscoderJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJob.TranscoderJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__998dc37a756775928813d0741a5025ffef6546b5c9488978008ebf07d9f78ce5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54e9cbc1ab5d60d8ebbc1ba19bf7fe313ffc02f839492f2c06c386e32ac3138f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0ec850a03095c40c520a7c24d1a96a18e62f8e6b1d153e6d9c915e52918dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba16f6b603b37f99b254d1b3c6f5aeb1dd04380b3fea0b11b25a8044d68169b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0c5d9e09bd9f2942630f6710cb003f71e9ed3c042617b49cb998daab1a05fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TranscoderJob",
    "TranscoderJobConfig",
    "TranscoderJobConfigA",
    "TranscoderJobConfigAOutputReference",
    "TranscoderJobConfigAdBreaks",
    "TranscoderJobConfigAdBreaksList",
    "TranscoderJobConfigAdBreaksOutputReference",
    "TranscoderJobConfigEditListStruct",
    "TranscoderJobConfigEditListStructList",
    "TranscoderJobConfigEditListStructOutputReference",
    "TranscoderJobConfigElementaryStreams",
    "TranscoderJobConfigElementaryStreamsAudioStream",
    "TranscoderJobConfigElementaryStreamsAudioStreamOutputReference",
    "TranscoderJobConfigElementaryStreamsList",
    "TranscoderJobConfigElementaryStreamsOutputReference",
    "TranscoderJobConfigElementaryStreamsVideoStream",
    "TranscoderJobConfigElementaryStreamsVideoStreamH264",
    "TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg",
    "TranscoderJobConfigElementaryStreamsVideoStreamH264HlgOutputReference",
    "TranscoderJobConfigElementaryStreamsVideoStreamH264OutputReference",
    "TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr",
    "TranscoderJobConfigElementaryStreamsVideoStreamH264SdrOutputReference",
    "TranscoderJobConfigElementaryStreamsVideoStreamOutputReference",
    "TranscoderJobConfigEncryptions",
    "TranscoderJobConfigEncryptionsAes128",
    "TranscoderJobConfigEncryptionsAes128OutputReference",
    "TranscoderJobConfigEncryptionsDrmSystems",
    "TranscoderJobConfigEncryptionsDrmSystemsClearkey",
    "TranscoderJobConfigEncryptionsDrmSystemsClearkeyOutputReference",
    "TranscoderJobConfigEncryptionsDrmSystemsFairplay",
    "TranscoderJobConfigEncryptionsDrmSystemsFairplayOutputReference",
    "TranscoderJobConfigEncryptionsDrmSystemsOutputReference",
    "TranscoderJobConfigEncryptionsDrmSystemsPlayready",
    "TranscoderJobConfigEncryptionsDrmSystemsPlayreadyOutputReference",
    "TranscoderJobConfigEncryptionsDrmSystemsWidevine",
    "TranscoderJobConfigEncryptionsDrmSystemsWidevineOutputReference",
    "TranscoderJobConfigEncryptionsList",
    "TranscoderJobConfigEncryptionsMpegCenc",
    "TranscoderJobConfigEncryptionsMpegCencOutputReference",
    "TranscoderJobConfigEncryptionsOutputReference",
    "TranscoderJobConfigEncryptionsSampleAes",
    "TranscoderJobConfigEncryptionsSampleAesOutputReference",
    "TranscoderJobConfigEncryptionsSecretManagerKeySource",
    "TranscoderJobConfigEncryptionsSecretManagerKeySourceOutputReference",
    "TranscoderJobConfigInputs",
    "TranscoderJobConfigInputsList",
    "TranscoderJobConfigInputsOutputReference",
    "TranscoderJobConfigManifests",
    "TranscoderJobConfigManifestsList",
    "TranscoderJobConfigManifestsOutputReference",
    "TranscoderJobConfigMuxStreams",
    "TranscoderJobConfigMuxStreamsList",
    "TranscoderJobConfigMuxStreamsOutputReference",
    "TranscoderJobConfigMuxStreamsSegmentSettings",
    "TranscoderJobConfigMuxStreamsSegmentSettingsOutputReference",
    "TranscoderJobConfigOutput",
    "TranscoderJobConfigOutputOutputReference",
    "TranscoderJobConfigOverlays",
    "TranscoderJobConfigOverlaysAnimations",
    "TranscoderJobConfigOverlaysAnimationsAnimationFade",
    "TranscoderJobConfigOverlaysAnimationsAnimationFadeOutputReference",
    "TranscoderJobConfigOverlaysAnimationsAnimationFadeXy",
    "TranscoderJobConfigOverlaysAnimationsAnimationFadeXyOutputReference",
    "TranscoderJobConfigOverlaysAnimationsList",
    "TranscoderJobConfigOverlaysAnimationsOutputReference",
    "TranscoderJobConfigOverlaysImage",
    "TranscoderJobConfigOverlaysImageOutputReference",
    "TranscoderJobConfigOverlaysList",
    "TranscoderJobConfigOverlaysOutputReference",
    "TranscoderJobConfigPubsubDestination",
    "TranscoderJobConfigPubsubDestinationOutputReference",
    "TranscoderJobTimeouts",
    "TranscoderJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__971d1dc92cb010fe04d99ff4ed8aeb60384f3ae236e8b139af3c268555b5e4f6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    config: typing.Optional[typing.Union[TranscoderJobConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[TranscoderJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7bded4068e76980d98e558729ecf98b77cac09235400cd090d0288888238652b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422731a109e56cc8bdbd7d730198b951c58ff8b29875b801bd73db1412cbaf78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0eaa1de0e6a81d1d74b71cb3c626a8872a37b0a6361d584b348973640b7f13(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdef19b4f73d24e8acfdd1faeda249ab9bad58d8541994da331cf46204b8fdc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b3efface0b323e2acc6b4318a1f1514e476257a8411e7faa98298f558a1de1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7ca12e6f4ba33457a489f13a6fba44013613235b1974e8fda4d89407cf0611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42bd564edd919cdd4705255d48fd847adda5fe59241f3acb58cb0fd32a4fadd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    config: typing.Optional[typing.Union[TranscoderJobConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    template_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[TranscoderJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd470cba6ce8395a7333a95e25a9c37e32c11ff2004db9b2f5cc8038934b8ca(
    *,
    ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigAdBreaks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigEditListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigElementaryStreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigEncryptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigInputs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigManifests, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigMuxStreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    output: typing.Optional[typing.Union[TranscoderJobConfigOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigOverlays, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pubsub_destination: typing.Optional[typing.Union[TranscoderJobConfigPubsubDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe31edc353f9f98a99c619aa1f275f1371d2df4c2633cb6bc348ac1a8f198ec3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29aad383b38b203462190c4350f9e2f62f6c386871ba7373b6694161e002a01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigAdBreaks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a566bf0569f2d32185e74df8dad1b1747cec44e45de5d99318d877875c4a44e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigEditListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c77018f9e2f355a5272ac874db47a04c19e9820f30de718ba2f33be565c6cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigElementaryStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596db4b0fe59205b755d725d82e6bd0438933739242e63f6e4c725863c1a9104(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigEncryptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c8ea3a060e97796dbcc6f0ec52e9ad3f1ccac2f1895f0b89b1897f4a9754b5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigInputs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2c2d2de13b28b540e5d5779f36853ce418bc3c1a426446d0d3995022f742a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigManifests, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad495963f314c5f70ea969f91c1092c7dd0bdd6193013de23e61e96acd90bded(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigMuxStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f837d556c7513eb26f8f93874a46a9889d8356767230f785c2212b3b20eca08d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigOverlays, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d69c1e65ed8d006fb05ee7417841c4f43f5f2829d4930698f916113df2e99bf(
    value: typing.Optional[TranscoderJobConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db96242575cf0088869fdafaa12e61d5f9e83462f6cac51bb94a439e134c055(
    *,
    start_time_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b45b9c115232ed2f7a14c1d51cac3624a9d68b0a9f48ba807ec5aa240c931f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e734c55e281388e5cf37d57df5ee06a4e66fdf977f9ec9165ef5b767366f31(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f97a14dcf9fc3894f6e2e7f4fe1b9ffdb8d44af6e79354b144639ee477be9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed427424f409597d753ef587863e696cbd07471a2eb8a4bf05fa2939e4b57088(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ddf4c7aac60737515ab424de3620808315249bd0e3ddc3ee91c1a0c9d837be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07be8d9eefcf274429527ad582477d831d5ba743cb1a14376e10529314bd30e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigAdBreaks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f157f2a820597f1c4d2e61a91cb891b1b3e93ca0fa859cf83966629bd96a26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101897ff453883031846c59fd29b4f8f2aadf14103bbe2690743b8c8bb644b7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__decc06f84b2c506deefc1fb81094c5cd85e1bb624b6ceb70c2f5a977cb8ab411(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigAdBreaks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8209f79b6eb1e46e51fdeafa3cf13a8a46aa839bdd6c0c54554e6c9b418ab43f(
    *,
    inputs: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[builtins.str] = None,
    start_time_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae1dd78d91538160304c26d8a4fb8c93403acb33ae4672edcd6044f63aa7196(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e5e4e76762f508ee1992a2291db0e79537b87667684f02aa4a4b78655cb19b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1eeae247d85ed6df27c4744d8f047bc71f13ca02414e3cbafcac8ab8409e529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73aa700a2d0c86708e628bcca6fd34cfe33edecea095f19b49553d26ab9b082e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ad9861c17330ee552a1043d9ea513dc1bf24d1d46a924b61ef346a0f488dd4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375cb3f24c195c7464315ccb132dce8aa3bdcdab4be5d5949b59aeeaeceafe60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigEditListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c99ee2264355349cf691f8dedc78c492e37adc2d56b345690a206b2fce8bb33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b381d841ef0ea9fe143dc39f95cfcc42f8f713171c50cb63b01aa8b0fbf1fc0e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e93c8e1412201e7fd55cf0c36e4f56ce500661e0fbabf31b1b3a095ddccba3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a685fb615b8cda05d9afa29693bf51790593464d30a0893bfb843c7feed6a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22564f932fe49a927198a23d4974553522a68a75ec8f849402a2beea9139a65e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigEditListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc6078443d03b78b04a4c85bfbd2aa8e7423025189fc57bad2dc1af34aa47f5(
    *,
    audio_stream: typing.Optional[typing.Union[TranscoderJobConfigElementaryStreamsAudioStream, typing.Dict[builtins.str, typing.Any]]] = None,
    key: typing.Optional[builtins.str] = None,
    video_stream: typing.Optional[typing.Union[TranscoderJobConfigElementaryStreamsVideoStream, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1ba5830564d2e0063e71526b5a30684961c0ce6e00ca2ae053170ed8757ffb(
    *,
    bitrate_bps: jsii.Number,
    channel_count: typing.Optional[jsii.Number] = None,
    channel_layout: typing.Optional[typing.Sequence[builtins.str]] = None,
    codec: typing.Optional[builtins.str] = None,
    sample_rate_hertz: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b725d02692cd1f32b0cd6403514fd46126483b1e0486b0b5a332af9c8fde6b17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12cfc1369cfc88920ae3c238f72c357691a6f45dd8ca5e72e6e2853a50421d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12f6a0c257d369a602f1449ebc78f9278b0a3a84b6b5697ad3680e76f6576a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3be5018ebbb23377dfd3528a405cf01ad62fd7aa7ec04315d552ccfb4c7b09(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0e274b97604a00bb51f2f68f4ff6d2f33a437872533b1b2c9758a736c8d00d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b95358b48b1db40abf61b46e4d6369d5356b233b0d7474ac91041b3431168d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc22565aca643bff13da0ea6b25101a9e5d2aa0ea863b8ad0362d311fe13235(
    value: typing.Optional[TranscoderJobConfigElementaryStreamsAudioStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378c124985075997fa9f72b8ef08c9b3736e6b0fe8a4090a60bb2efa044af1da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bda3212ae27df01e558b7f3bcdc3b41a6af247f7f4dda5ea8f0848eb47ceeed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205cbc43099825dbef58fae61313b43adbb161af6249418641910a783f3f9c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a811ad663e1048d5f757f7a0749f8e3100d62bf90edbddcc7e9566569f9489(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8542aab0e448bf1363b964f888d2971236303db9bd3c224c33b09726df079d17(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6814f3372da84a3e3095ec1553792990a42e951e339030c42347aa42306f05c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigElementaryStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11bcae4df33c04cca14a68971d0c57d99135bc88f3a65d04bd6a67365c2f94b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd12d35f730a67d50abf143dc31a0a1140ed99789da87c55229da058c213163a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352dab74637792fc248ad6bcdd17f86c5914070539badb0353535e3ded5d3d7b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigElementaryStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738e6f6a48ea203f4501a0269cf7bbe9ecbfd393d19dac3b96859c90abb2a84d(
    *,
    h264: typing.Optional[typing.Union[TranscoderJobConfigElementaryStreamsVideoStreamH264, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599b679c19e20646a42263620b47a5e6890fd19bcaec3c147c9d9e7b6d708daa(
    *,
    bitrate_bps: jsii.Number,
    frame_rate: jsii.Number,
    crf_level: typing.Optional[jsii.Number] = None,
    entropy_coder: typing.Optional[builtins.str] = None,
    gop_duration: typing.Optional[builtins.str] = None,
    height_pixels: typing.Optional[jsii.Number] = None,
    hlg: typing.Optional[typing.Union[TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg, typing.Dict[builtins.str, typing.Any]]] = None,
    pixel_format: typing.Optional[builtins.str] = None,
    preset: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    rate_control_mode: typing.Optional[builtins.str] = None,
    sdr: typing.Optional[typing.Union[TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr, typing.Dict[builtins.str, typing.Any]]] = None,
    vbv_fullness_bits: typing.Optional[jsii.Number] = None,
    vbv_size_bits: typing.Optional[jsii.Number] = None,
    width_pixels: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf31f804345c37d5cfc7a30ef66a7026ca915814dd6878e130bc2b6ecfe98d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8a44175d6c32b4edc6467b4d76f640f1e7f9c8a4453a17bb770e8fd9944d7d(
    value: typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Hlg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018dc2e266fd40eb398cae7d8f68c794d8ae7f2c095771ab4b8c3ced72e057fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19fb8382a779f2c5459799830d5a277ef36c38ac4ec6ef70b37f831e37368fe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48b0fcd4f175c3907ca271061d0ee1cb6dc5cb06baf7e2bf047eb73db4a093a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028f235c20cb829306ed68ca540131007358d6e59e063c4125b55d23bdb5d144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b270f18b529bd0434bd0b7f9f98411645c6eaee0ea3652c17cd66eaf47be44e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1de17c905088c59e6eba782b810c0efed3ce899ecfb8225edad79ac6db64ddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc505e931e787f5ddef944204026eb02aa8ddd351af7a60df157ffab81c01d51(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79463aea52344bfef79efb41ec63de1b0a89674e994b1a6f86f1edba2f941a91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10c3f191c5416cf7eebca02f797086601d6de5d984161de465cbffcf974421d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79242772ae03ab48ed6b8b4ede06bc7ded16e77ebac4756296815c6e35d2434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b4bf5bb7f478658bfbe12a5c914fc0d1b6eb743829e48c426305300806f767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402ad0894cce4e0a8044f07bf7caf3170eb279ba653f0b909c219c55d9554c20(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a240e60e62ddb7f878d7d406194e426f8bc4af2ae3bda348701a38b696d04ef9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85bae5effac4b8f6663cfb66ca55b8b487c8529001fab7a78ecf33a6b266dcab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f242f9cc60aaa69841e65aad4e69a2f311a95ff14c520ae33c9ff30fcad96889(
    value: typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb43436ed32eb27eaf04020ac8ba95c8a448b8f88010aa757d1da80834a70c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a471cb644f1ca2b6010ae3f6e1bc43da9e6074ab890b5510551a9c08c05f565(
    value: typing.Optional[TranscoderJobConfigElementaryStreamsVideoStreamH264Sdr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77367f26c75867c2c8695108b72af39474a10a1174e1a39b7b989b6bc4401279(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc6a2054ff735a1dd7f573f73705ee62baedded9858f9dbc586608512ba8113(
    value: typing.Optional[TranscoderJobConfigElementaryStreamsVideoStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1bef622684aef3ddc3b2430fa49ee68bce6641a5cd87f19a7d4a99bad3644d(
    *,
    id: builtins.str,
    aes128: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsAes128, typing.Dict[builtins.str, typing.Any]]] = None,
    drm_systems: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystems, typing.Dict[builtins.str, typing.Any]]] = None,
    mpeg_cenc: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsMpegCenc, typing.Dict[builtins.str, typing.Any]]] = None,
    sample_aes: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsSampleAes, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_manager_key_source: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsSecretManagerKeySource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4f704d0295a4027cee658b0ed4791e123b72d44a2f73493d13d16a0e9ed6f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4ac489dbd636d339b273be6ceacfa1182a9ff902852cac4019bf360f79954b(
    value: typing.Optional[TranscoderJobConfigEncryptionsAes128],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b163236852b495f2ee7a47471c4c19ef6216ee5ddecf462aed65a89f5f902838(
    *,
    clearkey: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystemsClearkey, typing.Dict[builtins.str, typing.Any]]] = None,
    fairplay: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystemsFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
    playready: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystemsPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
    widevine: typing.Optional[typing.Union[TranscoderJobConfigEncryptionsDrmSystemsWidevine, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719497a194a592ad1fe66ace8f05889f4fa4a47f18f019d891a8e185626bf8de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17346df479404674ef8813d72db7380bc55d6209526134bbbe21c875ff2eb72a(
    value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsClearkey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e8ece8b67785998712f1f6336a2e62b89ad4a6425589910ef9834351e783be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfdc7ea90b7ce5f6b563b0d70a9d2a74d4c0a3d587a0dd62506d18d0fbc2b39(
    value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsFairplay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7553f05f8fed5a6e02f5a080a410ec615808a0d7ff3ad2c18f83c639b717f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af2a614aa23668d9a2f4ab4ae72c280ef98b2cb8f4cc28402f394289c7906cc(
    value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystems],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d25735a45ff92423a1710e418ca256980d1a9397c5f6256969610bc2dcc94d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5159ad126578c53c7e345fbde7e4a9a835df2d966de0a42cef71889fe3847616(
    value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsPlayready],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351759ee31e1469c19124fba7d8c3d58b89e8bff6da20c22e405bdaeca5384c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de6d3566beae66d8df7870c50a1a97d39f94e4e517c3236afe3342b35cc6712(
    value: typing.Optional[TranscoderJobConfigEncryptionsDrmSystemsWidevine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ac948e5cca7831a4a670a754d0293af3a2873c3ae75e1d4676d629a123429a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f71e48cda8428f8f26fab17e7bed005dfef8c663a08627697c57894a629ba72(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da3def669a5ce0c80e9517f123664595d8b21499dbb649ba2af5aa976d89030(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5a0447041a55f0028eb38e03f1f06185e5e01e431fdeb52cd8543cd1822918(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec583aeb9e5724fc1c5e5fd4a6aa2b3144adf4bd5bc9d66d0b1425bef6e6dac1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b7b626a5d23179cbfd35835c3c8a63592fd76e7d5699cb0f5395ac3a5480d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigEncryptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622d33adbf2cd6f27cfc07dae7c8301ac875845434fd5af6d704b6a96f7ef5c9(
    *,
    scheme: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d60f273bd7ecb4c9aecf7ae9802a575391481bb1558aca482327be847e807ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2b0ba2ee8017aba02d5a1f8e6f81b1723ff8c3c8c8cacde55ff083a3e486d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8a2571ac9a24e420772d706aa8828edabbd88f318caf0c8579ee45c5bbc96e(
    value: typing.Optional[TranscoderJobConfigEncryptionsMpegCenc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64f2e7b9af9802f185c7521aa782b9f00d51e2bcaa27ceef64772a69c08ba3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99488a56cee5589cb605f0ff89c928791a2bd5eca48b25049c56761607947c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a959cbb7364e25302570d2a0ea9cca707ccfdddf777c84a8f90705e8b6e0aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigEncryptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2071a5e6fd405f37e1eea85f78c9a12866a28ff7a7595ce9a15a0e0cfcb51d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b61d2cb4d769b805955ddae707235b9e6adf6a9275c283dbb290e4027165734(
    value: typing.Optional[TranscoderJobConfigEncryptionsSampleAes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bde16d20d71e8787150884f9bc9680d5bd4a3d19ed6b6df2ca5a3d581dde172(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aad2a6d70f43617cd732b32bc48d36dfa28f7dd4e50d8b902f5f90dfa3852c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e8002218c38fe114c5555f3cf998e035d4bd90ee9641e94d2e415c29445be6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c409b1b843cffae25f1810a7a885d9a69b3aefb2a6058219f132adc6ba0508f(
    value: typing.Optional[TranscoderJobConfigEncryptionsSecretManagerKeySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c105cd42b1e373d56c1dc552f1604423a63c86523a5de34884d19893fd3736(
    *,
    key: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f688fd5bec3fe578651eebe6c8c240fe8a9f1baf01e25f5da27dff1bdaf18f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb10b49eb96fb68724d4e6dc945f0b4da3a781951ab8f8bb76432e527c034f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec881e93c48395ddc00c577b04beac2e8ab66873b3e2ad794efd8b87118f1175(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd2e21caa777ca5c43bbbca20b9bef5e7fc3ee80b3a8c8a25d181d7a8747293(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84464ee738c263e57e643455e054bf92a0d47b21c01b2b1df122065c6e2b20f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e4803bfdbf6f27f0bc5073b96754bb981e660fcbf3603a33b9bb0057ff4951(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigInputs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadd041c9eb29a8e3c3a88ad631bff07cab1540ab930dec0c77a8e6438c93480(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555d9fb4cd68155b7990b9d68b988c27786cbc68445dc3ad021a1e451c8b5b9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9efb741ad433d07fa933151642fe87ba44f60253c2a540c6981a475b313845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b10e84f0b1c9694bdb34094ba41b629a371acd9eecc14ddefb32614020c1c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigInputs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3299846a45fa50eb961fb3547923b9795bfda1eaf954c5b2ff5376050b814204(
    *,
    file_name: typing.Optional[builtins.str] = None,
    mux_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747ad9d87582e871a715e9b38437082398ee80ed4859d5aea107d1a977d1693d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77694167d663c3d2878ce84db2e5c2dae4f6b52092a9f498c789a69b3191921d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120c7e622b560664f1c0811f66895beadd9be92040d90185e4684de78625db29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce1ed1830a64978abebacc8ea60164de16e264dc07884970d7643a8a309f9ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1770210e3f16eeafb84f7d7a884c9a79982e6e1ddb1143e4d3798756bcae19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee81127271a0194199d5271100396ccd10472d91e975bc47e0860421d0016f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigManifests]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3fa77139e506fedb18c46ebc334586ca1585d5e8fa3b1d2ece1f047f1d7b2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7063ac2bce9121d1055ff266b84a70b55b066b8a6426cfbc1835a923f459476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a72321cf0ede80b9708978c49382ad98d8fccbc7e4fd3a795381567acab2d05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2ab09c00c5268caf0fa6f010d5010571b8527812b88af1ed58b82d7893a1d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed55f941534822e884b46342041bab14d5a1d27b1d3a9c2e3e3c916bb11ce3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigManifests]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874fb7f81c2a7280bd2552ffda0535d2bc97b53cf6d18b90a9189048545a1f86(
    *,
    container: typing.Optional[builtins.str] = None,
    elementary_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_id: typing.Optional[builtins.str] = None,
    file_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    segment_settings: typing.Optional[typing.Union[TranscoderJobConfigMuxStreamsSegmentSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdc289a275fd0ade68e4966075e22d7600211b75a390a8b6713aa992a4d448a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24756aad1c3052f51634d0d3bef30910ad09d3c7c5852b89b4ea86564a8e973c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b5d18fe160a25680bac874f91facecacd379f29960831476274ae2495ff551(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6523eff98af9078a8b4fc8f8240fdccec64d220a8c82ab3daa082eab580eefae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20264599db2096076c88ab0f86702dd05873955076a5f74ce81178324cd6acad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f70af97452efa29a4f64593c177e3e58aae3cfed6bfcb44fdd3af9db6ec4f20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigMuxStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4450cde215f7ad1e83cbd0e3e4d76ec06d668b56e5d1b6a576fa9efa0000f342(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d15e106b3aeef12a64158da80c8c94ae7b0a14811fcc6d60e1e184de7755b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd464def39a764cad917378ada0005764c0476aaf07520dcdc574207378ccde(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5507bc635297c357b387d6561ea81d37e7e1983f415272a7ae7ced44fd4e299(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f6284d390f324346d35e828da450e61df71d0797447e400e047450c48829c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165e9e66a1d5c27dfbf419b566af6f4b9d489115aff8e27aea5975f0da392df0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01d1a652a1ca5ae32b0053e5de200c0095c6725248d25b786b5a9527f32a55b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigMuxStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad652bcf46247890ec104409ef12a162abfd11599635c4541767732f9a96159(
    *,
    segment_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8582dd8f9a925b9f66d4e7a985f5de8637a11d2779f2036a195195135fd530(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b0e68b9f1710bdb2aee1297303e30ffbc111ce1bd0056c95e29f1ef15b964a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddbdc9f55ffa1d44845863f82c2d4ee643b1b79dea81514f50a32c3f34e0565(
    value: typing.Optional[TranscoderJobConfigMuxStreamsSegmentSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d180a1d63d43109073f1924468a02537abacb7748b412c09a056fa57cdb16d53(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb59c40a6bbe0d69820c8062cc30d30c06671d98ce57b238999b5e493bd3f745(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1420ceade537ba565715781b69a38912aac4afd994223850d257ddac54ae6cbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187052f28cf60587f0f1cf8c387d3b088f833f170d4a3c26ad353cb17ba59648(
    value: typing.Optional[TranscoderJobConfigOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5150eace55f012fa9ec61ab6d77405d940c4982f64428f619110b1e44235f08(
    *,
    animations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    image: typing.Optional[typing.Union[TranscoderJobConfigOverlaysImage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b969103d63eb101d8eab29689fb44c1994e5cb608668f0fed4a2a4a2546bd4c0(
    *,
    animation_fade: typing.Optional[typing.Union[TranscoderJobConfigOverlaysAnimationsAnimationFade, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b88d95f3ea6cb96324fac6e2e81a6a0b71d42bddb0e83ba7e22de102bcdea4(
    *,
    fade_type: builtins.str,
    end_time_offset: typing.Optional[builtins.str] = None,
    start_time_offset: typing.Optional[builtins.str] = None,
    xy: typing.Optional[typing.Union[TranscoderJobConfigOverlaysAnimationsAnimationFadeXy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948b849e91edbbd5eb48749aa27577c8dbec946700849194fd758ec40509de46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21495c253e651d628ba959b5f92551632fa269aad8bb23a256482c0c274fa55e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59603e809e5bcad35fde6a30dbc1a961f7e1c14dd43142bb7469e99e23ddf2da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6969a4ce1a67be6fbdcf3409af21c801f6b688032804ac6e1bd06b7405d055(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d7f5baa0be1263bf201c7ad3f0d5dfb235661f2966590126785b3e8281be50(
    value: typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d9424873aa9dfc0415389819acebe48dd5384d2c1673c8598b9019d1417755(
    *,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1959a969f9b37b404daa106d3988639a6237b09ed3e8440389b3adbfe5b8c963(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ded68c9095298733bbb7fd70e63558d4738ac44e531ce3522430e7facd63f6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa229312b43bb724a020465b5709c83b62e53a4dfebef068877b79354bacd97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa00009641a6b3fc553ac7db576af56758d25d39331bf8a5f42647a42a123b6e(
    value: typing.Optional[TranscoderJobConfigOverlaysAnimationsAnimationFadeXy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27875486d050a2f557dc62be840254cdc3fe76663a36e73a1497f36e11f2f6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9dacf948d2175c559dd6143a68955afe24bece33072f7e8f6d4aa4bf4e0138(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3664649d5e7d0092a2414232e16a417877a79493e29f13bc7d9cdfa756cb5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085e194a8b4f1386b04751b133689a92b0aa58a8bf43927770830ca64c62297f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a31406c8c9258e6bfd4ba95e79e5489f8d48f803389cdb906bfcdcd4c61b62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd8c68223bce13ef9971a2bfd531bb5d251d8377e9ad6360ac0c63f42ef4b30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlaysAnimations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e655621cb89132261e3fa78119b016d5d982014e517873303cdd632ccf5b4f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5cab9aebb6d14516f54d102baf73d2766b5b9c208babf04ef1745f3c589838(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigOverlaysAnimations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb758861bc1ced9f759ff906d5a3c022883f501fd77f89b3a3cde119a4936729(
    *,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3548d5a31fe8677456860ac2ca0fafa4d37be218dad4dd6a8d563be24fe1f9c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efff01684c6083fdc500d72d1cd34bb959715ee85b654bc1aa85782eb1397686(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1343a1452c4ae222e6ca7e2955896f420a073a02df5c33ec236696bd3a6490(
    value: typing.Optional[TranscoderJobConfigOverlaysImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67c07c2301c770275c9172e6a58cabbd606f3fa25394cbd14c6c5af652ef3b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da34a974ef5d0bd4bfbc75e8b652d5f0adf1372912ffdcff8a43d6b265429e8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503d45034579db7a5994dade50f571983216080e8888d76f7a41d6cabd442026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed76ce39b1abf68006d7db8758559a23ed1c959be8ac60bdc500659e4b23f491(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b6cccbbd63323fda737cdf21cb017de28325be726e39436291d456f18d827e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4acc0f9a072005e98677d43072a11d06a34443311976c991964f73c1c221006(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobConfigOverlays]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e113d1df7945ff92dcdfbdea2bef7ea5e1f60d215633e20e7938063e1eb236(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb20a2e34c984e8aece81a534b4daf460c0963870670c3f56337c6dd603d3d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fd38d5ca7592b9183ce1a74563b32d03fa84837840c449d6e28b37b5ee11be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobConfigOverlays]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988fd4178606858f608d8d73efeac9a2d8d3603e17f3925c46ad50c26c7a50e1(
    *,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8844f20731773e385fbed2aa3aa0aca799d04bbc291930eb422758aa096dfd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4eefcf92cfcb966cd02d03c975a6b9436f7e3e98ae077f2bbb09a7f649f9a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de03496d81c27def52efe483eae07b95d935f0ad87e6eda529d7652e9ca2aa40(
    value: typing.Optional[TranscoderJobConfigPubsubDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb34e88f78fe5823b593b6d022d6ff3b5f78ff88be761c868df8876eaed8d7cc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998dc37a756775928813d0741a5025ffef6546b5c9488978008ebf07d9f78ce5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e9cbc1ab5d60d8ebbc1ba19bf7fe313ffc02f839492f2c06c386e32ac3138f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0ec850a03095c40c520a7c24d1a96a18e62f8e6b1d153e6d9c915e52918dd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba16f6b603b37f99b254d1b3c6f5aeb1dd04380b3fea0b11b25a8044d68169b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0c5d9e09bd9f2942630f6710cb003f71e9ed3c042617b49cb998daab1a05fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
