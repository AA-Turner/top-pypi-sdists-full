r'''
# `google_clouddeploy_delivery_pipeline`

Refer to the Terraform Registry for docs: [`google_clouddeploy_delivery_pipeline`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline).
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


class ClouddeployDeliveryPipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline google_clouddeploy_delivery_pipeline}.'''

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
        serial_pipeline: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipeline", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployDeliveryPipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline google_clouddeploy_delivery_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#location ClouddeployDeliveryPipeline#location}
        :param name: Name of the ``DeliveryPipeline``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#name ClouddeployDeliveryPipeline#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#annotations ClouddeployDeliveryPipeline#annotations}
        :param description: Description of the ``DeliveryPipeline``. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#description ClouddeployDeliveryPipeline#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#id ClouddeployDeliveryPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#labels ClouddeployDeliveryPipeline#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#project ClouddeployDeliveryPipeline#project}
        :param serial_pipeline: serial_pipeline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#serial_pipeline ClouddeployDeliveryPipeline#serial_pipeline}
        :param suspended: When suspended, no new releases or rollouts can be created, but in-progress ones will complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#suspended ClouddeployDeliveryPipeline#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#timeouts ClouddeployDeliveryPipeline#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f6d2becf637609069b5fd59e6eabe3ee22126543da43549222507d364a5f57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ClouddeployDeliveryPipelineConfig(
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
        '''Generates CDKTF code for importing a ClouddeployDeliveryPipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ClouddeployDeliveryPipeline to import.
        :param import_from_id: The id of the existing ClouddeployDeliveryPipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ClouddeployDeliveryPipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4f486d8fa365334a44911795038912ee6d313ec21d3576e7c2c709b3c2f688)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSerialPipeline")
    def put_serial_pipeline(
        self,
        *,
        stages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param stages: stages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stages ClouddeployDeliveryPipeline#stages}
        '''
        value = ClouddeployDeliveryPipelineSerialPipeline(stages=stages)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#create ClouddeployDeliveryPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#delete ClouddeployDeliveryPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#update ClouddeployDeliveryPipeline#update}.
        '''
        value = ClouddeployDeliveryPipelineTimeouts(
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
    def condition(self) -> "ClouddeployDeliveryPipelineConditionList":
        return typing.cast("ClouddeployDeliveryPipelineConditionList", jsii.get(self, "condition"))

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
    ) -> "ClouddeployDeliveryPipelineSerialPipelineOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineOutputReference", jsii.get(self, "serialPipeline"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ClouddeployDeliveryPipelineTimeoutsOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipeline"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipeline"], jsii.get(self, "serialPipelineInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployDeliveryPipelineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployDeliveryPipelineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dbf60e8a5ac661255863e1049b13f8c9ed51ea9c9f91a542c86291d687f559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1711d99f755970aaa593fdf57e26e07f505363d1b9ef5ba80ff11d452c0344d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c01bb67dcc40c01314d098abe04287be8fa03ed445e92593f66973ce0300d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e048057bfb254c65a694948ac37bbd05dd4ed6dadd095b521c0a8ae8d94e40a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3011a27cd565aaa8e6e01dfdee67dee4f8a3e427a571d3e8ff65a178d8d226c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3ca7cfe7606bf6997582151a4a7c73f086df28f5590ca0a085404af42ac678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4d8d7c4e660eeb932856e1f5c18921c8a9f2ae686e65b08ab9248295f06f72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64b54e0ae79567d0a1f95ed9d83b2779a1714ebf246d86a80e2c515282b677b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class ClouddeployDeliveryPipelineCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45c676f470c198c16fe06bcba673c843e04d78ca19aea9b4468e6a1bec559137)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94518569ccba9d1e9a20ec6ad6c4ce017ab430af45877d80409eb00b8562edc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228a43997ba4e5812fe6084e6e27950d8c067645078e1f2f6e12ae91cc5abf65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab31d7ec69007901a53ca1d3adb22e30f8513e368d63303f9431d3d2a224ef46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73bca1f9359f4a89383a34599e5e57f704a01f4e5f77f2ab92d8540c8bef0e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__249224777bcb676c4558918de946bec4c2562a5781fb3afeed163bf517f64e17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pipelineReadyCondition")
    def pipeline_ready_condition(
        self,
    ) -> "ClouddeployDeliveryPipelineConditionPipelineReadyConditionList":
        return typing.cast("ClouddeployDeliveryPipelineConditionPipelineReadyConditionList", jsii.get(self, "pipelineReadyCondition"))

    @builtins.property
    @jsii.member(jsii_name="targetsPresentCondition")
    def targets_present_condition(
        self,
    ) -> "ClouddeployDeliveryPipelineConditionTargetsPresentConditionList":
        return typing.cast("ClouddeployDeliveryPipelineConditionTargetsPresentConditionList", jsii.get(self, "targetsPresentCondition"))

    @builtins.property
    @jsii.member(jsii_name="targetsTypeCondition")
    def targets_type_condition(
        self,
    ) -> "ClouddeployDeliveryPipelineConditionTargetsTypeConditionList":
        return typing.cast("ClouddeployDeliveryPipelineConditionTargetsTypeConditionList", jsii.get(self, "targetsTypeCondition"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployDeliveryPipelineCondition]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03579ca183e8567df8adba4ca2a7fc267505fef2f4133d67dfa9cfa335ebc6eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionPipelineReadyCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class ClouddeployDeliveryPipelineConditionPipelineReadyCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineConditionPipelineReadyCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineConditionPipelineReadyConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionPipelineReadyConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c91147f78840a38c9eab4720ed98de5d2a22be89d49c7965a001ce5ec00a5882)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae3d0af9f580d452814f80aadc4c4f03228fe7748e5633c8aa0b49e5fc3681a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f153a8a79486f3e88e7b42b2e1d98dd46288001b9a0eb7d6adf4f6297ed6109)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07b966011e0d4091d985b241572df925b04f665f4fe725ebaae305acb0649e8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3be028be45426ca38f4d63e324c5539cc3f9681f5f76c1fd127adefc16ff09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec2673c769495647b3bd70d860177115ed06e816a68012304df7d9efcfca925)
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
    ) -> typing.Optional[ClouddeployDeliveryPipelineConditionPipelineReadyCondition]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineConditionPipelineReadyCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineConditionPipelineReadyCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e2ff9d2b5c3225bc01adf05c1845355608a05c135bfad7f9f8ee757e6413e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsPresentCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class ClouddeployDeliveryPipelineConditionTargetsPresentCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineConditionTargetsPresentCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineConditionTargetsPresentConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsPresentConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6423c36a5683aa05f1152f472b7d5cf94ba70962883944fec26910f7d084a888)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819b52da79e4b0e072217dccb2b1acbeb4ee6a22c1b220f29a433fb5ef9d695a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c9d287ecd9b9666ac5eb6440f4e21fb9f2a18bf7c22f01880068a5e6820869)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78038831e64d108ab27f952c47e6ef3c3f79bbb097f6329bf68619b6065218f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b976f633c8fc26f6dcccc66274b4836cbaecb6dca87f9a1b3683cdcb6cf594d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b174696157bbeafb6d0150c3f73b1ce2e63a3174635d4d14f4dfb14476679128)
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
    ) -> typing.Optional[ClouddeployDeliveryPipelineConditionTargetsPresentCondition]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineConditionTargetsPresentCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineConditionTargetsPresentCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b7c211b73d3889603608cb698480d91d87e7d0b749d70ca1548048c9d5fd72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsTypeCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class ClouddeployDeliveryPipelineConditionTargetsTypeCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineConditionTargetsTypeCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineConditionTargetsTypeConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsTypeConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf50a5a007a598f8b3b8be570bbc5ce5146c699947eb85757b37e69dde0f92f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae434d6770e24dbfcac7a7cabdc529772f2d83bdceace62c0affa320c84c10e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40dd052c376c59e9772230dfbdf398a3fa5349b6b02248966b8d9c76b1fdd38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__344182f27aa53f162c42ed6e771e8c35e2e04724f3fed6af3cebe299fca69230)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47fb31221d62ae4b1a725417bde5b15c6feb3bb1de0c5d9fa562c2848476eff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04e5b67a1b79fca4e3c1d7b2604f853cda5fb86ba9627a26048bed16bbeb53e2)
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
    ) -> typing.Optional[ClouddeployDeliveryPipelineConditionTargetsTypeCondition]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineConditionTargetsTypeCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineConditionTargetsTypeCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afefd0e05208aa87f27dee80632c3cbb848ad1a9825a0e890948aeb764560cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineConfig",
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
class ClouddeployDeliveryPipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        serial_pipeline: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipeline", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployDeliveryPipelineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#location ClouddeployDeliveryPipeline#location}
        :param name: Name of the ``DeliveryPipeline``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#name ClouddeployDeliveryPipeline#name}
        :param annotations: User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy. See https://google.aip.dev/128#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#annotations ClouddeployDeliveryPipeline#annotations}
        :param description: Description of the ``DeliveryPipeline``. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#description ClouddeployDeliveryPipeline#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#id ClouddeployDeliveryPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field ``effective_labels`` for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#labels ClouddeployDeliveryPipeline#labels}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#project ClouddeployDeliveryPipeline#project}
        :param serial_pipeline: serial_pipeline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#serial_pipeline ClouddeployDeliveryPipeline#serial_pipeline}
        :param suspended: When suspended, no new releases or rollouts can be created, but in-progress ones will complete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#suspended ClouddeployDeliveryPipeline#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#timeouts ClouddeployDeliveryPipeline#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(serial_pipeline, dict):
            serial_pipeline = ClouddeployDeliveryPipelineSerialPipeline(**serial_pipeline)
        if isinstance(timeouts, dict):
            timeouts = ClouddeployDeliveryPipelineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7d420b3bb0d4dd1a78694afa730bbee29379b99845303e5bc49ebecdd7bd9e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#location ClouddeployDeliveryPipeline#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the ``DeliveryPipeline``. Format is ``[a-z]([a-z0-9-]{0,61}[a-z0-9])?``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#name ClouddeployDeliveryPipeline#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#annotations ClouddeployDeliveryPipeline#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the ``DeliveryPipeline``. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#description ClouddeployDeliveryPipeline#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#id ClouddeployDeliveryPipeline#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#labels ClouddeployDeliveryPipeline#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#project ClouddeployDeliveryPipeline#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_pipeline(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipeline"]:
        '''serial_pipeline block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#serial_pipeline ClouddeployDeliveryPipeline#serial_pipeline}
        '''
        result = self._values.get("serial_pipeline")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipeline"], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When suspended, no new releases or rollouts can be created, but in-progress ones will complete.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#suspended ClouddeployDeliveryPipeline#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ClouddeployDeliveryPipelineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#timeouts ClouddeployDeliveryPipeline#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipeline",
    jsii_struct_bases=[],
    name_mapping={"stages": "stages"},
)
class ClouddeployDeliveryPipelineSerialPipeline:
    def __init__(
        self,
        *,
        stages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param stages: stages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stages ClouddeployDeliveryPipeline#stages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f21a0795432925fb1deaf3a6dfc41bb2919941f1850d453e799aefdf3a2bec)
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if stages is not None:
            self._values["stages"] = stages

    @builtins.property
    def stages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStages"]]]:
        '''stages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stages ClouddeployDeliveryPipeline#stages}
        '''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipeline(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afd88821b0c6aeb0833497cd9c9bbbb0f97ebe51107e4f1f5f55ca7ee447afab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStages")
    def put_stages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb6a235866b7cd7bb7a02498bdd3e467def5f539da1d78c279d7441405a8b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStages", [value]))

    @jsii.member(jsii_name="resetStages")
    def reset_stages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStages", []))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> "ClouddeployDeliveryPipelineSerialPipelineStagesList":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesList", jsii.get(self, "stages"))

    @builtins.property
    @jsii.member(jsii_name="stagesInput")
    def stages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStages"]]], jsii.get(self, "stagesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipeline]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipeline], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipeline],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed600858b6536e2ea0c3e6eda6358fab3e979e549438121d171cc7a51fe2e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStages",
    jsii_struct_bases=[],
    name_mapping={
        "deploy_parameters": "deployParameters",
        "profiles": "profiles",
        "strategy": "strategy",
        "target_id": "targetId",
    },
)
class ClouddeployDeliveryPipelineSerialPipelineStages:
    def __init__(
        self,
        *,
        deploy_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
        strategy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        target_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deploy_parameters: deploy_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#deploy_parameters ClouddeployDeliveryPipeline#deploy_parameters}
        :param profiles: Skaffold profiles to use when rendering the manifest for this stage's ``Target``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#profiles ClouddeployDeliveryPipeline#profiles}
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#strategy ClouddeployDeliveryPipeline#strategy}
        :param target_id: The target_id to which this stage points. This field refers exclusively to the last segment of a target name. For example, this field would just be ``my-target`` (rather than ``projects/project/locations/location/targets/my-target``). The location of the ``Target`` is inferred to be the same as the location of the ``DeliveryPipeline`` that contains this ``Stage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#target_id ClouddeployDeliveryPipeline#target_id}
        '''
        if isinstance(strategy, dict):
            strategy = ClouddeployDeliveryPipelineSerialPipelineStagesStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e96264602fc4ef1c9f73a994ddd5179850d70f44fd32c3b8d2194016f8a673)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters"]]]:
        '''deploy_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#deploy_parameters ClouddeployDeliveryPipeline#deploy_parameters}
        '''
        result = self._values.get("deploy_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters"]]], result)

    @builtins.property
    def profiles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Skaffold profiles to use when rendering the manifest for this stage's ``Target``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#profiles ClouddeployDeliveryPipeline#profiles}
        '''
        result = self._values.get("profiles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def strategy(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategy"]:
        '''strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#strategy ClouddeployDeliveryPipeline#strategy}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategy"], result)

    @builtins.property
    def target_id(self) -> typing.Optional[builtins.str]:
        '''The target_id to which this stage points.

        This field refers exclusively to the last segment of a target name. For example, this field would just be ``my-target`` (rather than ``projects/project/locations/location/targets/my-target``). The location of the ``Target`` is inferred to be the same as the location of the ``DeliveryPipeline`` that contains this ``Stage``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#target_id ClouddeployDeliveryPipeline#target_id}
        '''
        result = self._values.get("target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters",
    jsii_struct_bases=[],
    name_mapping={"values": "values", "match_target_labels": "matchTargetLabels"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters:
    def __init__(
        self,
        *,
        values: typing.Mapping[builtins.str, builtins.str],
        match_target_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param values: Required. Values are deploy parameters in key-value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#values ClouddeployDeliveryPipeline#values}
        :param match_target_labels: Optional. Deploy parameters are applied to targets with match labels. If unspecified, deploy parameters are applied to all targets (including child targets of a multi-target). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#match_target_labels ClouddeployDeliveryPipeline#match_target_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ed04fb8cfa07660e277a853b4efc0df635e1b6ad999a9a167bd3873b948f4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#values ClouddeployDeliveryPipeline#values}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#match_target_labels ClouddeployDeliveryPipeline#match_target_labels}
        '''
        result = self._values.get("match_target_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5984937e6299f3b74b6d5c446c627654b710585c9b78026aa3ea92187ca3028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9773fd125cec01d635c3d52bd6eb955e1a855bd42a7dc71a509352df627f5beb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ece48e562d879f85967887a310170476730e092143faaea55a289bdc8cdcc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__887c42df025a4cdb68240a32d50f9331662440c7e0fd7f115b9bc150b8565864)
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
            type_hints = typing.get_type_hints(_typecheckingstub__897e3e44a82b3c9bcfa35b358b0e1c07794a7ab9d5991bf102ecf294b6e684c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea355a1e002bdf92837bda9c535ff71f88ca114e58e1bca209178170326ca990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__484d4257d3a079650555cfe62853f3ecf18587897d34e0700e4f9302a511df73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c96b5c9426b1a9b0d53d46c49b228aff9d80962cff52587df918ebe62f91acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchTargetLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8dab540ea8ca610c382daac6a653d08aa6f930ef3276cc21504edfff23bb9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c063da0eeae93a62f7abbd628e36d95f3622cdeea91a3f1fd8e58a78346e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineSerialPipelineStagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4357803e10f270618d5debe61f902a3cd36d6c1398efc30017ebfd970a477f3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d34ba4422c28cdbdbe3f6d1ca842ac5fcff0cae411e9f0bda02663cc689c8ad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0523177180ab6b0f1f0a4ed9d2e119c5692e301f19fe022454480e2f1e6d805c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08a704df71b3513cce64d17c7f8d09ca6b2aaad51a14334354b7e948b8408414)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83ca4387c7a2689d2643b225b1e59eb01c562331147d3b73e378ecf9d748d95a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1879db875f649cf27c633ad262da4ef2a0a3adb6f05b0facb1ab5b489d5c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__747debe07a8d0ccffed772a06daa93d13d6480f1ce54332bb457fca9edfea539)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDeployParameters")
    def put_deploy_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b3db53c7ba2b5de085f06f3901d19c1d71adc5ebdf9644fd68f9e2368fe916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeployParameters", [value]))

    @jsii.member(jsii_name="putStrategy")
    def put_strategy(
        self,
        *,
        canary: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary", typing.Dict[builtins.str, typing.Any]]] = None,
        standard: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param canary: canary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary ClouddeployDeliveryPipeline#canary}
        :param standard: standard block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#standard ClouddeployDeliveryPipeline#standard}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategy(
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
    ) -> ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList:
        return typing.cast(ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList, jsii.get(self, "deployParameters"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference", jsii.get(self, "strategy"))

    @builtins.property
    @jsii.member(jsii_name="deployParametersInput")
    def deploy_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]], jsii.get(self, "deployParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="profilesInput")
    def profiles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "profilesInput"))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategy"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategy"], jsii.get(self, "strategyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c0931469831a0144c4c9427e224bb1d5eee3387a0eead523e7619dcb737ed176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetId"))

    @target_id.setter
    def target_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89cfc3b7ce0140483ebef1f54a24f2afb4b088081d8c77b77c2506e60eca4ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f37d84ebe1f48149f0393cb405233d3381ef41ecdde1515c788062bf9b33ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategy",
    jsii_struct_bases=[],
    name_mapping={"canary": "canary", "standard": "standard"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategy:
    def __init__(
        self,
        *,
        canary: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary", typing.Dict[builtins.str, typing.Any]]] = None,
        standard: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param canary: canary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary ClouddeployDeliveryPipeline#canary}
        :param standard: standard block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#standard ClouddeployDeliveryPipeline#standard}
        '''
        if isinstance(canary, dict):
            canary = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary(**canary)
        if isinstance(standard, dict):
            standard = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard(**standard)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6279f6785178548ebbaf2b70aea55bb958a98a8c507a5ac8fc4fee99fdae451f)
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
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary"]:
        '''canary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary ClouddeployDeliveryPipeline#canary}
        '''
        result = self._values.get("canary")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary"], result)

    @builtins.property
    def standard(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard"]:
        '''standard block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#standard ClouddeployDeliveryPipeline#standard}
        '''
        result = self._values.get("standard")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary",
    jsii_struct_bases=[],
    name_mapping={
        "canary_deployment": "canaryDeployment",
        "custom_canary_deployment": "customCanaryDeployment",
        "runtime_config": "runtimeConfig",
    },
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary:
    def __init__(
        self,
        *,
        canary_deployment: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_canary_deployment: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_config: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param canary_deployment: canary_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary_deployment ClouddeployDeliveryPipeline#canary_deployment}
        :param custom_canary_deployment: custom_canary_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#custom_canary_deployment ClouddeployDeliveryPipeline#custom_canary_deployment}
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#runtime_config ClouddeployDeliveryPipeline#runtime_config}
        '''
        if isinstance(canary_deployment, dict):
            canary_deployment = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment(**canary_deployment)
        if isinstance(custom_canary_deployment, dict):
            custom_canary_deployment = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment(**custom_canary_deployment)
        if isinstance(runtime_config, dict):
            runtime_config = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig(**runtime_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a207f5f44e4b037d6c4b07932f6ba916b2c682662a0a04266d78e650241ea99b)
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
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment"]:
        '''canary_deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary_deployment ClouddeployDeliveryPipeline#canary_deployment}
        '''
        result = self._values.get("canary_deployment")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment"], result)

    @builtins.property
    def custom_canary_deployment(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment"]:
        '''custom_canary_deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#custom_canary_deployment ClouddeployDeliveryPipeline#custom_canary_deployment}
        '''
        result = self._values.get("custom_canary_deployment")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment"], result)

    @builtins.property
    def runtime_config(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig"]:
        '''runtime_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#runtime_config ClouddeployDeliveryPipeline#runtime_config}
        '''
        result = self._values.get("runtime_config")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment",
    jsii_struct_bases=[],
    name_mapping={
        "percentages": "percentages",
        "postdeploy": "postdeploy",
        "predeploy": "predeploy",
        "verify": "verify",
    },
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment:
    def __init__(
        self,
        *,
        percentages: typing.Sequence[jsii.Number],
        postdeploy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param percentages: Required. The percentage based deployments that will occur as a part of a ``Rollout``. List is expected in ascending order and each integer n is 0 <= n < 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#percentages ClouddeployDeliveryPipeline#percentages}
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#postdeploy ClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#predeploy ClouddeployDeliveryPipeline#predeploy}
        :param verify: Whether to run verify tests after each percentage deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#verify ClouddeployDeliveryPipeline#verify}
        '''
        if isinstance(postdeploy, dict):
            postdeploy = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy(**postdeploy)
        if isinstance(predeploy, dict):
            predeploy = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy(**predeploy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54aee5fa0d1aed2b48111ee320d4221d3b09d417d08fc8db9733a1e3fcedc722)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#percentages ClouddeployDeliveryPipeline#percentages}
        '''
        result = self._values.get("percentages")
        assert result is not None, "Required property 'percentages' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def postdeploy(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy"]:
        '''postdeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#postdeploy ClouddeployDeliveryPipeline#postdeploy}
        '''
        result = self._values.get("postdeploy")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy"], result)

    @builtins.property
    def predeploy(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy"]:
        '''predeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#predeploy ClouddeployDeliveryPipeline#predeploy}
        '''
        result = self._values.get("predeploy")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy"], result)

    @builtins.property
    def verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run verify tests after each percentage deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#verify ClouddeployDeliveryPipeline#verify}
        '''
        result = self._values.get("verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfe3e6c9196cf3fa8349c563ccb3226d2abeb6704e80f1e80ea8dd9d8c0e413c)
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
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy(
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
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy(
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
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference", jsii.get(self, "postdeploy"))

    @builtins.property
    @jsii.member(jsii_name="predeploy")
    def predeploy(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference", jsii.get(self, "predeploy"))

    @builtins.property
    @jsii.member(jsii_name="percentagesInput")
    def percentages_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "percentagesInput"))

    @builtins.property
    @jsii.member(jsii_name="postdeployInput")
    def postdeploy_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy"], jsii.get(self, "postdeployInput"))

    @builtins.property
    @jsii.member(jsii_name="predeployInput")
    def predeploy_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy"], jsii.get(self, "predeployInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__035128ae9eb3674a034b016345d093e22c6c31a39ca7f1056565aae231bf0ef6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a75d728cdd55f5eb3260b6cce9f618317769c2a9891092db63ce865b683d6fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac3a437f6f4155da2409939c93370d64fb959679f5c5fac54d49f641dd18f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551c7bad9d6dc30ebf9ef1d36fdb0c33bf3f427b3284f5ecf89b8dee634b5f8c)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__260fe1794033e37b5ef1e3780f1773b82e9b949b6f87b25b7a62e52dd81e8056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad495084942bee533536f83aa6b7eaaad582e33236f23c57c0427ee0ededbbb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bba7a8a8876f2094283cd5fd9188aee9b8082ff50af564462064302c3f7d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__962fdd029ab7fef0cc6669a84b295ec831305a33da811550673dca0b0207a1b2)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9465dddf2a23acdf86cabe74961a51236b9ce4ccc2a9c5c91f66aedb45acecfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e7363c187f5d2041991e3d82ab3b5211dc25080c4cd633dced4773c8a5032a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830f5dca045f7a7fe49d891bc9131ba26001bdafa7e46ae71b7a460868d4f919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment",
    jsii_struct_bases=[],
    name_mapping={"phase_configs": "phaseConfigs"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment:
    def __init__(
        self,
        *,
        phase_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param phase_configs: phase_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#phase_configs ClouddeployDeliveryPipeline#phase_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f76050263c1212bd65ef32fa43bd16e9dbc4af66896ad56b185aa8ed789aeb)
            check_type(argname="argument phase_configs", value=phase_configs, expected_type=type_hints["phase_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phase_configs": phase_configs,
        }

    @builtins.property
    def phase_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs"]]:
        '''phase_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#phase_configs ClouddeployDeliveryPipeline#phase_configs}
        '''
        result = self._values.get("phase_configs")
        assert result is not None, "Required property 'phase_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2b705864461ab277d58b88a8db875faabe40946c6775634d8704c64317f224)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPhaseConfigs")
    def put_phase_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae2838c1a6431fcbe3670f657d38142353fac98b286e8411e95d286ec847452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPhaseConfigs", [value]))

    @builtins.property
    @jsii.member(jsii_name="phaseConfigs")
    def phase_configs(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList", jsii.get(self, "phaseConfigs"))

    @builtins.property
    @jsii.member(jsii_name="phaseConfigsInput")
    def phase_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs"]]], jsii.get(self, "phaseConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829034f821f401e8bff4994978f564853276aa180eca86cf03c4c359ddcff44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs",
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
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs:
    def __init__(
        self,
        *,
        percentage: jsii.Number,
        phase_id: builtins.str,
        postdeploy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param percentage: Required. Percentage deployment for the phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#percentage ClouddeployDeliveryPipeline#percentage}
        :param phase_id: Required. The ID to assign to the ``Rollout`` phase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ``^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#phase_id ClouddeployDeliveryPipeline#phase_id}
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#postdeploy ClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#predeploy ClouddeployDeliveryPipeline#predeploy}
        :param profiles: Skaffold profiles to use when rendering the manifest for this phase. These are in addition to the profiles list specified in the ``DeliveryPipeline`` stage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#profiles ClouddeployDeliveryPipeline#profiles}
        :param verify: Whether to run verify tests after the deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#verify ClouddeployDeliveryPipeline#verify}
        '''
        if isinstance(postdeploy, dict):
            postdeploy = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy(**postdeploy)
        if isinstance(predeploy, dict):
            predeploy = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy(**predeploy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75ee60612b94cd86e95d689009a877ae24e44c5a8152b4d8798cde070f99ef0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#percentage ClouddeployDeliveryPipeline#percentage}
        '''
        result = self._values.get("percentage")
        assert result is not None, "Required property 'percentage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def phase_id(self) -> builtins.str:
        '''Required.

        The ID to assign to the ``Rollout`` phase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ``^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#phase_id ClouddeployDeliveryPipeline#phase_id}
        '''
        result = self._values.get("phase_id")
        assert result is not None, "Required property 'phase_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postdeploy(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy"]:
        '''postdeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#postdeploy ClouddeployDeliveryPipeline#postdeploy}
        '''
        result = self._values.get("postdeploy")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy"], result)

    @builtins.property
    def predeploy(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy"]:
        '''predeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#predeploy ClouddeployDeliveryPipeline#predeploy}
        '''
        result = self._values.get("predeploy")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy"], result)

    @builtins.property
    def profiles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Skaffold profiles to use when rendering the manifest for this phase.

        These are in addition to the profiles list specified in the ``DeliveryPipeline`` stage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#profiles ClouddeployDeliveryPipeline#profiles}
        '''
        result = self._values.get("profiles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to run verify tests after the deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#verify ClouddeployDeliveryPipeline#verify}
        '''
        result = self._values.get("verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44085d9cdcf980c0d790b6081a85d20b6674de73cf68c321af92e9ec3cf979aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed30341a1f5c990a8f46dcbe422309f87b01c28d745416f88acf16139437f575)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7613fc1239471f914d28d8905a3a423cf2f262aa1899960e36b19cebb5e931)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19284ed8eebbfce18c3db6425e4f567dde143b4be38312893aee1683db4f2354)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aba2c26fc00f8628f6b117c8b2d8a9af5b6ade74668629ed519fd7fb304d0fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af00c1bc611da3b2836b50f95ab031ff357bfd46397886ea949dadfbc1f3c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3296919ab97f18b78d71f007e6538a7e1603c27d2291f050437331090be2030f)
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
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy(
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
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy(
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
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference", jsii.get(self, "postdeploy"))

    @builtins.property
    @jsii.member(jsii_name="predeploy")
    def predeploy(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference", jsii.get(self, "predeploy"))

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
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy"], jsii.get(self, "postdeployInput"))

    @builtins.property
    @jsii.member(jsii_name="predeployInput")
    def predeploy_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy"], jsii.get(self, "predeployInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1fbfa19f885f80b4534020f92f222d3c36b89fecd66fd5f1b4258ab1ed5f7450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phaseId")
    def phase_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phaseId"))

    @phase_id.setter
    def phase_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e376c7d792bdfe740845c5cb0e281d8210832fbc6c909a33a109ddb51a9050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profiles")
    def profiles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "profiles"))

    @profiles.setter
    def profiles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439f8defa46f6abb0c0762cde27f71c7b6483cebafc40ce7a734e6e19b0a959c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07edce63bf3eac1f45b513f42a42ac207b8dcfb8704e548887fa73cc553aee30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ef587bf4fc807363253239b8a86456a4467ac99da35d147f6deb88c23d5512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e31bbaa61d3064bfb2ad5494f2986914a2fdfdab6656227ec12d3ac435554e)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c274a50e73c6afa7784144974345d675166b56cdae69cb6de3156fa022e2fe1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85410580f9415f9f03a9136c6ac772719860cb13381f3f01a7ba299871f0550d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72857f9a7100935c6bfacc53124204d2a0eb3cc1132fdeb50b757ce43896b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d85996c5f1077ae36373f6122c7c0ce7027ac7d9b698f39c24e81c16493ad2c)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1019aa3a670073f87bfeae2b7dcf5e1ada05418136f041d556172a7a6e4f2c4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ff56a99656cfd0851f33195b1f309fdce46ae5184a264a0f9ab58566e9a9866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3edc7509c1f58e6643393ee032be92a9f35b0639eff34d4fbe0fe57c210f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f17f7ed86e7eb760e0ac17289f41e953abbc0c074b28927a878713a39f20696d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCanaryDeployment")
    def put_canary_deployment(
        self,
        *,
        percentages: typing.Sequence[jsii.Number],
        postdeploy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy, typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy, typing.Dict[builtins.str, typing.Any]]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param percentages: Required. The percentage based deployments that will occur as a part of a ``Rollout``. List is expected in ascending order and each integer n is 0 <= n < 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#percentages ClouddeployDeliveryPipeline#percentages}
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#postdeploy ClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#predeploy ClouddeployDeliveryPipeline#predeploy}
        :param verify: Whether to run verify tests after each percentage deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#verify ClouddeployDeliveryPipeline#verify}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment(
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
        phase_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param phase_configs: phase_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#phase_configs ClouddeployDeliveryPipeline#phase_configs}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment(
            phase_configs=phase_configs
        )

        return typing.cast(None, jsii.invoke(self, "putCustomCanaryDeployment", [value]))

    @jsii.member(jsii_name="putRuntimeConfig")
    def put_runtime_config(
        self,
        *,
        cloud_run: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_run: cloud_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#cloud_run ClouddeployDeliveryPipeline#cloud_run}
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#kubernetes ClouddeployDeliveryPipeline#kubernetes}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig(
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
    ) -> ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference:
        return typing.cast(ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference, jsii.get(self, "canaryDeployment"))

    @builtins.property
    @jsii.member(jsii_name="customCanaryDeployment")
    def custom_canary_deployment(
        self,
    ) -> ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference:
        return typing.cast(ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference, jsii.get(self, "customCanaryDeployment"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfig")
    def runtime_config(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference", jsii.get(self, "runtimeConfig"))

    @builtins.property
    @jsii.member(jsii_name="canaryDeploymentInput")
    def canary_deployment_input(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment], jsii.get(self, "canaryDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="customCanaryDeploymentInput")
    def custom_canary_deployment_input(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment], jsii.get(self, "customCanaryDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigInput")
    def runtime_config_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig"], jsii.get(self, "runtimeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f71979981dbd2cdbe27cc2ae891b1e3886a49600b4ff32ff81be8425b522ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig",
    jsii_struct_bases=[],
    name_mapping={"cloud_run": "cloudRun", "kubernetes": "kubernetes"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig:
    def __init__(
        self,
        *,
        cloud_run: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_run: cloud_run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#cloud_run ClouddeployDeliveryPipeline#cloud_run}
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#kubernetes ClouddeployDeliveryPipeline#kubernetes}
        '''
        if isinstance(cloud_run, dict):
            cloud_run = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun(**cloud_run)
        if isinstance(kubernetes, dict):
            kubernetes = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes(**kubernetes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053e65bdfc776ca68b3221ca3ad417ca5938cc838e4c7a6463e1adfb6092cea3)
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
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun"]:
        '''cloud_run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#cloud_run ClouddeployDeliveryPipeline#cloud_run}
        '''
        result = self._values.get("cloud_run")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun"], result)

    @builtins.property
    def kubernetes(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes"]:
        '''kubernetes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#kubernetes ClouddeployDeliveryPipeline#kubernetes}
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun",
    jsii_struct_bases=[],
    name_mapping={
        "automatic_traffic_control": "automaticTrafficControl",
        "canary_revision_tags": "canaryRevisionTags",
        "prior_revision_tags": "priorRevisionTags",
        "stable_revision_tags": "stableRevisionTags",
    },
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun:
    def __init__(
        self,
        *,
        automatic_traffic_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        canary_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        prior_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        stable_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param automatic_traffic_control: Whether Cloud Deploy should update the traffic stanza in a Cloud Run Service on the user's behalf to facilitate traffic splitting. This is required to be true for CanaryDeployments, but optional for CustomCanaryDeployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#automatic_traffic_control ClouddeployDeliveryPipeline#automatic_traffic_control}
        :param canary_revision_tags: Optional. A list of tags that are added to the canary revision while the canary phase is in progress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary_revision_tags ClouddeployDeliveryPipeline#canary_revision_tags}
        :param prior_revision_tags: Optional. A list of tags that are added to the prior revision while the canary phase is in progress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#prior_revision_tags ClouddeployDeliveryPipeline#prior_revision_tags}
        :param stable_revision_tags: Optional. A list of tags that are added to the final stable revision when the stable phase is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stable_revision_tags ClouddeployDeliveryPipeline#stable_revision_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918ae210d81316b67a4d82dcfaf75f281dacaab9551da1e24f5ed4d96c6201fe)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#automatic_traffic_control ClouddeployDeliveryPipeline#automatic_traffic_control}
        '''
        result = self._values.get("automatic_traffic_control")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def canary_revision_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A list of tags that are added to the canary revision while the canary phase is in progress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary_revision_tags ClouddeployDeliveryPipeline#canary_revision_tags}
        '''
        result = self._values.get("canary_revision_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prior_revision_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A list of tags that are added to the prior revision while the canary phase is in progress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#prior_revision_tags ClouddeployDeliveryPipeline#prior_revision_tags}
        '''
        result = self._values.get("prior_revision_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stable_revision_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A list of tags that are added to the final stable revision when the stable phase is applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stable_revision_tags ClouddeployDeliveryPipeline#stable_revision_tags}
        '''
        result = self._values.get("stable_revision_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a57e316ab76ede49dcda1a4ec022f0140d644f4ad4c847d4a7dc1226d65f2534)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ecb0d7ccc84a781a09e516ac5687bcdcedf9694b7e7bbff860f6ffbd892b8b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticTrafficControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="canaryRevisionTags")
    def canary_revision_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "canaryRevisionTags"))

    @canary_revision_tags.setter
    def canary_revision_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2481ba56ecae35c1f813e5bcdefbfd10d75dbae79f92378d2a0769ec95956cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canaryRevisionTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priorRevisionTags")
    def prior_revision_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "priorRevisionTags"))

    @prior_revision_tags.setter
    def prior_revision_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f88122631037c4f3460d33d6b1c0f627731afcbb5fb37fb8d4fe0db5b20645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priorRevisionTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stableRevisionTags")
    def stable_revision_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stableRevisionTags"))

    @stable_revision_tags.setter
    def stable_revision_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c15ddcb2bd827110e82171156ab4a2736dc28db8f4a16e2bf8c34e833ab890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stableRevisionTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6aa7727d81837d6eee51c440d0b39ab86a69be502ee9aacaf998286302becb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_service_mesh": "gatewayServiceMesh",
        "service_networking": "serviceNetworking",
    },
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes:
    def __init__(
        self,
        *,
        gateway_service_mesh: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        service_networking: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gateway_service_mesh: gateway_service_mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#gateway_service_mesh ClouddeployDeliveryPipeline#gateway_service_mesh}
        :param service_networking: service_networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service_networking ClouddeployDeliveryPipeline#service_networking}
        '''
        if isinstance(gateway_service_mesh, dict):
            gateway_service_mesh = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh(**gateway_service_mesh)
        if isinstance(service_networking, dict):
            service_networking = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking(**service_networking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed9128e437978ba8be3ca972b3c42bc042021f03babf80329cbc0474c15ce00)
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
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh"]:
        '''gateway_service_mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#gateway_service_mesh ClouddeployDeliveryPipeline#gateway_service_mesh}
        '''
        result = self._values.get("gateway_service_mesh")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh"], result)

    @builtins.property
    def service_networking(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking"]:
        '''service_networking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service_networking ClouddeployDeliveryPipeline#service_networking}
        '''
        result = self._values.get("service_networking")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh",
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
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh:
    def __init__(
        self,
        *,
        deployment: builtins.str,
        http_route: builtins.str,
        service: builtins.str,
        pod_selector_label: typing.Optional[builtins.str] = None,
        route_destinations: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations", typing.Dict[builtins.str, typing.Any]]] = None,
        route_update_wait_time: typing.Optional[builtins.str] = None,
        stable_cutback_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment: Required. Name of the Kubernetes Deployment whose traffic is managed by the specified HTTPRoute and Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#deployment ClouddeployDeliveryPipeline#deployment}
        :param http_route: Required. Name of the Gateway API HTTPRoute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#http_route ClouddeployDeliveryPipeline#http_route}
        :param service: Required. Name of the Kubernetes Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service ClouddeployDeliveryPipeline#service}
        :param pod_selector_label: Optional. The label to use when selecting Pods for the Deployment and Service resources. This label must already be present in both resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#pod_selector_label ClouddeployDeliveryPipeline#pod_selector_label}
        :param route_destinations: route_destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#route_destinations ClouddeployDeliveryPipeline#route_destinations}
        :param route_update_wait_time: Optional. The time to wait for route updates to propagate. The maximum configurable time is 3 hours, in seconds format. If unspecified, there is no wait time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#route_update_wait_time ClouddeployDeliveryPipeline#route_update_wait_time}
        :param stable_cutback_duration: Optional. The amount of time to migrate traffic back from the canary Service to the original Service during the stable phase deployment. If specified, must be between 15s and 3600s. If unspecified, there is no cutback time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stable_cutback_duration ClouddeployDeliveryPipeline#stable_cutback_duration}
        '''
        if isinstance(route_destinations, dict):
            route_destinations = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations(**route_destinations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b28c4e966f3da33d39457fe902acbce5c1ea82a207670446d7125949664b90)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#deployment ClouddeployDeliveryPipeline#deployment}
        '''
        result = self._values.get("deployment")
        assert result is not None, "Required property 'deployment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_route(self) -> builtins.str:
        '''Required. Name of the Gateway API HTTPRoute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#http_route ClouddeployDeliveryPipeline#http_route}
        '''
        result = self._values.get("http_route")
        assert result is not None, "Required property 'http_route' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. Name of the Kubernetes Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service ClouddeployDeliveryPipeline#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pod_selector_label(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The label to use when selecting Pods for the Deployment and Service resources. This label must already be present in both resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#pod_selector_label ClouddeployDeliveryPipeline#pod_selector_label}
        '''
        result = self._values.get("pod_selector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_destinations(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations"]:
        '''route_destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#route_destinations ClouddeployDeliveryPipeline#route_destinations}
        '''
        result = self._values.get("route_destinations")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations"], result)

    @builtins.property
    def route_update_wait_time(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The time to wait for route updates to propagate. The maximum configurable time is 3 hours, in seconds format. If unspecified, there is no wait time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#route_update_wait_time ClouddeployDeliveryPipeline#route_update_wait_time}
        '''
        result = self._values.get("route_update_wait_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stable_cutback_duration(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The amount of time to migrate traffic back from the canary Service to the original Service during the stable phase deployment. If specified, must be between 15s and 3600s. If unspecified, there is no cutback time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stable_cutback_duration ClouddeployDeliveryPipeline#stable_cutback_duration}
        '''
        result = self._values.get("stable_cutback_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__364712597d94972671c289de14471beccf5efe4091347b6d5a153d9de881c9dd)
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
        :param destination_ids: Required. The clusters where the Gateway API HTTPRoute resource will be deployed to. Valid entries include the associated entities IDs configured in the Target resource and "@self" to include the Target cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#destination_ids ClouddeployDeliveryPipeline#destination_ids}
        :param propagate_service: Optional. Whether to propagate the Kubernetes Service to the route destination clusters. The Service will always be deployed to the Target cluster even if the HTTPRoute is not. This option may be used to facilitiate successful DNS lookup in the route destination clusters. Can only be set to true if destinations are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#propagate_service ClouddeployDeliveryPipeline#propagate_service}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations(
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
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference", jsii.get(self, "routeDestinations"))

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
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations"], jsii.get(self, "routeDestinationsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f3bb1aa50fc68ef28cae5e9c3e17f495cb54ba95234eecd5d4818d937aeabc75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpRoute")
    def http_route(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpRoute"))

    @http_route.setter
    def http_route(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7859ce09cfc23d8e461e7603c2938024c9eb6bdccbfe7c6f590369ec5989c239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpRoute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podSelectorLabel")
    def pod_selector_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podSelectorLabel"))

    @pod_selector_label.setter
    def pod_selector_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba55502c12ca415aa252d4c1d8da1f5f5f400d04ba22fa16311a79e0ab03d874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podSelectorLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeUpdateWaitTime")
    def route_update_wait_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeUpdateWaitTime"))

    @route_update_wait_time.setter
    def route_update_wait_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ece407dfc77d8e9506a4d911308027989d78af40d2423e5a33ebf64888a964d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeUpdateWaitTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37985640589a17ea7aeaa8fab2b54a9ced578a47667091619eb31d3779d66469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stableCutbackDuration")
    def stable_cutback_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stableCutbackDuration"))

    @stable_cutback_duration.setter
    def stable_cutback_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3833c244b862da1aebc19a5986ce6151d98c9e036cfa9ead75f9621207e0627a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stableCutbackDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4355cc4b8bfc1cc4142c2c61da2845cd695b1710468a9f6af5a41703d229ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations",
    jsii_struct_bases=[],
    name_mapping={
        "destination_ids": "destinationIds",
        "propagate_service": "propagateService",
    },
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations:
    def __init__(
        self,
        *,
        destination_ids: typing.Sequence[builtins.str],
        propagate_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_ids: Required. The clusters where the Gateway API HTTPRoute resource will be deployed to. Valid entries include the associated entities IDs configured in the Target resource and "@self" to include the Target cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#destination_ids ClouddeployDeliveryPipeline#destination_ids}
        :param propagate_service: Optional. Whether to propagate the Kubernetes Service to the route destination clusters. The Service will always be deployed to the Target cluster even if the HTTPRoute is not. This option may be used to facilitiate successful DNS lookup in the route destination clusters. Can only be set to true if destinations are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#propagate_service ClouddeployDeliveryPipeline#propagate_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7195c90b1b72739b67e6cdb56e10ec4332ddd79e8ae33677340830028b7994e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#destination_ids ClouddeployDeliveryPipeline#destination_ids}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#propagate_service ClouddeployDeliveryPipeline#propagate_service}
        '''
        result = self._values.get("propagate_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0545bc5932e4b873c1d2878ee56b97cea9b423663880fb8dc9a8f3d634ed08bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cea30ea8522f7ffc3b40a1de457e136340e8477c8ef7c70559aa4522cd394d0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec603ab1f8aed908b0d87085d7100b348061c1c783586b3e0ec6020ce2c1ea3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagateService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94abf342e5a443fd5e46891eff6136575110070364c297443b8e29b80ea7eda7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc3fa076a568e7d09c99ee522fc52d685695c97d244a0db879f41aad48a27217)
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
        route_destinations: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations, typing.Dict[builtins.str, typing.Any]]] = None,
        route_update_wait_time: typing.Optional[builtins.str] = None,
        stable_cutback_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment: Required. Name of the Kubernetes Deployment whose traffic is managed by the specified HTTPRoute and Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#deployment ClouddeployDeliveryPipeline#deployment}
        :param http_route: Required. Name of the Gateway API HTTPRoute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#http_route ClouddeployDeliveryPipeline#http_route}
        :param service: Required. Name of the Kubernetes Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service ClouddeployDeliveryPipeline#service}
        :param pod_selector_label: Optional. The label to use when selecting Pods for the Deployment and Service resources. This label must already be present in both resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#pod_selector_label ClouddeployDeliveryPipeline#pod_selector_label}
        :param route_destinations: route_destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#route_destinations ClouddeployDeliveryPipeline#route_destinations}
        :param route_update_wait_time: Optional. The time to wait for route updates to propagate. The maximum configurable time is 3 hours, in seconds format. If unspecified, there is no wait time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#route_update_wait_time ClouddeployDeliveryPipeline#route_update_wait_time}
        :param stable_cutback_duration: Optional. The amount of time to migrate traffic back from the canary Service to the original Service during the stable phase deployment. If specified, must be between 15s and 3600s. If unspecified, there is no cutback time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stable_cutback_duration ClouddeployDeliveryPipeline#stable_cutback_duration}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh(
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
        :param deployment: Required. Name of the Kubernetes Deployment whose traffic is managed by the specified Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#deployment ClouddeployDeliveryPipeline#deployment}
        :param service: Required. Name of the Kubernetes Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service ClouddeployDeliveryPipeline#service}
        :param disable_pod_overprovisioning: Optional. Whether to disable Pod overprovisioning. If Pod overprovisioning is disabled then Cloud Deploy will limit the number of total Pods used for the deployment strategy to the number of Pods the Deployment has on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#disable_pod_overprovisioning ClouddeployDeliveryPipeline#disable_pod_overprovisioning}
        :param pod_selector_label: Optional. The label to use when selecting Pods for the Deployment resource. This label must already be present in the Deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#pod_selector_label ClouddeployDeliveryPipeline#pod_selector_label}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking(
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
    ) -> ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference:
        return typing.cast(ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference, jsii.get(self, "gatewayServiceMesh"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworking")
    def service_networking(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference", jsii.get(self, "serviceNetworking"))

    @builtins.property
    @jsii.member(jsii_name="gatewayServiceMeshInput")
    def gateway_service_mesh_input(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh], jsii.get(self, "gatewayServiceMeshInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkingInput")
    def service_networking_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking"], jsii.get(self, "serviceNetworkingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb9c805f8f5e7675ba9e56ff79f63ac86a9800cd9944ad16ddbe955b0ab5770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking",
    jsii_struct_bases=[],
    name_mapping={
        "deployment": "deployment",
        "service": "service",
        "disable_pod_overprovisioning": "disablePodOverprovisioning",
        "pod_selector_label": "podSelectorLabel",
    },
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking:
    def __init__(
        self,
        *,
        deployment: builtins.str,
        service: builtins.str,
        disable_pod_overprovisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pod_selector_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment: Required. Name of the Kubernetes Deployment whose traffic is managed by the specified Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#deployment ClouddeployDeliveryPipeline#deployment}
        :param service: Required. Name of the Kubernetes Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service ClouddeployDeliveryPipeline#service}
        :param disable_pod_overprovisioning: Optional. Whether to disable Pod overprovisioning. If Pod overprovisioning is disabled then Cloud Deploy will limit the number of total Pods used for the deployment strategy to the number of Pods the Deployment has on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#disable_pod_overprovisioning ClouddeployDeliveryPipeline#disable_pod_overprovisioning}
        :param pod_selector_label: Optional. The label to use when selecting Pods for the Deployment resource. This label must already be present in the Deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#pod_selector_label ClouddeployDeliveryPipeline#pod_selector_label}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d63b5396698fdaa275dc2c582e54f79f7e8089d463f5f0449891f7a9dadc3cf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#deployment ClouddeployDeliveryPipeline#deployment}
        '''
        result = self._values.get("deployment")
        assert result is not None, "Required property 'deployment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''Required. Name of the Kubernetes Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service ClouddeployDeliveryPipeline#service}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#disable_pod_overprovisioning ClouddeployDeliveryPipeline#disable_pod_overprovisioning}
        '''
        result = self._values.get("disable_pod_overprovisioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pod_selector_label(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The label to use when selecting Pods for the Deployment resource. This label must already be present in the Deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#pod_selector_label ClouddeployDeliveryPipeline#pod_selector_label}
        '''
        result = self._values.get("pod_selector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7db2dfc9139f713e9416195f1703453daa4eaf0972726a365725bf3b7ae27588)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57892a5c68c4ff3de910754b5a014126f35bc26891fb1a72e7803149d3ee1eeb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__602583ffdab6c8138ba7e939249cd9b13ef1e9ce4320d9d733aaa071430f4aae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePodOverprovisioning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podSelectorLabel")
    def pod_selector_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podSelectorLabel"))

    @pod_selector_label.setter
    def pod_selector_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f38cea316e5f827620918d797873399a390465b93871457b78666a5dfaf486a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podSelectorLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb42d498bab90d6e664664dc4054823d555ec32094ef53cf5907fadb501bfdd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3cc62906cf4e9d57bae8a25f4468776916fc9c3afb7a9777d3f0b7237121e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17cefe7268cf33d5df7563df59471872a74b13f9b6f39f63da5587d94fdc0cbb)
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
        :param automatic_traffic_control: Whether Cloud Deploy should update the traffic stanza in a Cloud Run Service on the user's behalf to facilitate traffic splitting. This is required to be true for CanaryDeployments, but optional for CustomCanaryDeployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#automatic_traffic_control ClouddeployDeliveryPipeline#automatic_traffic_control}
        :param canary_revision_tags: Optional. A list of tags that are added to the canary revision while the canary phase is in progress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary_revision_tags ClouddeployDeliveryPipeline#canary_revision_tags}
        :param prior_revision_tags: Optional. A list of tags that are added to the prior revision while the canary phase is in progress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#prior_revision_tags ClouddeployDeliveryPipeline#prior_revision_tags}
        :param stable_revision_tags: Optional. A list of tags that are added to the final stable revision when the stable phase is applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#stable_revision_tags ClouddeployDeliveryPipeline#stable_revision_tags}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun(
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
        gateway_service_mesh: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh, typing.Dict[builtins.str, typing.Any]]] = None,
        service_networking: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gateway_service_mesh: gateway_service_mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#gateway_service_mesh ClouddeployDeliveryPipeline#gateway_service_mesh}
        :param service_networking: service_networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#service_networking ClouddeployDeliveryPipeline#service_networking}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes(
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
    ) -> ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference:
        return typing.cast(ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference, jsii.get(self, "cloudRun"))

    @builtins.property
    @jsii.member(jsii_name="kubernetes")
    def kubernetes(
        self,
    ) -> ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference:
        return typing.cast(ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference, jsii.get(self, "kubernetes"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunInput")
    def cloud_run_input(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun], jsii.get(self, "cloudRunInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesInput")
    def kubernetes_input(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes], jsii.get(self, "kubernetesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d4d54f981d8ea0adb31a02c26530b305b4ff5a3825250393ceb341011efaf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8ee9054ffb165373c39cad35e26bea02331f38005045f3e950d035d956d32b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCanary")
    def put_canary(
        self,
        *,
        canary_deployment: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_canary_deployment: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_config: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param canary_deployment: canary_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#canary_deployment ClouddeployDeliveryPipeline#canary_deployment}
        :param custom_canary_deployment: custom_canary_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#custom_canary_deployment ClouddeployDeliveryPipeline#custom_canary_deployment}
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#runtime_config ClouddeployDeliveryPipeline#runtime_config}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary(
            canary_deployment=canary_deployment,
            custom_canary_deployment=custom_canary_deployment,
            runtime_config=runtime_config,
        )

        return typing.cast(None, jsii.invoke(self, "putCanary", [value]))

    @jsii.member(jsii_name="putStandard")
    def put_standard(
        self,
        *,
        postdeploy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#postdeploy ClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#predeploy ClouddeployDeliveryPipeline#predeploy}
        :param verify: Whether to verify a deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#verify ClouddeployDeliveryPipeline#verify}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard(
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
    ) -> ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference:
        return typing.cast(ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference, jsii.get(self, "canary"))

    @builtins.property
    @jsii.member(jsii_name="standard")
    def standard(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference", jsii.get(self, "standard"))

    @builtins.property
    @jsii.member(jsii_name="canaryInput")
    def canary_input(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary], jsii.get(self, "canaryInput"))

    @builtins.property
    @jsii.member(jsii_name="standardInput")
    def standard_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard"], jsii.get(self, "standardInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategy]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96674be6ed6059ba28d78010047bb7ad8548cb2ee330c76028d14089ad64570d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard",
    jsii_struct_bases=[],
    name_mapping={
        "postdeploy": "postdeploy",
        "predeploy": "predeploy",
        "verify": "verify",
    },
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard:
    def __init__(
        self,
        *,
        postdeploy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        predeploy: typing.Optional[typing.Union["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy", typing.Dict[builtins.str, typing.Any]]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param postdeploy: postdeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#postdeploy ClouddeployDeliveryPipeline#postdeploy}
        :param predeploy: predeploy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#predeploy ClouddeployDeliveryPipeline#predeploy}
        :param verify: Whether to verify a deployment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#verify ClouddeployDeliveryPipeline#verify}
        '''
        if isinstance(postdeploy, dict):
            postdeploy = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy(**postdeploy)
        if isinstance(predeploy, dict):
            predeploy = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy(**predeploy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8588b9a4c14a13e04b21c3d1283fd0c8ddb81e58c6471c6406e547ae74c318f4)
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
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy"]:
        '''postdeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#postdeploy ClouddeployDeliveryPipeline#postdeploy}
        '''
        result = self._values.get("postdeploy")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy"], result)

    @builtins.property
    def predeploy(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy"]:
        '''predeploy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#predeploy ClouddeployDeliveryPipeline#predeploy}
        '''
        result = self._values.get("predeploy")
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy"], result)

    @builtins.property
    def verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to verify a deployment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#verify ClouddeployDeliveryPipeline#verify}
        '''
        result = self._values.get("verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5a51401519c9cb53526ea4e31d3cf30bfbb058362701154ce1364fb964a7118)
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
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy(
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
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        value = ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy(
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
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference", jsii.get(self, "postdeploy"))

    @builtins.property
    @jsii.member(jsii_name="predeploy")
    def predeploy(
        self,
    ) -> "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference":
        return typing.cast("ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference", jsii.get(self, "predeploy"))

    @builtins.property
    @jsii.member(jsii_name="postdeployInput")
    def postdeploy_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy"], jsii.get(self, "postdeployInput"))

    @builtins.property
    @jsii.member(jsii_name="predeployInput")
    def predeploy_input(
        self,
    ) -> typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy"]:
        return typing.cast(typing.Optional["ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy"], jsii.get(self, "predeployInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b08b3727aeda51b0bc23619ca3fbc798246584b5d85eb9c72e4833afc5ab6b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed7c63b38ca06ce52183625c562a4a3a8f8f9b81319d3a107a685b27d6dd77c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139a7f96696b64073c10a290abb94660217f88c3092d3ce76f5aa18c4a0d7cd8)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the postdeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bad2c659f16339536041227e0fae4ffd4a65df39defff8c3bc1e14ad6ba01d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b68155c6fd5000440ea1ef8a94018042e7f1d52e5ec52a42fecb2da327f14b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cda0f666a4a56a5f39f3117c6592b26407b3e45056a3111652e8722b3e1d90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3296a6480131bb2da19144599442edf3c4d30c097e9ae77905287b929796a95)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. A sequence of skaffold custom actions to invoke during execution of the predeploy job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#actions ClouddeployDeliveryPipeline#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9fcd4e410d3d471a5fc78f344f4f475ffc986253412ab5c23a1ad789efdccee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d02f1a891539dab7220f6a000fa958d2f4d36ba5bdbffd8632196dfca138b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy]:
        return typing.cast(typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67177059fb02282ddcf8cc57364fa40c3679b07702a34933b16be6ce7efd601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ClouddeployDeliveryPipelineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#create ClouddeployDeliveryPipeline#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#delete ClouddeployDeliveryPipeline#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#update ClouddeployDeliveryPipeline#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0157f4128516dda135c2fcd7e21b84ded5da07f1e3a6916763111782c3e0dbaa)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#create ClouddeployDeliveryPipeline#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#delete ClouddeployDeliveryPipeline#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_delivery_pipeline#update ClouddeployDeliveryPipeline#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeliveryPipelineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeliveryPipelineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeliveryPipeline.ClouddeployDeliveryPipelineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d290f8419dbfcfe15f00546a82c877fdfcf13c956244608c7f67c00cf42a2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9e04736a09454e9796ec93424bfbccad4d4c380ff370ff2ea15832fc355c62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8133dfdc811dce83faa0569a7cae10864cff8a5fce7a0a7371aea11db8385cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c891764b48d1ee1ed1037df1488b7f4b42de73a73ace5fb00e49f13a7cd4e735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea5596f5102ba4752ea9ccb9c59198457a8bb286ca06781b4f410cd7bac1584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ClouddeployDeliveryPipeline",
    "ClouddeployDeliveryPipelineCondition",
    "ClouddeployDeliveryPipelineConditionList",
    "ClouddeployDeliveryPipelineConditionOutputReference",
    "ClouddeployDeliveryPipelineConditionPipelineReadyCondition",
    "ClouddeployDeliveryPipelineConditionPipelineReadyConditionList",
    "ClouddeployDeliveryPipelineConditionPipelineReadyConditionOutputReference",
    "ClouddeployDeliveryPipelineConditionTargetsPresentCondition",
    "ClouddeployDeliveryPipelineConditionTargetsPresentConditionList",
    "ClouddeployDeliveryPipelineConditionTargetsPresentConditionOutputReference",
    "ClouddeployDeliveryPipelineConditionTargetsTypeCondition",
    "ClouddeployDeliveryPipelineConditionTargetsTypeConditionList",
    "ClouddeployDeliveryPipelineConditionTargetsTypeConditionOutputReference",
    "ClouddeployDeliveryPipelineConfig",
    "ClouddeployDeliveryPipelineSerialPipeline",
    "ClouddeployDeliveryPipelineSerialPipelineOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStages",
    "ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters",
    "ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersList",
    "ClouddeployDeliveryPipelineSerialPipelineStagesDeployParametersOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesList",
    "ClouddeployDeliveryPipelineSerialPipelineStagesOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategy",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeployOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeployOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsList",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeployOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeployOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRunOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinationsOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworkingOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeployOutputReference",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy",
    "ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeployOutputReference",
    "ClouddeployDeliveryPipelineTimeouts",
    "ClouddeployDeliveryPipelineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f9f6d2becf637609069b5fd59e6eabe3ee22126543da43549222507d364a5f57(
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
    serial_pipeline: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipeline, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployDeliveryPipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6a4f486d8fa365334a44911795038912ee6d313ec21d3576e7c2c709b3c2f688(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dbf60e8a5ac661255863e1049b13f8c9ed51ea9c9f91a542c86291d687f559(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1711d99f755970aaa593fdf57e26e07f505363d1b9ef5ba80ff11d452c0344d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c01bb67dcc40c01314d098abe04287be8fa03ed445e92593f66973ce0300d0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e048057bfb254c65a694948ac37bbd05dd4ed6dadd095b521c0a8ae8d94e40a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3011a27cd565aaa8e6e01dfdee67dee4f8a3e427a571d3e8ff65a178d8d226c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3ca7cfe7606bf6997582151a4a7c73f086df28f5590ca0a085404af42ac678(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4d8d7c4e660eeb932856e1f5c18921c8a9f2ae686e65b08ab9248295f06f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b54e0ae79567d0a1f95ed9d83b2779a1714ebf246d86a80e2c515282b677b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c676f470c198c16fe06bcba673c843e04d78ca19aea9b4468e6a1bec559137(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94518569ccba9d1e9a20ec6ad6c4ce017ab430af45877d80409eb00b8562edc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228a43997ba4e5812fe6084e6e27950d8c067645078e1f2f6e12ae91cc5abf65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab31d7ec69007901a53ca1d3adb22e30f8513e368d63303f9431d3d2a224ef46(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bca1f9359f4a89383a34599e5e57f704a01f4e5f77f2ab92d8540c8bef0e46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249224777bcb676c4558918de946bec4c2562a5781fb3afeed163bf517f64e17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03579ca183e8567df8adba4ca2a7fc267505fef2f4133d67dfa9cfa335ebc6eb(
    value: typing.Optional[ClouddeployDeliveryPipelineCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91147f78840a38c9eab4720ed98de5d2a22be89d49c7965a001ce5ec00a5882(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae3d0af9f580d452814f80aadc4c4f03228fe7748e5633c8aa0b49e5fc3681a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f153a8a79486f3e88e7b42b2e1d98dd46288001b9a0eb7d6adf4f6297ed6109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b966011e0d4091d985b241572df925b04f665f4fe725ebaae305acb0649e8e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3be028be45426ca38f4d63e324c5539cc3f9681f5f76c1fd127adefc16ff09b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec2673c769495647b3bd70d860177115ed06e816a68012304df7d9efcfca925(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e2ff9d2b5c3225bc01adf05c1845355608a05c135bfad7f9f8ee757e6413e2(
    value: typing.Optional[ClouddeployDeliveryPipelineConditionPipelineReadyCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6423c36a5683aa05f1152f472b7d5cf94ba70962883944fec26910f7d084a888(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819b52da79e4b0e072217dccb2b1acbeb4ee6a22c1b220f29a433fb5ef9d695a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c9d287ecd9b9666ac5eb6440f4e21fb9f2a18bf7c22f01880068a5e6820869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78038831e64d108ab27f952c47e6ef3c3f79bbb097f6329bf68619b6065218f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b976f633c8fc26f6dcccc66274b4836cbaecb6dca87f9a1b3683cdcb6cf594d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b174696157bbeafb6d0150c3f73b1ce2e63a3174635d4d14f4dfb14476679128(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b7c211b73d3889603608cb698480d91d87e7d0b749d70ca1548048c9d5fd72(
    value: typing.Optional[ClouddeployDeliveryPipelineConditionTargetsPresentCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf50a5a007a598f8b3b8be570bbc5ce5146c699947eb85757b37e69dde0f92f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae434d6770e24dbfcac7a7cabdc529772f2d83bdceace62c0affa320c84c10e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40dd052c376c59e9772230dfbdf398a3fa5349b6b02248966b8d9c76b1fdd38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344182f27aa53f162c42ed6e771e8c35e2e04724f3fed6af3cebe299fca69230(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fb31221d62ae4b1a725417bde5b15c6feb3bb1de0c5d9fa562c2848476eff6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e5b67a1b79fca4e3c1d7b2604f853cda5fb86ba9627a26048bed16bbeb53e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afefd0e05208aa87f27dee80632c3cbb848ad1a9825a0e890948aeb764560cb7(
    value: typing.Optional[ClouddeployDeliveryPipelineConditionTargetsTypeCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7d420b3bb0d4dd1a78694afa730bbee29379b99845303e5bc49ebecdd7bd9e(
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
    serial_pipeline: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipeline, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployDeliveryPipelineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f21a0795432925fb1deaf3a6dfc41bb2919941f1850d453e799aefdf3a2bec(
    *,
    stages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd88821b0c6aeb0833497cd9c9bbbb0f97ebe51107e4f1f5f55ca7ee447afab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb6a235866b7cd7bb7a02498bdd3e467def5f539da1d78c279d7441405a8b95(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed600858b6536e2ea0c3e6eda6358fab3e979e549438121d171cc7a51fe2e66(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipeline],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e96264602fc4ef1c9f73a994ddd5179850d70f44fd32c3b8d2194016f8a673(
    *,
    deploy_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
    strategy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    target_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ed04fb8cfa07660e277a853b4efc0df635e1b6ad999a9a167bd3873b948f4c(
    *,
    values: typing.Mapping[builtins.str, builtins.str],
    match_target_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5984937e6299f3b74b6d5c446c627654b710585c9b78026aa3ea92187ca3028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9773fd125cec01d635c3d52bd6eb955e1a855bd42a7dc71a509352df627f5beb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ece48e562d879f85967887a310170476730e092143faaea55a289bdc8cdcc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887c42df025a4cdb68240a32d50f9331662440c7e0fd7f115b9bc150b8565864(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897e3e44a82b3c9bcfa35b358b0e1c07794a7ab9d5991bf102ecf294b6e684c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea355a1e002bdf92837bda9c535ff71f88ca114e58e1bca209178170326ca990(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484d4257d3a079650555cfe62853f3ecf18587897d34e0700e4f9302a511df73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c96b5c9426b1a9b0d53d46c49b228aff9d80962cff52587df918ebe62f91acd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8dab540ea8ca610c382daac6a653d08aa6f930ef3276cc21504edfff23bb9e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c063da0eeae93a62f7abbd628e36d95f3622cdeea91a3f1fd8e58a78346e9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4357803e10f270618d5debe61f902a3cd36d6c1398efc30017ebfd970a477f3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d34ba4422c28cdbdbe3f6d1ca842ac5fcff0cae411e9f0bda02663cc689c8ad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0523177180ab6b0f1f0a4ed9d2e119c5692e301f19fe022454480e2f1e6d805c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a704df71b3513cce64d17c7f8d09ca6b2aaad51a14334354b7e948b8408414(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ca4387c7a2689d2643b225b1e59eb01c562331147d3b73e378ecf9d748d95a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1879db875f649cf27c633ad262da4ef2a0a3adb6f05b0facb1ab5b489d5c76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747debe07a8d0ccffed772a06daa93d13d6480f1ce54332bb457fca9edfea539(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b3db53c7ba2b5de085f06f3901d19c1d71adc5ebdf9644fd68f9e2368fe916(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesDeployParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0931469831a0144c4c9427e224bb1d5eee3387a0eead523e7619dcb737ed176(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cfc3b7ce0140483ebef1f54a24f2afb4b088081d8c77b77c2506e60eca4ab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f37d84ebe1f48149f0393cb405233d3381ef41ecdde1515c788062bf9b33ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6279f6785178548ebbaf2b70aea55bb958a98a8c507a5ac8fc4fee99fdae451f(
    *,
    canary: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary, typing.Dict[builtins.str, typing.Any]]] = None,
    standard: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a207f5f44e4b037d6c4b07932f6ba916b2c682662a0a04266d78e650241ea99b(
    *,
    canary_deployment: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_canary_deployment: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_config: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54aee5fa0d1aed2b48111ee320d4221d3b09d417d08fc8db9733a1e3fcedc722(
    *,
    percentages: typing.Sequence[jsii.Number],
    postdeploy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    predeploy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe3e6c9196cf3fa8349c563ccb3226d2abeb6704e80f1e80ea8dd9d8c0e413c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035128ae9eb3674a034b016345d093e22c6c31a39ca7f1056565aae231bf0ef6(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75d728cdd55f5eb3260b6cce9f618317769c2a9891092db63ce865b683d6fde(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac3a437f6f4155da2409939c93370d64fb959679f5c5fac54d49f641dd18f96(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551c7bad9d6dc30ebf9ef1d36fdb0c33bf3f427b3284f5ecf89b8dee634b5f8c(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260fe1794033e37b5ef1e3780f1773b82e9b949b6f87b25b7a62e52dd81e8056(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad495084942bee533536f83aa6b7eaaad582e33236f23c57c0427ee0ededbbb6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bba7a8a8876f2094283cd5fd9188aee9b8082ff50af564462064302c3f7d22(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPostdeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962fdd029ab7fef0cc6669a84b295ec831305a33da811550673dca0b0207a1b2(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9465dddf2a23acdf86cabe74961a51236b9ce4ccc2a9c5c91f66aedb45acecfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7363c187f5d2041991e3d82ab3b5211dc25080c4cd633dced4773c8a5032a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830f5dca045f7a7fe49d891bc9131ba26001bdafa7e46ae71b7a460868d4f919(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCanaryDeploymentPredeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f76050263c1212bd65ef32fa43bd16e9dbc4af66896ad56b185aa8ed789aeb(
    *,
    phase_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2b705864461ab277d58b88a8db875faabe40946c6775634d8704c64317f224(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae2838c1a6431fcbe3670f657d38142353fac98b286e8411e95d286ec847452(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829034f821f401e8bff4994978f564853276aa180eca86cf03c4c359ddcff44a(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeployment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75ee60612b94cd86e95d689009a877ae24e44c5a8152b4d8798cde070f99ef0(
    *,
    percentage: jsii.Number,
    phase_id: builtins.str,
    postdeploy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    predeploy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    profiles: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44085d9cdcf980c0d790b6081a85d20b6674de73cf68c321af92e9ec3cf979aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed30341a1f5c990a8f46dcbe422309f87b01c28d745416f88acf16139437f575(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7613fc1239471f914d28d8905a3a423cf2f262aa1899960e36b19cebb5e931(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19284ed8eebbfce18c3db6425e4f567dde143b4be38312893aee1683db4f2354(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aba2c26fc00f8628f6b117c8b2d8a9af5b6ade74668629ed519fd7fb304d0fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af00c1bc611da3b2836b50f95ab031ff357bfd46397886ea949dadfbc1f3c2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3296919ab97f18b78d71f007e6538a7e1603c27d2291f050437331090be2030f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbfa19f885f80b4534020f92f222d3c36b89fecd66fd5f1b4258ab1ed5f7450(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e376c7d792bdfe740845c5cb0e281d8210832fbc6c909a33a109ddb51a9050(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439f8defa46f6abb0c0762cde27f71c7b6483cebafc40ce7a734e6e19b0a959c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07edce63bf3eac1f45b513f42a42ac207b8dcfb8704e548887fa73cc553aee30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ef587bf4fc807363253239b8a86456a4467ac99da35d147f6deb88c23d5512(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e31bbaa61d3064bfb2ad5494f2986914a2fdfdab6656227ec12d3ac435554e(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c274a50e73c6afa7784144974345d675166b56cdae69cb6de3156fa022e2fe1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85410580f9415f9f03a9136c6ac772719860cb13381f3f01a7ba299871f0550d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72857f9a7100935c6bfacc53124204d2a0eb3cc1132fdeb50b757ce43896b8a(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPostdeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d85996c5f1077ae36373f6122c7c0ce7027ac7d9b698f39c24e81c16493ad2c(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1019aa3a670073f87bfeae2b7dcf5e1ada05418136f041d556172a7a6e4f2c4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff56a99656cfd0851f33195b1f309fdce46ae5184a264a0f9ab58566e9a9866(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3edc7509c1f58e6643393ee032be92a9f35b0639eff34d4fbe0fe57c210f2d(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryCustomCanaryDeploymentPhaseConfigsPredeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17f7ed86e7eb760e0ac17289f41e953abbc0c074b28927a878713a39f20696d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f71979981dbd2cdbe27cc2ae891b1e3886a49600b4ff32ff81be8425b522ed9(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053e65bdfc776ca68b3221ca3ad417ca5938cc838e4c7a6463e1adfb6092cea3(
    *,
    cloud_run: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918ae210d81316b67a4d82dcfaf75f281dacaab9551da1e24f5ed4d96c6201fe(
    *,
    automatic_traffic_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    canary_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    prior_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    stable_revision_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57e316ab76ede49dcda1a4ec022f0140d644f4ad4c847d4a7dc1226d65f2534(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecb0d7ccc84a781a09e516ac5687bcdcedf9694b7e7bbff860f6ffbd892b8b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2481ba56ecae35c1f813e5bcdefbfd10d75dbae79f92378d2a0769ec95956cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f88122631037c4f3460d33d6b1c0f627731afcbb5fb37fb8d4fe0db5b20645(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c15ddcb2bd827110e82171156ab4a2736dc28db8f4a16e2bf8c34e833ab890(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6aa7727d81837d6eee51c440d0b39ab86a69be502ee9aacaf998286302becb(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigCloudRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed9128e437978ba8be3ca972b3c42bc042021f03babf80329cbc0474c15ce00(
    *,
    gateway_service_mesh: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    service_networking: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b28c4e966f3da33d39457fe902acbce5c1ea82a207670446d7125949664b90(
    *,
    deployment: builtins.str,
    http_route: builtins.str,
    service: builtins.str,
    pod_selector_label: typing.Optional[builtins.str] = None,
    route_destinations: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations, typing.Dict[builtins.str, typing.Any]]] = None,
    route_update_wait_time: typing.Optional[builtins.str] = None,
    stable_cutback_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364712597d94972671c289de14471beccf5efe4091347b6d5a153d9de881c9dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bb1aa50fc68ef28cae5e9c3e17f495cb54ba95234eecd5d4818d937aeabc75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7859ce09cfc23d8e461e7603c2938024c9eb6bdccbfe7c6f590369ec5989c239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba55502c12ca415aa252d4c1d8da1f5f5f400d04ba22fa16311a79e0ab03d874(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ece407dfc77d8e9506a4d911308027989d78af40d2423e5a33ebf64888a964d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37985640589a17ea7aeaa8fab2b54a9ced578a47667091619eb31d3779d66469(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3833c244b862da1aebc19a5986ce6151d98c9e036cfa9ead75f9621207e0627a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4355cc4b8bfc1cc4142c2c61da2845cd695b1710468a9f6af5a41703d229ba(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7195c90b1b72739b67e6cdb56e10ec4332ddd79e8ae33677340830028b7994e(
    *,
    destination_ids: typing.Sequence[builtins.str],
    propagate_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0545bc5932e4b873c1d2878ee56b97cea9b423663880fb8dc9a8f3d634ed08bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea30ea8522f7ffc3b40a1de457e136340e8477c8ef7c70559aa4522cd394d0d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec603ab1f8aed908b0d87085d7100b348061c1c783586b3e0ec6020ce2c1ea3b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94abf342e5a443fd5e46891eff6136575110070364c297443b8e29b80ea7eda7(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesGatewayServiceMeshRouteDestinations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3fa076a568e7d09c99ee522fc52d685695c97d244a0db879f41aad48a27217(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb9c805f8f5e7675ba9e56ff79f63ac86a9800cd9944ad16ddbe955b0ab5770(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d63b5396698fdaa275dc2c582e54f79f7e8089d463f5f0449891f7a9dadc3cf(
    *,
    deployment: builtins.str,
    service: builtins.str,
    disable_pod_overprovisioning: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pod_selector_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db2dfc9139f713e9416195f1703453daa4eaf0972726a365725bf3b7ae27588(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57892a5c68c4ff3de910754b5a014126f35bc26891fb1a72e7803149d3ee1eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602583ffdab6c8138ba7e939249cd9b13ef1e9ce4320d9d733aaa071430f4aae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f38cea316e5f827620918d797873399a390465b93871457b78666a5dfaf486a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb42d498bab90d6e664664dc4054823d555ec32094ef53cf5907fadb501bfdd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3cc62906cf4e9d57bae8a25f4468776916fc9c3afb7a9777d3f0b7237121e9(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfigKubernetesServiceNetworking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17cefe7268cf33d5df7563df59471872a74b13f9b6f39f63da5587d94fdc0cbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d4d54f981d8ea0adb31a02c26530b305b4ff5a3825250393ceb341011efaf3(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyCanaryRuntimeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ee9054ffb165373c39cad35e26bea02331f38005045f3e950d035d956d32b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96674be6ed6059ba28d78010047bb7ad8548cb2ee330c76028d14089ad64570d(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8588b9a4c14a13e04b21c3d1283fd0c8ddb81e58c6471c6406e547ae74c318f4(
    *,
    postdeploy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    predeploy: typing.Optional[typing.Union[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy, typing.Dict[builtins.str, typing.Any]]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a51401519c9cb53526ea4e31d3cf30bfbb058362701154ce1364fb964a7118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08b3727aeda51b0bc23619ca3fbc798246584b5d85eb9c72e4833afc5ab6b8b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed7c63b38ca06ce52183625c562a4a3a8f8f9b81319d3a107a685b27d6dd77c(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandard],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139a7f96696b64073c10a290abb94660217f88c3092d3ce76f5aa18c4a0d7cd8(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bad2c659f16339536041227e0fae4ffd4a65df39defff8c3bc1e14ad6ba01d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68155c6fd5000440ea1ef8a94018042e7f1d52e5ec52a42fecb2da327f14b20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cda0f666a4a56a5f39f3117c6592b26407b3e45056a3111652e8722b3e1d90a(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPostdeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3296a6480131bb2da19144599442edf3c4d30c097e9ae77905287b929796a95(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fcd4e410d3d471a5fc78f344f4f475ffc986253412ab5c23a1ad789efdccee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d02f1a891539dab7220f6a000fa958d2f4d36ba5bdbffd8632196dfca138b9d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67177059fb02282ddcf8cc57364fa40c3679b07702a34933b16be6ce7efd601(
    value: typing.Optional[ClouddeployDeliveryPipelineSerialPipelineStagesStrategyStandardPredeploy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0157f4128516dda135c2fcd7e21b84ded5da07f1e3a6916763111782c3e0dbaa(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d290f8419dbfcfe15f00546a82c877fdfcf13c956244608c7f67c00cf42a2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e04736a09454e9796ec93424bfbccad4d4c380ff370ff2ea15832fc355c62a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8133dfdc811dce83faa0569a7cae10864cff8a5fce7a0a7371aea11db8385cca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c891764b48d1ee1ed1037df1488b7f4b42de73a73ace5fb00e49f13a7cd4e735(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea5596f5102ba4752ea9ccb9c59198457a8bb286ca06781b4f410cd7bac1584(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeliveryPipelineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
