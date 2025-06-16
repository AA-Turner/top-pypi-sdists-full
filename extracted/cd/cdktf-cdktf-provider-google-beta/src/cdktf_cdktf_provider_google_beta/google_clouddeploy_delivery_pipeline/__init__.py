r'''
# `google_clouddeploy_delivery_pipeline`

Refer to the Terraform Registry for docs: [`google_clouddeploy_delivery_pipeline`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline).
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


class GoogleClouddeployDeliveryPipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline google_clouddeploy_delivery_pipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        serial_pipeline: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipeline", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline google_clouddeploy_delivery_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#location GoogleClouddeployDeliveryPipeline#location}
        :param name: Name of the ``DeliveryPipeline``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#name GoogleClouddeployDeliveryPipeline#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#annotations GoogleClouddeployDeliveryPipeline#annotations}
        :param description: Description of the ``DeliveryPipeline``. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#description GoogleClouddeployDeliveryPipeline#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#id GoogleClouddeployDeliveryPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#labels GoogleClouddeployDeliveryPipeline#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#project GoogleClouddeployDeliveryPipeline#project}
        :param serial_pipeline: serial_pipeline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#serial_pipeline GoogleClouddeployDeliveryPipeline#serial_pipeline}
        :param suspended: When suspended, no new releases or rollouts can be created, but in-progress ones will complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#suspended GoogleClouddeployDeliveryPipeline#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#timeouts GoogleClouddeployDeliveryPipeline#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b55bc45b3ebdd6f7c310f804dad347588e73194b4b19d07f1ae1076afd61bac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleClouddeployDeliveryPipelineConfig(
            location=location,
            name=name,
            annotations=annotations,
            description=description,
            id=id,
            labels=labels,
            project=project,
            serial_pipeline=serial_pipeline,
            suspended=suspended,
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
        '''Generates CDKTF code for importing a GoogleClouddeployDeliveryPipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleClouddeployDeliveryPipeline to import.
        :param import_from_id: The id of the existing GoogleClouddeployDeliveryPipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleClouddeployDeliveryPipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486b96d403f91955495fc04e0e7c91cc3b7061ad9cf3f6a5dfd64d0efcc4e238)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSerialPipeline")
    def put_serial_pipeline(
        self,
        *,
        stages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param stages: stages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stages GoogleClouddeployDeliveryPipeline#stages}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipeline(stages=stages)

        return typing.cast(None, jsii.invoke(self, "putSerialPipeline", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#create GoogleClouddeployDeliveryPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#delete GoogleClouddeployDeliveryPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#update GoogleClouddeployDeliveryPipeline#update}.
        '''
        value = GoogleClouddeployDeliveryPipelineTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSerialPipeline")
    def reset_serial_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerialPipeline", []))

    @jsii.member(jsii_name="resetSuspended")
    def reset_suspended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspended", []))

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
    @jsii.member(jsii_name="condition")
    def condition(self) -> "GoogleClouddeployDeliveryPipelineConditionList":
        return typing.cast("GoogleClouddeployDeliveryPipelineConditionList", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

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
    @jsii.member(jsii_name="serialPipeline")
    def serial_pipeline(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineOutputReference", jsii.get(self, "serialPipeline"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleClouddeployDeliveryPipelineTimeoutsOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serialPipelineInput")
    def serial_pipeline_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipeline"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipeline"], jsii.get(self, "serialPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedInput")
    def suspended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suspendedInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployDeliveryPipelineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployDeliveryPipelineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304cb9088ef7d0debe18b24ad2d8f938cb7e88adc87f7db37449f6cea4659b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c2b3ab604c1a5d5980e61cfa0dfd3ec3c20c50752151094bea5ba55ed8dbd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b37ff579e684bc1dbed3cf5a92079c35b75677a9dd31e80dddadcbcc038023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4025c3d084f982e3945e8416239bf5cbceb5dbb9e23b7dc1a2bd9a5b5b33575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26cf533211b422a3eb5ced0b50cee50561f2829d7cc1b9bf073af03864cc146d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c0185ac1c437944470e77ab166e3965af0d4ceba7815a459170e0fa863bb2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac3ba9d34bfa4b93318d6c083f45525c7cb47c7bb18b8b67373b9c0a5cef5d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspended")
    def suspended(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suspended"))

    @suspended.setter
    def suspended(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99585f358e3bc5ad6fe8da048320bc9641e2c273f954c813cfe5da6b41b626f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleClouddeployDeliveryPipelineCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c48ad054e924f72aa9e0ca0478fc7dff32503cc86e69491c33188906b2c738fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeliveryPipelineConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45a18dd94faccbc095dd7d9bc4fa5b1b65f0e03c9504427aa8cc3fa1089e48e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeliveryPipelineConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd81e6774268527239803443dfc3374b445cdafec82b929b94da85a73a0b0d86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33d5af5e5a5ce5df42693893390450cdd44610891dfc6ed0cd34829f4d937eae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79f249d5af39c324741096198c9ec2a48a0c4df151c3c8761d6a56135527dd1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c92de1d7b9ef4e8b9b6e35c64fb873b2d34731f203d2d3cdca94f6dc32db7e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pipelineReadyCondition")
    def pipeline_ready_condition(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionList":
        return typing.cast("GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionList", jsii.get(self, "pipelineReadyCondition"))

    @builtins.property
    @jsii.member(jsii_name="targetsPresentCondition")
    def targets_present_condition(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionList":
        return typing.cast("GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionList", jsii.get(self, "targetsPresentCondition"))

    @builtins.property
    @jsii.member(jsii_name="targetsTypeCondition")
    def targets_type_condition(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionList":
        return typing.cast("GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionList", jsii.get(self, "targetsTypeCondition"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineCondition]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6553b8d42b3ed70ef38ebff84a89250b05bac7a732876295c9468ffbf2f7b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionPipelineReadyCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleClouddeployDeliveryPipelineConditionPipelineReadyCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineConditionPipelineReadyCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ca8e0c667be452658dfafad17f113327c17a00fcc36fd30cf6c6dddde977133)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c649390d4443a09dbbd9907ac37db0f036697ca62651d11fbc3f50d88a2d7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9467983c402a0cbbb6128b56a5a0f034a32912644fb8632ace98d4d9feda3877)
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
            type_hints = typing.get_type_hints(_typecheckingstub__527bb4a78a6b01cc9539f17fb26271e17c3db860a44844fef2ba83124971550e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a04eec647d5f10c58d380ce70d366bc310ac1e74f17eb87119e6b3967d1ba47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64f7598cfeb5bea99a4e01763d99869272cc84cdb82170940e4587c6dd053203)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineConditionPipelineReadyCondition]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineConditionPipelineReadyCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineConditionPipelineReadyCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d7ac06c4d84737262bd13ef99df8d08c329ea287ee481a8c732ecef44dcae9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionTargetsPresentCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleClouddeployDeliveryPipelineConditionTargetsPresentCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineConditionTargetsPresentCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a3e79eed1b61895228c74a9d6b46f4dc48d38d587787ad3356ffbdebb7e775)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b3c34bd43fca7ef56c0b8f2c3b64b19d59b842066f336e191578bbe3bf1cba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae229339d7198d94a486f613363b9963756b98e8b50291f951352f361bc9882)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9355fd85d1684f1c10ac9bccf464fde15712c5a250d0d3774ffe79bb7fa7f288)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e353d7c1cc474ba3ca7cf7ac1c67fadce6e0d8e6dfec9e2113300b4279877caa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d3c5923e98072637668e277406dba65ba537e09a2916819172be466b4aed693)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="missingTargets")
    def missing_targets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "missingTargets"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineConditionTargetsPresentCondition]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineConditionTargetsPresentCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineConditionTargetsPresentCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c42c110426423ee9a1441e569aa34ede94bb0b9a219a0ad5026c022e65d994b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionTargetsTypeCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleClouddeployDeliveryPipelineConditionTargetsTypeCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineConditionTargetsTypeCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d294265df84b8116459f81e5bf7d74d82389358b914a2ffa198377a32d0b475)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bea6abd212a33f1e8772b718f29c8feb645e9aa9c6db1643cc5fae5ca652293)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4cc1c0f7054cbacbefffa71bc040c5f1d2b1d368e0468e9e608ccdbb8e69df7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__195d89630e23841e0b41220bfac8dd625d97fcb369ad1071af80b2f0a7c0fdc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__794a42cbd2639f5b353c0390b1ea28c2420ff385a2f78383056397c503bd9f10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__610bd6207857e9222d88580bcb7d5549aa9d2798bd1249736a0c2cb952b6d800)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="errorDetails")
    def error_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorDetails"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineConditionTargetsTypeCondition]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineConditionTargetsTypeCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineConditionTargetsTypeCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba81af60db414105b3e97aacf41fb1e12aa9d0dde0d273d71bcf7b188f8aaddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineConfig",
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
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "serial_pipeline": "serialPipeline",
        "suspended": "suspended",
        "timeouts": "timeouts",
    },
)
class GoogleClouddeployDeliveryPipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        serial_pipeline: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipeline", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#location GoogleClouddeployDeliveryPipeline#location}
        :param name: Name of the ``DeliveryPipeline``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#name GoogleClouddeployDeliveryPipeline#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#annotations GoogleClouddeployDeliveryPipeline#annotations}
        :param description: Description of the ``DeliveryPipeline``. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#description GoogleClouddeployDeliveryPipeline#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#id GoogleClouddeployDeliveryPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#labels GoogleClouddeployDeliveryPipeline#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#project GoogleClouddeployDeliveryPipeline#project}
        :param serial_pipeline: serial_pipeline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#serial_pipeline GoogleClouddeployDeliveryPipeline#serial_pipeline}
        :param suspended: When suspended, no new releases or rollouts can be created, but in-progress ones will complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#suspended GoogleClouddeployDeliveryPipeline#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#timeouts GoogleClouddeployDeliveryPipeline#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(serial_pipeline, dict):
            serial_pipeline = GoogleClouddeployDeliveryPipelineSerialPipeline(**serial_pipeline)
        if isinstance(timeouts, dict):
            timeouts = GoogleClouddeployDeliveryPipelineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa7d8c0bbde56ab348740e0ab529665a6c5a196d9e74e8ffd7eb25a13ec4eb3)
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
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument serial_pipeline", value=serial_pipeline, expected_type=type_hints["serial_pipeline"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if serial_pipeline is not None:
            self._values["serial_pipeline"] = serial_pipeline
        if suspended is not None:
            self._values["suspended"] = suspended
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#location GoogleClouddeployDeliveryPipeline#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the ``DeliveryPipeline``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#name GoogleClouddeployDeliveryPipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User annotations.

        These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field ``effective_annotations`` for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#annotations GoogleClouddeployDeliveryPipeline#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the ``DeliveryPipeline``. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#description GoogleClouddeployDeliveryPipeline#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#id GoogleClouddeployDeliveryPipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are attributes that can be set and used by both the user and by Google Cloud Deploy.

        Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field ``effective_labels`` for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#labels GoogleClouddeployDeliveryPipeline#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#project GoogleClouddeployDeliveryPipeline#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_pipeline(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipeline"]:
        '''serial_pipeline block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#serial_pipeline GoogleClouddeployDeliveryPipeline#serial_pipeline}
        '''
        result = self._values.get("serial_pipeline")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipeline"], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When suspended, no new releases or rollouts can be created, but in-progress ones will complete.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#suspended GoogleClouddeployDeliveryPipeline#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleClouddeployDeliveryPipelineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#timeouts GoogleClouddeployDeliveryPipeline#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipeline",
    jsii_struct_bases=[],
    name_mapping={"stages": "stages"},
)
class GoogleClouddeployDeliveryPipelineSerialPipeline:
    def __init__(
        self,
        *,
        stages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param stages: stages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stages GoogleClouddeployDeliveryPipeline#stages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e3664541fccfdbf694f881712cc009c248f3139b5b4b090135829a8b6463f9)
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if stages is not None:
            self._values["stages"] = stages

    @builtins.property
    def stages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStages"]]]:
        '''stages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stages GoogleClouddeployDeliveryPipeline#stages}
        '''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipeline(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5945a2091550c193269b98d05830bda2155d19965f369b375fdd1f3dac451b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStages")
    def put_stages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f629910366e4f8c42c90e99e66d169d062658f65e6bd029966145dab03691c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStages", [value]))

    @jsii.member(jsii_name="resetStages")
    def reset_stages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStages", []))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesList":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesList", jsii.get(self, "stages"))

    @builtins.property
    @jsii.member(jsii_name="stagesInput")
    def stages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStages"]]], jsii.get(self, "stagesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipeline]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipeline], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipeline],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a950130d66c5a27e52e13e02b2bd9e89a1d896d9b00d7a7f4b7e320f36774cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStages",
    jsii_struct_bases=[],
    name_mapping={
        "deploy_parameters": "deployParameters",
        "profiles": "profiles",
        "strategy": "strategy",
        "target_id": "targetId",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStages:
    def __init__(
        self,
        *,
        deploy_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
        strategy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        target_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deploy_parameters: deploy_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#deploy_parameters GoogleClouddeployDeliveryPipeline#deploy_parameters}
        :param profiles: Skaffold profiles to use when rendering the manifest for this stage's ``Target``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#profiles GoogleClouddeployDeliveryPipeline#profiles}
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#strategy GoogleClouddeployDeliveryPipeline#strategy}
        :param target_id: The target_id to which this stage points. This field refers exclusively to the last segment of a target name. For example, this field would just be ``my-target`` (rather than ``projects/project/locations/location/targets/my-target``). The location of the ``Target`` is inferred to be the same as the location of the ``DeliveryPipeline`` that contains this ``Stage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#target_id GoogleClouddeployDeliveryPipeline#target_id}
        '''
        if isinstance(strategy, dict):
            strategy = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c77944373e30764a11ad3ec7b6d167d4385bb4293f574ed2af6cb2136a694f)
            check_type(argname="argument deploy_parameters", value=deploy_parameters, expected_type=type_hints["deploy_parameters"])
            check_type(argname="argument profiles", value=profiles, expected_type=type_hints["profiles"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deploy_parameters is not None:
            self._values["deploy_parameters"] = deploy_parameters
        if profiles is not None:
            self._values["profiles"] = profiles
        if strategy is not None:
            self._values["strategy"] = strategy
        if target_id is not None:
            self._values["target_id"] = target_id

    @builtins.property
    def deploy_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters"]]]:
        '''deploy_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#deploy_parameters GoogleClouddeployDeliveryPipeline#deploy_parameters}
        '''
        result = self._values.get("deploy_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters"]]], result)

    @builtins.property
    def profiles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Skaffold profiles to use when rendering the manifest for this stage's ``Target``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#profiles GoogleClouddeployDeliveryPipeline#profiles}
        '''
        result = self._values.get("profiles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def strategy(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy"]:
        '''strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#strategy GoogleClouddeployDeliveryPipeline#strategy}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy"], result)

    @builtins.property
    def target_id(self) -> typing.Optional[builtins.str]:
        '''The target_id to which this stage points.

        This field refers exclusively to the last segment of a target name. For example, this field would just be ``my-target`` (rather than ``projects/project/locations/location/targets/my-target``). The location of the ``Target`` is inferred to be the same as the location of the ``DeliveryPipeline`` that contains this ``Stage``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#target_id GoogleClouddeployDeliveryPipeline#target_id}
        '''
        result = self._values.get("target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters",
    jsii_struct_bases=[],
    name_mapping={"values": "values", "match_target_labels": "matchTargetLabels"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters:
    def __init__(
        self,
        *,
        values: typing.Mapping[builtins.str, builtins.str],
        match_target_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param values: Required. Values are deploy parameters in key-value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#values GoogleClouddeployDeliveryPipeline#values}
        :param match_target_labels: Optional. Deploy parameters are applied to targets with match labels. If unspecified, deploy parameters are applied to all targets (including child targets of a multi-target). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#match_target_labels GoogleClouddeployDeliveryPipeline#match_target_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8b61115abb669289db7d072bbf7bbb07de312859171696e658464b72ceafd7)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument match_target_labels", value=match_target_labels, expected_type=type_hints["match_target_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "values": values,
        }
        if match_target_labels is not None:
            self._values["match_target_labels"] = match_target_labels

    @builtins.property
    def values(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Required. Values are deploy parameters in key-value pairs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#values GoogleClouddeployDeliveryPipeline#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def match_target_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Deploy parameters are applied to targets with match labels. If unspecified, deploy parameters are applied to all targets (including child targets of a multi-target).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#match_target_labels GoogleClouddeployDeliveryPipeline#match_target_labels}
        '''
        result = self._values.get("match_target_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abf28ddfa5933cdc600909120e61282141bacdb3b69001f94f0147735305368d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9005d0485c82c1f5dc453ffc5a8c4849b85fc545dec101cb3b0b7daf3739062)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7100d4edc95e17d5c5a192043238e9dcfde7bcfc69413e7e16045ba2237745f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fcf26473135d13ce75147f1743190efcea5b92f86b41f79f6592486504ea59f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f55b13361879cd3729dbe02e844b204aa84f50076f4a3a9adf4dca8bab2923e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3a7977208b25971093c7aa687689f9a1f571c009c2a950f3328990cfd5ff68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2984148ca6901306bd9ee0ec189fd1974fb15c4259bb35bd27e200063c27c9b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchTargetLabels")
    def reset_match_target_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchTargetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="matchTargetLabelsInput")
    def match_target_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "matchTargetLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchTargetLabels")
    def match_target_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "matchTargetLabels"))

    @match_target_labels.setter
    def match_target_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529213850ac322e1ad86d09883f09ce48dec2ba1e141a1ef314ce998c7e88870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchTargetLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ac50e7ce63c4ccbd53ae67d14246c9d6eb5b7b98621c5acbdb5f59fe71a558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dfe0312694666a5e71de2b200e3deb2c1df8b0956f67a0ec045f0bad495080a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb6f8488b16345923805e1992a4945999100d05636a906bb654def8c92f5d6f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72422b20cf9b19db3192e7fb33d63d08fd4a5e70fdebcd347512067ae175b8b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b864ccefcc85e50d61610fce9624b91aa6d6721388a5f7d28df00f0db1d9a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b0426ad94c858bce76ffbeb7d66fbec2350cca9dbf61abea37445b181131628)
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
            type_hints = typing.get_type_hints(_typecheckingstub__436eb70260b985d86ddaa101b50d94723ce67ff82637450ceaf4bd8685908123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a34e7e6f19a0c3afbb5c7f52368de55fb9a21008d313c0622c445686f9f4067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9967898f60c765aafe7de483eba6bdd623080edb9e7df3f58c7e682478a1e698)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDeployParameters")
    def put_deploy_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21428197ad1d9f919a05b53601001f7779cee1edfe154a3f4a79ff32512a7a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeployParameters", [value]))

    @jsii.member(jsii_name="putStrategy")
    def put_strategy(
        self,
        *,
        canary: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary", typing.Dict[builtins.str, typing.Any]]] = None,
        standard: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param canary: canary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary GoogleClouddeployDeliveryPipeline#canary}
        :param standard: standard block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#standard GoogleClouddeployDeliveryPipeline#standard}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy(
            canary=canary, standard=standard
        )

        return typing.cast(None, jsii.invoke(self, "putStrategy", [value]))

    @jsii.member(jsii_name="resetDeployParameters")
    def reset_deploy_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeployParameters", []))

    @jsii.member(jsii_name="resetProfiles")
    def reset_profiles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfiles", []))

    @jsii.member(jsii_name="resetStrategy")
    def reset_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrategy", []))

    @jsii.member(jsii_name="resetTargetId")
    def reset_target_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetId", []))

    @builtins.property
    @jsii.member(jsii_name="deployParameters")
    def deploy_parameters(
        self,
    ) -> GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList:
        return typing.cast(GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList, jsii.get(self, "deployParameters"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference", jsii.get(self, "strategy"))

    @builtins.property
    @jsii.member(jsii_name="deployParametersInput")
    def deploy_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]], jsii.get(self, "deployParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="profilesInput")
    def profiles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "profilesInput"))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy"], jsii.get(self, "strategyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetIdInput")
    def target_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="profiles")
    def profiles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "profiles"))

    @profiles.setter
    def profiles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe3aade4d5c246e52e50e1e5542156d40240f86214e0940b026fe5f126bb8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetId"))

    @target_id.setter
    def target_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d9a007566267755ed1aaba4fce9f6267af2ed97f09c3c8b45629432f4e515b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d9c2e22d6229b1fc1cbf219b851e319fbff83e82f532b8c4b628d668f26b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy",
    jsii_struct_bases=[],
    name_mapping={"canary": "canary", "standard": "standard"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy:
    def __init__(
        self,
        *,
        canary: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary", typing.Dict[builtins.str, typing.Any]]] = None,
        standard: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param canary: canary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary GoogleClouddeployDeliveryPipeline#canary}
        :param standard: standard block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#standard GoogleClouddeployDeliveryPipeline#standard}
        '''
        if isinstance(canary, dict):
            canary = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary(**canary)
        if isinstance(standard, dict):
            standard = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard(**standard)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11def406533660312fcb8c410e6f6d00fefe2c8cc0120bd848e09093731a29b8)
            check_type(argname="argument canary", value=canary, expected_type=type_hints["canary"])
            check_type(argname="argument standard", value=standard, expected_type=type_hints["standard"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if canary is not None:
            self._values["canary"] = canary
        if standard is not None:
            self._values["standard"] = standard

    @builtins.property
    def canary(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary"]:
        '''canary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary GoogleClouddeployDeliveryPipeline#canary}
        '''
        result = self._values.get("canary")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary"], result)

    @builtins.property
    def standard(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard"]:
        '''standard block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#standard GoogleClouddeployDeliveryPipeline#standard}
        '''
        result = self._values.get("standard")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary",
    jsii_struct_bases=[],
    name_mapping={
        "canary_deployment": "canaryDeployment",
        "custom_canary_deployment": "customCanaryDeployment",
        "runtime_config": "runtimeConfig",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary:
    def __init__(
        self,
        *,
        canary_deployment: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_canary_deployment: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_config: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param canary_deployment: canary_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary_deployment GoogleClouddeployDeliveryPipeline#canary_deployment}
        :param custom_canary_deployment: custom_canary_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#custom_canary_deployment GoogleClouddeployDeliveryPipeline#custom_canary_deployment}
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#runtime_config GoogleClouddeployDeliveryPipeline#runtime_config}
        '''
        if isinstance(canary_deployment, dict):
            canary_deployment = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment(**canary_deployment)
        if isinstance(custom_canary_deployment, dict):
            custom_canary_deployment = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment(**custom_canary_deployment)
        if isinstance(runtime_config, dict):
            runtime_config = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig(**runtime_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352b49f14c99d5902add6cbfd3e8574f72a26d342fdf3bbd3861548c451c5701)
            check_type(argname="argument canary_deployment", value=canary_deployment, expected_type=type_hints["canary_deployment"])
            check_type(argname="argument custom_canary_deployment", value=custom_canary_deployment, expected_type=type_hints["custom_canary_deployment"])
            check_type(argname="argument runtime_config", value=runtime_config, expected_type=type_hints["runtime_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if canary_deployment is not None:
            self._values["canary_deployment"] = canary_deployment
        if custom_canary_deployment is not None:
            self._values["custom_canary_deployment"] = custom_canary_deployment
        if runtime_config is not None:
            self._values["runtime_config"] = runtime_config

    @builtins.property
    def canary_deployment(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment"]:
        '''canary_deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary_deployment GoogleClouddeployDeliveryPipeline#canary_deployment}
        '''
        result = self._values.get("canary_deployment")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment"], result)

    @builtins.property
    def custom_canary_deployment(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment"]:
        '''custom_canary_deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#custom_canary_deployment GoogleClouddeployDeliveryPipeline#custom_canary_deployment}
        '''
        result = self._values.get("custom_canary_deployment")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment"], result)

    @builtins.property
    def runtime_config(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig"]:
        '''runtime_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#runtime_config GoogleClouddeployDeliveryPipeline#runtime_config}
        '''
        result = self._values.get("runtime_config")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment",
    jsii_struct_bases=[],
    name_mapping={
        "percentages": "percentages",
        "postdeploy": "postdeploy",
        "predeploy": "predeploy",
        "verify": "verify",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment:
    def __init__(
        self,
        *,
        percentages: typing.Sequence[jsii.Number],
        postdeploy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param percentages: Required. The percentage based deployments that will occur as a part of a ``Rollout``. List is expected in ascending order and each integer n is 0 <= n < 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#percentages GoogleClouddeployDeliveryPipeline#percentages}
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#postdeploy GoogleClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#predeploy GoogleClouddeployDeliveryPipeline#predeploy}
        :param verify: Whether to run verify tests after each percentage deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#verify GoogleClouddeployDeliveryPipeline#verify}
        '''
        if isinstance(postdeploy, dict):
            postdeploy = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy(**postdeploy)
        if isinstance(predeploy, dict):
            predeploy = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy(**predeploy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a03804f56da33e28f7bd7a93810a066d810e85dd23bd5e37aca1dfcd86217ef)
            check_type(argname="argument percentages", value=percentages, expected_type=type_hints["percentages"])
            check_type(argname="argument postdeploy", value=postdeploy, expected_type=type_hints["postdeploy"])
            check_type(argname="argument predeploy", value=predeploy, expected_type=type_hints["predeploy"])
            check_type(argname="argument verify", value=verify, expected_type=type_hints["verify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "percentages": percentages,
        }
        if postdeploy is not None:
            self._values["postdeploy"] = postdeploy
        if predeploy is not None:
            self._values["predeploy"] = predeploy
        if verify is not None:
            self._values["verify"] = verify

    @builtins.property
    def percentages(self) -> typing.List[jsii.Number]:
        '''Required.

        The percentage based deployments that will occur as a part of a ``Rollout``. List is expected in ascending order and each integer n is 0 <= n < 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#percentages GoogleClouddeployDeliveryPipeline#percentages}
        '''
        result = self._values.get("percentages")
        assert result is not None, "Required property 'percentages' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def postdeploy(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy"]:
        '''postdeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#postdeploy GoogleClouddeployDeliveryPipeline#postdeploy}
        '''
        result = self._values.get("postdeploy")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy"], result)

    @builtins.property
    def predeploy(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy"]:
        '''predeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#predeploy GoogleClouddeployDeliveryPipeline#predeploy}
        '''
        result = self._values.get("predeploy")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy"], result)

    @builtins.property
    def verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run verify tests after each percentage deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#verify GoogleClouddeployDeliveryPipeline#verify}
        '''
        result = self._values.get("verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fb6d0145df968ed99061335712183360976af549fd012bf515f19bf24908ada)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostdeploy")
    def put_postdeploy(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy(
            actions=actions
        )

        return typing.cast(None, jsii.invoke(self, "putPostdeploy", [value]))

    @jsii.member(jsii_name="putPredeploy")
    def put_predeploy(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy(
            actions=actions
        )

        return typing.cast(None, jsii.invoke(self, "putPredeploy", [value]))

    @jsii.member(jsii_name="resetPostdeploy")
    def reset_postdeploy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostdeploy", []))

    @jsii.member(jsii_name="resetPredeploy")
    def reset_predeploy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredeploy", []))

    @jsii.member(jsii_name="resetVerify")
    def reset_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerify", []))

    @builtins.property
    @jsii.member(jsii_name="postdeploy")
    def postdeploy(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference", jsii.get(self, "postdeploy"))

    @builtins.property
    @jsii.member(jsii_name="predeploy")
    def predeploy(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference", jsii.get(self, "predeploy"))

    @builtins.property
    @jsii.member(jsii_name="percentagesInput")
    def percentages_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "percentagesInput"))

    @builtins.property
    @jsii.member(jsii_name="postdeployInput")
    def postdeploy_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy"], jsii.get(self, "postdeployInput"))

    @builtins.property
    @jsii.member(jsii_name="predeployInput")
    def predeploy_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy"], jsii.get(self, "predeployInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyInput")
    def verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyInput"))

    @builtins.property
    @jsii.member(jsii_name="percentages")
    def percentages(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "percentages"))

    @percentages.setter
    def percentages(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435d37ba65571cc605f457c312e58037f31674c871bed51980eea128141c8fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verify")
    def verify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verify"))

    @verify.setter
    def verify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a7054b22d42615af052d42d8f8a33bedfc31012d844cbb5fdc865691842edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25994b6cd177deed712267c97066fded5f3c9abe2e24fa56d962be7a69d634a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6c272180abc3ac252df80260c188a660fe0f79817e50978701efeb266b76aa)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4298581324f73c0908dae287ef7e4589abdbca56ba14dc59197dde7b77783bae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed0df3acf294ea843ac70dde79b10ef7fb68c393d54136ec99c2bce30485841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb78e537d07e6336f5c33ab6900f251508746c13c78de3dd4566e19441d28494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b53b6469b8ca9194c8852a1d892bbef690899ffe98b1e2ef62a03a8e442548)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1766a5a18420aaa68d45101fc382dafc7faef9d9dc60a49fe4297a7d86df5b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a534280336beaf07bf7c895d5cc886b617cc1069e5bc13a8dd10df87e8c47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f58b1f7f856267399c5ef97d78026119e4e735db111e06123637e6bacc96ec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment",
    jsii_struct_bases=[],
    name_mapping={"phase_configs": "phaseConfigs"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment:
    def __init__(
        self,
        *,
        phase_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param phase_configs: phase_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#phase_configs GoogleClouddeployDeliveryPipeline#phase_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a95eb3da3a4ee5088509e22d5473a91ddca1c77a9db26b2b9eee0233ba399b)
            check_type(argname="argument phase_configs", value=phase_configs, expected_type=type_hints["phase_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phase_configs": phase_configs,
        }

    @builtins.property
    def phase_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs"]]:
        '''phase_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#phase_configs GoogleClouddeployDeliveryPipeline#phase_configs}
        '''
        result = self._values.get("phase_configs")
        assert result is not None, "Required property 'phase_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f10402ed2f3a0d21e484fa96b84659b6657454d1f4886c0715f2743d6a76ff0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPhaseConfigs")
    def put_phase_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6105aaf9e6226a2ed0db50703f51e9a347d1ece6f15887c7a0b2030972004cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPhaseConfigs", [value]))

    @builtins.property
    @jsii.member(jsii_name="phaseConfigs")
    def phase_configs(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList", jsii.get(self, "phaseConfigs"))

    @builtins.property
    @jsii.member(jsii_name="phaseConfigsInput")
    def phase_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs"]]], jsii.get(self, "phaseConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2be5d623768e2f59a6aaacab401b3e671fcc00ce6fff7faf576ca4287e2a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "percentage": "percentage",
        "phase_id": "phaseId",
        "postdeploy": "postdeploy",
        "predeploy": "predeploy",
        "profiles": "profiles",
        "verify": "verify",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs:
    def __init__(
        self,
        *,
        percentage: jsii.Number,
        phase_id: builtins.str,
        postdeploy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param percentage: Required. Percentage deployment for the phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#percentage GoogleClouddeployDeliveryPipeline#percentage}
        :param phase_id: Required. The ID to assign to the ``Rollout`` phase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ``^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#phase_id GoogleClouddeployDeliveryPipeline#phase_id}
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#postdeploy GoogleClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#predeploy GoogleClouddeployDeliveryPipeline#predeploy}
        :param profiles: Skaffold profiles to use when rendering the manifest for this phase. These are in addition to the profiles list specified in the ``DeliveryPipeline`` stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#profiles GoogleClouddeployDeliveryPipeline#profiles}
        :param verify: Whether to run verify tests after the deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#verify GoogleClouddeployDeliveryPipeline#verify}
        '''
        if isinstance(postdeploy, dict):
            postdeploy = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy(**postdeploy)
        if isinstance(predeploy, dict):
            predeploy = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy(**predeploy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ce62687fe3c5867c21c5f0a7dd362fb27be9ffa85e893c1b42b1ba0d711c86)
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
            check_type(argname="argument phase_id", value=phase_id, expected_type=type_hints["phase_id"])
            check_type(argname="argument postdeploy", value=postdeploy, expected_type=type_hints["postdeploy"])
            check_type(argname="argument predeploy", value=predeploy, expected_type=type_hints["predeploy"])
            check_type(argname="argument profiles", value=profiles, expected_type=type_hints["profiles"])
            check_type(argname="argument verify", value=verify, expected_type=type_hints["verify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "percentage": percentage,
            "phase_id": phase_id,
        }
        if postdeploy is not None:
            self._values["postdeploy"] = postdeploy
        if predeploy is not None:
            self._values["predeploy"] = predeploy
        if profiles is not None:
            self._values["profiles"] = profiles
        if verify is not None:
            self._values["verify"] = verify

    @builtins.property
    def percentage(self) -> jsii.Number:
        '''Required. Percentage deployment for the phase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#percentage GoogleClouddeployDeliveryPipeline#percentage}
        '''
        result = self._values.get("percentage")
        assert result is not None, "Required property 'percentage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def phase_id(self) -> builtins.str:
        '''Required.

        The ID to assign to the ``Rollout`` phase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ``^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#phase_id GoogleClouddeployDeliveryPipeline#phase_id}
        '''
        result = self._values.get("phase_id")
        assert result is not None, "Required property 'phase_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postdeploy(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy"]:
        '''postdeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#postdeploy GoogleClouddeployDeliveryPipeline#postdeploy}
        '''
        result = self._values.get("postdeploy")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy"], result)

    @builtins.property
    def predeploy(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy"]:
        '''predeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#predeploy GoogleClouddeployDeliveryPipeline#predeploy}
        '''
        result = self._values.get("predeploy")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy"], result)

    @builtins.property
    def profiles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Skaffold profiles to use when rendering the manifest for this phase.

        These are in addition to the profiles list specified in the ``DeliveryPipeline`` stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#profiles GoogleClouddeployDeliveryPipeline#profiles}
        '''
        result = self._values.get("profiles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run verify tests after the deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#verify GoogleClouddeployDeliveryPipeline#verify}
        '''
        result = self._values.get("verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92155f627463f6b3dd490fd900c017f869e5d8656ecb0d6605c661f66c443607)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176b59bcbf8684f7bf0a06926ff1d85927e37e32f019d38fbecfc9bcef6403f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab086b70b51ec58057bcaf523cade9f0f3bcb285b30f6bdf877ab155510e8e6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d64f071c360ba3f854c5faf680f568c8e45b8a4a12163248c7ca36afda022e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44ead080f7c71cb4f6bb9f62d4b167f051a59790303aa61975146ec09b364b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af2a8170f6e69b228f0f76daa8ffeb49bc3a34d98ed55aedd1fb3f134dad6e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5516425286b77b702a27aa3c49d8e76bea753d640728dc353fe7e65bcf69e987)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostdeploy")
    def put_postdeploy(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy(
            actions=actions
        )

        return typing.cast(None, jsii.invoke(self, "putPostdeploy", [value]))

    @jsii.member(jsii_name="putPredeploy")
    def put_predeploy(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy(
            actions=actions
        )

        return typing.cast(None, jsii.invoke(self, "putPredeploy", [value]))

    @jsii.member(jsii_name="resetPostdeploy")
    def reset_postdeploy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostdeploy", []))

    @jsii.member(jsii_name="resetPredeploy")
    def reset_predeploy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredeploy", []))

    @jsii.member(jsii_name="resetProfiles")
    def reset_profiles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfiles", []))

    @jsii.member(jsii_name="resetVerify")
    def reset_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerify", []))

    @builtins.property
    @jsii.member(jsii_name="postdeploy")
    def postdeploy(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference", jsii.get(self, "postdeploy"))

    @builtins.property
    @jsii.member(jsii_name="predeploy")
    def predeploy(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference", jsii.get(self, "predeploy"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="phaseIdInput")
    def phase_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="postdeployInput")
    def postdeploy_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy"], jsii.get(self, "postdeployInput"))

    @builtins.property
    @jsii.member(jsii_name="predeployInput")
    def predeploy_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy"], jsii.get(self, "predeployInput"))

    @builtins.property
    @jsii.member(jsii_name="profilesInput")
    def profiles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "profilesInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyInput")
    def verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyInput"))

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f3eb5654a753b7ba98939cebdd2809eed2747684187d7e4f9ab0940484fafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phaseId")
    def phase_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phaseId"))

    @phase_id.setter
    def phase_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99b694074bcae7d944dc3de2343087844b86d437343650503f0b3d86c7366d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profiles")
    def profiles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "profiles"))

    @profiles.setter
    def profiles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f2030f00eafb06cdbb35595a7ada398ca02967a9ced095bca90d448edc0b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verify")
    def verify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verify"))

    @verify.setter
    def verify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f776b632132ba7d424b29720ed54a9fdcbf8658fd4d86302951523d6aea6da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c055b79b885b89b6dfe82a4a958da647c07038a0164185acb200c66c9c398be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711789ad7cb018e39f8573e6d636f5165e2fd52cf296c7a4d4b605b2c6a28c9c)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__296f9202fadc6dc4b224d412f65455ff04b1b7d19a34d4ceb07bc62c5577ca8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0276f4a901e575c3ec8decf8c633f6e7a91dce7e2817efe68dda8a703fedb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b16561efb98255638d6d71043560d2fa559df4bd34ed2a46556ef550c4b5d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa326081b710683ceef44727dcb3454ed98a7027e4dc98bec6f4307c2436c4f)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbbee0052fe12fc936427ac1cba655575c190d83c33ab67206a3e656975d8e8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2b4dfb09cee5000d741e11808e6882b273c7bff6c37669b4ef9dab0fa7cc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24215d3a57c4a3e05a7db3fb7df983461eff27cf689604db00702a4559c93f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__304cba84c9f05b50f5f12f3ded7d69e34530167037a59e805016bc5f9612bf0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCanaryDeployment")
    def put_canary_deployment(
        self,
        *,
        percentages: typing.Sequence[jsii.Number],
        postdeploy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy, typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy, typing.Dict[builtins.str, typing.Any]]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param percentages: Required. The percentage based deployments that will occur as a part of a ``Rollout``. List is expected in ascending order and each integer n is 0 <= n < 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#percentages GoogleClouddeployDeliveryPipeline#percentages}
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#postdeploy GoogleClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#predeploy GoogleClouddeployDeliveryPipeline#predeploy}
        :param verify: Whether to run verify tests after each percentage deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#verify GoogleClouddeployDeliveryPipeline#verify}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment(
            percentages=percentages,
            postdeploy=postdeploy,
            predeploy=predeploy,
            verify=verify,
        )

        return typing.cast(None, jsii.invoke(self, "putCanaryDeployment", [value]))

    @jsii.member(jsii_name="putCustomCanaryDeployment")
    def put_custom_canary_deployment(
        self,
        *,
        phase_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param phase_configs: phase_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#phase_configs GoogleClouddeployDeliveryPipeline#phase_configs}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment(
            phase_configs=phase_configs
        )

        return typing.cast(None, jsii.invoke(self, "putCustomCanaryDeployment", [value]))

    @jsii.member(jsii_name="putRuntimeConfig")
    def put_runtime_config(
        self,
        *,
        cloud_run: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_run: cloud_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#cloud_run GoogleClouddeployDeliveryPipeline#cloud_run}
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#kubernetes GoogleClouddeployDeliveryPipeline#kubernetes}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig(
            cloud_run=cloud_run, kubernetes=kubernetes
        )

        return typing.cast(None, jsii.invoke(self, "putRuntimeConfig", [value]))

    @jsii.member(jsii_name="resetCanaryDeployment")
    def reset_canary_deployment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanaryDeployment", []))

    @jsii.member(jsii_name="resetCustomCanaryDeployment")
    def reset_custom_canary_deployment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCanaryDeployment", []))

    @jsii.member(jsii_name="resetRuntimeConfig")
    def reset_runtime_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeConfig", []))

    @builtins.property
    @jsii.member(jsii_name="canaryDeployment")
    def canary_deployment(
        self,
    ) -> GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference:
        return typing.cast(GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference, jsii.get(self, "canaryDeployment"))

    @builtins.property
    @jsii.member(jsii_name="customCanaryDeployment")
    def custom_canary_deployment(
        self,
    ) -> GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference:
        return typing.cast(GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference, jsii.get(self, "customCanaryDeployment"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfig")
    def runtime_config(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference", jsii.get(self, "runtimeConfig"))

    @builtins.property
    @jsii.member(jsii_name="canaryDeploymentInput")
    def canary_deployment_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment], jsii.get(self, "canaryDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="customCanaryDeploymentInput")
    def custom_canary_deployment_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment], jsii.get(self, "customCanaryDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigInput")
    def runtime_config_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig"], jsii.get(self, "runtimeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c433bbaedbae0246708fc44089da44dafff3081eef4b9874bd76f89ed3ac3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig",
    jsii_struct_bases=[],
    name_mapping={"cloud_run": "cloudRun", "kubernetes": "kubernetes"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig:
    def __init__(
        self,
        *,
        cloud_run: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_run: cloud_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#cloud_run GoogleClouddeployDeliveryPipeline#cloud_run}
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#kubernetes GoogleClouddeployDeliveryPipeline#kubernetes}
        '''
        if isinstance(cloud_run, dict):
            cloud_run = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun(**cloud_run)
        if isinstance(kubernetes, dict):
            kubernetes = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes(**kubernetes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93dca6331599f4ab31081deb6100f8454e01c649d7c7151d0fa2c00f6ad3efa)
            check_type(argname="argument cloud_run", value=cloud_run, expected_type=type_hints["cloud_run"])
            check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_run is not None:
            self._values["cloud_run"] = cloud_run
        if kubernetes is not None:
            self._values["kubernetes"] = kubernetes

    @builtins.property
    def cloud_run(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun"]:
        '''cloud_run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#cloud_run GoogleClouddeployDeliveryPipeline#cloud_run}
        '''
        result = self._values.get("cloud_run")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun"], result)

    @builtins.property
    def kubernetes(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes"]:
        '''kubernetes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#kubernetes GoogleClouddeployDeliveryPipeline#kubernetes}
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun",
    jsii_struct_bases=[],
    name_mapping={
        "automatic_traffic_control": "automaticTrafficControl",
        "canary_revision_tags": "canaryRevisionTags",
        "prior_revision_tags": "priorRevisionTags",
        "stable_revision_tags": "stableRevisionTags",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun:
    def __init__(
        self,
        *,
        automatic_traffic_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        canary_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        prior_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        stable_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param automatic_traffic_control: Whether Cloud Deploy should update the traffic stanza in a Cloud Run Service on the user's behalf to facilitate traffic splitting. This is required to be true for CanaryDeployments, but optional for CustomCanaryDeployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#automatic_traffic_control GoogleClouddeployDeliveryPipeline#automatic_traffic_control}
        :param canary_revision_tags: Optional. A list of tags that are added to the canary revision while the canary phase is in progress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary_revision_tags GoogleClouddeployDeliveryPipeline#canary_revision_tags}
        :param prior_revision_tags: Optional. A list of tags that are added to the prior revision while the canary phase is in progress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#prior_revision_tags GoogleClouddeployDeliveryPipeline#prior_revision_tags}
        :param stable_revision_tags: Optional. A list of tags that are added to the final stable revision when the stable phase is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stable_revision_tags GoogleClouddeployDeliveryPipeline#stable_revision_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc3b374220af533827c40d91abeb699e6a7a09f6981d46989cf65a799a131a9)
            check_type(argname="argument automatic_traffic_control", value=automatic_traffic_control, expected_type=type_hints["automatic_traffic_control"])
            check_type(argname="argument canary_revision_tags", value=canary_revision_tags, expected_type=type_hints["canary_revision_tags"])
            check_type(argname="argument prior_revision_tags", value=prior_revision_tags, expected_type=type_hints["prior_revision_tags"])
            check_type(argname="argument stable_revision_tags", value=stable_revision_tags, expected_type=type_hints["stable_revision_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic_traffic_control is not None:
            self._values["automatic_traffic_control"] = automatic_traffic_control
        if canary_revision_tags is not None:
            self._values["canary_revision_tags"] = canary_revision_tags
        if prior_revision_tags is not None:
            self._values["prior_revision_tags"] = prior_revision_tags
        if stable_revision_tags is not None:
            self._values["stable_revision_tags"] = stable_revision_tags

    @builtins.property
    def automatic_traffic_control(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Cloud Deploy should update the traffic stanza in a Cloud Run Service on the user's behalf to facilitate traffic splitting.

        This is required to be true for CanaryDeployments, but optional for CustomCanaryDeployments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#automatic_traffic_control GoogleClouddeployDeliveryPipeline#automatic_traffic_control}
        '''
        result = self._values.get("automatic_traffic_control")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def canary_revision_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A list of tags that are added to the canary revision while the canary phase is in progress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary_revision_tags GoogleClouddeployDeliveryPipeline#canary_revision_tags}
        '''
        result = self._values.get("canary_revision_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prior_revision_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A list of tags that are added to the prior revision while the canary phase is in progress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#prior_revision_tags GoogleClouddeployDeliveryPipeline#prior_revision_tags}
        '''
        result = self._values.get("prior_revision_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stable_revision_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A list of tags that are added to the final stable revision when the stable phase is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stable_revision_tags GoogleClouddeployDeliveryPipeline#stable_revision_tags}
        '''
        result = self._values.get("stable_revision_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73bd9c3300de8fd6d689c8a8047d45dfc0d5c219ff8b81044e43ac389b507b84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutomaticTrafficControl")
    def reset_automatic_traffic_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticTrafficControl", []))

    @jsii.member(jsii_name="resetCanaryRevisionTags")
    def reset_canary_revision_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanaryRevisionTags", []))

    @jsii.member(jsii_name="resetPriorRevisionTags")
    def reset_prior_revision_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriorRevisionTags", []))

    @jsii.member(jsii_name="resetStableRevisionTags")
    def reset_stable_revision_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStableRevisionTags", []))

    @builtins.property
    @jsii.member(jsii_name="automaticTrafficControlInput")
    def automatic_traffic_control_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automaticTrafficControlInput"))

    @builtins.property
    @jsii.member(jsii_name="canaryRevisionTagsInput")
    def canary_revision_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "canaryRevisionTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="priorRevisionTagsInput")
    def prior_revision_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "priorRevisionTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="stableRevisionTagsInput")
    def stable_revision_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stableRevisionTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticTrafficControl")
    def automatic_traffic_control(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automaticTrafficControl"))

    @automatic_traffic_control.setter
    def automatic_traffic_control(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e013497f8da57456528ac0bc5e81ff232b86dcccdeb115a2e50e0c1bccf137e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticTrafficControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="canaryRevisionTags")
    def canary_revision_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "canaryRevisionTags"))

    @canary_revision_tags.setter
    def canary_revision_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5c36a0491cd83f9576203681b57d611b5a8cd0701e98a72bd58f4f87651e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canaryRevisionTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priorRevisionTags")
    def prior_revision_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "priorRevisionTags"))

    @prior_revision_tags.setter
    def prior_revision_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae4aaba30803294b2709cafcaca2a753fdec777c89d828bbe603e375d76f3cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priorRevisionTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stableRevisionTags")
    def stable_revision_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stableRevisionTags"))

    @stable_revision_tags.setter
    def stable_revision_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a68502c12d9a8f0cbe0ac6106fa3d834c3bd1dad43e299e252b5a2aad9e8ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stableRevisionTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274b1c9e7f28f4ec19fcaf51f207dc7077df9da11098928393b3bb4ebaf54678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_service_mesh": "gatewayServiceMesh",
        "service_networking": "serviceNetworking",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes:
    def __init__(
        self,
        *,
        gateway_service_mesh: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        service_networking: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gateway_service_mesh: gateway_service_mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#gateway_service_mesh GoogleClouddeployDeliveryPipeline#gateway_service_mesh}
        :param service_networking: service_networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service_networking GoogleClouddeployDeliveryPipeline#service_networking}
        '''
        if isinstance(gateway_service_mesh, dict):
            gateway_service_mesh = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh(**gateway_service_mesh)
        if isinstance(service_networking, dict):
            service_networking = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking(**service_networking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e7c6fd38ce1a6953cfa205398857542f62cd218fbe0e4ffbf7fc97b7554058)
            check_type(argname="argument gateway_service_mesh", value=gateway_service_mesh, expected_type=type_hints["gateway_service_mesh"])
            check_type(argname="argument service_networking", value=service_networking, expected_type=type_hints["service_networking"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway_service_mesh is not None:
            self._values["gateway_service_mesh"] = gateway_service_mesh
        if service_networking is not None:
            self._values["service_networking"] = service_networking

    @builtins.property
    def gateway_service_mesh(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh"]:
        '''gateway_service_mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#gateway_service_mesh GoogleClouddeployDeliveryPipeline#gateway_service_mesh}
        '''
        result = self._values.get("gateway_service_mesh")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh"], result)

    @builtins.property
    def service_networking(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking"]:
        '''service_networking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service_networking GoogleClouddeployDeliveryPipeline#service_networking}
        '''
        result = self._values.get("service_networking")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh",
    jsii_struct_bases=[],
    name_mapping={
        "deployment": "deployment",
        "http_route": "httpRoute",
        "service": "service",
        "pod_selector_label": "podSelectorLabel",
        "route_destinations": "routeDestinations",
        "route_update_wait_time": "routeUpdateWaitTime",
        "stable_cutback_duration": "stableCutbackDuration",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh:
    def __init__(
        self,
        *,
        deployment: builtins.str,
        http_route: builtins.str,
        service: builtins.str,
        pod_selector_label: typing.Optional[builtins.str] = None,
        route_destinations: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations", typing.Dict[builtins.str, typing.Any]]] = None,
        route_update_wait_time: typing.Optional[builtins.str] = None,
        stable_cutback_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment: Required. Name of the Kubernetes Deployment whose traffic is managed by the specified HTTPRoute and Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#deployment GoogleClouddeployDeliveryPipeline#deployment}
        :param http_route: Required. Name of the Gateway API HTTPRoute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#http_route GoogleClouddeployDeliveryPipeline#http_route}
        :param service: Required. Name of the Kubernetes Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service GoogleClouddeployDeliveryPipeline#service}
        :param pod_selector_label: Optional. The label to use when selecting Pods for the Deployment and Service resources. This label must already be present in both resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#pod_selector_label GoogleClouddeployDeliveryPipeline#pod_selector_label}
        :param route_destinations: route_destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#route_destinations GoogleClouddeployDeliveryPipeline#route_destinations}
        :param route_update_wait_time: Optional. The time to wait for route updates to propagate. The maximum configurable time is 3 hours, in seconds format. If unspecified, there is no wait time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#route_update_wait_time GoogleClouddeployDeliveryPipeline#route_update_wait_time}
        :param stable_cutback_duration: Optional. The amount of time to migrate traffic back from the canary Service to the original Service during the stable phase deployment. If specified, must be between 15s and 3600s. If unspecified, there is no cutback time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stable_cutback_duration GoogleClouddeployDeliveryPipeline#stable_cutback_duration}
        '''
        if isinstance(route_destinations, dict):
            route_destinations = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations(**route_destinations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73c52718762db7849906eb3afa75b31b7c389056c49c38c9ea7364e2be0cd17)
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument http_route", value=http_route, expected_type=type_hints["http_route"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument pod_selector_label", value=pod_selector_label, expected_type=type_hints["pod_selector_label"])
            check_type(argname="argument route_destinations", value=route_destinations, expected_type=type_hints["route_destinations"])
            check_type(argname="argument route_update_wait_time", value=route_update_wait_time, expected_type=type_hints["route_update_wait_time"])
            check_type(argname="argument stable_cutback_duration", value=stable_cutback_duration, expected_type=type_hints["stable_cutback_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployment": deployment,
            "http_route": http_route,
            "service": service,
        }
        if pod_selector_label is not None:
            self._values["pod_selector_label"] = pod_selector_label
        if route_destinations is not None:
            self._values["route_destinations"] = route_destinations
        if route_update_wait_time is not None:
            self._values["route_update_wait_time"] = route_update_wait_time
        if stable_cutback_duration is not None:
            self._values["stable_cutback_duration"] = stable_cutback_duration

    @builtins.property
    def deployment(self) -> builtins.str:
        '''Required. Name of the Kubernetes Deployment whose traffic is managed by the specified HTTPRoute and Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#deployment GoogleClouddeployDeliveryPipeline#deployment}
        '''
        result = self._values.get("deployment")
        assert result is not None, "Required property 'deployment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_route(self) -> builtins.str:
        '''Required. Name of the Gateway API HTTPRoute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#http_route GoogleClouddeployDeliveryPipeline#http_route}
        '''
        result = self._values.get("http_route")
        assert result is not None, "Required property 'http_route' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. Name of the Kubernetes Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service GoogleClouddeployDeliveryPipeline#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pod_selector_label(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The label to use when selecting Pods for the Deployment and Service resources. This label must already be present in both resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#pod_selector_label GoogleClouddeployDeliveryPipeline#pod_selector_label}
        '''
        result = self._values.get("pod_selector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_destinations(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations"]:
        '''route_destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#route_destinations GoogleClouddeployDeliveryPipeline#route_destinations}
        '''
        result = self._values.get("route_destinations")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations"], result)

    @builtins.property
    def route_update_wait_time(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The time to wait for route updates to propagate. The maximum configurable time is 3 hours, in seconds format. If unspecified, there is no wait time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#route_update_wait_time GoogleClouddeployDeliveryPipeline#route_update_wait_time}
        '''
        result = self._values.get("route_update_wait_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stable_cutback_duration(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The amount of time to migrate traffic back from the canary Service to the original Service during the stable phase deployment. If specified, must be between 15s and 3600s. If unspecified, there is no cutback time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stable_cutback_duration GoogleClouddeployDeliveryPipeline#stable_cutback_duration}
        '''
        result = self._values.get("stable_cutback_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17412bc2592cc51d96b3734f69c69cdd8ec07373dc972d888d54df5b065b1e9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRouteDestinations")
    def put_route_destinations(
        self,
        *,
        destination_ids: typing.Sequence[builtins.str],
        propagate_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_ids: Required. The clusters where the Gateway API HTTPRoute resource will be deployed to. Valid entries include the associated entities IDs configured in the Target resource and "@self" to include the Target cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#destination_ids GoogleClouddeployDeliveryPipeline#destination_ids}
        :param propagate_service: Optional. Whether to propagate the Kubernetes Service to the route destination clusters. The Service will always be deployed to the Target cluster even if the HTTPRoute is not. This option may be used to facilitiate successful DNS lookup in the route destination clusters. Can only be set to true if destinations are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#propagate_service GoogleClouddeployDeliveryPipeline#propagate_service}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations(
            destination_ids=destination_ids, propagate_service=propagate_service
        )

        return typing.cast(None, jsii.invoke(self, "putRouteDestinations", [value]))

    @jsii.member(jsii_name="resetPodSelectorLabel")
    def reset_pod_selector_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodSelectorLabel", []))

    @jsii.member(jsii_name="resetRouteDestinations")
    def reset_route_destinations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteDestinations", []))

    @jsii.member(jsii_name="resetRouteUpdateWaitTime")
    def reset_route_update_wait_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteUpdateWaitTime", []))

    @jsii.member(jsii_name="resetStableCutbackDuration")
    def reset_stable_cutback_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStableCutbackDuration", []))

    @builtins.property
    @jsii.member(jsii_name="routeDestinations")
    def route_destinations(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference", jsii.get(self, "routeDestinations"))

    @builtins.property
    @jsii.member(jsii_name="deploymentInput")
    def deployment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRouteInput")
    def http_route_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="podSelectorLabelInput")
    def pod_selector_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podSelectorLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="routeDestinationsInput")
    def route_destinations_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations"], jsii.get(self, "routeDestinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="routeUpdateWaitTimeInput")
    def route_update_wait_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeUpdateWaitTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="stableCutbackDurationInput")
    def stable_cutback_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stableCutbackDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployment"))

    @deployment.setter
    def deployment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da7544bb124c68ede17b48c17e58173e164734018553c1064284da4724292dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpRoute")
    def http_route(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpRoute"))

    @http_route.setter
    def http_route(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a149684f6be6d6bf943b017f323a47368cd822b2b0e7a2b52180c9d9deabd3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpRoute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podSelectorLabel")
    def pod_selector_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podSelectorLabel"))

    @pod_selector_label.setter
    def pod_selector_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8d02d7dc63c15a77cd60847e71893d0ba2e758f5e604e616c0cf68f9a3ca990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podSelectorLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeUpdateWaitTime")
    def route_update_wait_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeUpdateWaitTime"))

    @route_update_wait_time.setter
    def route_update_wait_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cf5f8c60cf6bce93c8c8fdab42a2a817c4d55313f82d7e271b819c1a18d369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeUpdateWaitTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d56049875ca24be8d3debef419b8924a793a2f7329b16dabd287e42722290de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stableCutbackDuration")
    def stable_cutback_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stableCutbackDuration"))

    @stable_cutback_duration.setter
    def stable_cutback_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9c6556c1dd78657c458624282c740c0c21c87c37121d0ac82b9affa6a3dd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stableCutbackDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8d74e5282f773107e263ce6ca532861398e99092c267880596f395900b65fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations",
    jsii_struct_bases=[],
    name_mapping={
        "destination_ids": "destinationIds",
        "propagate_service": "propagateService",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations:
    def __init__(
        self,
        *,
        destination_ids: typing.Sequence[builtins.str],
        propagate_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_ids: Required. The clusters where the Gateway API HTTPRoute resource will be deployed to. Valid entries include the associated entities IDs configured in the Target resource and "@self" to include the Target cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#destination_ids GoogleClouddeployDeliveryPipeline#destination_ids}
        :param propagate_service: Optional. Whether to propagate the Kubernetes Service to the route destination clusters. The Service will always be deployed to the Target cluster even if the HTTPRoute is not. This option may be used to facilitiate successful DNS lookup in the route destination clusters. Can only be set to true if destinations are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#propagate_service GoogleClouddeployDeliveryPipeline#propagate_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3082bc9bc0cbf05de15d13bdfd5b8850394a79c2c053f6dd8bdeb578b341e8ba)
            check_type(argname="argument destination_ids", value=destination_ids, expected_type=type_hints["destination_ids"])
            check_type(argname="argument propagate_service", value=propagate_service, expected_type=type_hints["propagate_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_ids": destination_ids,
        }
        if propagate_service is not None:
            self._values["propagate_service"] = propagate_service

    @builtins.property
    def destination_ids(self) -> typing.List[builtins.str]:
        '''Required.

        The clusters where the Gateway API HTTPRoute resource will be deployed to. Valid entries include the associated entities IDs configured in the Target resource and "@self" to include the Target cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#destination_ids GoogleClouddeployDeliveryPipeline#destination_ids}
        '''
        result = self._values.get("destination_ids")
        assert result is not None, "Required property 'destination_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def propagate_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether to propagate the Kubernetes Service to the route destination clusters. The Service will always be deployed to the Target cluster even if the HTTPRoute is not. This option may be used to facilitiate successful DNS lookup in the route destination clusters. Can only be set to true if destinations are specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#propagate_service GoogleClouddeployDeliveryPipeline#propagate_service}
        '''
        result = self._values.get("propagate_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6beff47db237b4a2a5e21643e50cbf7ee6c0e7350ceaf669332d43f010e6df4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPropagateService")
    def reset_propagate_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagateService", []))

    @builtins.property
    @jsii.member(jsii_name="destinationIdsInput")
    def destination_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="propagateServiceInput")
    def propagate_service_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "propagateServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationIds")
    def destination_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationIds"))

    @destination_ids.setter
    def destination_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f3a5297bcd6a53de45291c2574e7d9752a697d75f6d2fe3137fc7f6e207254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="propagateService")
    def propagate_service(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "propagateService"))

    @propagate_service.setter
    def propagate_service(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c2f1e98b18c34dca3032abb251b73a6191d4ef208e487c5f0b0c965a4eae23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagateService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9ff3062d91c8e0d462749ae416b436d89eb989e83dac979ce275c1d412f31d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__629f24bbfda2f5861fbff8b06d6214c23ef1670a9c039c15817819bdde91a8ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGatewayServiceMesh")
    def put_gateway_service_mesh(
        self,
        *,
        deployment: builtins.str,
        http_route: builtins.str,
        service: builtins.str,
        pod_selector_label: typing.Optional[builtins.str] = None,
        route_destinations: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations, typing.Dict[builtins.str, typing.Any]]] = None,
        route_update_wait_time: typing.Optional[builtins.str] = None,
        stable_cutback_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment: Required. Name of the Kubernetes Deployment whose traffic is managed by the specified HTTPRoute and Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#deployment GoogleClouddeployDeliveryPipeline#deployment}
        :param http_route: Required. Name of the Gateway API HTTPRoute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#http_route GoogleClouddeployDeliveryPipeline#http_route}
        :param service: Required. Name of the Kubernetes Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service GoogleClouddeployDeliveryPipeline#service}
        :param pod_selector_label: Optional. The label to use when selecting Pods for the Deployment and Service resources. This label must already be present in both resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#pod_selector_label GoogleClouddeployDeliveryPipeline#pod_selector_label}
        :param route_destinations: route_destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#route_destinations GoogleClouddeployDeliveryPipeline#route_destinations}
        :param route_update_wait_time: Optional. The time to wait for route updates to propagate. The maximum configurable time is 3 hours, in seconds format. If unspecified, there is no wait time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#route_update_wait_time GoogleClouddeployDeliveryPipeline#route_update_wait_time}
        :param stable_cutback_duration: Optional. The amount of time to migrate traffic back from the canary Service to the original Service during the stable phase deployment. If specified, must be between 15s and 3600s. If unspecified, there is no cutback time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stable_cutback_duration GoogleClouddeployDeliveryPipeline#stable_cutback_duration}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh(
            deployment=deployment,
            http_route=http_route,
            service=service,
            pod_selector_label=pod_selector_label,
            route_destinations=route_destinations,
            route_update_wait_time=route_update_wait_time,
            stable_cutback_duration=stable_cutback_duration,
        )

        return typing.cast(None, jsii.invoke(self, "putGatewayServiceMesh", [value]))

    @jsii.member(jsii_name="putServiceNetworking")
    def put_service_networking(
        self,
        *,
        deployment: builtins.str,
        service: builtins.str,
        disable_pod_overprovisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pod_selector_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment: Required. Name of the Kubernetes Deployment whose traffic is managed by the specified Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#deployment GoogleClouddeployDeliveryPipeline#deployment}
        :param service: Required. Name of the Kubernetes Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service GoogleClouddeployDeliveryPipeline#service}
        :param disable_pod_overprovisioning: Optional. Whether to disable Pod overprovisioning. If Pod overprovisioning is disabled then Cloud Deploy will limit the number of total Pods used for the deployment strategy to the number of Pods the Deployment has on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#disable_pod_overprovisioning GoogleClouddeployDeliveryPipeline#disable_pod_overprovisioning}
        :param pod_selector_label: Optional. The label to use when selecting Pods for the Deployment resource. This label must already be present in the Deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#pod_selector_label GoogleClouddeployDeliveryPipeline#pod_selector_label}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking(
            deployment=deployment,
            service=service,
            disable_pod_overprovisioning=disable_pod_overprovisioning,
            pod_selector_label=pod_selector_label,
        )

        return typing.cast(None, jsii.invoke(self, "putServiceNetworking", [value]))

    @jsii.member(jsii_name="resetGatewayServiceMesh")
    def reset_gateway_service_mesh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayServiceMesh", []))

    @jsii.member(jsii_name="resetServiceNetworking")
    def reset_service_networking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNetworking", []))

    @builtins.property
    @jsii.member(jsii_name="gatewayServiceMesh")
    def gateway_service_mesh(
        self,
    ) -> GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference:
        return typing.cast(GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference, jsii.get(self, "gatewayServiceMesh"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworking")
    def service_networking(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference", jsii.get(self, "serviceNetworking"))

    @builtins.property
    @jsii.member(jsii_name="gatewayServiceMeshInput")
    def gateway_service_mesh_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh], jsii.get(self, "gatewayServiceMeshInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkingInput")
    def service_networking_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking"], jsii.get(self, "serviceNetworkingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7695250a8c427fee82a224d02b03045287086fb7f9eea20c18d5f5684aaa99d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking",
    jsii_struct_bases=[],
    name_mapping={
        "deployment": "deployment",
        "service": "service",
        "disable_pod_overprovisioning": "disablePodOverprovisioning",
        "pod_selector_label": "podSelectorLabel",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking:
    def __init__(
        self,
        *,
        deployment: builtins.str,
        service: builtins.str,
        disable_pod_overprovisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pod_selector_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment: Required. Name of the Kubernetes Deployment whose traffic is managed by the specified Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#deployment GoogleClouddeployDeliveryPipeline#deployment}
        :param service: Required. Name of the Kubernetes Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service GoogleClouddeployDeliveryPipeline#service}
        :param disable_pod_overprovisioning: Optional. Whether to disable Pod overprovisioning. If Pod overprovisioning is disabled then Cloud Deploy will limit the number of total Pods used for the deployment strategy to the number of Pods the Deployment has on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#disable_pod_overprovisioning GoogleClouddeployDeliveryPipeline#disable_pod_overprovisioning}
        :param pod_selector_label: Optional. The label to use when selecting Pods for the Deployment resource. This label must already be present in the Deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#pod_selector_label GoogleClouddeployDeliveryPipeline#pod_selector_label}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c7e829d3da0cf9e42507d8b271deca8875b17b65d043b7e67232c47f2694a4)
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument disable_pod_overprovisioning", value=disable_pod_overprovisioning, expected_type=type_hints["disable_pod_overprovisioning"])
            check_type(argname="argument pod_selector_label", value=pod_selector_label, expected_type=type_hints["pod_selector_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployment": deployment,
            "service": service,
        }
        if disable_pod_overprovisioning is not None:
            self._values["disable_pod_overprovisioning"] = disable_pod_overprovisioning
        if pod_selector_label is not None:
            self._values["pod_selector_label"] = pod_selector_label

    @builtins.property
    def deployment(self) -> builtins.str:
        '''Required. Name of the Kubernetes Deployment whose traffic is managed by the specified Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#deployment GoogleClouddeployDeliveryPipeline#deployment}
        '''
        result = self._values.get("deployment")
        assert result is not None, "Required property 'deployment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. Name of the Kubernetes Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service GoogleClouddeployDeliveryPipeline#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disable_pod_overprovisioning(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether to disable Pod overprovisioning. If Pod overprovisioning is disabled then Cloud Deploy will limit the number of total Pods used for the deployment strategy to the number of Pods the Deployment has on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#disable_pod_overprovisioning GoogleClouddeployDeliveryPipeline#disable_pod_overprovisioning}
        '''
        result = self._values.get("disable_pod_overprovisioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pod_selector_label(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The label to use when selecting Pods for the Deployment resource. This label must already be present in the Deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#pod_selector_label GoogleClouddeployDeliveryPipeline#pod_selector_label}
        '''
        result = self._values.get("pod_selector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__362179957a61382d325bc893ef7acaa6150417dd5dd75453c9832579f1f1102a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisablePodOverprovisioning")
    def reset_disable_pod_overprovisioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisablePodOverprovisioning", []))

    @jsii.member(jsii_name="resetPodSelectorLabel")
    def reset_pod_selector_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodSelectorLabel", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentInput")
    def deployment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePodOverprovisioningInput")
    def disable_pod_overprovisioning_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disablePodOverprovisioningInput"))

    @builtins.property
    @jsii.member(jsii_name="podSelectorLabelInput")
    def pod_selector_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podSelectorLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployment"))

    @deployment.setter
    def deployment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f1e1096ae82c6841d7fc475c5e92cc29605d3854ca30e66078bc84f1e60e658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disablePodOverprovisioning")
    def disable_pod_overprovisioning(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disablePodOverprovisioning"))

    @disable_pod_overprovisioning.setter
    def disable_pod_overprovisioning(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c54433174be89448c372564bf3adf267626d37bca73706278c3c3cef7b4909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePodOverprovisioning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podSelectorLabel")
    def pod_selector_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podSelectorLabel"))

    @pod_selector_label.setter
    def pod_selector_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896ab4f3b9a96639c423b6c8f7931198b8378fac53da010605267fb50e3becce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podSelectorLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e07d85ca6a17e64678e49d41c6e262ee55b3450f4b882508185daad7886d2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077a538c0721acd7d464e48e44a2a164488504d8cc52ee7c105e5bbca0b7c587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__657440fe5d61decc3a160a48ca2283d4dec388991d7be8f898de804e1a48788c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudRun")
    def put_cloud_run(
        self,
        *,
        automatic_traffic_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        canary_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        prior_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        stable_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param automatic_traffic_control: Whether Cloud Deploy should update the traffic stanza in a Cloud Run Service on the user's behalf to facilitate traffic splitting. This is required to be true for CanaryDeployments, but optional for CustomCanaryDeployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#automatic_traffic_control GoogleClouddeployDeliveryPipeline#automatic_traffic_control}
        :param canary_revision_tags: Optional. A list of tags that are added to the canary revision while the canary phase is in progress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary_revision_tags GoogleClouddeployDeliveryPipeline#canary_revision_tags}
        :param prior_revision_tags: Optional. A list of tags that are added to the prior revision while the canary phase is in progress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#prior_revision_tags GoogleClouddeployDeliveryPipeline#prior_revision_tags}
        :param stable_revision_tags: Optional. A list of tags that are added to the final stable revision when the stable phase is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#stable_revision_tags GoogleClouddeployDeliveryPipeline#stable_revision_tags}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun(
            automatic_traffic_control=automatic_traffic_control,
            canary_revision_tags=canary_revision_tags,
            prior_revision_tags=prior_revision_tags,
            stable_revision_tags=stable_revision_tags,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudRun", [value]))

    @jsii.member(jsii_name="putKubernetes")
    def put_kubernetes(
        self,
        *,
        gateway_service_mesh: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh, typing.Dict[builtins.str, typing.Any]]] = None,
        service_networking: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gateway_service_mesh: gateway_service_mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#gateway_service_mesh GoogleClouddeployDeliveryPipeline#gateway_service_mesh}
        :param service_networking: service_networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#service_networking GoogleClouddeployDeliveryPipeline#service_networking}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes(
            gateway_service_mesh=gateway_service_mesh,
            service_networking=service_networking,
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetes", [value]))

    @jsii.member(jsii_name="resetCloudRun")
    def reset_cloud_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudRun", []))

    @jsii.member(jsii_name="resetKubernetes")
    def reset_kubernetes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetes", []))

    @builtins.property
    @jsii.member(jsii_name="cloudRun")
    def cloud_run(
        self,
    ) -> GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference:
        return typing.cast(GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference, jsii.get(self, "cloudRun"))

    @builtins.property
    @jsii.member(jsii_name="kubernetes")
    def kubernetes(
        self,
    ) -> GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference:
        return typing.cast(GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference, jsii.get(self, "kubernetes"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunInput")
    def cloud_run_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun], jsii.get(self, "cloudRunInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesInput")
    def kubernetes_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes], jsii.get(self, "kubernetesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42bf10375399f0f4ff37aff2ca1f49013a7d9579552dbf8b2eab3e98e0d91af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc2f2ee70505cc71f053bae8d08b0370dc10815a1a7ad113efd9576d6b78a0e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCanary")
    def put_canary(
        self,
        *,
        canary_deployment: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_canary_deployment: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_config: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param canary_deployment: canary_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#canary_deployment GoogleClouddeployDeliveryPipeline#canary_deployment}
        :param custom_canary_deployment: custom_canary_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#custom_canary_deployment GoogleClouddeployDeliveryPipeline#custom_canary_deployment}
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#runtime_config GoogleClouddeployDeliveryPipeline#runtime_config}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary(
            canary_deployment=canary_deployment,
            custom_canary_deployment=custom_canary_deployment,
            runtime_config=runtime_config,
        )

        return typing.cast(None, jsii.invoke(self, "putCanary", [value]))

    @jsii.member(jsii_name="putStandard")
    def put_standard(
        self,
        *,
        postdeploy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#postdeploy GoogleClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#predeploy GoogleClouddeployDeliveryPipeline#predeploy}
        :param verify: Whether to verify a deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#verify GoogleClouddeployDeliveryPipeline#verify}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard(
            postdeploy=postdeploy, predeploy=predeploy, verify=verify
        )

        return typing.cast(None, jsii.invoke(self, "putStandard", [value]))

    @jsii.member(jsii_name="resetCanary")
    def reset_canary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanary", []))

    @jsii.member(jsii_name="resetStandard")
    def reset_standard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandard", []))

    @builtins.property
    @jsii.member(jsii_name="canary")
    def canary(
        self,
    ) -> GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference:
        return typing.cast(GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference, jsii.get(self, "canary"))

    @builtins.property
    @jsii.member(jsii_name="standard")
    def standard(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference", jsii.get(self, "standard"))

    @builtins.property
    @jsii.member(jsii_name="canaryInput")
    def canary_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary], jsii.get(self, "canaryInput"))

    @builtins.property
    @jsii.member(jsii_name="standardInput")
    def standard_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard"], jsii.get(self, "standardInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5152c094e65f19545f62114144d189a6bb9d5c286deac0243aa0e033783376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard",
    jsii_struct_bases=[],
    name_mapping={
        "postdeploy": "postdeploy",
        "predeploy": "predeploy",
        "verify": "verify",
    },
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard:
    def __init__(
        self,
        *,
        postdeploy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#postdeploy GoogleClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#predeploy GoogleClouddeployDeliveryPipeline#predeploy}
        :param verify: Whether to verify a deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#verify GoogleClouddeployDeliveryPipeline#verify}
        '''
        if isinstance(postdeploy, dict):
            postdeploy = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy(**postdeploy)
        if isinstance(predeploy, dict):
            predeploy = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy(**predeploy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c28849902c44a85c41e9d0a0dffffb309de959e92f0daddea501c869a9723d)
            check_type(argname="argument postdeploy", value=postdeploy, expected_type=type_hints["postdeploy"])
            check_type(argname="argument predeploy", value=predeploy, expected_type=type_hints["predeploy"])
            check_type(argname="argument verify", value=verify, expected_type=type_hints["verify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if postdeploy is not None:
            self._values["postdeploy"] = postdeploy
        if predeploy is not None:
            self._values["predeploy"] = predeploy
        if verify is not None:
            self._values["verify"] = verify

    @builtins.property
    def postdeploy(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy"]:
        '''postdeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#postdeploy GoogleClouddeployDeliveryPipeline#postdeploy}
        '''
        result = self._values.get("postdeploy")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy"], result)

    @builtins.property
    def predeploy(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy"]:
        '''predeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#predeploy GoogleClouddeployDeliveryPipeline#predeploy}
        '''
        result = self._values.get("predeploy")
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy"], result)

    @builtins.property
    def verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to verify a deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#verify GoogleClouddeployDeliveryPipeline#verify}
        '''
        result = self._values.get("verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__385bee20f5c709d7f071e9c418b9bda79a4f44d76438b13a167a12034d51266a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostdeploy")
    def put_postdeploy(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy(
            actions=actions
        )

        return typing.cast(None, jsii.invoke(self, "putPostdeploy", [value]))

    @jsii.member(jsii_name="putPredeploy")
    def put_predeploy(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        value = GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy(
            actions=actions
        )

        return typing.cast(None, jsii.invoke(self, "putPredeploy", [value]))

    @jsii.member(jsii_name="resetPostdeploy")
    def reset_postdeploy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostdeploy", []))

    @jsii.member(jsii_name="resetPredeploy")
    def reset_predeploy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredeploy", []))

    @jsii.member(jsii_name="resetVerify")
    def reset_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerify", []))

    @builtins.property
    @jsii.member(jsii_name="postdeploy")
    def postdeploy(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference", jsii.get(self, "postdeploy"))

    @builtins.property
    @jsii.member(jsii_name="predeploy")
    def predeploy(
        self,
    ) -> "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference":
        return typing.cast("GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference", jsii.get(self, "predeploy"))

    @builtins.property
    @jsii.member(jsii_name="postdeployInput")
    def postdeploy_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy"], jsii.get(self, "postdeployInput"))

    @builtins.property
    @jsii.member(jsii_name="predeployInput")
    def predeploy_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy"], jsii.get(self, "predeployInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyInput")
    def verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyInput"))

    @builtins.property
    @jsii.member(jsii_name="verify")
    def verify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verify"))

    @verify.setter
    def verify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ad95878b09ebfe696630082a432a808c62b8b386dc67cc8d8103d914c1028d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10601cb76bbbc0d2a89fc7183676d8bcf98a57941269f8bfffbf861af890bd5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6b18ebb05a1a945c1865ab90fdaa9e69958f6194ecc674154c5ac39be8b3da)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f6b00df4c2813f815678d75d45128517abad38562c74891ff4d723f03d4e7f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3d14352b1a2351fa9af8644ae24cce02977fa806a21945299bea48ddfb3f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7e8a57053cadf584fa483e0f92cae736c6758d9f9c5b624b68ebe2d88d1045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d40840f1afe39fd5109331e48b56ba43c9c88d5e6471ae9bbf2846c7b4ecb47)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#actions GoogleClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22ea5b5d09c03da4363e00ecfae097a29b15137f3805e9f0626690b346b325a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55afb50935a47b12bd0d0ca3165d80abb388a0f2288ac7fe95d74a9820660dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy]:
        return typing.cast(typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5395a50a62202fcdaf4f7c8132cfef83ae2d0adf665af367d4e0c11e4625618e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleClouddeployDeliveryPipelineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#create GoogleClouddeployDeliveryPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#delete GoogleClouddeployDeliveryPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#update GoogleClouddeployDeliveryPipeline#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc8b9431c261ca1a72980fd6d0499a13faaf209819b1d4ef245d26e73c92b3e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#create GoogleClouddeployDeliveryPipeline#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#delete GoogleClouddeployDeliveryPipeline#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_delivery_pipeline#update GoogleClouddeployDeliveryPipeline#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeliveryPipelineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeliveryPipelineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeliveryPipeline.GoogleClouddeployDeliveryPipelineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92eadb026315908613c62570faadd3a8ab92a25b725353dc3c2155ca55f1a678)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05a15766774de0a8068dd7a4fdfa7dc8233b581ad41c88ef0f4013ae52f971f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7112fd93a3ffbb96b4171d48860660e01fbb8c154250f1e41358e9e6a36c344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17af23c29bb8aa139f85d3d686d73d1234ad9c3e594e9eee594e9a015d342170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec1d0cb77be32c032b1b2ab2cef23e7bfc9ff71f2c98691b38945aa58884202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleClouddeployDeliveryPipeline",
    "GoogleClouddeployDeliveryPipelineCondition",
    "GoogleClouddeployDeliveryPipelineConditionList",
    "GoogleClouddeployDeliveryPipelineConditionOutputReference",
    "GoogleClouddeployDeliveryPipelineConditionPipelineReadyCondition",
    "GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionList",
    "GoogleClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference",
    "GoogleClouddeployDeliveryPipelineConditionTargetsPresentCondition",
    "GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionList",
    "GoogleClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference",
    "GoogleClouddeployDeliveryPipelineConditionTargetsTypeCondition",
    "GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionList",
    "GoogleClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference",
    "GoogleClouddeployDeliveryPipelineConfig",
    "GoogleClouddeployDeliveryPipelineSerialPipeline",
    "GoogleClouddeployDeliveryPipelineSerialPipelineOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStages",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesList",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy",
    "GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference",
    "GoogleClouddeployDeliveryPipelineTimeouts",
    "GoogleClouddeployDeliveryPipelineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2b55bc45b3ebdd6f7c310f804dad347588e73194b4b19d07f1ae1076afd61bac(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    serial_pipeline: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipeline, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__486b96d403f91955495fc04e0e7c91cc3b7061ad9cf3f6a5dfd64d0efcc4e238(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304cb9088ef7d0debe18b24ad2d8f938cb7e88adc87f7db37449f6cea4659b5a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c2b3ab604c1a5d5980e61cfa0dfd3ec3c20c50752151094bea5ba55ed8dbd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b37ff579e684bc1dbed3cf5a92079c35b75677a9dd31e80dddadcbcc038023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4025c3d084f982e3945e8416239bf5cbceb5dbb9e23b7dc1a2bd9a5b5b33575(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cf533211b422a3eb5ced0b50cee50561f2829d7cc1b9bf073af03864cc146d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c0185ac1c437944470e77ab166e3965af0d4ceba7815a459170e0fa863bb2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac3ba9d34bfa4b93318d6c083f45525c7cb47c7bb18b8b67373b9c0a5cef5d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99585f358e3bc5ad6fe8da048320bc9641e2c273f954c813cfe5da6b41b626f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48ad054e924f72aa9e0ca0478fc7dff32503cc86e69491c33188906b2c738fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45a18dd94faccbc095dd7d9bc4fa5b1b65f0e03c9504427aa8cc3fa1089e48e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd81e6774268527239803443dfc3374b445cdafec82b929b94da85a73a0b0d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d5af5e5a5ce5df42693893390450cdd44610891dfc6ed0cd34829f4d937eae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f249d5af39c324741096198c9ec2a48a0c4df151c3c8761d6a56135527dd1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c92de1d7b9ef4e8b9b6e35c64fb873b2d34731f203d2d3cdca94f6dc32db7e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6553b8d42b3ed70ef38ebff84a89250b05bac7a732876295c9468ffbf2f7b01(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca8e0c667be452658dfafad17f113327c17a00fcc36fd30cf6c6dddde977133(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c649390d4443a09dbbd9907ac37db0f036697ca62651d11fbc3f50d88a2d7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9467983c402a0cbbb6128b56a5a0f034a32912644fb8632ace98d4d9feda3877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527bb4a78a6b01cc9539f17fb26271e17c3db860a44844fef2ba83124971550e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a04eec647d5f10c58d380ce70d366bc310ac1e74f17eb87119e6b3967d1ba47(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f7598cfeb5bea99a4e01763d99869272cc84cdb82170940e4587c6dd053203(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d7ac06c4d84737262bd13ef99df8d08c329ea287ee481a8c732ecef44dcae9c(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineConditionPipelineReadyCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a3e79eed1b61895228c74a9d6b46f4dc48d38d587787ad3356ffbdebb7e775(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b3c34bd43fca7ef56c0b8f2c3b64b19d59b842066f336e191578bbe3bf1cba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae229339d7198d94a486f613363b9963756b98e8b50291f951352f361bc9882(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9355fd85d1684f1c10ac9bccf464fde15712c5a250d0d3774ffe79bb7fa7f288(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e353d7c1cc474ba3ca7cf7ac1c67fadce6e0d8e6dfec9e2113300b4279877caa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3c5923e98072637668e277406dba65ba537e09a2916819172be466b4aed693(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c42c110426423ee9a1441e569aa34ede94bb0b9a219a0ad5026c022e65d994b(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineConditionTargetsPresentCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d294265df84b8116459f81e5bf7d74d82389358b914a2ffa198377a32d0b475(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bea6abd212a33f1e8772b718f29c8feb645e9aa9c6db1643cc5fae5ca652293(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4cc1c0f7054cbacbefffa71bc040c5f1d2b1d368e0468e9e608ccdbb8e69df7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195d89630e23841e0b41220bfac8dd625d97fcb369ad1071af80b2f0a7c0fdc0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794a42cbd2639f5b353c0390b1ea28c2420ff385a2f78383056397c503bd9f10(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610bd6207857e9222d88580bcb7d5549aa9d2798bd1249736a0c2cb952b6d800(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba81af60db414105b3e97aacf41fb1e12aa9d0dde0d273d71bcf7b188f8aaddd(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineConditionTargetsTypeCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa7d8c0bbde56ab348740e0ab529665a6c5a196d9e74e8ffd7eb25a13ec4eb3(
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
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    serial_pipeline: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipeline, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e3664541fccfdbf694f881712cc009c248f3139b5b4b090135829a8b6463f9(
    *,
    stages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5945a2091550c193269b98d05830bda2155d19965f369b375fdd1f3dac451b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f629910366e4f8c42c90e99e66d169d062658f65e6bd029966145dab03691c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a950130d66c5a27e52e13e02b2bd9e89a1d896d9b00d7a7f4b7e320f36774cc0(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipeline],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c77944373e30764a11ad3ec7b6d167d4385bb4293f574ed2af6cb2136a694f(
    *,
    deploy_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
    strategy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    target_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8b61115abb669289db7d072bbf7bbb07de312859171696e658464b72ceafd7(
    *,
    values: typing.Mapping[builtins.str, builtins.str],
    match_target_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf28ddfa5933cdc600909120e61282141bacdb3b69001f94f0147735305368d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9005d0485c82c1f5dc453ffc5a8c4849b85fc545dec101cb3b0b7daf3739062(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7100d4edc95e17d5c5a192043238e9dcfde7bcfc69413e7e16045ba2237745f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcf26473135d13ce75147f1743190efcea5b92f86b41f79f6592486504ea59f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f55b13361879cd3729dbe02e844b204aa84f50076f4a3a9adf4dca8bab2923e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3a7977208b25971093c7aa687689f9a1f571c009c2a950f3328990cfd5ff68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2984148ca6901306bd9ee0ec189fd1974fb15c4259bb35bd27e200063c27c9b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529213850ac322e1ad86d09883f09ce48dec2ba1e141a1ef314ce998c7e88870(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ac50e7ce63c4ccbd53ae67d14246c9d6eb5b7b98621c5acbdb5f59fe71a558(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dfe0312694666a5e71de2b200e3deb2c1df8b0956f67a0ec045f0bad495080a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6f8488b16345923805e1992a4945999100d05636a906bb654def8c92f5d6f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72422b20cf9b19db3192e7fb33d63d08fd4a5e70fdebcd347512067ae175b8b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b864ccefcc85e50d61610fce9624b91aa6d6721388a5f7d28df00f0db1d9a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0426ad94c858bce76ffbeb7d66fbec2350cca9dbf61abea37445b181131628(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436eb70260b985d86ddaa101b50d94723ce67ff82637450ceaf4bd8685908123(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a34e7e6f19a0c3afbb5c7f52368de55fb9a21008d313c0622c445686f9f4067(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9967898f60c765aafe7de483eba6bdd623080edb9e7df3f58c7e682478a1e698(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21428197ad1d9f919a05b53601001f7779cee1edfe154a3f4a79ff32512a7a36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe3aade4d5c246e52e50e1e5542156d40240f86214e0940b026fe5f126bb8e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d9a007566267755ed1aaba4fce9f6267af2ed97f09c3c8b45629432f4e515b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d9c2e22d6229b1fc1cbf219b851e319fbff83e82f532b8c4b628d668f26b02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11def406533660312fcb8c410e6f6d00fefe2c8cc0120bd848e09093731a29b8(
    *,
    canary: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary, typing.Dict[builtins.str, typing.Any]]] = None,
    standard: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352b49f14c99d5902add6cbfd3e8574f72a26d342fdf3bbd3861548c451c5701(
    *,
    canary_deployment: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_canary_deployment: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_config: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a03804f56da33e28f7bd7a93810a066d810e85dd23bd5e37aca1dfcd86217ef(
    *,
    percentages: typing.Sequence[jsii.Number],
    postdeploy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    predeploy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb6d0145df968ed99061335712183360976af549fd012bf515f19bf24908ada(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435d37ba65571cc605f457c312e58037f31674c871bed51980eea128141c8fa3(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a7054b22d42615af052d42d8f8a33bedfc31012d844cbb5fdc865691842edd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25994b6cd177deed712267c97066fded5f3c9abe2e24fa56d962be7a69d634a3(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6c272180abc3ac252df80260c188a660fe0f79817e50978701efeb266b76aa(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4298581324f73c0908dae287ef7e4589abdbca56ba14dc59197dde7b77783bae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed0df3acf294ea843ac70dde79b10ef7fb68c393d54136ec99c2bce30485841(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb78e537d07e6336f5c33ab6900f251508746c13c78de3dd4566e19441d28494(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b53b6469b8ca9194c8852a1d892bbef690899ffe98b1e2ef62a03a8e442548(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1766a5a18420aaa68d45101fc382dafc7faef9d9dc60a49fe4297a7d86df5b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a534280336beaf07bf7c895d5cc886b617cc1069e5bc13a8dd10df87e8c47b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f58b1f7f856267399c5ef97d78026119e4e735db111e06123637e6bacc96ec8(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a95eb3da3a4ee5088509e22d5473a91ddca1c77a9db26b2b9eee0233ba399b(
    *,
    phase_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f10402ed2f3a0d21e484fa96b84659b6657454d1f4886c0715f2743d6a76ff0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6105aaf9e6226a2ed0db50703f51e9a347d1ece6f15887c7a0b2030972004cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2be5d623768e2f59a6aaacab401b3e671fcc00ce6fff7faf576ca4287e2a3c(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ce62687fe3c5867c21c5f0a7dd362fb27be9ffa85e893c1b42b1ba0d711c86(
    *,
    percentage: jsii.Number,
    phase_id: builtins.str,
    postdeploy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    predeploy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92155f627463f6b3dd490fd900c017f869e5d8656ecb0d6605c661f66c443607(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176b59bcbf8684f7bf0a06926ff1d85927e37e32f019d38fbecfc9bcef6403f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab086b70b51ec58057bcaf523cade9f0f3bcb285b30f6bdf877ab155510e8e6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d64f071c360ba3f854c5faf680f568c8e45b8a4a12163248c7ca36afda022e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ead080f7c71cb4f6bb9f62d4b167f051a59790303aa61975146ec09b364b64(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af2a8170f6e69b228f0f76daa8ffeb49bc3a34d98ed55aedd1fb3f134dad6e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5516425286b77b702a27aa3c49d8e76bea753d640728dc353fe7e65bcf69e987(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f3eb5654a753b7ba98939cebdd2809eed2747684187d7e4f9ab0940484fafd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99b694074bcae7d944dc3de2343087844b86d437343650503f0b3d86c7366d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f2030f00eafb06cdbb35595a7ada398ca02967a9ced095bca90d448edc0b21(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f776b632132ba7d424b29720ed54a9fdcbf8658fd4d86302951523d6aea6da5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c055b79b885b89b6dfe82a4a958da647c07038a0164185acb200c66c9c398be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711789ad7cb018e39f8573e6d636f5165e2fd52cf296c7a4d4b605b2c6a28c9c(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296f9202fadc6dc4b224d412f65455ff04b1b7d19a34d4ceb07bc62c5577ca8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0276f4a901e575c3ec8decf8c633f6e7a91dce7e2817efe68dda8a703fedb5e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b16561efb98255638d6d71043560d2fa559df4bd34ed2a46556ef550c4b5d5(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa326081b710683ceef44727dcb3454ed98a7027e4dc98bec6f4307c2436c4f(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbee0052fe12fc936427ac1cba655575c190d83c33ab67206a3e656975d8e8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2b4dfb09cee5000d741e11808e6882b273c7bff6c37669b4ef9dab0fa7cc12(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24215d3a57c4a3e05a7db3fb7df983461eff27cf689604db00702a4559c93f3(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304cba84c9f05b50f5f12f3ded7d69e34530167037a59e805016bc5f9612bf0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c433bbaedbae0246708fc44089da44dafff3081eef4b9874bd76f89ed3ac3a(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93dca6331599f4ab31081deb6100f8454e01c649d7c7151d0fa2c00f6ad3efa(
    *,
    cloud_run: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc3b374220af533827c40d91abeb699e6a7a09f6981d46989cf65a799a131a9(
    *,
    automatic_traffic_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    canary_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    prior_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    stable_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bd9c3300de8fd6d689c8a8047d45dfc0d5c219ff8b81044e43ac389b507b84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e013497f8da57456528ac0bc5e81ff232b86dcccdeb115a2e50e0c1bccf137e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5c36a0491cd83f9576203681b57d611b5a8cd0701e98a72bd58f4f87651e7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae4aaba30803294b2709cafcaca2a753fdec777c89d828bbe603e375d76f3cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a68502c12d9a8f0cbe0ac6106fa3d834c3bd1dad43e299e252b5a2aad9e8ac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274b1c9e7f28f4ec19fcaf51f207dc7077df9da11098928393b3bb4ebaf54678(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e7c6fd38ce1a6953cfa205398857542f62cd218fbe0e4ffbf7fc97b7554058(
    *,
    gateway_service_mesh: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    service_networking: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73c52718762db7849906eb3afa75b31b7c389056c49c38c9ea7364e2be0cd17(
    *,
    deployment: builtins.str,
    http_route: builtins.str,
    service: builtins.str,
    pod_selector_label: typing.Optional[builtins.str] = None,
    route_destinations: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations, typing.Dict[builtins.str, typing.Any]]] = None,
    route_update_wait_time: typing.Optional[builtins.str] = None,
    stable_cutback_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17412bc2592cc51d96b3734f69c69cdd8ec07373dc972d888d54df5b065b1e9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da7544bb124c68ede17b48c17e58173e164734018553c1064284da4724292dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a149684f6be6d6bf943b017f323a47368cd822b2b0e7a2b52180c9d9deabd3c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d02d7dc63c15a77cd60847e71893d0ba2e758f5e604e616c0cf68f9a3ca990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cf5f8c60cf6bce93c8c8fdab42a2a817c4d55313f82d7e271b819c1a18d369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d56049875ca24be8d3debef419b8924a793a2f7329b16dabd287e42722290de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9c6556c1dd78657c458624282c740c0c21c87c37121d0ac82b9affa6a3dd7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d74e5282f773107e263ce6ca532861398e99092c267880596f395900b65fb1(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3082bc9bc0cbf05de15d13bdfd5b8850394a79c2c053f6dd8bdeb578b341e8ba(
    *,
    destination_ids: typing.Sequence[builtins.str],
    propagate_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6beff47db237b4a2a5e21643e50cbf7ee6c0e7350ceaf669332d43f010e6df4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f3a5297bcd6a53de45291c2574e7d9752a697d75f6d2fe3137fc7f6e207254(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c2f1e98b18c34dca3032abb251b73a6191d4ef208e487c5f0b0c965a4eae23(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9ff3062d91c8e0d462749ae416b436d89eb989e83dac979ce275c1d412f31d(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629f24bbfda2f5861fbff8b06d6214c23ef1670a9c039c15817819bdde91a8ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7695250a8c427fee82a224d02b03045287086fb7f9eea20c18d5f5684aaa99d3(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c7e829d3da0cf9e42507d8b271deca8875b17b65d043b7e67232c47f2694a4(
    *,
    deployment: builtins.str,
    service: builtins.str,
    disable_pod_overprovisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pod_selector_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362179957a61382d325bc893ef7acaa6150417dd5dd75453c9832579f1f1102a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1e1096ae82c6841d7fc475c5e92cc29605d3854ca30e66078bc84f1e60e658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c54433174be89448c372564bf3adf267626d37bca73706278c3c3cef7b4909(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896ab4f3b9a96639c423b6c8f7931198b8378fac53da010605267fb50e3becce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e07d85ca6a17e64678e49d41c6e262ee55b3450f4b882508185daad7886d2f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077a538c0721acd7d464e48e44a2a164488504d8cc52ee7c105e5bbca0b7c587(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657440fe5d61decc3a160a48ca2283d4dec388991d7be8f898de804e1a48788c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42bf10375399f0f4ff37aff2ca1f49013a7d9579552dbf8b2eab3e98e0d91af(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2f2ee70505cc71f053bae8d08b0370dc10815a1a7ad113efd9576d6b78a0e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5152c094e65f19545f62114144d189a6bb9d5c286deac0243aa0e033783376(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c28849902c44a85c41e9d0a0dffffb309de959e92f0daddea501c869a9723d(
    *,
    postdeploy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    predeploy: typing.Optional[typing.Union[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385bee20f5c709d7f071e9c418b9bda79a4f44d76438b13a167a12034d51266a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ad95878b09ebfe696630082a432a808c62b8b386dc67cc8d8103d914c1028d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10601cb76bbbc0d2a89fc7183676d8bcf98a57941269f8bfffbf861af890bd5b(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6b18ebb05a1a945c1865ab90fdaa9e69958f6194ecc674154c5ac39be8b3da(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6b00df4c2813f815678d75d45128517abad38562c74891ff4d723f03d4e7f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3d14352b1a2351fa9af8644ae24cce02977fa806a21945299bea48ddfb3f0f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7e8a57053cadf584fa483e0f92cae736c6758d9f9c5b624b68ebe2d88d1045(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d40840f1afe39fd5109331e48b56ba43c9c88d5e6471ae9bbf2846c7b4ecb47(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ea5b5d09c03da4363e00ecfae097a29b15137f3805e9f0626690b346b325a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55afb50935a47b12bd0d0ca3165d80abb388a0f2288ac7fe95d74a9820660dfc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5395a50a62202fcdaf4f7c8132cfef83ae2d0adf665af367d4e0c11e4625618e(
    value: typing.Optional[GoogleClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc8b9431c261ca1a72980fd6d0499a13faaf209819b1d4ef245d26e73c92b3e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92eadb026315908613c62570faadd3a8ab92a25b725353dc3c2155ca55f1a678(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a15766774de0a8068dd7a4fdfa7dc8233b581ad41c88ef0f4013ae52f971f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7112fd93a3ffbb96b4171d48860660e01fbb8c154250f1e41358e9e6a36c344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17af23c29bb8aa139f85d3d686d73d1234ad9c3e594e9eee594e9a015d342170(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec1d0cb77be32c032b1b2ab2cef23e7bfc9ff71f2c98691b38945aa58884202(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeliveryPipelineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
