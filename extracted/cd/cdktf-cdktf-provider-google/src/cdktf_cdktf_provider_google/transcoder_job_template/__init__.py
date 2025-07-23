r'''
# `google_transcoder_job_template`

Refer to the Terraform Registry for docs: [`google_transcoder_job_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template).
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


class TranscoderJobTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template google_transcoder_job_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        job_template_id: builtins.str,
        location: builtins.str,
        config: typing.Optional[typing.Union["TranscoderJobTemplateConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["TranscoderJobTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template google_transcoder_job_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param job_template_id: ID to use for the Transcoding job template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#job_template_id TranscoderJobTemplate#job_template_id}
        :param location: The location of the transcoding job template resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#location TranscoderJobTemplate#location}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#config TranscoderJobTemplate#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#id TranscoderJobTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this job template. You can use these to organize and group your job templates. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#labels TranscoderJobTemplate#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#project TranscoderJobTemplate#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#timeouts TranscoderJobTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8d562ed6ac7ac2f34e24a37b239d8a72bf397a27bf48388b1d0631ce1906b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = TranscoderJobTemplateConfig(
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
        '''Generates CDKTF code for importing a TranscoderJobTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TranscoderJobTemplate to import.
        :param import_from_id: The id of the existing TranscoderJobTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TranscoderJobTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5e52062e916c092b9df7130de2caf29f8c956059497a7daebc3ff1ed37b4ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigInputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigManifests", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union["TranscoderJobTemplateConfigOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigOverlays", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pubsub_destination: typing.Optional[typing.Union["TranscoderJobTemplateConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_breaks: ad_breaks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#ad_breaks TranscoderJobTemplate#ad_breaks}
        :param edit_list: edit_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#edit_list TranscoderJobTemplate#edit_list}
        :param elementary_streams: elementary_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#elementary_streams TranscoderJobTemplate#elementary_streams}
        :param encryptions: encryptions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#encryptions TranscoderJobTemplate#encryptions}
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#inputs TranscoderJobTemplate#inputs}
        :param manifests: manifests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#manifests TranscoderJobTemplate#manifests}
        :param mux_streams: mux_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#mux_streams TranscoderJobTemplate#mux_streams}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#output TranscoderJobTemplate#output}
        :param overlays: overlays block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#overlays TranscoderJobTemplate#overlays}
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#pubsub_destination TranscoderJobTemplate#pubsub_destination}
        '''
        value = TranscoderJobTemplateConfigA(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#create TranscoderJobTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#delete TranscoderJobTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#update TranscoderJobTemplate#update}.
        '''
        value = TranscoderJobTemplateTimeouts(
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
    def config(self) -> "TranscoderJobTemplateConfigAOutputReference":
        return typing.cast("TranscoderJobTemplateConfigAOutputReference", jsii.get(self, "config"))

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
    def timeouts(self) -> "TranscoderJobTemplateTimeoutsOutputReference":
        return typing.cast("TranscoderJobTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["TranscoderJobTemplateConfigA"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigA"], jsii.get(self, "configInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TranscoderJobTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TranscoderJobTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b11fb46980afe2144cb3b13d69bca4ef0503bc18c4750b396119715da4eef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobTemplateId")
    def job_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobTemplateId"))

    @job_template_id.setter
    def job_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e8b5cfa3f14944bb09f2044077c7b2f5eb7df34a6164c35fd8655408b3778f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobTemplateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04783dd4a67ffa129c250fca7ff9a9202731176ffa62486757cdb879620b2d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9e8dbbedb2ad3fcfdcc626c8c752b80963c2d1245c7cf3ee0661e5dc2c9bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f010efe1c3541f82ec030cc5edf77c28e7672b4cd888ac587b585e3b5e86a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfig",
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
class TranscoderJobTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: typing.Optional[typing.Union["TranscoderJobTemplateConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["TranscoderJobTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param job_template_id: ID to use for the Transcoding job template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#job_template_id TranscoderJobTemplate#job_template_id}
        :param location: The location of the transcoding job template resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#location TranscoderJobTemplate#location}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#config TranscoderJobTemplate#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#id TranscoderJobTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this job template. You can use these to organize and group your job templates. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#labels TranscoderJobTemplate#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#project TranscoderJobTemplate#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#timeouts TranscoderJobTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = TranscoderJobTemplateConfigA(**config)
        if isinstance(timeouts, dict):
            timeouts = TranscoderJobTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15da54943f51bfcaa731a9eaf1fe0b44ec9e7a9c67d4bead2341487c680aa17)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#job_template_id TranscoderJobTemplate#job_template_id}
        '''
        result = self._values.get("job_template_id")
        assert result is not None, "Required property 'job_template_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the transcoding job template resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#location TranscoderJobTemplate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["TranscoderJobTemplateConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#config TranscoderJobTemplate#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#id TranscoderJobTemplate#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#labels TranscoderJobTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#project TranscoderJobTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["TranscoderJobTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#timeouts TranscoderJobTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["TranscoderJobTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigA",
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
class TranscoderJobTemplateConfigA:
    def __init__(
        self,
        *,
        ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigInputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigManifests", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        output: typing.Optional[typing.Union["TranscoderJobTemplateConfigOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigOverlays", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pubsub_destination: typing.Optional[typing.Union["TranscoderJobTemplateConfigPubsubDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_breaks: ad_breaks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#ad_breaks TranscoderJobTemplate#ad_breaks}
        :param edit_list: edit_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#edit_list TranscoderJobTemplate#edit_list}
        :param elementary_streams: elementary_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#elementary_streams TranscoderJobTemplate#elementary_streams}
        :param encryptions: encryptions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#encryptions TranscoderJobTemplate#encryptions}
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#inputs TranscoderJobTemplate#inputs}
        :param manifests: manifests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#manifests TranscoderJobTemplate#manifests}
        :param mux_streams: mux_streams block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#mux_streams TranscoderJobTemplate#mux_streams}
        :param output: output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#output TranscoderJobTemplate#output}
        :param overlays: overlays block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#overlays TranscoderJobTemplate#overlays}
        :param pubsub_destination: pubsub_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#pubsub_destination TranscoderJobTemplate#pubsub_destination}
        '''
        if isinstance(output, dict):
            output = TranscoderJobTemplateConfigOutput(**output)
        if isinstance(pubsub_destination, dict):
            pubsub_destination = TranscoderJobTemplateConfigPubsubDestination(**pubsub_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30faaf3db4541a86a5333975f2c6105418c7b514ea25771159af53154086d2c)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigAdBreaks"]]]:
        '''ad_breaks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#ad_breaks TranscoderJobTemplate#ad_breaks}
        '''
        result = self._values.get("ad_breaks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigAdBreaks"]]], result)

    @builtins.property
    def edit_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigEditListStruct"]]]:
        '''edit_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#edit_list TranscoderJobTemplate#edit_list}
        '''
        result = self._values.get("edit_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigEditListStruct"]]], result)

    @builtins.property
    def elementary_streams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigElementaryStreams"]]]:
        '''elementary_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#elementary_streams TranscoderJobTemplate#elementary_streams}
        '''
        result = self._values.get("elementary_streams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigElementaryStreams"]]], result)

    @builtins.property
    def encryptions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigEncryptions"]]]:
        '''encryptions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#encryptions TranscoderJobTemplate#encryptions}
        '''
        result = self._values.get("encryptions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigEncryptions"]]], result)

    @builtins.property
    def inputs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigInputs"]]]:
        '''inputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#inputs TranscoderJobTemplate#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigInputs"]]], result)

    @builtins.property
    def manifests(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigManifests"]]]:
        '''manifests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#manifests TranscoderJobTemplate#manifests}
        '''
        result = self._values.get("manifests")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigManifests"]]], result)

    @builtins.property
    def mux_streams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigMuxStreams"]]]:
        '''mux_streams block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#mux_streams TranscoderJobTemplate#mux_streams}
        '''
        result = self._values.get("mux_streams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigMuxStreams"]]], result)

    @builtins.property
    def output(self) -> typing.Optional["TranscoderJobTemplateConfigOutput"]:
        '''output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#output TranscoderJobTemplate#output}
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigOutput"], result)

    @builtins.property
    def overlays(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigOverlays"]]]:
        '''overlays block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#overlays TranscoderJobTemplate#overlays}
        '''
        result = self._values.get("overlays")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigOverlays"]]], result)

    @builtins.property
    def pubsub_destination(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigPubsubDestination"]:
        '''pubsub_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#pubsub_destination TranscoderJobTemplate#pubsub_destination}
        '''
        result = self._values.get("pubsub_destination")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigPubsubDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76bd977a5bf8de0bce9d66369d195241b5c1b4fc8080c2fdb34acc48bdb4b3f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdBreaks")
    def put_ad_breaks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigAdBreaks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513edef6817aa7a2b808e7d51c2e84ec1506ee780206afe508f29dcc4f342c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdBreaks", [value]))

    @jsii.member(jsii_name="putEditList")
    def put_edit_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigEditListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378718d4bc35b8764393e1f55b3a174ac17eb94437739f73fe35bb92ba0fe863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEditList", [value]))

    @jsii.member(jsii_name="putElementaryStreams")
    def put_elementary_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigElementaryStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92778e7e3021889385997dee038df59a1f2ed57235c4bed721d7b386a84f3521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElementaryStreams", [value]))

    @jsii.member(jsii_name="putEncryptions")
    def put_encryptions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigEncryptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e092739223c306c6bd097a91a92e638c867a5259f56d476ebd6d1caa948183cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEncryptions", [value]))

    @jsii.member(jsii_name="putInputs")
    def put_inputs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigInputs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ed7f8b0e979cced9a04f5d747187d5c825a38f0f8ae9b69e241270a77ee6ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputs", [value]))

    @jsii.member(jsii_name="putManifests")
    def put_manifests(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigManifests", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8962f320650901de9fffec22b3f82bf1f39cbc11a48938bada21153111523e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManifests", [value]))

    @jsii.member(jsii_name="putMuxStreams")
    def put_mux_streams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigMuxStreams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf4e4a9aa57a8cd679499f789f71c373496c6e66ac0e43dde42643eb6b0ee46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMuxStreams", [value]))

    @jsii.member(jsii_name="putOutput")
    def put_output(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: URI for the output file(s). For example, gs://my-bucket/outputs/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#uri TranscoderJobTemplate#uri}
        '''
        value = TranscoderJobTemplateConfigOutput(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putOutput", [value]))

    @jsii.member(jsii_name="putOverlays")
    def put_overlays(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigOverlays", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017afaf5cf3db31027186f60e7bd396493fe41770125ec3e679b3f438110d929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOverlays", [value]))

    @jsii.member(jsii_name="putPubsubDestination")
    def put_pubsub_destination(
        self,
        *,
        topic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topic: The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#topic TranscoderJobTemplate#topic}
        '''
        value = TranscoderJobTemplateConfigPubsubDestination(topic=topic)

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
    def ad_breaks(self) -> "TranscoderJobTemplateConfigAdBreaksList":
        return typing.cast("TranscoderJobTemplateConfigAdBreaksList", jsii.get(self, "adBreaks"))

    @builtins.property
    @jsii.member(jsii_name="editList")
    def edit_list(self) -> "TranscoderJobTemplateConfigEditListStructList":
        return typing.cast("TranscoderJobTemplateConfigEditListStructList", jsii.get(self, "editList"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreams")
    def elementary_streams(self) -> "TranscoderJobTemplateConfigElementaryStreamsList":
        return typing.cast("TranscoderJobTemplateConfigElementaryStreamsList", jsii.get(self, "elementaryStreams"))

    @builtins.property
    @jsii.member(jsii_name="encryptions")
    def encryptions(self) -> "TranscoderJobTemplateConfigEncryptionsList":
        return typing.cast("TranscoderJobTemplateConfigEncryptionsList", jsii.get(self, "encryptions"))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> "TranscoderJobTemplateConfigInputsList":
        return typing.cast("TranscoderJobTemplateConfigInputsList", jsii.get(self, "inputs"))

    @builtins.property
    @jsii.member(jsii_name="manifests")
    def manifests(self) -> "TranscoderJobTemplateConfigManifestsList":
        return typing.cast("TranscoderJobTemplateConfigManifestsList", jsii.get(self, "manifests"))

    @builtins.property
    @jsii.member(jsii_name="muxStreams")
    def mux_streams(self) -> "TranscoderJobTemplateConfigMuxStreamsList":
        return typing.cast("TranscoderJobTemplateConfigMuxStreamsList", jsii.get(self, "muxStreams"))

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> "TranscoderJobTemplateConfigOutputOutputReference":
        return typing.cast("TranscoderJobTemplateConfigOutputOutputReference", jsii.get(self, "output"))

    @builtins.property
    @jsii.member(jsii_name="overlays")
    def overlays(self) -> "TranscoderJobTemplateConfigOverlaysList":
        return typing.cast("TranscoderJobTemplateConfigOverlaysList", jsii.get(self, "overlays"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestination")
    def pubsub_destination(
        self,
    ) -> "TranscoderJobTemplateConfigPubsubDestinationOutputReference":
        return typing.cast("TranscoderJobTemplateConfigPubsubDestinationOutputReference", jsii.get(self, "pubsubDestination"))

    @builtins.property
    @jsii.member(jsii_name="adBreaksInput")
    def ad_breaks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigAdBreaks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigAdBreaks"]]], jsii.get(self, "adBreaksInput"))

    @builtins.property
    @jsii.member(jsii_name="editListInput")
    def edit_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigEditListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigEditListStruct"]]], jsii.get(self, "editListInput"))

    @builtins.property
    @jsii.member(jsii_name="elementaryStreamsInput")
    def elementary_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigElementaryStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigElementaryStreams"]]], jsii.get(self, "elementaryStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionsInput")
    def encryptions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigEncryptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigEncryptions"]]], jsii.get(self, "encryptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigInputs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigInputs"]]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestsInput")
    def manifests_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigManifests"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigManifests"]]], jsii.get(self, "manifestsInput"))

    @builtins.property
    @jsii.member(jsii_name="muxStreamsInput")
    def mux_streams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigMuxStreams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigMuxStreams"]]], jsii.get(self, "muxStreamsInput"))

    @builtins.property
    @jsii.member(jsii_name="outputInput")
    def output_input(self) -> typing.Optional["TranscoderJobTemplateConfigOutput"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigOutput"], jsii.get(self, "outputInput"))

    @builtins.property
    @jsii.member(jsii_name="overlaysInput")
    def overlays_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigOverlays"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigOverlays"]]], jsii.get(self, "overlaysInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubDestinationInput")
    def pubsub_destination_input(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigPubsubDestination"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigPubsubDestination"], jsii.get(self, "pubsubDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TranscoderJobTemplateConfigA]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8888a1643358dbbd8d3d342cc24c8f6374d4eda35da5f2441365aa10e8a70727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigAdBreaks",
    jsii_struct_bases=[],
    name_mapping={"start_time_offset": "startTimeOffset"},
)
class TranscoderJobTemplateConfigAdBreaks:
    def __init__(
        self,
        *,
        start_time_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param start_time_offset: Start time in seconds for the ad break, relative to the output file timeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#start_time_offset TranscoderJobTemplate#start_time_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5c6edadc95ca36220e52b5cfc9dfd2d9615478a3431a5135d5329206d793b2)
            check_type(argname="argument start_time_offset", value=start_time_offset, expected_type=type_hints["start_time_offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if start_time_offset is not None:
            self._values["start_time_offset"] = start_time_offset

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''Start time in seconds for the ad break, relative to the output file timeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#start_time_offset TranscoderJobTemplate#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigAdBreaks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigAdBreaksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigAdBreaksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59ef08553eb101c0f655c80513b7c2d8465a9d89f6b1a1732483f738df335f6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigAdBreaksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91cded2d83d47eba927003171cfe6f3e34c3dc34590f63a0114ed59599e8cb56)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigAdBreaksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52dcc055962f3621d807e95cde9f493f6d2cea2b30929203497f3a7cd188829)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d85cbc1f3f0653b2bbddcc0bcae6b718c78021b4b570c019fe79e5f0128999ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49c741709c1d87f52728dfa7e3a84460e13af16be75b1700a88070cbf8077c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigAdBreaks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigAdBreaks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigAdBreaks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2468d0d52fbeae805b89e7a6759dd42e0c4d2ea22ab0297e67a04612764b3afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigAdBreaksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigAdBreaksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__065a532c592bb60d9ad06ccd24d5734d5bfbdca038d59c9c5b6b1a86a8d143f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67d15e5b1ff9f4d40cbf6a09a1397aafd201ddba705be3468b4afb97b0da1243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigAdBreaks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigAdBreaks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigAdBreaks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5201944fb9ebe0fa92f8853cb0bd411d5e3658461a0a5779991200ff73c0d33c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEditListStruct",
    jsii_struct_bases=[],
    name_mapping={
        "inputs": "inputs",
        "key": "key",
        "start_time_offset": "startTimeOffset",
    },
)
class TranscoderJobTemplateConfigEditListStruct:
    def __init__(
        self,
        *,
        inputs: typing.Optional[typing.Sequence[builtins.str]] = None,
        key: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inputs: List of values identifying files that should be used in this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#inputs TranscoderJobTemplate#inputs}
        :param key: A unique key for this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#key TranscoderJobTemplate#key}
        :param start_time_offset: Start time in seconds for the atom, relative to the input file timeline. The default is '0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#start_time_offset TranscoderJobTemplate#start_time_offset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264d6bc0ef48fa89aaf03a20cb5521ad8563db3df316862350555cc067391aa6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#inputs TranscoderJobTemplate#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#key TranscoderJobTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''Start time in seconds for the atom, relative to the input file timeline.  The default is '0s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#start_time_offset TranscoderJobTemplate#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEditListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEditListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEditListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd5643e6de1d5d19c0bdcdbce6a597b62ef9fe315b33e4dc0adb02d757af8901)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigEditListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0334693955e5c4f2869add272bfc7b8155301fc7c6373d27e4c690cb6778330)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigEditListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310450d14d48d2a99182559723b2eabdc59b6a80e5486dbd372a1f2d878e4029)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68b4fb5bb4e0b2cf0c6e6f6b9f2d3861e6ab0d76627d3eda9af192e9d6ef8ad3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__369e8cf0c79fa7c7064b81f172a0bc26456018268fa927226abba0f68f2d0146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigEditListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigEditListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigEditListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739906b619aef6a90a4bdf6f539f7a8f670fc8398b1be163e40a36b3b3d3b854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigEditListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEditListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26ad0a5a2f2bc57cf65a6dca9ef6dae889b2f5483c37f9e238fa9ae12f9b08f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__262d10c6b5042cb2338cb750e248da5e37c4742024d3b274574c97a0be660d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740b8a4540c1283660bc4a2f122b2a03a834bc5f0cb0a8148f65cf0294adbc45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59278046822d27cc959f59253a1ce42bca87188b26a34fdbae56cd389e699256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigEditListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigEditListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigEditListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8277a4afcf8b3b3c0bc205c5ab194fdb216e6a07e46dde0b834bbfe470af1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreams",
    jsii_struct_bases=[],
    name_mapping={
        "audio_stream": "audioStream",
        "key": "key",
        "video_stream": "videoStream",
    },
)
class TranscoderJobTemplateConfigElementaryStreams:
    def __init__(
        self,
        *,
        audio_stream: typing.Optional[typing.Union["TranscoderJobTemplateConfigElementaryStreamsAudioStream", typing.Dict[builtins.str, typing.Any]]] = None,
        key: typing.Optional[builtins.str] = None,
        video_stream: typing.Optional[typing.Union["TranscoderJobTemplateConfigElementaryStreamsVideoStream", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_stream: audio_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#audio_stream TranscoderJobTemplate#audio_stream}
        :param key: A unique key for this atom. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#key TranscoderJobTemplate#key}
        :param video_stream: video_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#video_stream TranscoderJobTemplate#video_stream}
        '''
        if isinstance(audio_stream, dict):
            audio_stream = TranscoderJobTemplateConfigElementaryStreamsAudioStream(**audio_stream)
        if isinstance(video_stream, dict):
            video_stream = TranscoderJobTemplateConfigElementaryStreamsVideoStream(**video_stream)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e18ed9ac680731d0b1cc060e6ebc75d8e25a3a4b6e579db0792c05ad8c43ff6a)
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
    ) -> typing.Optional["TranscoderJobTemplateConfigElementaryStreamsAudioStream"]:
        '''audio_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#audio_stream TranscoderJobTemplate#audio_stream}
        '''
        result = self._values.get("audio_stream")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigElementaryStreamsAudioStream"], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this atom.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#key TranscoderJobTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def video_stream(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStream"]:
        '''video_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#video_stream TranscoderJobTemplate#video_stream}
        '''
        result = self._values.get("video_stream")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStream"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigElementaryStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsAudioStream",
    jsii_struct_bases=[],
    name_mapping={
        "bitrate_bps": "bitrateBps",
        "channel_count": "channelCount",
        "channel_layout": "channelLayout",
        "codec": "codec",
        "sample_rate_hertz": "sampleRateHertz",
    },
)
class TranscoderJobTemplateConfigElementaryStreamsAudioStream:
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
        :param bitrate_bps: Audio bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#bitrate_bps TranscoderJobTemplate#bitrate_bps}
        :param channel_count: Number of audio channels. The default is '2'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#channel_count TranscoderJobTemplate#channel_count}
        :param channel_layout: A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#channel_layout TranscoderJobTemplate#channel_layout}
        :param codec: The codec for this audio stream. The default is 'aac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#codec TranscoderJobTemplate#codec}
        :param sample_rate_hertz: The audio sample rate in Hertz. The default is '48000'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#sample_rate_hertz TranscoderJobTemplate#sample_rate_hertz}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f997f98a422ff83b875ace2685de3076ca32a426f512ac5879dde995e30bc3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#bitrate_bps TranscoderJobTemplate#bitrate_bps}
        '''
        result = self._values.get("bitrate_bps")
        assert result is not None, "Required property 'bitrate_bps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def channel_count(self) -> typing.Optional[jsii.Number]:
        '''Number of audio channels. The default is '2'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#channel_count TranscoderJobTemplate#channel_count}
        '''
        result = self._values.get("channel_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def channel_layout(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of channel names specifying layout of the audio channels.  The default is ["fl", "fr"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#channel_layout TranscoderJobTemplate#channel_layout}
        '''
        result = self._values.get("channel_layout")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def codec(self) -> typing.Optional[builtins.str]:
        '''The codec for this audio stream. The default is 'aac'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#codec TranscoderJobTemplate#codec}
        '''
        result = self._values.get("codec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate_hertz(self) -> typing.Optional[jsii.Number]:
        '''The audio sample rate in Hertz. The default is '48000'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#sample_rate_hertz TranscoderJobTemplate#sample_rate_hertz}
        '''
        result = self._values.get("sample_rate_hertz")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigElementaryStreamsAudioStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__060eba394648af2ebe507baf3be3a57ef8dcf666b817251faca698a3f4990180)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d4c828c3c96edee233bb69b14399e41f19d8107a8ffb8c4ea735d85b1a80d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitrateBps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelCount")
    def channel_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "channelCount"))

    @channel_count.setter
    def channel_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d35e4755c8499bbdff745eaa8da9d799b57003a96df7e72eb163cca6532c92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelLayout")
    def channel_layout(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "channelLayout"))

    @channel_layout.setter
    def channel_layout(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09338f5b914ae0330e1373ba1eb970f7aa1d58ac2a56ab8aedc75b975a6bb151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelLayout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codec")
    def codec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codec"))

    @codec.setter
    def codec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96af2a1a41c2355b5ccaa1ade6c4ed703aed9ab905deeaf5587b485d3fedcd17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRateHertz")
    def sample_rate_hertz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRateHertz"))

    @sample_rate_hertz.setter
    def sample_rate_hertz(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8416b02ebc081999612fc725ed5dc12e1336005095f75a814c47f8c7514be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRateHertz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigElementaryStreamsAudioStream]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigElementaryStreamsAudioStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsAudioStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c4282aea922c85c6846c5d1c217a2951d696caf79f42fe35ae93148f4bab30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigElementaryStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2de3d3655d75207e423933d0b58bc16c9b54ae5cfffb3bd942e414238dbde835)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigElementaryStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b25d8f00918fdeb924d95d85a3d939ceb78e20380f0a8fecfba08199598f6dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigElementaryStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39031cf0857c401fee7045e848540abf145cdcfdb1a492b698cbf03003baf304)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a2083128d514646d1b732ed0accc76108eb12274a42ff42377e2afaec41d9bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3daf41d3933eef8e8490eb74062452a13e5158b5d24804a90c7045d9e3d3cc26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigElementaryStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigElementaryStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigElementaryStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc6bb316af0b03219dd87d1f3536db344ae55284b58bfc5ead3fe1e159e853b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigElementaryStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__570993684365e37e258eabd6875fe03d50a0f77e5f30684e85bc8669a921e47c)
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
        :param bitrate_bps: Audio bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#bitrate_bps TranscoderJobTemplate#bitrate_bps}
        :param channel_count: Number of audio channels. The default is '2'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#channel_count TranscoderJobTemplate#channel_count}
        :param channel_layout: A list of channel names specifying layout of the audio channels. The default is ["fl", "fr"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#channel_layout TranscoderJobTemplate#channel_layout}
        :param codec: The codec for this audio stream. The default is 'aac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#codec TranscoderJobTemplate#codec}
        :param sample_rate_hertz: The audio sample rate in Hertz. The default is '48000'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#sample_rate_hertz TranscoderJobTemplate#sample_rate_hertz}
        '''
        value = TranscoderJobTemplateConfigElementaryStreamsAudioStream(
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
        h264: typing.Optional[typing.Union["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param h264: h264 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#h264 TranscoderJobTemplate#h264}
        '''
        value = TranscoderJobTemplateConfigElementaryStreamsVideoStream(h264=h264)

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
    ) -> TranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference:
        return typing.cast(TranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference, jsii.get(self, "audioStream"))

    @builtins.property
    @jsii.member(jsii_name="videoStream")
    def video_stream(
        self,
    ) -> "TranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference":
        return typing.cast("TranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference", jsii.get(self, "videoStream"))

    @builtins.property
    @jsii.member(jsii_name="audioStreamInput")
    def audio_stream_input(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigElementaryStreamsAudioStream]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigElementaryStreamsAudioStream], jsii.get(self, "audioStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="videoStreamInput")
    def video_stream_input(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStream"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStream"], jsii.get(self, "videoStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c59b47734ba06ecd909e6f129063b54aa2e226f6bfa1e1996a60559e65e47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigElementaryStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigElementaryStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigElementaryStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c3ec5850467d356f171edf432e839eb930451eecf71da73909ea3e6c10492f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsVideoStream",
    jsii_struct_bases=[],
    name_mapping={"h264": "h264"},
)
class TranscoderJobTemplateConfigElementaryStreamsVideoStream:
    def __init__(
        self,
        *,
        h264: typing.Optional[typing.Union["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param h264: h264 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#h264 TranscoderJobTemplate#h264}
        '''
        if isinstance(h264, dict):
            h264 = TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264(**h264)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f8f3593102f04f526b5f1a745f372446db9f70d64fc8869a7c239dc1426b01)
            check_type(argname="argument h264", value=h264, expected_type=type_hints["h264"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if h264 is not None:
            self._values["h264"] = h264

    @builtins.property
    def h264(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264"]:
        '''h264 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#h264 TranscoderJobTemplate#h264}
        '''
        result = self._values.get("h264")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigElementaryStreamsVideoStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264",
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
class TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264:
    def __init__(
        self,
        *,
        bitrate_bps: jsii.Number,
        frame_rate: jsii.Number,
        crf_level: typing.Optional[jsii.Number] = None,
        entropy_coder: typing.Optional[builtins.str] = None,
        gop_duration: typing.Optional[builtins.str] = None,
        height_pixels: typing.Optional[jsii.Number] = None,
        hlg: typing.Optional[typing.Union["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg", typing.Dict[builtins.str, typing.Any]]] = None,
        pixel_format: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        rate_control_mode: typing.Optional[builtins.str] = None,
        sdr: typing.Optional[typing.Union["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr", typing.Dict[builtins.str, typing.Any]]] = None,
        vbv_fullness_bits: typing.Optional[jsii.Number] = None,
        vbv_size_bits: typing.Optional[jsii.Number] = None,
        width_pixels: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: The video bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#bitrate_bps TranscoderJobTemplate#bitrate_bps}
        :param frame_rate: The target video frame rate in frames per second (FPS). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#frame_rate TranscoderJobTemplate#frame_rate}
        :param crf_level: Target CRF level. The default is '21'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#crf_level TranscoderJobTemplate#crf_level}
        :param entropy_coder: The entropy coder to use. The default is 'cabac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#entropy_coder TranscoderJobTemplate#entropy_coder}
        :param gop_duration: Select the GOP size based on the specified duration. The default is '3s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#gop_duration TranscoderJobTemplate#gop_duration}
        :param height_pixels: The height of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#height_pixels TranscoderJobTemplate#height_pixels}
        :param hlg: hlg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#hlg TranscoderJobTemplate#hlg}
        :param pixel_format: Pixel format to use. The default is 'yuv420p'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#pixel_format TranscoderJobTemplate#pixel_format}
        :param preset: Enforces the specified codec preset. The default is 'veryfast'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#preset TranscoderJobTemplate#preset}
        :param profile: Enforces the specified codec profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#profile TranscoderJobTemplate#profile}
        :param rate_control_mode: Specify the mode. The default is 'vbr'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#rate_control_mode TranscoderJobTemplate#rate_control_mode}
        :param sdr: sdr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#sdr TranscoderJobTemplate#sdr}
        :param vbv_fullness_bits: Initial fullness of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#vbv_fullness_bits TranscoderJobTemplate#vbv_fullness_bits}
        :param vbv_size_bits: Size of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#vbv_size_bits TranscoderJobTemplate#vbv_size_bits}
        :param width_pixels: The width of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#width_pixels TranscoderJobTemplate#width_pixels}
        '''
        if isinstance(hlg, dict):
            hlg = TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg(**hlg)
        if isinstance(sdr, dict):
            sdr = TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr(**sdr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdfcfefe79f07f6ef3c5db530863129a838829155bd6e7ff09cba338711ef39)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#bitrate_bps TranscoderJobTemplate#bitrate_bps}
        '''
        result = self._values.get("bitrate_bps")
        assert result is not None, "Required property 'bitrate_bps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frame_rate(self) -> jsii.Number:
        '''The target video frame rate in frames per second (FPS).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#frame_rate TranscoderJobTemplate#frame_rate}
        '''
        result = self._values.get("frame_rate")
        assert result is not None, "Required property 'frame_rate' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def crf_level(self) -> typing.Optional[jsii.Number]:
        '''Target CRF level. The default is '21'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#crf_level TranscoderJobTemplate#crf_level}
        '''
        result = self._values.get("crf_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def entropy_coder(self) -> typing.Optional[builtins.str]:
        '''The entropy coder to use. The default is 'cabac'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#entropy_coder TranscoderJobTemplate#entropy_coder}
        '''
        result = self._values.get("entropy_coder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gop_duration(self) -> typing.Optional[builtins.str]:
        '''Select the GOP size based on the specified duration. The default is '3s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#gop_duration TranscoderJobTemplate#gop_duration}
        '''
        result = self._values.get("gop_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def height_pixels(self) -> typing.Optional[jsii.Number]:
        '''The height of the video in pixels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#height_pixels TranscoderJobTemplate#height_pixels}
        '''
        result = self._values.get("height_pixels")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hlg(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg"]:
        '''hlg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#hlg TranscoderJobTemplate#hlg}
        '''
        result = self._values.get("hlg")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg"], result)

    @builtins.property
    def pixel_format(self) -> typing.Optional[builtins.str]:
        '''Pixel format to use. The default is 'yuv420p'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#pixel_format TranscoderJobTemplate#pixel_format}
        '''
        result = self._values.get("pixel_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preset(self) -> typing.Optional[builtins.str]:
        '''Enforces the specified codec preset. The default is 'veryfast'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#preset TranscoderJobTemplate#preset}
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Enforces the specified codec profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#profile TranscoderJobTemplate#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_control_mode(self) -> typing.Optional[builtins.str]:
        '''Specify the mode. The default is 'vbr'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#rate_control_mode TranscoderJobTemplate#rate_control_mode}
        '''
        result = self._values.get("rate_control_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sdr(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr"]:
        '''sdr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#sdr TranscoderJobTemplate#sdr}
        '''
        result = self._values.get("sdr")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr"], result)

    @builtins.property
    def vbv_fullness_bits(self) -> typing.Optional[jsii.Number]:
        '''Initial fullness of the Video Buffering Verifier (VBV) buffer in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#vbv_fullness_bits TranscoderJobTemplate#vbv_fullness_bits}
        '''
        result = self._values.get("vbv_fullness_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vbv_size_bits(self) -> typing.Optional[jsii.Number]:
        '''Size of the Video Buffering Verifier (VBV) buffer in bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#vbv_size_bits TranscoderJobTemplate#vbv_size_bits}
        '''
        result = self._values.get("vbv_size_bits")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def width_pixels(self) -> typing.Optional[jsii.Number]:
        '''The width of the video in pixels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#width_pixels TranscoderJobTemplate#width_pixels}
        '''
        result = self._values.get("width_pixels")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__727bd9010e63c5ba4eff6747349afc27746d73bf660d56725a5041884e2f31c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17f01d1231cc4523e19178ce2557d27444f21c9ce75da99a0f908e6b36bf00a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b5189848a1c2654866eb6780ec5c870fe90799bd53e17532213daa163f2f2bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHlg")
    def put_hlg(self) -> None:
        value = TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg()

        return typing.cast(None, jsii.invoke(self, "putHlg", [value]))

    @jsii.member(jsii_name="putSdr")
    def put_sdr(self) -> None:
        value = TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr()

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
    ) -> TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference:
        return typing.cast(TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference, jsii.get(self, "hlg"))

    @builtins.property
    @jsii.member(jsii_name="sdr")
    def sdr(
        self,
    ) -> "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference":
        return typing.cast("TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference", jsii.get(self, "sdr"))

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
    ) -> typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg], jsii.get(self, "hlgInput"))

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
    ) -> typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr"], jsii.get(self, "sdrInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3cfac3d2d83161ace4ce6622ee2ff2fd67dfbec42a30f273b388fb3396210bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitrateBps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crfLevel")
    def crf_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "crfLevel"))

    @crf_level.setter
    def crf_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b39da567a8108c0bd5e5fce490189983435e60c306813647c46666f6461f71a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crfLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entropyCoder")
    def entropy_coder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entropyCoder"))

    @entropy_coder.setter
    def entropy_coder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fabb14dc83774c8fda99046b72141587d1be75eaf746bf8ce4ba37fb48487cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entropyCoder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frameRate")
    def frame_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frameRate"))

    @frame_rate.setter
    def frame_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398801ef70fccfec093e84f6d0be4872306ac1d8725c0e99e15c4ec4c9622fdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gopDuration")
    def gop_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gopDuration"))

    @gop_duration.setter
    def gop_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c826a4f1f2c779bc38538f434d9933a172e73c0f6cc0879e68b4b020e29a6d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gopDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="heightPixels")
    def height_pixels(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "heightPixels"))

    @height_pixels.setter
    def height_pixels(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea2d51a496af6549d8307faa598dd521152e639451cfd883d91a30eee5cd58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "heightPixels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pixelFormat")
    def pixel_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pixelFormat"))

    @pixel_format.setter
    def pixel_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00737ce28b27344ce2b372ee0339af8cb61696512ce6ff2fea2d27d3c15a86e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pixelFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preset")
    def preset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preset"))

    @preset.setter
    def preset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b023936ea461c257aa224a634c690d7ce284764ca8a30af0c4ffbfb7cec5f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdc629c3d580b236e22ea681ed36793369448bece8183cb97728a020070e326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rateControlMode")
    def rate_control_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rateControlMode"))

    @rate_control_mode.setter
    def rate_control_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48478a5aa9dff27b771fe3e6089dd1244802a387583fe0e753d0c90cdf48f99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateControlMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vbvFullnessBits")
    def vbv_fullness_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vbvFullnessBits"))

    @vbv_fullness_bits.setter
    def vbv_fullness_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a290c3468e3dcbbb0b70f9b7236990df06c6d6602a5d55c71c562c93c7900f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vbvFullnessBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vbvSizeBits")
    def vbv_size_bits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vbvSizeBits"))

    @vbv_size_bits.setter
    def vbv_size_bits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbe1c5a22f248dd23536b24444a1bc94b6b7ccb0acdff7e78f6546c56543303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vbvSizeBits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="widthPixels")
    def width_pixels(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "widthPixels"))

    @width_pixels.setter
    def width_pixels(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5737dbc474a1295ec57d3c6eb274290795529865104b9bc70a396b84be3978d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "widthPixels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300a25a58a4661ef9c04280095ebc125d758544c85002f19fb9882b3d42e0397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f30210689b03e7c597f5ef083209fdcfa71d8340de432e17875eaa76e72234a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dea1eac5e2629de9265d45fff339c825f3f8448721848a627a8ccbb21d58892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__584cfb7a03c09485fb5b478e791f04c1c671ed75df6265a5e03241f1d31a874d)
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
        hlg: typing.Optional[typing.Union[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg, typing.Dict[builtins.str, typing.Any]]] = None,
        pixel_format: typing.Optional[builtins.str] = None,
        preset: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        rate_control_mode: typing.Optional[builtins.str] = None,
        sdr: typing.Optional[typing.Union[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr, typing.Dict[builtins.str, typing.Any]]] = None,
        vbv_fullness_bits: typing.Optional[jsii.Number] = None,
        vbv_size_bits: typing.Optional[jsii.Number] = None,
        width_pixels: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bitrate_bps: The video bitrate in bits per second. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#bitrate_bps TranscoderJobTemplate#bitrate_bps}
        :param frame_rate: The target video frame rate in frames per second (FPS). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#frame_rate TranscoderJobTemplate#frame_rate}
        :param crf_level: Target CRF level. The default is '21'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#crf_level TranscoderJobTemplate#crf_level}
        :param entropy_coder: The entropy coder to use. The default is 'cabac'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#entropy_coder TranscoderJobTemplate#entropy_coder}
        :param gop_duration: Select the GOP size based on the specified duration. The default is '3s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#gop_duration TranscoderJobTemplate#gop_duration}
        :param height_pixels: The height of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#height_pixels TranscoderJobTemplate#height_pixels}
        :param hlg: hlg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#hlg TranscoderJobTemplate#hlg}
        :param pixel_format: Pixel format to use. The default is 'yuv420p'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#pixel_format TranscoderJobTemplate#pixel_format}
        :param preset: Enforces the specified codec preset. The default is 'veryfast'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#preset TranscoderJobTemplate#preset}
        :param profile: Enforces the specified codec profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#profile TranscoderJobTemplate#profile}
        :param rate_control_mode: Specify the mode. The default is 'vbr'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#rate_control_mode TranscoderJobTemplate#rate_control_mode}
        :param sdr: sdr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#sdr TranscoderJobTemplate#sdr}
        :param vbv_fullness_bits: Initial fullness of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#vbv_fullness_bits TranscoderJobTemplate#vbv_fullness_bits}
        :param vbv_size_bits: Size of the Video Buffering Verifier (VBV) buffer in bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#vbv_size_bits TranscoderJobTemplate#vbv_size_bits}
        :param width_pixels: The width of the video in pixels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#width_pixels TranscoderJobTemplate#width_pixels}
        '''
        value = TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264(
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
    ) -> TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference:
        return typing.cast(TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference, jsii.get(self, "h264"))

    @builtins.property
    @jsii.member(jsii_name="h264Input")
    def h264_input(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264], jsii.get(self, "h264Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStream]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb16bb1127852f958788179a497a0d2089f70b9d0d39c7d1800434c2f82291c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptions",
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
class TranscoderJobTemplateConfigEncryptions:
    def __init__(
        self,
        *,
        id: builtins.str,
        aes128: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsAes128", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_systems: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsDrmSystems", typing.Dict[builtins.str, typing.Any]]] = None,
        mpeg_cenc: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsMpegCenc", typing.Dict[builtins.str, typing.Any]]] = None,
        sample_aes: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsSampleAes", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_manager_key_source: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Identifier for this set of encryption options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#id TranscoderJobTemplate#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param aes128: aes128 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#aes128 TranscoderJobTemplate#aes128}
        :param drm_systems: drm_systems block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#drm_systems TranscoderJobTemplate#drm_systems}
        :param mpeg_cenc: mpeg_cenc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#mpeg_cenc TranscoderJobTemplate#mpeg_cenc}
        :param sample_aes: sample_aes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#sample_aes TranscoderJobTemplate#sample_aes}
        :param secret_manager_key_source: secret_manager_key_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#secret_manager_key_source TranscoderJobTemplate#secret_manager_key_source}
        '''
        if isinstance(aes128, dict):
            aes128 = TranscoderJobTemplateConfigEncryptionsAes128(**aes128)
        if isinstance(drm_systems, dict):
            drm_systems = TranscoderJobTemplateConfigEncryptionsDrmSystems(**drm_systems)
        if isinstance(mpeg_cenc, dict):
            mpeg_cenc = TranscoderJobTemplateConfigEncryptionsMpegCenc(**mpeg_cenc)
        if isinstance(sample_aes, dict):
            sample_aes = TranscoderJobTemplateConfigEncryptionsSampleAes(**sample_aes)
        if isinstance(secret_manager_key_source, dict):
            secret_manager_key_source = TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource(**secret_manager_key_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf6ae8376dc4ac3993e208596b8f28b3c2f8ab58941e8a61981dae678f56580)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#id TranscoderJobTemplate#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aes128(self) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsAes128"]:
        '''aes128 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#aes128 TranscoderJobTemplate#aes128}
        '''
        result = self._values.get("aes128")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsAes128"], result)

    @builtins.property
    def drm_systems(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystems"]:
        '''drm_systems block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#drm_systems TranscoderJobTemplate#drm_systems}
        '''
        result = self._values.get("drm_systems")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystems"], result)

    @builtins.property
    def mpeg_cenc(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsMpegCenc"]:
        '''mpeg_cenc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#mpeg_cenc TranscoderJobTemplate#mpeg_cenc}
        '''
        result = self._values.get("mpeg_cenc")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsMpegCenc"], result)

    @builtins.property
    def sample_aes(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsSampleAes"]:
        '''sample_aes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#sample_aes TranscoderJobTemplate#sample_aes}
        '''
        result = self._values.get("sample_aes")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsSampleAes"], result)

    @builtins.property
    def secret_manager_key_source(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource"]:
        '''secret_manager_key_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#secret_manager_key_source TranscoderJobTemplate#secret_manager_key_source}
        '''
        result = self._values.get("secret_manager_key_source")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsAes128",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobTemplateConfigEncryptionsAes128:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsAes128(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEncryptionsAes128OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsAes128OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff4826c0fa17db951354a6f1439976e1404658847b52d314cd9c57c6a6dd2c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsAes128]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsAes128], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsAes128],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e879fc5fc3b0687f98c4095ad56c8775b9c70c4e73df4fafd97fac418ee489f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystems",
    jsii_struct_bases=[],
    name_mapping={
        "clearkey": "clearkey",
        "fairplay": "fairplay",
        "playready": "playready",
        "widevine": "widevine",
    },
)
class TranscoderJobTemplateConfigEncryptionsDrmSystems:
    def __init__(
        self,
        *,
        clearkey: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey", typing.Dict[builtins.str, typing.Any]]] = None,
        fairplay: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay", typing.Dict[builtins.str, typing.Any]]] = None,
        playready: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready", typing.Dict[builtins.str, typing.Any]]] = None,
        widevine: typing.Optional[typing.Union["TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clearkey: clearkey block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#clearkey TranscoderJobTemplate#clearkey}
        :param fairplay: fairplay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#fairplay TranscoderJobTemplate#fairplay}
        :param playready: playready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#playready TranscoderJobTemplate#playready}
        :param widevine: widevine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#widevine TranscoderJobTemplate#widevine}
        '''
        if isinstance(clearkey, dict):
            clearkey = TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey(**clearkey)
        if isinstance(fairplay, dict):
            fairplay = TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay(**fairplay)
        if isinstance(playready, dict):
            playready = TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready(**playready)
        if isinstance(widevine, dict):
            widevine = TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine(**widevine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9221d0ea8b781ddba54353805044bf4c4b982af7b0441cb51da48346d0589cc2)
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
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey"]:
        '''clearkey block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#clearkey TranscoderJobTemplate#clearkey}
        '''
        result = self._values.get("clearkey")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey"], result)

    @builtins.property
    def fairplay(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay"]:
        '''fairplay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#fairplay TranscoderJobTemplate#fairplay}
        '''
        result = self._values.get("fairplay")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay"], result)

    @builtins.property
    def playready(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready"]:
        '''playready block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#playready TranscoderJobTemplate#playready}
        '''
        result = self._values.get("playready")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready"], result)

    @builtins.property
    def widevine(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine"]:
        '''widevine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#widevine TranscoderJobTemplate#widevine}
        '''
        result = self._values.get("widevine")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsDrmSystems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e169bb9c086fa5775970485cd7e7982253d412f49782ab71c537d5de6a55d555)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab0745ceb252e00ea52de422a65168a4dab39ef56bcaef2278c847f32d1ee7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b9a9ce381b4bff1b23b29f47626b07c448864e3216c88a83936bde73575a2ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b715362ea473807cb69e420f36fb85e1b73aa27417ffe97d96e8f09ea84879b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02eeb1f34bce0605dfc459a27d48d09f5c351a6de0208f3ccdf70863ae0a6e8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClearkey")
    def put_clearkey(self) -> None:
        value = TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey()

        return typing.cast(None, jsii.invoke(self, "putClearkey", [value]))

    @jsii.member(jsii_name="putFairplay")
    def put_fairplay(self) -> None:
        value = TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay()

        return typing.cast(None, jsii.invoke(self, "putFairplay", [value]))

    @jsii.member(jsii_name="putPlayready")
    def put_playready(self) -> None:
        value = TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready()

        return typing.cast(None, jsii.invoke(self, "putPlayready", [value]))

    @jsii.member(jsii_name="putWidevine")
    def put_widevine(self) -> None:
        value = TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine()

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
    ) -> TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference:
        return typing.cast(TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference, jsii.get(self, "clearkey"))

    @builtins.property
    @jsii.member(jsii_name="fairplay")
    def fairplay(
        self,
    ) -> TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference:
        return typing.cast(TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference, jsii.get(self, "fairplay"))

    @builtins.property
    @jsii.member(jsii_name="playready")
    def playready(
        self,
    ) -> "TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference":
        return typing.cast("TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference", jsii.get(self, "playready"))

    @builtins.property
    @jsii.member(jsii_name="widevine")
    def widevine(
        self,
    ) -> "TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference":
        return typing.cast("TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference", jsii.get(self, "widevine"))

    @builtins.property
    @jsii.member(jsii_name="clearkeyInput")
    def clearkey_input(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey], jsii.get(self, "clearkeyInput"))

    @builtins.property
    @jsii.member(jsii_name="fairplayInput")
    def fairplay_input(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay], jsii.get(self, "fairplayInput"))

    @builtins.property
    @jsii.member(jsii_name="playreadyInput")
    def playready_input(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready"], jsii.get(self, "playreadyInput"))

    @builtins.property
    @jsii.member(jsii_name="widevineInput")
    def widevine_input(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine"], jsii.get(self, "widevineInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystems]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystems], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystems],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45462148306bef0a1dc1a52aaec62f1321d4fb0c4f9a2d7ad097f78636791664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__383a3f1bad2985086a3afd366fd28676fdf31b720b6609a63610d02b18fb34e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ba2ee23daee96d5fd1fa03a351189fdf782c225b6def49588effe20922650c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b785df258b627bf3fbe961d6dfac75c59b467efbee04abd7f403e191e03b8ad8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1acb73eceb227393ff6c6cbfa1bd161211d95785f97d7b55367f1856f24d291f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigEncryptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1d3dd9ac5e284c3085c8a3e506ab721a32d28ca5eefa895dd8f9b731a5c3806)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigEncryptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1cae0280f768011673e6f1b55a5ead15c0b70b00542a343821785a0dcde49e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigEncryptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa7176abc5bb05869be544bc5ed775dcba9158ea32cb7670c077e7fba279bd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8920b6d7b3028c08feb275c6ba9952d0971392b93f4bdc083d374894d43747b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8783683edb8af4602b373a0e14b1d4622d5bc10010c1e264de34b92bde26e08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigEncryptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigEncryptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigEncryptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a2a709aff5f43b7569caf3d857d638a3bddba0b718d43a80faf959e49b85a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsMpegCenc",
    jsii_struct_bases=[],
    name_mapping={"scheme": "scheme"},
)
class TranscoderJobTemplateConfigEncryptionsMpegCenc:
    def __init__(self, *, scheme: builtins.str) -> None:
        '''
        :param scheme: Specify the encryption scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#scheme TranscoderJobTemplate#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391fcde7cc0207ce20a3e71c2ace30741d22e3692b8a5344745c7ef3f8a6cc63)
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scheme": scheme,
        }

    @builtins.property
    def scheme(self) -> builtins.str:
        '''Specify the encryption scheme.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#scheme TranscoderJobTemplate#scheme}
        '''
        result = self._values.get("scheme")
        assert result is not None, "Required property 'scheme' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsMpegCenc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEncryptionsMpegCencOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsMpegCencOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c46c875e7f0ed6689a7d73bac59f9c810bd699d8d00551a335a6401868efdb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eb09e82714a547a2ea4f5394320ab0af54e12bc828dad672ebbc263f65321a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsMpegCenc]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsMpegCenc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsMpegCenc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc02c6bda45b0ec5cdd160243e78593145cf6933053eb1d2a469be784c6be45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigEncryptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a46203c07ab668e35f2f624aee335dea1d0ef566b852caaa86cff2f8fde6cb08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAes128")
    def put_aes128(self) -> None:
        value = TranscoderJobTemplateConfigEncryptionsAes128()

        return typing.cast(None, jsii.invoke(self, "putAes128", [value]))

    @jsii.member(jsii_name="putDrmSystems")
    def put_drm_systems(
        self,
        *,
        clearkey: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey, typing.Dict[builtins.str, typing.Any]]] = None,
        fairplay: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
        playready: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
        widevine: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param clearkey: clearkey block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#clearkey TranscoderJobTemplate#clearkey}
        :param fairplay: fairplay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#fairplay TranscoderJobTemplate#fairplay}
        :param playready: playready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#playready TranscoderJobTemplate#playready}
        :param widevine: widevine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#widevine TranscoderJobTemplate#widevine}
        '''
        value = TranscoderJobTemplateConfigEncryptionsDrmSystems(
            clearkey=clearkey,
            fairplay=fairplay,
            playready=playready,
            widevine=widevine,
        )

        return typing.cast(None, jsii.invoke(self, "putDrmSystems", [value]))

    @jsii.member(jsii_name="putMpegCenc")
    def put_mpeg_cenc(self, *, scheme: builtins.str) -> None:
        '''
        :param scheme: Specify the encryption scheme. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#scheme TranscoderJobTemplate#scheme}
        '''
        value = TranscoderJobTemplateConfigEncryptionsMpegCenc(scheme=scheme)

        return typing.cast(None, jsii.invoke(self, "putMpegCenc", [value]))

    @jsii.member(jsii_name="putSampleAes")
    def put_sample_aes(self) -> None:
        value = TranscoderJobTemplateConfigEncryptionsSampleAes()

        return typing.cast(None, jsii.invoke(self, "putSampleAes", [value]))

    @jsii.member(jsii_name="putSecretManagerKeySource")
    def put_secret_manager_key_source(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#secret_version TranscoderJobTemplate#secret_version}
        '''
        value = TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource(
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
    def aes128(self) -> TranscoderJobTemplateConfigEncryptionsAes128OutputReference:
        return typing.cast(TranscoderJobTemplateConfigEncryptionsAes128OutputReference, jsii.get(self, "aes128"))

    @builtins.property
    @jsii.member(jsii_name="drmSystems")
    def drm_systems(
        self,
    ) -> TranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference:
        return typing.cast(TranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference, jsii.get(self, "drmSystems"))

    @builtins.property
    @jsii.member(jsii_name="mpegCenc")
    def mpeg_cenc(
        self,
    ) -> TranscoderJobTemplateConfigEncryptionsMpegCencOutputReference:
        return typing.cast(TranscoderJobTemplateConfigEncryptionsMpegCencOutputReference, jsii.get(self, "mpegCenc"))

    @builtins.property
    @jsii.member(jsii_name="sampleAes")
    def sample_aes(
        self,
    ) -> "TranscoderJobTemplateConfigEncryptionsSampleAesOutputReference":
        return typing.cast("TranscoderJobTemplateConfigEncryptionsSampleAesOutputReference", jsii.get(self, "sampleAes"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerKeySource")
    def secret_manager_key_source(
        self,
    ) -> "TranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference":
        return typing.cast("TranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference", jsii.get(self, "secretManagerKeySource"))

    @builtins.property
    @jsii.member(jsii_name="aes128Input")
    def aes128_input(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsAes128]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsAes128], jsii.get(self, "aes128Input"))

    @builtins.property
    @jsii.member(jsii_name="drmSystemsInput")
    def drm_systems_input(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystems]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystems], jsii.get(self, "drmSystemsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mpegCencInput")
    def mpeg_cenc_input(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsMpegCenc]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsMpegCenc], jsii.get(self, "mpegCencInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleAesInput")
    def sample_aes_input(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsSampleAes"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsSampleAes"], jsii.get(self, "sampleAesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretManagerKeySourceInput")
    def secret_manager_key_source_input(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource"], jsii.get(self, "secretManagerKeySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e3419a55bc3c91204a519f0034856b9eeda4e27cc76b7fb632a6e50be89535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigEncryptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigEncryptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigEncryptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ccbd69b11635a1595443a6888b1fb36356f208cb5f81c6e0edc39c737a0681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsSampleAes",
    jsii_struct_bases=[],
    name_mapping={},
)
class TranscoderJobTemplateConfigEncryptionsSampleAes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsSampleAes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEncryptionsSampleAesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsSampleAesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55b50ef511268a9c0c35f3a2281c54210f79cfe09b7bb16a4a11fd3ec15eee1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsSampleAes]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsSampleAes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsSampleAes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55aa1920516e17c7fa30b7fb0bb111f22d64b2fdb8b82042fe61768ecf247619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#secret_version TranscoderJobTemplate#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8416e2ce33897740fca0704fc74303c09cabe54e8535b48e3085d1c25660bca5)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The name of the Secret Version containing the encryption key in the following format: projects/{project}/secrets/{secret_id}/versions/{version_number}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#secret_version TranscoderJobTemplate#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8722178fd7cad1f3fea870c62494d4a83739165c99c8f920b72dc6eb4f5240ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cb9d54c6cbdcb6079d74bb40c6fce98349e881238bc263b48f45d64d6dfc58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfde0aa80532c2f6585dcc04933363c6c0c8d4fc6a26db4048e236f28b947b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigInputs",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "uri": "uri"},
)
class TranscoderJobTemplateConfigInputs:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: A unique key for this input. Must be specified when using advanced mapping and edit lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#key TranscoderJobTemplate#key}
        :param uri: URI of the media. Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, gs://bucket/inputs/file.mp4). If empty, the value is populated from Job.input_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#uri TranscoderJobTemplate#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563bde1254bd735fb6313081ded1f411209bd7793db4bafc9cde5788ad95fe10)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#key TranscoderJobTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI of the media.

        Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, gs://bucket/inputs/file.mp4).
        If empty, the value is populated from Job.input_uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#uri TranscoderJobTemplate#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigInputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigInputsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigInputsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6fc422ce158bd58c59136dd2cc8ef59943ccdfbd3c39ed073b9b8423ef5ce7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigInputsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c288a00f402fae3e8d33d2f2ddca521cef09088d9de448bda5e99391b82b105)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigInputsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49a16dc82a7d98c65f0ed94e310d01e649fa32e7c35b51a4292de594be66794)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b3e73d65d11f9da68179b900e25101789816ffeb0b293cfe02576d5d04ad385)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5628c27754403d133efe2c3b794c08f243ed9b74676fbd15cc5db44a97f7b0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigInputs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigInputs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigInputs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abed7a70b269a4116301c54c47747c0fe59529bae8392c85d343c691443bdd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigInputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigInputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8479844506873589ff3bcf6fe517f8f8d13312ca2e2e391762106ab20edfd347)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67692380fbafeac76b046f51421743c03f4f69c1826d8270e99f55e8e23a0aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e33b06cfab23043f1d2ff20c1e1fa2d5ff56919bdf5524b7437df73afb87d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigInputs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigInputs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigInputs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786d6e6246a847907bbabb056b5e90886d497e450f88ae7e849e8eb3cc45e0a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigManifests",
    jsii_struct_bases=[],
    name_mapping={
        "file_name": "fileName",
        "mux_streams": "muxStreams",
        "type": "type",
    },
)
class TranscoderJobTemplateConfigManifests:
    def __init__(
        self,
        *,
        file_name: typing.Optional[builtins.str] = None,
        mux_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_name: The name of the generated file. The default is 'manifest'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#file_name TranscoderJobTemplate#file_name}
        :param mux_streams: List of user supplied MuxStream.key values that should appear in this manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#mux_streams TranscoderJobTemplate#mux_streams}
        :param type: Type of the manifest. Possible values: ["MANIFEST_TYPE_UNSPECIFIED", "HLS", "DASH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#type TranscoderJobTemplate#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ea6da9630114869c4516f908b755e4edb58576cbfcbdb916f5b11c12116b08)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#file_name TranscoderJobTemplate#file_name}
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mux_streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user supplied MuxStream.key values that should appear in this manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#mux_streams TranscoderJobTemplate#mux_streams}
        '''
        result = self._values.get("mux_streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of the manifest. Possible values: ["MANIFEST_TYPE_UNSPECIFIED", "HLS", "DASH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#type TranscoderJobTemplate#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigManifests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigManifestsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigManifestsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac3d0d180deb3c88147a066340b494ee8816d6a6a899a44cc20826d302d65eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigManifestsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad8b9c2c8e4e20b55288cb0b34e09c52279c578417431a4c2b187a34d5cdca3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigManifestsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351a55ab193c608a2dfa6710468d903526c3fb07aa225e5ad59e4b7c19d64e65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dea94c9adb8b9a51418fec1d6d0e36bf99cdd7c81e6932b20a0db5efc861a2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4960ba7f658d5876f872cb8ab2010efb54311530b53e092763a20c74145ca285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigManifests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigManifests]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigManifests]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e5b8225f9da3fbaa48d3abfefb33870686793c70130cf5382a1b047b038a685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigManifestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigManifestsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fdf4c2ea337041e731284b108a49cd90d14f3759904ac8a5175df58eb662dd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d58315335129422166f5f9817158bcd04a9d8394ed0d1b84c036175e9647013c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="muxStreams")
    def mux_streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "muxStreams"))

    @mux_streams.setter
    def mux_streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb89a501a0e43a9c25c52a0bf3a30243e8f0faf9c1d1cb4b5cf9ee8c49668d8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "muxStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfcaa2299d1df17baffa2f24549df3f61c26a18f2f8f56cf950c5879708a8712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigManifests]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigManifests]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigManifests]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe609814951c491e98f5a8190e5be4d481e2a28cdc8f8738c022b7d4686c476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigMuxStreams",
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
class TranscoderJobTemplateConfigMuxStreams:
    def __init__(
        self,
        *,
        container: typing.Optional[builtins.str] = None,
        elementary_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
        encryption_id: typing.Optional[builtins.str] = None,
        file_name: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        segment_settings: typing.Optional[typing.Union["TranscoderJobTemplateConfigMuxStreamsSegmentSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param container: The container format. The default is 'mp4'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#container TranscoderJobTemplate#container}
        :param elementary_streams: List of ElementaryStream.key values multiplexed in this stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#elementary_streams TranscoderJobTemplate#elementary_streams}
        :param encryption_id: Identifier of the encryption configuration to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#encryption_id TranscoderJobTemplate#encryption_id}
        :param file_name: The name of the generated file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#file_name TranscoderJobTemplate#file_name}
        :param key: A unique key for this multiplexed stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#key TranscoderJobTemplate#key}
        :param segment_settings: segment_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#segment_settings TranscoderJobTemplate#segment_settings}
        '''
        if isinstance(segment_settings, dict):
            segment_settings = TranscoderJobTemplateConfigMuxStreamsSegmentSettings(**segment_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00908041b849f74a7cf9e4fd72566572aec99e553374f4a32bb5d811ba4baf9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#container TranscoderJobTemplate#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elementary_streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of ElementaryStream.key values multiplexed in this stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#elementary_streams TranscoderJobTemplate#elementary_streams}
        '''
        result = self._values.get("elementary_streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def encryption_id(self) -> typing.Optional[builtins.str]:
        '''Identifier of the encryption configuration to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#encryption_id TranscoderJobTemplate#encryption_id}
        '''
        result = self._values.get("encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_name(self) -> typing.Optional[builtins.str]:
        '''The name of the generated file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#file_name TranscoderJobTemplate#file_name}
        '''
        result = self._values.get("file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A unique key for this multiplexed stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#key TranscoderJobTemplate#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_settings(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigMuxStreamsSegmentSettings"]:
        '''segment_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#segment_settings TranscoderJobTemplate#segment_settings}
        '''
        result = self._values.get("segment_settings")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigMuxStreamsSegmentSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigMuxStreams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigMuxStreamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigMuxStreamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7e76a34fd747c28874e2fd935d12e28fe2b2f3850d1f6c6fe84aee21767c84f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigMuxStreamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8341e9e7d37799900448bd8f7f6840be206d8dae19e2172835f21df8417cc516)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigMuxStreamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e2c13e5e1cc2e44ebffdb31bd8fdeb650bd6c33d4a1a09e7d2bad3c94d9ee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e93d070b5fd74ce504d23a42a46e65c377991ba4c1de2ad09e609845df6c91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81f0fce39e7fe4e95ce1e5c307ad22cfcca2386ae224189b5347ee99992fe1ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigMuxStreams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigMuxStreams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigMuxStreams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f8f0074a6b950b6d2cc3a7c781515eff16f3dc5f66b107a958334f37dc5b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigMuxStreamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigMuxStreamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cac5ae13dd09a55a3b6cad4411d43b766b0685df1286e9d63754b4a3b1628dc)
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
        :param segment_duration: Duration of the segments in seconds. The default is '6.0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#segment_duration TranscoderJobTemplate#segment_duration}
        '''
        value = TranscoderJobTemplateConfigMuxStreamsSegmentSettings(
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
    ) -> "TranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference":
        return typing.cast("TranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference", jsii.get(self, "segmentSettings"))

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
    ) -> typing.Optional["TranscoderJobTemplateConfigMuxStreamsSegmentSettings"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigMuxStreamsSegmentSettings"], jsii.get(self, "segmentSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e8f6287a25bdbba290edf95a4955153884e3562652d8a9ae53c308bc6d5137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elementaryStreams")
    def elementary_streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "elementaryStreams"))

    @elementary_streams.setter
    def elementary_streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43722850b67b02d4a9e30095693fc735d73aacb754f98956982f56941208ad7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elementaryStreams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionId")
    def encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionId"))

    @encryption_id.setter
    def encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4fdbd620e22dae8490ee48580bdb37a4066546fc577235b864689e031f62c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a0d0683fb98dacfcb661bcff5fc5a52c830ca949cf7feb9d7ffc61af50d67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939a13231cb3b764bdf50de46dd27680df29f756fc468ff6fd1efe0e990dbfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigMuxStreams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigMuxStreams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigMuxStreams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4161efb8d9616059e33a941c390cee08ecba83c94d26fc2ff890b2c9040b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigMuxStreamsSegmentSettings",
    jsii_struct_bases=[],
    name_mapping={"segment_duration": "segmentDuration"},
)
class TranscoderJobTemplateConfigMuxStreamsSegmentSettings:
    def __init__(
        self,
        *,
        segment_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param segment_duration: Duration of the segments in seconds. The default is '6.0s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#segment_duration TranscoderJobTemplate#segment_duration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95cabce345abbd32a880630de0cedef12b20f5ae558520a0cf01d2e09d17bbdf)
            check_type(argname="argument segment_duration", value=segment_duration, expected_type=type_hints["segment_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if segment_duration is not None:
            self._values["segment_duration"] = segment_duration

    @builtins.property
    def segment_duration(self) -> typing.Optional[builtins.str]:
        '''Duration of the segments in seconds. The default is '6.0s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#segment_duration TranscoderJobTemplate#segment_duration}
        '''
        result = self._values.get("segment_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigMuxStreamsSegmentSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbcbb7a9534ad302fd18837fbb582efa7225f80e7c9f85ec13d7703013a84e4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dbd776b908cf2d95ef50452e639bf6dde0f05cb8114a2fcccd29e9f18c15cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segmentDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigMuxStreamsSegmentSettings]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigMuxStreamsSegmentSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigMuxStreamsSegmentSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabc3d509010876b22813ec9f8bf405c450ca9ec7dfbffcdf7cc8221de4cdb04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOutput",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class TranscoderJobTemplateConfigOutput:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: URI for the output file(s). For example, gs://my-bucket/outputs/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#uri TranscoderJobTemplate#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2083f04ecc8161edc4cae11f2da65bdb834b8b47af157eb87a36620d3dd8313a)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''URI for the output file(s). For example, gs://my-bucket/outputs/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#uri TranscoderJobTemplate#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__127cecb9301998ee5b2ab036d81930a4a5aa786d40c21d574a16d557fdd2634f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f07b64a4acf313d5988e7f8fcb8854c9654a749125836d887305e5cdfa6a457c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TranscoderJobTemplateConfigOutput]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5171ad24b7dd9e6416cb9659eb8ac9c710cc13928dbaba25ec769fdbbf7d27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlays",
    jsii_struct_bases=[],
    name_mapping={"animations": "animations", "image": "image"},
)
class TranscoderJobTemplateConfigOverlays:
    def __init__(
        self,
        *,
        animations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TranscoderJobTemplateConfigOverlaysAnimations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        image: typing.Optional[typing.Union["TranscoderJobTemplateConfigOverlaysImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param animations: animations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#animations TranscoderJobTemplate#animations}
        :param image: image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#image TranscoderJobTemplate#image}
        '''
        if isinstance(image, dict):
            image = TranscoderJobTemplateConfigOverlaysImage(**image)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9070065729daa28c0607510a35dfa24896da8ed964fcad5a7b8b1c9d873d46ea)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigOverlaysAnimations"]]]:
        '''animations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#animations TranscoderJobTemplate#animations}
        '''
        result = self._values.get("animations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TranscoderJobTemplateConfigOverlaysAnimations"]]], result)

    @builtins.property
    def image(self) -> typing.Optional["TranscoderJobTemplateConfigOverlaysImage"]:
        '''image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#image TranscoderJobTemplate#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigOverlaysImage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigOverlays(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysAnimations",
    jsii_struct_bases=[],
    name_mapping={"animation_fade": "animationFade"},
)
class TranscoderJobTemplateConfigOverlaysAnimations:
    def __init__(
        self,
        *,
        animation_fade: typing.Optional[typing.Union["TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param animation_fade: animation_fade block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#animation_fade TranscoderJobTemplate#animation_fade}
        '''
        if isinstance(animation_fade, dict):
            animation_fade = TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade(**animation_fade)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ab58da6371a7ba2f8a6ac89537c3a268d55ccb85beb79afad365ae5d5fc963)
            check_type(argname="argument animation_fade", value=animation_fade, expected_type=type_hints["animation_fade"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if animation_fade is not None:
            self._values["animation_fade"] = animation_fade

    @builtins.property
    def animation_fade(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade"]:
        '''animation_fade block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#animation_fade TranscoderJobTemplate#animation_fade}
        '''
        result = self._values.get("animation_fade")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigOverlaysAnimations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade",
    jsii_struct_bases=[],
    name_mapping={
        "fade_type": "fadeType",
        "end_time_offset": "endTimeOffset",
        "start_time_offset": "startTimeOffset",
        "xy": "xy",
    },
)
class TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade:
    def __init__(
        self,
        *,
        fade_type: builtins.str,
        end_time_offset: typing.Optional[builtins.str] = None,
        start_time_offset: typing.Optional[builtins.str] = None,
        xy: typing.Optional[typing.Union["TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fade_type: Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:. - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified. - 'FADE_IN': Fade the overlay object into view. - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#fade_type TranscoderJobTemplate#fade_type}
        :param end_time_offset: The time to end the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#end_time_offset TranscoderJobTemplate#end_time_offset}
        :param start_time_offset: The time to start the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#start_time_offset TranscoderJobTemplate#start_time_offset}
        :param xy: xy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#xy TranscoderJobTemplate#xy}
        '''
        if isinstance(xy, dict):
            xy = TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy(**xy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028b810054f7f36773b2686f9e570dfe869b97604f1020eb7ac9c8721263a829)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#fade_type TranscoderJobTemplate#fade_type}
        '''
        result = self._values.get("fade_type")
        assert result is not None, "Required property 'fade_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_time_offset(self) -> typing.Optional[builtins.str]:
        '''The time to end the fade animation, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#end_time_offset TranscoderJobTemplate#end_time_offset}
        '''
        result = self._values.get("end_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time_offset(self) -> typing.Optional[builtins.str]:
        '''The time to start the fade animation, in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#start_time_offset TranscoderJobTemplate#start_time_offset}
        '''
        result = self._values.get("start_time_offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xy(
        self,
    ) -> typing.Optional["TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy"]:
        '''xy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#xy TranscoderJobTemplate#xy}
        '''
        result = self._values.get("xy")
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5be16536d57e98ee053bb9ae3023b6aaf3c6c4985bb6ac98b319957a27243b88)
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
        :param x: Normalized x coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#x TranscoderJobTemplate#x}
        :param y: Normalized y coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#y TranscoderJobTemplate#y}
        '''
        value = TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy(x=x, y=y)

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
    ) -> "TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference":
        return typing.cast("TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference", jsii.get(self, "xy"))

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
    ) -> typing.Optional["TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy"]:
        return typing.cast(typing.Optional["TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy"], jsii.get(self, "xyInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeOffset")
    def end_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTimeOffset"))

    @end_time_offset.setter
    def end_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5fc6b0c428c6f07e449b34a2ed23f56c6bc343fbb9d5286b497b90a341fa85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fadeType")
    def fade_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fadeType"))

    @fade_type.setter
    def fade_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037ec823c66fa7ae20b4f5347323cf0032dc58658b07ca8de85381dd4ceb8c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fadeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimeOffset")
    def start_time_offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTimeOffset"))

    @start_time_offset.setter
    def start_time_offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b4386386856ae12f511070b677dd9592458479e5225e3651bcb1d2843bcf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimeOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4b4b267c60ef8bac1710c422865a88c4d72559fe9fd740922a705d4a59f54f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy",
    jsii_struct_bases=[],
    name_mapping={"x": "x", "y": "y"},
)
class TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy:
    def __init__(
        self,
        *,
        x: typing.Optional[jsii.Number] = None,
        y: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param x: Normalized x coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#x TranscoderJobTemplate#x}
        :param y: Normalized y coordinate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#y TranscoderJobTemplate#y}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc14838c845684dc5d35482d10fb19c4e35c6e7b4d0c73313a5ea3bd8379873)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#x TranscoderJobTemplate#x}
        '''
        result = self._values.get("x")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def y(self) -> typing.Optional[jsii.Number]:
        '''Normalized y coordinate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#y TranscoderJobTemplate#y}
        '''
        result = self._values.get("y")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eb080a6aee5e875e83e94cf9c58c84c9a39451cb42860d7e83a5b0c4fb7200b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a23ee7204665ed370ea55eacd8323ef345d3fedd7b971e6c85adf96d1555c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "x", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="y")
    def y(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "y"))

    @y.setter
    def y(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d4a782f109498ab25974fdedcddc13471338ef748c2b6a02df96a4ac41e7d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "y", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672763e8876334fbc402eed13412bd0a4d918d33076439ff11b7c1b6e63fc400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigOverlaysAnimationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysAnimationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2d4f39cda0607de1a3ebb13e4edf2f7809ad49f686614561f29bc16a99c9d99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigOverlaysAnimationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a560597f487cf0d3ad4d158533675090311a9d89ab49a66329f7fd2dce4d465)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigOverlaysAnimationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65382767936ec6cc7a346ca622acb1e5a2cacc4f924da77f5cec339ad9f73fbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a58515444aaec2bbe00e76d7abf920e1d079c2e568893a8b2e4c7fea3743419b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a7d28e0317399f4c737befc6f748fcc8e9f72211df89dab1269aafd963ef9ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlaysAnimations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlaysAnimations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlaysAnimations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2dcc38606315b4642e64857b94867987231a9ff2b295e51e72045d61d9e29ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigOverlaysAnimationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysAnimationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30d0868084a0431152d59480bc2c03d2f4a1efc061e76dd24e5e564969dc2bd8)
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
        xy: typing.Optional[typing.Union[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param fade_type: Required. Type of fade animation: 'FADE_IN' or 'FADE_OUT'. The possible values are:. - 'FADE_TYPE_UNSPECIFIED': The fade type is not specified. - 'FADE_IN': Fade the overlay object into view. - 'FADE_OUT': Fade the overlay object out of view. Possible values: ["FADE_TYPE_UNSPECIFIED", "FADE_IN", "FADE_OUT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#fade_type TranscoderJobTemplate#fade_type}
        :param end_time_offset: The time to end the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#end_time_offset TranscoderJobTemplate#end_time_offset}
        :param start_time_offset: The time to start the fade animation, in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#start_time_offset TranscoderJobTemplate#start_time_offset}
        :param xy: xy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#xy TranscoderJobTemplate#xy}
        '''
        value = TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade(
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
    ) -> TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference:
        return typing.cast(TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference, jsii.get(self, "animationFade"))

    @builtins.property
    @jsii.member(jsii_name="animationFadeInput")
    def animation_fade_input(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade], jsii.get(self, "animationFadeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigOverlaysAnimations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigOverlaysAnimations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigOverlaysAnimations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d72e2956f6a3298741928ddbea27ca9668e078c1b34a98b670ca5981912849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysImage",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class TranscoderJobTemplateConfigOverlaysImage:
    def __init__(self, *, uri: builtins.str) -> None:
        '''
        :param uri: URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#uri TranscoderJobTemplate#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f47c3df33d12942c4d19d9780aef23e225e030b7cc1382f50309b8875db90d)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#uri TranscoderJobTemplate#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigOverlaysImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigOverlaysImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__236ca091ca9fc9ff0c91e077c7a7e5fe3897f0e42aec1447fc46b7ee8eed7adf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a4c8e9020508501ecc6229e8dc3b22a2019e62c7c26c21b9ddffc3c684ba08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigOverlaysImage]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigOverlaysImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigOverlaysImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d23f45be72817ce619ed33e2638b75a53a96723c6d8068d5d5efe119015479f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigOverlaysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__828ee35d321e2a535ae99dd59c9076fd98f07330a57648abd9da024bd4dd9e51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TranscoderJobTemplateConfigOverlaysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d9365149e669ee26e911bb6136440556de929118e2d1a1da8d1c59d3bad5da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TranscoderJobTemplateConfigOverlaysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c5785f720ea95482bc4ab09fb265a3c2f18c5227c33bd1aa60fea616bc5022)
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
            type_hints = typing.get_type_hints(_typecheckingstub__567c8e2e6b724a548fbca77fe13464c974d66a0fe0a4564f131b0efa31a7374a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11689189af79c37085ab9cbfcca829fa6605d462d6ec7e4dd9bd53a892068c17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlays]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlays]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlays]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9c0f8b39c99357752d12b8e8ab5c138c936b64294b8798f8c8d2f7e8ad2c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TranscoderJobTemplateConfigOverlaysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigOverlaysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__315c0fe7c4f609bbccc1afa97b673e24abf793436adfe75fdc0ba3a851ea9845)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAnimations")
    def put_animations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e09159dd4db3efdef4292847839b3f53b5f0c899bed3f47cafe886516a2e1f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnimations", [value]))

    @jsii.member(jsii_name="putImage")
    def put_image(self, *, uri: builtins.str) -> None:
        '''
        :param uri: URI of the image in Cloud Storage. For example, gs://bucket/inputs/image.png. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#uri TranscoderJobTemplate#uri}
        '''
        value = TranscoderJobTemplateConfigOverlaysImage(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="resetAnimations")
    def reset_animations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnimations", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @builtins.property
    @jsii.member(jsii_name="animations")
    def animations(self) -> TranscoderJobTemplateConfigOverlaysAnimationsList:
        return typing.cast(TranscoderJobTemplateConfigOverlaysAnimationsList, jsii.get(self, "animations"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> TranscoderJobTemplateConfigOverlaysImageOutputReference:
        return typing.cast(TranscoderJobTemplateConfigOverlaysImageOutputReference, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="animationsInput")
    def animations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlaysAnimations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlaysAnimations]]], jsii.get(self, "animationsInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[TranscoderJobTemplateConfigOverlaysImage]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigOverlaysImage], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigOverlays]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigOverlays]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigOverlays]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff863af21761d7effaaf9d16c26ee405f69697e79fb7e9d811f766baaa2bd7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigPubsubDestination",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class TranscoderJobTemplateConfigPubsubDestination:
    def __init__(self, *, topic: typing.Optional[builtins.str] = None) -> None:
        '''
        :param topic: The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#topic TranscoderJobTemplate#topic}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8112dc4ea283b4dc463ede4aa6a0a0d86a11203f8da7ce7a80a6a078c971fa)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[builtins.str]:
        '''The name of the Pub/Sub topic to publish job completion notification to. For example: projects/{project}/topics/{topic}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#topic TranscoderJobTemplate#topic}
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateConfigPubsubDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateConfigPubsubDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateConfigPubsubDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1b6e2844c83e9b0e220cb0a7dc3fa48d33fb70abcb8470c8009785ce63e3cd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d235d3e012859b324fd75bdaa99040106f1c1670b940b64d4517aa8d3d2d9ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TranscoderJobTemplateConfigPubsubDestination]:
        return typing.cast(typing.Optional[TranscoderJobTemplateConfigPubsubDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TranscoderJobTemplateConfigPubsubDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469d3411897351101793653d49dc452fa3f875ee5a0554db725e9c9e3819482e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class TranscoderJobTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#create TranscoderJobTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#delete TranscoderJobTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#update TranscoderJobTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8b03c76ebad5184e4368c97bffb9600cfa329d0097968a5b680e14bb4b337a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#create TranscoderJobTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#delete TranscoderJobTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/transcoder_job_template#update TranscoderJobTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TranscoderJobTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TranscoderJobTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.transcoderJobTemplate.TranscoderJobTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d65e616e8f60e56a947d8159fb3c420d1f76f71802b2a77f83fc2833133736c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__901c9c638c1c8f6b68286e7536338b63912304cd397086c67ad20eabdb77befe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4a598c1260e017ac8b1656d47d83fcfb261ecda4eda43eb2c523638900946d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3e11188a4a6f4cf9214817309fcd7468687756fa54674f253f7df01e6b5507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6261fd2f9d0be6fa6a6915dea2a784b926f82922dde2f04a9eea3a4e9f1bc2d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TranscoderJobTemplate",
    "TranscoderJobTemplateConfig",
    "TranscoderJobTemplateConfigA",
    "TranscoderJobTemplateConfigAOutputReference",
    "TranscoderJobTemplateConfigAdBreaks",
    "TranscoderJobTemplateConfigAdBreaksList",
    "TranscoderJobTemplateConfigAdBreaksOutputReference",
    "TranscoderJobTemplateConfigEditListStruct",
    "TranscoderJobTemplateConfigEditListStructList",
    "TranscoderJobTemplateConfigEditListStructOutputReference",
    "TranscoderJobTemplateConfigElementaryStreams",
    "TranscoderJobTemplateConfigElementaryStreamsAudioStream",
    "TranscoderJobTemplateConfigElementaryStreamsAudioStreamOutputReference",
    "TranscoderJobTemplateConfigElementaryStreamsList",
    "TranscoderJobTemplateConfigElementaryStreamsOutputReference",
    "TranscoderJobTemplateConfigElementaryStreamsVideoStream",
    "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264",
    "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg",
    "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264HlgOutputReference",
    "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264OutputReference",
    "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr",
    "TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264SdrOutputReference",
    "TranscoderJobTemplateConfigElementaryStreamsVideoStreamOutputReference",
    "TranscoderJobTemplateConfigEncryptions",
    "TranscoderJobTemplateConfigEncryptionsAes128",
    "TranscoderJobTemplateConfigEncryptionsAes128OutputReference",
    "TranscoderJobTemplateConfigEncryptionsDrmSystems",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkeyOutputReference",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplayOutputReference",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsOutputReference",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayreadyOutputReference",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine",
    "TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevineOutputReference",
    "TranscoderJobTemplateConfigEncryptionsList",
    "TranscoderJobTemplateConfigEncryptionsMpegCenc",
    "TranscoderJobTemplateConfigEncryptionsMpegCencOutputReference",
    "TranscoderJobTemplateConfigEncryptionsOutputReference",
    "TranscoderJobTemplateConfigEncryptionsSampleAes",
    "TranscoderJobTemplateConfigEncryptionsSampleAesOutputReference",
    "TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource",
    "TranscoderJobTemplateConfigEncryptionsSecretManagerKeySourceOutputReference",
    "TranscoderJobTemplateConfigInputs",
    "TranscoderJobTemplateConfigInputsList",
    "TranscoderJobTemplateConfigInputsOutputReference",
    "TranscoderJobTemplateConfigManifests",
    "TranscoderJobTemplateConfigManifestsList",
    "TranscoderJobTemplateConfigManifestsOutputReference",
    "TranscoderJobTemplateConfigMuxStreams",
    "TranscoderJobTemplateConfigMuxStreamsList",
    "TranscoderJobTemplateConfigMuxStreamsOutputReference",
    "TranscoderJobTemplateConfigMuxStreamsSegmentSettings",
    "TranscoderJobTemplateConfigMuxStreamsSegmentSettingsOutputReference",
    "TranscoderJobTemplateConfigOutput",
    "TranscoderJobTemplateConfigOutputOutputReference",
    "TranscoderJobTemplateConfigOverlays",
    "TranscoderJobTemplateConfigOverlaysAnimations",
    "TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade",
    "TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeOutputReference",
    "TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy",
    "TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXyOutputReference",
    "TranscoderJobTemplateConfigOverlaysAnimationsList",
    "TranscoderJobTemplateConfigOverlaysAnimationsOutputReference",
    "TranscoderJobTemplateConfigOverlaysImage",
    "TranscoderJobTemplateConfigOverlaysImageOutputReference",
    "TranscoderJobTemplateConfigOverlaysList",
    "TranscoderJobTemplateConfigOverlaysOutputReference",
    "TranscoderJobTemplateConfigPubsubDestination",
    "TranscoderJobTemplateConfigPubsubDestinationOutputReference",
    "TranscoderJobTemplateTimeouts",
    "TranscoderJobTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ee8d562ed6ac7ac2f34e24a37b239d8a72bf397a27bf48388b1d0631ce1906b5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    job_template_id: builtins.str,
    location: builtins.str,
    config: typing.Optional[typing.Union[TranscoderJobTemplateConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[TranscoderJobTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5b5e52062e916c092b9df7130de2caf29f8c956059497a7daebc3ff1ed37b4ae(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b11fb46980afe2144cb3b13d69bca4ef0503bc18c4750b396119715da4eef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e8b5cfa3f14944bb09f2044077c7b2f5eb7df34a6164c35fd8655408b3778f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04783dd4a67ffa129c250fca7ff9a9202731176ffa62486757cdb879620b2d34(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9e8dbbedb2ad3fcfdcc626c8c752b80963c2d1245c7cf3ee0661e5dc2c9bbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f010efe1c3541f82ec030cc5edf77c28e7672b4cd888ac587b585e3b5e86a3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15da54943f51bfcaa731a9eaf1fe0b44ec9e7a9c67d4bead2341487c680aa17(
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
    config: typing.Optional[typing.Union[TranscoderJobTemplateConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[TranscoderJobTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30faaf3db4541a86a5333975f2c6105418c7b514ea25771159af53154086d2c(
    *,
    ad_breaks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigAdBreaks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edit_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigEditListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elementary_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigElementaryStreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryptions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigEncryptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigInputs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    manifests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigManifests, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mux_streams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigMuxStreams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    output: typing.Optional[typing.Union[TranscoderJobTemplateConfigOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    overlays: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigOverlays, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pubsub_destination: typing.Optional[typing.Union[TranscoderJobTemplateConfigPubsubDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bd977a5bf8de0bce9d66369d195241b5c1b4fc8080c2fdb34acc48bdb4b3f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513edef6817aa7a2b808e7d51c2e84ec1506ee780206afe508f29dcc4f342c00(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigAdBreaks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378718d4bc35b8764393e1f55b3a174ac17eb94437739f73fe35bb92ba0fe863(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigEditListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92778e7e3021889385997dee038df59a1f2ed57235c4bed721d7b386a84f3521(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigElementaryStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e092739223c306c6bd097a91a92e638c867a5259f56d476ebd6d1caa948183cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigEncryptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ed7f8b0e979cced9a04f5d747187d5c825a38f0f8ae9b69e241270a77ee6ad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigInputs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8962f320650901de9fffec22b3f82bf1f39cbc11a48938bada21153111523e0e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigManifests, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf4e4a9aa57a8cd679499f789f71c373496c6e66ac0e43dde42643eb6b0ee46(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigMuxStreams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017afaf5cf3db31027186f60e7bd396493fe41770125ec3e679b3f438110d929(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigOverlays, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8888a1643358dbbd8d3d342cc24c8f6374d4eda35da5f2441365aa10e8a70727(
    value: typing.Optional[TranscoderJobTemplateConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5c6edadc95ca36220e52b5cfc9dfd2d9615478a3431a5135d5329206d793b2(
    *,
    start_time_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ef08553eb101c0f655c80513b7c2d8465a9d89f6b1a1732483f738df335f6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91cded2d83d47eba927003171cfe6f3e34c3dc34590f63a0114ed59599e8cb56(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52dcc055962f3621d807e95cde9f493f6d2cea2b30929203497f3a7cd188829(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85cbc1f3f0653b2bbddcc0bcae6b718c78021b4b570c019fe79e5f0128999ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c741709c1d87f52728dfa7e3a84460e13af16be75b1700a88070cbf8077c63(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2468d0d52fbeae805b89e7a6759dd42e0c4d2ea22ab0297e67a04612764b3afc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigAdBreaks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065a532c592bb60d9ad06ccd24d5734d5bfbdca038d59c9c5b6b1a86a8d143f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d15e5b1ff9f4d40cbf6a09a1397aafd201ddba705be3468b4afb97b0da1243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5201944fb9ebe0fa92f8853cb0bd411d5e3658461a0a5779991200ff73c0d33c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigAdBreaks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264d6bc0ef48fa89aaf03a20cb5521ad8563db3df316862350555cc067391aa6(
    *,
    inputs: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[builtins.str] = None,
    start_time_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5643e6de1d5d19c0bdcdbce6a597b62ef9fe315b33e4dc0adb02d757af8901(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0334693955e5c4f2869add272bfc7b8155301fc7c6373d27e4c690cb6778330(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310450d14d48d2a99182559723b2eabdc59b6a80e5486dbd372a1f2d878e4029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b4fb5bb4e0b2cf0c6e6f6b9f2d3861e6ab0d76627d3eda9af192e9d6ef8ad3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369e8cf0c79fa7c7064b81f172a0bc26456018268fa927226abba0f68f2d0146(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739906b619aef6a90a4bdf6f539f7a8f670fc8398b1be163e40a36b3b3d3b854(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigEditListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ad0a5a2f2bc57cf65a6dca9ef6dae889b2f5483c37f9e238fa9ae12f9b08f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262d10c6b5042cb2338cb750e248da5e37c4742024d3b274574c97a0be660d76(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740b8a4540c1283660bc4a2f122b2a03a834bc5f0cb0a8148f65cf0294adbc45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59278046822d27cc959f59253a1ce42bca87188b26a34fdbae56cd389e699256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8277a4afcf8b3b3c0bc205c5ab194fdb216e6a07e46dde0b834bbfe470af1aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigEditListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18ed9ac680731d0b1cc060e6ebc75d8e25a3a4b6e579db0792c05ad8c43ff6a(
    *,
    audio_stream: typing.Optional[typing.Union[TranscoderJobTemplateConfigElementaryStreamsAudioStream, typing.Dict[builtins.str, typing.Any]]] = None,
    key: typing.Optional[builtins.str] = None,
    video_stream: typing.Optional[typing.Union[TranscoderJobTemplateConfigElementaryStreamsVideoStream, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f997f98a422ff83b875ace2685de3076ca32a426f512ac5879dde995e30bc3(
    *,
    bitrate_bps: jsii.Number,
    channel_count: typing.Optional[jsii.Number] = None,
    channel_layout: typing.Optional[typing.Sequence[builtins.str]] = None,
    codec: typing.Optional[builtins.str] = None,
    sample_rate_hertz: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060eba394648af2ebe507baf3be3a57ef8dcf666b817251faca698a3f4990180(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4c828c3c96edee233bb69b14399e41f19d8107a8ffb8c4ea735d85b1a80d5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d35e4755c8499bbdff745eaa8da9d799b57003a96df7e72eb163cca6532c92(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09338f5b914ae0330e1373ba1eb970f7aa1d58ac2a56ab8aedc75b975a6bb151(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96af2a1a41c2355b5ccaa1ade6c4ed703aed9ab905deeaf5587b485d3fedcd17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8416b02ebc081999612fc725ed5dc12e1336005095f75a814c47f8c7514be5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c4282aea922c85c6846c5d1c217a2951d696caf79f42fe35ae93148f4bab30(
    value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsAudioStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de3d3655d75207e423933d0b58bc16c9b54ae5cfffb3bd942e414238dbde835(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b25d8f00918fdeb924d95d85a3d939ceb78e20380f0a8fecfba08199598f6dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39031cf0857c401fee7045e848540abf145cdcfdb1a492b698cbf03003baf304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2083128d514646d1b732ed0accc76108eb12274a42ff42377e2afaec41d9bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3daf41d3933eef8e8490eb74062452a13e5158b5d24804a90c7045d9e3d3cc26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc6bb316af0b03219dd87d1f3536db344ae55284b58bfc5ead3fe1e159e853b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigElementaryStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570993684365e37e258eabd6875fe03d50a0f77e5f30684e85bc8669a921e47c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c59b47734ba06ecd909e6f129063b54aa2e226f6bfa1e1996a60559e65e47a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c3ec5850467d356f171edf432e839eb930451eecf71da73909ea3e6c10492f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigElementaryStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f8f3593102f04f526b5f1a745f372446db9f70d64fc8869a7c239dc1426b01(
    *,
    h264: typing.Optional[typing.Union[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdfcfefe79f07f6ef3c5db530863129a838829155bd6e7ff09cba338711ef39(
    *,
    bitrate_bps: jsii.Number,
    frame_rate: jsii.Number,
    crf_level: typing.Optional[jsii.Number] = None,
    entropy_coder: typing.Optional[builtins.str] = None,
    gop_duration: typing.Optional[builtins.str] = None,
    height_pixels: typing.Optional[jsii.Number] = None,
    hlg: typing.Optional[typing.Union[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg, typing.Dict[builtins.str, typing.Any]]] = None,
    pixel_format: typing.Optional[builtins.str] = None,
    preset: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    rate_control_mode: typing.Optional[builtins.str] = None,
    sdr: typing.Optional[typing.Union[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr, typing.Dict[builtins.str, typing.Any]]] = None,
    vbv_fullness_bits: typing.Optional[jsii.Number] = None,
    vbv_size_bits: typing.Optional[jsii.Number] = None,
    width_pixels: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727bd9010e63c5ba4eff6747349afc27746d73bf660d56725a5041884e2f31c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17f01d1231cc4523e19178ce2557d27444f21c9ce75da99a0f908e6b36bf00a(
    value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Hlg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5189848a1c2654866eb6780ec5c870fe90799bd53e17532213daa163f2f2bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cfac3d2d83161ace4ce6622ee2ff2fd67dfbec42a30f273b388fb3396210bf0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b39da567a8108c0bd5e5fce490189983435e60c306813647c46666f6461f71a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fabb14dc83774c8fda99046b72141587d1be75eaf746bf8ce4ba37fb48487cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398801ef70fccfec093e84f6d0be4872306ac1d8725c0e99e15c4ec4c9622fdd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c826a4f1f2c779bc38538f434d9933a172e73c0f6cc0879e68b4b020e29a6d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea2d51a496af6549d8307faa598dd521152e639451cfd883d91a30eee5cd58d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00737ce28b27344ce2b372ee0339af8cb61696512ce6ff2fea2d27d3c15a86e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b023936ea461c257aa224a634c690d7ce284764ca8a30af0c4ffbfb7cec5f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdc629c3d580b236e22ea681ed36793369448bece8183cb97728a020070e326(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48478a5aa9dff27b771fe3e6089dd1244802a387583fe0e753d0c90cdf48f99c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a290c3468e3dcbbb0b70f9b7236990df06c6d6602a5d55c71c562c93c7900f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbe1c5a22f248dd23536b24444a1bc94b6b7ccb0acdff7e78f6546c56543303(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5737dbc474a1295ec57d3c6eb274290795529865104b9bc70a396b84be3978d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300a25a58a4661ef9c04280095ebc125d758544c85002f19fb9882b3d42e0397(
    value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30210689b03e7c597f5ef083209fdcfa71d8340de432e17875eaa76e72234a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dea1eac5e2629de9265d45fff339c825f3f8448721848a627a8ccbb21d58892(
    value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStreamH264Sdr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584cfb7a03c09485fb5b478e791f04c1c671ed75df6265a5e03241f1d31a874d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb16bb1127852f958788179a497a0d2089f70b9d0d39c7d1800434c2f82291c(
    value: typing.Optional[TranscoderJobTemplateConfigElementaryStreamsVideoStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf6ae8376dc4ac3993e208596b8f28b3c2f8ab58941e8a61981dae678f56580(
    *,
    id: builtins.str,
    aes128: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsAes128, typing.Dict[builtins.str, typing.Any]]] = None,
    drm_systems: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystems, typing.Dict[builtins.str, typing.Any]]] = None,
    mpeg_cenc: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsMpegCenc, typing.Dict[builtins.str, typing.Any]]] = None,
    sample_aes: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsSampleAes, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_manager_key_source: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff4826c0fa17db951354a6f1439976e1404658847b52d314cd9c57c6a6dd2c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e879fc5fc3b0687f98c4095ad56c8775b9c70c4e73df4fafd97fac418ee489f4(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsAes128],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9221d0ea8b781ddba54353805044bf4c4b982af7b0441cb51da48346d0589cc2(
    *,
    clearkey: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey, typing.Dict[builtins.str, typing.Any]]] = None,
    fairplay: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
    playready: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
    widevine: typing.Optional[typing.Union[TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e169bb9c086fa5775970485cd7e7982253d412f49782ab71c537d5de6a55d555(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab0745ceb252e00ea52de422a65168a4dab39ef56bcaef2278c847f32d1ee7e(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsClearkey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9a9ce381b4bff1b23b29f47626b07c448864e3216c88a83936bde73575a2ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b715362ea473807cb69e420f36fb85e1b73aa27417ffe97d96e8f09ea84879b(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsFairplay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02eeb1f34bce0605dfc459a27d48d09f5c351a6de0208f3ccdf70863ae0a6e8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45462148306bef0a1dc1a52aaec62f1321d4fb0c4f9a2d7ad097f78636791664(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystems],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383a3f1bad2985086a3afd366fd28676fdf31b720b6609a63610d02b18fb34e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ba2ee23daee96d5fd1fa03a351189fdf782c225b6def49588effe20922650c(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsPlayready],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b785df258b627bf3fbe961d6dfac75c59b467efbee04abd7f403e191e03b8ad8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acb73eceb227393ff6c6cbfa1bd161211d95785f97d7b55367f1856f24d291f(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsDrmSystemsWidevine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d3dd9ac5e284c3085c8a3e506ab721a32d28ca5eefa895dd8f9b731a5c3806(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1cae0280f768011673e6f1b55a5ead15c0b70b00542a343821785a0dcde49e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa7176abc5bb05869be544bc5ed775dcba9158ea32cb7670c077e7fba279bd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8920b6d7b3028c08feb275c6ba9952d0971392b93f4bdc083d374894d43747b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8783683edb8af4602b373a0e14b1d4622d5bc10010c1e264de34b92bde26e08b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a2a709aff5f43b7569caf3d857d638a3bddba0b718d43a80faf959e49b85a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigEncryptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391fcde7cc0207ce20a3e71c2ace30741d22e3692b8a5344745c7ef3f8a6cc63(
    *,
    scheme: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c46c875e7f0ed6689a7d73bac59f9c810bd699d8d00551a335a6401868efdb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb09e82714a547a2ea4f5394320ab0af54e12bc828dad672ebbc263f65321a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc02c6bda45b0ec5cdd160243e78593145cf6933053eb1d2a469be784c6be45(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsMpegCenc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46203c07ab668e35f2f624aee335dea1d0ef566b852caaa86cff2f8fde6cb08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e3419a55bc3c91204a519f0034856b9eeda4e27cc76b7fb632a6e50be89535(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ccbd69b11635a1595443a6888b1fb36356f208cb5f81c6e0edc39c737a0681(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigEncryptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b50ef511268a9c0c35f3a2281c54210f79cfe09b7bb16a4a11fd3ec15eee1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55aa1920516e17c7fa30b7fb0bb111f22d64b2fdb8b82042fe61768ecf247619(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsSampleAes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8416e2ce33897740fca0704fc74303c09cabe54e8535b48e3085d1c25660bca5(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8722178fd7cad1f3fea870c62494d4a83739165c99c8f920b72dc6eb4f5240ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb9d54c6cbdcb6079d74bb40c6fce98349e881238bc263b48f45d64d6dfc58f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfde0aa80532c2f6585dcc04933363c6c0c8d4fc6a26db4048e236f28b947b4d(
    value: typing.Optional[TranscoderJobTemplateConfigEncryptionsSecretManagerKeySource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563bde1254bd735fb6313081ded1f411209bd7793db4bafc9cde5788ad95fe10(
    *,
    key: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fc422ce158bd58c59136dd2cc8ef59943ccdfbd3c39ed073b9b8423ef5ce7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c288a00f402fae3e8d33d2f2ddca521cef09088d9de448bda5e99391b82b105(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49a16dc82a7d98c65f0ed94e310d01e649fa32e7c35b51a4292de594be66794(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3e73d65d11f9da68179b900e25101789816ffeb0b293cfe02576d5d04ad385(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5628c27754403d133efe2c3b794c08f243ed9b74676fbd15cc5db44a97f7b0f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abed7a70b269a4116301c54c47747c0fe59529bae8392c85d343c691443bdd9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigInputs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8479844506873589ff3bcf6fe517f8f8d13312ca2e2e391762106ab20edfd347(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67692380fbafeac76b046f51421743c03f4f69c1826d8270e99f55e8e23a0aca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e33b06cfab23043f1d2ff20c1e1fa2d5ff56919bdf5524b7437df73afb87d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786d6e6246a847907bbabb056b5e90886d497e450f88ae7e849e8eb3cc45e0a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigInputs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ea6da9630114869c4516f908b755e4edb58576cbfcbdb916f5b11c12116b08(
    *,
    file_name: typing.Optional[builtins.str] = None,
    mux_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac3d0d180deb3c88147a066340b494ee8816d6a6a899a44cc20826d302d65eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad8b9c2c8e4e20b55288cb0b34e09c52279c578417431a4c2b187a34d5cdca3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351a55ab193c608a2dfa6710468d903526c3fb07aa225e5ad59e4b7c19d64e65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dea94c9adb8b9a51418fec1d6d0e36bf99cdd7c81e6932b20a0db5efc861a2b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4960ba7f658d5876f872cb8ab2010efb54311530b53e092763a20c74145ca285(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5b8225f9da3fbaa48d3abfefb33870686793c70130cf5382a1b047b038a685(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigManifests]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdf4c2ea337041e731284b108a49cd90d14f3759904ac8a5175df58eb662dd7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58315335129422166f5f9817158bcd04a9d8394ed0d1b84c036175e9647013c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb89a501a0e43a9c25c52a0bf3a30243e8f0faf9c1d1cb4b5cf9ee8c49668d8a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfcaa2299d1df17baffa2f24549df3f61c26a18f2f8f56cf950c5879708a8712(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe609814951c491e98f5a8190e5be4d481e2a28cdc8f8738c022b7d4686c476(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigManifests]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00908041b849f74a7cf9e4fd72566572aec99e553374f4a32bb5d811ba4baf9(
    *,
    container: typing.Optional[builtins.str] = None,
    elementary_streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_id: typing.Optional[builtins.str] = None,
    file_name: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    segment_settings: typing.Optional[typing.Union[TranscoderJobTemplateConfigMuxStreamsSegmentSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e76a34fd747c28874e2fd935d12e28fe2b2f3850d1f6c6fe84aee21767c84f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8341e9e7d37799900448bd8f7f6840be206d8dae19e2172835f21df8417cc516(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e2c13e5e1cc2e44ebffdb31bd8fdeb650bd6c33d4a1a09e7d2bad3c94d9ee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e93d070b5fd74ce504d23a42a46e65c377991ba4c1de2ad09e609845df6c91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f0fce39e7fe4e95ce1e5c307ad22cfcca2386ae224189b5347ee99992fe1ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f8f0074a6b950b6d2cc3a7c781515eff16f3dc5f66b107a958334f37dc5b9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigMuxStreams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cac5ae13dd09a55a3b6cad4411d43b766b0685df1286e9d63754b4a3b1628dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e8f6287a25bdbba290edf95a4955153884e3562652d8a9ae53c308bc6d5137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43722850b67b02d4a9e30095693fc735d73aacb754f98956982f56941208ad7d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fdbd620e22dae8490ee48580bdb37a4066546fc577235b864689e031f62c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a0d0683fb98dacfcb661bcff5fc5a52c830ca949cf7feb9d7ffc61af50d67b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939a13231cb3b764bdf50de46dd27680df29f756fc468ff6fd1efe0e990dbfd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4161efb8d9616059e33a941c390cee08ecba83c94d26fc2ff890b2c9040b15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigMuxStreams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cabce345abbd32a880630de0cedef12b20f5ae558520a0cf01d2e09d17bbdf(
    *,
    segment_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbcbb7a9534ad302fd18837fbb582efa7225f80e7c9f85ec13d7703013a84e4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbd776b908cf2d95ef50452e639bf6dde0f05cb8114a2fcccd29e9f18c15cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabc3d509010876b22813ec9f8bf405c450ca9ec7dfbffcdf7cc8221de4cdb04(
    value: typing.Optional[TranscoderJobTemplateConfigMuxStreamsSegmentSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2083f04ecc8161edc4cae11f2da65bdb834b8b47af157eb87a36620d3dd8313a(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127cecb9301998ee5b2ab036d81930a4a5aa786d40c21d574a16d557fdd2634f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07b64a4acf313d5988e7f8fcb8854c9654a749125836d887305e5cdfa6a457c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5171ad24b7dd9e6416cb9659eb8ac9c710cc13928dbaba25ec769fdbbf7d27c(
    value: typing.Optional[TranscoderJobTemplateConfigOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9070065729daa28c0607510a35dfa24896da8ed964fcad5a7b8b1c9d873d46ea(
    *,
    animations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    image: typing.Optional[typing.Union[TranscoderJobTemplateConfigOverlaysImage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ab58da6371a7ba2f8a6ac89537c3a268d55ccb85beb79afad365ae5d5fc963(
    *,
    animation_fade: typing.Optional[typing.Union[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028b810054f7f36773b2686f9e570dfe869b97604f1020eb7ac9c8721263a829(
    *,
    fade_type: builtins.str,
    end_time_offset: typing.Optional[builtins.str] = None,
    start_time_offset: typing.Optional[builtins.str] = None,
    xy: typing.Optional[typing.Union[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be16536d57e98ee053bb9ae3023b6aaf3c6c4985bb6ac98b319957a27243b88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5fc6b0c428c6f07e449b34a2ed23f56c6bc343fbb9d5286b497b90a341fa85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037ec823c66fa7ae20b4f5347323cf0032dc58658b07ca8de85381dd4ceb8c29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b4386386856ae12f511070b677dd9592458479e5225e3651bcb1d2843bcf94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4b4b267c60ef8bac1710c422865a88c4d72559fe9fd740922a705d4a59f54f(
    value: typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFade],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc14838c845684dc5d35482d10fb19c4e35c6e7b4d0c73313a5ea3bd8379873(
    *,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb080a6aee5e875e83e94cf9c58c84c9a39451cb42860d7e83a5b0c4fb7200b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a23ee7204665ed370ea55eacd8323ef345d3fedd7b971e6c85adf96d1555c28(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d4a782f109498ab25974fdedcddc13471338ef748c2b6a02df96a4ac41e7d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672763e8876334fbc402eed13412bd0a4d918d33076439ff11b7c1b6e63fc400(
    value: typing.Optional[TranscoderJobTemplateConfigOverlaysAnimationsAnimationFadeXy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d4f39cda0607de1a3ebb13e4edf2f7809ad49f686614561f29bc16a99c9d99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a560597f487cf0d3ad4d158533675090311a9d89ab49a66329f7fd2dce4d465(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65382767936ec6cc7a346ca622acb1e5a2cacc4f924da77f5cec339ad9f73fbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58515444aaec2bbe00e76d7abf920e1d079c2e568893a8b2e4c7fea3743419b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7d28e0317399f4c737befc6f748fcc8e9f72211df89dab1269aafd963ef9ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dcc38606315b4642e64857b94867987231a9ff2b295e51e72045d61d9e29ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlaysAnimations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d0868084a0431152d59480bc2c03d2f4a1efc061e76dd24e5e564969dc2bd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d72e2956f6a3298741928ddbea27ca9668e078c1b34a98b670ca5981912849(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigOverlaysAnimations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f47c3df33d12942c4d19d9780aef23e225e030b7cc1382f50309b8875db90d(
    *,
    uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236ca091ca9fc9ff0c91e077c7a7e5fe3897f0e42aec1447fc46b7ee8eed7adf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4c8e9020508501ecc6229e8dc3b22a2019e62c7c26c21b9ddffc3c684ba08b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d23f45be72817ce619ed33e2638b75a53a96723c6d8068d5d5efe119015479f(
    value: typing.Optional[TranscoderJobTemplateConfigOverlaysImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828ee35d321e2a535ae99dd59c9076fd98f07330a57648abd9da024bd4dd9e51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d9365149e669ee26e911bb6136440556de929118e2d1a1da8d1c59d3bad5da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c5785f720ea95482bc4ab09fb265a3c2f18c5227c33bd1aa60fea616bc5022(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567c8e2e6b724a548fbca77fe13464c974d66a0fe0a4564f131b0efa31a7374a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11689189af79c37085ab9cbfcca829fa6605d462d6ec7e4dd9bd53a892068c17(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9c0f8b39c99357752d12b8e8ab5c138c936b64294b8798f8c8d2f7e8ad2c3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TranscoderJobTemplateConfigOverlays]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315c0fe7c4f609bbccc1afa97b673e24abf793436adfe75fdc0ba3a851ea9845(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e09159dd4db3efdef4292847839b3f53b5f0c899bed3f47cafe886516a2e1f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TranscoderJobTemplateConfigOverlaysAnimations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff863af21761d7effaaf9d16c26ee405f69697e79fb7e9d811f766baaa2bd7f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateConfigOverlays]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8112dc4ea283b4dc463ede4aa6a0a0d86a11203f8da7ce7a80a6a078c971fa(
    *,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b6e2844c83e9b0e220cb0a7dc3fa48d33fb70abcb8470c8009785ce63e3cd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d235d3e012859b324fd75bdaa99040106f1c1670b940b64d4517aa8d3d2d9ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469d3411897351101793653d49dc452fa3f875ee5a0554db725e9c9e3819482e(
    value: typing.Optional[TranscoderJobTemplateConfigPubsubDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8b03c76ebad5184e4368c97bffb9600cfa329d0097968a5b680e14bb4b337a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65e616e8f60e56a947d8159fb3c420d1f76f71802b2a77f83fc2833133736c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901c9c638c1c8f6b68286e7536338b63912304cd397086c67ad20eabdb77befe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4a598c1260e017ac8b1656d47d83fcfb261ecda4eda43eb2c523638900946d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3e11188a4a6f4cf9214817309fcd7468687756fa54674f253f7df01e6b5507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6261fd2f9d0be6fa6a6915dea2a784b926f82922dde2f04a9eea3a4e9f1bc2d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TranscoderJobTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
